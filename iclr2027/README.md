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

Complete-agent comparisons additionally examine query preservation, redundant
uniqueness, and source/destination timezone requirements. A further redirect
comparison finds that one generated requirement sentence elicits the same patch
as the sentence plus its executable check and failed observations.
The six-task Qwen cohort has identical official success in both arms; two cases
show added historical behavior. A newer matched-representation pair on Django
16819 instead produces the same semantic regression in both arms: replacing a
same-name index with different columns is incorrectly optimized away, despite
official success. The draft now includes this concrete limit of the procedure.

Implementation and evidence in the parent repository:

- `scripts/analysis/run_direct_history_pilot_v1.py`
- `docs/reports/direct-history-v1.md`
- `results/verified_train_test_v1/direct-history-v1/evidence.json`
- `docs/reports/repair-residual-v1.md`
- `docs/reports/direct-history-pytest-v1.md`
- `docs/reports/qwen-close-history-pairs-launch-20260908.md`
- `docs/reports/requirement-representation-redirect-20260908.md`
- `docs/reports/index-reduction-semantics-20260908.md`

Build:

~~~bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
~~~
