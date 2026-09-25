# ContextGraph ICLR 2027 manuscript

The current manuscript has **eight main-text pages**, references on pages 9–11,
and **26 pages in total**. The title remains **ContextGraph: Self-Improving Coding
Agents via Cross-Repository Experience Graphs**. `main.pdf` is the canonical PDF.

## September 25 revision: complete the learning workflow

The manuscript follows MulVul's problem–design–workflow–evaluation organization:
Introduction, Related Work, Problem and Motivation, Method, Experiments, Conclusion.
The introduction retains six prose paragraphs followed by three contribution bullets.
The memory unit remains an abstract strategy or warning with applicability and source
context. It is retrieved before planning and after errors. After every task, both
successful and failed trajectories supply new lessons; the graph is updated and the
new experience is immediately available to subsequent tasks.

Figure 2 (previously Figure 3) preserves the supplied architecture artwork and adds a
vector strip for the task-completion/update/retrieval cycle. Algorithm 1 describes
the complete process. The results overview, benchmark comparison, and cross-model
comparison are Figures 1, 3, and 4; ContextGraph uses the same red highlight in the
result figures. No numerical figure data changed.

The main comparisons use online-updating ContextGraph and the default memory-update
behavior of each baseline's open-source implementation. Related-Lite99 and DeepSWE113
report five-run means; each repetition resets the initial memory, and tasks are
evaluated in randomly shuffled order. Source coverage in
the pool-size study means the proportion of oracle-designated relevant sources
recovered by retrieval, not a resolution-rate ratio.

Section 5.5 and main Table 4 now highlight the requirement/implementation
comparison and the separate/composed-check comparison. The summary retains the
72/72 vs 40/72 timezone outcomes (16 regressions) and the 1/3 vs 3/3 withheld
joint-query outcomes. Detailed behavioral studies and their original figures
remain in Appendix F.
Two historical comparison tables were excluded on September 25 after the author
confirmed implementation defects in their ContextGraph runs: GPT-5.4 Verified500
and the six-interface Related-Lite99 comparison. Other result tables are retained. The main numerical
comparison is now the first appendix. Historical static episodic experiments remain
identified separately from the current main comparisons. Agent KB, Memory Transfer
Learning, ExpGraph, mini-SWE-agent, and Datacurve DeepSWE are cited in their relevant
roles. See `mulvul-online-revision-20260925.md` for changes and remaining author details.

Build/render checks and the prior draft are under
`/Users/zihanwu/Public/codes/ContextGraph/outputs/paper-mulvul-online-revision-20260925/`.
The following dated entries describe earlier revisions; figure/table numbers and
placement in those entries belong to their recorded dates.

## September 24 consistency revision

The abstract, introduction, method, and conclusion now share one architecture:
experience abstraction, graph retrieval, and memory access before planning and
after errors. Figure 3 shows that architecture. Its concrete retrieval path
(error pattern, shared rule, source strategy, past trajectory) follows the
repository's graph relations; it is not presented as an observed case trace.

Experiments proceed through overall repair effectiveness, model/pool-size
comparisons, retry success, and behavioral analysis. The three behavioral
analyses now form one subsection, with a finding about applicability context,
condition interactions, or failure-guided revision. Their original diagrams
and all results remain in the main text. They are not labeled as component
ablations of abstraction, graph retrieval, or memory timing.

The full-context retrieval proposal now returns strategies, warnings, and
source context through the core memory interface. Executable examples and
composition remain in the behavioral-study protocol. Cross-references in
both appendices have been updated. Checks and the pre-edit snapshot are in
`outputs/paper-unified-story-20260924/` in the main repository.

## September 24 cleanup and figures

Figure 3 now embeds the supplied Claude Design v1 vector PDF, retrieved from
the Figure 3 email's download page. It remains on page 3 and shows experience
abstraction, the experience graph and retrieval interface, and memory access
before planning and after errors. The original PDF and editable SVG are in
`figures/figure3-design-v1/`; the old TikZ source is retained but no longer
compiled. The caption identifies the graph links as illustrative. Shortened
duplicate figure/table captions and retrieval prose keep the main text at
eight pages without changing table values or the other figures. Checks and
the pre-edit snapshot are in `outputs/paper-figure3-gmail-20260924/` in the
main repository.

At the author's request, the compiled manuscript no longer contains red or
green experiment-planning annotations, TBD cells, unmeasured table extensions,
or their corresponding appendix protocols. Existing measured results are
preserved. The planning source files remain available as author records but
are not included by `main.tex`:

- `additional-evaluation.tex`
- `planned-experiments.tex`
- `table-additions.tex`
- `experiment-review.tex`

The automatic preparation/applicability proposal and unmeasured mechanism
comparisons are removed from `method-contract.tex`; implemented study details
remain. Full-context retrieval retains its design description, without the
unmeasured comparison table. Recorded source-bank coverage from the removed
planning table is preserved in `historical-tables/supplement.tex`.

The three-benchmark comparison is **Figure 5 (page 5)**: all nine methods on
Verified500, Related-Lite99, and DeepSWE113, displaying 27 resolution rates.
The pool-size study is **Table 1 (page 6)**, and the cross-model comparison
is **Figure 6 (page 6)**. The new figure
shows six memory conditions across four language models, with percentages
computed from all 24 original resolved/completed fractions. The style follows MulVul's
`fig/longtail_f1.png`: Times-style serif labels, white background, light gray
grid, and a red highlight for ContextGraph. The cross-model figure uses bars,
with hatching to distinguish oracle access. Both result figures are vector PDFs.

