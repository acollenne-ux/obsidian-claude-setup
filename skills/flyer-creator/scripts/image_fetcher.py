#!/usr/bin/env python3
"""
Image Fetcher — Recherche et téléchargement d'images de fond pour flyers.

Stratégies de récupération d'images :
1. image_search intégré Claude (recommandé — via le skill)
2. Unsplash Source (accès direct sans clé API)
3. Téléchargement direct depuis URL
4. Génération de gradients CSS (fallback sans image)

Usage:
    python3 image_fetcher.py --query "concert stage lights" --output bg.jpg
    python3 image_fetcher.py --url "https://example.com/image.jpg" --output bg.jpg
    python3 image_fetcher.py --gradient "135deg,#667eea,#764ba2" --output bg.png --size 2480x3508
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path


def download_image(url: str, output_path: str, timeout: int = 30) -> bool:
    """Télécharge une image depuis une URL."""
    try:
        result = subprocess.run(
            ['curl', '-sL', '-o', output_path, '--max-time', str(timeout), url],
            capture_output=True, text=True
        )
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"✅ Image téléchargée: {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"❌ Image trop petite ou corrompue", file=sys.stderr)
            if os.path.exists(output_path):
                os.remove(output_path)
            return False
            
    except Exception as e:
        print(f"❌ Erreur téléchargement: {e}", file=sys.stderr)
        return False


def fetch_unsplash(query: str, output_path: str, width: int = 2480, height: int = 3508) -> bool:
    """
    Récupère une image depuis Unsplash Source (sans clé API).
    Note: Ce service peut être instable. Préférer image_search de Claude.
    """
    encoded_query = query.replace(' ', ',')
    url = f"https://source.unsplash.com/{width}x{height}/?{encoded_query}"
    
    print(f"🔍 Recherche Unsplash: '{query}' ({width}x{height})")
    return download_image(url, output_path)


def generate_gradient_image(
    gradient_spec: str,
    output_path: str,
    width: int = 2480,
    height: int = 3508
) -> bool:
    """
    Génère une image de fond gradient via Pillow.
    
    gradient_spec format: "direction,color1,color2[,color3]"
    Ex: "vertical,#1a1a2e,#e94560" ou "diagonal,#667eea,#764ba2"
    """
    from PIL import Image, ImageDraw
    
    parts = [p.strip() for p in gradient_spec.split(',')]
    direction = parts[0] if len(parts) > 2 else "vertical"
    colors = parts[1:] if len(parts) > 2 else parts
    
    if len(colors) < 2:
        colors = ['#1a1a2e', '#e94560']
    
    def hex_to_rgb(hex_color: str) -> tuple:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    color_rgbs = [hex_to_rgb(c) for c in colors]
    
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        if direction in ('vertical', '180deg'):
            ratio = y / height
        elif direction in ('horizontal', '90deg'):
            ratio = 0.5  # Will handle differently
        elif direction in ('diagonal', '135deg'):
            ratio = (y / height * 0.7) + (0.3 * 0.5)
        else:
            ratio = y / height
        
        # Interpoler entre les couleurs
        if len(color_rgbs) == 2:
            r = int(color_rgbs[0][0] + (color_rgbs[1][0] - color_rgbs[0][0]) * ratio)
            g = int(color_rgbs[0][1] + (color_rgbs[1][1] - color_rgbs[0][1]) * ratio)
            b = int(color_rgbs[0][2] + (color_rgbs[1][2] - color_rgbs[0][2]) * ratio)
        else:
            # 3 couleurs : interpolation en 2 segments
            if ratio < 0.5:
                sub_ratio = ratio * 2
                r = int(color_rgbs[0][0] + (color_rgbs[1][0] - color_rgbs[0][0]) * sub_ratio)
                g = int(color_rgbs[0][1] + (color_rgbs[1][1] - color_rgbs[0][1]) * sub_ratio)
                b = int(color_rgbs[0][2] + (color_rgbs[1][2] - color_rgbs[0][2]) * sub_ratio)
            else:
                sub_ratio = (ratio - 0.5) * 2
                r = int(color_rgbs[1][0] + (color_rgbs[2][0] - color_rgbs[1][0]) * sub_ratio)
                g = int(color_rgbs[1][1] + (color_rgbs[2][1] - color_rgbs[1][1]) * sub_ratio)
                b = int(color_rgbs[1][2] + (color_rgbs[2][2] - color_rgbs[1][2]) * sub_ratio)
        
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        if direction in ('horizontal', '90deg'):
            for x in range(width):
                x_ratio = x / width
                xr = int(color_rgbs[0][0] + (color_rgbs[1][0] - color_rgbs[0][0]) * x_ratio)
                xg = int(color_rgbs[0][1] + (color_rgbs[1][1] - color_rgbs[0][1]) * x_ratio)
                xb = int(color_rgbs[0][2] + (color_rgbs[1][2] - color_rgbs[0][2]) * x_ratio)
                draw.point((x, y), fill=(xr, xg, xb))
        else:
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    img.save(output_path)
    print(f"✅ Gradient généré: {output_path} ({width}x{height})")
    return True


def darken_image(input_path: str, output_path: str = None, opacity: float = 0.5) -> str:
    """
    Assombrit une image pour améliorer la lisibilité du texte par-dessus.
    
    opacity: 0.0 (image originale) à 1.0 (noir complet)
    Recommandé: 0.4-0.6 pour les flyers
    """
    from PIL import Image, ImageEnhance
    
    if output_path is None:
        output_path = input_path
    
    img = Image.open(input_path).convert('RGBA')
    
    # Créer un overlay noir
    overlay = Image.new('RGBA', img.size, (0, 0, 0, int(255 * opacity)))
    
    # Composer
    darkened = Image.alpha_composite(img, overlay)
    darkened = darkened.convert('RGB')
    darkened.save(output_path)
    
    print(f"✅ Image assombrie (opacité {opacity}): {output_path}")
    return output_path


def blur_image(input_path: str, output_path: str = None, radius: int = 3) -> str:
    """Applique un flou gaussien à une image."""
    from PIL import Image, ImageFilter
    
    if output_path is None:
        output_path = input_path
    
    img = Image.open(input_path)
    blurred = img.filter(ImageFilter.GaussianBlur(radius=radius))
    blurred.save(output_path)
    
    print(f"✅ Image floutée (radius {radius}): {output_path}")
    return output_path


def resize_cover(input_path: str, output_path: str, width: int, height: int) -> str:
    """
    Redimensionne une image en mode 'cover' (remplit tout en gardant les proportions).
    Équivalent CSS object-fit: cover.
    """
    from PIL import Image
    
    img = Image.open(input_path)
    img_ratio = img.width / img.height
    target_ratio = width / height
    
    if img_ratio > target_ratio:
        # Image plus large : crop horizontal
        new_height = height
        new_width = int(height * img_ratio)
    else:
        # Image plus haute : crop vertical
        new_width = width
        new_height = int(width / img_ratio)
    
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Crop centré
    left = (new_width - width) // 2
    top = (new_height - height) // 2
    img = img.crop((left, top, left + width, top + height))
    
    img.save(output_path)
    print(f"✅ Image redimensionnée (cover): {output_path} ({width}x{height})")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Image Fetcher pour Flyer Creator")
    parser.add_argument('--query', help='Termes de recherche pour Unsplash')
    parser.add_argument('--url', help='URL directe de l\'image à télécharger')
    parser.add_argument('--gradient', help='Spec de gradient: direction,color1,color2')
    parser.add_argument('--output', required=True, help='Chemin de sortie')
    parser.add_argument('--size', default='2480x3508', help='Taille WxH (défaut: A4 300DPI)')
    parser.add_argument('--darken', type=float, default=None, help='Assombrir (0.0-1.0)')
    parser.add_argument('--blur', type=int, default=None, help='Flou gaussien (radius)')
    
    args = parser.parse_args()
    
    width, height = [int(x) for x in args.size.split('x')]
    
    success = False
    
    if args.url:
        success = download_image(args.url, args.output)
    elif args.gradient:
        success = generate_gradient_image(args.gradient, args.output, width, height)
    elif args.query:
        success = fetch_unsplash(args.query, args.output, width, height)
    
    if success:
        if args.darken is not None:
            darken_image(args.output, args.output, args.darken)
        if args.blur is not None:
            blur_image(args.output, args.output, args.blur)
    else:
        print("❌ Aucune image générée. Utilisation du fallback gradient.", file=sys.stderr)
        generate_gradient_image("vertical,#1a1a2e,#0d0221", args.output, width, height)


if __name__ == '__main__':
    main()
