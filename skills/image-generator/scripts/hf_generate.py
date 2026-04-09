#!/usr/bin/env python3
"""
hf_generate.py — Wrapper HuggingFace Spaces pour generation d'images IA

Utilise l'API HuggingFace Inference pour interagir avec les Spaces de generation d'images.
Supporte FLUX.1 (schnell/dev), SDXL, SD3.5 et tout Space compatible.

Usage:
    python hf_generate.py \
        --prompt "A cat on the moon" \
        --space "black-forest-labs/FLUX.1-schnell" \
        --size 1024 \
        --variants 2 \
        --output "C:/tmp/image-generator/session/"

    python hf_generate.py \
        --prompt "anime girl" \
        --negative "low quality, blurry" \
        --space "stabilityai/stable-diffusion-3.5-large" \
        --size 1024 \
        --cfg 7.0 \
        --steps 30 \
        --variants 1 \
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

# Chemins
AI_CONFIG = Path.home() / ".claude" / "tools" / "ai_config.json"
API_KEYS = Path.home() / ".claude" / "tools" / "api_keys.json"

# Spaces pre-configures
SPACES = {
    "flux-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux-dev": "black-forest-labs/FLUX.1-dev",
    "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
    "sd3.5": "stabilityai/stable-diffusion-3.5-large",
    "sdxl-turbo": "stabilityai/sdxl-turbo",
}

# Parametres par defaut par Space
SPACE_DEFAULTS = {
    "black-forest-labs/FLUX.1-schnell": {
        "steps": 4,
        "cfg": 0.0,
        "scheduler": None,
        "supports_negative": False,
    },
    "black-forest-labs/FLUX.1-dev": {
        "steps": 28,
        "cfg": 3.5,
        "scheduler": None,
        "supports_negative": False,
    },
    "stabilityai/stable-diffusion-xl-base-1.0": {
        "steps": 30,
        "cfg": 7.0,
        "scheduler": "DPM++ 2M Karras",
        "supports_negative": True,
    },
    "stabilityai/stable-diffusion-3.5-large": {
        "steps": 28,
        "cfg": 5.0,
        "scheduler": "DPM++ 2M",
        "supports_negative": True,
    },
    "stabilityai/sdxl-turbo": {
        "steps": 1,
        "cfg": 0.0,
        "scheduler": None,
        "supports_negative": False,
    },
}


def load_hf_token():
    """Charge le token HuggingFace depuis ai_config.json ou api_keys.json."""
    for config_path in [AI_CONFIG, API_KEYS]:
        if config_path.exists():
            try:
                data = json.loads(config_path.read_text(encoding="utf-8"))
                # ai_config.json format
                if "providers" in data:
                    for provider in data["providers"]:
                        if provider.get("name", "").lower() in ("huggingface", "hf"):
                            return provider.get("api_key")
                # api_keys.json format
                if "huggingface" in data:
                    return data["huggingface"].get("api_key")
                if "HuggingFace" in data:
                    return data["HuggingFace"].get("api_key")
            except (json.JSONDecodeError, KeyError):
                continue
    # Fallback: variable d'environnement
    return os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")


def generate_via_inference_api(prompt, negative_prompt, space, params, hf_token):
    """Genere une image via l'API Inference HuggingFace."""
    import urllib.request
    import urllib.error

    # Determiner l'URL API
    # Pour les modeles text-to-image, utiliser l'API Inference
    api_url = f"https://router.huggingface.co/hf-inference/models/{space}"

    # Construire le payload
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": params.get("steps", 28),
            "width": params.get("width", 1024),
            "height": params.get("height", 1024),
        },
    }

    if params.get("cfg") and params["cfg"] > 0:
        payload["parameters"]["guidance_scale"] = params["cfg"]

    if negative_prompt and params.get("supports_negative", True):
        payload["parameters"]["negative_prompt"] = negative_prompt

    if params.get("seed") and params["seed"] >= 0:
        payload["parameters"]["seed"] = params["seed"]

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json",
        "Accept": "image/png",
    }

    json_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(api_url, data=json_data, headers=headers, method="POST")

    start_time = time.time()
    max_retries = 3
    retry_delay = 10

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                content_type = response.headers.get("Content-Type", "")
                data = response.read()

                if "image" in content_type:
                    elapsed = int((time.time() - start_time) * 1000)
                    return data, elapsed

                # Reponse JSON (peut etre une erreur ou du base64)
                try:
                    json_resp = json.loads(data.decode("utf-8"))
                    if isinstance(json_resp, list) and json_resp:
                        if "image" in json_resp[0]:
                            img_data = base64.b64decode(json_resp[0]["image"])
                            elapsed = int((time.time() - start_time) * 1000)
                            return img_data, elapsed
                    if "error" in json_resp:
                        error_msg = json_resp["error"]
                        if "loading" in str(error_msg).lower() or "queue" in str(error_msg).lower():
                            wait = json_resp.get("estimated_time", retry_delay)
                            print(f"[HF] Modele en chargement, attente {wait:.0f}s... (tentative {attempt+1}/{max_retries})", file=sys.stderr)
                            time.sleep(min(wait, 60))
                            continue
                        raise RuntimeError(f"Erreur HF API: {error_msg}")
                except json.JSONDecodeError:
                    raise RuntimeError(f"Reponse inattendue: Content-Type={content_type}")

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code == 503:
                print(f"[HF] Service temporairement indisponible (503), retry {attempt+1}/{max_retries}...", file=sys.stderr)
                time.sleep(retry_delay)
                continue
            elif e.code == 429:
                print(f"[HF] Rate limit atteint (429), attente {retry_delay}s...", file=sys.stderr)
                time.sleep(retry_delay)
                continue
            raise RuntimeError(f"Erreur HTTP {e.code}: {body[:500]}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Erreur connexion: {e.reason}")

    raise RuntimeError(f"Echec apres {max_retries} tentatives")


