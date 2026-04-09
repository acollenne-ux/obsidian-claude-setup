# Audio Providers — Reference

## Rankings Qualite TTS (MOS — Mean Opinion Score, 2025-2026)

| Rang | Modele | MOS | Type | Latence | Langues |
|------|--------|-----|------|---------|---------|
| 1 | Sesame CSM | 4.7 | Open-source (HF) | ~5s | EN |
| 2 | Orpheus | 4.6 | Open-source (HF) | ~5s | EN |
| 3 | Dia 1.6B | ~4.4 | Open-source (HF) | ~3s | EN (dialogue) |
| 4 | ElevenLabs | ~4.3 | Commercial API | <1s | 70+ |
| 5 | Cartesia Sonic | ~4.3 | Commercial API | 95ms | 15 |
| 6 | Kokoro-82M | 4.2 | Open-source Apache | <0.3s | EN |
| 7 | F5-TTS | 4.1 | Open-source (HF) | ~3s | Multi |
| 8 | OpenAI TTS | ~4.0 | API | ~1s | Multi |

## Techniques Cles 2025-2026

### Flow Matching > Diffusion
- Transformation directe bruit→audio (transport optimal)
- Training plus stable, meilleure generalisation
- Sampling plus rapide que la diffusion iterative
- Exemples : FlashAudio, MaskGCT, F5-TTS

### State Space Models (Mamba) > Transformers
- Scaling lineaire vs quadratique
- Ideal pour le streaming audio temps reel
- Cartesia Sonic = premiere implementation production
- Pauses, interruptions, respiration naturelles

### Neural Codecs
- **DAC** > EnCodec (meilleure qualite audio)
- **SpectroStream** : meilleur 2025 (76.3% preference vs DAC)
- Residual Vector Quantization (RVQ)

### MaskGCT (ICLR 2025)
- Fully non-autoregressif (tous tokens en parallele)
- Pas besoin d'alignement texte-parole explicite
- State-of-the-art zero-shot (100K heures d'entrainement)

## Providers Configures

### OpenAI TTS
- **Endpoint** : POST https://api.openai.com/v1/audio/speech
- **Modeles** : tts-1 ($15/1M chars), tts-1-hd ($30/1M chars)
- **Voix** : alloy, echo, fable, onyx, nova, shimmer
- **Max** : 4096 chars/requete
- **Config** : ai_config.json provider "openai"

### OpenAI Whisper (STT)
- **Endpoint** : POST https://api.openai.com/v1/audio/transcriptions
- **Modeles** : whisper-1, gpt-4o-transcribe
- **Max** : 25MB/fichier
- **Tarif** : $0.006/minute

### HuggingFace Spaces (gratuits)
- **Kokoro** : hexgrad/Kokoro-TTS — TTS rapide
- **Dia** : nari-labs/Dia-1.6B — dialogue/audiobook
- **Sesame CSM** : sesame/csm-1b — haute fidelite
- **Orpheus** : canopylabs/orpheus-tts — expressif
- **F5-TTS** : mrfakename/E2-F5-TTS — flow matching
- **XTTS-v2** : coqui/xtts — voice cloning 16 langues
- **OpenVoice** : myshell-ai/OpenVoiceV2 — cloning temps reel
- **MusicGen** : facebook/MusicGen — musique conditionnee
- **Stable Audio** : stabilityai/stable-audio-open-1.0 — instrumental
- **Tango 2** : declare-lab/tango2 — effets sonores
- **AudioLDM2** : haoheliu/audioldm2-text2audio — audio general
