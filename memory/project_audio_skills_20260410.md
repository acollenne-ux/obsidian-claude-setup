---
name: Audio Skills Suite 10/04
description: Suite audio IA complète — audio-generator (L3) + audio-studio (L4) + 4 scripts + 4 agents + audio_engine.py, routage multi-provider (OpenAI TTS, HF Spaces Kokoro/Dia/Sesame/MusicGen/Tango2)
type: project
---

## Audio Generation Skills — Installés le 10/04/2026

### Nouveaux skills
- **audio-generator** (L3 SPECIALIST) — Miroir exact de image-generator pour l'audio
  - 5 phases : Analyse Brief → Prompt Rewriting → Routage + Génération → Scoring → Livraison
  - 8 types de routage : tts, tts-dialogue, tts-hifi, voice-clone, music, sfx, stt, tts-fast
  - 3 modes qualité : draft (1 provider), standard (2), best (3)
  - Scripts : openai_tts.py, openai_stt.py, hf_audio_generate.py, audio_gen_router.py
  - Agents : audio-prompt-architect, audio-quality-scorer, voice-consistency-manager

- **audio-studio** (L4 DELIVERY) — Miroir exact de image-studio pour l'audio
  - 6 phases : Brief → Asset Intake → Arrangement → Mix/Master → Art Direction → Export
  - Types : podcast, audiobook, jingle, voiceover-music, composition, montage
  - Agents : audio-art-director, brief-analyst

### Outil partagé
- `~/.claude/tools/audio_engine.py` — 8 commandes ffmpeg : info, normalize, concat, mix, fade, convert, trim, volume

### Dépendances installées
- ffmpeg 8.1 (dans Python313/Scripts/, dans PATH)
- pydub 0.25.1, soundfile 0.13.1, gradio_client 2.4.0

### Providers audio configurés
- **OpenAI TTS** : tts-1, tts-1-hd, 6 voix (nova, alloy, echo, fable, onyx, shimmer)
- **OpenAI Whisper** : whisper-1, gpt-4o-transcribe (STT)
- **HF Spaces** (gratuits) : Kokoro-82M, Dia 1.6B, Sesame CSM, Orpheus, F5-TTS, XTTS-v2, OpenVoice, MusicGen, Stable Audio, Tango 2, AudioLDM2

### Intégration arborescence
- CLAUDE.md : ligne audio ajoutée dans sélection intelligente
- deep-research : détection domaine audio + dispatch automatique
- skill-tree-manager : enregistrement L3 + L4

**Why:** Aucune capacité audio n'existait dans l'écosystème (0 skill, 0 lib, 0 MCP). Open-source a atteint la parité avec le commercial (MOS 4.7 Sesame CSM vs 4.3 ElevenLabs).
**How to apply:** Toute demande audio → audio-generator, composition multi-pistes → audio-studio. Routage intelligent selon type/langue/budget.
