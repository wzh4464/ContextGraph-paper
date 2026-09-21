"""ContextGraph Figures 1-2, design revision.

Hand-built SVG (no bitmap crops). Writes fig1-concept.svg, fig2-overview.svg and
index.html (review page), then exports vector PDF + 3x PNG with headless Chromium.

    uv run --no-project python paper/iclr2027/figures/contextgraph-design/draw.py
    uv run --no-project python paper/iclr2027/figures/contextgraph-design/draw.py --no-export

Export uses Playwright's chrome-headless-shell. If it exits with status 127, it is missing
system libraries (libatk, libatk-bridge, libXdamage, libasound, libatspi, libcups, libXRes):
`apt-get download` them, `dpkg-deb -x` into a folder, and point LD_LIBRARY_PATH at its lib dir.
"""
from pathlib import Path
import glob, os, subprocess, sys, tempfile

HERE = Path(__file__).resolve().parent

SANS = "'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif"
MONO = "'IBM Plex Mono', Menlo, Consolas, monospace"
MATH = "'STIX Two Text', 'Times New Roman', Times, serif"
FONTS = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600"
         "&family=IBM+Plex+Sans:wght@400;500;600"
         "&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400;1,600&display=block")

INK, INK2, INK3, RULE = "#1E2632", "#4B5667", "#8A93A1", "#D5DAE1"
AMBER, AMBER_T = "#B5670F", "#94540B"
VIOLET, PASS, FAIL = "#6650A6", "#2E8150", "#C4462A"
ROLE = {  # fill, stroke, letter
    "r": ("#DCE6F4", "#3D649C", "#22416E"),
    "I": ("#FBE6C1", "#B5670F", "#7A4308"),
    "A": ("#D2EAE2", "#2C7A64", "#1B5646"),
    "O": ("#E6DFF4", "#6650A6", "#45337E"),
}
ROLE_NAME = {"r": "requirement", "I": "input", "A": "operation", "O": "observer"}
LINE = {"slate": INK2, "amber": AMBER, "violet": VIOLET}


# ---------- primitives ----------
def text(x, y, s, size=13, weight=400, fill=INK, anchor="middle", family=None,
         italic=False, central=False, extra=""):
    a = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"', f'fill="{fill}"',
         f'text-anchor="{anchor}"']
    if weight != 400: a.append(f'font-weight="{weight}"')
    if family: a.append(f'font-family="{family}"')
    if italic: a.append('font-style="italic"')
    if central: a.append('dominant-baseline="central"')
    return f'<text {" ".join(a)}{extra}>{s}</text>'


def math(s, size=None):
    sz = f' font-size="{size}"' if size else ""
    return f'<tspan font-family="{MATH}" font-style="italic"{sz}>{s}</tspan>'


def vsup(sign, size=13, after=""):
    """V^- / V^+ as tspans (no reliance on superscript glyphs); `after` returns to the baseline."""
    s = math("V", size) + f'<tspan dx="1.6" dy="-4.5" font-size="{size*0.66:.1f}">{sign}</tspan>'
    return s + (f'<tspan dy="4.5">{after}</tspan>' if after else "")


def rect(x, y, w, h, rx, fill, stroke, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def line(x1, y1, x2, y2, stroke, sw=1.2, cap="round"):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="{cap}"/>')


def arrow(fid, d, color="slate", sw=1.5, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{LINE[color]}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"{ds} marker-end="url(#{fid}-ah-{color})"/>')


def markers(fid):
    out = []
    for name, c in LINE.items():
        out.append(f'<marker id="{fid}-ah-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                   f'markerWidth="8.5" markerHeight="8.5" markerUnits="userSpaceOnUse" orient="auto">'
                   f'<path d="M0,0.8 L10,5 L0,9.2 L2.6,5 Z" fill="{c}"/></marker>')
    return "<defs>" + "".join(out) + "</defs>"


def chip(x, y, role, r=11, ghost=False):
    fill, stroke, ink = ROLE[role]
    fs = r * 1.28
    if ghost:
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="#B3BAC4" '
                f'stroke-width="1.1" stroke-dasharray="2.4 2"/>'
                + text(x, y + 0.5, role, fs, 600, "#A7AEB8", family=MATH, italic=True, central=True))
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
            + text(x, y + 0.5, role, fs, 600, ink, family=MATH, italic=True, central=True))


def diamond(cx, cy, dx, dy, r, edge, sw=1.6, letters=True):
    """The experience unit: requirement r linked to witness (I, A, O)."""
    p = {"r": (cx - dx, cy), "I": (cx, cy - dy), "A": (cx + dx, cy), "O": (cx, cy + dy)}
    out = [line(*p[a], *p[b], edge, sw) for a, b in (("r", "I"), ("I", "A"), ("A", "O"), ("O", "r"))]
    for k, (x, y) in p.items():
        if letters:
            out.append(chip(x, y, k, r))
        else:
            f, s, _ = ROLE[k]
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}" stroke="{s}" stroke-width="1.1"/>')
    return "".join(out), p


