"""Cross-model comparison from the per-model rates in crossmodel_data.json.

Run: python figures/scripts/draw_crossmodel.py -> figures/crossmodel_comparison.pdf

Uses the serif typography of the benchmark figure, with ContextGraph in red.
Oracle access has a distinct hatched bar.
"""
import json
import numpy as np
from matplotlib.patches import Patch
from draw_benchmark_pool import OUT, RED, GRAY, plt, save

data = json.loads((OUT / "crossmodel_data.json").read_text())
rates = np.array(data["rates"], dtype=float)  # methods x models, percent
COLORS = {"None": GRAY, "Random summaries": "#8E44AD", "Mem0": "#27AE60",
          "Oracle summary": "#FFFFFF", "ContextGraph": RED}
methods = data["methods"]
colors = [COLORS[m] for m in methods]
labels = ["No memory" if m == "None" else m for m in methods]
ORACLE, CG = methods.index("Oracle summary"), methods.index("ContextGraph")

fig, axes = plt.subplots(1, len(data["models"]), figsize=(6.6, 2.3), sharey=True)
fig.subplots_adjust(left=0.073, right=0.99, bottom=0.08,
                    top=0.68, wspace=0.14)
for j, ax in enumerate(axes):
    for i, rate in enumerate(rates[:, j]):
        ax.bar(i, rate, width=0.70, color=colors[i],
               edgecolor="#555555" if i == ORACLE else colors[i],
               hatch="////" if i == ORACLE else None, linewidth=0.65, zorder=3)
        ax.text(i, rate + 1.0, f"{rate:.1f}", ha="center", va="bottom",
                fontsize=7.5, fontweight="bold" if i == CG else "normal")
    ax.set(xlim=(-0.7, len(methods) - 0.3), ylim=(0, 43), xticks=[],
           yticks=[0, 10, 20, 30, 40])
    ax.set_title(data["models"][j], fontsize=10, pad=7)
    ax.grid(axis="y")
    ax.tick_params(axis="y", length=2.5, pad=3)
axes[0].set_ylabel("Resolution rate (%)", labelpad=3)
handles = [Patch(facecolor=c, edgecolor="#555555" if i == ORACLE else c,
                 hatch="////" if i == ORACLE else None, label=label)
           for i, (c, label) in enumerate(zip(colors, labels))]
fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False,
           bbox_to_anchor=(0.54, 1.02), fontsize=10,
           handlelength=1.2, handletextpad=0.45, columnspacing=1.4, labelspacing=0.45)
save(fig, "crossmodel_comparison")
