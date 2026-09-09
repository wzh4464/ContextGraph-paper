"""Draw the implemented source-witness retrieval and composition path."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).with_name('memory_method')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                     'pdf.fonttype': 42, 'svg.fonttype': 'none'})
fig, ax = plt.subplots(figsize=(7.6, 2.9))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax.set(xlim=(0, 7.6), ylim=(0, 2.9))
ax.axis('off')


def box(x, y, w, h, text, color='#edf2f6'):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle='round,pad=0.025,rounding_size=0.04',
        linewidth=.8, edgecolor='#64748b', facecolor=color))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center',
            fontsize=10, linespacing=1.35, color='#182b3a')


def arrow(a, b, dashed=False):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=10,
        linewidth=.9, color='#476477', linestyle='--' if dashed else '-'))


box(.10, 1.55, 1.55, .68, 'Public issue\n+ code reads')
box(2.02, 1.55, 1.43, .68, 'Qwen / FAISS\nsource IDs')
box(3.82, 1.55, 1.43, .68, 'Graph join\nfull witness')
box(5.62, 1.55, 1.84, .68, 'Compose on the\ncurrent operation', '#e6f0eb')
for left, right in [(1.67, 2.00), (3.47, 3.80), (5.27, 5.60)]:
    arrow((left, 1.89), (right, 1.89))

box(2.02, .07, 3.23, 1.07,
    'Source repair → executable witness\n'
    'Trigger → operation → observer\n'
    'Input relations · source executions', '#f7f1e7')
ax.text(3.64, 1.29, 'REUSABLE SOURCE GRAPH', ha='center', va='center',
        fontsize=8, color='#715c3b')
arrow((4.54, 1.34), (4.54, 1.53))
ax.text(.88, .60, 'Historical issues\nand repairs', ha='center', va='center',
        fontsize=9, color='#476477', linespacing=1.4)
arrow((1.67, .60), (2.00, .60))

box(5.62, .07, 1.84, 1.07, 'Execute condition\n↓\nRepair and verify', '#e6f0eb')
arrow((6.54, 1.53), (6.54, 1.17))
ax.plot([.88, .88, 6.54, 6.54], [2.25, 2.63, 2.63, 2.43],
        color='#476477', linewidth=.9, linestyle='--')
arrow((6.54, 2.43), (6.54, 2.25), dashed=True)
ax.text(3.65, 2.66, 'retain public objects and operation sequence',
        ha='center', va='bottom', fontsize=9, color='#476477')
for suffix in ('.pdf', '.svg', '.png'):
    fig.savefig(OUT.with_suffix(suffix), dpi=220, bbox_inches='tight', pad_inches=.02)
plt.close(fig)
