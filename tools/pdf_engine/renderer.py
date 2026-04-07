"""
renderer.py — Pipeline complet de rendu PDF.

Moteurs supportes (auto-detection) :
  1. Playwright (Chromium)  : moteur principal — CSS moderne, sans dep systeme
  2. WeasyPrint             : fallback Linux/Mac (necessite GTK sur Windows)

Pipeline :
  1. parse_markdown_document  -> structure intermediaire
  2. markdown_to_html         -> HTML enrichi (callouts, mermaid, kpi, footnotes)
  3. assemble_document        -> composition finale (cover + summary + TOC + body + footnotes + sources)
  4. render_html_to_pdf       -> PDF final via le moteur disponible
  5. quality_check (optionnel) -> validation post-generation

Templates supportes :
  - executive   : minimaliste, gros titres, beaucoup de blanc
  - financial   : KPI cards, tableaux denses, palette sobre
  - technical   : code colore, monospace, diagrammes
  - research    : footnotes academiques, palette neutre
  - minimal     : N&B austere
"""
import os
import re
import logging
from pathlib import Path
from datetime import datetime

from .markdown_parser import parse_markdown_document, image_to_base64
from .components import (
    cover_page, executive_summary, confidence_bar, toc_html,
    kpi_dashboard, callout, footnotes_section, sources_appendix,
    document_footer, format_inline, html_escape,
)
from .mermaid import render_mermaid_block

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent / "templates"
AVAILABLE_TEMPLATES = ['executive', 'financial', 'technical', 'research', 'minimal']
DEFAULT_TEMPLATE = 'executive'


def list_templates() -> list[str]:
    """Liste les templates CSS disponibles."""
    return AVAILABLE_TEMPLATES


def load_template_css(template: str) -> str:
    """Charge le CSS d'un template (base.css + theme specifique)."""
    base = TEMPLATES_DIR / "base.css"
    theme = TEMPLATES_DIR / f"{template}.css"
    css = ""
    if base.exists():
        css += base.read_text(encoding='utf-8')
    if theme.exists():
        css += "\n" + theme.read_text(encoding='utf-8')
    return css


# =====================================================================
# MARKDOWN -> HTML (avec extensions enrichies)
# =====================================================================
def markdown_to_html(content: str) -> str:
    """Convertit le markdown en HTML enrichi (callouts, mermaid, code, tables, KPI inline)."""
    lines = content.split('\n')
    html_parts = []
    i = 0
    in_list = False
    in_ol = False

    def close_lists():
        nonlocal in_list, in_ol
        if in_list:
            html_parts.append('</ul>')
            in_list = False
        if in_ol:
            html_parts.append('</ol>')
            in_ol = False

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        # Fermer listes si necessaire
        if in_list and not re.match(r'^[-*]\s', stripped):
            html_parts.append('</ul>')
            in_list = False
        if in_ol and not re.match(r'^\d+\.\s', stripped):
            html_parts.append('</ol>')
            in_ol = False

        # Image : ![alt](path)
        img_match = re.match(r'^!\[([^\]]*)\]\((.+?)\)\s*$', stripped)
        if img_match:
            alt, path = img_match.group(1), img_match.group(2)
            b64 = image_to_base64(path)
            if b64:
                html_parts.append(f'<figure><img src="{b64}" alt="{html_escape(alt)}" />')
                if alt:
                    html_parts.append(f'<figcaption>{html_escape(alt)}</figcaption>')
                html_parts.append('</figure>')
            else:
                html_parts.append(f'<p class="image-missing">[Image manquante : {html_escape(alt or os.path.basename(path))}]</p>')
            i += 1
            continue

        # Bloc Mermaid
        if stripped == '```mermaid' or stripped.startswith('```mermaid'):
            i += 1
            mermaid_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                mermaid_lines.append(lines[i])
                i += 1
            i += 1
            html_parts.append(render_mermaid_block('\n'.join(mermaid_lines)))
            continue

        # Bloc code (avec langue eventuelle)
        if stripped.startswith('```'):
            lang = stripped[3:].strip() or 'text'
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1
            code_html = html_escape('\n'.join(code_lines))
            highlighted = _highlight_code(code_html, lang)
            html_parts.append(f'<pre class="lang-{lang}"><code>{highlighted}</code></pre>')
            continue

        # Callout GitHub-style : > [!NOTE] / [!TIP] / [!IMPORTANT] / [!WARNING] / [!CAUTION]
        callout_match = re.match(r'^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$', stripped)
        if callout_match:
            ctype = callout_match.group(1)
            first_line = callout_match.group(2).strip()
            i += 1
            body_lines = []
            if first_line:
                body_lines.append(first_line)
            while i < len(lines) and lines[i].strip().startswith('>'):
                body_lines.append(lines[i].strip().lstrip('>').strip())
                i += 1
            body_html = '<p>' + '<br/>'.join(format_inline(b) for b in body_lines if b) + '</p>'
            html_parts.append(callout(ctype, body_html))
            continue

        # Tableau Markdown
        if '|' in stripped and stripped.startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i].strip() and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            html_parts.append(_render_table(table_lines))
            continue

        # Titres
        h_match = re.match(r'^(#{1,6})\s+(.+)', stripped)
        if h_match:
            level = len(h_match.group(1))
            title_text = h_match.group(2).strip()
            clean_title = re.sub(r'[*`]', '', title_text)
            anchor = re.sub(r'[^a-z0-9]+', '-', clean_title.lower()).strip('-')
            html_parts.append(f'<h{level} id="{anchor}">{format_inline(title_text)}</h{level}>')
            i += 1
            continue

        # Separateur
        if re.match(r'^-{3,}$', stripped) or re.match(r'^\*{3,}$', stripped):
            html_parts.append('<hr />')
            i += 1
            continue

        # Blockquote standard
        if stripped.startswith('>') and not callout_match:
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip().lstrip('>').strip())
                i += 1
            html_parts.append(f'<blockquote>{format_inline(" ".join(quote_lines))}</blockquote>')
            continue

        # Liste a puces
        if re.match(r'^[-*]\s', stripped):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            item = re.sub(r'^[-*]\s+', '', stripped)
            html_parts.append(f'<li>{format_inline(item)}</li>')
            i += 1
            continue

        # Liste numerotee
        if re.match(r'^\d+\.\s', stripped):
            if not in_ol:
                html_parts.append('<ol>')
                in_ol = True
            item = re.sub(r'^\d+\.\s+', '', stripped)
            html_parts.append(f'<li>{format_inline(item)}</li>')
            i += 1
            continue

        # Ligne vide
        if not stripped:
            html_parts.append('')
            i += 1
            continue

        # Paragraphe
        html_parts.append(f'<p>{format_inline(stripped)}</p>')
        i += 1

    close_lists()
    return '\n'.join(html_parts)


