# ICLR 2027 research draft

`main.tex` is the current evidence-based working draft. The existing `../main.tex`
remains the historical NeurIPS-style preprint; its effect claims have not all been
revalidated and are not copied into this draft.

Existing Related-Lite Flat/Card reports record 18/99 each. An extended audit found
one appended Flat Docker log whose full-file hash no longer matches its receipt;
an independent frozen-verifier recheck of the unchanged prediction reproduces the
original failure and passes its evidence checks. The first-prediction outcomes are
unchanged, and the original provenance limitation remains disclosed. The new
Verified 350/150 experiment remains work in progress, with no
invented test score.

A subsequent deterministic audit of all 198 original Flat/Card trajectories
finds a median of five recorded action prefixes retaining any original served
memory response in each arm, with no original response retained at the last
recorded action prefix. It uses the saved processor configurations and pinned
SWE-agent source, with 1,426 direct boundary checks and a 66-record regression.
This establishes transient original response retention, not complete forgetting
or a causal explanation for repair outcomes. Its plan, full audit, and validation
are bound in the evidence map; existing scores and runtime are unchanged.
`retention-reproduction-v1.zip` provides a standalone structural reproduction of
all 198 records and 1,426 boundary checks, using the original processing methods
and source-bound history metadata. Two builds are byte-identical, a fresh archive
passes isolated replay, and five missing/changed-evidence checks are rejected.
No original message text is included; content-based delivery remains covered by
the separate delivery package. Extract the archive and run
`uv run --no-project python reproduce.py` from its directory.

