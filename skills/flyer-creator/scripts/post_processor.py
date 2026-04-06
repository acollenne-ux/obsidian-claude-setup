#!/usr/bin/env python3
"""
Post Processor — Compositing d'images et ajustements finaux pour les flyers.

Fonctionnalités :
- Ajout de photos de personnes avec masque circulaire
- Compositing de QR codes sur le flyer
- Ajout de logos sponsors
- Ajustements luminosité/contraste/netteté
- Export final en différents formats

Usage:
    python3 post_processor.py --flyer flyer.png --add-person photo.jpg 100 200 150
    python3 post_processor.py --flyer flyer.png --add-qr qr.png 2200 3200
    python3 post_processor.py --flyer flyer.png --sharpen 1.3 --contrast 1.1
"""

import argparse
import os
import sys
from pathlib import Path


def make_circular_photo(
    image_path: str,
    size: int = 150,
    border_width: int = 3,
    border_color: tuple = (255, 255, 255, 255),
    shadow: bool = True,
    shadow_offset: int = 4,
    shadow_blur: int = 10,
    shadow_color: tuple = (0, 0, 0, 80)
) -> 'Image':
    """
    Crée une photo circulaire avec bordure et ombre portée.
    
    Returns: Image PIL en RGBA
    """
    from PIL import Image, ImageDraw, ImageFilter
    
    # Ouvrir et redimensionner
    img = Image.open(image_path).convert('RGBA')
    img = img.resize((size, size), Image.LANCZOS)
    
    # Créer le masque circulaire
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, size, size), fill=255)
    
    # Appliquer le masque
    circular = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    circular.paste(img, (0, 0), mask)
    
    # Taille finale avec bordure et ombre
    total_size = size + (border_width * 2) + (shadow_offset * 2 if shadow else 0) + (shadow_blur if shadow else 0)
    result = Image.new('RGBA', (total_size, total_size), (0, 0, 0, 0))
    
    offset_x = border_width + (shadow_blur // 2 if shadow else 0)
    offset_y = border_width + (shadow_blur // 2 if shadow else 0)
    
    # Dessiner l'ombre
    if shadow:
        shadow_layer = Image.new('RGBA', (total_size, total_size), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        sx = offset_x + shadow_offset
        sy = offset_y + shadow_offset
        shadow_draw.ellipse(
            (sx - border_width, sy - border_width,
             sx + size + border_width, sy + size + border_width),
            fill=shadow_color
        )
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
        result = Image.alpha_composite(result, shadow_layer)
    
    # Dessiner la bordure
    border_draw = ImageDraw.Draw(result)
    border_draw.ellipse(
        (offset_x - border_width, offset_y - border_width,
         offset_x + size + border_width, offset_y + size + border_width),
        fill=border_color
    )
    
    # Coller la photo circulaire
    result.paste(circular, (offset_x, offset_y), circular)
    
    return result


def add_photo_to_flyer(
    flyer_path: str,
    photo_path: str,
    x: int,
    y: int,
    size: int = 150,
    output_path: str = None,
    border_color: tuple = (255, 255, 255, 255),
    name: str = None,
    name_font_size: int = 14
) -> str:
    """
    Ajoute une photo de personne (circulaire) sur le flyer.
    """
    from PIL import Image, ImageDraw, ImageFont
    
    if output_path is None:
        output_path = flyer_path
    
    flyer = Image.open(flyer_path).convert('RGBA')
    circular = make_circular_photo(photo_path, size, border_color=border_color)
    
    # Coller la photo
    flyer.paste(circular, (x, y), circular)
    
    # Ajouter le nom si fourni
    if name:
        draw = ImageDraw.Draw(flyer)
        try:
            font = ImageFont.truetype(
                '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf',
                size=name_font_size
            )
        except Exception:
            font = ImageFont.load_default()
        
        # Centrer le texte sous la photo
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = x + (circular.width - text_width) // 2
        text_y = y + circular.height + 8
        
        # Ombre du texte
        draw.text((text_x + 1, text_y + 1), name, fill=(0, 0, 0, 128), font=font)
        draw.text((text_x, text_y), name, fill=(255, 255, 255, 255), font=font)
    
    flyer = flyer.convert('RGB')
    flyer.save(output_path, quality=95)
    print(f"✅ Photo ajoutée à ({x}, {y}): {output_path}")
    return output_path


def add_qr_to_flyer(
    flyer_path: str,
    qr_path: str,
    x: int,
    y: int,
    output_path: str = None
) -> str:
    """Ajoute un QR code sur le flyer."""
    from PIL import Image
    
    if output_path is None:
        output_path = flyer_path
    
    flyer = Image.open(flyer_path).convert('RGBA')
    qr = Image.open(qr_path).convert('RGBA')
    
    flyer.paste(qr, (x, y), qr)
    
    flyer = flyer.convert('RGB')
    flyer.save(output_path, quality=95)
    print(f"✅ QR code ajouté à ({x}, {y}): {output_path}")
    return output_path


def add_sponsor_banner(
    flyer_path: str,
    logo_paths: list,
    y_position: int = None,
    banner_height: int = 80,
    banner_bg: tuple = (255, 255, 255, 230),
    logo_height: int = 40,
    padding: int = 20,
    output_path: str = None
) -> str:
    """
    Ajoute un bandeau de logos sponsors en bas du flyer.
    """
    from PIL import Image, ImageDraw
    
    if output_path is None:
        output_path = flyer_path
    
    flyer = Image.open(flyer_path).convert('RGBA')
    
    if y_position is None:
        y_position = flyer.height - banner_height - 20
    
    # Dessiner le bandeau
    banner = Image.new('RGBA', (flyer.width, banner_height), banner_bg)
    
    # Charger et redimensionner les logos
    logos = []
    for path in logo_paths:
        if os.path.exists(path):
            logo = Image.open(path).convert('RGBA')
            ratio = logo_height / logo.height
            new_width = int(logo.width * ratio)
            logo = logo.resize((new_width, logo_height), Image.LANCZOS)
            logos.append(logo)
    
    if logos:
        # Calculer l'espacement
        total_logos_width = sum(l.width for l in logos)
        available_width = flyer.width - (2 * padding)
        gap = (available_width - total_logos_width) // (len(logos) + 1) if len(logos) > 0 else 0
        gap = max(gap, 15)  # Minimum 15px de gap
        
        # Placer les logos centrés dans le bandeau
        total_used = total_logos_width + gap * (len(logos) - 1)
        start_x = (flyer.width - total_used) // 2
        current_x = start_x
        
        for logo in logos:
            logo_y = (banner_height - logo.height) // 2
            banner.paste(logo, (current_x, logo_y), logo)
            current_x += logo.width + gap
    
    # Coller le bandeau sur le flyer
    flyer.paste(banner, (0, y_position), banner)
    
    flyer = flyer.convert('RGB')
    flyer.save(output_path, quality=95)
    print(f"✅ Bandeau sponsors ajouté ({len(logos)} logos): {output_path}")
    return output_path


def adjust_image(
    image_path: str,
    output_path: str = None,
    brightness: float = None,
    contrast: float = None,
    sharpness: float = None,
    saturation: float = None
) -> str:
    """
    Ajuste les propriétés d'une image.
    
    Valeurs : 1.0 = original, <1.0 = diminuer, >1.0 = augmenter
    """
    from PIL import Image, ImageEnhance
    
    if output_path is None:
        output_path = image_path
    
    img = Image.open(image_path)
    
    if brightness is not None:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    if contrast is not None:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if sharpness is not None:
        img = ImageEnhance.Sharpness(img).enhance(sharpness)
    if saturation is not None:
        img = ImageEnhance.Color(img).enhance(saturation)
    
    img.save(output_path, quality=95)
    
    adjustments = []
    if brightness: adjustments.append(f"brightness={brightness}")
    if contrast: adjustments.append(f"contrast={contrast}")
    if sharpness: adjustments.append(f"sharpness={sharpness}")
    if saturation: adjustments.append(f"saturation={saturation}")
    
    print(f"✅ Ajustements appliqués ({', '.join(adjustments)}): {output_path}")
    return output_path


def convert_to_pdf(image_path: str, output_path: str = None) -> str:
    """Convertit un PNG en PDF A4."""
    from PIL import Image
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    
    if output_path is None:
        output_path = image_path.replace('.png', '.pdf').replace('.jpg', '.pdf')
    
    img = Image.open(image_path)
    
    # Dimensions A4 en points (72 DPI)
    a4_width, a4_height = A4
    
    c = canvas.Canvas(output_path, pagesize=A4)
    c.drawImage(image_path, 0, 0, width=a4_width, height=a4_height,
                preserveAspectRatio=True, anchor='c')
    c.save()
    
    print(f"✅ PDF généré: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Post Processor pour Flyer Creator")
    parser.add_argument('--flyer', required=True, help='Chemin du flyer PNG')
    parser.add_argument('--output', help='Chemin de sortie (défaut: modifie le flyer)')
    
    # Ajout d'éléments
    parser.add_argument('--add-person', nargs=4, metavar=('PHOTO', 'X', 'Y', 'SIZE'),
                       help='Ajouter une photo circulaire')
    parser.add_argument('--person-name', help='Nom sous la photo')
    parser.add_argument('--add-qr', nargs=3, metavar=('QR', 'X', 'Y'),
                       help='Ajouter un QR code')
    parser.add_argument('--add-sponsors', nargs='+', metavar='LOGO',
                       help='Ajouter des logos sponsors')
    
    # Ajustements
    parser.add_argument('--brightness', type=float, help='Luminosité (1.0=original)')
    parser.add_argument('--contrast', type=float, help='Contraste (1.0=original)')
    parser.add_argument('--sharpness', type=float, help='Netteté (1.0=original)')
    parser.add_argument('--saturation', type=float, help='Saturation (1.0=original)')
    
    # Export
    parser.add_argument('--to-pdf', action='store_true', help='Convertir en PDF')
    
    args = parser.parse_args()
    output = args.output or args.flyer
    
    if args.add_person:
        photo, x, y, size = args.add_person
        add_photo_to_flyer(args.flyer, photo, int(x), int(y), int(size),
                          output, name=args.person_name)
    
    if args.add_qr:
        qr, x, y = args.add_qr
        add_qr_to_flyer(args.flyer, qr, int(x), int(y), output)
    
    if args.add_sponsors:
        add_sponsor_banner(args.flyer, args.add_sponsors, output_path=output)
    
    if any([args.brightness, args.contrast, args.sharpness, args.saturation]):
        adjust_image(args.flyer, output,
                    brightness=args.brightness,
                    contrast=args.contrast,
                    sharpness=args.sharpness,
                    saturation=args.saturation)
    
    if args.to_pdf:
        convert_to_pdf(output)


if __name__ == '__main__':
    main()
