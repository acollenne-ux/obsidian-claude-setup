"""
mermaid.py — Rendu de blocs Mermaid en images PNG embedables.

Strategie :
  1. Detecter `mmdc` (mermaid-cli via npm) -> rendu PNG haute qualite
  2. Sinon : afficher le code source dans un bloc style "diagramme"

Pas de dependance Python obligatoire (mmdc est externe via Node.js).
"""
import os
import shutil
import subprocess
import tempfile
import hashlib
import logging
from pathlib import Path
from .markdown_parser import image_to_base64

logger = logging.getLogger(__name__)

# Cache pour eviter de re-rendre le meme diagramme
_CACHE_DIR = Path(tempfile.gettempdir()) / "mermaid_cache"
_CACHE_DIR.mkdir(exist_ok=True)


def is_mermaid_available() -> bool:
    """Verifie si mermaid-cli (mmdc) est disponible."""
    return shutil.which('mmdc') is not None or shutil.which('mmdc.cmd') is not None


def render_mermaid(code: str, theme: str = 'default') -> str | None:
    """Rend un bloc Mermaid en data URI base64 PNG.

    Retourne None si mmdc indisponible ou en cas d'erreur.
    """
    if not is_mermaid_available():
        return None

    # Hash pour cache
    h = hashlib.md5(f"{code}|{theme}".encode()).hexdigest()
    cached_png = _CACHE_DIR / f"{h}.png"

    if not cached_png.exists():
        # Ecrire le code dans un fichier temporaire
        with tempfile.NamedTemporaryFile('w', suffix='.mmd', delete=False, encoding='utf-8') as f:
            f.write(code)
            mmd_path = f.name

        try:
            # mmdc -i input.mmd -o output.png -t default -b transparent
            cmd = [
                'mmdc' if shutil.which('mmdc') else 'mmdc.cmd',
                '-i', mmd_path,
                '-o', str(cached_png),
                '-t', theme,
                '-b', 'white',
                '-w', '1200',
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                logger.warning(f"[Mermaid] Erreur rendu : {result.stderr[:200]}")
                return None
        except (subprocess.TimeoutExpired, OSError) as e:
            logger.warning(f"[Mermaid] Exception : {e}")
            return None
        finally:
            try:
                os.unlink(mmd_path)
            except OSError:
                pass

    return image_to_base64(str(cached_png))


def mermaid_fallback_html(code: str) -> str:
    """Affiche le code Mermaid dans un bloc style si rendu indisponible."""
    from .components import html_escape
    return f'''
<div class="mermaid-fallback">
    <div class="mermaid-label">[Diagramme Mermaid]</div>
    <pre class="mermaid-code">{html_escape(code)}</pre>
    <p class="mermaid-hint">Installez mermaid-cli (npm i -g @mermaid-js/mermaid-cli) pour le rendu visuel.</p>
</div>
'''


def render_mermaid_block(code: str) -> str:
    """Point d'entree : rend un bloc Mermaid en HTML embedable."""
    b64 = render_mermaid(code)
    if b64:
        return f'<div class="mermaid-diagram"><img src="{b64}" alt="Mermaid diagram" /></div>'
    return mermaid_fallback_html(code)
