# Figure 3: ContextGraph architecture

`fig3-contextgraph.svg` is the editable source (396 x 222 pt, Helvetica).
It descends from the Claude Design v1 artwork and adds panel (c), which the
LaTeX source used to draw separately in TikZ.

Rebuild the PDF by printing the SVG with headless Chrome, which embeds the
fonts as TrueType (cairo-based converters emit Type 3 glyphs):

```bash
{ echo '<!doctype html><html><head><meta charset="utf-8"><style>@page{size:396pt 222pt;margin:0}html,body{margin:0}svg{display:block;width:396pt;height:222pt}</style></head><body>'; cat fig3-contextgraph.svg; echo '</body></html>'; } > /tmp/fig3.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --print-to-pdf=fig3-contextgraph.pdf file:///tmp/fig3.html
```
