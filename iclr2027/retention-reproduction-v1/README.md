# Original memory-response retention reproduction

Run from this directory with Python 3.10 or later (standard library only):

```bash
uv run --no-project python reproduce.py
```

All 198 original Flat/Card-v1 records must match `expected-retention.json`, including
every retention interval and all 1,426 rendered processor boundary checks.
Each record joins the original first-attempt evidence by trajectory SHA. Missing
tasks, changed configurations, changed results or changed bundle files fail.
No API, model, benchmark solver, database or Docker service is called.

`projection.json.gz` preserves the original order and structural metadata of every
history entry, saved processor settings, and the SHA, character count and line
count of each served memory response. It contains no original message text or
commands. The replay uses shape placeholders with the same line count for memory
responses, and empty content for other messages. Content-independent retention
decisions and omitted memory-response placeholders therefore match the original
audit. Omitted text for non-memory messages is intentionally not reconstructed.
These placeholders are a representation of recorded data, not simulated agent
trajectories or new experimental outcomes.

`retention_core.py` contains the original `_get_omit_indices`, `__call__`,
`_get_content_text` and `_set_content_text` methods/functions, copied verbatim from
`original_history_processors.py`. The only new class code adapts the frozen saved
configuration without requiring Pydantic or the rest of SWE-agent. Source hashes,
the Git revision, method hashes and MIT license are included. The archived raw
trajectory audit separately invoked the complete original processor on all
boundary checks and verified the original source against that Git revision.

Both arms ever received memory on 99/99 tasks; none retain an original response
at the final recorded action prefix. Median prefixes retaining any original
response are five per arm, against median total action prefixes of 497 and 495.
These post-observation measurements are not a causal effect or proof of forgetting.
They do not track paraphrases, copies elsewhere, internal state or every wire
request/retry. Correct repository-card content, actual delivery and raw official
verification are outside this structural package. The separately bound delivery
package reproduces content-based delivery checks. The prior Flat verifier-log
reconciliation limitation and unchanged fixed 99-task denominator still apply.

This is a local anonymous supplement draft; it has not been uploaded or submitted.
