# ContextGraph — arXiv Paper Source

LaTeX source for the ContextGraph arXiv preprint, scaffolded with the
`vibelab-academic-plans/ml-paper-writing` NeurIPS 2025 template.

## Build

```bash
cd paper
make            # pdflatex → bibtex → pdflatex × 2 → main.pdf
make clean      # remove aux/log/pdf
```

Requires a TeX Live distribution with `neurips.sty` dependencies (`natbib`, `algorithm2e`,
`tabularray`, `booktabs`, `microtype`, `enumitem`, `nicefrac`, `physics`, `mathtools`).

## Files

| File | Purpose |
|---|---|
| `main.tex`        | Paper body. Uses `\usepackage[preprint, nonatbib]{neurips}` so it renders for arXiv (not anonymized). Switch to `[final]` for camera-ready, or remove `preprint` for double-blind submission. |
| `references.bib`  | Bibliography. **All entries need re-verification** before submission — see warning at top of file. |
| `extra_pkgs.tex`  | Shared package preamble copied from the NeurIPS template. |
| `neurips.sty`     | Style file. |
| `Makefile`        | Build orchestration (handles `pdfcrop` for figures, four-pass bib build). |

## Result placeholders

Three results subsections are intentionally left as TODO blocks while the full SWE-bench
runs are still in progress. Search `main.tex` for `% TODO` to find them all:

1. **§5.2 Full SWE-bench-Verified (500 problems)** — populate from
   `results/live_experiment/eval_*` once `swebench.harness.run_evaluation` finishes for
   all five conditions. Required columns: Eval / Resolved / Rate / vs no\_memory /
   McNemar p-value.
2. **§5.3 SWE-bench-Pro** — same five conditions on Pro; comment on whether the relative
   ranking from §5.2 holds under distribution shift.
3. **§5.4 Ablations** — channel ablation (cosine / +BM25 / +PPR), depth ablation
   (PlaybookEntry-only → +CanonicalRule → +Strategy → full), top-$K$ sweep, MMR on/off.

The 50-problem development numbers (Table 1) are already filled in from the screenshot
provided at scaffolding time:

| Method      | Eval  | Resolved | Rate  | vs no\_memory |
|-------------|-------|----------|-------|---------------|
| contextgraph| 48/50 | **32**   | 66.6% | **+8.6 pp**   |
| expel       | 50/50 | 32       | 64.0% | +6.0 pp       |
| faiss       | 49/50 | 30       | 61.2% | +3.2 pp       |
| agentkb     | 48/50 | 29       | 60.4% | +2.4 pp       |
| no\_memory  | 50/50 | 29       | 58.0% | baseline      |

If the live numbers diverge once you re-run, update Table 1 in `main.tex` together with
the abstract numbers ($66.6\%$ vs.\ $58.0\%$, $+8.6$~pp).

## Citation hygiene before submission

Per `vibelab-academic-plans/ml-paper-writing` and the
`inno-reference-audit` skill, every `\cite{}` key in `main.tex` must be verified
against Semantic Scholar / arXiv / Crossref before posting:

```bash
uv run python ../vibelab-academic-plans/inno-reference-audit/scripts/verify-citations.py \
    --bib references.bib --tex main.tex
```

Any citation that is approximate (e.g. tang2025agentkb, nikishin2024never) should be
replaced with verified bibtex from Semantic Scholar before pushing to arXiv.

## Updating from the screenshot table

The Table 1 screenshot lives at `~/Desktop/截屏2026-05-06 下午2.55.33.png`. If the
50-problem numbers are re-computed, update both:
- `\begin{tabular}{lrrrr} ... \end{tabular}` block in §5.1
- the abstract paragraph (4 spots: 32/48, 66.6%, 58.0%, +8.6 pp; and the +2.6 / +5.4 / +6.2 pp head-to-head deltas).