- `figures/benchmark_comparison.pdf`: three-benchmark comparison.
- `figures/crossmodel_comparison.pdf`: four-model memory comparison.
- `figures/crossmodel_data.json`: original counts and settings for all 24 conditions.
- `figures/draw_crossmodel.py`: cross-model figure renderer.
- `figures/pool_size_coverage.pdf`: superseded pool-size figure; no longer compiled.
- `figures/benchmark_pool_data.json`: measured values and reporting settings.
- `figures/draw_benchmark_pool.py`: reproducible rendering script; requires matplotlib.

The original results overview, comparison diagram, architecture diagram, and
behavior figure PDFs are unchanged. All their hashes were checked against the
pre-edit snapshot. At the author's request, the two original design diagrams
now appear before the experiments: Figure 2 (page 3) follows the motivation
case, and Figure 4 (page 4) concludes the method. Their captions retain the
behavioral-study context. The core experience-memory diagram is Figure 3
(page 3). Checks are in `outputs/paper-front-design-figures-20260924/`.

The manuscript now contains five main-text tables and six main-text figures.
Appendices retain historical comparisons, supplied results, development cases,
executable-study implementation, and published reference scores. The numerical
companion to Figure 5 is Table 18 (page 24). Its standalone version is
`main-table-preview.pdf` (one page); empty LoLBench columns and the incomplete
slide-derived rate panel have been removed. The slide's recorded counts remain
in `new-results-20260916.tex`. Detailed run metadata was not supplied for the
additional Related-Lite99 and Gemini summaries. The Codex/GPT-5.5 result is
now identified as the LoLBench Python experiment described below.

## Measured results and author decisions

The main comparison uses DeepSeek V4 Pro 0813 and mini-SWE-agent. ExpeRepair
and ACE are author adaptations to that agent. Related-Lite99 and DeepSWE113
report means across five runs, without standard deviations. Verified500
retains its recorded rate; a five-run mean is not inferred for it.
ContextGraph reports 69.2%, 36.3%, and 72.1%, respectively. Agent KB leads
Related-Lite99 at 38.2%; ContextGraph leads the other two benchmarks.

The author confirmed the fourth benchmark on September 24: 20 Python tasks
selected from LoLBench, with a graph built from other Python tasks and Codex
using GPT-5.5. No memory resolves 1/20 at pass@1 (5.0%); ContextGraph resolves
3/20 at pass@1 (15.0%) and 5/20 at pass@3 (25.0%). The author subsequently
confirmed that the other memory methods also resolve 1/20. Table 16 now
reports 5.0% pass@1 for FAISS Flat, ExpeL, Agent KB, ExpeRepair, ReasoningBank,
ACE, and Supermemory, following the method roster of the main comparison.
The abstract, contribution, results, and conclusion state that ContextGraph
leads these evaluated methods on the LoLBench Python subset. The old 5/30
entry is corrected to 5/20; the latest
update does not establish a no-memory pass@3 result, so that cell is omitted.
This configuration is described separately from the matched three-benchmark
comparison in Figure 5. The abstract, introduction, experiments, and
conclusion incorporate the LoLBench result, citing the public dataset at
https://huggingface.co/datasets/lolbench26/LoLBench.
The source count and task IDs are not inferred from the dataset's language
totals. These are author-supplied results, not a new solver or verification run.
The initial snapshot and checks are in `outputs/paper-lolbench-python20-20260924/`;
the baseline update is checked in `outputs/paper-lolbench-baselines-20260924/`
in the main repository. No baseline pass@3 values or repeated-run means are
inferred from the new aggregate counts.

The four Django behavioral pairs retain Fail/Pass for no memory/memory.
The separate-history control retains Pass, 2/2, 1/3, 2/2, and 2/3.
The retry study retains its three completed rounds; no fourth round is planned
in the manuscript. All historical configurations retain their recorded counts,
denominators, and paired statistics.

Table 1 uses GPT-5.4 and one attempt per task. The 50/100/200/300-summary
resolution rates are 21.88%, 27.55%, 26.80%, and 34.69%; source coverage is
41.3%, 45.8%, 51.4%, and 60.7%. The original resolved/completed counts remain
in the table, Appendix A, and the source data. The author canceled USD/resolution for
this study. The source-coverage definition still awaits author clarification;
these measurements have not been relabeled as Recall@3 or same-repository coverage.

The benchmark name remains Related-Lite99 throughout the compiled manuscript.
`main-table-preview.csv` remains the earlier experiment-entry worksheet;
this cleanup changes the paper and PDF preview, not that planning worksheet.
The open `main-table-preview.xlsx` is not overwritten.

## Verification and history

The cleanup snapshot and checks are in the main repository at
`outputs/paper-clean-figures-20260924/`. The later cross-model-figure and
pool-table revision is checked in `outputs/paper-crossmodel-figure-20260924/`.
It preserves all 24 cross-model fractions and both pool-size metrics. The
existing figure PDFs are unchanged. The build has no undefined references,
overfull boxes, or TBD text. No solver experiment or new measurement was run.

Earlier changes and source mappings are retained in:

- `outputs/paper-cross-repository-memory-20260924/`
- `outputs/paper-verified500-update-20260924/`
- `outputs/paper-related99-update-20260924/`
- `outputs/paper-deepswe-percentages-20260924/`
- `outputs/paper-restore-design-figures-20260924/`
- `outputs/paper-table2-result-20260924/`
- `outputs/paper-separate-history-result-20260924/`
- `outputs/paper-pool-coverage-20260924/`

Older architecture notes, experiment guides, and original-table archives are
author records, not compiled manuscript sections. Current author instructions
and the definitions above take precedence over earlier planned configurations.

## Build

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```