The official [ICLR 2027 author guide](https://iclr.cc/Conferences/2027/AuthorGuidelines)
sets abstract and full-paper deadlines at September 18 and September 25, 2026,
23:59 AoE, respectively (Beijing: September 19 and September 26, 19:59).
Main text is limited to nine pages at submission. The downloaded official style
archive and individual files are pinned in `template-source.json`.

An AI-use section is included using the actual work performed; human review is
still pending, as stated in the draft. No paper or abstract has been submitted.

Build locally:

```bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
```

Tectonic 0.17.0 was installed from its official release. The manuscript is anonymous.
`statistical-reproduction-v1.zip` is a local anonymous statistical supplement draft:
594 first-prediction verdicts reproduce all 18 Related-Lite comparisons, with both
fixed denominators and the stated Holm families. Extract it and follow its README;
the script needs only the pinned NumPy dependency and makes no service calls.
An independent rebuild produced the identical archive. Missing-record,
changed-verdict and file-integrity checks were exercised in temporary copies.
This package recomputes statistics; the full raw verifier/delivery evidence and
experimental environment still need a complete anonymous release and human review.
`evidence-map.json` binds current claims and export validation to repository artifacts.

The separately completed adaptive Card-v2 revision resolves 16/99; Flat and
Card-v1 each resolve 18/99. Its 99 original evidence chains pass the completion
audit, with exact cards on 97/99 and no phase refusals. The 39 hard `exit_cost`
labels exceed the registered maximum of 32. Both fixed exact paired comparisons
have Holm-adjusted p=1; the same 88-task sensitivity is reported separately.
`card2-statistical-reproduction-v1.zip` supplies the corresponding 297 verdicts
and reproduces all four comparisons, preserving the original six-condition
bundle. Follow its README for the independently validated NumPy 2.5.0 replay;
the older bundle pins 2.5.2. This revision was informed by historical target
observations, and its completion analysis was attached after execution began.
The results remain exploratory and do not identify a causal memory benefit.

A separate metadata census reads all 594 original solver trajectories and checks
their original hashes before and after collection. Saved SWE-agent/SWE-ReX version
declarations and selected model/history settings agree across the six conditions.
The Git recorder reads HEAD without checking dirty state, and SWE-ReX's Git hash
is unavailable in every record. These declarations are distinct from the stronger
before/after verifier-environment binding and do not reconstruct each historical
solver interpreter, imported module or wire request. The full non-secret projection
and source check are in `docs/reports/gfx-solver-metadata-20260907/` in the parent repo.

The literature update also cites Saha's cue-anchored delivery/compaction study and
Adam's ontology-grounded project-memory evaluation. Delivery and provenance audits
have prior work; this draft's retention result concerns the fixed processor's
selection of original responses in 198 original trajectories and does not establish
a causal benefit from reinjection. The two versioned PDFs and full-text review
are recorded in `docs/literature/2026-09-07/` in the parent repository.

`delivery-reproduction-v1.zip` separately reproduces all 594 original memory and
Control exposure records from source-bound projected histories, using the original
classifier functions and preserving response text, frozen cards and trajectory
joins. The standalone script uses only the Python standard library. Its README
explains the retained public benchmark traceback paths and the limits of the
recorded-channel and identity scans. Raw verifier execution and debug-log
rate-limit checks are outside this package. Both packages are local review drafts.

`verification-reproduction-v1.zip` adds all 594 original prediction files, with
original official report/result and verified-patch bytes for 302 nonempty
predictions. The other 292 retain their empty-submission short-circuit records;
the package does not claim test execution for them. It replays the original report
matcher, checks patch/trajectory joins to the existing audits, and preserves Flat's
historical Docker-log exception. Two builds are identical; a freshly extracted
archive passes isolated replay and exports six exact 99-prediction JSONL files.
Six missing/changed-evidence checks are rejected. Run `uv run --no-project python
reproduce.py --predictions-dir predictions` inside the extracted directory.
Receipts and evidence manifests are explicitly projected fields with original
hashes, while prediction/report/verified-patch bytes are exact. This package does
not re-execute tests or reconstruct the full runtime and Docker evidence chain.
It remains a local review draft, with no new predictions or changed outcomes.

`runtime-image-manifests-v1.zip` checks the public-registry manifest bytes for
the base and all 99 fixed task images against their original immutable digests.
The 100 roots and selected platform descriptors correspond to 188 distinct raw
manifest objects; two builds match, isolated replay passes, and nine corruption
checks are rejected. It downloads no configuration/layer payloads and runs no
images, so complete execution reproducibility remains unfinished. Extract and run
`uv run --no-project python -I reproduce.py`. A separate source audit found the
archived `environment.yml` is HTML; its recovered declaration differs from the
frozen installation and is not used as an installation lock. The underlying
observations and limitations are in `docs/reports/gfx-runtime-portability-20260907/`
in the parent repository.

`figures/original_response_retention.pdf` (also SVG/PNG) plots all 198 audited
Flat/Card-v1 sequences in the same fixed task-ID order. Its four colors distinguish
before first retention, original-response retention, later absence and no recorded
action. First retention can be late: prefixes 3--125 for Flat and 3--359 for Card.
The five-prefix median is a retention count, not the first five actions. The
adjacent JSON records every plotted cell, source/output hashes, task order and
versions. Generate an independent copy in a new directory with:

```bash
uv run --no-project --with matplotlib==3.11.1 --with numpy==2.5.2 python scripts/analysis/plot_gfx_response_retention_v1.py --retention paper/iclr2027/retention-reproduction-v1/expected-retention.json --identities paper/iclr2027/retention-reproduction-v1/original-attempts.json --out-dir /tmp/contextgraph-retention-figure
```

`verdict-semantics-reproduction-v1.zip` replays the frozen harness comparison for
all 287 complete recorded before/after comparisons. All reports match; 15 setup failures
and 292 empty predictions remain separately identified within the same 594
original attempts. In this frozen Related-Lite implementation, `resolved` requires
FAIL_TO_PASS success but does not veto PASS_TO_PASS failures. Four resolved
predictions have recorded PASSED-to-FAILED regressions: Flat and Graph on
Django-34570, Rules and Control on Django-33461. PASS_TO_PASS success also includes
some unchanged skipped, failed or missing statuses. The manuscript now states
these criterion semantics; original official scores are unchanged. The package
contains original status-log/report bytes, pinned test lists and the frozen source,
but does not reparse complete raw test stdout or execute tests. These rules do not
redefine the separate SWE-bench Verified campaign.

The archived paired-effect figure uses the already audited 99-task and 88-task
comparisons, with unadjusted paired bootstrap intervals. Its PDF, SVG and PNG are
in `figures/`; the adjacent JSON records exact plotted values, input/output hashes
and the plotting version. From the ContextGraph root, regenerate with:

```bash
uv run --no-project --with matplotlib==3.11.1 python scripts/analysis/plot_archived_paired_effects.py --source docs/reports/gfx-expanded-audit-20260906/paired-comparisons.json --out-dir paper/iclr2027/figures
```

The original Flat-reference plot excludes Control and local Verified results.
The current manuscript uses `figures/archived_effects_with_control.pdf`, which
adds the completed contemporaneous Control audit; its adjacent JSON binds the
six-arm comparisons. Neither figure includes the unfinished Verified campaign.

The original Verified scheduler and registered analysis closed incomplete on
September 6 at 12:52 UTC. Django11740's three original predictions were resolved;
Xarray6992's three were unresolved. Django16256 Flat's original empty prediction
was also officially unresolved after command timeouts, while its outer status
classification interrupted admission. The original records and analysis remain
unchanged. A separately disclosed operational-stop amendment then started only
previously unstarted attempts with the same frozen inputs and budget limits.
That continuation closed at 14:05 UTC after four complete blocks: a Sphinx Control
response contained an optional null array argument that crashed the SWE-agent
parser after 47 protocol-valid API calls. Its official receipt records an empty
patch; the strict audit continues to reject its generic error stop. Fourteen slots
were attempted, thirteen pass the full audit, and 436 remain unstarted. A separate
parser candidate passes recorded-call regression checks and completed its separate
training-only infrastructure gate at 15:56 UTC. All three protocol/delivery audits
passed; Control and Flat were officially resolved, Graph submitted an empty patch.
The real runs recorded zero optional-null omissions, so branch coverage comes
from the recorded-call regression. The candidate is not deployed to the formal
test runtime. Both nonempty training verifications passed the required 8 FAIL_TO_PASS
and 133 PASS_TO_PASS tests, while each raw suite still reported 1 failed/142 passed.
These are training observations, not a formal memory-effect estimate.
Combined original formal and new training solver accounting is $226.428930;
with $20 monitoring reserved, another $105 whole block exceeds the unchanged $300
allowance. No new formal attempts are admitted.
The full 150-task denominator remains fixed per arm and no formal effect estimate
is reported. See the bound amendment checkpoint and deployment records.

Two separate portable-entry Docker diagnostics completed on September 7 (Beijing), using the frozen evaluator and original Flat predictions for Astropy-15082 and Django-11776. Both full reports were byte-identical to their original p1 reports, retaining one resolved and one unresolved result. All 36 container inspections were network-none; original input images and package bytes were unchanged. These known-outcome checks reused images on jie and are not a new benchmark score or a clean-machine release test. The source package and full execution archive remain private local drafts pending source licensing and publication review. See `../../docs/reports/gfx-portable-verifier-20260907/README.md` and its collection receipt.

A separate training-only source-scoped candidate bank was built after the prior 30-rule semantic audit. It revises the ten partly-supported explanations, retaining all 350 sources and 459 rules; 449 original records/vectors and all evidence/tags are unchanged. Twenty unchanged sample vectors reproduce exactly with the pinned local embedding stack. Ten source-derived checks and six boundary tests pass. This candidate is not deployed to the frozen formal experiment, and no repair effect is measured. See `../../docs/reports/verified-rule-revision-20260907/README.md`; the earlier manuscript findings continue to describe the original bank.

A later source-excluded development diagnostic selects 70 public issues from that
previously inspected training pool and builds both retrieval banks from the other
280 sources. It exposed a swallowed Lucene clause-limit error on Matplotlib-22719.
A separate BM25 chunking candidate completed all 280 retrieval calls after two
disclosed infrastructure adjustments; all earlier incomplete records are retained.
Graph's weak-tag Hit@3 is 52/70 in the base bank and 53/70 in the revised bank,
versus 50/70 for Flat in each. The labels share the graph's mechanism taxonomy and
are not independent relevance judgments or repair outcomes. All 74 available
ordinary-query BM25 reference outputs reproduce exactly, and all four long-query
recoveries are recorded. The formal runtime, manuscript and PDF are unchanged.
See `../../docs/reports/verified-source-holdout-20260907/README.md` for complete
denominators, failed starts, candidate semantics and source-exclusion checks.

The new full-universe patch-overlap appendix audits all 693 original Related-Lite
records, including the separate Card-v2 condition. It joins 641 recorded response
hashes and measures 3,020 actual patch blocks, alongside all 28,809 source-pool /
target pairs. Seven targets outside the historical exclusion list have observed
same-repository added-line Jaccard at least 0.5 in every memory condition. The old
99-task scores and 88-task sensitivity are retained; lexical overlap is not a
cheating or causal-use verdict. One pinned target diff is malformed, and its
strict-hunk comparisons remain unknown. `patch-overlap-reproduction-v1.zip`
provides a standalone replay from hashed edit features, with no raw patch lines
or response text. Follow its README; the underlying capture and source-extraction
checks are bound in `../../docs/reports/gfx-full-overlap-20260907/`.

Appendix B follows this with an exact file-hunk comparison over the same full
universe. Nineteen targets have exactly matching Python-file hunks in the current
source pool; full matching source delivery is confirmed on 16/99 targets in each
memory condition except Rules (13/99). The additional Matplotlib-23172 case has
an exact implementation match despite whole-patch Jaccard .375. The earlier
Sympy-26642 short-edit example is clarified: its shared line is the complete
Python fix, and the extra line is contributor metadata. These observations do not
change repair scores or task exclusions. The hashed-feature replay, all 19 pairs,
limits, and independent Git checks are in
`../../docs/reports/gfx-exact-hunks-20260907/README.md`.

Appendix C records a separately frozen first-memory literal-patch replay. The
selection preserves all 99 targets (95 nonempty predictions, four empty), but
the first run stopped after seven attempts following an Astropy verifier setup
failure and an admission-check defect. Every report and the 92 unstarted targets
are retained; no overall replay rate is computed. The new readiness classifier
is separate from receipt integrity and has been exercised by a real one-task
environment diagnostic. The replay also records the 31 field differences between
archived cases and pinned parquet metadata, without replacing original evidence.
See `../../docs/reports/gfx-literal-replay-20260907/README.md`.
