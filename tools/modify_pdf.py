"""
modify_pdf.py — Outil de modification de PDF existants.

Operations supportees :
  - merge      : fusionner plusieurs PDFs
  - split      : decouper un PDF en pages individuelles
  - extract    : extraire un range de pages
  - watermark  : ajouter un watermark texte
  - rotate     : rotation des pages
  - metadata   : modifier les metadonnees (titre, auteur, sujet)
  - info       : afficher infos d'un PDF

Dependances : pypdf (preferentiel) ou PyPDF2.
Watermark texte : reportlab pour generer le watermark.

Usage :
  python modify_pdf.py merge a.pdf b.pdf c.pdf -o out.pdf
  python modify_pdf.py split big.pdf -o pages_dir/
  python modify_pdf.py extract big.pdf 1-5 -o intro.pdf
  python modify_pdf.py watermark doc.pdf "CONFIDENTIEL" -o watermarked.pdf
  python modify_pdf.py rotate doc.pdf 90 -o rotated.pdf
  python modify_pdf.py metadata doc.pdf --title "Nouveau" --author "Alex" -o updated.pdf
  python modify_pdf.py info doc.pdf
"""
import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _import_pypdf():
    """Import flexible : pypdf > PyPDF2."""
    try:
        from pypdf import PdfReader, PdfWriter
        return PdfReader, PdfWriter, 'pypdf'
    except ImportError:
        try:
            from PyPDF2 import PdfReader, PdfWriter
            return PdfReader, PdfWriter, 'PyPDF2'
        except ImportError as e:
            raise SystemExit("Erreur : pypdf ou PyPDF2 requis. pip install pypdf") from e


# =====================================================================
# OPERATIONS
# =====================================================================
def merge_pdfs(inputs: list[str], output: str) -> dict:
    """Fusionne plusieurs PDFs en un seul."""
    PdfReader, PdfWriter, _ = _import_pypdf()
    writer = PdfWriter()
    total_pages = 0
    for pdf in inputs:
        if not os.path.exists(pdf):
            logger.warning(f"Fichier ignore (introuvable) : {pdf}")
            continue
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
            total_pages += 1
    with open(output, 'wb') as f:
        writer.write(f)
    return {'output': output, 'pages': total_pages, 'inputs': len(inputs)}


def split_pdf(input_pdf: str, output_dir: str) -> dict:
    """Decoupe un PDF en pages individuelles."""
    PdfReader, PdfWriter, _ = _import_pypdf()
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    reader = PdfReader(input_pdf)
    base = Path(input_pdf).stem
    files = []
    for i, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)
        out = os.path.join(output_dir, f"{base}_page_{i:03d}.pdf")
        with open(out, 'wb') as f:
            writer.write(f)
        files.append(out)
    return {'output_dir': output_dir, 'pages': len(files), 'files': files}


def extract_pages(input_pdf: str, page_range: str, output: str) -> dict:
    """Extrait un range de pages : '1-5', '3', '1,3,5'."""
    PdfReader, PdfWriter, _ = _import_pypdf()
    reader = PdfReader(input_pdf)
    total = len(reader.pages)
    pages_to_extract = _parse_range(page_range, total)
    writer = PdfWriter()
    for p in pages_to_extract:
        if 1 <= p <= total:
            writer.add_page(reader.pages[p - 1])
    with open(output, 'wb') as f:
        writer.write(f)
    return {'output': output, 'pages_extracted': len(pages_to_extract)}


def _parse_range(spec: str, total: int) -> list[int]:
    """Parse '1-5', '3', '1,3,5-7' en liste de numeros de pages (1-indexes)."""
    pages = []
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return pages


def add_watermark(input_pdf: str, text: str, output: str,
                  opacity: float = 0.15, font_size: int = 60) -> dict:
    """Ajoute un watermark texte diagonal sur chaque page."""
    PdfReader, PdfWriter, _ = _import_pypdf()
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.colors import Color
    except ImportError as e:
        raise SystemExit("reportlab requis pour watermark : pip install reportlab") from e

    import tempfile
    # Generer le watermark PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        wm_path = tmp.name
    c = canvas.Canvas(wm_path, pagesize=A4)
    width, height = A4
    c.setFillColor(Color(0.5, 0.5, 0.5, alpha=opacity))
    c.setFont("Helvetica-Bold", font_size)
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.save()

    wm_reader = PdfReader(wm_path)
    wm_page = wm_reader.pages[0]

    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(wm_page)
        writer.add_page(page)
    with open(output, 'wb') as f:
        writer.write(f)

    try:
        os.unlink(wm_path)
    except OSError:
        pass

    return {'output': output, 'watermark': text, 'pages': len(reader.pages)}


def rotate_pdf(input_pdf: str, angle: int, output: str) -> dict:
    """Rotation de toutes les pages (90, 180, 270)."""
    if angle not in (90, 180, 270, -90, -180, -270):
        raise ValueError("Angle doit etre 90, 180 ou 270")
    PdfReader, PdfWriter, _ = _import_pypdf()
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(angle)
        writer.add_page(page)
    with open(output, 'wb') as f:
        writer.write(f)
    return {'output': output, 'angle': angle, 'pages': len(reader.pages)}


