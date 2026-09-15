# ContextGraph ICLR working paper

Read [main.pdf](main.pdf) or edit [main.tex](main.tex).

The 2026-09-15 revision restores the historical benchmark tables and organizes
the paper around the method's advantages: experience improves resolution and
reduces retry rounds; executable requirements add omitted behaviors; graph
relations compose historical conditions with the current workflow.

The PDF has **eight main-text pages, one reference page, three historical
appendix pages, and four planned-experiment pages** (16 pages total).
ICLR fonts and margins are unchanged. The main text contains seven
tables and two figures. Four restored historical tables cover Verified500,
Related-Lite98 cross-model results, Related-Lite99 cumulative pass@k, and memory
pool size. The appendix restores seven further tables: cross-model episodic
replication, the older V2 aggregate, Verified dev50, Pro50, graph schema, the
six-interface comparison, and redirect refinement.

[planned-experiments.tex](planned-experiments.tex) contains ten additional
tables with explicit TBD cells. The logical review separates historical system
results, content interventions, and graph delivery; specifies the range
transformation's semantics; and defines shared outcome suites, missing-result
handling, relation-reconstruction ablations, and cost accounting for the plans.
All fourteen recorded result tables retain their original data.

Historical results retain their original model, source pool, task denominator,
and attempt regime. This editing pass restores reported aggregate data;
it does not rerun or reverify their underlying patches. The current executable
memory evidence comes from the Verified source280/dev70 development track.
The new matched four-benchmark comparison remains incomplete.

The argument proceeds from useful memory to its representation and retrieval:

1. Earlier benchmark results show the utility of experience, including 25
   Related-Lite resolutions in two passes versus three without memory.
2. Paired interventions identify query preservation, redundant uniqueness,
   and destination-timezone requirements supplied by history.
3. Content comparisons explain why the triggering input matters.
4. FAISS selects candidate sources; the graph supplies the input and operation
   relations used to construct joint checks and guide refinement.

[Historical table sources](historical-tables/README.md) records the restoration
map. The original historical preprint remains unchanged at `../main.tex`.

Supporting development reports in the parent repository:

- `docs/reports/memory-first-research-20260908.md`
- `docs/reports/memory-information-two-20260908.md`
- `docs/reports/requirement-feedback-constraint-20260908.md`
- `docs/reports/memory-content-four-20260908.md`
- `docs/reports/memory-to-graph-design-20260908.md`
- `docs/reports/paper-table-restoration-20260915.md`

Build:

```bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
```
