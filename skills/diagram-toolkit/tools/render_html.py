#!/usr/bin/env python3
"""Render HTML diagram files to PNG, PDF, or SVG via Playwright (Chromium headless)."""

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def parse_args():
    parser = argparse.ArgumentParser(description="Render HTML diagrams to PNG/PDF/SVG")
    parser.add_argument("--input", "-i", required=True, help="Path to the HTML file")
    parser.add_argument(
        "--format", "-f", default="png", help="Comma-separated formats: png,pdf,svg"
    )
    parser.add_argument(
        "--output", "-o", default=".", help="Output directory (default: current dir)"
    )
    return parser.parse_args()


def render_png(page, output_path: Path):
    """Screenshot body element at 2x scale (retina)."""
    body = page.query_selector("body")
    if not body:
        print(f"[ERROR] PNG: no <body> element found")
        return False
    box = body.bounding_box()
    if not box:
        print(f"[ERROR] PNG: could not get body bounding box")
        return False
    page.screenshot(
        path=str(output_path),
        clip={"x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"]},
        scale="device",
    )
    print(f"[OK] PNG generated: {output_path}")
    return True


def render_pdf(page, output_path: Path):
    """Print to PDF in landscape A4 with background colors."""
    page.pdf(
        path=str(output_path),
        format="A4",
        landscape=True,
        print_background=True,
        margin={"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
    )
    print(f"[OK] PDF generated: {output_path}")
    return True


def render_svg(page, output_path: Path):
    """Attempt DOM serialization of .diagram-container or fallback to body."""
    svg_content = page.evaluate("""() => {
        const container = document.querySelector('.diagram-container');
        const target = container || document.body;
        const svg = target.querySelector('svg');
        if (svg) return svg.outerHTML;
        // Fallback: serialize inner HTML
        return target.innerHTML;
    }""")
    if not svg_content or not svg_content.strip():
        print(f"[ERROR] SVG: no content found to serialize")
        return False
    output_path.write_text(svg_content, encoding="utf-8")
    print(f"[OK] SVG generated: {output_path}")
    return True


RENDERERS = {
    "png": render_png,
    "pdf": render_pdf,
    "svg": render_svg,
}


def main():
    args = parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.is_file():
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(1)

    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    formats = [f.strip().lower() for f in args.format.split(",")]
    invalid = [f for f in formats if f not in RENDERERS]
    if invalid:
        print(f"[ERROR] Unsupported format(s): {', '.join(invalid)}. Use: png, pdf, svg")
        sys.exit(1)

    stem = input_path.stem
    file_url = input_path.as_uri()

    errors = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1600, "height": 900},
            device_scale_factor=2,
        )

        try:
            page.goto(file_url, wait_until="networkidle")
            page.evaluate("() => document.fonts.ready")
            page.wait_for_timeout(300)  # small settle for CSS animations
        except Exception as e:
            print(f"[ERROR] Failed to load {input_path}: {e}")
            browser.close()
            sys.exit(1)

        for fmt in formats:
            out_file = output_dir / f"{stem}.{fmt}"
            try:
                success = RENDERERS[fmt](page, out_file)
                if not success:
                    errors += 1
            except Exception as e:
                print(f"[ERROR] {fmt.upper()} render failed: {e}")
                errors += 1

        browser.close()

    if errors:
        print(f"\n[WARN] {errors} format(s) failed out of {len(formats)}")
        sys.exit(1)
    else:
        print(f"\n[OK] All {len(formats)} format(s) rendered successfully")


if __name__ == "__main__":
    main()
