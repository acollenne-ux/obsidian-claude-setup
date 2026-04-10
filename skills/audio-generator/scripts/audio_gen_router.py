#!/usr/bin/env python3
"""
audio_gen_router.py — Routeur intelligent multi-provider pour generation audio

Selectionne et orchestre les providers (OpenAI TTS, HuggingFace Spaces)
selon le type de tache, la langue et le mode qualite.

Usage:
    python audio_gen_router.py generate \
        --text "Bonjour le monde" \
        --type tts \
        --language fr \
        --mode standard \
        --output "C:/tmp/audio-generator/session/"

    python audio_gen_router.py list-providers
    python audio_gen_router.py test-providers --type tts
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

# Matrice de routage : type -> [providers ordonnes par priorite]
# Mis a jour avril 2026 — base sur TTS Arena, MOS scores, et disponibilite HF Spaces
ROUTING_TABLE = {
    "tts": [
        {"name": "qwen3-tts", "script": "hf_audio_generate.py", "args": ["--space", "qwen3-tts"]},
        {"name": "openai", "script": "openai_tts.py", "args": ["--model", "tts-1-hd"]},
        {"name": "kokoro", "script": "hf_audio_generate.py", "args": ["--space", "kokoro"]},
        {"name": "edge-tts-hf", "script": "hf_audio_generate.py", "args": ["--space", "edge-tts-hf"]},
    ],
    "tts-dialogue": [
        {"name": "dia", "script": "hf_audio_generate.py", "args": ["--space", "dia"]},
        {"name": "qwen3-tts", "script": "hf_audio_generate.py", "args": ["--space", "qwen3-tts"]},
        {"name": "openai", "script": "openai_tts.py", "args": ["--model", "tts-1-hd"]},
        {"name": "kokoro", "script": "hf_audio_generate.py", "args": ["--space", "kokoro"]},
    ],
    "tts-hifi": [
        {"name": "qwen3-tts", "script": "hf_audio_generate.py", "args": ["--space", "qwen3-tts"]},
        {"name": "f5-tts", "script": "hf_audio_generate.py", "args": ["--space", "f5-tts"]},
        {"name": "dia", "script": "hf_audio_generate.py", "args": ["--space", "dia"]},
        {"name": "openai", "script": "openai_tts.py", "args": ["--model", "tts-1-hd"]},
    ],
    "voice-clone": [
        {"name": "qwen3-tts", "script": "hf_audio_generate.py", "args": ["--space", "qwen3-tts"]},
        {"name": "f5-tts", "script": "hf_audio_generate.py", "args": ["--space", "f5-tts"]},
        {"name": "openvoice", "script": "hf_audio_generate.py", "args": ["--space", "openvoice"]},
    ],
    "music": [
        {"name": "tencent-song", "script": "hf_audio_generate.py", "args": ["--space", "tencent-song"]},
        {"name": "musicgen-unlimited", "script": "hf_audio_generate.py", "args": ["--space", "musicgen-unlimited"]},
    ],
    "sfx": [
        {"name": "musicgen-unlimited", "script": "hf_audio_generate.py", "args": ["--space", "musicgen-unlimited"]},
    ],
    "stt": [
        {"name": "openai-whisper", "script": "openai_stt.py", "args": ["--model", "whisper-1"]},
    ],
    "tts-fast": [
        {"name": "kokoro", "script": "hf_audio_generate.py", "args": ["--space", "kokoro"]},
        {"name": "edge-tts-hf", "script": "hf_audio_generate.py", "args": ["--space", "edge-tts-hf"]},
        {"name": "openai-fast", "script": "openai_tts.py", "args": ["--model", "tts-1"]},
    ],
}

# Modes qualite → nombre de providers a appeler
QUALITY_MODES = {
    "draft": 1,
    "standard": 2,
    "best": 3,
}


def run_provider(provider_config, text, output_dir, extra_args=None):
    """Execute un script provider et retourne le resultat."""
    script = SCRIPTS_DIR / provider_config["script"]
    cmd = [PYTHON, str(script)]

    if "openai_tts" in provider_config["script"]:
        cmd.extend(["--text", text])
        cmd.extend(["--prefix", provider_config["name"]])
    elif "openai_stt" in provider_config["script"]:
        cmd.extend(["--audio-file", text])  # text = chemin fichier pour STT
        cmd.extend(["--prefix", provider_config["name"]])
    else:
        cmd.extend(["--text", text])
        cmd.extend(["--prefix", provider_config["name"]])

    cmd.extend(provider_config.get("args", []))
    cmd.extend(["--output", str(output_dir)])

    if extra_args:
        cmd.extend(extra_args)

    print(f"[Router] Appel {provider_config['name']}: {' '.join(cmd[:6])}...", file=sys.stderr)

    start = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=180
        )
        elapsed = int((time.time() - start) * 1000)

        if result.returncode == 0:
            try:
                metadata = json.loads(result.stdout)
                metadata["router_time_ms"] = elapsed
                return {"status": "success", "provider": provider_config["name"], "metadata": metadata}
            except json.JSONDecodeError:
                return {"status": "success", "provider": provider_config["name"],
                        "raw_output": result.stdout[:1000], "router_time_ms": elapsed}
        else:
            return {"status": "error", "provider": provider_config["name"],
                    "error": result.stderr[:500], "router_time_ms": elapsed}

    except subprocess.TimeoutExpired:
        return {"status": "error", "provider": provider_config["name"],
                "error": "Timeout (180s)"}
    except Exception as e:
        return {"status": "error", "provider": provider_config["name"],
                "error": str(e)}


def cmd_generate(args):
    """Commande principale : generer audio avec routage intelligent."""
    task_type = args.type
    mode = args.mode
    text = args.text

    # Lire depuis fichier si specifie
    if args.text_file and os.path.exists(args.text_file):
        text = Path(args.text_file).read_text(encoding="utf-8")

    if task_type not in ROUTING_TABLE:
        print(f"ERREUR: Type inconnu '{task_type}'. Types valides: {list(ROUTING_TABLE.keys())}",
              file=sys.stderr)
        sys.exit(1)

    providers = ROUTING_TABLE[task_type]
    max_providers = min(QUALITY_MODES.get(mode, 2), len(providers))

    # Creer session
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output) / session_id if not args.no_session else Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extra args
    extra = []
    if args.voice:
        extra.extend(["--voice", args.voice])
    if args.format:
        extra.extend(["--format", args.format])
    if args.speed:
        extra.extend(["--speed", str(args.speed)])
    if args.reference_audio:
        extra.extend(["--reference-audio", args.reference_audio])
    if args.duration:
        extra.extend(["--duration", str(args.duration)])
    if args.consent_confirmed:
        extra.append("--consent-confirmed")
    if args.language:
        extra.extend(["--language", args.language])

    # Executer les providers
    results = []
    for i, provider in enumerate(providers[:max_providers]):
        print(f"\n[Router] Provider {i+1}/{max_providers}: {provider['name']}", file=sys.stderr)
        result = run_provider(provider, text, output_dir, extra)
        results.append(result)

        if result["status"] == "success":
            print(f"[Router] {provider['name']} OK", file=sys.stderr)
        else:
            print(f"[Router] {provider['name']} ECHEC: {result.get('error', 'unknown')[:200]}",
                  file=sys.stderr)
            # En mode draft, essayer le provider suivant
            if mode == "draft" and i < len(providers) - 1:
                print(f"[Router] Fallback vers {providers[i+1]['name']}...", file=sys.stderr)
                max_providers = min(max_providers + 1, len(providers))

    # Selectionner le meilleur
    successful = [r for r in results if r["status"] == "success"]
    best = successful[0] if successful else None

    # Rapport final
    report = {
        "session_id": session_id,
        "type": task_type,
        "mode": mode,
        "text_length": len(text),
        "providers_called": max_providers,
        "results": results,
        "selected": best["provider"] if best else None,
        "output_dir": str(output_dir),
        "timestamp": datetime.now().isoformat(),
    }

    report_path = output_dir / "router_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))

    if not best:
        print("\n[Router] ECHEC: Aucun provider n'a reussi.", file=sys.stderr)
        sys.exit(1)


def cmd_list_providers(args):
    """Liste tous les providers disponibles."""
    for task_type, providers in ROUTING_TABLE.items():
        print(f"\n{task_type}:")
        for i, p in enumerate(providers):
            print(f"  {i+1}. {p['name']} ({p['script']})")


def cmd_test_providers(args):
    """Teste la disponibilite des providers."""
    task_type = args.type or "tts"
    if task_type not in ROUTING_TABLE:
        print(f"Type inconnu: {task_type}")
        return

    test_text = "Test audio generation."
    output_dir = Path("C:/tmp/audio-generator/test")
    output_dir.mkdir(parents=True, exist_ok=True)

    for provider in ROUTING_TABLE[task_type]:
        print(f"Testing {provider['name']}...", end=" ")
        result = run_provider(provider, test_text, output_dir)
        if result["status"] == "success":
            print("OK")
        else:
            print(f"FAIL: {result.get('error', 'unknown')[:100]}")


def main():
    parser = argparse.ArgumentParser(description="Audio Generation Router")
    subparsers = parser.add_subparsers(dest="command")

    # generate
    gen = subparsers.add_parser("generate", help="Generer audio")
    gen.add_argument("--text", default="", help="Texte ou prompt")
    gen.add_argument("--text-file", default=None, help="Fichier texte")
    gen.add_argument("--type", default="tts",
                     choices=list(ROUTING_TABLE.keys()), help="Type de tache")
    gen.add_argument("--mode", default="standard",
                     choices=list(QUALITY_MODES.keys()), help="Mode qualite")
    gen.add_argument("--output", default="C:/tmp/audio-generator",
                     help="Dossier de sortie")
    gen.add_argument("--voice", default=None, help="Voix (OpenAI)")
    gen.add_argument("--format", default=None, help="Format sortie")
    gen.add_argument("--speed", type=float, default=None, help="Vitesse")
    gen.add_argument("--language", default=None, help="Code langue")
    gen.add_argument("--reference-audio", default=None, help="Audio reference (cloning)")
    gen.add_argument("--duration", type=int, default=None, help="Duree (musique/SFX)")
    gen.add_argument("--consent-confirmed", action="store_true", help="Consentement voice cloning")
    gen.add_argument("--no-session", action="store_true", help="Pas de sous-dossier session")

    # list-providers
    subparsers.add_parser("list-providers", help="Lister les providers")

    # test-providers
    test = subparsers.add_parser("test-providers", help="Tester les providers")
    test.add_argument("--type", default="tts", help="Type a tester")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "list-providers":
        cmd_list_providers(args)
    elif args.command == "test-providers":
        cmd_test_providers(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
