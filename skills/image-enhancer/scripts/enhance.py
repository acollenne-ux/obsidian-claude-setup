#!/usr/bin/env python3
"""
Image Enhancer — Script principal de super-résolution et restauration
=====================================================================
Pipeline professionnel combinant Real-ESRGAN, GFPGAN, débruitage et sharpening.
Fallback CPU automatique si le GPU n'est pas disponible.

Usage:
    python enhance.py --input image.jpg --output result.png --pipeline auto --scale 4
"""

import argparse
import os
import sys
import time
import warnings
warnings.filterwarnings("ignore")

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

# ── Configuration ──
MODELS_DIR = "/home/claude/models"
MODEL_URLS = {
    "RealESRGAN_x4plus": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
    "RealESRGAN_x4plus_anime_6B": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth",
    "GFPGANv1.4": "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth",
}


def log(msg, level="INFO"):
    symbols = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERR": "❌", "RUN": "🔄"}
    print(f"  {symbols.get(level, '•')} [{level}] {msg}")


def analyze_image(input_path):
    """Phase 0 : Diagnostic automatique de l'image"""
    img = Image.open(input_path)
    w, h = img.size
    file_size = os.path.getsize(input_path)
    fmt = img.format or os.path.splitext(input_path)[1].upper().replace(".", "")
    mode = img.mode
    megapixels = (w * h) / 1e6

    # Détecter artefacts JPEG
    is_jpeg = fmt.upper() in ("JPEG", "JPG")
    needs_denoise = is_jpeg and file_size < (w * h * 0.5)  # Forte compression

    # Déterminer le pipeline
    if w < 256 and h < 256:
        pipeline = "aggressive"
    elif w < 1024 and h < 1024:
        pipeline = "standard"
    elif w >= 1024 and h >= 1024:
        pipeline = "light"
    else:
        pipeline = "standard"

    info = {
        "width": w, "height": h, "format": fmt, "mode": mode,
        "file_size": file_size, "megapixels": megapixels,
        "is_jpeg": is_jpeg, "needs_denoise": needs_denoise,
        "suggested_pipeline": pipeline
    }

    log(f"Image: {w}x{h} | {fmt} | {mode} | {file_size/1024:.1f} KB | {megapixels:.2f} MP")
    log(f"Pipeline suggéré: {pipeline}")
    if needs_denoise:
        log("Artefacts JPEG détectés → débruitage recommandé", "WARN")

    return info


def download_model(name):
    """Télécharger un modèle s'il n'existe pas"""
    os.makedirs(MODELS_DIR, exist_ok=True)
    path = os.path.join(MODELS_DIR, f"{name}.pth")
    if os.path.exists(path):
        return path
    url = MODEL_URLS.get(name)
    if not url:
        log(f"URL inconnue pour le modèle {name}", "ERR")
        return None
    log(f"Téléchargement du modèle {name}...", "RUN")
    try:
        import urllib.request
        urllib.request.urlretrieve(url, path)
        log(f"Modèle {name} téléchargé ({os.path.getsize(path)/1e6:.1f} MB)", "OK")
        return path
    except Exception as e:
        log(f"Échec téléchargement {name}: {e}", "ERR")
        return None


def denoise_image(img_cv, strength=10):
    """Débruitage OpenCV (fastNlMeansDenoisingColored)"""
    log(f"Débruitage (h={strength})...", "RUN")
    return cv2.fastNlMeansDenoisingColored(img_cv, None, strength, strength, 7, 21)


def sharpen_image(img_pil, amount=1.5):
    """Sharpening via UnsharpMask (PIL)"""
    log(f"Sharpening (amount={amount})...", "RUN")
    return img_pil.filter(ImageFilter.UnsharpMask(radius=1.5, percent=int(amount * 100), threshold=2))


def clahe_contrast(img_cv):
    """Contraste adaptatif CLAHE"""
    log("Amélioration contraste (CLAHE)...", "RUN")
    lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def upscale_realesrgan(img_cv, scale=4, model_name="RealESRGAN_x4plus"):
    """Upscale avec Real-ESRGAN"""
    try:
        from realesrgan import RealESRGANer
        from basicsr.archs.rrdbnet_arch import RRDBNet
        import torch

        model_path = download_model(model_name)
        if not model_path:
            return None

        # Configurer le modèle
        if "anime" in model_name:
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
        else:
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        log(f"Device: {device}", "INFO")

        upsampler = RealESRGANer(
            scale=4,
            model_path=model_path,
            model=model,
            tile=512 if device.type == 'cpu' else 0,
            tile_pad=10,
            pre_pad=0,
            half=False,
            device=device,
        )

        log(f"Upscale x{scale} avec {model_name}...", "RUN")
        output, _ = upsampler.enhance(img_cv, outscale=scale)
        log(f"Upscale terminé: {output.shape[1]}x{output.shape[0]}", "OK")
        return output

    except ImportError as e:
        log(f"Real-ESRGAN non disponible: {e}", "WARN")
        return None
    except Exception as e:
        log(f"Erreur Real-ESRGAN: {e}", "WARN")
        return None


