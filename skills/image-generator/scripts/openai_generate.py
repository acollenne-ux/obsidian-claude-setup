#!/usr/bin/env python3
"""
openai_generate.py — Wrapper OpenAI API pour generation d'images (DALL-E 3 / GPT-Image)

Usage:
    python openai_generate.py \
        --prompt "A professional photograph of a cat" \
        --model "dall-e-3" \
        --size "1024x1024" \
        --quality "hd" \
        --style "natural" \
        --variants 2 \
        --output "C:/tmp/image-generator/session/"
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

AI_CONFIG = Path.home() / ".claude" / "tools" / "ai_config.json"
API_KEYS = Path.home() / ".claude" / "tools" / "api_keys.json"

VALID_SIZES_DALLE3 = ["1024x1024", "1024x1792", "1792x1024"]
VALID_QUALITIES = ["standard", "hd"]
VALID_STYLES = ["natural", "vivid"]


def load_openai_key():
    """Charge la cle OpenAI depuis ai_config.json ou api_keys.json."""
    for config_path in [AI_CONFIG, API_KEYS]:
        if config_path.exists():
            try:
                data = json.loads(config_path.read_text(encoding="utf-8"))
                if "providers" in data:
                    for provider in data["providers"]:
                        if provider.get("name", "").lower() == "openai":
                            return provider.get("api_key")
                if "openai" in data:
                    return data["openai"].get("api_key")
                if "OpenAI" in data:
                    return data["OpenAI"].get("api_key")
            except (json.JSONDecodeError, KeyError):
                continue
    return os.environ.get("OPENAI_API_KEY")


def generate_image(prompt, api_key, model="dall-e-3", size="1024x1024",
                   quality="hd", style="natural", response_format="b64_json"):
    """Genere une image via l'API OpenAI Images."""
    url = "https://api.openai.com/v1/images/generations"

    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": response_format,
    }

    if model == "dall-e-3":
        payload["quality"] = quality
        payload["style"] = style

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    json_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")

    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
            elapsed = int((time.time() - start_time) * 1000)

            if "data" not in data or not data["data"]:
                raise RuntimeError(f"Reponse vide: {json.dumps(data)[:500]}")

            result = data["data"][0]
            revised_prompt = result.get("revised_prompt", prompt)

            if response_format == "b64_json":
                image_data = base64.b64decode(result["b64_json"])
            else:
                # URL - telecharger l'image
                img_url = result["url"]
                img_req = urllib.request.Request(img_url)
                with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                    image_data = img_resp.read()

            return image_data, elapsed, revised_prompt

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            error_json = json.loads(body)
            error_msg = error_json.get("error", {}).get("message", body[:500])
        except json.JSONDecodeError:
            error_msg = body[:500]

        if e.code == 429:
            raise RuntimeError(f"Rate limit OpenAI atteint. Attendre avant de reessayer. Detail: {error_msg}")
        elif e.code == 400:
            raise RuntimeError(f"Requete invalide (prompt rejete ou parametre incorrect): {error_msg}")
        elif e.code == 401:
            raise RuntimeError("Cle API OpenAI invalide ou expiree")
        else:
            raise RuntimeError(f"Erreur HTTP {e.code}: {error_msg}")

    except urllib.error.URLError as e:
        raise RuntimeError(f"Erreur connexion OpenAI: {e.reason}")


def main():
    parser = argparse.ArgumentParser(description="Generate images via OpenAI API (DALL-E 3 / GPT-Image)")
    parser.add_argument("--prompt", required=True, help="Prompt de generation")
    parser.add_argument("--model", default="dall-e-3", help="Modele (dall-e-3, gpt-image-1)")
    parser.add_argument("--size", default="1024x1024", choices=VALID_SIZES_DALLE3, help="Taille de l'image")
    parser.add_argument("--quality", default="hd", choices=VALID_QUALITIES, help="Qualite (standard, hd)")
    parser.add_argument("--style", default="natural", choices=VALID_STYLES, help="Style (natural, vivid)")
    parser.add_argument("--variants", type=int, default=1, help="Nombre de variantes")
    parser.add_argument("--output", required=True, help="Dossier de sortie")
    parser.add_argument("--prefix", default="openai", help="Prefixe des fichiers")

    args = parser.parse_args()

    # Charger la cle
    api_key = load_openai_key()
    if not api_key:
        print("ERREUR: Cle OpenAI non trouvee dans ai_config.json, api_keys.json ou $OPENAI_API_KEY", file=sys.stderr)
        sys.exit(1)

    # Creer le dossier de sortie
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generer les variantes
    results = []
    for i in range(args.variants):
        print(f"[OpenAI] Generation variante {i+1}/{args.variants} via {args.model}...", file=sys.stderr)

        try:
            image_data, elapsed_ms, revised_prompt = generate_image(
                prompt=args.prompt,
                api_key=api_key,
                model=args.model,
                size=args.size,
                quality=args.quality,
                style=args.style,
            )

            filename = f"{args.prefix}_v{i+1}.png"
            filepath = output_dir / filename
            filepath.write_bytes(image_data)

            result = {
                "file": filename,
                "path": str(filepath),
                "provider": "openai",
                "model": args.model,
                "revised_prompt": revised_prompt,
                "time_ms": elapsed_ms,
                "status": "success",
                "size_bytes": len(image_data),
            }
            results.append(result)
            print(f"[OpenAI] Variante {i+1} sauvegardee: {filepath} ({len(image_data)} bytes, {elapsed_ms}ms)", file=sys.stderr)
            if revised_prompt != args.prompt:
                print(f"[OpenAI] Prompt revise par OpenAI: {revised_prompt[:200]}...", file=sys.stderr)

        except Exception as e:
            result = {
                "file": None,
                "provider": "openai",
                "model": args.model,
                "status": "error",
                "error": str(e),
            }
            results.append(result)
            print(f"[OpenAI] ERREUR variante {i+1}: {e}", file=sys.stderr)

    # Metadata
    metadata = {
        "provider": "openai",
        "model": args.model,
        "prompt": args.prompt,
        "params": {
            "size": args.size,
            "quality": args.quality,
            "style": args.style,
        },
        "variants": results,
        "timestamp": datetime.now().isoformat(),
    }

    meta_path = output_dir / f"{args.prefix}_metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
