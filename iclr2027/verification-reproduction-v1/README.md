# Original predictions and official report reproduction

This local anonymous review draft supplies all 594 original predictions across
the six completed Related-Lite conditions, retaining failures and empty patches.
The 302 nonempty predictions include original report.json, result.json and verified
patch.diff bytes. The 292 empty predictions retain the original empty-submission
short-circuit receipt fields; no test execution is claimed for those predictions.
Raw bytes are content-addressed and base64 encoded in projection.json.gz.

With Python 3.10 or later, run from this directory (standard library only):

```bash
uv run --no-project python reproduce.py
uv run --no-project python reproduce.py --predictions-dir predictions
```

The second command creates six 99-row JSONL prediction files. JSON serialization
may differ from the original .pred files, but every model_patch string is exact.
The raw original .pred bytes remain in the projection. No solver, verifier,
Docker, model, database or network call is made by either command.

Replay verifies original prediction and patch hashes against the existing audited
verdicts, compares both original official report representations using the original
report matcher, and checks every empty-prediction exemption. Every condition uses
the same frozen 99-task universe. Receipt projections are labelled explicitly:
they preserve selected original fields and the original receipt hash, not the full
receipt bytes. Similarly, selected evidence-manifest fields and its original hash
are supplied without private filesystem paths. Original test names in report bytes
are unchanged. All exported source files were hashed before and after collection;
trajectory hashes join the earlier audits, without rereading or exporting raw
trajectories in this collection.

The prior Flat matplotlib-23687 Docker-log hash exception remains in verdicts and
the replay output. Its first prediction and report still say unresolved; the
independent frozen-verifier recheck agrees. This package neither substitutes the
recheck outcome nor reconstructs the historical Docker log. No p1r outcomes replace
any original prediction.

This package makes original patches and report labels inspectable. It does not
rerun tests, reconstruct the complete runtime/Docker chain, establish report
authenticity without the separately bound private evidence, or demonstrate causal
memory effects. Test-output logs, complete runtime images, the anonymous execution
environment and human author review remain outside this draft. Existing source
overlap, adaptive design and image-lineage limitations continue to apply. The
unfinished Card-v2 and local Verified campaigns contribute no records here.

No external upload or submission has occurred. Identity, credential, home-path
and email patterns are checked on decoded raw artifacts and package members;
these bounded scans do not guarantee anonymity against every inference.
