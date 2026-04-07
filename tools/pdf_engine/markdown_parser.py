"""
markdown_parser.py — Parsing enrichi du Markdown vers structures intermediaires.

Gere :
  - Frontmatter YAML (kpis, cover, classification, version, author...)
  - Callouts GitHub-style : > [!NOTE] / [!TIP] / [!IMPORTANT] / [!WARNING] / [!CAUTION]
  - Footnotes [^1] avec section automatique
  - Blocs Mermaid ```mermaid ... ```
  - Code highlighted ```python
  - Tables, listes, headings, blockquotes standards
  - Images ![alt](path) avec resolution + base64
  - Extraction TOC, executive summary, sources, score de confiance

Sortie : dict structure pret pour le renderer.
"""
import re
import os
import base64
from pathlib import Path
from typing import Any


# =====================================================================
# CONSTANTES
# =====================================================================
CALLOUT_TYPES = {
    'NOTE':      {'color': '#2b6cb0', 'bg': '#ebf8ff', 'icon': 'i', 'label': 'Note'},
    'TIP':       {'color': '#38a169', 'bg': '#f0fff4', 'icon': '*', 'label': 'Astuce'},
    'IMPORTANT': {'color': '#805ad5', 'bg': '#faf5ff', 'icon': '!', 'label': 'Important'},
    'WARNING':   {'color': '#d69e2e', 'bg': '#fffaf0', 'icon': '!', 'label': 'Attention'},
    'CAUTION':   {'color': '#e53e3e', 'bg': '#fff5f5', 'icon': 'X', 'label': 'Danger'},
}


# =====================================================================
# FRONTMATTER YAML SIMPLE (sans dependance pyyaml)
# =====================================================================
def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extrait le frontmatter YAML d'un document Markdown.

    Format supporte :
        ---
        title: Mon titre
        author: Alex
        kpis:
          - label: Revenue
            value: $1.2B
            change: +12%
            sentiment: positive
        ---

    Retourne (frontmatter_dict, content_sans_frontmatter).
    """
    if not content.startswith('---'):
        return {}, content

    lines = content.split('\n')
    if len(lines) < 2:
        return {}, content

    # Trouver la fin du frontmatter
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break

    if end_idx is None:
        return {}, content

    yaml_lines = lines[1:end_idx]
    rest = '\n'.join(lines[end_idx + 1:])

    return _simple_yaml_parse(yaml_lines), rest


def _simple_yaml_parse(lines: list[str]) -> dict:
    """Parser YAML minimaliste : strings, listes simples, listes de dicts."""
    result: dict[str, Any] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith('#'):
            i += 1
            continue
        # Cle: valeur sur une ligne
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)$', line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val:
            # Valeur inline
            result[key] = _strip_quotes(val)
            i += 1
        else:
            # Bloc indente (liste ou dict)
            block_lines = []
            i += 1
            while i < len(lines) and (lines[i].startswith(' ') or lines[i].startswith('\t') or not lines[i].strip()):
                if lines[i].strip():
                    block_lines.append(lines[i])
                i += 1
            result[key] = _parse_block(block_lines)
    return result


def _parse_block(lines: list[str]) -> Any:
    """Parse un bloc indente : liste de strings ou liste de dicts."""
    if not lines:
        return None
    # Verifier si c'est une liste de dicts (- key: value)
    first = lines[0].strip()
    if first.startswith('- '):
        items = []
        current_item: dict[str, Any] | None = None
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('- '):
                # Nouveau item
                if current_item is not None:
                    items.append(current_item)
                rest = stripped[2:]
                m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)$', rest)
                if m:
                    current_item = {m.group(1): _strip_quotes(m.group(2).strip())}
                else:
                    # Liste simple de strings
                    items.append(_strip_quotes(rest))
                    current_item = None
            elif current_item is not None:
                m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)$', stripped)
                if m:
                    current_item[m.group(1)] = _strip_quotes(m.group(2).strip())
        if current_item is not None:
            items.append(current_item)
        return items
    return None


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


# =====================================================================
# EXTRACTION D'ELEMENTS STRUCTURELS
# =====================================================================
def extract_toc(content: str) -> list[dict]:
    """Extrait la table des matieres."""
    toc = []
    in_code = False
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r'^(#{1,6})\s+(.+)', stripped)
        if m:
            level = len(m.group(1))
            title = re.sub(r'[*`\[\]()]', '', m.group(2)).strip()
            anchor = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            toc.append({'level': level, 'title': title, 'anchor': anchor})
    return toc


def extract_executive_summary(content: str) -> str:
    """Extrait ou genere un resume executif."""
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
    # Fallback : premiers paragraphes
    paras = []
    for line in lines:
        s = line.strip()
        if s and not s.startswith('#') and not s.startswith('|') and not s.startswith('---') and not s.startswith('>'):
            clean = re.sub(r'[*`]', '', s)
            if len(clean) > 20:
                paras.append(clean)
            if len(paras) >= 3:
                break
    return '\n'.join(paras) if paras else ''


def extract_confidence_score(content: str) -> int | None:
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


def extract_sources(content: str) -> list[str]:
    """Extrait les sources/references."""
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
            if line.strip().startswith(('- ', '* ')) or re.match(r'^\d+\.\s', line.strip()):
                sources.append(re.sub(r'^[-*\d.]\s*', '', line.strip()))
            elif line.strip() and not line.strip().startswith('#'):
                sources.append(line.strip())
    return sources


def extract_footnotes(content: str) -> tuple[str, dict[str, str]]:
    """Extrait les footnotes [^id]: definition et les remplace par des refs.

    Retourne (content_modifie, footnotes_dict).
    """
    footnotes: dict[str, str] = {}
    # Definitions : [^id]: texte
    def_pattern = re.compile(r'^\[\^([^\]]+)\]:\s*(.+)$', re.MULTILINE)
    for m in def_pattern.finditer(content):
        footnotes[m.group(1)] = m.group(2).strip()
    # Supprimer les definitions du contenu
    content = def_pattern.sub('', content)
    return content, footnotes


# =====================================================================
# PARSING PRINCIPAL
# =====================================================================
def parse_markdown_document(content: str) -> dict:
    """Parse complet d'un document Markdown vers structure intermediaire.

    Retourne un dict avec :
      - frontmatter : dict du YAML
      - body        : Markdown sans frontmatter et sans footnote-defs
      - toc         : liste des titres
      - summary     : resume executif
      - score       : score de confiance (ou None)
      - sources     : liste des sources
      - footnotes   : dict id -> texte
      - kpis        : liste des KPI cards (depuis frontmatter)
    """
    fm, body = parse_frontmatter(content)
    body, footnotes = extract_footnotes(body)
    return {
        'frontmatter': fm,
        'body': body,
        'toc': extract_toc(body),
        'summary': extract_executive_summary(body),
        'score': extract_confidence_score(body),
        'sources': extract_sources(body),
        'footnotes': footnotes,
        'kpis': fm.get('kpis', []) if isinstance(fm.get('kpis'), list) else [],
    }


# =====================================================================
# UTILITAIRES IMAGES
# =====================================================================
def image_to_base64(img_path: str) -> str | None:
    """Convertit une image en data URI base64."""
    try:
        if os.path.exists(img_path):
            ext = Path(img_path).suffix.lower().lstrip('.')
            mime = {'png': 'png', 'jpg': 'jpeg', 'jpeg': 'jpeg', 'gif': 'gif', 'svg': 'svg+xml'}.get(ext, 'png')
            with open(img_path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
            return f'data:image/{mime};base64,{b64}'
    except (OSError, ValueError):
        pass
    return None
