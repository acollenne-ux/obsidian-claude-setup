"""
components.py — Composants HTML reutilisables pour le rendu PDF.

Composants disponibles :
  - cover_page         : page de garde complete (logo, titre, classification, version)
  - executive_summary  : encart resume executif
  - confidence_bar     : barre de score de confiance coloree
  - toc                : table des matieres avec numeros de pages
  - kpi_dashboard      : grille de KPI cards (style dashboard financier)
  - callout            : callout GitHub-style (Note/Tip/Warning/etc.)
  - footnotes_section  : section finale des footnotes
  - sources_appendix   : annexe sources/methodologie
  - document_footer    : pied de document
"""
import re
from datetime import datetime
from .markdown_parser import CALLOUT_TYPES, image_to_base64


# =====================================================================
# FORMATAGE INLINE (gras, italique, code, liens)
# =====================================================================
def format_inline(text: str) -> str:
    """Applique le formatage inline markdown vers HTML, avec footnotes."""
    # Echapper les caracteres HTML dangereux d'abord (mais preserver les entites existantes)
    # On ne touche pas aux entities & deja presentes
    # Footnote refs [^id] -> sup
    text = re.sub(r'\[\^([^\]]+)\]', r'<sup class="fn-ref"><a href="#fn-\1">[\1]</a></sup>', text)
    # Gras
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italique
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Code inline
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Liens
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def html_escape(text: str) -> str:
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))


# =====================================================================
# COVER PAGE (page de garde complete, separee)
# =====================================================================
def cover_page(title: str, frontmatter: dict, doc_type: str = 'analysis',
               date_str: str | None = None) -> str:
    """Genere une vraie page de garde : logo, titre, sous-titre, meta, classification."""
    if date_str is None:
        date_str = datetime.now().strftime('%d/%m/%Y')

    subtitle = frontmatter.get('subtitle', '')
    author = frontmatter.get('author', 'Claude Code - Deep Research')
    version = frontmatter.get('version', '1.0')
    classification = frontmatter.get('classification', 'INTERNE')
    logo_path = frontmatter.get('logo', '')

    logo_html = ''
    if logo_path:
        b64 = image_to_base64(logo_path)
        if b64:
            logo_html = f'<img src="{b64}" class="cover-logo" alt="logo" />'

    type_label = {
        'code': 'Document Code',
        'guide': 'Guide Technique',
        'modifications': 'Journal des Modifications',
        'analysis': "Rapport d'Analyse",
        'financial': 'Analyse Financiere',
        'research': 'Rapport de Recherche',
        'executive': 'Synthese Executive',
    }.get(doc_type, "Rapport")

    classification_color = {
        'PUBLIC': '#38a169',
        'INTERNE': '#3182ce',
        'CONFIDENTIEL': '#d69e2e',
        'STRICT': '#e53e3e',
    }.get(classification.upper(), '#3182ce')

    return f'''
<div class="cover-page">
    <div class="cover-top">
        {logo_html}
        <div class="cover-classification" style="border-color:{classification_color};color:{classification_color}">
            {classification.upper()}
        </div>
    </div>
    <div class="cover-center">
        <div class="cover-type">{type_label}</div>
        <h1 class="cover-title">{html_escape(title)}</h1>
        {f'<p class="cover-subtitle">{html_escape(subtitle)}</p>' if subtitle else ''}
        <div class="cover-divider"></div>
        <div class="cover-meta">
            <div><span class="meta-label">Date</span><span class="meta-value">{date_str}</span></div>
            <div><span class="meta-label">Auteur</span><span class="meta-value">{html_escape(author)}</span></div>
            <div><span class="meta-label">Version</span><span class="meta-value">{html_escape(version)}</span></div>
        </div>
    </div>
    <div class="cover-bottom">
        <p class="cover-footer">Document genere automatiquement &middot; Claude Code &middot; Deep Research</p>
    </div>
</div>
<div class="page-break"></div>
'''


# =====================================================================
# EXECUTIVE SUMMARY
# =====================================================================
def executive_summary(summary: str) -> str:
    if not summary:
        return ''
    paras = ''.join(f'<p>{format_inline(p)}</p>' for p in summary.split('\n') if p.strip())
    return f'''
<div class="executive-summary">
    <h3>Resume executif</h3>
    {paras}
</div>
'''


