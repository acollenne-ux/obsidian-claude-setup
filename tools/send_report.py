"""
send_report.py - Generateur PDF professionnel + envoi email.
Version 2.0 - Migration WeasyPrint avec fallback fpdf2.

Usage :
  python send_report.py "Sujet" "contenu markdown" [email]
  python send_report.py "Sujet" --file chemin.md [email]

Fonctionnalites :
- Moteur WeasyPrint (HTML/CSS) avec fallback fpdf2
- Templates CSS professionnels (couleurs corporate)
- Table des matieres automatique
- En-tetes/pieds de page avec numerotation
- Score de confiance visuel (barres colorees)
- Resume executif en premiere page
- Sections avec bordures et ombres
- Tableaux styles, blocs de code, listes
- Annexes pour sources et methodologie
- Images inline : ![alt](chemin_image.png)
"""
import sys, os, json, smtplib, re, base64, hashlib, logging, glob as glob_mod
from datetime import datetime
from math import ceil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# --- Logging structure ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _find_dejavu_font():
    """Recherche la police DejaVuSans.ttf sur le systeme."""
    search_paths = [
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        # Windows
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts\DejaVuSans.ttf"),
        r"C:\Windows\Fonts\DejaVuSans.ttf",
        # Relatif au script
        str(Path(__file__).parent / "DejaVuSans.ttf"),
        str(Path(__file__).parent / "fonts" / "DejaVuSans.ttf"),
    ]
    for p in search_paths:
        if os.path.isfile(p):
            return p
    # Recherche globale Linux
    found = glob_mod.glob("/usr/share/fonts/**/DejaVuSans.ttf", recursive=True)
    if found:
        return found[0]
    return None

DEJAVU_FONT_PATH = _find_dejavu_font()

# --- Detection moteur PDF ---
USE_WEASYPRINT = False
try:
    from weasyprint import HTML as WeasyHTML
    import markdown as md_lib
    USE_WEASYPRINT = True
    logger.info("[PDF Engine] WeasyPrint detecte - mode HTML/CSS actif")
except ImportError:
    try:
        from fpdf import FPDF
        from fpdf.enums import XPos, YPos
        logger.info("[PDF Engine] Fallback fpdf2 actif")
    except ImportError:
        logger.error("[ERREUR] Aucun moteur PDF disponible. Installez weasyprint ou fpdf2.")
        sys.exit(1)

CONFIG_PATH = Path(__file__).parent / "email_config.json"
REPORTS_DIR = Path(__file__).parent / "reports"
DEFAULT_TO = "acollenne@gmail.com"

# =====================================================================
# COULEURS & CONSTANTES CORPORATE
# =====================================================================
COLORS = {
    'primary': '#1a365d',       # Bleu fonce corporate
    'secondary': '#2b6cb0',     # Bleu accent
    'accent': '#3182ce',        # Bleu clair
    'success': '#38a169',        # Vert
    'warning': '#d69e2e',        # Orange
    'danger': '#e53e3e',         # Rouge
    'text': '#2d3748',           # Texte principal
    'text_light': '#718096',     # Texte secondaire
    'bg_light': '#f7fafc',       # Fond clair
    'bg_code': '#1a202c',        # Fond code sombre
    'border': '#e2e8f0',         # Bordures
    'table_header': '#1a365d',   # En-tete tableau
    'table_alt': '#ebf4ff',      # Ligne alternee tableau
}

DOC_TYPES = {
    'code': {'label': 'Document Code', 'color': '#2d3748', 'icon': '&#128187;'},
    'guide': {'label': 'Guide', 'color': '#276749', 'icon': '&#128214;'},
    'modifications': {'label': 'Journal des modifications', 'color': '#744210', 'icon': '&#128221;'},
    'analysis': {'label': "Rapport d'analyse", 'color': '#1a365d', 'icon': '&#128202;'},
}


# =====================================================================
# UTILITAIRES
# =====================================================================
def sanitize(text):
    """Remplace uniquement les caracteres Unicode speciaux (emojis, symboles).
    Preserve les accents francais et autres caracteres latins."""
    # Ne remplacer que les symboles/emojis vraiment problematiques
    table = {
        '\u2019': "'", '\u2018': "'", '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '--', '\u2026': '...',
        '\u2022': '-', '\u2023': '-', '\u25e6': '-',
        '\u2705': '[OK]', '\u274c': '[X]', '\u26a0': '[!]',
        '\u2713': '[v]', '\u2714': '[v]', '\u2717': '[x]',
    }
    for k, v in table.items():
        text = text.replace(k, v)
    # Si on utilise une police Unicode (DejaVu), retourner tel quel
    if DEJAVU_FONT_PATH:
        return text
    # Sinon fallback : encoder en latin-1 (conserve les accents francais)
    try:
        return text.encode('latin-1', errors='replace').decode('latin-1')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')


