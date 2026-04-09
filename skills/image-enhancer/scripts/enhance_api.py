#!/usr/bin/env python3
"""
enhance_api.py — Enhancement via HuggingFace Spaces API (Pipeline E)

Fallback quand les deps locales (realesrgan, gfpgan, torch) ne sont pas installees.
Utilise les HF Spaces via l'API Inference pour upscale/restauration.

Usage:
    python enhance_api.py --input image.jpg --output image_enhanced.png --pipeline auto
    python enhance_api.py --input photo.jpg --output photo_enhanced.png --face_restore true
"""

import argparse
import base64
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

AI_CONFIG = Path.home() / ".claude" / "tools" / "ai_config.json"
API_KEYS = Path.home() / ".claude" / "tools" / "api_keys.json"

# HuggingFace Spaces pour enhancement
SPACES = {
    "supir": "Fabrice-TIERCELIN/SUPIR",
    "codeformer": "sczhou/CodeFormer",
    "gfpgan": "hysts/GFPGAN",
    "aura_sr": "finegrain/finegrain-image-enhancer",
}


def load_hf_token():
    """Charge le token HuggingFace."""
    for config_path in [AI_CONFIG, API_KEYS]:
        if config_path.exists():
            try:
                data = json.loads(config_path.read_text(encoding="utf-8"))
                if "providers" in data:
                    for provider in data["providers"]:
                        if provider.get("name", "").lower() in ("huggingface", "hf"):
                            return provider.get("api_key")
                if "huggingface" in data:
                    return data["huggingface"].get("api_key")
                if "HuggingFace" in data:
                    return data["HuggingFace"].get("api_key")
            except (json.JSONDecodeError, KeyError):
                continue
    return os.environ.get("HF_TOKEN")


def check_local_deps():
    """Verifie si les deps locales sont installees."""
    try:
        import realesrgan
        return True
    except ImportError:
        return False


def detect_faces(image_path):
    """Detecte si l'image contient des visages via Pillow basique."""
    try:
        from PIL import Image
        img = Image.open(image_path)
        # Heuristique simple : si l'image est un portrait (ratio ~3:4 ou ~2:3), presumer visage
        w, h = img.size
        ratio = w / h
        # Les portraits sont typiquement plus hauts que larges
        if 0.5 < ratio < 0.9:
            return True
        # Pour une detection plus precise, il faudrait OpenCV Haar cascade
        # mais on ne l'a pas forcement installe
        return False
    except Exception:
        return False


def get_image_info(image_path):
    """Retourne les infos de l'image."""
    try:
        from PIL import Image
        img = Image.open(image_path)
        w, h = img.size
        return {
            "width": w,
            "height": h,
            "mode": img.mode,
            "format": img.format,
            "size_bytes": os.path.getsize(image_path),
            "megapixels": round(w * h / 1e6, 2),
        }
    except Exception as e:
        return {"error": str(e)}


def enhance_via_api(image_path, space_id, hf_token, params=None):
    """Envoie l'image a un HF Space pour enhancement."""
    import urllib.request
    import urllib.error

    # Lire l'image en base64
    with open(image_path, "rb") as f:
        image_data = f.read()

    image_b64 = base64.b64encode(image_data).decode("utf-8")

    # Determiner le content type
    ext = Path(image_path).suffix.lower()
    mime_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    mime = mime_types.get(ext, "image/png")

    # Appel API Inference
    api_url = f"https://router.huggingface.co/hf-inference/models/{space_id}"

    # Pour les modeles image-to-image, envoyer les bytes directement
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Accept": "image/png",
    }

    req = urllib.request.Request(api_url, data=image_data, headers=headers, method="POST")
    headers_content = {"Content-Type": mime}
    for k, v in headers_content.items():
        req.add_header(k, v)

    start_time = time.time()
    max_retries = 3

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                content_type = response.headers.get("Content-Type", "")
                data = response.read()
                elapsed = int((time.time() - start_time) * 1000)

                if "image" in content_type:
                    return data, elapsed

                # Reponse JSON (erreur ou base64)
                try:
                    json_resp = json.loads(data.decode("utf-8"))
                    if "error" in json_resp:
                        error_msg = json_resp["error"]
                        if "loading" in str(error_msg).lower():
                            wait = json_resp.get("estimated_time", 30)
                            print(f"[ENHANCE-API] Modele en chargement, attente {wait:.0f}s...", file=sys.stderr)
                            time.sleep(min(wait, 60))
                            continue
                        raise RuntimeError(f"Erreur HF: {error_msg}")
                except json.JSONDecodeError:
                    # Peut etre des bytes image sans bon Content-Type
                    if len(data) > 1000:
                        return data, elapsed
                    raise RuntimeError(f"Reponse inattendue ({len(data)} bytes)")

        except urllib.error.HTTPError as e:
            if e.code in (503, 429):
                print(f"[ENHANCE-API] HTTP {e.code}, retry {attempt+1}/{max_retries}...", file=sys.stderr)
                time.sleep(15)
                continue
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {body[:500]}")

    raise RuntimeError(f"Echec apres {max_retries} tentatives")


