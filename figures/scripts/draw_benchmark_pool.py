"""Render the benchmark-comparison figure (and an optional pool-size curve).

Run: python figures/scripts/draw_benchmark_pool.py -> figures/benchmark_comparison.pdf

Style: serif type, white background, light gray grid, red circles and blue
squares. No inferred error bars.
Run with a Python environment containing matplotlib.
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent          # data files live here
FIG_DIR = OUT.parent                            # PDFs are written to figures/, where main.tex includes them
DATA = json.loads((OUT / "benchmark_pool_data.json").read_text())
RED, BLUE, GRAY = "#C73527", "#2984B9", "#858585"
TIMES = Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf")
if TIMES.exists():
    font_manager.fontManager.addfont(str(TIMES))
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 10.5,
    "axes.linewidth": 0.7,
    "xtick.labelsize": 9,
    "ytick.labelsize": 10,
    "grid.color": "#DDDDDD",
    "grid.linewidth": 0.55,
    "axes.axisbelow": True,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})


def save(fig, stem):
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.025)
    plt.close(fig)


def benchmarks():
    data = DATA["benchmarks"]
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.45), sharey=True)
    fig.subplots_adjust(left=0.195, right=0.99, bottom=0.17,
                        top=0.89, wspace=0.16)
    methods = data["methods"]
    names = [m + ("\u2020" if m in data["author_adaptations"] else "")
             for m in methods]
    for panel, (ax, result) in enumerate(zip(axes, data["results"])):
        rates = result["rates"]
        for row, (method, rate) in enumerate(zip(methods, rates)):
            color = RED if method == "ContextGraph" else GRAY if row == 0 else BLUE
            marker = "o" if method == "ContextGraph" else "s"
            ax.hlines(row, 0, rate, color=color, linewidth=1.6, alpha=0.5)
            ax.plot(rate, row, marker=marker, color=color, markersize=4.5)
            ax.annotate(f"{rate:.1f}", (rate, row), xytext=(4, 0),
                        textcoords="offset points", va="center", fontsize=9,
                        fontweight="bold" if rate == max(rates) else "normal")
        ax.set_title(f"({chr(97 + panel)}) {result['name']}", pad=8)
        ax.set(xlim=(0, 88), xticks=[0, 20, 40, 60, 80],
               ylim=(len(methods) - 0.5, -0.5),
               yticks=range(len(methods)), xlabel="Resolution rate (%)")
        ax.grid(axis="x")
        ax.tick_params(axis="y", length=0, pad=7)
    axes[0].set_yticklabels(names)
    axes[0].get_yticklabels()[-1].set_fontweight("bold")
    save(fig, "benchmark_comparison")


def pool_size():
    """Optional pool-size curve (resolution only); not used in the paper."""
    data = DATA["pool_size"]
    fig, ax = plt.subplots(figsize=(6.6, 1.95))
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.25, top=0.97)
    x = data["summaries"]
    ax.plot(x, data["resolution_rate"], "o-", color=RED, linewidth=1.8,
            markersize=5.5, label="Resolution rate")
    for xx, yy in zip(x, data["resolution_rate"]):
        ax.annotate(f"{yy:.1f}", (xx, yy), xytext=(0, 7),
                    textcoords="offset points", ha="center", fontsize=10)
    ax.set(xlim=(35, 315), ylim=(0, 45), xticks=x, yticks=[0, 10, 20, 30, 40],
           xlabel="Number of summaries", ylabel="Resolution rate (%)")
    ax.grid()
    save(fig, "pool_size_resolution")


if __name__ == "__main__":
    benchmarks()
