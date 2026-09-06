# Anonymous statistical reproduction draft

This local supplement recomputes the completed Related-Lite repair-outcome table
and paired-effect figure from 594 supplied first-prediction verdicts (six arms,
99 fixed tasks each). The full 99-task analysis and the historical 88-task
source-overlap sensitivity remain separate. All 18 comparisons reproduce exactly,
including discordant pairs, two-sided exact McNemar tests, 200,000-draw paired
percentile-bootstrap intervals (seed 42), and the stated retrospective Holm
families. Confidence intervals are unadjusted. The supplied statistical core is
byte-identical to the original analysis.

With Python 3.12 and uv installed, run in this directory:

```bash
uv run --no-project --with numpy==2.5.2 python reproduce.py
```

Dependencies can be installed in advance; the reproduction script uses no API,
SSH, Docker, credentials or network calls. Optional `--out results.json` writes
the recomputed tables to a new file. All input and code files are hash-checked.

The conditions are `gfx-control` (Control), `gfx-flat` (Flat), `gfx-skill` (Card),
`gfx-graph` (Graph), `gfx-rules` (Rules), and `gfx-loc` (File list). Original IDs,
failures, empty predictions and terminal labels are retained. Later successful
solver reruns never replace first predictions. `exit_cost` can denote a call cap
and does not establish a dollar-budget overrun.

The source audits check the frozen verifier evidence and join actual memory
delivery or Control absence to the same trajectory hashes before export. This
bundle reproduces statistics from those verdicts; it does not independently
re-execute the raw verifier or delivery audits. Source-audit, original prediction
and trajectory hashes are supplied without host paths. Full raw evidence, the
complete experimental environment and human author review remain outside this
draft statistical package.

Flat's matplotlib-23687 record retains its historical Docker-log hash exception.
An independent frozen-verifier recheck of the identical first prediction agrees
with its unresolved verdict. This preserves the outcome but does not reconstruct
the historical log. The row records both the exception and recheck provenance.

The archive reflects adaptive historical interventions and incomplete general
source-contamination evidence; these are exploratory operational comparisons,
not a clean confirmatory identification of a memory mechanism. Near-duplicate
sensitivity does not certify every leakage channel. The unfinished Verified
350/150 campaign and Card-v2 campaign contribute no outcomes to this package.

This is a local review draft. No upload or submission has been performed.