def update_metadata(input_pdf: str, output: str, **meta) -> dict:
    """Met a jour les metadonnees : title, author, subject, keywords."""
    PdfReader, PdfWriter, _ = _import_pypdf()
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    # Construire le dict des metadonnees
    md = {}
    if meta.get('title'):
        md['/Title'] = meta['title']
    if meta.get('author'):
        md['/Author'] = meta['author']
    if meta.get('subject'):
        md['/Subject'] = meta['subject']
    if meta.get('keywords'):
        md['/Keywords'] = meta['keywords']
    md['/ModDate'] = f"D:{datetime.now().strftime('%Y%m%d%H%M%S')}"
    writer.add_metadata(md)
    with open(output, 'wb') as f:
        writer.write(f)
    return {'output': output, 'metadata_set': list(md.keys())}


def pdf_info(input_pdf: str) -> dict:
    """Affiche les infos d'un PDF."""
    PdfReader, _, _ = _import_pypdf()
    reader = PdfReader(input_pdf)
    info = {
        'path': input_pdf,
        'pages': len(reader.pages),
        'size_kb': round(os.path.getsize(input_pdf) / 1024, 1),
    }
    try:
        meta = reader.metadata
        if meta:
            info['title'] = meta.title or ''
            info['author'] = meta.author or ''
            info['subject'] = meta.subject or ''
            info['producer'] = meta.producer or ''
            info['creator'] = meta.creator or ''
    except (AttributeError, ValueError):
        pass
    try:
        info['encrypted'] = reader.is_encrypted
    except AttributeError:
        info['encrypted'] = False
    return info


# =====================================================================
# CLI
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="Outil de modification de PDF")
    sub = parser.add_subparsers(dest='cmd', required=True)

    # merge
    p_merge = sub.add_parser('merge', help='Fusionner plusieurs PDFs')
    p_merge.add_argument('inputs', nargs='+', help='PDFs en entree')
    p_merge.add_argument('-o', '--output', required=True, help='PDF de sortie')

    # split
    p_split = sub.add_parser('split', help='Decouper un PDF en pages')
    p_split.add_argument('input', help='PDF a decouper')
    p_split.add_argument('-o', '--output', required=True, help='Repertoire de sortie')

    # extract
    p_ext = sub.add_parser('extract', help='Extraire des pages')
    p_ext.add_argument('input', help='PDF source')
    p_ext.add_argument('range', help='Range : 1-5, 3, ou 1,3,5')
    p_ext.add_argument('-o', '--output', required=True, help='PDF de sortie')

    # watermark
    p_wm = sub.add_parser('watermark', help='Ajouter un watermark')
    p_wm.add_argument('input', help='PDF source')
    p_wm.add_argument('text', help='Texte du watermark')
    p_wm.add_argument('-o', '--output', required=True, help='PDF de sortie')
    p_wm.add_argument('--opacity', type=float, default=0.15)
    p_wm.add_argument('--font-size', type=int, default=60)

    # rotate
    p_rot = sub.add_parser('rotate', help='Rotation des pages')
    p_rot.add_argument('input', help='PDF source')
    p_rot.add_argument('angle', type=int, help='Angle (90/180/270)')
    p_rot.add_argument('-o', '--output', required=True, help='PDF de sortie')

    # metadata
    p_meta = sub.add_parser('metadata', help='Modifier les metadonnees')
    p_meta.add_argument('input', help='PDF source')
    p_meta.add_argument('-o', '--output', required=True, help='PDF de sortie')
    p_meta.add_argument('--title')
    p_meta.add_argument('--author')
    p_meta.add_argument('--subject')
    p_meta.add_argument('--keywords')

    # info
    p_info = sub.add_parser('info', help='Afficher les infos d\'un PDF')
    p_info.add_argument('input', help='PDF a inspecter')

    args = parser.parse_args()

    try:
        if args.cmd == 'merge':
            r = merge_pdfs(args.inputs, args.output)
            logger.info(f"[OK] Merge : {r['inputs']} fichiers -> {r['output']} ({r['pages']} pages)")
        elif args.cmd == 'split':
            r = split_pdf(args.input, args.output)
            logger.info(f"[OK] Split : {r['pages']} fichiers dans {r['output_dir']}")
        elif args.cmd == 'extract':
            r = extract_pages(args.input, args.range, args.output)
            logger.info(f"[OK] Extract : {r['pages_extracted']} pages -> {r['output']}")
        elif args.cmd == 'watermark':
            r = add_watermark(args.input, args.text, args.output, args.opacity, args.font_size)
            logger.info(f"[OK] Watermark '{args.text}' ajoute sur {r['pages']} pages -> {r['output']}")
        elif args.cmd == 'rotate':
            r = rotate_pdf(args.input, args.angle, args.output)
            logger.info(f"[OK] Rotation {args.angle} appliquee sur {r['pages']} pages -> {r['output']}")
        elif args.cmd == 'metadata':
            r = update_metadata(
                args.input, args.output,
                title=args.title, author=args.author,
                subject=args.subject, keywords=args.keywords,
            )
            logger.info(f"[OK] Metadata mises a jour : {r['metadata_set']} -> {r['output']}")
        elif args.cmd == 'info':
            info = pdf_info(args.input)
            for k, v in info.items():
                print(f"  {k:12s} : {v}")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        logger.error(f"[ERREUR] {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
