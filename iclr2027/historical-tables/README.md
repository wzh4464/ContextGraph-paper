# Restored historical tables

The current manuscript restores eleven historical tables alongside its three
existing requirement/content/composition tables. All nine preprint table
blocks are preserved verbatim in `preprint-tables-original.tex`; that archive
is not compiled. Their original captions include interpretations superseded
by the current text. `iclr-previous-tables-original.tex` preserves the earlier
six-interface table, and `redirect-table-original.tex` preserves the redirect
refinement comparison.

| Current table | Historical source | Placement |
|---|---|---|
| Related-Lite99 cross-model V1 | `3e51135:main.tex`, `tab:swectx-crossmodel` | Main Figure 5 (`fig:swectx-crossmodel`) |
| Related-Lite99 cumulative pass@k | `3e51135:main.tex`, `tab:swectx-stream` | Main Table 4 (`tab:swectx-stream`) |
| Memory pool size | `3e51135:main.tex`, `tab:swectx-poolsize` | Main Table 5 (`tab:swectx-poolsize`); V2 in Table 8 |
| Verified500 | `3e51135:main.tex`, `tab:verified500` | Appendix Table 6 (`tab:verified500-historical`) |
| Episodic cross-model replication | `3e51135:main.tex`, `tab:swectx-xmodel` | Appendix Table 7 |
| Related-Lite99 V2 aggregate | `3e51135:main.tex`, `tab:swectx` | Appendix Table 8 |
| Verified dev50 | `3e51135:main.tex`, `tab:dev50` | Appendix Table 9 |
| Pro50 (originally disabled) | `3e51135:main.tex`, `tab:pro50` | Appendix Table 10 |
| Historical graph schema | `3e51135:main.tex`, `tab:schema` | Appendix Table 11 |
| Related-Lite99 six interfaces | `7917b0a:iclr2027/main.tex`, `tab:audit` | Appendix Table 12 |
| Django14404 refinement | `6fc8be3:iclr2027/main.tex`, `tab:residual` | Appendix Table 13 |

Values retain their historical denominators. The V1 pool-size comparison no
longer uses the old V2 control delta; the V2 headline remains a separate table.
The main cross-model figure displays rates derived from the original fractions;
all 24 fractions are retained in `figures/crossmodel_data.json`. The complete
original rates and paired statistics remain in the archive. The Pro table
retains its asymmetric budget description. An external paper's Sonnet scores,
old significance decorations, and interpretations are not transplanted into
our current result tables. No numerical outcome is added by this restoration.

The September 16 update adds user-confirmed new experiments from slide9 of
`context_graph_v9_no_movie.pptx`. Main Table4 now reports346/500 for the new
then-reported GPT-5.4/mini-SWE-agent experiment; the historical318/500 table above retains
its exact numerical body and original protocol. Tables16--18 transcribe the
other new result sets, with unspecified settings markedTBD. The original
slide remains unchanged. See `new-results-20260916.tex` and the root-repository
report `docs/reports/ppt-code-update-20260916.md` for source mapping and the
three outstanding author queries; no new paired statistics are inferred.

On September 24 the author replaced the current Verified500 panel with nine
methods using DeepSeek V4 Pro 0813 and mini-SWE-agent. The current no-memory
and FAISS counts are 308/500 and 326/500; ContextGraph remains 346/500, while
the strongest baseline is ReasoningBank at 335/500. ExpeRepair and ACE use the
author's adaptations to mini-SWE-agent. The historical tables in this directory
retain their original models, counts, and paired statistics.

The September 24 cleanup converts the current main comparison into Figure 4.
The later author revision restores pool size to Table 5 and converts the
four-model comparison into Figure 5. Empty green additions and their appendix
protocols are removed; all recorded historical cells remain. The supplied
slide summaries retain their recorded values in Tables 14–16, with one note
about missing detailed run metadata. The earlier table numbers and TBD
annotations in the September 16 history above describe that earlier revision.
The source-bank coverage counts are retained at the end of `supplement.tex`.
