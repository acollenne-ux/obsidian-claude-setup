#!/usr/bin/env python3
"""
annotate.py — Dessine les bbox d'anomalies (geom.json) sur les PNG rasterisés.

Usage:
    python annotate.py --pages <dir> --anomalies geom.json --out <dir>
"""

import argparse
import json
import sys
from pathlib import Path

SEVERITY_COLORS = {
    "critical": (220, 38, 38),
    "high": (234, 88, 12),
    "medium": (234, 179, 8),
    "low": (59, 130, 246),
}


def main() -> int:
    from PIL import Image, ImageDraw, ImageFont

    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", required=True, help="Dossier PNG rasterisés")
    ap.add_argument("--anomalies", required=True, help="geom.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dpi", type=int, default=200)
    args = ap.parse_args()

    data = json.loads(Path(args.anomalies).read_text(encoding="utf-8"))
    pages_dir = Path(args.pages)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    by_page: dict[int, list] = {}
    for a in data.get("anomalies", []):
        by_page.setdefault(a["page"], []).append(a)

    scale = args.dpi / 72.0
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()

    pngs = sorted(pages_dir.glob("page-*.png"))
    for idx, png in enumerate(pngs, start=1):
        img = Image.open(png).convert("RGB")
        draw = ImageDraw.Draw(img, "RGBA")
        for a in by_page.get(idx, []):
            x, y, w, h = a["bbox"]
            x1 = x * scale
            y1 = y * scale
            x2 = (x + w) * scale
            y2 = (y + h) * scale
            color = SEVERITY_COLORS.get(a["severity"], (200, 200, 200))
            draw.rectangle([x1, y1, x2, y2],
                           outline=color + (255,), width=3,
                           fill=color + (40,))
            label = f"{a['issue']} [{a['severity']}]"
            draw.text((x1 + 4, y1 + 4), label, fill=color + (255,), font=font)
        dst = out_dir / png.name
        img.save(dst)
        print(f"annotated: {dst}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
