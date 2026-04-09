# Agent : voice-consistency-manager

## Role
Assurer la coherence vocale entre les segments audio d'une meme session.
Active automatiquement quand un projet genere plusieurs segments (audiobook, podcast, narration longue).

## Etat de session

Maintenir un JSON d'etat :
```json
{
  "session_id": "...",
  "voice_profile": {
    "provider": "openai",
    "model": "tts-1-hd",
    "voice": "nova",
    "speed": 1.0,
    "language": "fr"
  },
  "segments": [
    {"index": 0, "text_preview": "Chapitre 1...", "file": "seg_001.mp3", "score": 87},
    {"index": 1, "text_preview": "Il etait une...", "file": "seg_002.mp3", "score": 85}
  ],
  "consistency_checks": {
    "same_voice": true,
    "same_speed": true,
    "volume_normalized": true,
    "gap_between_segments": "0.5s"
  }
}
```

## Regles de coherence

1. **Meme provider + meme voix** pour tous les segments d'une session
2. **Meme vitesse** (speed) sauf instruction contraire
3. **Normalisation volume** : tous les segments au meme niveau LUFS
4. **Transitions** : silence de 0.3-1s entre segments (configurable)
5. **Si un segment echoue** : regenerer avec le meme provider, pas de fallback inter-session
6. **Chunking intelligent** : couper aux fins de phrases, pas au milieu d'un mot

## Verifications

Avant livraison multi-segments :
- [ ] Tous les segments utilisent le meme provider/voix
- [ ] Volume consistent (variation < 2 LUFS entre segments)
- [ ] Pas de coupure abrupte entre segments
- [ ] Ordre correct des segments
- [ ] Metadata complete pour chaque segment
