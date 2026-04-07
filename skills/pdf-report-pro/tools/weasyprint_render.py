#!/usr/bin/env python3
"""
Rendu HTML -> PDF via WeasyPrint (défaut) avec fallback Playwright puis send_report.py.

Usage:
    python weasyprint_render.py input.html output.pdf
"""
import sys
from pathlib import Path

def render_weasyprint(html_path: Path, pdf_path: Path) -> bool:
    try:
        from weasyprint import HTML, CSS
        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        return True
    except Exception as e:
        print(f"[weasyprint KO] {e}", file=sys.stderr)
        return False

def render_playwright(html_path: Path, pdf_path: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file:///{html_path.resolve().as_posix()}")
            page.pdf(path=str(pdf_path), format="A4", margin={"top": "2.5cm", "right": "2.5cm", "bottom": "3cm", "left": "2.5cm"})
            browser.close()
        return True
    except Exception as e:
        print(f"[playwright KO] {e}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: weasyprint_render.py input.html output.pdf")
        sys.exit(1)
    html_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2])
    if render_weasyprint(html_path, pdf_path):
        print(f"[OK weasyprint] {pdf_path}")
        return
    if render_playwright(html_path, pdf_path):
        print(f"[OK playwright fallback] {pdf_path}")
        return
    print("[FAIL] Aucun moteur de rendu disponible. Fallback Markdown via send_report.py requis.", file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()
