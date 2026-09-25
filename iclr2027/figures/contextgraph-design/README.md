# ContextGraph figures: design revision (2026-09-21)

This folder contains the author's concept comparison and executable-study
overview, redrawn from `../contextgraph-author-style/`. Both original PDFs
remain unchanged in the main text. At the author's request on September 24,
they appear before the experiments: Figure 2 follows the motivation case on
page 3, and Figure 4 concludes the method on page 4. Their labels are
`fig:concept` and `fig:behavior-workflow` in `experience-memory.tex`.
The core abstract-experience architecture is Figure 3, drawn from
`../experience-memory-overview.tex`. The body remains eight pages.
`../contextgraph-design.zip` is the original package snapshot.

| Figure | SVG | PDF | PNG (3×) |
|---|---|---|---|
| Figure 1 · concept | [SVG](fig1-concept.svg) | [PDF](fig1-concept.pdf) | [PNG](fig1-concept.png) |
| Figure 2 · overview | [SVG](fig2-overview.svg) | [PDF](fig2-overview.pdf) | [PNG](fig2-overview.png) |

`index.html` is the review page. It shows both figures with captions, and a print-size toggle displays them at \linewidth (5.5 in).

```latex
\includegraphics[width=\linewidth]{figures/contextgraph-design/fig1-concept.pdf}
\includegraphics[width=\linewidth]{figures/contextgraph-design/fig2-overview.pdf}
```

## Design

- **Roles.** Each role keeps one colour in both figures: *r* is blue, *I* amber, *A* teal and *O* violet. Role letters are set in STIX Two italic to match the paper's math.
- **Lines.** Amber lines carry memory traffic (store, link, top-3 IDs, recover). Violet dashed lines carry execution feedback (observations, rerun). Slate lines show task flow. ✓/✗ appear only on the source checks and illustrate witness acceptance, not results.
- **Figure 1.** The two rows share the same past repair, current issue, agent and patch columns. Only the memory interface in the middle differs. Row (a) keeps the requirement sentence and shows the witness slots as empty. Row (b) composes `R(lo, hi)` with `filter(field=x)` into `filter(field__range=R(x,x))`, which is the range adapter defined in the executable-analysis appendix.
- **Figure 2.** Memory, meaning the FAISS index and the context graph, sits in a strip between Build (A) and Apply (B). Build writes into it from above and Apply reads from it below, so no line crosses a stage. The relation network is illustrative and is not a schema export.
- **Icons.** All icons are drawn vectors, and no MemCo bitmap crops are used.
- **Type.** Labels use IBM Plex Sans and code uses IBM Plex Mono. At \linewidth, labels are 6.4 pt and the smallest text is 5.2 pt.

## Original design captions (the manuscript uses behavioral-study captions)

**Figure 1:** From retrieved advice to executable requirements. (a) A retrieval-as-text interface returns the historical requirement $r$ as a sentence; its input, operation, and observer are not retained. (b) ContextGraph links $r$ to its witness $(I, A, O)$, recovers the historical input and observer, and composes them with the current operation: `filter(field=x)` becomes `filter(field__range=R(x,x))`. Observations return to the agent, and the condition reruns after each edit. The comparison concerns the memory interface; agents in both settings may run task tests.

**Figure 2:** ContextGraph overview. (A) A source writer turns a past repair into a requirement $r$ and witness $W=(I,A,O)$. An accepted witness fails on the original version $V^-$ and passes on the repaired $V^+$; the experience is then linked into memory. (B) FAISS over Qwen3-Embedding-8B returns the top three source identities from the same repository, and graph joins recover their witnesses and relations. The historical input is composed with the current operation and executed on the working tree; observations guide edits, and submitted patches go to the official verifier.

## Rebuild

```sh
uv run --no-project python paper/iclr2027/figures/contextgraph-design/draw.py
```

`draw.py` is the only source. It writes both SVGs and `index.html` (built from `page.template.html`), then exports each PDF and PNG with Playwright's `chrome-headless-shell`. It downloads static TTF fonts, so every PDF font is embedded as TrueType (Type0) and none as Type 3. Use `--no-export` to write only the SVGs and the page. If Chromium exits with status 127, it is missing system libraries; the docstring in `draw.py` lists them.
