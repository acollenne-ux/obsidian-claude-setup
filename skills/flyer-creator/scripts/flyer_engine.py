#!/usr/bin/env python3
"""
Flyer Engine — Moteur principal de génération de flyers via HTML/CSS + Playwright.

Usage:
    python3 flyer_engine.py --html <path_to_html> --output <output.png> [options]

Options:
    --width <px>        Largeur du viewport (défaut: 2480 pour A4 300DPI)
    --height <px>       Hauteur du viewport (défaut: 3508 pour A4 300DPI)
    --format <format>   Format prédéfini: a4, a5, square, letter, instagram, story
    --dpi <dpi>         Résolution: 300 (print), 150 (web), 72 (screen)
    --scale <factor>    Facteur d'échelle du rendu (défaut: 2 pour haute qualité)
    --pdf               Générer aussi un PDF
    --wait <ms>         Temps d'attente pour le chargement des polices (défaut: 3000)
"""

import argparse
import os
import sys
import json
import base64
from pathlib import Path

# Formats prédéfinis (largeur x hauteur en pixels)
FORMATS = {
    # 300 DPI
    "a4":        (2480, 3508),
    "a5":        (1748, 2480),
    "square":    (2480, 2480),
    "letter":    (2551, 3295),
    # Digital
    "instagram": (1080, 1080),
    "story":     (1080, 1920),
    "facebook":  (1200, 630),
    # 150 DPI
    "a4_web":    (1240, 1754),
    "a5_web":    (874, 1240),
}

# Facteurs d'échelle par DPI
DPI_SCALE = {
    300: 2,    # Viewport 1240x1754, scale 2x → 2480x3508
    150: 1,    # Viewport 1240x1754, scale 1x → 1240x1754
    72:  1,    # Viewport natif
}


def encode_image_base64(image_path: str) -> str:
    """Encode une image en base64 pour embedding HTML."""
    ext = Path(image_path).suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml',
    }
    mime = mime_types.get(ext, 'image/png')
    with open(image_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:{mime};base64,{data}"


def inject_images_as_base64(html_content: str, image_map: dict) -> str:
    """
    Remplace les placeholders d'images dans le HTML par des data URIs base64.
    
    image_map: dict de {placeholder: chemin_fichier}
    Ex: {"{{BACKGROUND_IMAGE}}": "/path/to/bg.jpg", "{{SPONSOR1}}": "/path/to/logo.png"}
    """
    for placeholder, filepath in image_map.items():
        if os.path.exists(filepath):
            data_uri = encode_image_base64(filepath)
            html_content = html_content.replace(placeholder, data_uri)
        else:
            print(f"⚠ Image non trouvée: {filepath}", file=sys.stderr)
    return html_content


def inject_text_data(html_content: str, data: dict) -> str:
    """
    Remplace les placeholders de texte dans le HTML.
    
    data: dict de {placeholder: valeur}
    Ex: {"{{TITLE}}": "Mon Événement", "{{DATE}}": "15 Juin 2026"}
    """
    for placeholder, value in data.items():
        html_content = html_content.replace(placeholder, str(value))
    return html_content


def render_html_to_png(
    html_content: str,
    output_path: str,
    width: int = 1240,
    height: int = 1754,
    scale: int = 2,
    wait_ms: int = 3000
) -> str:
    """
    Rend le HTML en PNG via Playwright (Chromium headless).
    
    Returns: chemin du fichier PNG généré
    """
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=['--no-sandbox', '--disable-gpu', '--font-render-hinting=none']
        )
        
        page = browser.new_page(
            viewport={'width': width, 'height': height},
            device_scale_factor=scale
        )
        
        # Charger le HTML
        page.set_content(html_content, wait_until='networkidle')
        
        # Attendre le chargement des Google Fonts
        page.wait_for_timeout(wait_ms)
        
        # Attendre que les fonts soient chargées
        try:
            page.evaluate("() => document.fonts.ready")
        except Exception:
            pass  # Fallback si l'API fonts n'est pas disponible
        
        # Capture en PNG
        page.screenshot(
            path=output_path,
            full_page=False,
            type='png'
        )
        
        browser.close()
    
    print(f"✅ Flyer généré: {output_path}")
    print(f"   Résolution: {width * scale}×{height * scale}px")
    return output_path


