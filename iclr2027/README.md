# ContextGraph ICLR working paper

Read [main.pdf](main.pdf) or edit [main.tex](main.tex).

The paper studies history as a source of requirements missing from the current
issue. On Django 14404, ordinary repairs pass official verification but discard
query parameters. Supplying the same historical repair in the first call
preserves the required deployment prefix and query together, producing the same
method AST as a later history-guided revision with one generation call instead
of two. A second pytest case uses the same upfront-history procedure to repair
both skip levels in one call; the observed ordinary sequence needed a diagnostic
revision. These development comparisons motivate the simpler procedure in the paper.

Implementation and evidence in the parent repository:

- `scripts/analysis/run_direct_history_pilot_v1.py`
- `docs/reports/direct-history-v1.md`
- `results/verified_train_test_v1/direct-history-v1/evidence.json`
- `docs/reports/repair-residual-v1.md`
- `docs/reports/direct-history-pytest-v1.md`

Build:

~~~bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
~~~
