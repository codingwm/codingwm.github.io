"""Scaling plots for the 8/31 updates page — values hardcoded below.

    uv run --with matplotlib python make_0831_plots.py
        ->  assets/rubric-scaling-swe.png
        ->  assets/rubric-scaling-mle.png

Style copied from cwm-agent/plot_scaling.py (commit 837d519). That script reads the
real grading reports; this one hardcodes the numbers so the site repo stays
self-contained. When real numbers land, regenerate from cwm-agent instead.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

# palette (dataviz reference instance, light mode)
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SERIES = "#e1e0d9", "#c3c2b7", "#2a78d6"

# Hand-edit the resolved counts below, then rerun this script. Every value is a
# whole-number count out of `total`; the percent is computed, and labels show both.

# SWE-bench Verified (cwm10/cwm100/baseline match the official grading reports in cwm-agent).
SWE = {
    "sizes": [15, 227, 1006],
    "counts": [58, 56, 185],  # resolved instances per rubric-library size
    "baseline_count": 362,  # interpreter feedback (haiku45-final.json)
    "total": 500,
    "ylabel": "SWE-bench Verified resolved (%)",
    "title": "SWE-bench Verified — resolve rate vs rubric library size",
    "subtitle": "Haiku 4.5 agent, 500 instances per point, top-15 retrieval, Opus 5 grader",
    "xlim": (10, 1500),
    "out": "assets/rubric-scaling-swe.png",
}

# MLE-bench Lite.
MLE = {
    "sizes": [10, 100, 1000],
    "counts": [1, 2, 6],  # medals per rubric-library size
    "baseline_count": 9,  # interpreter feedback
    "total": 22,
    "ylabel": "MLE-bench Lite medal rate (%)",
    "title": "MLE-bench Lite — medal rate vs rubric library size",
    "subtitle": "Haiku 4.5 agent, 22 Lite competitions per point, Opus 5 grader",
    "xlim": (7, 1500),
    "out": "assets/rubric-scaling-mle.png",
}


def draw(spec: dict):
    sizes, counts, total = spec["sizes"], spec["counts"], spec["total"]
    rates = [100 * c / total for c in counts]
    baseline = 100 * spec["baseline_count"] / total

    fig, ax = plt.subplots(figsize=(7, 4.4), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    # reference line: interpreter feedback (real execution)
    ax.axhline(baseline, color=AXIS, lw=1.5, ls=(0, (5, 4)), zorder=1)
    ax.annotate(
        f"Interpreter feedback (real execution)  {baseline:.1f}%  ({spec['baseline_count']}/{total})",
        xy=(sizes[0], baseline), xytext=(0, 8), textcoords="offset points",
        color=INK2, fontsize=9.5, va="bottom",
    )

    # the CWM series
    ax.plot(sizes, rates, color=SERIES, lw=2, marker="o", ms=9,
            mfc=SERIES, mec=SURFACE, mew=2, zorder=3)
    for s, r, c in zip(sizes, rates, counts):
        ax.annotate(f"{r:.1f}%\n{c}/{total}", xy=(s, r), xytext=(0, 11),
                    textcoords="offset points", ha="center", va="bottom",
                    color=INK, fontsize=10, linespacing=1.3)

    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator(sizes))
    ax.set_xticklabels([str(s) for s in sizes])
    ax.set_xlim(*spec["xlim"])
    ax.set_ylim(0, 80)
    ax.set_xlabel("Rubric library size (criteria available to retrieval)", color=INK2, fontsize=10)
    ax.set_ylabel(spec["ylabel"], color=INK2, fontsize=10)

    ax.set_title(spec["title"], color=INK, fontsize=12, loc="left", pad=16)
    ax.text(0, 1.02, spec["subtitle"], transform=ax.transAxes, color=MUTED, fontsize=9)

    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(axis="y", color=GRID, lw=0.75)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)

    out = Path(spec["out"])
    out.parent.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, facecolor=SURFACE, bbox_inches="tight")
    print(f"wrote {out}: sizes={sizes} rates={[f'{r:.1f}' for r in rates]} baseline={baseline:.1f}")


if __name__ == "__main__":
    draw(SWE)
    draw(MLE)