# =====================================================================
# CONFIDENCE BAR
# =====================================================================
def confidence_bar(score: int | None) -> str:
    if score is None:
        return ''
    if score >= 70:
        color, label = '#38a169', 'Elevee'
    elif score >= 40:
        color, label = '#d69e2e', 'Moyenne'
    else:
        color, label = '#e53e3e', 'Faible'
    return f'''
<div class="confidence-box">
    <span class="confidence-title">Niveau de confiance :</span>
    <div class="confidence-bar">
        <div class="fill" style="width:{score}%;background:{color}"></div>
    </div>
    <span class="confidence-label" style="color:{color}">{score}%</span>
    <span class="confidence-tag" style="color:{color}">{label}</span>
</div>
'''


# =====================================================================
# TOC
# =====================================================================
def toc_html(toc: list[dict]) -> str:
    if not toc:
        return ''
    items = ''.join(
        f'<li class="toc-{item["level"]}"><a href="#{item["anchor"]}">{html_escape(item["title"])}</a></li>'
        for item in toc
    )
    return f'<div class="toc"><h3>Table des matieres</h3><ul>{items}</ul></div>'


# =====================================================================
# KPI DASHBOARD
# =====================================================================
def kpi_dashboard(kpis: list) -> str:
    """Genere une grille de KPI cards depuis le frontmatter YAML."""
    if not kpis:
        return ''
    cards = []
    for kpi in kpis:
        if not isinstance(kpi, dict):
            continue
        label = html_escape(str(kpi.get('label', '')))
        value = html_escape(str(kpi.get('value', '')))
        change = str(kpi.get('change', ''))
        sentiment = str(kpi.get('sentiment', 'neutral')).lower()
        sentiment_color = {
            'positive': '#38a169',
            'negative': '#e53e3e',
            'neutral': '#718096',
        }.get(sentiment, '#718096')
        change_html = ''
        if change:
            arrow = '+' if sentiment == 'positive' else ('-' if sentiment == 'negative' else '~')
            change_clean = change.lstrip('+-')
            change_html = f'<div class="kpi-change" style="color:{sentiment_color}">{arrow} {html_escape(change_clean)}</div>'
        cards.append(f'''
<div class="kpi-card" style="border-top:3px solid {sentiment_color}">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div>
    {change_html}
</div>''')
    return f'<div class="kpi-dashboard">{"".join(cards)}</div>'


# =====================================================================
# CALLOUTS GitHub-style
# =====================================================================
def callout(callout_type: str, content: str) -> str:
    """Genere un callout GitHub-style."""
    info = CALLOUT_TYPES.get(callout_type.upper(), CALLOUT_TYPES['NOTE'])
    return f'''
<div class="callout callout-{callout_type.lower()}" style="background:{info['bg']};border-left-color:{info['color']}">
    <div class="callout-header" style="color:{info['color']}">
        <span class="callout-icon">[{info['icon']}]</span>
        <span class="callout-label">{info['label']}</span>
    </div>
    <div class="callout-body">{content}</div>
</div>
'''


# =====================================================================
# FOOTNOTES
# =====================================================================
def footnotes_section(footnotes: dict[str, str]) -> str:
    if not footnotes:
        return ''
    items = ''.join(
        f'<li id="fn-{fid}"><span class="fn-num">[{fid}]</span> {format_inline(text)}</li>'
        for fid, text in footnotes.items()
    )
    return f'''
<div class="footnotes">
    <h2>Notes de bas de page</h2>
    <ol class="footnotes-list">{items}</ol>
</div>
'''


# =====================================================================
# SOURCES APPENDIX
# =====================================================================
def sources_appendix(sources: list[str]) -> str:
    if not sources:
        return ''
    items = ''.join(f'<div class="source-item">{format_inline(s)}</div>' for s in sources)
    return f'''
<div class="annexes">
    <h2>Annexes - Sources et Methodologie</h2>
    <div class="section-box">{items}</div>
</div>
'''


# =====================================================================
# DOCUMENT FOOTER
# =====================================================================
def document_footer(date_str: str) -> str:
    return f'''
<div class="document-footer">
    <p>Document genere automatiquement par Claude Code - Deep Research Multi-Agents</p>
    <p>{date_str} &middot; acollenne@gmail.com</p>
</div>
'''