def restore_faces_gfpgan(img_cv):
    """Restauration faciale avec GFPGAN"""
    try:
        from gfpgan import GFPGANer

        model_path = download_model("GFPGANv1.4")
        if not model_path:
            return img_cv

        log("Restauration faciale (GFPGAN v1.4)...", "RUN")
        restorer = GFPGANer(
            model_path=model_path,
            upscale=1,  # Pas d'upscale supplémentaire
            arch='clean',
            channel_multiplier=2,
        )

        _, _, output = restorer.enhance(
            img_cv,
            has_aligned=False,
            only_center_face=False,
            paste_back=True,
        )
        log("Restauration faciale terminée", "OK")
        return output

    except ImportError as e:
        log(f"GFPGAN non disponible: {e}", "WARN")
        return img_cv
    except Exception as e:
        log(f"Erreur GFPGAN: {e}", "WARN")
        return img_cv


def upscale_cpu_fallback(img_cv, scale=4):
    """Fallback CPU : Lanczos + Sharpen + CLAHE"""
    log(f"[FALLBACK CPU] Upscale x{scale} avec Lanczos...", "RUN")
    h, w = img_cv.shape[:2]
    upscaled = cv2.resize(img_cv, (w * scale, h * scale), interpolation=cv2.INTER_LANCZOS4)

    # Sharpen via kernel
    kernel = np.array([[-0.5, -1, -0.5],
                       [-1,   7, -1],
                       [-0.5, -1, -0.5]]) / 2.0
    sharpened = cv2.filter2D(upscaled, -1, kernel)

    # CLAHE
    result = clahe_contrast(sharpened)
    log(f"[FALLBACK CPU] Terminé: {result.shape[1]}x{result.shape[0]}", "OK")
    return result


def detect_faces(img_cv):
    """Détecter si l'image contient des visages"""
    try:
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        cascade_paths = [
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml',
            '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml',
        ]
        for path in cascade_paths:
            if os.path.exists(path):
                detector = cv2.CascadeClassifier(path)
                faces = detector.detectMultiScale(gray, 1.1, 4, minSize=(20, 20))
                count = len(faces)
                if count > 0:
                    log(f"Visages détectés: {count}", "INFO")
                return count > 0
        return False
    except Exception:
        return False