# =====================================================================
# SYNTAX HIGHLIGHTING (Pygments si disponible)
# =====================================================================
_PYGMENTS_AVAILABLE = False
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, TextLexer
    from pygments.formatters import HtmlFormatter
    from pygments.util import ClassNotFound
    _PYGMENTS_AVAILABLE = True
    _PYGMENTS_FORMATTER = HtmlFormatter(nowrap=True, style='monokai')
    _PYGMENTS_CSS = HtmlFormatter(style='monokai').get_style_defs('.highlight')
except ImportError:
    _PYGMENTS_CSS = ""


def _highlight_code(code_html: str, lang: str) -> str:
    """Applique syntax highlighting si Pygments dispo, sinon retourne tel quel."""
    if not _PYGMENTS_AVAILABLE or not lang or lang == 'text':
        return code_html
    try:
        # On doit re-decoder les entites HTML pour Pygments
        import html as html_mod
        raw = html_mod.unescape(code_html)
        try:
            lexer = get_lexer_by_name(lang)
        except ClassNotFound:
            lexer = TextLexer()
        return highlight(raw, lexer, _PYGMENTS_FORMATTER)
    except (ImportError, ValueError, RuntimeError):
        return code_html


def _render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        if re.match(r'^\s*\|[-:\s|]+\|\s*$', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if any(c.strip() for c in cells):
            rows.append(cells)
    if not rows:
        return ''
    html = '<table>\n<thead><tr>'
    for cell in rows[0]:
        html += f'<th>{format_inline(cell)}</th>'
    html += '</tr></thead>\n<tbody>'
    for row in rows[1:]:
        html += '<tr>'
        for cell in row:
            html += f'<td>{format_inline(cell)}</td>'
        html += '</tr>\n'
    html += '</tbody></table>'
    return html


# =====================================================================
# ASSEMBLAGE COMPLET
# =====================================================================
def assemble_document(title: str, parsed: dict, template: str,
                      doc_type: str, with_cover: bool = True) -> str:
    """Assemble le document HTML complet pret pour WeasyPrint."""
    now = datetime.now()
    date_str = now.strftime('%d/%m/%Y a %H:%M')

    css = load_template_css(template)
    # Injecter la date dans @top-right
    css = css.replace('REPORT_DATE_PLACEHOLDER', date_str)
    # Injecter le CSS Pygments si dispo
    if _PYGMENTS_CSS:
        css += "\n" + _PYGMENTS_CSS

    # Composants
    cover_html = cover_page(title, parsed['frontmatter'], doc_type, date_str) if with_cover else ''
    summary_html = executive_summary(parsed['summary'])
    confidence_html = confidence_bar(parsed['score'])
    kpi_html = kpi_dashboard(parsed['kpis'])
    toc_section = toc_html(parsed['toc'])
    body_html = markdown_to_html(parsed['body'])
    footnotes_html = footnotes_section(parsed['footnotes'])
    sources_html = sources_appendix(parsed['sources'])
    footer_html = document_footer(date_str)

    type_label = {
        'code': 'Document Code',
        'guide': 'Guide',
        'modifications': 'Modifications',
        'analysis': "Rapport d'analyse",
        'financial': 'Analyse Financiere',
        'research': 'Recherche',
        'executive': 'Synthese Executive',
    }.get(doc_type, "Rapport")

    # Banner uniquement si pas de cover
    banner_html = ''
    if not with_cover:
        banner_html = f'''
<div class="cover-banner">
    <h1>{html_escape(title)}</h1>
    <p class="subtitle">{type_label} &middot; {date_str} &middot; Claude Code - Deep Research</p>
</div>
'''

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>{html_escape(title)}</title>
    <style>{css}</style>
</head>
<body>
{cover_html}
{banner_html}
{summary_html}
{confidence_html}
{kpi_html}
{toc_section}
<div class="main-content">
{body_html}
</div>
{footnotes_html}
{sources_html}
{footer_html}
</body>
</html>'''


# =====================================================================
# POINT D'ENTREE PRINCIPAL
# =====================================================================
# =====================================================================
# DETECTION MOTEUR PDF
# =====================================================================
def detect_engine() -> str:
    """Detecte le meilleur moteur PDF disponible.

    Ordre : playwright (Chromium) > weasyprint > erreur.
    """
    try:
        import playwright  # noqa: F401
        return 'playwright'
    except ImportError:
        pass
    try:
        # WeasyPrint peut s'importer mais echouer au runtime si GTK manquant
        from weasyprint import HTML as _H  # noqa: F401
        # Test reel : essayer de creer un objet
        _H(string='<html><body>x</body></html>')
        return 'weasyprint'
    except (ImportError, OSError):
        pass
    return 'none'


def render_html_to_pdf_playwright(html_doc: str, output: str, base_url: str | None = None) -> None:
    """Rend HTML -> PDF via Playwright (Chromium)."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # set_content avec base_url pour resoudre les ressources locales si besoin
        if base_url:
            page.goto(f"data:text/html;base64,")  # init
        page.set_content(html_doc, wait_until='networkidle')
        page.pdf(
            path=output,
            format='A4',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
            prefer_css_page_size=True,
        )
        browser.close()


def render_html_to_pdf_weasyprint(html_doc: str, output: str,
                                  base_url: str | None = None,
                                  pdf_ua: bool = False) -> None:
    """Rend HTML -> PDF via WeasyPrint."""
    from weasyprint import HTML as WeasyHTML
    kwargs = {}
    if pdf_ua:
        kwargs['pdf_variant'] = 'pdf/ua-1'
    try:
        WeasyHTML(string=html_doc, base_url=base_url).write_pdf(output, **kwargs)
    except TypeError:
        WeasyHTML(string=html_doc, base_url=base_url).write_pdf(output)


def render_pdf(title: str, content: str, output: str,
               template: str = DEFAULT_TEMPLATE,
               doc_type: str = 'analysis',
               with_cover: bool = True,
               check_quality: bool = False,
               pdf_ua: bool = False,
               engine: str | None = None) -> dict:
    """Genere un PDF professionnel a partir d'un Markdown.

    Args:
        title: titre du document
        content: contenu Markdown (avec frontmatter YAML optionnel)
        output: chemin du PDF de sortie
        template: nom du template (executive/financial/technical/research/minimal)
        doc_type: type de document (analysis/code/guide/financial/research/executive)
        with_cover: ajouter une page de garde complete
        check_quality: lancer un quality check apres generation
        pdf_ua: tagger PDF/UA-1 (accessibilite ISO, WeasyPrint uniquement)
        engine: forcer un moteur ('playwright' ou 'weasyprint'). None = auto-detect.

    Returns:
        dict avec : path, pages, size, template, engine, errors
    """
    if template not in AVAILABLE_TEMPLATES:
        logger.warning(f"Template '{template}' inconnu, fallback vers '{DEFAULT_TEMPLATE}'")
        template = DEFAULT_TEMPLATE

    parsed = parse_markdown_document(content)

    # Override depuis frontmatter
    fm = parsed['frontmatter']
    if 'template' in fm and fm['template'] in AVAILABLE_TEMPLATES:
        template = fm['template']
    if 'doc_type' in fm:
        doc_type = fm['doc_type']

    html_doc = assemble_document(title, parsed, template, doc_type, with_cover=with_cover)

    # Detection du moteur
    if engine is None:
        engine = detect_engine()
    if engine == 'none':
        raise RuntimeError(
            "Aucun moteur PDF disponible. Installez : pip install playwright && playwright install chromium"
        )

    base_url = str(Path(output).parent.absolute())

    if engine == 'playwright':
        render_html_to_pdf_playwright(html_doc, output, base_url=base_url)
    elif engine == 'weasyprint':
        render_html_to_pdf_weasyprint(html_doc, output, base_url=base_url, pdf_ua=pdf_ua)
    else:
        raise RuntimeError(f"Moteur PDF inconnu : {engine}")

    result = {
        'path': output,
        'template': template,
        'doc_type': doc_type,
        'engine': engine,
        'size_kb': round(os.path.getsize(output) / 1024, 1) if os.path.exists(output) else 0,
        'errors': [],
    }

    if check_quality:
        from .quality_check import check_pdf_quality
        qc = check_pdf_quality(output)
        result.update(qc)

    return result
