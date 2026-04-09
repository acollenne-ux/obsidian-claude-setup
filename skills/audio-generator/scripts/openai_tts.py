#!/usr/bin/env python3
"""
openai_tts.py — Wrapper OpenAI API pour generation audio TTS

Usage:
    python openai_tts.py \
        --text "Bonjour, ceci est un test de synthese vocale." \
        --voice "nova" \
        --model "tts-1-hd" \
        --format "mp3" \
        --speed 1.0 \
        --output "C:/tmp/audio-generator/session/"
"""

import argparse
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

VALID_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
VALID_MODELS = ["tts-1", "tts-1-hd"]
VALID_FORMATS = ["mp3", "opus", "aac", "flac", "wav", "pcm"]
MAX_CHARS = 4096


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


def chunk_text(text, max_chars=MAX_CHARS):
    """Decoupe le texte en chunks de max_chars, en respectant les phrases."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current = ""
    sentences = text.replace(".\n", ".|SPLIT|").replace(". ", ".|SPLIT|").split("|SPLIT|")

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current = (current + " " + sentence).strip() if current else sentence
        else:
            if current:
                chunks.append(current)
            current = sentence

    if current:
        chunks.append(current)

    return chunks if chunks else [text[:max_chars]]


def generate_speech(text, api_key, model="tts-1-hd", voice="nova",
                    speed=1.0, response_format="mp3"):
    """Genere un audio via l'API OpenAI TTS."""
    url = "https://api.openai.com/v1/audio/speech"

    payload = {
        "model": model,
        "input": text,
        "voice": voice,
        "speed": speed,
        "response_format": response_format,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    json_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")

    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            audio_data = response.read()
            elapsed = int((time.time() - start_time) * 1000)
            return audio_data, elapsed

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            error_json = json.loads(body)
            error_msg = error_json.get("error", {}).get("message", body[:500])
        except json.JSONDecodeError:
            error_msg = body[:500]

        if e.code == 429:
            raise RuntimeError(f"Rate limit OpenAI atteint: {error_msg}")
        elif e.code == 400:
            raise RuntimeError(f"Requete invalide: {error_msg}")
        elif e.code == 401:
            raise RuntimeError("Cle API OpenAI invalide ou expiree")
        else:
            raise RuntimeError(f"Erreur HTTP {e.code}: {error_msg}")

    except urllib.error.URLError as e:
        raise RuntimeError(f"Erreur connexion OpenAI: {e.reason}")


def main():
    parser = argparse.ArgumentParser(description="Generate speech via OpenAI TTS API")
    parser.add_argument("--text", required=True, help="Texte a convertir en audio")
    parser.add_argument("--voice", default="nova", choices=VALID_VOICES,
                        help="Voix (alloy, echo, fable, onyx, nova, shimmer)")
    parser.add_argument("--model", default="tts-1-hd", choices=VALID_MODELS,
                        help="Modele (tts-1, tts-1-hd)")
    parser.add_argument("--format", default="mp3", choices=VALID_FORMATS,
                        help="Format de sortie")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Vitesse (0.25-4.0, defaut 1.0)")
    parser.add_argument("--output", required=True, help="Dossier de sortie")
    parser.add_argument("--prefix", default="openai_tts", help="Prefixe fichiers")
    parser.add_argument("--text-file", default=None,
                        help="Fichier texte a lire (alternative a --text)")

    args = parser.parse_args()

    # Charger texte depuis fichier si specifie
    text = args.text
    if args.text_file and os.path.exists(args.text_file):
        text = Path(args.text_file).read_text(encoding="utf-8")

    # Charger la cle
    api_key = load_openai_key()
    if not api_key:
        print("ERREUR: Cle OpenAI non trouvee dans ai_config.json, api_keys.json ou $OPENAI_API_KEY",
              file=sys.stderr)
        sys.exit(1)

    # Creer le dossier de sortie
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Chunker le texte si necessaire
    chunks = chunk_text(text)
    total_chunks = len(chunks)

    results = []
    all_audio = bytearray()

    for idx, chunk in enumerate(chunks):
        print(f"[OpenAI-TTS] Generation chunk {idx+1}/{total_chunks} "
              f"({len(chunk)} chars) via {args.model}/{args.voice}...", file=sys.stderr)

        try:
            audio_data, elapsed_ms = generate_speech(
                text=chunk,
                api_key=api_key,
                model=args.model,
                voice=args.voice,
                speed=args.speed,
                response_format=args.format,
            )

            if total_chunks == 1:
                filename = f"{args.prefix}.{args.format}"
            else:
                filename = f"{args.prefix}_chunk{idx+1}.{args.format}"

            filepath = output_dir / filename
            filepath.write_bytes(audio_data)
            all_audio.extend(audio_data)

            result = {
                "file": filename,
                "path": str(filepath),
                "provider": "openai",
                "model": args.model,
                "voice": args.voice,
                "chunk_index": idx,
                "chunk_chars": len(chunk),
                "time_ms": elapsed_ms,
                "status": "success",
                "size_bytes": len(audio_data),
            }
            results.append(result)
            print(f"[OpenAI-TTS] Chunk {idx+1} sauvegarde: {filepath} "
                  f"({len(audio_data)} bytes, {elapsed_ms}ms)", file=sys.stderr)

        except Exception as e:
            result = {
                "file": None,
                "provider": "openai",
                "model": args.model,
                "voice": args.voice,
                "chunk_index": idx,
                "status": "error",
                "error": str(e),
            }
            results.append(result)
            print(f"[OpenAI-TTS] ERREUR chunk {idx+1}: {e}", file=sys.stderr)

    # Si multi-chunks et format mp3, concatener avec ffmpeg
    if total_chunks > 1 and all(r["status"] == "success" for r in results):
        try:
            import subprocess
            concat_file = output_dir / "concat_list.txt"
            with open(concat_file, "w") as f:
                for r in results:
                    f.write(f"file '{r['file']}'\n")

            merged_path = output_dir / f"{args.prefix}_merged.{args.format}"
            subprocess.run([
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(concat_file), "-c", "copy", str(merged_path)
            ], capture_output=True, check=True, cwd=str(output_dir))

            concat_file.unlink()
            print(f"[OpenAI-TTS] Chunks fusionnes: {merged_path}", file=sys.stderr)
        except Exception as e:
            print(f"[OpenAI-TTS] Warning: fusion echouee: {e}", file=sys.stderr)

    # Metadata
    metadata = {
        "provider": "openai",
        "model": args.model,
        "voice": args.voice,
        "text": text[:500] + ("..." if len(text) > 500 else ""),
        "text_length": len(text),
        "chunks": total_chunks,
        "params": {
            "speed": args.speed,
            "format": args.format,
        },
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }

    meta_path = output_dir / f"{args.prefix}_metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
