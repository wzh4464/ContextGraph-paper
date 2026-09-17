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
| Related-Lite98 cross-model V1 | `3e51135:main.tex`, `tab:swectx-crossmodel` | Main Table 1 |
| Related-Lite99 cumulative pass@k | `3e51135:main.tex`, `tab:swectx-stream` | Main Table 2 |
| Memory pool size | `3e51135:main.tex`, `tab:swectx-poolsize` | Main Table 3; V2 in Table 10 |
| Verified500 | `3e51135:main.tex`, `tab:verified500` | Appendix Table 8 (`tab:verified500-historical`) |
| Episodic cross-model replication | `3e51135:main.tex`, `tab:swectx-xmodel` | Appendix Table 9 |
| Related-Lite98 V2 aggregate | `3e51135:main.tex`, `tab:swectx` | Appendix Table 10 |
| Verified dev50 | `3e51135:main.tex`, `tab:dev50` | Appendix Table 11 |
| Pro50 (originally disabled) | `3e51135:main.tex`, `tab:pro50` | Appendix Table 12 |
| Historical graph schema | `3e51135:main.tex`, `tab:schema` | Appendix Table 13 |
| Related-Lite99 six interfaces | `7917b0a:iclr2027/main.tex`, `tab:audit` | Appendix Table 14 |
| Django14404 refinement | `6fc8be3:iclr2027/main.tex`, `tab:residual` | Appendix Table 15 |

Values retain their historical denominators. The V1 pool-size comparison no
longer uses the old V2 control delta; the V2 headline remains a separate table.
The main cross-model table displays the original fractions; the complete
original rates and paired statistics remain in the archive. The Pro table
retains its asymmetric budget description. An external paper's Sonnet scores,
old significance decorations, and interpretations are not transplanted into
our current result tables. No numerical outcome is added by this restoration.

The September 16 update adds user-confirmed new experiments from slide9 of
`context_graph_v9_no_movie.pptx`. Main Table4 now reports346/500 for the new
GPT-5.4/mini-SWE-agent experiment; the historical318/500 table above retains
its exact numerical body and original protocol. Tables16--18 transcribe the
other new result sets, with unspecified settings markedTBD. The original
slide remains unchanged. See `new-results-20260916.tex` and the root-repository
report `docs/reports/ppt-code-update-20260916.md` for source mapping and the
three outstanding author queries; no new paired statistics are inferred.
