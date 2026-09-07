# ContextGraph ICLR working paper

The paper now centers on **when a repair experience applies** and how a coding
agent can test that condition before choosing an edit.

Read [main.pdf](main.pdf) or edit [main.tex](main.tex). The method is a development
candidate; the completed Related-Lite scores motivate it and do not measure its
benefit.

The argument has three parts:

1. Relevant historical advice can prescribe an unsuitable action when input,
   runtime, or program state changes.
2. A memory-guided check can distinguish those situations before editing.
3. The method should improve verified repairs at the same total budget, with
   trajectories showing which observations changed the agent's decisions.

The local applicability pilot uses two queries from the 70-task development
partition within Verified's 350 training tasks. Both conditions receive the
identical persistent Graph packet from the 280-source bank. The intervention
adds a policy requesting at most two discriminating checks before editing.
This first prototype is a solver instruction, not an enforced gate or a learned
classifier. The ordinary and applicability conditions use the same model,
tools, images, 100-call limit and $3 budget threshold.

All four runs completed: the instruction arm resolved both tasks; ordinary
memory produced two empty patches. The instruction arm first edited source at
actions 19 and 10, while neither ordinary run edited source. This suggests a
change in how the agent moves from diagnosis to editing, without establishing
that a particular historical source supplied the decisive information.
Two follow-up runs kept the same instruction and removed only the memory packet.
Both also resolved, producing exactly the same patches in 30 and 34 calls.
The instruction-only prototype will not be expanded as a memory method.
The next candidate asks whether the behavior changed by a source repair selects
more useful transferable checks; a real Django source check is working, while
automatic extraction and target transfer remain untested.
The parent repository's `docs/reports/applicability-pilot-v1.md` records the
development result and the decision this comparison will inform.

Pilot implementation in the parent repository:

- experiments/ab_test/applicability.py
- scripts/analysis/run_applicability_pilot_v1.py
- configs/verified_train_test_v1/applicability-pilot-v1/
- results/verified_train_test_v1/applicability-pilot-v1/

Every prediction is verified immediately. A single worker runs the pilot;
trajectory snapshots are recorded every ten minutes for inspection.

Five audit appendices, operational chronology, and the audit-procedure
contribution have been removed from the manuscript. Existing raw records and
reproduction packages remain available for the completed results.
[evidence-map.json](evidence-map.json) is the historical evidence catalog; many
of its claims no longer appear in the active paper. The previous audit-oriented
draft is retained by Git at commit 139df9f.

Build:

~~~bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
~~~

No abstract or paper has been submitted. Human review remains pending.
