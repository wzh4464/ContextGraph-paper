# ICLR 2027 research draft

`main.tex` is the current evidence-based working draft. The existing `../main.tex`
remains the historical NeurIPS-style preprint; its effect claims have not all been
revalidated and are not copied into this draft.

Existing Related-Lite Flat/Card reports record 18/99 each. An extended audit found
one appended Flat Docker log whose full-file hash no longer matches its receipt;
an independent frozen-verifier recheck of the unchanged prediction reproduces the
original failure and passes its evidence checks. The first-prediction outcomes are
unchanged, and the original provenance limitation remains disclosed. The new
Verified 350/150 experiment remains work in progress, with no
invented test score.

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

The archived paired-effect figure uses the already audited 99-task and 88-task
comparisons, with unadjusted paired bootstrap intervals. Its PDF, SVG and PNG are
in `figures/`; the adjacent JSON records exact plotted values, input/output hashes
and the plotting version. From the ContextGraph root, regenerate with:

```bash
uv run --no-project --with matplotlib==3.11.1 python scripts/analysis/plot_archived_paired_effects.py --source docs/reports/gfx-expanded-audit-20260906/paired-comparisons.json --out-dir paper/iclr2027/figures
```

The original Flat-reference plot excludes Control and local Verified results.
The current manuscript uses `figures/archived_effects_with_control.pdf`, which
adds the completed contemporaneous Control audit; its adjacent JSON binds the
six-arm comparisons. Neither figure includes the unfinished Verified campaign.

The September 6, 11:57 UTC Verified snapshot has two audited original results on
the first task (Control and Flat resolved), while Graph remains ungraded. These
partial receipts validate the analysis integration and do not form a success
rate or treatment effect. The full 150-task denominator remains fixed per arm.
