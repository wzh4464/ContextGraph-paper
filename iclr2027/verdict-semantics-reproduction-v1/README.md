# Frozen verifier status-comparison reproduction

This local anonymous supplement retains the six original 99-task Related-Lite
conditions. All 594 records remain: 292 empty predictions, 15 original verifier
setup failures, and 287 completed test-status comparisons. Original official
resolved labels and previous provenance exceptions are unchanged.

With Python 3.10 or later, run in this directory (standard library only):

```bash
uv run --no-project python reproduce.py
```

Optional `--out audit.json` writes the complete recomputed audit to a new file.
No tests, Docker operations, benchmark solvers, model calls or network requests
are executed. The frozen harness source is parsed as Python AST; only its pure
compare_results function and resolved Boolean expression are evaluated. Container
launch functions in that source are never run. The separate audit core is copied
byte-for-byte from the completed source audit.

Original test_output.txt/report.json bytes and the pinned dataset's test lists
are supplied in the compressed projection. These logs contain the harness's
recorded parsed test-status maps plus setup output; they are not complete raw
stdout/stderr for every test command. Replay checks the recorded map counts,
recomputes all 287 complete comparisons exactly, and joins receipt/report hashes
to the unchanged first-prediction audit. It does not reparse original runner
stdout or rerun tests. Empty submissions and setup failures remain explicitly
outside the complete-comparison count and inside the fixed record universe.

In this frozen Related-Lite harness, resolved requires all FAIL_TO_PASS tests
to pass; PASS_TO_PASS failures do not veto it. Four officially resolved original
predictions contain a recorded PASSED-to-FAILED PASS_TO_PASS test: Flat and Graph
on Django-34570, and Rules and Control on Django-33461. The original official
scores stay unchanged; this is a description of the criterion, not replacement
labels or an alternative memory-effect estimate.

PASS_TO_PASS success can also include unchanged nonpassing statuses. Across the
287 completed comparisons, 732 such prediction/test occurrences comprise 280
SKIPPED-to-SKIPPED, 151 FAILED-to-FAILED, and 301 MISSING-to-MISSING cases, spanning
36 predictions (12 officially resolved). These are repeated status occurrences,
not independent tests or proof that those tests executed successfully.

This package does not reconstruct the full Docker/runtime evidence, certify
report authenticity independently of the original bound records, or identify
causal memory effects. The previous Flat historical log exception, source-overlap
and adaptive-design limitations remain. Local Verified uses its own benchmark
and verifier; its outcomes are not included or redefined. Complete anonymous
experimental release and human review remain pending. No upload or submission
has occurred. Bounded decoded identifier/credential/path/email screening is not
a universal anonymity guarantee.
