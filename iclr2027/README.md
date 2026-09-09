# ContextGraph ICLR working paper

Read [main.pdf](main.pdf) or edit [main.tex](main.tex).

The 2026-09-09 revision has **eight pages of main text**, followed by one
reference page (nine PDF pages). It uses the unchanged ICLR template, fonts
and margins. Figure 1 connects FAISS candidate selection, the source witness
graph and composition along the current operation. Table 3 presents the
matched-current-feedback comparison that motivates executable joint conditions.

The draft studies how history supplies requirements omitted from a current
issue. Complete-agent interventions distinguish query preservation, redundant
uniqueness and destination-timezone behavior even when both compared repairs
pass official verification. Content comparisons examine which information
communicates the required behavior and when its triggering condition is lost.
Execution feedback can make a failed condition concrete; applicability and
combined inputs determine what the resulting repair actually achieves.
The method section defines the executable memory unit, explains the graph's
input and operation relations, and describes the finite point-range adapter.
`figures/draw_memory_method.py` produces the vector method figure using the
parent project's existing matplotlib environment.
The Django12663 content matrix in `figures/memory_content_scope.pdf` shows how
feedback can recover named tuples while breaking ordinary sequence subclasses.
Two further development cases show that a failing historical example can
exercise a different function or branch from the current issue; neither memory
input improved that historical behavior in the six complete-agent attempts.
Its parent-repository generator, `scripts/analysis/plot_memory_content_scope_v1.py`,
reads the closed prediction, official verification and raw behavior receipts;
`figures/memory_content_scope.json` records the plotted observations and inputs.

The experiments in this draft use the Verified source280/dev70 development
track. The separate formal150 partition remains unused. Current graph retrieval
and source-presentation development is tracked in the parent repository; its
running outcomes are not included as completed results in the paper.

Implementation and evidence:

- `docs/reports/memory-first-research-20260908.md`
- `docs/reports/memory-information-two-20260908.md`
- `docs/reports/requirement-feedback-constraint-20260908.md`
- `docs/reports/memory-content-four-20260908.md`
- `docs/reports/memory-to-graph-design-20260908.md`
- `data/verified_train_test_v1/source-requirement-agents-v1/final-assessment.json`
- `data/verified_train_test_v1/source-requirement-gap-contact-v2/assessment.json`
- `docs/literature/2026-09-08/utility-rewards-and-missing-requirements.md`

Build:

~~~bash
cd paper/iclr2027
~/.local/bin/tectonic main.tex --keep-logs
~~~
