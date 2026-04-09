#!/usr/bin/env python3
"""
gemini_generate.py — Wrapper Gemini API pour generation d'images (Nano Banana 2)

Utilise l'API Gemini avec responseModalities IMAGE pour generer des images.
Supporte Gemini 2.0 Flash (image gen experimental) et futur Gemini 3.1 Flash Image.

Usage:
    python gemini_generate.py \
        --prompt "A photorealistic cat on the Moon" \
        --model "gemini-2.0-flash-exp" \
        --size "1024x1024" \
        --variants 2 \
        --output "C:/tmp/image-generator/session/"
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

# Modeles supportes pour la generation d'images
MODELS = {
    "gemini-flash": "gemini-2.5-flash-image",
    "gemini-flash-image": "gemini-2.5-flash-image",
    "nano-banana-2": "gemini-3.1-flash-image-preview",
    "gemini-3-pro": "gemini-3-pro-image-preview",
    "imagen-4": "imagen-4.0-generate-001",
    "imagen-4-fast": "imagen-4.0-fast-generate-001",
    "imagen-4-ultra": "imagen-4.0-ultra-generate-001",
    "default": "gemini-2.5-flash-image",
}

# Resolutions supportees
ASPECT_RATIOS = {
    "1:1": (1024, 1024),
    "16:9": (1344, 768),
    "9:16": (768, 1344),
    "4:3": (1152, 896),
    "3:4": (896, 1152),
    "3:2": (1216, 832),
    "2:3": (832, 1216),
}


def load_gemini_key():
    """Charge la cle Gemini depuis ai_config.json ou api_keys.json."""
    for config_path in [AI_CONFIG, API_KEYS]:
        if config_path.exists():
            try:
                data = json.loads(config_path.read_text(encoding="utf-8"))
                if "providers" in data:
                    for provider in data["providers"]:
                        name = provider.get("name", "").lower()
                        if name in ("gemini", "google", "google_ai"):
                            return provider.get("api_key")
                for key in ("gemini", "Gemini", "google_ai", "GEMINI_API_KEY"):
                    if key in data:
                        val = data[key]
                        if isinstance(val, dict):
                            return val.get("api_key")
                        elif isinstance(val, str):
                            return val
            except (json.JSONDecodeError, KeyError):
                continue
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")


def generate_image(prompt, api_key, model="gemini-2.0-flash-exp", aspect_ratio="1:1"):
    """Genere une image via l'API Gemini generateContent avec responseModalities IMAGE."""
    import urllib.request
    import urllib.error

    # Resoudre le modele
    resolved_model = MODELS.get(model, model)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{resolved_model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "temperature": 1.0,
        },
    }

    headers = {
        "Content-Type": "application/json",
    }

    json_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")

    start_time = time.time()
    max_retries = 3

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                data = json.loads(response.read().decode("utf-8"))
                elapsed = int((time.time() - start_time) * 1000)

                # Extraire l'image de la reponse
                candidates = data.get("candidates", [])
                if not candidates:
                    raise RuntimeError(f"Pas de candidats dans la reponse: {json.dumps(data)[:500]}")

                parts = candidates[0].get("content", {}).get("parts", [])
                image_data = None
                text_response = None

                for part in parts:
                    if "inlineData" in part:
                        mime_type = part["inlineData"].get("mimeType", "image/png")
                        b64_data = part["inlineData"]["data"]
                        image_data = base64.b64decode(b64_data)
                    elif "text" in part:
                        text_response = part["text"]

                if image_data:
                    return image_data, elapsed, text_response

                # Pas d'image — le modele a peut-etre refuse
                if text_response:
                    raise RuntimeError(f"Gemini n'a pas genere d'image. Reponse texte: {text_response[:500]}")
                raise RuntimeError(f"Reponse sans image ni texte: {json.dumps(data)[:500]}")

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                error_json = json.loads(body)
                error_msg = error_json.get("error", {}).get("message", body[:500])
            except json.JSONDecodeError:
                error_msg = body[:500]

            if e.code == 429:
                wait = 15 * (attempt + 1)
                print(f"[Gemini] Rate limit (429), attente {wait}s... (tentative {attempt+1}/{max_retries})", file=sys.stderr)
                time.sleep(wait)
                continue
            elif e.code == 503:
                print(f"[Gemini] Service indisponible (503), retry {attempt+1}/{max_retries}...", file=sys.stderr)
                time.sleep(10)
                continue
            elif e.code == 400:
                raise RuntimeError(f"Requete invalide (prompt rejete?): {error_msg}")
            elif e.code == 403:
                raise RuntimeError(f"Acces refuse — verifier la cle API et les permissions image gen: {error_msg}")
            else:
                raise RuntimeError(f"Erreur HTTP {e.code}: {error_msg}")

        except urllib.error.URLError as e:
            raise RuntimeError(f"Erreur connexion Gemini: {e.reason}")

    raise RuntimeError(f"Echec apres {max_retries} tentatives")


