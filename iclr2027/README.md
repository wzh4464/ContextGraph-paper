# ContextGraph ICLR working paper

The method under development stores a past repair as an **executable check of
its observable effect**. Source execution confirms what changed; target
execution asks whether that behavior helps choose the current repair.

Read [main.pdf](main.pdf) or edit [main.tex](main.tex).

Current evidence:

- The earlier 99-task Related-Lite comparison resolves 17 tasks without memory,
  18 with flat patches, and 18 with an added procedure card.
- Six Verified development runs show that the two successful applicability
  repairs also occur without memory, with identical patches. This rejects
  expanding the instruction-only prototype as the memory method.
- Four checks generated from fixed Matplotlib code miss its repaired branch.
  An automatically generated rendering check, with one model correction of an
  invalid API call, exposes the source effect: 57,600 / 40,000 non-background
  pixels before the patch, zero afterward. An internal-cache check was excluded
  from transfer because the target API has no corresponding cache.

The new development comparison gives the same target solver the original
source patch, the executable effect check, or no memory. Its target is
Matplotlib 20826 in Verified’s 70-task development partition. The 150-task
Verified evaluation partition remains separate. Target outcomes are pending.

Implementation in the parent repository:

- `scripts/analysis/run_repair_check_source_v1.py`
- `scripts/analysis/run_repair_effect_pilot_v1.py`
- `experiments/ab_test/repair_checks.py`

Each target prediction is verified immediately; trajectories are reviewed every
ten minutes. The target comparison uses one worker and a shared task budget.

Build:

~~~bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
~~~
