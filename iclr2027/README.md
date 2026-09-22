# ContextGraph ICLR 2027 manuscript

The current manuscript has **eight main-text pages**, references on pages 9–10,
and 30 pages in total. It explains the problem, method, and observed results
using concrete repair examples. The paper calls the method **ContextGraph**;
retrieval and update choices are described directly instead of using internal
release names.

## Main text

1. Introduction: three challenges and three explicit contributions; each
   contribution points to its method, experiment, and observed result.
2. Background and motivation: concrete input roles and interactions that
   explain the design.
3. Method: requirement memory, condition composition, and execution feedback.
   These names also identify the three contributions and mechanism studies.
4. Experiments: repair success, three mechanism studies in that same order,
   then models, retries, and pool size. Each group ends with an explicit finding.
5. Discussion and related work: reusable design ideas and the current operation coverage.
6. Conclusion.

The original three-panel results overview is restored as Figure 1.
Seven completed result tables are restored to the main text, including
Verified500 (346/500 versus 309/500), the three behavioral tables, cross-model
Related-Lite98, cumulative Related-Lite99 results, and the pool-size comparison.
All original cells in the **18 recorded tables** are preserved. Twelve tables
now have green additions so every numbered table, and each comparison panel,
has at least four data rows and four columns. Headers are excluded from the
row count; the method/metric column is included. Each experiment retains its
own model, memory pool, task counts, and attempt setting.

## Figures

- `figures/paper_results_overview.pdf`: original three-panel numerical overview.
- `figures/contextgraph-design/fig1-concept.pdf`: executable requirements,
  main Figure 2.
- `figures/contextgraph-design/fig2-overview.pdf`: memory construction and use,
  main Figure 3.
- `figures/memory_content_scope.pdf`: the detailed behavior comparison in the appendix.

All four PDFs are byte-identical to the files before the writing revision.
The two design PDFs also match paper commit `91aa76a`. The unused
`paper_final_overview.*` placeholder files remain available but are not
included in the manuscript.

## Experiments and author material

The **16 pending tables** remain in the appendices, with unmeasured cells
marked red TBD. New rows and columns are green, with green TBD for results to
collect. Existing coverage counts remain black. No new experimental result
was added by this revision.

- `additional-evaluation.tex`: four-benchmark, held-out behavior, mechanism,
  and coverage/cost result panels formerly occupying the main text.
- `planned-experiments.tex`: sampling, comparisons, outcomes, and remaining tables.
- `method-contract.tex`: concise implementation and evaluation details.
- `historical-tables/supplement.tex`: eight additional recorded tables.
- `new-results-20260916.tex`: three supplied result tables and the full-context
  search design.
- `development-details.tex`: case inputs and observed repair behavior.
- `table-additions.tex`: green definitions of the new conditions, measurements,
  denominators, and matched-run settings, linked from each expanded table.
- `绿色表格补充清单.md`: Chinese checklist distinguishing new runs from log recovery.
- `recorded-results.tex`: archive of the former appendix organization of the
  seven tables now restored to the main text; not compiled.
- `author-experiment-protocol.md`: preserved detailed execution instructions;
  not compiled into the paper.
- `实验补齐与结论判读.md`: experiment priorities and practical-effect examples
  for author use. Those examples are not measurements or expected scores.
- `method-evaluation-contract.json`: internal run specification; unchanged by
  this writing revision.

Red experiment marking and green table additions are controlled by `experiment-review.tex`.
`\expcriterion` notes and `experiment-decision-guide.tex` are no longer
rendered in the manuscript; the source text and Chinese author guide retain
the planning information. `\experimentreviewfalse` removes the red styling,
without filling any missing result.

The automatic reproducer preparation, applicability assessor, and shared
validator remain planned work. The paper describes the implemented retrieval
and researcher-written adapters, and states this implementation status where
it explains the input to composition.

## Build

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The challenge-to-contribution-to-evidence mapping is in
`contribution-alignment-20260922.md`.
Verification of this revision is under the main repository's
`outputs/01a0af7d-50b6-7233-ba4f-cc18f3bdf1c4/green-table-extension/support/`.
