# Original methods from SWE-agent, MIT license; see SWE-agent-LICENSE.
# Revision: a15c8ffb344a2c314728e52280ffc1bc5fcfd094
from __future__ import annotations

def _get_content_text(entry: HistoryItem) -> str:
    if isinstance(entry["content"], str):
        return entry["content"]
    assert len(entry["content"]) == 1, "Expected single message in content"
    return entry["content"][0]["text"]


def _set_content_text(entry: HistoryItem, text: str) -> None:
    if isinstance(entry["content"], str):
        entry["content"] = text
    else:
        assert len(entry["content"]) == 1, "Expected single message in content"
        entry["content"][0]["text"] = text


class ReplayProcessor:
    """Configuration adapter; the two processing methods below are verbatim."""
    def __init__(self, config):
        expected = {'n': 5, 'polling': 1, 'type': 'last_n_observations',
                    'always_keep_output_for_tags': ['keep_output'],
                    'always_remove_output_for_tags': ['remove_output']}
        if config != expected:
            raise ValueError('Different saved processor configuration')
        self.n = config['n']
        self.polling = config['polling']
        self.always_keep_output_for_tags = set(config['always_keep_output_for_tags'])
        self.always_remove_output_for_tags = set(config['always_remove_output_for_tags'])

    def _get_omit_indices(self, history: History) -> list[int]:
        observation_indices = [
            idx
            for idx, entry in enumerate(history)
            if entry.get("message_type") == "observation" and not entry.get("is_demo", False)
        ]
        last_removed_idx = max(0, (len(observation_indices) // self.polling) * self.polling - self.n)
        # Note: We never remove the first observation, as it is the instance template
        return observation_indices[1:last_removed_idx]

    def __call__(self, history: History) -> History:
        new_history = []
        omit_content_idxs = self._get_omit_indices(history)
        for idx, entry in enumerate(history):
            tags = set(entry.get("tags", []))
            if ((idx not in omit_content_idxs) or (tags & self.always_keep_output_for_tags)) and not (
                tags & self.always_remove_output_for_tags
            ):
                new_history.append(entry)
            else:
                data = entry.copy()
                assert data.get("message_type") == "observation", (
                    f"Expected observation for dropped entry, got: {data.get('message_type')}"
                )
                text = _get_content_text(data)
                _set_content_text(data, f"Old environment output: ({len(text.splitlines())} lines omitted)")
                new_history.append(data)
        return new_history
