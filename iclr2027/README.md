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