def render_html_to_pdf(
    html_content: str,
    output_path: str,
    width: int = 1240,
    height: int = 1754,
    wait_ms: int = 3000
) -> str:
    """Rend le HTML en PDF via Playwright."""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox', '--disable-gpu'])
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.set_content(html_content, wait_until='networkidle')
        page.wait_for_timeout(wait_ms)
        
        page.pdf(
            path=output_path,
            width=f"{width}px",
            height=f"{height}px",
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        
        browser.close()
    
    print(f"✅ PDF généré: {output_path}")
    return output_path


def build_flyer_html(
    template_path: str,
    text_data: dict = None,
    image_map: dict = None,
    custom_css: str = None,
    google_fonts: list = None
) -> str:
    """
    Construit le HTML final du flyer à partir d'un template.
    
    Args:
        template_path: chemin vers le template HTML
        text_data: dict des textes à injecter
        image_map: dict des images à injecter en base64
        custom_css: CSS additionnel à injecter
        google_fonts: liste des noms de Google Fonts à charger
    
    Returns: HTML complet prêt à rendre
    """
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Injecter les Google Fonts
    if google_fonts:
        fonts_query = "&family=".join([f.replace(' ', '+') for f in google_fonts])
        fonts_link = f'<link href="https://fonts.googleapis.com/css2?family={fonts_query}&display=swap" rel="stylesheet">'
        html = html.replace('</head>', f'{fonts_link}\n</head>')
    
    # Injecter le CSS personnalisé
    if custom_css:
        html = html.replace('</head>', f'<style>{custom_css}</style>\n</head>')
    
    # Injecter les textes
    if text_data:
        html = inject_text_data(html, text_data)
    
    # Injecter les images en base64
    if image_map:
        html = inject_images_as_base64(html, image_map)
    
    return html


def generate_flyer(
    template_path: str,
    output_path: str,
    text_data: dict = None,
    image_map: dict = None,
    custom_css: str = None,
    google_fonts: list = None,
    format_name: str = "a4",
    dpi: int = 300,
    generate_pdf: bool = False,
    wait_ms: int = 3000
) -> dict:
    """
    Fonction principale de génération de flyer.
    
    Returns: dict avec les chemins des fichiers générés
    """
    # Résoudre le format
    if format_name in FORMATS:
        base_width, base_height = FORMATS[format_name]
    else:
        base_width, base_height = FORMATS["a4"]
    
    # Calculer le viewport et le scale
    scale = DPI_SCALE.get(dpi, 2)
    viewport_width = base_width // scale
    viewport_height = base_height // scale
    
    # Construire le HTML
    html = build_flyer_html(
        template_path=template_path,
        text_data=text_data,
        image_map=image_map,
        custom_css=custom_css,
        google_fonts=google_fonts
    )
    
    results = {}
    
    # Rendre en PNG
    png_path = render_html_to_png(
        html_content=html,
        output_path=output_path,
        width=viewport_width,
        height=viewport_height,
        scale=scale,
        wait_ms=wait_ms
    )
    results['png'] = png_path
    
    # Rendre en PDF si demandé
    if generate_pdf:
        pdf_path = output_path.replace('.png', '.pdf')
        render_html_to_pdf(
            html_content=html,
            output_path=pdf_path,
            width=viewport_width,
            height=viewport_height,
            wait_ms=wait_ms
        )
        results['pdf'] = pdf_path
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Flyer Engine — Génération de flyers professionnels")
    parser.add_argument('--html', required=True, help='Chemin vers le fichier HTML du flyer')
    parser.add_argument('--output', required=True, help='Chemin de sortie du PNG')
    parser.add_argument('--width', type=int, default=None, help='Largeur viewport')
    parser.add_argument('--height', type=int, default=None, help='Hauteur viewport')
    parser.add_argument('--format', default='a4', choices=list(FORMATS.keys()), help='Format prédéfini')
    parser.add_argument('--dpi', type=int, default=300, choices=[72, 150, 300], help='Résolution DPI')
    parser.add_argument('--scale', type=int, default=None, help='Facteur de scale')
    parser.add_argument('--pdf', action='store_true', help='Générer aussi un PDF')
    parser.add_argument('--wait', type=int, default=3000, help='Temps d\'attente fonts (ms)')
    parser.add_argument('--data', default=None, help='Fichier JSON de données textuelles')
    parser.add_argument('--images', default=None, help='Fichier JSON de mapping images')
    
    args = parser.parse_args()
    
    # Lire le HTML
    with open(args.html, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Charger les données
    text_data = {}
    if args.data:
        with open(args.data, 'r', encoding='utf-8') as f:
            text_data = json.load(f)
    
    image_map = {}
    if args.images:
        with open(args.images, 'r', encoding='utf-8') as f:
            image_map = json.load(f)
    
    # Résoudre les dimensions
    if args.width and args.height:
        width, height = args.width, args.height
    else:
        width, height = FORMATS.get(args.format, FORMATS['a4'])
    
    scale = args.scale or DPI_SCALE.get(args.dpi, 2)
    viewport_w = width // scale
    viewport_h = height // scale
    
    # Injecter les données
    if text_data:
        html_content = inject_text_data(html_content, text_data)
    if image_map:
        html_content = inject_images_as_base64(html_content, image_map)
    
    # Rendre
    render_html_to_png(html_content, args.output, viewport_w, viewport_h, scale, args.wait)
    
    if args.pdf:
        pdf_path = args.output.replace('.png', '.pdf')
        render_html_to_pdf(html_content, pdf_path, viewport_w, viewport_h, args.wait)


if __name__ == '__main__':
    main()
