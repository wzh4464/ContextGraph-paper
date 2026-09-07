# Anonymous patch-overlap reproduction draft

This package replays all 693 original Related-Lite records (seven conditions,
99 tasks each) and all 28,809 pairs of 291 source patches with 99 target patches.
From this directory, run:

```bash
uv run --no-project python -I -S -B reproduce.py
```

Only the Python standard library is needed. No service, model, solver or verifier
is called. The package checks every file hash and compares the full computed
pair/record results, not just aggregate counts. The original overlap functions
are preserved in `overlap_core.py`; only its replay function is called.

Features are SHA256 sets of normalized added lines, normalized signed changes,
and file/sign/exact nonblank changed-line bodies. The first text screen uses
nonblank lines starting with +, excluding +++ headers. Separate hunk parsing
avoids diff headers and test-hint prose, retains indentation for file-aware
features, and records interrupted hunks. Set similarity ignores order and
multiplicity; whitespace normalization hides indentation differences.

The pinned target patch for Sympy-27868 fails both hunk parsing and Git's read-only
patch syntax check. It remains in every fixed universe: its text-screen values
are lexical observations, while its strict-hunk comparisons are unknown. A missing
response is not a clean-knowledge certificate. Partial patch blocks are flagged.

All 641 bound response hashes and 693 trajectory identities were checked against
the existing delivery audits before feature extraction. The source pool is a
snapshot observed on 7 September 2026; it does not by itself attest historical
availability. Source IDs in responses are compared against that snapshot, and
literal full-patch presence is retained separately. No outcomes select records,
and neither the original 99-task repair scores nor the historical 88-task
sensitivity is changed. Card-v2 remains a separate adaptive condition.

The package contains no raw patch lines or complete response text. Source/response
hashes and public task/source IDs are retained. This replay checks arithmetic over
the projected edit features; it does not re-extract them from the private original
histories, repeat the source-capture audit, prove semantic duplication, unauthorized
access, causal use or absence of other contamination channels. The source bindings
identify those inputs and extraction code. Human review and a complete experimental
release remain pending. This is a local draft; no external upload has occurred.
