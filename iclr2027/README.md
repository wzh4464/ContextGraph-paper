# ContextGraph ICLR working paper

The research question is whether a past repair's **observable effect** can
identify useful observations for the next repair. The implemented source
construction generates an executable check and runs it before and after the
historical patch. Using that relation to guide a target repair remains an
unresolved method step.

Read [main.pdf](main.pdf) or edit [main.tex](main.tex).

The earlier 99-task Related-Lite comparison resolves 17 tasks without memory,
18 with flat patches, and 18 with an added procedure card. In a separate
Verified development pilot, both successful applicability repairs also occur
without memory, with identical patches. Those repairs therefore do not require
historical content.

An automatically generated rendering check captures the Matplotlib 23314
source repair: two inputs produce 57,600 and 40,000 non-background pixels before
the patch, and zero afterward. This establishes a source contrast, not target
use of that contrast.

The completed Matplotlib 20826 comparison used the same solver, applicability
instruction, and budget. The original-patch arm used 32 calls ($3.109032), the
effect-check arm 34 ($3.011330), and no memory 33 ($3.031290). All reached the
cost threshold without production-code edits and submitted empty patches,
immediately recorded as unresolved by the official verifier. The effect-check
arm did not adapt and execute the source rendering relation. Thus this trial
tested supplying check text; it did not execute a target-transfer algorithm.
Three unresolved outcomes establish neither equivalence nor that source checks
are ineffective. Expansion of this text-delivery prototype is stopped.

Matplotlib 20826 belongs to Verified's 70-task development partition. These
pilots do not use the separate 150-task evaluation partition.

Implementation in the parent repository:

- `scripts/analysis/run_repair_check_source_v1.py`
- `scripts/analysis/run_repair_effect_pilot_v1.py`
- `experiments/ab_test/repair_checks.py`

Build:

~~~bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
~~~
