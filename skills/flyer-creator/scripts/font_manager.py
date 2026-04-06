#!/usr/bin/env python3
"""
Font Manager — Téléchargement et gestion des Google Fonts pour les flyers.

Usage:
    python3 font_manager.py --fonts "Bebas Neue,Poppins" --output ./assets/fonts/
    python3 font_manager.py --list  # Liste les polices installées localement
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path


# Mapping des polices populaires vers leurs URLs de téléchargement Google Fonts
FONT_URLS = {
    "Bebas Neue": "https://fonts.google.com/download?family=Bebas+Neue",
    "Oswald": "https://fonts.google.com/download?family=Oswald",
    "Anton": "https://fonts.google.com/download?family=Anton",
    "Montserrat": "https://fonts.google.com/download?family=Montserrat",
    "Raleway": "https://fonts.google.com/download?family=Raleway",
    "Playfair Display": "https://fonts.google.com/download?family=Playfair+Display",
    "Abril Fatface": "https://fonts.google.com/download?family=Abril+Fatface",
    "Merriweather": "https://fonts.google.com/download?family=Merriweather",
    "Fredoka One": "https://fonts.google.com/download?family=Fredoka+One",
    "Cormorant Garamond": "https://fonts.google.com/download?family=Cormorant+Garamond",
    "Poppins": "https://fonts.google.com/download?family=Poppins",
    "Open Sans": "https://fonts.google.com/download?family=Open+Sans",
    "Lato": "https://fonts.google.com/download?family=Lato",
    "Inter": "https://fonts.google.com/download?family=Inter",
    "Roboto": "https://fonts.google.com/download?family=Roboto",
    "Nunito": "https://fonts.google.com/download?family=Nunito",
    "Quicksand": "https://fonts.google.com/download?family=Quicksand",
    "Source Sans Pro": "https://fonts.google.com/download?family=Source+Sans+Pro",
    "Work Sans": "https://fonts.google.com/download?family=Work+Sans",
    "Lora": "https://fonts.google.com/download?family=Lora",
    "Baloo 2": "https://fonts.google.com/download?family=Baloo+2",
    "Source Serif Pro": "https://fonts.google.com/download?family=Source+Serif+Pro",
}


def get_google_fonts_css_url(font_names: list, weights: str = "300;400;500;600;700;800;900") -> str:
    """
    Génère l'URL CSS Google Fonts pour injection dans le HTML.
    
    Returns: URL complète pour <link href="...">
    """
    families = []
    for name in font_names:
        encoded = name.replace(' ', '+')
        families.append(f"family={encoded}:wght@{weights}")
    
    query = "&".join(families)
    return f"https://fonts.googleapis.com/css2?{query}&display=swap"


def get_google_fonts_link_tag(font_names: list) -> str:
    """
    Génère le tag <link> complet pour injection dans le <head> HTML.
    """
    url = get_google_fonts_css_url(font_names)
    return f'<link rel="preconnect" href="https://fonts.googleapis.com">\n' \
           f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n' \
           f'<link href="{url}" rel="stylesheet">'


def list_installed_fonts() -> list:
    """Liste toutes les polices installées localement."""
    try:
        result = subprocess.run(
            ['fc-list', '--format=%{family}\n'],
            capture_output=True, text=True
        )
        fonts = sorted(set(
            line.strip().split(',')[0]
            for line in result.stdout.strip().split('\n')
            if line.strip()
        ))
        return fonts
    except Exception as e:
        print(f"Erreur listing polices: {e}", file=sys.stderr)
        return []


def check_font_available(font_name: str) -> bool:
    """Vérifie si une police est disponible localement."""
    installed = list_installed_fonts()
    return any(font_name.lower() in f.lower() for f in installed)


def download_font(font_name: str, output_dir: str) -> bool:
    """
    Télécharge une police Google Fonts dans le dossier spécifié.
    
    Note: Dans le contexte Playwright, les polices sont chargées via CSS.
    Ce téléchargement est pour usage Pillow/ReportLab si nécessaire.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if font_name not in FONT_URLS:
        print(f"⚠ Police '{font_name}' non trouvée dans le catalogue", file=sys.stderr)
        return False
    
    url = FONT_URLS[font_name]
    zip_path = os.path.join(output_dir, f"{font_name.replace(' ', '_')}.zip")
    
    try:
        subprocess.run(
            ['curl', '-sL', '-o', zip_path, url],
            check=True, capture_output=True
        )
        
        # Extraire le ZIP
        font_dir = os.path.join(output_dir, font_name.replace(' ', '_'))
        os.makedirs(font_dir, exist_ok=True)
        subprocess.run(
            ['unzip', '-o', '-q', zip_path, '-d', font_dir],
            check=True, capture_output=True
        )
        
        # Nettoyer le ZIP
        os.remove(zip_path)
        
        print(f"✅ Police téléchargée: {font_name} → {font_dir}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur téléchargement {font_name}: {e}", file=sys.stderr)
        return False


