"""typst_render.py — Moteur de rendu PDF principal (Typst 0.14+)

Usage:
    python typst_render.py <input.typ> <output.pdf>

Si typst n'est pas installé, fallback automatique vers WeasyPrint puis Playwright.
Typst 0.14 produit des PDF taggés (PDF/UA) nativement.
"""
from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path


def find_typst() -> str | None:
    found = shutil.which("typst")
    if found:
        return found
    # Fallback : winget install path (PATH pas rechargé sans redémarrage shell)
    candidates = [
        Path.home() / "AppData/Local/Microsoft/WinGet/Packages/Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe/typst-x86_64-pc-windows-msvc/typst.exe",
        Path.home() / "AppData/Local/Microsoft/WinGet/Links/typst.exe",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return None


def render_typst(src: Path, out: Path) -> bool:
    typst = find_typst()
    if not typst:
        return False
    cmd = [typst, "compile", "--pdf-standard", "a-3b", str(src), str(out)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode == 0 and out.exists():
            print(f"[OK] Typst -> {out}")
            return True
        # Retry sans pdf-standard si version trop ancienne
        r = subprocess.run([typst, "compile", str(src), str(out)],
                           capture_output=True, text=True, timeout=120)
        if r.returncode == 0 and out.exists():
            print(f"[OK] Typst (no PDF/A) -> {out}")
            return True
        print(f"[ERR] Typst: {r.stderr}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERR] Typst exception: {e}", file=sys.stderr)
        return False


def fallback_weasyprint(html_src: Path, out: Path) -> bool:
    try:
        from weasyprint import HTML  # type: ignore
        HTML(filename=str(html_src)).write_pdf(str(out))
        print(f"[OK] WeasyPrint fallback -> {out}")
        return True
    except Exception as e:
        print(f"[WARN] WeasyPrint indisponible: {e}", file=sys.stderr)
        return False


def fallback_playwright(html_src: Path, out: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page()
            page.goto(html_src.absolute().as_uri())
            page.pdf(path=str(out), format="A4", print_background=True,
                     margin={"top": "2.5cm", "bottom": "2.5cm", "left": "2.5cm", "right": "2.5cm"})
            b.close()
        print(f"[OK] Playwright fallback -> {out}")
        return True
    except Exception as e:
        print(f"[ERR] Playwright fallback: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) != 3:
        print("Usage: typst_render.py <input> <output.pdf>")
        sys.exit(1)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)

    if src.suffix == ".typ":
        if render_typst(src, out):
            return
        print("[INFO] Typst absent — installer via 'winget install Typst.Typst' pour activer le moteur principal")
        sys.exit(2)
    elif src.suffix in (".html", ".htm"):
        if fallback_weasyprint(src, out):
            return
        if fallback_playwright(src, out):
            return
        sys.exit(3)
    else:
        print(f"[ERR] Format non supporté: {src.suffix}")
        sys.exit(4)


if __name__ == "__main__":
    main()
