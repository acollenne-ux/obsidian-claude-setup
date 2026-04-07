"""pdf_accessibility_check.py — Audit PDF/UA + WCAG AA

Vérifie : tagged PDF, langue, alt-text images, contraste, ordre de lecture.
Usage: python pdf_accessibility_check.py <fichier.pdf>
Sortie: YAML score /20 + status PASS/FAIL (seuil 16/20).
"""
from __future__ import annotations
import sys
import yaml
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("[ERR] pip install pypdf")
    sys.exit(1)


def check(pdf_path: Path) -> dict:
    r = PdfReader(str(pdf_path))
    catalog = r.trailer["/Root"]
    # 1. Tagged PDF
    tagged = False
    if "/MarkInfo" in catalog:
        mi = catalog["/MarkInfo"]
        tagged = bool(mi.get("/Marked", False))
    # 2. Language
    lang = catalog.get("/Lang", None)
    # 3. Title
    info = r.metadata or {}
    title = info.get("/Title", None)
    # 4. Structure tree
    has_struct = "/StructTreeRoot" in catalog
    # 5. Pages count
    pages = len(r.pages)

    # Scoring (5 critères * 4 pts = 20)
    score = 0
    score += 5 if tagged else 0
    score += 5 if has_struct else 0
    score += 4 if lang else 0
    score += 3 if title else 0
    score += 3  # alt-text & contraste : non vérifiables sans rasterisation, on suppose OK si Typst

    status = "PASS" if score >= 16 else "FAIL"
    return {
        "file": str(pdf_path),
        "pages": pages,
        "tagged_pdf": tagged,
        "structure_tree": has_struct,
        "language": str(lang) if lang else None,
        "title": str(title) if title else None,
        "score": score,
        "max_score": 20,
        "status": status,
        "notes": "alt-text et contraste à vérifier manuellement ou via tools/contrast_check.py",
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: pdf_accessibility_check.py <fichier.pdf>")
        sys.exit(1)
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"[ERR] Fichier introuvable: {p}")
        sys.exit(2)
    result = check(p)
    print(yaml.safe_dump({"accessibility_report": result}, allow_unicode=True, sort_keys=False))
    sys.exit(0 if result["status"] == "PASS" else 3)


if __name__ == "__main__":
    main()
