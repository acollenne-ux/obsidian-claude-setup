#!/usr/bin/env python3
"""
hf_audio_generate.py — Wrapper HuggingFace Spaces pour generation audio IA

Supporte TTS (Kokoro, Dia, Sesame, Orpheus, F5-TTS), voice cloning (XTTS-v2, OpenVoice),
musique (MusicGen, Stable Audio), et sound effects (Tango 2, AudioLDM2).

Usage:
    python hf_audio_generate.py \
        --text "Hello world" \
        --space "kokoro" \
        --output "C:/tmp/audio-generator/session/"

    python hf_audio_generate.py \
        --text "A dramatic orchestral piece" \
        --space "musicgen" \
        --duration 15 \
        --output "C:/tmp/audio-generator/session/"
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

AI_CONFIG = Path.home() / ".claude" / "tools" / "ai_config.json"
API_KEYS = Path.home() / ".claude" / "tools" / "api_keys.json"

# Spaces pre-configures
SPACES = {
    # TTS
    "kokoro": "hexgrad/Kokoro-TTS",
    "dia": "nari-labs/Dia-1.6B",
    "sesame-csm": "sesame/csm-1b",
    "orpheus": "canopylabs/orpheus-tts",
    "f5-tts": "mrfakename/E2-F5-TTS",
    # Voice cloning
    "xtts-v2": "coqui/xtts",
    "openvoice": "myshell-ai/OpenVoiceV2",
    # Music
    "musicgen": "facebook/MusicGen",
    "stable-audio": "stabilityai/stable-audio-open-1.0",
    # Sound effects
    "tango2": "declare-lab/tango2",
    "audioldm2": "haoheliu/audioldm2-text2audio",
    # STT
    "whisper-large": "openai/whisper-large-v3",
}

# Type de tache par Space
SPACE_TYPE = {
    "hexgrad/Kokoro-TTS": "tts",
    "nari-labs/Dia-1.6B": "tts",
    "sesame/csm-1b": "tts",
    "canopylabs/orpheus-tts": "tts",
    "mrfakename/E2-F5-TTS": "tts",
    "coqui/xtts": "voice-clone",
    "myshell-ai/OpenVoiceV2": "voice-clone",
    "facebook/MusicGen": "music",
    "stabilityai/stable-audio-open-1.0": "music",
    "declare-lab/tango2": "sfx",
    "haoheliu/audioldm2-text2audio": "sfx",
    "openai/whisper-large-v3": "stt",
}


def load_hf_token():
    """Charge le token HuggingFace depuis ai_config.json ou api_keys.json."""
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
    return os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")


def generate_via_gradio(text, space, hf_token, reference_audio=None, duration=None):
    """Genere audio via gradio_client (methode principale pour les Spaces audio)."""
    try:
        from gradio_client import Client, handle_file
    except ImportError:
        raise RuntimeError("gradio_client non installe. pip install gradio_client")

    client = Client(space, hf_token=hf_token)
    start_time = time.time()

    space_type = SPACE_TYPE.get(space, "tts")

    try:
        # Adapter l'appel selon le Space
        if space == "hexgrad/Kokoro-TTS":
            result = client.predict(text, api_name="/predict")
        elif space == "nari-labs/Dia-1.6B":
            result = client.predict(text, api_name="/predict")
        elif space == "mrfakename/E2-F5-TTS":
            if reference_audio:
                result = client.predict(
                    ref_audio_input=handle_file(reference_audio),
                    gen_text_input=text,
                    api_name="/predict",
                )
            else:
                result = client.predict(text, api_name="/predict")
        elif space == "coqui/xtts":
            if not reference_audio:
                raise RuntimeError("XTTS-v2 necessite un audio de reference (--reference-audio)")
            result = client.predict(
                text,
                handle_file(reference_audio),
                api_name="/predict",
            )
        elif space == "myshell-ai/OpenVoiceV2":
            if not reference_audio:
                raise RuntimeError("OpenVoice necessite un audio de reference (--reference-audio)")
            result = client.predict(
                text,
                handle_file(reference_audio),
                api_name="/predict",
            )
        elif space == "facebook/MusicGen":
            result = client.predict(
                text,
                duration or 10,
                api_name="/predict",
            )
        elif space == "stabilityai/stable-audio-open-1.0":
            result = client.predict(
                text,
                duration or 10,
                api_name="/predict",
            )
        elif space in ("declare-lab/tango2", "haoheliu/audioldm2-text2audio"):
            result = client.predict(text, api_name="/predict")
        else:
            # Appel generique
            result = client.predict(text, api_name="/predict")

        elapsed = int((time.time() - start_time) * 1000)

        # Gerer differents types de resultats
        if isinstance(result, str) and os.path.exists(result):
            with open(result, "rb") as f:
                return f.read(), elapsed
        elif isinstance(result, tuple):
            # Certains Spaces retournent (sample_rate, audio_array) ou (filepath, ...)
            for item in result:
                if isinstance(item, str) and os.path.exists(item):
                    with open(item, "rb") as f:
                        return f.read(), elapsed
            # Si c'est (sample_rate, numpy_array), sauvegarder en wav
            if len(result) == 2:
                try:
                    import soundfile as sf
                    import numpy as np
                    import io
                    sr, audio = result
                    if isinstance(audio, (list, tuple)):
                        audio = np.array(audio)
                    buf = io.BytesIO()
                    sf.write(buf, audio, sr, format="WAV")
                    return buf.getvalue(), elapsed
                except Exception:
                    pass
        elif isinstance(result, dict) and "audio" in result:
            if os.path.exists(result["audio"]):
                with open(result["audio"], "rb") as f:
                    return f.read(), elapsed

        raise RuntimeError(f"Resultat inattendu de {space}: {type(result)}")

    except Exception as e:
        if "No API" in str(e) or "api_name" in str(e):
            # Essayer sans api_name
            try:
                result = client.predict(text)
                elapsed = int((time.time() - start_time) * 1000)
                if isinstance(result, str) and os.path.exists(result):
                    with open(result, "rb") as f:
                        return f.read(), elapsed
            except Exception:
                pass
        raise


def generate_via_inference_api(text, space, hf_token):
    """Fallback: genere via l'API Inference HF (pour les modeles qui le supportent)."""
    import urllib.request
    import urllib.error

    api_url = f"https://router.huggingface.co/hf-inference/models/{space}"

    payload = {"inputs": text}
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json",
        "Accept": "audio/flac",
    }

    json_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(api_url, data=json_data, headers=headers, method="POST")

    start_time = time.time()
    max_retries = 3

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                content_type = response.headers.get("Content-Type", "")
                data = response.read()

                if "audio" in content_type:
                    elapsed = int((time.time() - start_time) * 1000)
                    return data, elapsed

                try:
                    json_resp = json.loads(data.decode("utf-8"))
                    if "error" in json_resp:
                        error_msg = json_resp["error"]
                        if "loading" in str(error_msg).lower():
                            wait = json_resp.get("estimated_time", 15)
                            print(f"[HF-Audio] Modele en chargement, attente {wait:.0f}s...",
                                  file=sys.stderr)
                            time.sleep(min(wait, 60))
                            continue
                        raise RuntimeError(f"Erreur HF API: {error_msg}")
                except json.JSONDecodeError:
                    elapsed = int((time.time() - start_time) * 1000)
                    return data, elapsed

        except urllib.error.HTTPError as e:
            if e.code in (503, 429):
                print(f"[HF-Audio] HTTP {e.code}, retry {attempt+1}/{max_retries}...",
                      file=sys.stderr)
                time.sleep(15)
                continue
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Erreur HTTP {e.code}: {body[:500]}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Erreur connexion: {e.reason}")

    raise RuntimeError(f"Echec apres {max_retries} tentatives")