def generate_via_gradio_client(prompt, negative_prompt, space, params, hf_token):
    """Fallback: genere via gradio_client si disponible."""
    try:
        from gradio_client import Client
    except ImportError:
        raise RuntimeError("gradio_client non installe. Installer avec: pip install gradio_client")

    client = Client(space, hf_token=hf_token)

    # Tenter l'API predict standard
    start_time = time.time()
    result = client.predict(
        prompt,
        api_name="/predict" if not negative_prompt else "/generate",
    )
    elapsed = int((time.time() - start_time) * 1000)

    if isinstance(result, str) and os.path.exists(result):
        with open(result, "rb") as f:
            return f.read(), elapsed

    raise RuntimeError(f"Resultat inattendu de gradio_client: {type(result)}")


def resolve_space(space_name):
    """Resout un alias de Space ou retourne le nom tel quel."""
    return SPACES.get(space_name, space_name)


def get_space_defaults(space):
    """Retourne les parametres par defaut pour un Space."""
    return SPACE_DEFAULTS.get(space, {
        "steps": 28,
        "cfg": 7.0,
        "scheduler": None,
        "supports_negative": True,
    })


def main():
    parser = argparse.ArgumentParser(description="Generate images via HuggingFace Spaces")
    parser.add_argument("--prompt", required=True, help="Prompt de generation")
    parser.add_argument("--negative", default=None, help="Prompt negatif (si supporte)")
    parser.add_argument("--space", default="flux-schnell", help="Space HF ou alias (flux-schnell, flux-dev, sdxl, sd3.5, sdxl-turbo)")
    parser.add_argument("--size", type=int, default=1024, help="Taille de l'image (carre)")
    parser.add_argument("--width", type=int, default=None, help="Largeur (override --size)")
    parser.add_argument("--height", type=int, default=None, help="Hauteur (override --size)")
    parser.add_argument("--cfg", type=float, default=None, help="CFG scale (override defaut du Space)")
    parser.add_argument("--steps", type=int, default=None, help="Nombre de steps (override defaut du Space)")
    parser.add_argument("--seed", type=int, default=-1, help="Seed (-1 = random)")
    parser.add_argument("--variants", type=int, default=1, help="Nombre de variantes a generer")
    parser.add_argument("--output", required=True, help="Dossier de sortie")
    parser.add_argument("--prefix", default="hf", help="Prefixe des fichiers de sortie")
    parser.add_argument("--method", default="api", choices=["api", "gradio"], help="Methode d'appel (api ou gradio)")

    args = parser.parse_args()

    # Charger le token
    hf_token = load_hf_token()
    if not hf_token:
        print("ERREUR: Token HuggingFace non trouve dans ai_config.json, api_keys.json ou $HF_TOKEN", file=sys.stderr)
        sys.exit(1)

    # Resoudre le Space
    space = resolve_space(args.space)
    defaults = get_space_defaults(space)

    # Parametres finaux
    params = {
        "steps": args.steps or defaults.get("steps", 28),
        "cfg": args.cfg if args.cfg is not None else defaults.get("cfg", 7.0),
        "width": args.width or args.size,
        "height": args.height or args.size,
        "seed": args.seed,
        "supports_negative": defaults.get("supports_negative", True),
    }

    # Creer le dossier de sortie
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generer les variantes
    results = []
    for i in range(args.variants):
        variant_seed = args.seed if args.seed >= 0 else int(time.time() * 1000 + i) % (2**32)
        params["seed"] = variant_seed

        print(f"[HF] Generation variante {i+1}/{args.variants} via {space} (seed={variant_seed})...", file=sys.stderr)

        try:
            if args.method == "api":
                image_data, elapsed_ms = generate_via_inference_api(
                    args.prompt, args.negative, space, params, hf_token
                )
            else:
                image_data, elapsed_ms = generate_via_gradio_client(
                    args.prompt, args.negative, space, params, hf_token
                )

            # Sauvegarder l'image
            filename = f"{args.prefix}_v{i+1}.png"
            filepath = output_dir / filename
            filepath.write_bytes(image_data)

            result = {
                "file": filename,
                "path": str(filepath),
                "provider": "huggingface",
                "space": space,
                "seed": variant_seed,
                "time_ms": elapsed_ms,
                "status": "success",
                "size_bytes": len(image_data),
            }
            results.append(result)
            print(f"[HF] Variante {i+1} sauvegardee: {filepath} ({len(image_data)} bytes, {elapsed_ms}ms)", file=sys.stderr)

        except Exception as e:
            result = {
                "file": None,
                "provider": "huggingface",
                "space": space,
                "seed": variant_seed,
                "status": "error",
                "error": str(e),
            }
            results.append(result)
            print(f"[HF] ERREUR variante {i+1}: {e}", file=sys.stderr)

    # Sauvegarder les metadata
    metadata = {
        "provider": "huggingface",
        "space": space,
        "prompt": args.prompt,
        "negative_prompt": args.negative,
        "params": {
            "steps": params["steps"],
            "cfg_scale": params["cfg"],
            "width": params["width"],
            "height": params["height"],
        },
        "variants": results,
        "timestamp": datetime.now().isoformat(),
    }

    meta_path = output_dir / f"{args.prefix}_metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    # Output JSON sur stdout pour le routeur
    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
