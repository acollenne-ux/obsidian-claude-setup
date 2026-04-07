"""
quality_check.py — Verifications post-generation du PDF.

Verifie :
  - Le fichier existe et n'est pas vide
  - Nombre de pages
  - Taille du fichier
  - Texte extractible (pas image-only)
  - Bookmarks/TOC presents
  - Score de lisibilite basique (Flesch approximatif)

Utilise pypdf si disponible (preinstalle souvent comme dep de weasyprint).
"""
import os
import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def check_pdf_quality(pdf_path: str) -> dict:
    """Lance les verifications qualite et retourne un dict de resultats."""
    result: dict = {
        'qc_ok': False,
        'qc_pages': 0,
        'qc_size_kb': 0,
        'qc_has_text': False,
        'qc_has_bookmarks': False,
        'qc_text_length': 0,
        'qc_warnings': [],
        'qc_errors': [],
    }

    if not os.path.exists(pdf_path):
        result['qc_errors'].append('Fichier PDF inexistant')
        return result

    size = os.path.getsize(pdf_path)
    result['qc_size_kb'] = round(size / 1024, 1)

    if size < 1024:
        result['qc_errors'].append(f'PDF trop petit ({size} bytes)')
        return result

    # Tenter pypdf
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            result['qc_warnings'].append('pypdf non installe : verifications limitees')
            result['qc_ok'] = size > 1024
            return result

    try:
        reader = PdfReader(pdf_path)
        result['qc_pages'] = len(reader.pages)

        # Extraire le texte
        all_text = ""
        for page in reader.pages:
            try:
                all_text += page.extract_text() or ""
            except (AttributeError, TypeError, ValueError):
                continue
        result['qc_text_length'] = len(all_text)
        result['qc_has_text'] = len(all_text) > 100

        # Bookmarks (outline)
        try:
            outline = reader.outline
            result['qc_has_bookmarks'] = bool(outline)
        except (AttributeError, TypeError):
            result['qc_has_bookmarks'] = False

        # Verifications metier
        if result['qc_pages'] == 0:
            result['qc_errors'].append('Aucune page')
        if result['qc_pages'] > 200:
            result['qc_warnings'].append(f'Document tres long ({result["qc_pages"]} pages)')
        if not result['qc_has_text']:
            result['qc_errors'].append('Pas de texte extractible (image-only?)')
        if size > 10 * 1024 * 1024:
            result['qc_warnings'].append(f'PDF volumineux ({result["qc_size_kb"]} KB)')

        # Score de lisibilite simple
        if all_text:
            words = re.findall(r'\b\w+\b', all_text)
            sentences = re.findall(r'[.!?]+', all_text)
            if sentences and words:
                avg_words_per_sentence = len(words) / max(len(sentences), 1)
                result['qc_avg_words_per_sentence'] = round(avg_words_per_sentence, 1)
                if avg_words_per_sentence > 35:
                    result['qc_warnings'].append('Phrases tres longues (>35 mots/phrase)')

        result['qc_ok'] = (
            len(result['qc_errors']) == 0
            and result['qc_pages'] > 0
            and result['qc_has_text']
        )

    except (OSError, ValueError, RuntimeError) as e:
        result['qc_errors'].append(f'Erreur lecture PDF : {type(e).__name__}: {e}')

    return result


def format_quality_report(qc: dict) -> str:
    """Formate le rapport QC pour affichage console."""
    status = "OK" if qc.get('qc_ok') else "ECHEC"
    lines = [
        f"  Quality Check : {status}",
        f"    Pages          : {qc.get('qc_pages', 0)}",
        f"    Taille         : {qc.get('qc_size_kb', 0)} KB",
        f"    Texte extract. : {'oui' if qc.get('qc_has_text') else 'non'} ({qc.get('qc_text_length', 0)} chars)",
        f"    Bookmarks      : {'oui' if qc.get('qc_has_bookmarks') else 'non'}",
    ]
    if qc.get('qc_warnings'):
        lines.append("  Warnings :")
        for w in qc['qc_warnings']:
            lines.append(f"    [!] {w}")
    if qc.get('qc_errors'):
        lines.append("  Erreurs :")
        for e in qc['qc_errors']:
            lines.append(f"    [X] {e}")
    return '\n'.join(lines)