def main():
    parser = argparse.ArgumentParser(description="Image Enhancement via HuggingFace Spaces API")
    parser.add_argument("--input", required=True, help="Image source")
    parser.add_argument("--output", default=None, help="Image de sortie (defaut: input_enhanced.png)")
    parser.add_argument("--pipeline", default="auto", choices=["auto", "supir", "codeformer", "gfpgan", "aura_sr"],
                       help="Pipeline a utiliser")
    parser.add_argument("--face_restore", default="auto", choices=["auto", "true", "false"],
                       help="Restauration faciale")
    parser.add_argument("--force_api", action="store_true", help="Forcer l'utilisation de l'API meme si deps locales presentes")

    args = parser.parse_args()

    # Verifier le fichier source
    if not os.path.exists(args.input):
        print(f"ERREUR: Fichier introuvable: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Determiner le fichier de sortie
    if args.output is None:
        input_path = Path(args.input)
        args.output = str(input_path.parent / f"{input_path.stem}_enhanced.png")

    # Verifier si les deps locales sont disponibles
    has_local = check_local_deps()
    if has_local and not args.force_api:
        print("[ENHANCE-API] Deps locales detectees. Utilisez enhance.py pour le pipeline local.", file=sys.stderr)
        print("[ENHANCE-API] Ajoutez --force_api pour forcer l'API.", file=sys.stderr)
        # On continue quand meme via API si explicitement demande
        if args.pipeline != "auto":
            pass
        else:
            sys.exit(0)

    # Charger le token HF
    hf_token = load_hf_token()
    if not hf_token:
        print("ERREUR: Token HuggingFace non trouve", file=sys.stderr)
        sys.exit(1)

    # Analyser l'image
    info = get_image_info(args.input)
    print(f"[ENHANCE-API] Image: {info.get('width', '?')}x{info.get('height', '?')}, {info.get('megapixels', '?')} MP", file=sys.stderr)

    # Detecter les visages
    has_faces = detect_faces(args.input)
    if args.face_restore == "true":
        has_faces = True
    elif args.face_restore == "false":
        has_faces = False

    # Selectionner le pipeline
    pipeline = args.pipeline
    if pipeline == "auto":
        if has_faces:
            pipeline = "codeformer"
            print("[ENHANCE-API] Visages detectes → Pipeline CodeFormer", file=sys.stderr)
        elif info.get("megapixels", 0) < 1:
            pipeline = "supir"
            print("[ENHANCE-API] Basse resolution → Pipeline SUPIR", file=sys.stderr)
        else:
            pipeline = "aura_sr"
            print("[ENHANCE-API] General → Pipeline Aura SR (rapide)", file=sys.stderr)

    space_id = SPACES.get(pipeline)
    if not space_id:
        print(f"ERREUR: Pipeline inconnu: {pipeline}", file=sys.stderr)
        sys.exit(1)

    print(f"[ENHANCE-API] Utilisation de {space_id}...", file=sys.stderr)

    try:
        enhanced_data, elapsed_ms = enhance_via_api(args.input, space_id, hf_token)

        # Sauvegarder
        Path(args.output).write_bytes(enhanced_data)
        print(f"[ENHANCE-API] Sauvegarde: {args.output} ({len(enhanced_data)} bytes, {elapsed_ms}ms)", file=sys.stderr)

        # Rapport
        result = {
            "input": args.input,
            "output": args.output,
            "pipeline": pipeline,
            "space": space_id,
            "method": "api",
            "input_info": info,
            "output_size_bytes": len(enhanced_data),
            "time_ms": elapsed_ms,
            "face_restore": has_faces,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"[ENHANCE-API] ERREUR: {e}", file=sys.stderr)
        result = {
            "input": args.input,
            "pipeline": pipeline,
            "status": "error",
            "error": str(e),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