def strip_inline(text):
    """Supprime le formatage markdown inline."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'[\1]', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    return text


def detect_type(title):
    """Detecte le type de document a partir du titre."""
    t = title.upper()
    if ' - CODE' in t or t.endswith('CODE'): return 'code'
    if 'GUIDE' in t or 'MISE EN ROUTE' in t: return 'guide'
    if 'MODIF' in t or 'AJOUT' in t: return 'modifications'
    return 'analysis'


def extract_toc(content):
    """Extrait la table des matieres depuis les titres markdown."""
    toc = []
    for line in content.split('\n'):
        m = re.match(r'^(#{1,6})\s+(.+)', line.strip())
        if m:
            level = len(m.group(1))
            title = re.sub(r'[*`\[\]()]', '', m.group(2)).strip()
            anchor = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            toc.append({'level': level, 'title': title, 'anchor': anchor})
    return toc


def extract_executive_summary(content):
    """Extrait ou genere un resume executif depuis le contenu."""
    lines = content.split('\n')
    summary_lines = []
    in_summary = False
    for line in lines:
        stripped = line.strip().lower()
        if re.match(r'^#{1,2}\s*(resume|summary|executive|synthese|conclusion)', stripped):
            in_summary = True
            continue
        if in_summary:
            if re.match(r'^#{1,2}\s', line.strip()) and not re.match(r'^#{3,}', line.strip()):
                break
            if line.strip():
                summary_lines.append(line.strip())
    if summary_lines:
        return '\n'.join(summary_lines[:10])
    # Fallback : premiers paragraphes non-titre
    paras = []
    for line in lines:
        if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('|'):
            clean = re.sub(r'[*`]', '', line.strip())
            if len(clean) > 20:
                paras.append(clean)
            if len(paras) >= 3:
                break
    return '\n'.join(paras) if paras else ''


def extract_confidence_score(content):
    """Detecte un score de confiance dans le contenu."""
    patterns = [
        r'(?:score|confiance|confidence|fiabilit).*?(\d{1,3})\s*[%/]',
        r'(\d{1,3})\s*[%/]\s*(?:de\s+)?(?:confiance|fiabilit|confidence)',
        r'(?:note|rating).*?(\d{1,2})/10',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            val = int(m.group(1))
            if '/10' in pat:
                val = val * 10
            return min(max(val, 0), 100)
    return None


def score_color(score):
    """Retourne la couleur CSS selon le score."""
    if score >= 70: return COLORS['success']
    if score >= 40: return COLORS['warning']
    return COLORS['danger']


def image_to_base64(img_path):
    """Convertit une image en data URI base64 pour HTML."""
    try:
        if os.path.exists(img_path):
            ext = Path(img_path).suffix.lower().lstrip('.')
            mime = {'png':'png','jpg':'jpeg','jpeg':'jpeg','gif':'gif','svg':'svg+xml'}.get(ext,'png')
            with open(img_path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
            return f'data:image/{mime};base64,{b64}'
    except Exception:
        pass
    return None


# =====================================================================
# TEMPLATE CSS PROFESSIONNEL
# =====================================================================
CSS_TEMPLATE = """
@page {
    size: A4;
    margin: 20mm 18mm 25mm 18mm;
    @top-left {
        content: string(doc-title);
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 8pt;
        color: #718096;
    }
    @top-right {
        content: "REPORT_DATE_PLACEHOLDER";
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 8pt;
        color: #718096;
    }
    @bottom-center {
        content: "Page " counter(page) " / " counter(pages);
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 8pt;
        color: #a0aec0;
    }
    @bottom-right {
        content: "Claude Code | Deep Research";
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 7pt;
        color: #cbd5e0;
    }
}
@page :first {
    margin-top: 15mm;
    @top-left { content: none; }
    @top-right { content: none; }
}

* { box-sizing: border-box; }

body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #2d3748;
    -webkit-font-smoothing: antialiased;
}

/* --- COVER / TITRE --- */
.cover-banner {
    background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
    color: white;
    padding: 28px 32px;
    border-radius: 8px;
    margin-bottom: 8px;
    box-shadow: 0 4px 15px rgba(26, 54, 93, 0.3);
}
.cover-banner h1 {
    font-size: 20pt;
    margin: 0 0 6px 0;
    font-weight: 700;
    letter-spacing: -0.3px;
}
.cover-banner .subtitle {
    font-size: 9pt;
    opacity: 0.85;
    margin: 0;
}

/* --- EXECUTIVE SUMMARY --- */
.executive-summary {
    background: #ebf8ff;
    border-left: 4px solid #2b6cb0;
    padding: 16px 20px;
    margin: 16px 0;
    border-radius: 0 6px 6px 0;
    font-size: 9.5pt;
    color: #2a4365;
    line-height: 1.7;
}
.executive-summary h3 {
    margin: 0 0 8px 0;
    color: #1a365d;
    font-size: 11pt;
}

/* --- CONFIDENCE SCORE --- */
.confidence-box {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 12px 0 20px 0;
    padding: 10px 16px;
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
}
.confidence-bar {
    flex: 1;
    height: 10px;
    background: #e2e8f0;
    border-radius: 5px;
    overflow: hidden;
}
.confidence-bar .fill {
    height: 100%;
    border-radius: 5px;
    transition: width 0.3s;
}
.confidence-label {
    font-weight: 700;
    font-size: 14pt;
    min-width: 50px;
    text-align: right;
}