def enhance_image(input_path, output_path, pipeline="auto", scale=4,
                  face_restore="auto", do_sharpen=True, do_denoise="auto",
                  denoise_strength=10, model_type="general"):
    """
    Pipeline principal d'amélioration d'image.
    """
    start_time = time.time()

    print("\n" + "=" * 60)
    print("  IMAGE ENHANCER — Super-Résolution & Restauration")
    print("=" * 60 + "\n")

    # Phase 0 : Diagnostic
    log("Phase 0 : Diagnostic...", "RUN")
    info = analyze_image(input_path)

    # Auto-détection du pipeline
    if pipeline == "auto":
        pipeline = info["suggested_pipeline"]
        log(f"Pipeline auto-sélectionné: {pipeline}")

    # Charger l'image
    img_cv = cv2.imread(input_path)
    if img_cv is None:
        log(f"Impossible de lire l'image: {input_path}", "ERR")
        sys.exit(1)

    # Auto-détection denoise
    if do_denoise == "auto":
        do_denoise = info["needs_denoise"] or pipeline in ("aggressive", "restore")

    # Auto-détection face restore
    has_faces = detect_faces(img_cv)
    if face_restore == "auto":
        face_restore = has_faces

    # ── Exécution du pipeline ──

    # Étape 1 : Débruitage
    if do_denoise:
        strength = denoise_strength if pipeline != "restore" else 15
        img_cv = denoise_image(img_cv, strength=strength)

    # Étape 2 : Upscale (si pipeline != light)
    upscale_method = "none"
    if pipeline in ("aggressive", "standard", "restore"):
        # Choisir le modèle
        if model_type == "anime":
            model_name = "RealESRGAN_x4plus_anime_6B"
        else:
            model_name = "RealESRGAN_x4plus"

        result = upscale_realesrgan(img_cv, scale=scale, model_name=model_name)
        if result is not None:
            img_cv = result
            upscale_method = model_name
        else:
            log("Fallback vers upscale CPU...", "WARN")
            img_cv = upscale_cpu_fallback(img_cv, scale=scale)
            upscale_method = "CPU Lanczos (fallback)"

    # Étape 3 : Restauration faciale
    face_method = "non"
    if face_restore and face_restore != "false":
        img_cv = restore_faces_gfpgan(img_cv)
        face_method = "GFPGAN v1.4"

    # Étape 4 : Contraste adaptatif (pour pipeline restore et light)
    if pipeline in ("restore", "light"):
        img_cv = clahe_contrast(img_cv)

    # Étape 5 : Sharpening
    sharpen_info = "non"
    if do_sharpen:
        img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        if pipeline == "aggressive":
            img_pil = sharpen_image(img_pil, amount=2.0)
            sharpen_info = "fort (amount=200%)"
        elif pipeline == "standard":
            img_pil = sharpen_image(img_pil, amount=1.5)
            sharpen_info = "moyen (amount=150%)"
        else:
            img_pil = sharpen_image(img_pil, amount=1.0)
            sharpen_info = "léger (amount=100%)"
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # ── Sauvegarde ──
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    cv2.imwrite(output_path, img_cv, [cv2.IMWRITE_PNG_COMPRESSION, 3])

    elapsed = time.time() - start_time
    out_h, out_w = img_cv.shape[:2]
    out_size = os.path.getsize(output_path)

    # ── Rapport ──
    pipeline_names = {
        "aggressive": "A — Upscale agressif",
        "standard": "B — Upscale standard",
        "light": "C — Amélioration sans upscale",
        "restore": "D — Restauration photo ancienne",
    }

    print("\n" + "═" * 60)
    print("  RAPPORT D'AMÉLIORATION D'IMAGE")
    print("═" * 60)
    print(f"  Source       : {os.path.basename(input_path)} ({info['width']}x{info['height']}, {info['format']}, {info['file_size']/1024:.1f} KB)")
    print(f"  Résultat     : {os.path.basename(output_path)} ({out_w}x{out_h}, PNG, {out_size/1024:.1f} KB)")
    print(f"  Pipeline     : {pipeline_names.get(pipeline, pipeline)}")
    print(f"  Facteur      : x{scale}" if pipeline != "light" else "  Facteur      : aucun (amélioration seule)")
    print(f"  Modèle       : {upscale_method}")
    print(f"  Face restore : {face_method}")
    print(f"  Denoise      : {'oui (h=' + str(denoise_strength) + ')' if do_denoise else 'non'}")
    print(f"  Sharpening   : {sharpen_info}")
    print(f"  Temps        : {elapsed:.1f} secondes")
    print("═" * 60 + "\n")

    return output_path


# ── CLI ──
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Enhancer — Super-Résolution & Restauration")
    parser.add_argument("--input", "-i", required=True, help="Chemin de l'image source")
    parser.add_argument("--output", "-o", required=True, help="Chemin de sortie (PNG recommandé)")
    parser.add_argument("--pipeline", "-p", default="auto",
                        choices=["auto", "aggressive", "standard", "light", "restore"],
                        help="Pipeline à utiliser (défaut: auto)")
    parser.add_argument("--scale", "-s", type=int, default=4, choices=[2, 4],
                        help="Facteur d'upscale (défaut: 4)")
    parser.add_argument("--face_restore", "-f", default="auto",
                        help="Restauration faciale: true/false/auto (défaut: auto)")
    parser.add_argument("--sharpen", default="true",
                        help="Sharpening: true/false (défaut: true)")
    parser.add_argument("--denoise", default="auto",
                        help="Débruitage: true/false/auto (défaut: auto)")
    parser.add_argument("--denoise_strength", type=int, default=10,
                        help="Force du débruitage: 3-15 (défaut: 10)")
    parser.add_argument("--model", "-m", default="general",
                        choices=["general", "anime"],
                        help="Type de modèle: general/anime (défaut: general)")

    args = parser.parse_args()

    # Parse booleans
    face_val = args.face_restore
    if face_val.lower() == "true":
        face_val = True
    elif face_val.lower() == "false":
        face_val = False

    denoise_val = args.denoise
    if denoise_val.lower() == "true":
        denoise_val = True
    elif denoise_val.lower() == "false":
        denoise_val = False

    enhance_image(
        input_path=args.input,
        output_path=args.output,
        pipeline=args.pipeline,
        scale=args.scale,
        face_restore=face_val,
        do_sharpen=args.sharpen.lower() == "true",
        do_denoise=denoise_val,
        denoise_strength=args.denoise_strength,
        model_type=args.model,
    )
