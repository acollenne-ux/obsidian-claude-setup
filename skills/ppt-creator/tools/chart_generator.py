#!/usr/bin/env python3
"""Chart Tufte-compliant pour ppt-creator. Voir pdf-report-pro/tools/chart_generator.py."""
import sys
from pathlib import Path

PRIMARY = "#0B3D91"

def main():
    args = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    data = [float(x) for x in args.get("data", "1,2,3").split(",")]
    kind = args.get("kind", "line")
    out = Path(args.get("out", "chart.png"))
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    if kind == "bar":
        ax.bar(range(len(data)), data, color=PRIMARY, edgecolor="none")
    else:
        ax.plot(data, color=PRIMARY, linewidth=1.8)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.grid(False); ax.set_facecolor("white")
    fig.tight_layout(); fig.savefig(out, dpi=300, bbox_inches="tight"); plt.close(fig)
    print(f"[OK] {out}")

if __name__ == "__main__":
    main()