def est_width(s, size, k=0.54):
    return len(s) * size * k


def legend(right, y, size=11):
    items, gap, cr = list(ROLE), 14, 7.5
    widths = [2 * cr + 5 + est_width(ROLE_NAME[k], size) for k in items]
    x = right - sum(widths) - gap * (len(items) - 1)
    out = []
    for k, w in zip(items, widths):
        out.append(chip(x + cr, y, k, cr))
        out.append(text(x + 2 * cr + 5, y + 0.5, ROLE_NAME[k], size, 400, INK2, "start", central=True))
        x += w + gap
    return "".join(out)


def tick(x, y, s=1.0):
    return (f'<path d="M{x-4.2*s},{y+0.3*s} L{x-1.2*s},{y+3.4*s} L{x+4.6*s},{y-3.6*s}" fill="none" '
            f'stroke="{PASS}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(x, y, s=1.0):
    return (f'<path d="M{x-3.3*s},{y-3.3*s} L{x+3.3*s},{y+3.3*s} M{x+3.3*s},{y-3.3*s} L{x-3.3*s},{y+3.3*s}" '
            f'fill="none" stroke="{FAIL}" stroke-width="1.9" stroke-linecap="round"/>')


# ---------- icons (drawn at origin; place with translate/scale) ----------
def g(x, y, body, s=1.0):
    sc = f" scale({s})" if s != 1 else ""
    return f'<g transform="translate({x} {y}){sc}">{body}</g>'


def icon_repair(x, y, s=1.0):
    b = (rect(-8, -17, 22, 28, 3, "#EEF1F4", "#8C96A4", 1.1)
         + rect(-13, -12, 22, 28, 3, "#FFFFFF", INK2, 1.3)
         + line(-9, -5, 4, -5, PASS, 1.8) + line(-9, 0.5, 2, 0.5, FAIL, 1.8)
         + line(-9, 6, 5, 6, "#C3CAD3", 1.8) + line(-9, 11, 0, 11, "#C3CAD3", 1.8))
    return g(x, y, b, s)


def icon_issue(x, y, s=1.0):
    b = (f'<path d="M-11,-14 H5 L11,-8 V14 H-11 Z" fill="#FFFFFF" stroke="{INK2}" stroke-width="1.3" stroke-linejoin="round"/>'
         f'<path d="M5,-14 V-8 H11" fill="none" stroke="{INK2}" stroke-width="1.1" stroke-linejoin="round"/>'
         + line(-7, -6, 2, -6, "#C3CAD3", 1.8) + line(-7, -1, 6, -1, "#C3CAD3", 1.8)
         + line(-7, 4, 3, 4, "#C3CAD3", 1.8)
         + f'<circle cx="7" cy="11" r="6.5" fill="#FFFFFF" stroke="{INK2}" stroke-width="1.3"/>'
         f'<circle cx="7" cy="11" r="1.9" fill="{INK2}"/>')
    return g(x, y, b, s)


def icon_patch(x, y, s=1.0):
    b = (f'<path d="M-11,-14 H5 L11,-8 V14 H-11 Z" fill="#FFFFFF" stroke="{INK2}" stroke-width="1.3" stroke-linejoin="round"/>'
         f'<path d="M5,-14 V-8 H11" fill="none" stroke="{INK2}" stroke-width="1.1" stroke-linejoin="round"/>'
         + line(-7, -5, 4, -5, PASS, 1.8) + line(-7, 0.5, 2, 0.5, FAIL, 1.8)
         + line(-7, 6, 6, 6, PASS, 1.8))
    return g(x, y, b, s)


def icon_agent(x, y, s=1.0):
    b = (line(0, -12, 0, -17, INK2, 1.4)
         + f'<circle cx="0" cy="-19" r="2.4" fill="{INK2}"/>'
         + rect(-19.5, -4.5, 5, 9, 2, INK2, INK2, 0) + rect(14.5, -4.5, 5, 9, 2, INK2, INK2, 0)
         + rect(-16, -12, 32, 25, 8, "#E7EDF5", INK2, 1.4)
         + rect(-10.5, -6, 21, 11, 5.5, "#FFFFFF", INK2, 1.1)
         + f'<circle cx="-4.5" cy="-0.5" r="2" fill="{INK}"/><circle cx="4.5" cy="-0.5" r="2" fill="{INK}"/>')
    return g(x, y, b, s)


def icon_faiss(x, y):
    shades = [.75, .3, .55, .15, .9, .4,
              .2, .65, .35, .85, .25, .6,
              .5, .15, .8, .45, .7, .3,
              .9, .45, .25, .6, .2, .75]
    b = [rect(-22, -16, 44, 32, 4, "#FFFFFF", "#8C96A4", 1.1)]
    for i, o in enumerate(shades):
        cx, cy = -16.5 + (i % 6) * 6.2, -10.5 + (i // 6) * 6.2
        b.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="4.6" height="4.6" rx="1" fill="#3D649C" fill-opacity="{o}"/>')
    return g(x, y, "".join(b))


def icon_search(x, y):
    b = (f'<circle cx="-3" cy="-3" r="10" fill="#FFFFFF" stroke="{INK2}" stroke-width="1.6"/>'
         + line(-8, -6, 2, -6, "#9FB3D1", 1.8) + line(-8, -2, 0, -2, "#9FB3D1", 1.8)
         + line(-8, 2, 1, 2, "#9FB3D1", 1.8)
         + line(4.5, 4.5, 12, 12, INK2, 3))
    return g(x, y, b)


def icon_terminal(x, y):
    b = (rect(-20, -15, 40, 30, 4, "#F4F1FA", INK2, 1.3) + line(-20, -8, 20, -8, INK2, 1.1, "butt")
         + "".join(f'<circle cx="{-15.5 + i * 4.2}" cy="-11.5" r="1.2" fill="{INK2}"/>' for i in range(3))
         + f'<path d="M-13,-2 L-8,2 L-13,6" fill="none" stroke="{VIOLET}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
         + line(-5, 6.5, 3, 6.5, VIOLET, 1.7))
    return g(x, y, b)


def icon_shield(x, y):
    b = (f'<path d="M0,-15 L12,-10.5 V-1 C12,7 6.5,12.5 0,15.5 C-6.5,12.5 -12,7 -12,-1 V-10.5 Z" '
         f'fill="#E4F2E9" stroke="{PASS}" stroke-width="1.4" stroke-linejoin="round"/>' + tick(0, 0.5, 1.1))
    return g(x, y, b)


def icon_compose(x, y):
    fI, sI, tI = ROLE["I"]
    fA, sA, tA = ROLE["A"]
    b = (f'<path d="M-26,-12 H0 V12 H-26 Q-30,12 -30,8 V-8 Q-30,-12 -26,-12 Z" fill="{fI}" stroke="{sI}" stroke-width="1.3"/>'
         f'<path d="M0,-12 H26 Q30,-12 30,-8 V8 Q30,12 26,12 H0 Z" fill="{fA}" stroke="{sA}" stroke-width="1.3"/>'
         + text(-14, 0.5, "I", 15, 600, tI, family=MATH, italic=True, central=True)
         + text(15, 0.5, "A", 15, 600, tA, family=MATH, italic=True, central=True))
    return g(x, y, b)


def svg_open(w, h, fid, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" id="{fid}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}" font-family="{SANS}">' + markers(fid)
            + f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>')


# ---------- Figure 1: concept comparison ----------
def fig1():
    W, H, fid = 800, 362, "f1"
    o = [svg_open(W, H, fid, "Two rows share the same past repair, current issue, agent and patch. "
                  "(a) Retrieved advice passes the requirement as a sentence with no witness. "
                  "(b) ContextGraph recovers a linked witness, composes the historical input R(x,x) with the "
                  "current operation filter(field=x), and reruns the executable condition after each edit.")]

    # (a) Retrieved advice
    o.append(rect(6, 6, 788, 146, 9, "#F6F7F9", "#E0E4EA"))
    o.append(text(22, 28, "(a) Retrieved advice", 14.5, 600, anchor="start"))
    o.append(legend(782, 23))
    o.append(icon_repair(60, 55))
    o.append(text(60, 90, "Past repair", 13, 500))
    o.append(icon_issue(60, 113))
    o.append(text(60, 144, "Current issue", 13, 500))

    o.append(arrow(fid, "M86,55 H140", "amber"))
    o.append(text(113, 47, "summarize", 11.5, 400, AMBER_T))
    o.append(f'<path d="M155,37 H449 Q458,37 458,46 V64 Q458,73 449,73 H182 L164,85 L168,73 H155 '
             f'Q146,73 146,64 V46 Q146,37 155,37 Z" fill="#FFFFFF" stroke="#9AA3AF" stroke-width="1.2" stroke-linejoin="round"/>')
    o.append(chip(164, 55, "r", 8.5))
    o.append(text(179, 55.5, "“Range lookups must accept named tuples.”", 12.5, 400, INK, "start", central=True))
    for i, k in enumerate("IAO"):
        o.append(chip(486 + i * 23, 55, k, 8.5, ghost=True))
    o.append(text(509, 83, "no witness", 11, 400, INK3))
    o.append(arrow(fid, "M552,55 H612 C628,55 630,80 646,80", "amber"))
    o.append(text(603, 47, "text in context", 11.5, 400, AMBER_T))
    o.append(arrow(fid, "M86,113 H612 C628,113 630,96 646,96"))
    o.append(icon_agent(670, 88))
    o.append(text(670, 122, "Agent", 13, 500))
    o.append(arrow(fid, "M696,88 H731"))
    o.append(icon_patch(755, 88))
    o.append(text(755, 122, "Patch", 13, 500))

    # (b) ContextGraph
    o.append(rect(6, 160, 788, 196, 9, "#F2F6FB", "#CCD8E7"))
    o.append(text(22, 182, "(b) ContextGraph", 14.5, 600, anchor="start"))
    o.append(icon_repair(60, 220))
    o.append(text(60, 255, "Past repair", 13, 500))
    o.append(icon_issue(60, 312))
    o.append(text(60, 343, "Current issue", 13, 500))

    o.append(arrow(fid, "M86,220 H112", "amber"))
    o.append(text(99, 212, "store", 11.5, 400, AMBER_T))
    o.append(rect(118, 192, 168, 104, 8, "#FFFFFF", "#B8C3D1", 1.1, "4 3"))
    nbrs = {"n1": (137, 206), "n2": (267, 206), "n3": (139, 272), "n4": (267, 268)}
    d, p = diamond(202, 236, 38, 28, 11, AMBER, 1.8)
    for a, b in (("n1", "r"), ("n1", "I"), ("n2", "A"), ("n3", "O"), ("n4", "A")):
        o.append(line(*nbrs[a], *p[b], "#CDD3DB", 1.1))
    for x, y in nbrs.values():
        o.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#EDEFF2" stroke="#B9C0CA" stroke-width="1"/>')
    o.append(d)
    o.append(text(202, 289, "linked experience", 11, 400, INK2))
    o.append(arrow(fid, "M286,227 H332", "amber"))
    o.append(text(309, 219, "recover", 11.5, 400, AMBER_T))

    # executable condition card
    cx0 = 336
    o.append(rect(cx0, 188, 234, 124, 8, "#FFFFFF", INK2, 1.3))
    o.append(text(cx0 + 14, 207, "Executable condition", 12.5, 600, INK, "start"))
    o.append(chip(cx0 + 21, 227, "I", 8.5))
    o.append(text(cx0 + 36, 227.5, "R(lo, hi)", 11.5, 400, INK, "start", MONO, central=True))
    o.append(text(cx0 + 224, 227.5, "history", 10.5, 400, AMBER_T, "end", central=True))
    o.append(chip(cx0 + 21, 249, "A", 8.5))
    o.append(text(cx0 + 36, 249.5, "filter(field=x)", 11.5, 400, INK, "start", MONO, central=True))
    o.append(text(cx0 + 224, 249.5, "current", 10.5, 400, INK2, "end", central=True))
    o.append(line(cx0 + 12, 262, cx0 + 222, 262, RULE, 1, "butt"))
    o.append(f'<path d="M{cx0+17},{274} L{cx0+25},{279} L{cx0+17},{284} Z" fill="{INK2}"/>')
    o.append(text(cx0 + 36, 279.5,
                  f'<tspan fill="{ROLE["A"][2]}">filter(field__range=</tspan><tspan fill="{AMBER_T}" font-weight="600">R(x,x)</tspan>'
                  f'<tspan fill="{ROLE["A"][2]}">)</tspan>', 11.5, 500, INK, "start", MONO, central=True))
    o.append(chip(cx0 + 21, 299, "O", 8.5))
    o.append(text(cx0 + 36, 299.5, "query accepted · same rows", 11.5, 400, INK, "start", central=True))

    # current operation lane into the card's A row
    o.append(arrow(fid, "M86,312 H302 Q314,312 314,300 V261 Q314,249 326,249 H333"))
    o.append(text(200, 329, "locate operation", 11.5, 400, INK2))

    # execution loop
    o.append(arrow(fid, "M570,244 H646", "violet", dash="4 3"))
    o.append(text(608, 236, "observations", 11, 400, VIOLET))
    o.append(icon_agent(670, 244))
    o.append(text(670, 279, "Agent", 13, 500))
    o.append(arrow(fid, "M696,244 H731"))
    o.append(icon_patch(755, 244))
    o.append(text(755, 279, "Patch", 13, 500))
    o.append(arrow(fid, "M768,244 H778 Q786,244 786,252 V324 Q786,332 778,332 H467 Q459,332 459,324 V315",
                   "violet", dash="4 3"))
    o.append(text(626, 325, "rerun after each edit", 11.5, 400, VIOLET))
    o.append("</svg>")
    return W, H, "".join(o)


# ---------- Figure 2: method overview ----------
def fig2():
    W, H, fid = 800, 386, "f2"
    o = [svg_open(W, H, fid, "Build: a past repair becomes a requirement and witness, checked on the original and "
                  "repaired versions and linked into memory. Memory: a FAISS index and a context graph. Apply: the "
                  "current issue queries FAISS for the top three sources, graph joins recover their witnesses, the "
                  "historical input is composed with the current operation, executed on the working tree, and the "
                  "agent's submitted patch goes to the official verifier.")]

    # (A) Build source memory
    o.append(rect(6, 6, 788, 122, 9, "#FBF7EF", "#EBDDC5"))
    o.append(text(22, 28, "(A) Build source memory", 14.5, 600, anchor="start"))
    o.append(legend(782, 23))
    o.append(icon_repair(70, 64, 1.35))
    o.append(text(70, 112, "Past repair", 13, 500))
    o.append(arrow(fid, "M100,66 H192"))
    o.append(text(146, 58, "source writer", 11.5, 400, INK2))
    d, _ = diamond(252, 66, 34, 24, 10.5, INK2, 1.4)
    o.append(d)
    o.append(text(252, 112, "requirement + witness", 13, 500))
    o.append(arrow(fid, "M306,66 H430"))
    o.append(text(368, 58, "run on " + vsup("−", 12.5, ", ") + vsup("+", 12.5), 11.5, 400, INK2))
    for yy, sign, mark, word in ((52, "−", cross, "fails"), (80, "+", tick, "passes")):
        o.append(rect(436, yy - 10, 104, 20, 10, "#FFFFFF", "#D8CCB5", 1.1))
        o.append(text(452, yy + 0.5, vsup(sign, 13), 11, 400, INK, "start", central=True))
        o.append(mark(482, yy))
        o.append(text(494, yy + 0.5, word, 11.5, 400, INK2, "start", central=True))
    o.append(text(488, 112, "source checks", 13, 500))
    o.append(arrow(fid, "M544,66 H688 Q700,66 700,78 V151", "amber"))
    o.append(text(622, 58, "link", 11.5, 400, AMBER_T))

    # Memory strip
    o.append(rect(6, 136, 788, 86, 9, "#FFFFFF", "#CFD6DF"))
    o.append(text(22, 158, "Memory", 13, 600, anchor="start"))
    o.append(text(152, 174, "FAISS index", 12, 500, INK, "end"))
    o.append(text(152, 189, "Qwen3-Embedding-8B", 10.5, 400, INK3, "end"))
    o.append(icon_faiss(182, 178))
    o.append(arrow(fid, "M206,178 H304", "amber"))
    o.append(text(255, 170, "top-3 IDs", 11.5, 400, AMBER_T))
    cxs, cy, hits, new = [336, 406, 476, 556, 628, 700, 764], 178, {0, 1, 2}, 5
    o.append(rect(310, 152, 192, 52, 14, "#FDF5E8", AMBER, 1.2, "4 3"))
    for a, b in zip(cxs, cxs[1:]):
        o.append(line(a + 18, cy, b - 18, cy, "#C9D0D9", 1.1))
    o.append(f'<path d="M556,165 Q628,141 700,165" fill="none" stroke="#C9D0D9" stroke-width="1.1"/>')
    o.append(f'<path d="M628,191 Q696,215 764,191" fill="none" stroke="#C9D0D9" stroke-width="1.1"/>')
    for i, x in enumerate(cxs):
        if i == new:
            o.append(f'<circle cx="{x}" cy="{cy}" r="23" fill="#FFFFFF" stroke="{INK3}" stroke-width="1" stroke-dasharray="3 2.5"/>')
        d, _ = diamond(x, cy, 13, 13, 5, AMBER if i in hits else ("#6D7888" if i == new else "#C3CAD3"),
                       1.4 if i in hits else 1.1, letters=False)
        o.append(d)
    o.append(text(596, 215, "context graph", 11.5, 400, INK2))

    # (B) Apply memory
    o.append(rect(6, 230, 788, 150, 9, "#F3F6FA", "#D9E1EB"))
    o.append(text(22, 252, "(B) Apply memory", 14.5, 600, anchor="start"))
    o.append(arrow(fid, "M182,294 V196"))
    o.append(text(190, 252, "query", 11.5, 400, INK2, "start"))
    o.append(arrow(fid, "M336,204 V292", "amber"))
    o.append(text(344, 252, math("r", 13) + ", " + math("W", 13) + ", relations", 11.5, 400, AMBER_T, "start"))

    Y, LY, SY = 312, 350, 364
    o.append(icon_issue(60, Y, 1.2))
    o.append(text(60, LY, "Current issue", 13, 500))
    o.append(text(60, SY, "+ repository", 11, 400, INK2))
    o.append(arrow(fid, f"M88,{Y} H156"))
    o.append(chip(101, Y - 11, "A", 7))
    o.append(text(112, Y - 10.5, "operation", 11, 400, INK2, "start", central=True))
    o.append(icon_search(182, Y))
    o.append(text(182, LY, "Retrieve", 13, 500))
    o.append(text(182, SY, "top-3, same repo", 11, 400, INK2))
    d, _ = diamond(336, Y, 15, 14, 5.5, AMBER, 1.5, letters=False)
    o.append(d)
    o.append(text(336, LY, "Graph join", 13, 500))
    o.append(text(336, SY, "full witness", 11, 400, INK2))
    o.append(arrow(fid, f"M360,{Y} H414", "amber"))
    o.append(icon_compose(450, Y))
    o.append(text(450, LY, "Compose", 13, 500))
    o.append(text(450, SY, "history " + math("I", 12) + " + current " + math("A", 12), 11, 400, INK2))
    o.append(arrow(fid, f"M486,{Y} H538"))
    o.append(text(512, Y - 8, "condition", 11, 400, INK2))
    o.append(icon_terminal(566, Y))
    o.append(text(566, LY, "Execute", 13, 500))
    o.append(text(566, SY, "on working tree", 11, 400, INK2))
    o.append(arrow(fid, f"M592,{Y} H652", "violet", dash="4 3"))
    o.append(text(622, Y - 8, "observations", 11, 400, VIOLET))
    o.append(icon_agent(680, Y + 2))
    o.append(text(680, LY, "Agent", 13, 500))
    o.append(text(680, SY, "edits the patch", 11, 400, INK2))
    o.append(arrow(fid, "M690,296 V288 Q690,280 682,280 H574 Q566,280 566,288 V295", "violet", dash="4 3"))
    o.append(text(628, 273, "rerun after edits", 11, 400, VIOLET))
    o.append(arrow(fid, f"M705,{Y} H740"))
    o.append(text(722, Y - 8, "submit", 11, 400, INK2))
    o.append(icon_shield(760, Y))
    o.append(text(760, LY, "Verifier", 13, 500))
    o.append(text(760, SY, "official", 11, 400, INK2))
    o.append("</svg>")
    return W, H, "".join(o)


# ---------- output ----------
def find_chrome():
    hits = sorted(glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell")))
    return hits[-1] if hits else None


STATIC_FONTS = ("https://fonts.googleapis.com/css?family=IBM+Plex+Sans:400,500,600"
                "|IBM+Plex+Mono:400,500,600|STIX+Two+Text:400,600,400i,600i")


def static_font_css():
    """Google serves static per-weight TTFs to non-browser clients. Chromium embeds those as
    TrueType in the PDF; the variable woff2 it gets as a browser would be embedded as Type 3."""
    import urllib.request
    try:
        with urllib.request.urlopen(STATIC_FONTS, timeout=20) as r:
            css = r.read().decode()
        return f"<style>{css}</style>" if ".ttf" in css else f'<link rel="stylesheet" href="{FONTS}">'
    except OSError:
        return f'<link rel="stylesheet" href="{FONTS}">'


def export(name, w, h, svg, chrome, font_css):
    page = (f'<!doctype html><html><head><meta charset="utf-8">{font_css}'
            f'<style>@page{{size:{w}px {h}px;margin:0}}html,body{{margin:0;padding:0;background:#fff}}'
            f'svg{{display:block}}</style></head><body>{svg}</body></html>')
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / f"{name}.html"
        src.write_text(page, encoding="utf-8")
        common = [chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                  "--virtual-time-budget=15000", "--run-all-compositor-stages-before-draw"]
        subprocess.run(common + ["--no-pdf-header-footer", "--print-to-pdf-no-header",
                                 f"--print-to-pdf={HERE / (name + '.pdf')}", src.as_uri()],
                       check=True, capture_output=True)
        subprocess.run(common + [f"--window-size={w},{h}", "--force-device-scale-factor=3",
                                 f"--screenshot={HERE / (name + '.png')}", src.as_uri()],
                       check=True, capture_output=True)


def main():
    figs = {"fig1-concept": fig1(), "fig2-overview": fig2()}
    for name, (w, h, svg) in figs.items():
        (HERE / f"{name}.svg").write_text(svg + "\n", encoding="utf-8")
    tpl = (HERE / "page.template.html").read_text(encoding="utf-8")
    page = tpl.replace("{{FIG1}}", figs["fig1-concept"][2]).replace("{{FIG2}}", figs["fig2-overview"][2])
    (HERE / "index.html").write_text(page, encoding="utf-8")
    if "--no-export" in sys.argv:
        return
    chrome = find_chrome()
    if not chrome:
        sys.exit("headless Chromium not found; rerun with --no-export or install playwright chromium")
    font_css = static_font_css()
    for name, (w, h, svg) in figs.items():
        export(name, w, h, svg, chrome, font_css)
        print(f"wrote {name}.svg/.pdf/.png ({w}x{h})")


if __name__ == "__main__":
    main()
