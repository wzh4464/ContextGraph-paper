# ContextGraph ICLR working paper

Read [main.pdf](main.pdf) or edit [main.tex](main.tex).

The September 15--16 revisions restore the historical benchmark tables and organize
the paper around the method's advantages: experience improves resolution and
reduces retry rounds; executable requirements add omitted behaviors; graph
relations compose historical conditions with the current workflow.

The PDF has **eight main-text pages, one reference page, three historical
appendix pages, two new-result/agentic-retrieval pages, and four planned-experiment
pages** (18 pages total).
ICLR fonts and margins are unchanged. The main text contains seven
tables and two figures. Main Table 4 reports the user-supplied Verified500 result,
346/500 versus 309/500 without memory. Three restored main-text tables cover
Related-Lite98 cross-model results, Related-Lite99 cumulative pass@k, and memory
pool size. The historical appendix preserves the earlier Verified500 result
(318/500) and seven further tables: cross-model episodic
replication, the older V2 aggregate, Verified dev50, Pro50, graph schema, the
six-interface comparison, and redirect refinement.

[planned-experiments.tex](planned-experiments.tex) contains ten additional
tables with explicit TBD cells. The logical review separates historical system
results, content interventions, and graph delivery; specifies the range
transformation's semantics; and defines shared outcome suites, missing-result
handling, relation-reconstruction ablations, and cost accounting for the plans.
All fourteen earlier result tables retain their original data.

[new-results-20260916.tex](new-results-20260916.tex) adds the other supplied
experiment summaries and the full-context code-agent retrieval design, including
one planned comparison. Together with the new main Table 4, this brings the
paper to eighteen result tables and eleven planned tables. Missing experiment
settings remain TBD; the outstanding count and denominator questions are
recorded in the parent repository's September 16 update report.

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
- `docs/reports/paper-logic-review-20260915.md`
- `docs/reports/ppt-code-update-20260916.md`

Build:

```bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
```