def resolve_space(space_name):
    """Resout un alias de Space ou retourne le nom tel quel."""
    return SPACES.get(space_name, space_name)


def main():
    parser = argparse.ArgumentParser(description="Generate audio via HuggingFace Spaces")
    parser.add_argument("--text", required=True, help="Texte ou prompt audio")
    parser.add_argument("--space", default="kokoro",
                        help="Space HF ou alias (kokoro, dia, musicgen, tango2, etc.)")
    parser.add_argument("--reference-audio", default=None,
                        help="Fichier audio de reference (pour voice cloning)")
    parser.add_argument("--duration", type=int, default=None,
                        help="Duree cible en secondes (pour musique/SFX)")
    parser.add_argument("--output", required=True, help="Dossier de sortie")
    parser.add_argument("--prefix", default="hf_audio", help="Prefixe fichiers")
    parser.add_argument("--method", default="gradio", choices=["gradio", "api"],
                        help="Methode d'appel (gradio ou api)")
    parser.add_argument("--consent-confirmed", action="store_true",
                        help="Confirme le consentement pour voice cloning")

    args = parser.parse_args()

    # Verifier consentement pour voice cloning
    space = resolve_space(args.space)
    space_type = SPACE_TYPE.get(space, "tts")

    if space_type == "voice-clone" and not args.consent_confirmed:
        print("ERREUR: Voice cloning necessite --consent-confirmed pour confirmer "
              "le consentement du proprietaire de la voix.", file=sys.stderr)
        sys.exit(1)

    # Charger le token
    hf_token = load_hf_token()
    if not hf_token:
        print("WARNING: Token HuggingFace non trouve. Certains Spaces peuvent etre inaccessibles.",
              file=sys.stderr)

    # Creer le dossier de sortie
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[HF-Audio] Generation via {space} (type={space_type})...", file=sys.stderr)

    try:
        if args.method == "gradio":
            audio_data, elapsed_ms = generate_via_gradio(
                args.text, space, hf_token,
                reference_audio=args.reference_audio,
                duration=args.duration,
            )
        else:
            audio_data, elapsed_ms = generate_via_inference_api(
                args.text, space, hf_token
            )

        # Determiner le format
        ext = "wav"
        if audio_data[:4] == b"fLaC":
            ext = "flac"
        elif audio_data[:3] == b"ID3" or audio_data[:2] == b"\xff\xfb":
            ext = "mp3"
        elif audio_data[:4] == b"OggS":
            ext = "ogg"

        filename = f"{args.prefix}.{ext}"
        filepath = output_dir / filename
        filepath.write_bytes(audio_data)

        result = {
            "file": filename,
            "path": str(filepath),
            "provider": "huggingface",
            "space": space,
            "type": space_type,
            "time_ms": elapsed_ms,
            "status": "success",
            "size_bytes": len(audio_data),
            "format": ext,
        }

        print(f"[HF-Audio] Sauvegarde: {filepath} ({len(audio_data)} bytes, {elapsed_ms}ms)",
              file=sys.stderr)

    except Exception as e:
        result = {
            "file": None,
            "provider": "huggingface",
            "space": space,
            "type": space_type,
            "status": "error",
            "error": str(e),
        }
        print(f"[HF-Audio] ERREUR: {e}", file=sys.stderr)

    # Metadata
    metadata = {
        "provider": "huggingface",
        "space": space,
        "type": space_type,
        "text": args.text[:500] + ("..." if len(args.text) > 500 else ""),
        "reference_audio": args.reference_audio,
        "duration": args.duration,
        "result": result,
        "timestamp": datetime.now().isoformat(),
    }

    meta_path = output_dir / f"{args.prefix}_metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(metadata, indent=2, ensure_ascii=False))

    if result["status"] == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()
