# ICLR 2027 research draft

`main.tex` is the current evidence-based working draft. The existing `../main.tex`
remains the historical NeurIPS-style preprint; its effect claims have not all been
revalidated and are not copied into this draft.

The completed result is the Related-Lite Flat/Card audit: 18/99 each. The new
Verified 350/150 experiment is described as work in progress, with no invented test score.

The official [ICLR 2027 author guide](https://iclr.cc/Conferences/2027/AuthorGuidelines)
sets abstract and full-paper deadlines at September 18 and September 25, 2026,
23:59 AoE, respectively (Beijing: September 19 and September 26, 19:59).
Main text is limited to nine pages at submission. The downloaded official style
archive and individual files are pinned in `template-source.json`.

An AI-use section is included using the actual work performed; human review is
still pending, as stated in the draft. No paper or abstract has been submitted.

Build locally:

```bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
```

Tectonic 0.17.0 was installed from its official release. The draft is anonymous,
but the accompanying repository evidence still needs an anonymous release package
before external submission. `evidence-map.json` binds current claims to repository artifacts.
