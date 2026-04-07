#!/usr/bin/env python3
"""
Générateur de charts Tufte-compliant (data-ink ratio strict).
Usage: python chart_generator.py kind=line data=1,2,3 out=chart.png
"""
import sys
from pathlib import Path

PRIMARY = "#0B3D91"
ACCENT = "#E63946"

def tufte_style(ax):
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#B0B0B0")
    ax.spines["bottom"].set_color("#B0B0B0")
    ax.tick_params(colors="#4A4A4A")
    ax.grid(False)
    ax.set_facecolor("white")

def make_chart(kind: str, data: list[float], out: Path, title: str = ""):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    if kind == "line":
        ax.plot(data, color=PRIMARY, linewidth=1.8)
    elif kind == "bar":
        ax.bar(range(len(data)), data, color=PRIMARY, edgecolor="none")
    else:
        ax.plot(data, color=PRIMARY)
    if title:
        ax.set_title(title, fontsize=11, color="#1A1A1A", loc="left", pad=12)
    tufte_style(ax)
    fig.tight_layout()
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)

def main():
    args = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    kind = args.get("kind", "line")
    data = [float(x) for x in args.get("data", "1,2,3").split(",")]
    out = Path(args.get("out", "chart.png"))
    title = args.get("title", "")
    make_chart(kind, data, out, title)
    print(f"[OK] {out}")

if __name__ == "__main__":
    main()
