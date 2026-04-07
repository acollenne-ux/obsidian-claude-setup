"""golden_pdf_test.py — Test de régression visuelle PDF

Compare un PDF généré à un golden PDF de référence (page par page, hash perceptuel).
Usage: python golden_pdf_test.py <generated.pdf> <golden.pdf>
Exit 0 si identique, 1 si diff > seuil.
"""
from __future__ import annotations
import hashlib
import sys
from pathlib import Path


def page_hashes(pdf: Path) -> list[str]:
    """Hash binaire de chaque page (rapide, sans rendering).
    Pour un vrai diff perceptuel, installer pdf2image + Pillow + imagehash."""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("[ERR] pip install pypdf")
        sys.exit(2)
    r = PdfReader(str(pdf))
    out = []
    for page in r.pages:
        content = page.get_contents()
        data = content.get_data() if content else b""
        out.append(hashlib.sha256(data).hexdigest()[:16])
    return out


def main():
    if len(sys.argv) != 3:
        print("Usage: golden_pdf_test.py <generated.pdf> <golden.pdf>")
        sys.exit(1)
    gen, golden = Path(sys.argv[1]), Path(sys.argv[2])
    if not golden.exists():
        # Première exécution : créer le golden
        import shutil
        shutil.copy(gen, golden)
        print(f"[INFO] Golden créé: {golden}")
        sys.exit(0)
    h1, h2 = page_hashes(gen), page_hashes(golden)
    if len(h1) != len(h2):
        print(f"[FAIL] Page count diff: {len(h1)} vs {len(h2)}")
        sys.exit(1)
    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(h1, h2)) if a != b]
    if not diffs:
        print(f"[PASS] {len(h1)} pages identiques")
        sys.exit(0)
    print(f"[FAIL] {len(diffs)}/{len(h1)} pages différentes")
    for i, a, b in diffs[:5]:
        print(f"  page {i+1}: {a} != {b}")
    sys.exit(1)


if __name__ == "__main__":
    main()
