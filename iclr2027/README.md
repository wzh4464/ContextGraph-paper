# ContextGraph ICLR working paper

Read [main.pdf](main.pdf) or edit [main.tex](main.tex).

The method question is which historical requirement an initial repair still
violates. On Django 14404, an initial repair and an issue-based revision pass
official verification but discard query parameters. A historical patch and an
executed source relation both produce the same revision, preserving the required
deployment prefix and the query string together. This establishes a corrective
contribution from memory; it does not establish a gain in official resolved rate
or an advantage of executable delivery over the patch.

Four source-blind candidates for Django 13343 already cover their historical
condition, illustrating when that relation adds no corrective signal. Both
cases use the development partition; the 150-task evaluation partition remains
unused by these pilots.

Implementation and evidence in the parent repository:

- `scripts/analysis/run_repair_residual_pilot_v1.py`
- `scripts/analysis/run_repair_candidate_pilot_v1.py`
- `docs/reports/repair-residual-v1.md`
- `docs/reports/repair-candidate-v1.md`

Build:

~~~bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
~~~
