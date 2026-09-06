# Separate adaptive Card-v2 statistical reproduction draft

This package supplies all 297 original verdicts for Flat, Card-v1 and Card-v2
on the same fixed 99-task Related-Lite manifest. It recomputes the two fixed
comparisons against Card-v2 and their same historical 88-task sensitivity:
discordant pairs, exact two-sided McNemar tests, Holm correction within each
two-comparison family, and unadjusted paired percentile-bootstrap intervals
(200,000 draws, seed 42). Its statistical core is byte-identical to the original.

With Python 3.12 and uv, run here:

```bash
uv run --no-project --with numpy==2.5.0 python reproduce.py
```

Dependencies may be installed beforehand. The script itself uses no API, SSH,
Docker or network calls and checks all supplied file hashes. Optional
`--out results.json` writes the recomputed tables to a new file.

Card-v2 resolves 16/99, versus 18/99 in each reference condition. All original
failures and empty submissions are retained. The historical exclusion list
leaves 16/88, 18/88 and 15/88 for Card-v2, Flat and Card-v1 respectively; it never
replaces the primary denominator. No later solver attempt is substituted.

This is an adaptive revision informed by the same historical tasks. Its
completion analysis plan was attached after the arm started and partial
outcomes were visible. Correction within two comparisons does not account for
that broader adaptive selection or establish a confirmatory causal claim.
Flat's historical appended-log exception and independent unchanged-prediction
recheck remain recorded. These verdict statistics do not rerun verification,
prove memory usefulness or certify general source independence.

Card-v2's separately checked delivery reaches 97/99 with the exact repository
card, satisfying the registered 95% threshold. Its 39 hard exit_cost labels fail
the registered maximum of 32; labels can represent a call cap. Other process
proxies are not certified by this statistical package.

The earlier six-condition statistical bundle remains unchanged. This package
does not pool the separate Verified 350/150 campaign or certify a complete
anonymous execution environment. It is a local review draft; no upload or
submission has occurred.