def find_font_file(font_name: str, search_dirs: list = None) -> str:
    """
    Trouve le fichier .ttf/.otf d'une police.
    Cherche dans les répertoires locaux et système.
    """
    if search_dirs is None:
        search_dirs = [
            '/usr/share/fonts',
            '/home/claude/flyer-creator/assets/fonts',
            os.path.expanduser('~/.local/share/fonts'),
        ]
    
    font_name_lower = font_name.lower().replace(' ', '')
    
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        for root, dirs, files in os.walk(search_dir):
            for f in files:
                if f.lower().endswith(('.ttf', '.otf')):
                    fname = f.lower().replace(' ', '').replace('-', '')
                    if font_name_lower in fname:
                        return os.path.join(root, f)
    
    return None


def get_font_for_pillow(font_name: str, size: int = 40, bold: bool = False):
    """
    Retourne un objet ImageFont pour Pillow.
    Télécharge la police si nécessaire.
    """
    from PIL import ImageFont
    
    # Chercher le fichier localement
    suffix = "Bold" if bold else "Regular"
    font_file = find_font_file(f"{font_name}-{suffix}")
    if not font_file:
        font_file = find_font_file(font_name)
    
    if font_file:
        return ImageFont.truetype(font_file, size=size)
    
    # Fallback sur les polices système
    fallbacks = [
        '/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf',
        '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    
    target = fallbacks[1] if bold else fallbacks[0]
    if os.path.exists(target):
        return ImageFont.truetype(target, size=size)
    
    for fb in fallbacks:
        if os.path.exists(fb):
            return ImageFont.truetype(fb, size=size)
    
    return ImageFont.load_default()


def main():
    parser = argparse.ArgumentParser(description="Font Manager pour Flyer Creator")
    parser.add_argument('--fonts', help='Noms des polices séparés par des virgules')
    parser.add_argument('--output', default='./assets/fonts/', help='Dossier de sortie')
    parser.add_argument('--list', action='store_true', help='Lister les polices installées')
    parser.add_argument('--check', help='Vérifier si une police est disponible')
    parser.add_argument('--css-url', help='Générer l\'URL CSS Google Fonts')
    
    args = parser.parse_args()
    
    if args.list:
        fonts = list_installed_fonts()
        print(f"\n📋 {len(fonts)} polices installées:\n")
        for f in fonts:
            print(f"  • {f}")
    
    elif args.check:
        available = check_font_available(args.check)
        print(f"{'✅' if available else '❌'} {args.check}: {'disponible' if available else 'non trouvée'}")
    
    elif args.css_url:
        font_list = [f.strip() for f in args.css_url.split(',')]
        url = get_google_fonts_css_url(font_list)
        print(f"\n🔗 URL Google Fonts CSS:\n{url}")
        print(f"\n📝 Tag HTML:\n{get_google_fonts_link_tag(font_list)}")
    
    elif args.fonts:
        font_list = [f.strip() for f in args.fonts.split(',')]
        for font in font_list:
            download_font(font, args.output)


if __name__ == '__main__':
    main()
