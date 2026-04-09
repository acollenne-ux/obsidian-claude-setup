#!/usr/bin/env python3
"""Valide basiquement la syntaxe d'un fichier diagramme (présence des blocs attendus).

Usage:
    python validate_diagram.py --input diagram.mmd
"""
import argparse
import re
import sys
from pathlib import Path


def detect_type(path: Path) -> str:
    ext = path.suffix.lower()
    return {".mmd": "mermaid", ".d2": "d2", ".dot": "graphviz", ".typ": "typst", ".html": "html"}.get(ext, "unknown")


def validate_mermaid(content: str) -> list[str]:
    errors = []
    keywords = ["graph", "flowchart", "sequenceDiagram", "gantt", "quadrantChart", "mindmap", "classDiagram", "erDiagram", "stateDiagram"]
    if not any(k in content for k in keywords):
        errors.append("No recognized Mermaid diagram keyword found")
    if re.search(r"\{\{[A-Z_]+\}\}", content):
        errors.append("Unfilled placeholders detected (e.g. {{VAR}})")
    return errors


def validate_graphviz(content: str) -> list[str]:
    errors = []
    if "digraph" not in content and "graph " not in content:
        errors.append("No 'digraph' or 'graph' keyword found")
    if content.count("{") != content.count("}"):
        errors.append("Unbalanced braces")
    return errors


def validate_d2(content: str) -> list[str]:
    errors = []
    if not content.strip():
        errors.append("Empty D2 file")
    return errors


def validate_typst(content: str) -> list[str]:
    errors = []
    if "#" not in content:
        errors.append("No Typst directive found")
    return errors


def validate_html(content: str) -> list[str]:
    errors = []
    if "<html" not in content.lower() and "<!doctype" not in content.lower():
        errors.append("No HTML document structure found")
    if re.search(r"\{\{[A-Z_]+\}\}", content):
        errors.append("Unfilled placeholders detected (e.g. {{VAR}})")
    return errors


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    args = p.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    diagram_type = detect_type(path)

    validators = {
        "mermaid": validate_mermaid,
        "graphviz": validate_graphviz,
        "d2": validate_d2,
        "typst": validate_typst,
        "html": validate_html,
    }
    if diagram_type not in validators:
        print(f"[ERROR] Unknown diagram type: {path.suffix}")
        sys.exit(1)

    errors = validators[diagram_type](content)
    if errors:
        print(f"[FAIL] {diagram_type}: {len(errors)} issue(s)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"[OK] {diagram_type} syntax valid: {path}")


if __name__ == "__main__":
    main()
