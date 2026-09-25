"""Render the gain-over-no-memory version of the benchmark-comparison figure.

Run: python figures/scripts/draw_benchmark_gain.py -> figures/benchmark_gain.pdf

Reads the same data file as draw_benchmark_pool.py (benchmark_pool_data.json,
tabulated in the first appendix table) and plots each method's rate minus the
no-memory rate on the same benchmark. No new data, no inferred error bars.
Style follows draw_benchmark_pool.py: serif type, red = ContextGraph,
blue = baselines.
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent            # data files live here
FIG_DIR = HERE.parent                             # PDFs are written to figures/
DATA = json.loads((HERE / "benchmark_pool_data.json").read_text())["benchmarks"]
RED, BLUE, GRAY = "#C73527", "#2984B9", "#858585"
TIMES = Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf")
if TIMES.exists():
    font_manager.fontManager.addfont(str(TIMES))
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "font.size": 10, "axes.titlesize": 10.5, "axes.linewidth": 0.7,
    "xtick.labelsize": 9, "ytick.labelsize": 10, "grid.color": "#DDDDDD",
    "grid.linewidth": 0.55, "axes.axisbelow": True, "pdf.fonttype": 42,
})

assert DATA["methods"][0] == "No memory"
methods = DATA["methods"][1:]
names = [m + ("†" if m in DATA["author_adaptations"] else "") for m in methods]

fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.2), sharey=True)
fig.subplots_adjust(left=0.17, right=0.99, bottom=0.2, top=0.82, wspace=0.12)
for i, (ax, res) in enumerate(zip(axes, DATA["results"])):
    base = res["rates"][0]
    gains = [round(r - base, 1) for r in res["rates"][1:]]
    for row, (m, g) in enumerate(zip(methods, gains)):
        is_cg = m == "ContextGraph"
        ax.barh(row, g, color=RED if is_cg else BLUE, height=0.62,
                alpha=0.95 if is_cg else 0.8)
        label = f"{g:+.1f}".replace("-", "−")
        ax.annotate(label, (g, row), xytext=(-3 if g < 0 else 3, 0),
                    textcoords="offset points", ha="right" if g < 0 else "left",
                    va="center", fontsize=8.5,
                    fontweight="bold" if is_cg else "normal")
    ax.axvline(0, color=GRAY, lw=0.9)
    ax.set_title(f"({chr(97 + i)}) {res['name']}\nno memory = {base:.1f}%",
                 pad=5, fontsize=9.5, linespacing=1.1)
    ax.set(xlim=(-6.5, 17.5), xticks=[0, 5, 10, 15],
           ylim=(len(methods) - 0.5, -0.5), yticks=range(len(methods)))
    ax.grid(axis="x")
    ax.tick_params(axis="y", length=0, pad=5)
axes[1].set_xlabel("Gain over no memory (percentage points)")
axes[0].set_yticklabels(names)
axes[0].get_yticklabels()[-1].set_fontweight("bold")
out = FIG_DIR / "benchmark_gain.pdf"
fig.savefig(out, bbox_inches="tight", pad_inches=0.025)
print("wrote", out)
