#!/usr/bin/env python3
"""Rendu multi-format de diagrammes (Mermaid / D2 / Graphviz / Typst).

Détecte automatiquement le type via l'extension, applique le thème, puis exporte en
SVG, PNG (2x) et PDF (A4 paysage) via le CLI approprié. Fallback Mermaid via npx.

Usage:
    python render.py --input diagram.mmd --format svg,png,pdf --theme mckinsey --output ./out/
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

THEME_APPLY = Path(__file__).parent / "theme_apply.py"
VALIDATE = Path(__file__).parent / "validate_diagram.py"


def detect_type(path: Path) -> str:
    return {".mmd": "mermaid", ".d2": "d2", ".dot": "graphviz", ".typ": "typst", ".html": "html"}.get(
        path.suffix.lower(), "unknown"
    )


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def run(args: list[str]) -> int:
    print(f"[CMD] {' '.join(args)}")
    return subprocess.call(args, shell=(sys.platform == "win32"))


def render_mermaid(src: Path, out_dir: Path, fmts: list[str], theme: str) -> list[Path]:
    outputs = []
    cli = which("mmdc") or which("mmdc.cmd")
    base_cmd = [cli] if cli else ["npx", "-y", "@mermaid-js/mermaid-cli"]
    # Charger les mermaid_theme_variables depuis le thème JSON
    theme_path = Path(__file__).parent.parent / "themes" / f"{theme}.json"
    mermaid_vars = {"fontFamily": "Inter, sans-serif"}
    if theme_path.exists():
        theme_data = json.loads(theme_path.read_text(encoding="utf-8"))
        mermaid_vars = theme_data.get("mermaid_theme_variables", mermaid_vars)
    theme_cfg = out_dir / f"_theme_{theme}.json"
    theme_cfg.write_text(
        json.dumps({"theme": "base", "themeVariables": mermaid_vars}),
        encoding="utf-8",
    )
    for fmt in fmts:
        out = out_dir / f"{src.stem}.{fmt}"
        cmd = base_cmd + ["-i", str(src), "-o", str(out), "-c", str(theme_cfg)]
        if fmt == "png":
            cmd += ["-s", "2"]
        if run(cmd) == 0 and out.exists():
            outputs.append(out)
    return outputs


def render_d2(src: Path, out_dir: Path, fmts: list[str]) -> list[Path]:
    cli = which("d2")
    if not cli:
        print("[WARN] d2 not found, skipping")
        return []
    outputs = []
    for fmt in fmts:
        if fmt == "pdf":
            continue  # d2 does not export PDF natively
        out = out_dir / f"{src.stem}.{fmt}"
        if run([cli, str(src), str(out)]) == 0:
            outputs.append(out)
    return outputs


def render_graphviz(src: Path, out_dir: Path, fmts: list[str]) -> list[Path]:
    cli = which("dot")
    if not cli:
        # Fallback : tenter rendu HTML si un template .html existe pour ce diagramme
        html_template = Path(__file__).parent.parent / "templates" / f"{src.stem}.html"
        if html_template.exists():
            print(f"[INFO] dot not found, falling back to HTML template: {html_template.name}")
            return render_html(html_template, out_dir, fmts)
        # Dernier recours : Mermaid graph (conversion basique)
        print("[WARN] graphviz/dot not found, falling back to Mermaid")
        mmd_fallback = out_dir / f"{src.stem}.mmd"
        content = src.read_text(encoding="utf-8")
        # Conversion basique digraph → Mermaid graph TD
        mmd_content = "graph TD\n"
        import re as _re
        for m in _re.finditer(r'"([^"]+)"\s*->\s*"([^"]+)"', content):
            mmd_content += f'    {m.group(1).replace(" ", "_")}["{m.group(1)}"] --> {m.group(2).replace(" ", "_")}["{m.group(2)}"]\n'
        mmd_fallback.write_text(mmd_content, encoding="utf-8")
        return render_mermaid(mmd_fallback, out_dir, fmts, "mckinsey")
    outputs = []
    for fmt in fmts:
        out = out_dir / f"{src.stem}.{fmt}"
        if run([cli, f"-T{fmt}", str(src), "-o", str(out)]) == 0:
            outputs.append(out)
    return outputs


def render_html(src: Path, out_dir: Path, fmts: list[str]) -> list[Path]:
    """Rend un diagramme HTML via Playwright (PNG @2x, PDF A4 paysage)."""
    render_html_script = Path(__file__).parent / "render_html.py"
    if not render_html_script.exists():
        print("[ERROR] render_html.py not found")
        return []
    fmt_arg = ",".join(fmts)
    cmd = [sys.executable, str(render_html_script), "--input", str(src),
           "--format", fmt_arg, "--output", str(out_dir)]
    if run(cmd) != 0:
        print("[ERROR] HTML rendering failed")
        return []
    outputs = []
    for fmt in fmts:
        out = out_dir / f"{src.stem}.{fmt}"
        if out.exists():
            outputs.append(out)
    return outputs


def render_typst(src: Path, out_dir: Path, fmts: list[str]) -> list[Path]:
    cli = which("typst")
    if not cli:
        print("[WARN] typst not found, skipping")
        return []
    outputs = []
    for fmt in fmts:
        if fmt not in ("pdf", "svg", "png"):
            continue
        out = out_dir / f"{src.stem}.{fmt}"
        if run([cli, "compile", "--format", fmt, str(src), str(out)]) == 0:
            outputs.append(out)
    return outputs


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--format", default="svg,png,pdf")
    p.add_argument("--theme", default="mckinsey")
    p.add_argument("--output", default="./out/")
    args = p.parse_args()

    src = Path(args.input).resolve()
    out_dir = Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    fmts = [f.strip() for f in args.format.split(",")]

    # Apply theme
    themed = out_dir / src.name
    subprocess.call([sys.executable, str(THEME_APPLY), "--input", str(src),
                     "--theme", args.theme, "--output", str(themed)])

    # Validate
    subprocess.call([sys.executable, str(VALIDATE), "--input", str(themed)])

    # Render
    diagram_type = detect_type(themed)
    renderers = {
        "mermaid": lambda: render_mermaid(themed, out_dir, fmts, args.theme),
        "d2": lambda: render_d2(themed, out_dir, fmts),
        "graphviz": lambda: render_graphviz(themed, out_dir, fmts),
        "typst": lambda: render_typst(themed, out_dir, fmts),
        "html": lambda: render_html(themed, out_dir, fmts),
    }
    if diagram_type not in renderers:
        print(f"[ERROR] Unsupported type: {src.suffix}")
        sys.exit(1)

    outputs = renderers[diagram_type]()
    print(f"\n[DONE] {len(outputs)} file(s) generated:")
    for o in outputs:
        print(f"  - {o}")


if __name__ == "__main__":
    main()
