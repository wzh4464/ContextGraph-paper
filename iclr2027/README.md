# ContextGraph ICLR working paper

Read [main.pdf](main.pdf) or edit [main.tex](main.tex).

The method turns a source repair's observable effect into an executed target
diagnostic. A source writer generates a relation check from the patch and
repaired code. A target writer binds that relation to the current task; the
repair solver receives the probe and its actual observations.

The completed Django development comparison establishes this execution path.
The source-informed diagnostic adds a default-storage boundary, but both it and
the issue-only procedure produce officially resolved repairs. Both patches also
pass the unchanged source check on that boundary. Total target writer and solver
costs are $3.059602 and $2.558255, respectively, under the experiment's meter.

The resulting insight is that a distinct observation need not change the repair
decision. The next method question is how to select source relations that
distinguish candidate edits. The current result does not demonstrate a repair
gain from memory.

Source Django 16493 belongs to the 280-task memory bank; target Django 13343
belongs to the separate 70-task development partition. The 150-task evaluation
partition is unused by this pilot.

Implementation in the parent repository:

- `scripts/analysis/run_repair_check_source_v1.py`
- `scripts/analysis/build_executed_probe_v1.py`
- `scripts/analysis/run_executed_probe_pilot_v1.py`
- `scripts/analysis/replay_executed_probe_relation_v1.py`

Results: `docs/reports/executed-probe-pilot-v1.md` in the parent repository.

Build:

~~~bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
~~~
