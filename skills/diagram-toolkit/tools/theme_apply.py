#!/usr/bin/env python3
"""Applique un thème (JSON) à un template de diagramme en remplaçant les placeholders.

Usage:
    python theme_apply.py --input diagram.mmd --theme mckinsey --output out.mmd
"""
import argparse
import json
from pathlib import Path

THEMES_DIR = Path(__file__).parent.parent / "themes"


def load_theme(name: str) -> dict:
    path = THEMES_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Theme not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def apply_theme(content: str, theme: dict) -> str:
    mapping = {
        "{{PRIMARY}}": theme.get("primary", "#002060"),
        "{{SECONDARY}}": theme.get("secondary", "#0F62FE"),
        "{{ACCENT}}": theme.get("accent", "#F0A500"),
        "{{NEUTRAL}}": theme.get("neutral", "#6C6C6C"),
        "{{BACKGROUND}}": theme.get("background", "#FFFFFF"),
        "{{TEXT}}": theme.get("text", "#1A1A1A"),
        "{{FONT_FAMILY}}": theme.get("font_family", "Inter, sans-serif"),
        "{{SHADOW}}": theme.get("shadow", "0 2px 8px rgba(0,0,0,0.08)"),
        "{{SHADOW_LG}}": theme.get("shadow_lg", "0 8px 24px rgba(0,0,0,0.12)"),
        "{{BORDER_RADIUS}}": theme.get("border_radius", "8px"),
        "{{HEADER_GRADIENT}}": theme.get("header_gradient", "linear-gradient(135deg, #002060, #0F62FE)"),
        "{{CARD_BG}}": theme.get("card_bg", "#F8F9FA"),
        "{{BORDER_COLOR}}": theme.get("border_color", "#E5E7EB"),
        "{{LETTER_SPACING}}": theme.get("letter_spacing", "0.02em"),
    }
    for k, v in mapping.items():
        content = content.replace(k, v)
    return content


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--theme", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    theme = load_theme(args.theme)
    content = Path(args.input).read_text(encoding="utf-8")
    Path(args.output).write_text(apply_theme(content, theme), encoding="utf-8")
    print(f"[OK] Theme '{args.theme}' applied -> {args.output}")


if __name__ == "__main__":
    main()
