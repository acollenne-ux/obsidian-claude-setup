#!/usr/bin/env python3
"""
QR Generator — Génération de QR codes pour les flyers.

Usage:
    python3 qr_generator.py --data "https://example.com" --output qr.png
    python3 qr_generator.py --data "tel:+33612345678" --output qr.png --size 200
    python3 qr_generator.py --data "BEGIN:VEVENT..." --output qr.png --color "#1a1a2e"
"""

import argparse
import os
import sys


def generate_qr_code(
    data: str,
    output_path: str,
    size: int = 200,
    border: int = 2,
    fg_color: str = "#000000",
    bg_color: str = "#FFFFFF",
    with_quiet_zone: bool = True,
    quiet_zone_px: int = 12
) -> str:
    """
    Génère un QR code en PNG.
    
    Args:
        data: Contenu à encoder (URL, texte, vCard, etc.)
        output_path: Chemin de sortie du PNG
        size: Taille en pixels du QR code final
        border: Nombre de modules de bordure dans le QR
        fg_color: Couleur du QR code (hex)
        bg_color: Couleur de fond du QR code (hex)
        with_quiet_zone: Ajouter une zone blanche autour
        quiet_zone_px: Taille de la quiet zone en pixels
    
    Returns: chemin du fichier généré
    """
    import qrcode
    from PIL import Image
    
    qr = qrcode.QRCode(
        version=None,  # Auto-détection de la version
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Haute correction
        box_size=10,
        border=border,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Convertir les couleurs hex en RGB
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    img = qr.make_image(
        fill_color=hex_to_rgb(fg_color),
        back_color=hex_to_rgb(bg_color)
    ).convert('RGBA')
    
    # Redimensionner
    qr_size = size - (2 * quiet_zone_px if with_quiet_zone else 0)
    img = img.resize((qr_size, qr_size), Image.LANCZOS)
    
    # Ajouter la quiet zone blanche
    if with_quiet_zone:
        final = Image.new('RGBA', (size, size), (255, 255, 255, 255))
        offset = quiet_zone_px
        final.paste(img, (offset, offset))
        img = final
    
    img.save(output_path)
    print(f"✅ QR code généré: {output_path} ({size}x{size}px)")
    return output_path


def generate_vcard_qr(
    name: str,
    phone: str = None,
    email: str = None,
    org: str = None,
    url: str = None,
    output_path: str = "qr_vcard.png",
    size: int = 200
) -> str:
    """Génère un QR code de type vCard (contact)."""
    vcard = "BEGIN:VCARD\nVERSION:3.0\n"
    vcard += f"FN:{name}\n"
    if phone:
        vcard += f"TEL:{phone}\n"
    if email:
        vcard += f"EMAIL:{email}\n"
    if org:
        vcard += f"ORG:{org}\n"
    if url:
        vcard += f"URL:{url}\n"
    vcard += "END:VCARD"
    
    return generate_qr_code(vcard, output_path, size)


def generate_event_qr(
    title: str,
    start: str,
    end: str = None,
    location: str = None,
    description: str = None,
    output_path: str = "qr_event.png",
    size: int = 200
) -> str:
    """
    Génère un QR code d'événement calendrier.
    
    start/end format: "20260615T190000" (YYYYMMDDTHHmmss)
    """
    vevent = "BEGIN:VCALENDAR\nBEGIN:VEVENT\n"
    vevent += f"SUMMARY:{title}\n"
    vevent += f"DTSTART:{start}\n"
    if end:
        vevent += f"DTEND:{end}\n"
    if location:
        vevent += f"LOCATION:{location}\n"
    if description:
        vevent += f"DESCRIPTION:{description}\n"
    vevent += "END:VEVENT\nEND:VCALENDAR"
    
    return generate_qr_code(vevent, output_path, size)


def generate_wifi_qr(
    ssid: str,
    password: str,
    auth_type: str = "WPA",
    output_path: str = "qr_wifi.png",
    size: int = 200
) -> str:
    """Génère un QR code WiFi."""
    wifi_data = f"WIFI:T:{auth_type};S:{ssid};P:{password};;"
    return generate_qr_code(wifi_data, output_path, size)


def main():
    parser = argparse.ArgumentParser(description="QR Generator pour Flyer Creator")
    parser.add_argument('--data', help='Données à encoder (URL, texte, etc.)')
    parser.add_argument('--output', required=True, help='Chemin de sortie PNG')
    parser.add_argument('--size', type=int, default=200, help='Taille en pixels')
    parser.add_argument('--color', default='#000000', help='Couleur du QR (hex)')
    parser.add_argument('--bg', default='#FFFFFF', help='Couleur de fond (hex)')
    parser.add_argument('--type', default='url', choices=['url', 'vcard', 'event', 'wifi'],
                       help='Type de QR code')
    
    # Options vCard
    parser.add_argument('--name', help='Nom (vCard)')
    parser.add_argument('--phone', help='Téléphone (vCard)')
    parser.add_argument('--email', help='Email (vCard)')
    parser.add_argument('--org', help='Organisation (vCard)')
    
    args = parser.parse_args()
    
    if args.type == 'vcard' and args.name:
        generate_vcard_qr(
            name=args.name,
            phone=args.phone,
            email=args.email,
            org=args.org,
            url=args.data,
            output_path=args.output,
            size=args.size
        )
    elif args.data:
        generate_qr_code(
            data=args.data,
            output_path=args.output,
            size=args.size,
            fg_color=args.color,
            bg_color=args.bg
        )
    else:
        print("❌ Veuillez fournir --data ou --name pour un vCard", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
