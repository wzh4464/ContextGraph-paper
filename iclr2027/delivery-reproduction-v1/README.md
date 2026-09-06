# Anonymous memory-delivery reproduction draft

This local package reproduces recorded delivery checks across all 594 completed
Related-Lite first attempts (six conditions, 99 tasks each). It joins each
projected history to the identical trajectory hash in the audited verdict table.
No unfinished Verified or Card-v2 attempts are included.

With Python 3.12 and uv installed, run from this extracted directory:

```bash
uv run --no-project python reproduce.py
```

The program uses only the Python standard library and makes no service calls.
The compressed projection is checked against its original uncompressed hash.
It checks input/code hashes, all original task identities, each reconstructed
census record, and the reported totals. Original memory and Control classifier
functions are copied verbatim; their complete source-file hashes are retained.

The expected totals are Control 99/99 with no enumerated direct memory exposure;
Flat 99/99 served; Card 99/99 served with the correct frozen repository card in
98/99; Graph 99/99 served; Rules 95/99 served; File list 96/99 served. All five
memory conditions have zero observed phase refusals. Wrong-card routing,
abstentions and missing responses remain visible; no task is removed.

Every original history position is preserved in order. All assistant function
names/IDs remain; memory-call arguments and matching tool-response contents are
retained. For Control, all recorded system messages, the first user prompt and
assistant actions are retained. Other message content is omitted because the
original classifiers do not inspect it. Card records contain the exact expected
card text drawn from the frozen file. The projection exporter is included.
The private original trajectories were hashed before and after projection and
matched the existing audit; this export does not alter their underlying files.
Generic home-directory path matches were traced to exact spans of the frozen
public issue text. These benchmark tracebacks remain unchanged; their separate
review records the task IDs, statement hashes and counts. Experiment author/host
identifiers and token patterns are still rejected. This narrow scan does not
guarantee anonymity against every possible inference.

This is a reproduction of the original classifiers over selected recorded fields,
not a guarantee of memory usefulness, semantic correctness, causal mechanism or
absence of unrecorded/pretraining knowledge. Shell detection follows the original
pattern and can miss unsupported invocation forms. Memory delivery does not
establish repair success. The unchanged statistical verdict table is supplied
to verify the trajectory join, not to redefine outcomes or select successful tasks.

Debug logs and official verifier execution are outside this package. In
particular, the reported rate-limit log census is not re-executed here, so this
package does not independently reproduce every part of the original service
gate. Source audit and response hashes are retained. The complete experimental
release and human author review remain pending. No external upload has occurred.
