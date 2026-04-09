#!/usr/bin/env python3
"""
openai_stt.py — Wrapper OpenAI Whisper API pour transcription audio (Speech-to-Text)

Usage:
    python openai_stt.py \
        --audio-file "C:/tmp/input.mp3" \
        --language "fr" \
        --format "text" \
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

VALID_FORMATS = ["json", "text", "srt", "verbose_json", "vtt"]
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB


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


def transcribe_audio(audio_path, api_key, model="whisper-1", language=None,
                     response_format="json", prompt=None):
    """Transcrit un fichier audio via l'API OpenAI Whisper."""
    url = "https://api.openai.com/v1/audio/transcriptions"

    # Lire le fichier audio
    audio_data = Path(audio_path).read_bytes()
    filename = Path(audio_path).name

    if len(audio_data) > MAX_FILE_SIZE:
        raise RuntimeError(f"Fichier trop volumineux ({len(audio_data)} bytes, max {MAX_FILE_SIZE})")

    # Construire la requete multipart
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = bytearray()

    # Champ file
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode())
    body.extend(b"Content-Type: application/octet-stream\r\n\r\n")
    body.extend(audio_data)
    body.extend(b"\r\n")

    # Champ model
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(b'Content-Disposition: form-data; name="model"\r\n\r\n')
    body.extend(model.encode())
    body.extend(b"\r\n")

    # Champ response_format
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(b'Content-Disposition: form-data; name="response_format"\r\n\r\n')
    body.extend(response_format.encode())
    body.extend(b"\r\n")

    # Champ language (optionnel)
    if language:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="language"\r\n\r\n')
        body.extend(language.encode())
        body.extend(b"\r\n")

    # Champ prompt (optionnel)
    if prompt:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="prompt"\r\n\r\n')
        body.extend(prompt.encode())
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode())

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }

    req = urllib.request.Request(url, data=bytes(body), headers=headers, method="POST")

    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = response.read().decode("utf-8")
            elapsed = int((time.time() - start_time) * 1000)
            return result, elapsed

    except urllib.error.HTTPError as e:
        body_err = e.read().decode("utf-8", errors="replace")
        try:
            error_json = json.loads(body_err)
            error_msg = error_json.get("error", {}).get("message", body_err[:500])
        except json.JSONDecodeError:
            error_msg = body_err[:500]
        raise RuntimeError(f"Erreur HTTP {e.code}: {error_msg}")

    except urllib.error.URLError as e:
        raise RuntimeError(f"Erreur connexion: {e.reason}")


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio via OpenAI Whisper API")
    parser.add_argument("--audio-file", required=True, help="Fichier audio a transcrire")
    parser.add_argument("--model", default="whisper-1",
                        help="Modele (whisper-1, gpt-4o-transcribe)")
    parser.add_argument("--language", default=None,
                        help="Code langue ISO 639-1 (fr, en, es, etc.)")
    parser.add_argument("--format", default="json", choices=VALID_FORMATS,
                        help="Format de sortie")
    parser.add_argument("--prompt", default=None,
                        help="Prompt contextuel pour guider la transcription")
    parser.add_argument("--output", required=True, help="Dossier de sortie")
    parser.add_argument("--prefix", default="whisper", help="Prefixe fichiers")

    args = parser.parse_args()

    # Verifier que le fichier existe
    if not os.path.exists(args.audio_file):
        print(f"ERREUR: Fichier audio introuvable: {args.audio_file}", file=sys.stderr)
        sys.exit(1)

    # Charger la cle
    api_key = load_openai_key()
    if not api_key:
        print("ERREUR: Cle OpenAI non trouvee", file=sys.stderr)
        sys.exit(1)

    # Creer le dossier de sortie
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[Whisper] Transcription de {args.audio_file} via {args.model}...", file=sys.stderr)

    try:
        result_text, elapsed_ms = transcribe_audio(
            audio_path=args.audio_file,
            api_key=api_key,
            model=args.model,
            language=args.language,
            response_format=args.format,
            prompt=args.prompt,
        )

        # Determiner l'extension
        ext_map = {"json": "json", "verbose_json": "json", "text": "txt", "srt": "srt", "vtt": "vtt"}
        ext = ext_map.get(args.format, "txt")
        filename = f"{args.prefix}_transcription.{ext}"
        filepath = output_dir / filename
        filepath.write_text(result_text, encoding="utf-8")

        print(f"[Whisper] Transcription sauvegardee: {filepath} ({elapsed_ms}ms)", file=sys.stderr)

        # Metadata
        metadata = {
            "provider": "openai",
            "model": args.model,
            "audio_file": args.audio_file,
            "language": args.language,
            "format": args.format,
            "output_file": str(filepath),
            "time_ms": elapsed_ms,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
        }

        meta_path = output_dir / f"{args.prefix}_metadata.json"
        meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

        # Output
        if args.format in ("json", "verbose_json"):
            print(result_text)
        else:
            print(json.dumps(metadata, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"[Whisper] ERREUR: {e}", file=sys.stderr)
        metadata = {
            "provider": "openai",
            "model": args.model,
            "audio_file": args.audio_file,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }
        print(json.dumps(metadata, indent=2, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