def main():
    parser = argparse.ArgumentParser(description="Generate images via Gemini API (Nano Banana 2)")
    parser.add_argument("--prompt", required=True, help="Prompt de generation")
    parser.add_argument("--model", default="default", help="Modele (gemini-flash, nano-banana-2, ou ID complet)")
    parser.add_argument("--size", default="1024x1024", help="Taille (1024x1024, ou ratio 16:9)")
    parser.add_argument("--variants", type=int, default=1, help="Nombre de variantes")
    parser.add_argument("--output", required=True, help="Dossier de sortie")
    parser.add_argument("--prefix", default="gemini", help="Prefixe des fichiers")

    args = parser.parse_args()

    # Charger la cle
    api_key = load_gemini_key()
    if not api_key:
        print("ERREUR: Cle Gemini non trouvee dans ai_config.json, api_keys.json ou $GEMINI_API_KEY", file=sys.stderr)
        sys.exit(1)

    # Determiner le ratio
    aspect_ratio = "1:1"
    if "x" in args.size:
        w, h = args.size.split("x")
        # Trouver le ratio le plus proche
        target_ratio = int(w) / int(h)
        best_match = min(ASPECT_RATIOS.keys(), key=lambda r: abs(ASPECT_RATIOS[r][0]/ASPECT_RATIOS[r][1] - target_ratio))
        aspect_ratio = best_match
    elif ":" in args.size:
        aspect_ratio = args.size

    # Creer le dossier
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generer les variantes
    results = []
    for i in range(args.variants):
        print(f"[Gemini] Generation variante {i+1}/{args.variants} via {args.model}...", file=sys.stderr)

        try:
            image_data, elapsed_ms, text_response = generate_image(
                prompt=args.prompt,
                api_key=api_key,
                model=args.model,
                aspect_ratio=aspect_ratio,
            )

            filename = f"{args.prefix}_v{i+1}.png"
            filepath = output_dir / filename
            filepath.write_bytes(image_data)

            result = {
                "file": filename,
                "path": str(filepath),
                "provider": "gemini",
                "model": MODELS.get(args.model, args.model),
                "text_response": text_response,
                "time_ms": elapsed_ms,
                "status": "success",
                "size_bytes": len(image_data),
            }
            results.append(result)
            print(f"[Gemini] Variante {i+1} sauvegardee: {filepath} ({len(image_data)} bytes, {elapsed_ms}ms)", file=sys.stderr)

        except Exception as e:
            result = {
                "file": None,
                "provider": "gemini",
                "model": MODELS.get(args.model, args.model),
                "status": "error",
                "error": str(e),
            }
            results.append(result)
            print(f"[Gemini] ERREUR variante {i+1}: {e}", file=sys.stderr)

    # Metadata
    metadata = {
        "provider": "gemini",
        "model": MODELS.get(args.model, args.model),
        "prompt": args.prompt,
        "params": {
            "aspect_ratio": aspect_ratio,
        },
        "variants": results,
        "timestamp": datetime.now().isoformat(),
    }

    meta_path = output_dir / f"{args.prefix}_metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
