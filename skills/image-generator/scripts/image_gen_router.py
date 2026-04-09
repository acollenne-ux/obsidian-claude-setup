#!/usr/bin/env python3
"""
image_gen_router.py — Routeur intelligent multi-provider pour generation d'images IA

Orchestre la generation via FLUX (HuggingFace), GPT-Image (OpenAI), Nano Banana 2 (Gemini),
et SDXL (HuggingFace). Route automatiquement vers le meilleur provider selon le type de tache.

Usage:
    python image_gen_router.py generate \
        --prompt "A photorealistic cat on the Moon" \
        --type photo \
        --quality standard \
        --size 1024 \
        --output C:/tmp/image-generator/session_001/

    python image_gen_router.py list-providers

    python image_gen_router.py test-providers
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PYTHON = sys.executable

# Matrice de routage : type → providers ordonnes par priorite
ROUTING_TABLE = {
    "photo": ["flux-schnell", "openai", "gemini"],
    "illustration": ["flux-schnell", "sdxl", "openai"],
    "text-in-image": ["openai", "gemini", "flux-schnell"],
    "logo": ["openai", "sdxl", "gemini"],
    "anime": ["sdxl", "flux-schnell", "openai"],
    "abstract": ["flux-schnell", "sdxl", "gemini"],
    "fast": ["gemini", "flux-schnell", "sdxl-turbo"],
}

# Nombre de providers et variantes par mode qualite
QUALITY_MODES = {
    "draft": {"providers": 1, "variants_per_provider": 1},
    "standard": {"providers": 2, "variants_per_provider": 2},
    "best": {"providers": 3, "variants_per_provider": 3},
}

# Mapping provider → script + parametres
PROVIDER_SCRIPTS = {
    "flux-schnell": {
        "script": "hf_generate.py",
        "args": {"--space": "flux-schnell", "--prefix": "flux_schnell"},
    },
    "flux-dev": {
        "script": "hf_generate.py",
        "args": {"--space": "flux-dev", "--prefix": "flux_dev"},
    },
    "sdxl": {
        "script": "hf_generate.py",
        "args": {"--space": "sdxl", "--prefix": "sdxl"},
    },
    "sdxl-turbo": {
        "script": "hf_generate.py",
        "args": {"--space": "sdxl-turbo", "--prefix": "sdxl_turbo"},
    },
    "sd3.5": {
        "script": "hf_generate.py",
        "args": {"--space": "sd3.5", "--prefix": "sd35"},
    },
    "openai": {
        "script": "openai_generate.py",
        "args": {"--model": "dall-e-3", "--quality": "hd", "--style": "natural", "--prefix": "openai"},
    },
    "gemini": {
        "script": "gemini_generate.py",
        "args": {"--model": "default", "--prefix": "gemini"},
    },
}


def run_provider(provider_name, prompt, negative_prompt, size, variants, output_dir):
    """Execute un script de generation pour un provider donne."""
    config = PROVIDER_SCRIPTS.get(provider_name)
    if not config:
        return {"provider": provider_name, "status": "error", "error": f"Provider inconnu: {provider_name}"}

    script_path = SCRIPTS_DIR / config["script"]
    if not script_path.exists():
        return {"provider": provider_name, "status": "error", "error": f"Script manquant: {script_path}"}

    cmd = [PYTHON, str(script_path), "--prompt", prompt, "--output", str(output_dir), "--variants", str(variants)]

    # Ajouter les args specifiques au provider
    for key, value in config["args"].items():
        cmd.extend([key, str(value)])

    # Ajouter la taille
    if "hf_generate" in config["script"]:
        cmd.extend(["--size", str(size)])
    elif "openai_generate" in config["script"]:
        # DALL-E 3 n'accepte que 1024x1024, 1024x1792, 1792x1024
        oai_size = f"{size}x{size}" if size >= 1024 else "1024x1024"
        cmd.extend(["--size", oai_size])
    elif "gemini_generate" in config["script"]:
        cmd.extend(["--size", f"{size}x{size}"])

    # Ajouter le prompt negatif si applicable
    if negative_prompt and "hf_generate" in config["script"]:
        cmd.extend(["--negative", negative_prompt])

    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
            encoding="utf-8",
            errors="replace",
        )

        elapsed = int((time.time() - start_time) * 1000)

        if result.returncode == 0:
            try:
                metadata = json.loads(result.stdout)
                metadata["total_time_ms"] = elapsed
                return metadata
            except json.JSONDecodeError:
                return {
                    "provider": provider_name,
                    "status": "success",
                    "total_time_ms": elapsed,
                    "raw_output": result.stdout[:1000],
                }
        else:
            return {
                "provider": provider_name,
                "status": "error",
                "error": result.stderr[:1000] if result.stderr else f"Exit code {result.returncode}",
                "total_time_ms": elapsed,
            }

    except subprocess.TimeoutExpired:
        return {
            "provider": provider_name,
            "status": "error",
            "error": "Timeout (180s)",
            "total_time_ms": 180000,
        }
    except Exception as e:
        return {
            "provider": provider_name,
            "status": "error",
            "error": str(e),
        }


def generate(args):
    """Commande principale de generation."""
    image_type = args.type
    quality = args.quality
    prompt = args.prompt
    negative = args.negative
    size = args.size
    output_dir = Path(args.output)

    # Creer le dossier de session
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determiner les providers
    providers_ordered = ROUTING_TABLE.get(image_type, ROUTING_TABLE["photo"])
    mode = QUALITY_MODES[quality]
    selected_providers = providers_ordered[:mode["providers"]]
    variants_per = mode["variants_per_provider"]

    print(f"[ROUTER] Type: {image_type} | Qualite: {quality} | Size: {size}", file=sys.stderr)
    print(f"[ROUTER] Providers selectionnes: {selected_providers} ({variants_per} variantes chacun)", file=sys.stderr)

    # Generer avec chaque provider
    all_results = []
    for provider in selected_providers:
        print(f"\n[ROUTER] Lancement {provider}...", file=sys.stderr)
        result = run_provider(provider, prompt, negative, size, variants_per, output_dir)
        all_results.append(result)

        status = result.get("status", "unknown")
        time_ms = result.get("total_time_ms", 0)
        if status == "error":
            error = result.get("error", "?")
            print(f"[ROUTER] {provider}: ERREUR — {error}", file=sys.stderr)
            # Fallback : essayer le provider suivant dans la liste
            remaining = [p for p in providers_ordered if p not in selected_providers and p != provider]
            if remaining:
                fallback = remaining[0]
                print(f"[ROUTER] Fallback vers {fallback}...", file=sys.stderr)
                fb_result = run_provider(fallback, prompt, negative, size, variants_per, output_dir)
                all_results.append(fb_result)
        else:
            print(f"[ROUTER] {provider}: OK ({time_ms}ms)", file=sys.stderr)

    # Consolider les resultats
    session_metadata = {
        "session_id": output_dir.name,
        "timestamp": datetime.now().isoformat(),
        "user_prompt": prompt,
        "negative_prompt": negative,
        "type": image_type,
        "quality_mode": quality,
        "size": size,
        "providers_requested": selected_providers,
        "results": all_results,
        "all_images": [],
    }

    # Collecter toutes les images generees
    for result in all_results:
        if "variants" in result:
            for variant in result["variants"]:
                if variant.get("status") == "success" and variant.get("file"):
                    session_metadata["all_images"].append({
                        "file": variant["file"],
                        "path": variant.get("path"),
                        "provider": result.get("provider", "unknown"),
                        "time_ms": variant.get("time_ms", 0),
                    })

    # Sauvegarder metadata session
    meta_path = output_dir / "session_metadata.json"
    meta_path.write_text(json.dumps(session_metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    # Output
    total_images = len(session_metadata["all_images"])
    successful = [r for r in all_results if r.get("status") != "error"]

    print(f"\n[ROUTER] === RESUME ===", file=sys.stderr)
    print(f"[ROUTER] Images generees: {total_images}", file=sys.stderr)
    print(f"[ROUTER] Providers OK: {len(successful)}/{len(all_results)}", file=sys.stderr)
    print(f"[ROUTER] Metadata: {meta_path}", file=sys.stderr)

    print(json.dumps(session_metadata, indent=2, ensure_ascii=False))


def list_providers(args):
    """Liste les providers disponibles."""
    print("=== PROVIDERS DISPONIBLES ===\n")
    for name, config in PROVIDER_SCRIPTS.items():
        script = config["script"]
        extra = config["args"]
        print(f"  {name}")
        print(f"    Script: {script}")
        print(f"    Args: {json.dumps(extra)}")
        print()

    print("\n=== MATRICE DE ROUTAGE ===\n")
    for img_type, providers in ROUTING_TABLE.items():
        print(f"  {img_type:20s} -> {' -> '.join(providers)}")

    print("\n=== MODES QUALITE ===\n")
    for mode, config in QUALITY_MODES.items():
        print(f"  {mode:10s} -> {config['providers']} providers, {config['variants_per_provider']} variantes/provider")


def test_providers(args):
    """Teste la connectivite de chaque provider."""
    print("=== TEST PROVIDERS ===\n")
    test_prompt = "A simple red circle on white background, minimalist"

    output_dir = Path("C:/tmp/image-generator/_test_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    output_dir.mkdir(parents=True, exist_ok=True)

    for name in ["flux-schnell", "openai", "gemini"]:
        print(f"  Testing {name}...", end=" ", flush=True)
        result = run_provider(name, test_prompt, None, 512, 1, output_dir)
        status = result.get("status", "unknown")
        if status == "error":
            print(f"ERREUR: {result.get('error', '?')[:100]}")
        else:
            time_ms = result.get("total_time_ms", 0)
            print(f"OK ({time_ms}ms)")

    print(f"\n  Resultats dans: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Image Generation Router — Multi-Provider")
    subparsers = parser.add_subparsers(dest="command")

    # generate
    gen_parser = subparsers.add_parser("generate", help="Generer des images")
    gen_parser.add_argument("--prompt", required=True, help="Prompt de generation")
    gen_parser.add_argument("--negative", default=None, help="Prompt negatif")
    gen_parser.add_argument("--type", default="photo",
                           choices=["photo", "illustration", "text-in-image", "logo", "anime", "abstract", "fast"],
                           help="Type d'image")
    gen_parser.add_argument("--quality", default="standard", choices=["draft", "standard", "best"],
                           help="Mode qualite")
    gen_parser.add_argument("--size", type=int, default=1024, help="Taille (carre)")
    gen_parser.add_argument("--output", required=True, help="Dossier de sortie")

    # list-providers
    subparsers.add_parser("list-providers", help="Lister les providers")

    # test-providers
    subparsers.add_parser("test-providers", help="Tester la connectivite")

    args = parser.parse_args()

    if args.command == "generate":
        generate(args)
    elif args.command == "list-providers":
        list_providers(args)
    elif args.command == "test-providers":
        test_providers(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