/* --- TABLE DES MATIERES --- */
.toc {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 16px 24px;
    margin: 16px 0 24px 0;
}
.toc h3 {
    color: #1a365d;
    margin: 0 0 10px 0;
    font-size: 11pt;
    border-bottom: 2px solid #2b6cb0;
    padding-bottom: 6px;
}
.toc ul {
    list-style: none;
    padding: 0;
    margin: 0;
}
.toc li {
    padding: 3px 0;
    border-bottom: 1px dotted #e2e8f0;
    font-size: 9pt;
}
.toc li:last-child { border-bottom: none; }
.toc li.toc-1 { font-weight: 700; color: #1a365d; padding-left: 0; }
.toc li.toc-2 { padding-left: 16px; color: #2d3748; }
.toc li.toc-3 { padding-left: 32px; color: #718096; font-size: 8.5pt; }
.toc li.toc-4 { padding-left: 48px; color: #a0aec0; font-size: 8pt; }
.toc li.toc-5 { padding-left: 60px; color: #a0aec0; font-size: 7.5pt; }
.toc li.toc-6 { padding-left: 72px; color: #cbd5e0; font-size: 7.5pt; }
.toc a { color: inherit; text-decoration: none; }
.toc a::after {
    content: target-counter(attr(href), page);
    float: right;
    color: #a0aec0;
}

/* --- TITRES --- */
h1 {
    font-size: 16pt;
    color: #1a365d;
    border-bottom: 3px solid #2b6cb0;
    padding-bottom: 6px;
    margin-top: 28px;
    margin-bottom: 12px;
    page-break-after: avoid;
    string-set: doc-title content();
}
h2 {
    font-size: 13pt;
    color: #2b6cb0;
    border-bottom: 2px solid #bee3f8;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
}
h3 {
    font-size: 11pt;
    color: #2c5282;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
}
h4 {
    font-size: 10pt;
    color: #4a5568;
    font-weight: 600;
    margin-top: 12px;
    margin-bottom: 6px;
}
h5 {
    font-size: 9pt;
    color: #718096;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 4px;
}
h6 {
    font-size: 8pt;
    color: #a0aec0;
    font-weight: 600;
    margin-top: 8px;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* --- TABLEAUX --- */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
}
thead th {
    background: #1a365d;
    color: white;
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
    font-size: 8.5pt;
}
tbody td {
    padding: 6px 10px;
    border-bottom: 1px solid #e2e8f0;
}
tbody tr:nth-child(even) { background: #ebf4ff; }
tbody tr:hover { background: #bee3f8; }

/* --- CODE --- */
pre {
    background: #1a202c;
    color: #e2e8f0;
    padding: 14px 18px;
    border-radius: 6px;
    font-family: 'Consolas', 'Fira Code', monospace;
    font-size: 8pt;
    line-height: 1.5;
    overflow-x: auto;
    margin: 10px 0;
    page-break-inside: avoid;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
}
code {
    background: #edf2f7;
    color: #c53030;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: 'Consolas', 'Fira Code', monospace;
    font-size: 8.5pt;
}
pre code {
    background: none;
    color: inherit;
    padding: 0;
}

/* --- LISTES --- */
ul, ol {
    margin: 8px 0;
    padding-left: 24px;
}
li {
    margin-bottom: 4px;
    line-height: 1.5;
}

/* --- BLOCKQUOTE --- */
blockquote {
    border-left: 4px solid #2b6cb0;
    margin: 12px 0;
    padding: 10px 16px;
    background: #f0f5ff;
    color: #2a4365;
    border-radius: 0 4px 4px 0;
    font-style: italic;
}

/* --- SEPARATEURS --- */
hr {
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 20px 0;
}

/* --- SECTIONS --- */
.section-box {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 14px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    page-break-inside: avoid;
}

/* --- ANNEXES --- */
.annexes {
    margin-top: 30px;
    padding-top: 16px;
    border-top: 3px solid #1a365d;
}
.annexes h2 {
    color: #1a365d;
}
.source-item {
    font-size: 8.5pt;
    color: #4a5568;
    padding: 4px 0;
    border-bottom: 1px dotted #e2e8f0;
}

/* --- IMAGES --- */
img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    margin: 8px 0;
}

/* --- PRINT HELPERS --- */
.page-break { page-break-before: always; }
.no-break { page-break-inside: avoid; }
"""


# =====================================================================
# MOTEUR WEASYPRINT (HTML/CSS)
# =====================================================================
def markdown_to_html(content):
    """Convertit le markdown en HTML structure avec sections."""
    lines = content.split('\n')
    html_parts = []
    i = 0
    in_list = False
    in_ol = False

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        # Fermer les listes en cours si la ligne n'est pas une liste
        if in_list and not re.match(r'^[-*]\s', stripped):
            html_parts.append('</ul>')
            in_list = False
        if in_ol and not re.match(r'^\d+\.\s', stripped):
            html_parts.append('</ol>')
            in_ol = False

        # Image : ![alt](path)
        img_match = re.match(r'!\[([^\]]*)\]\((.+?)\)', stripped)
        if img_match:
            alt, path = img_match.group(1), img_match.group(2)
            b64 = image_to_base64(path)
            if b64:
                html_parts.append(f'<img src="{b64}" alt="{alt}" />')
            else:
                html_parts.append(f'<p style="color:#a0aec0;font-style:italic">[Image: {alt} - {os.path.basename(path)}]</p>')
            i += 1
            continue

        # Bloc code
        if stripped.startswith('```'):
            lang = stripped[3:].strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))
                i += 1
            i += 1
            code_html = '\n'.join(code_lines)
            html_parts.append(f'<pre><code>{code_html}</code></pre>')
            continue

        # Tableau markdown
        if '|' in stripped and stripped.startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i].strip() and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            html_parts.append(render_table_html(table_lines))
            continue

        # Titres H1-H6
        h_match = re.match(r'^(#{1,6})\s+(.+)', stripped)
        if h_match:
            level = len(h_match.group(1))
            title_text = h_match.group(2).strip()
            # Nettoyer le markdown inline dans le titre
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

        # Blockquote
        if stripped.startswith('>'):
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

        # Paragraphe normal
        html_parts.append(f'<p>{format_inline(stripped)}</p>')
        i += 1

    # Fermer les listes ouvertes
    if in_list:
        html_parts.append('</ul>')
    if in_ol:
        html_parts.append('</ol>')

    return '\n'.join(html_parts)


def format_inline(text):
    """Applique le formatage inline markdown vers HTML."""
    # Gras
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italique
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Code inline
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Liens
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def render_table_html(lines):
    """Convertit un tableau markdown en HTML."""
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


def build_toc_html(toc):
    """Genere le HTML de la table des matieres."""
    if not toc:
        return ''
    html = '<div class="toc"><h3>Table des matieres</h3><ul>'
    for item in toc:
        html += f'<li class="toc-{item["level"]}"><a href="#{item["anchor"]}">{item["title"]}</a></li>'
    html += '</ul></div>'
    return html


def build_confidence_html(score):
    """Genere le HTML du score de confiance."""
    if score is None:
        return ''
    color = score_color(score)
    label = 'Elevee' if score >= 70 else ('Moyenne' if score >= 40 else 'Faible')
    return f'''<div class="confidence-box">
        <span style="font-size:9pt;color:#718096;font-weight:600">Confiance :</span>
        <div class="confidence-bar">
            <div class="fill" style="width:{score}%;background:{color}"></div>
        </div>
        <span class="confidence-label" style="color:{color}">{score}%</span>
        <span style="font-size:8pt;color:{color};font-weight:600">{label}</span>
    </div>'''


def build_executive_summary_html(summary):
    """Genere le HTML du resume executif."""
    if not summary:
        return ''
    paras = summary.split('\n')
    content = ''.join(f'<p>{format_inline(p)}</p>' for p in paras if p.strip())
    return f'<div class="executive-summary"><h3>Resume executif</h3>{content}</div>'


def extract_sources(content):
    """Extrait les sources/references du contenu."""
    sources = []
    in_sources = False
    for line in content.split('\n'):
        stripped = line.strip().lower()
        if re.match(r'^#{1,3}\s*(sources|references|bibliographie|liens)', stripped):
            in_sources = True
            continue
        if in_sources:
            if re.match(r'^#{1,2}\s', line.strip()) and not re.match(r'^#{3,}', line.strip()):
                break
            if line.strip().startswith(('- ', '* ', '1.')):
                sources.append(re.sub(r'^[-*\d.]\s*', '', line.strip()))
            elif line.strip() and not line.strip().startswith('#'):
                sources.append(line.strip())
    return sources


def build_annexes_html(sources):
    """Genere le HTML des annexes."""
    if not sources:
        return ''
    html = '<div class="annexes"><h2>Annexes - Sources et Methodologie</h2>'
    html += '<div class="section-box">'
    for src in sources:
        html += f'<div class="source-item">{format_inline(src)}</div>'
    html += '</div></div>'
    return html


def generate_pdf_weasyprint(title, content, path, doc_type='analysis'):
    """Genere un PDF professionnel via WeasyPrint."""
    info = DOC_TYPES.get(doc_type, DOC_TYPES['analysis'])
    now = datetime.now()
    date_str = now.strftime('%d/%m/%Y a %H:%M')

    # Extraire les elements structurels
    toc = extract_toc(content)
    summary = extract_executive_summary(content)
    score = extract_confidence_score(content)
    sources = extract_sources(content)

    # Construire le CSS avec la date
    css = CSS_TEMPLATE.replace('REPORT_DATE_PLACEHOLDER', date_str)

    # Construire le body HTML
    body_html = markdown_to_html(content)

    # Assembler le document complet
    html_doc = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <style>{css}</style>
</head>
<body>
    <!-- BANDEAU TITRE -->
    <div class="cover-banner">
        <h1>{title}</h1>
        <p class="subtitle">{info['label']}  |  {date_str}  |  Claude Code - Deep Research</p>
    </div>

    <!-- RESUME EXECUTIF -->
    {build_executive_summary_html(summary)}

    <!-- SCORE DE CONFIANCE -->
    {build_confidence_html(score)}

    <!-- TABLE DES MATIERES -->
    {build_toc_html(toc)}

    <!-- CONTENU PRINCIPAL -->
    <div class="main-content">
        {body_html}
    </div>

    <!-- ANNEXES -->
    {build_annexes_html(sources)}

    <!-- PIED DE DOCUMENT -->
    <div style="margin-top:30px;padding-top:12px;border-top:2px solid #e2e8f0;text-align:center">
        <p style="font-size:7.5pt;color:#a0aec0">
            Document genere automatiquement par Claude Code - Deep Research Multi-Agents<br>
            {date_str} | acollenne@gmail.com
        </p>
    </div>
</body>
</html>"""

    # Generer le PDF
    WeasyHTML(string=html_doc).write_pdf(path)
    return path


# =====================================================================
# MOTEUR FPDF2 (FALLBACK AMELIORE)
# =====================================================================
def get_header_color(doc_type):
    colors = {
        'code': (30, 30, 80),
        'guide': (20, 100, 60),
        'modifications': (120, 60, 10),
        'analysis': (26, 54, 93),  # #1a365d
    }
    return colors.get(doc_type, (26, 54, 93))


class PDFPro(FPDF):
    """Classe FPDF amelioree avec en-tetes/pieds de page pro."""

    def __init__(self, title, doc_type='analysis', toc_entries=None):
        super().__init__()
        self.doc_type = doc_type
        self.hcolor = get_header_color(doc_type)
        self.toc_entries = toc_entries or []
        self.set_auto_page_break(True, margin=20)
        self.set_margins(16, 20, 16)
        # Charger police Unicode si disponible (preserve accents francais)
        self._has_dejavu = False
        if DEJAVU_FONT_PATH:
            try:
                self.add_font('DejaVu', '', DEJAVU_FONT_PATH, uni=True)
                self.add_font('DejaVu', 'B', DEJAVU_FONT_PATH, uni=True)
                self.add_font('DejaVu', 'I', DEJAVU_FONT_PATH, uni=True)
                self._has_dejavu = True
                logger.info(f"Police DejaVuSans chargee depuis {DEJAVU_FONT_PATH}")
            except Exception as e:
                logger.warning(f"Impossible de charger DejaVuSans: {e}")
        self.doc_title = sanitize(title[:90])

    def header(self):
        r, g, b = self.hcolor
        # Ligne coloree en haut
        self.set_fill_color(r, g, b)
        self.rect(0, 0, 210, 3, 'F')
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(r, g, b)
        self.set_xy(16, 6)
        self.cell(120, 6, self.doc_title, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(160, 160, 160)
        self.cell(55, 6, datetime.now().strftime("%d/%m/%Y %H:%M"),
                  align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(226, 232, 240)
        self.line(16, self.get_y() + 1, 194, self.get_y() + 1)
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-14)
        # Ligne separatrice
        self.set_draw_color(226, 232, 240)
        self.line(16, self.get_y(), 194, self.get_y())
        self.ln(2)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(160, 175, 200)
        self.cell(90, 6, "Claude Code | Deep Research Multi-Agents")
        self.cell(88, 6, f"Page {self.page_no()}/{{nb}}",
                  align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def add_cover(self, title, doc_type, summary='', score=None):
        """Ajoute une page de couverture professionnelle."""
        r, g, b = self.hcolor
        # Bandeau principal
        self.set_fill_color(r, g, b)
        self.rect(16, self.get_y(), 178, 22, 'F')
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.set_xy(20, self.get_y() + 3)
        self.multi_cell(170, 8, sanitize(title[:100]), align="C")
        self.set_text_color(200, 215, 240)
        self.set_font("Helvetica", "I", 8.5)
        info = DOC_TYPES.get(doc_type, DOC_TYPES['analysis'])
        self.cell(178, 5, f"{info['label']}  |  {datetime.now().strftime('%d/%m/%Y a %H:%M')}  |  Claude Code",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(6)

        # Score de confiance
        if score is not None:
            self._draw_confidence(score)
            self.ln(4)

        # Resume executif
        if summary:
            self._draw_executive_summary(summary)
            self.ln(4)

    def _draw_confidence(self, score):
        """Dessine la barre de confiance."""
        if score >= 70:
            cr, cg, cb = (56, 161, 105)
        elif score >= 40:
            cr, cg, cb = (214, 158, 46)
        else:
            cr, cg, cb = (229, 62, 62)

        x0 = 16
        self.set_fill_color(247, 250, 252)
        self.set_draw_color(226, 232, 240)
        self.rect(x0, self.get_y(), 178, 12, 'DF')
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(113, 128, 150)
        self.set_xy(x0 + 4, self.get_y() + 1)
        self.cell(30, 10, "Confiance :")
        # Barre de fond
        bar_x = x0 + 36
        bar_w = 110
        self.set_fill_color(226, 232, 240)
        self.rect(bar_x, self.get_y() + 3, bar_w, 6, 'F')
        # Barre remplie
        self.set_fill_color(cr, cg, cb)
        self.rect(bar_x, self.get_y() + 3, bar_w * score / 100, 6, 'F')
        # Pourcentage
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(cr, cg, cb)
        self.set_xy(bar_x + bar_w + 4, self.get_y())
        self.cell(28, 10, f"{score}%", align="R")
        self.set_text_color(0, 0, 0)
        self.ln(14)

    def _draw_executive_summary(self, summary):
        """Dessine le bloc resume executif avec hauteur dynamique."""
        r, g, b = 43, 108, 176  # #2b6cb0
        x0 = 16
        y0 = self.get_y()
        padding = 12  # padding vertical total (haut + bas)
        title_h = 7   # hauteur du titre "Resume executif"
        clean = sanitize(strip_inline(summary[:400]))

        # Calculer la hauteur reelle du texte avec dry_run
        self.set_font("Helvetica", size=8)
        try:
            text_height = self.multi_cell(162, 4, clean, dry_run=True).height
        except (TypeError, AttributeError):
            # Fallback si dry_run non supporte (ancienne version fpdf2)
            str_w = self.get_string_width(clean)
            nb_lines = ceil(str_w / 162) if str_w > 0 else 1
            text_height = nb_lines * 4

        box_height = max(title_h + text_height + padding, 20)

        # Bordure gauche epaisse
        self.set_fill_color(r, g, b)
        self.rect(x0, y0, 3, box_height, 'F')
        # Fond
        self.set_fill_color(235, 248, 255)
        self.rect(x0 + 3, y0, 175, box_height, 'F')
        # Titre
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(26, 54, 93)
        self.set_xy(x0 + 8, y0 + 2)
        self.cell(0, 5, "Resume executif")
        # Contenu
        self.set_font("Helvetica", size=8)
        self.set_text_color(42, 67, 101)
        self.set_xy(x0 + 8, y0 + 2 + title_h)
        self.multi_cell(162, 4, clean)
        self.set_text_color(0, 0, 0)
        y_end = max(self.get_y(), y0 + box_height)
        self.set_y(y_end)

    def add_toc(self, toc):
        """Ajoute la table des matieres."""
        if not toc:
            return
        self.set_fill_color(247, 250, 252)
        self.set_draw_color(226, 232, 240)
        x0 = 16
        y0 = self.get_y()
        # Titre TdM
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(26, 54, 93)
        self.cell(0, 7, "Table des matieres", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(43, 108, 176)
        self.line(x0, self.get_y(), x0 + 60, self.get_y())
        self.ln(3)
        # Entrees
        for item in toc:
            indent = (item['level'] - 1) * 8
            if item['level'] == 1:
                self.set_font("Helvetica", "B", 8.5)
                self.set_text_color(26, 54, 93)
            elif item['level'] == 2:
                self.set_font("Helvetica", size=8)
                self.set_text_color(45, 55, 72)
            else:
                self.set_font("Helvetica", "I", 7.5)
                self.set_text_color(113, 128, 150)
            self.set_x(x0 + indent)
            self.cell(0, 4.5, sanitize(item['title'][:70]),
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(6)


def render_table_fpdf(pdf, lines, hcolor):
    """Rendu de tableau ameliore pour fpdf2."""
    rows = []
    for line in lines:
        if re.match(r'^\s*\|[-:\s|]+\|\s*$', line):
            continue
        cells = [sanitize(strip_inline(c.strip())) for c in line.strip('| ').split('|')]
        if any(c.strip() for c in cells):
            rows.append(cells)
    if not rows:
        return
    col_count = max(len(r) for r in rows)
    col_w = 162 / col_count

    for i, row in enumerate(rows):
        if i == 0:
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_fill_color(*hcolor)
            pdf.set_text_color(255, 255, 255)
        elif i % 2 == 0:
            pdf.set_font("Helvetica", size=7.5)
            pdf.set_fill_color(235, 244, 255)
            pdf.set_text_color(45, 55, 72)
        else:
            pdf.set_font("Helvetica", size=7.5)
            pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(45, 55, 72)
        pdf.set_x(pdf.l_margin)
        for j in range(col_count):
            cell_txt = row[j].strip()[:55] if j < len(row) else ''
            pdf.cell(col_w, 5.5, cell_txt, border=1, fill=True)
        pdf.ln()
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)


def render_text_with_links(pdf, raw_text, font_family="Helvetica", font_size=8.5):
    """Rend du texte avec liens cliquables en fpdf2.
    Detecte les patterns [texte](url) et utilise pdf.cell(link=url)."""
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
    # Nettoyer le gras/italique pour le texte hors liens
    clean_text = re.sub(r'\*\*(.+?)\*\*', r'\1', raw_text)
    clean_text = re.sub(r'\*(.+?)\*', r'\1', clean_text)
    clean_text = re.sub(r'`(.+?)`', r'[\1]', clean_text)

    parts = link_pattern.split(clean_text)
    # parts = [text_before, link_text, link_url, text_between, link_text2, url2, ...]
    idx = 0
    while idx < len(parts):
        if idx + 2 < len(parts) and (idx % 3 == 1):
            # C'est un lien : parts[idx] = texte, parts[idx+1] = url
            link_text = sanitize(parts[idx])
            link_url = parts[idx + 1]
            pdf.set_text_color(43, 108, 176)  # Bleu lien
            pdf.set_font(font_family, "U", font_size)
            pdf.cell(pdf.get_string_width(link_text) + 1, 5, link_text, link=link_url)
            pdf.set_font(font_family, "", font_size)
            pdf.set_text_color(45, 55, 72)
            idx += 2  # Sauter texte + url
        else:
            # Texte normal
            text_part = sanitize(parts[idx])
            if text_part:
                pdf.cell(pdf.get_string_width(text_part) + 0.5, 5, text_part)
            idx += 1


def try_insert_image(pdf, img_path):
    """Insert une image dans le PDF fpdf2."""
    try:
        if os.path.exists(img_path):
            img_w = 155
            pdf.set_x(pdf.l_margin)
            pdf.image(img_path, x=pdf.l_margin, w=img_w)
            pdf.ln(4)
            return True
    except Exception as e:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(160, 175, 200)
        pdf.cell(0, 5, f"[Image non disponible: {os.path.basename(img_path)}]",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)
    return False


def markdown_to_pdf_fpdf(pdf, content):
    """Rendu markdown vers fpdf2 (fallback ameliore)."""
    lines = content.split('\n')
    i = 0
    hcolor = pdf.hcolor

    while i < len(lines):
        raw = lines[i]
        line = sanitize(strip_inline(raw))
        stripped = line.strip()

        # Image
        img_match = re.match(r'!\[.*?\]\((.+?)\)', raw.strip())
        if img_match:
            try_insert_image(pdf, img_match.group(1))
            i += 1
            continue

        # Bloc code
        if stripped.startswith('```'):
            i += 1
            pdf.set_fill_color(26, 32, 44)
            pdf.set_draw_color(45, 55, 72)
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_line = sanitize(lines[i])
                pdf.set_font("Courier", size=7)
                pdf.set_text_color(226, 232, 240)
                pdf.set_x(pdf.l_margin)
                pdf.cell(0, 4.2, '  ' + code_line[:120], fill=True,
                         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                i += 1
            i += 1
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)
            continue

        # Tableau
        if '|' in stripped and stripped.startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i].strip() and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            pdf.set_x(pdf.l_margin)
            render_table_fpdf(pdf, table_lines, hcolor)
            continue

        # H1
        if re.match(r'^# [^#]', stripped):
            pdf.ln(5)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(*hcolor)
            pdf.cell(0, 8, stripped[2:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_draw_color(*hcolor)
            pdf.set_line_width(0.6)
            pdf.line(16, pdf.get_y(), 194, pdf.get_y())
            pdf.set_line_width(0.2)
            pdf.ln(3)
            pdf.set_text_color(0, 0, 0)

        # H2
        elif re.match(r'^## [^#]', stripped):
            pdf.ln(4)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(43, 108, 176)
            pdf.cell(0, 7, stripped[3:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_draw_color(190, 227, 248)
            pdf.line(16, pdf.get_y(), 194, pdf.get_y())
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)

        # H3
        elif re.match(r'^### [^#]', stripped):
            pdf.ln(3)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(44, 82, 130)
            pdf.cell(0, 6, stripped[4:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)

        # H4
        elif re.match(r'^#### [^#]', stripped):
            pdf.ln(2)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(74, 85, 104)
            pdf.cell(0, 5.5, stripped[5:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)

        # H5
        elif re.match(r'^##### [^#]', stripped):
            pdf.ln(2)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(113, 128, 150)
            pdf.cell(0, 5, stripped[6:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)

        # H6
        elif re.match(r'^###### ', stripped):
            pdf.ln(1)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_text_color(160, 174, 192)
            pdf.cell(0, 4.5, stripped[7:].upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)

        # Separateur
        elif re.match(r'^-{3,}$', stripped):
            pdf.ln(3)
            pdf.set_draw_color(226, 232, 240)
            pdf.set_line_width(0.4)
            pdf.line(16, pdf.get_y(), 194, pdf.get_y())
            pdf.set_line_width(0.2)
            pdf.ln(3)

        # Liste a puces
        elif re.match(r'^[-*] ', stripped):
            pdf.set_x(pdf.l_margin + 4)
            pdf.set_font("Helvetica", size=8.5)
            pdf.set_text_color(45, 55, 72)
            # Puce coloree
            pdf.set_text_color(*hcolor)
            pdf.cell(4, 5, chr(149))
            pdf.set_text_color(45, 55, 72)
            pdf.multi_cell(0, 5, stripped[2:].strip())

        # Liste numerotee
        elif re.match(r'^\d+\. ', stripped):
            pdf.set_x(pdf.l_margin + 4)
            pdf.set_font("Helvetica", size=8.5)
            pdf.set_text_color(45, 55, 72)
            pdf.multi_cell(0, 5, stripped)

        # Ligne vide
        elif not stripped:
            pdf.ln(2)

        # Ligne gras complete
        elif stripped.startswith('**') and stripped.endswith('**') and len(stripped) > 4:
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 9)
            pdf.multi_cell(0, 5, stripped.strip('*'))

        # Texte normal (avec detection de liens cliquables)
        else:
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", size=8.5)
            pdf.set_text_color(45, 55, 72)
            # Si le texte brut contient des liens markdown, les rendre cliquables
            if re.search(r'\[([^\]]+)\]\(([^\)]+)\)', raw.strip()):
                render_text_with_links(pdf, raw.strip())
                pdf.ln(5)
            else:
                pdf.multi_cell(0, 5, stripped)

        i += 1
    pdf.set_text_color(0, 0, 0)


def generate_pdf_fpdf(title, content, path, doc_type='analysis'):
    """Genere un PDF professionnel via fpdf2 (fallback)."""
    toc = extract_toc(content)
    summary = extract_executive_summary(content)
    score = extract_confidence_score(content)

    pdf = PDFPro(title, doc_type, toc)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Couverture
    pdf.add_cover(title, doc_type, summary, score)

    # Table des matieres
    pdf.add_toc(toc)

    # Contenu principal
    markdown_to_pdf_fpdf(pdf, content)

    # Pied de document
    pdf.ln(8)
    pdf.set_draw_color(226, 232, 240)
    pdf.set_line_width(0.4)
    pdf.line(16, pdf.get_y(), 194, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(160, 175, 200)
    pdf.cell(0, 4, f"Document genere par Claude Code - Deep Research | {datetime.now().strftime('%d/%m/%Y %H:%M')}",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(path)
    return path


# =====================================================================
# POINT D'ENTREE GENERATION PDF
# =====================================================================
def generate_pdf(title, content, path, doc_type='analysis'):
    """Genere un PDF en utilisant le meilleur moteur disponible."""
    if USE_WEASYPRINT:
        logger.info(f"  [WeasyPrint] Generation PDF : {Path(path).name}")
        return generate_pdf_weasyprint(title, content, path, doc_type)
    else:
        logger.info(f"  [fpdf2] Generation PDF : {Path(path).name}")
        return generate_pdf_fpdf(title, content, path, doc_type)


# =====================================================================
# ENVOI EMAIL (conserve et ameliore)
# =====================================================================
def send_email(subject, pdf_paths, recipient=DEFAULT_TO):
    """Envoie un email avec les PDFs en piece jointe."""
    sender = None
    pwd = None
    # Tenter de charger la config depuis le fichier JSON
    try:
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
        sender = cfg.get("sender_email")
        pwd = cfg.get("gmail_app_password")
    except FileNotFoundError:
        logger.warning(f"Fichier de config introuvable : {CONFIG_PATH}")
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Erreur lecture config email : {e}")
    # Fallback vers variables d'environnement
    if not sender:
        sender = os.environ.get('GMAIL_SENDER')
    if not pwd:
        pwd = os.environ.get('GMAIL_APP_PASSWORD')
    # Si toujours pas de credentials, sauvegarder localement sans crash
    if not sender or not pwd:
        logger.warning(
            "Configuration email manquante (ni email_config.json, ni variables "
            "d'environnement GMAIL_SENDER/GMAIL_APP_PASSWORD). "
            "PDF genere localement sans envoi."
        )
        for p in (pdf_paths if isinstance(pdf_paths, list) else [pdf_paths]):
            logger.info(f"  PDF disponible : {p}")
        return False

    if isinstance(pdf_paths, str):
        pdf_paths = [pdf_paths]

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    n = len(pdf_paths)
    files_list = ''.join(f'<li style="padding:4px 0">{Path(p).name}</li>' for p in pdf_paths)
    html = f"""<html><body style="font-family:'Segoe UI',Arial,sans-serif;max-width:700px;margin:auto;color:#2d3748">
    <div style="background:linear-gradient(135deg,#1a365d 0%,#2b6cb0 100%);padding:22px 28px;border-radius:8px 8px 0 0">
      <h2 style="color:white;margin:0;font-size:18px;font-weight:700">{subject}</h2>
      <p style="color:#bee3f8;margin:6px 0 0;font-size:11px">
        {datetime.now().strftime('%d/%m/%Y %H:%M')} &mdash; Claude Code - Deep Research
      </p>
    </div>
    <div style="background:#f7fafc;padding:20px 28px;border:1px solid #e2e8f0;border-top:none;border-radius:0 0 8px 8px">
      <p style="margin-top:0;color:#2d3748">{n} document(s) en piece(s) jointe(s) :</p>
      <ul style="color:#2b6cb0;font-weight:500">{files_list}</ul>
      <hr style="border:none;border-top:1px solid #e2e8f0;margin:16px 0">
      <p style="font-size:10px;color:#a0aec0;margin-bottom:0">
        Genere automatiquement par le systeme Deep Research multi-agents.
      </p>
    </div></body></html>"""
    msg.attach(MIMEText(html, "html"))

    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                          f'attachment; filename="{Path(pdf_path).name}"')
            msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
        srv.login(sender, pwd)
        srv.send_message(msg)
    logger.info(f"[Email] Envoye a {recipient} ({n} PDF(s))")


# =====================================================================
# MAIN
# =====================================================================
def main():
    if len(sys.argv) < 3:
        logger.info("Usage: python send_report.py 'Sujet' 'contenu_ou_--file' [email]")
        logger.info("       python send_report.py 'Sujet' --file chemin.md [email]")
        logger.info(f"Moteur PDF : {'WeasyPrint (HTML/CSS)' if USE_WEASYPRINT else 'fpdf2 (fallback)'}")
        sys.exit(1)

    subject = sys.argv[1]

    # Support --file pour lire le contenu depuis un fichier
    if sys.argv[2] == '--file':
        if len(sys.argv) < 4:
            logger.error("Erreur: --file necessite un chemin de fichier")
            sys.exit(1)
        file_path = sys.argv[3]
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        recipient = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_TO
    else:
        content = sys.argv[2]
        recipient = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_TO

    REPORTS_DIR.mkdir(exist_ok=True)
    doc_type = detect_type(subject)
    safe = re.sub(r'[^\w-]', '_', subject[:40])
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = str(REPORTS_DIR / f"rapport_{safe}_{ts}.pdf")

    engine = "WeasyPrint" if USE_WEASYPRINT else "fpdf2"
    logger.info(f"[Generation PDF] Moteur: {engine} | Type: {doc_type}")
    logger.info(f"  Titre : {subject[:60]}")
    generate_pdf(subject, content, pdf_path, doc_type)
    logger.info(f"  PDF genere : {pdf_path}")
    logger.info(f"  Envoi email a {recipient}...")
    result = send_email(subject, [pdf_path], recipient)
    if result is False:
        logger.warning("[SKIP] Email non envoye (config manquante). PDF disponible localement.")
    else:
        logger.info("[OK] Rapport envoye avec succes.")


if __name__ == "__main__":
    main()
