---
name: audio-generator
description: "Audio IA multi-provider (TTS, voice clone, musique, SFX, STT). Use when: audio, TTS, voix, musique, podcast, narration, transcription, SFX, voiceover."
argument-hint: "texte a lire ou prompt audio"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - TodoWrite
  - WebSearch
  - WebFetch
  - "mcp__claude_ai_Hugging_Face__dynamic_space"
  - "mcp__claude_ai_Hugging_Face__space_search"
  - "mcp__claude_ai_Hugging_Face__hub_repo_search"
---

# audio-generator — Generation Audio IA Multi-Provider

Skill L3 SPECIALIST pour la generation audio a partir de texte/prompts. Route intelligemment vers le meilleur provider selon le type de tache (TTS, voice cloning, musique, SFX, STT).

---

## POSITIONNEMENT ARBORESCENCE

```
L0 deep-research
 +-- L1 brainstorming
     +-- L3 audio-generator (SPECIALIST -- generation audio IA)  <-- CE SKILL
         +-- L4 audio-studio (DELIVERY -- mixage, mastering, export)
```

**Chainement amont** : deep-research, audio-studio
**Chainement aval** : audio-studio (si composition multi-pistes)

**Declencheurs auto** : "genere un audio", "lis ce texte", "TTS", "text-to-speech", "voix", "synthese vocale", "narration", "musique IA", "sound effects", "bruitage", "podcast", "audiobook", "jingle", "transcris", "speech-to-text", "voiceover", "clone voix"

---

## HARD-GATES

<HARD-GATE>
1. **TOUJOURS passer par l'agent `audio-prompt-architect`** avant envoi au provider
2. **TOUJOURS sauvegarder** dans `C:/tmp/audio-generator/<session>/` avec metadata JSON
3. **TOUJOURS declarer** le provider utilise, le modele et les parametres dans metadata
4. **TOUJOURS valider via `audio-quality-scorer`** avant livraison (sauf mode draft)
5. **JAMAIS generer de voix clonee** sans consentement explicite documente (`--consent-confirmed`)
6. **TOUJOURS verifier** la taille fichier avant export (limite 50MB par fichier audio)
7. **Si multi-segments** dans une session : TOUJOURS activer `voice-consistency-manager`
</HARD-GATE>

---

## PIPELINE 5 PHASES

### Phase 1 — Analyse du Brief

Analyser la demande et classifier :

```
AUDIO BRIEF — [titre]

Type de tache    : [tts | voice-clone | music | sfx | stt]
Langue           : [fr | en | multi | auto-detect]
Format cible     : [mp3 | wav | ogg | flac | aac] (defaut: mp3)
Duree estimee    : [courte <30s | moyenne 30s-5m | longue >5m]
Voix/style       : [masculine | feminine | neutre | specifique]
Mood/atmosphere  : [calm | energetic | dramatic | warm | professional | ...]
Multi-speaker    : [oui/non — si oui, nombre de locuteurs]
Reference audio  : [fichier reference fourni ? Pour voice cloning]
Mode qualite     : [draft | standard | best] (defaut: standard)
```

**Classification automatique du type :**
| Mots-cles detectes | Type |
|---------------------|------|
| lis, parle, dicte, narration, voix, TTS, voiceover | tts |
| clone, imite, meme voix, copie voix, reference audio | voice-clone |
| musique, chanson, jingle, melodie, beat, instrumental | music |
| bruitage, effet sonore, SFX, ambiance, sound effect | sfx |
| transcris, sous-titres, dictee, STT, speech-to-text | stt |

### Phase 2 — Prompt Rewriting (Agent `audio-prompt-architect`)

Invoquer l'agent `audio-prompt-architect` :

```markdown
## INPUT pour audio-prompt-architect
- Brief brut : [texte/prompt utilisateur]
- Type : [classification Phase 1]
- Langue : [langue cible]
- Voix/style : [preferences]
- Provider cible : [determine par la matrice de routage]

## OUTPUT attendu
- Texte/prompt optimise pour le provider
- Parametres techniques (voice, speed, format, model)
- Instructions SSML si applicable (OpenAI, Google)
```

### Phase 3 — Routage + Generation

#### 3A — Matrice de Routage

| Type de tache | Provider primaire | Provider secondaire | Fallback | Raison |
|---|---|---|---|---|
| **TTS standard** (en/fr/multi) | OpenAI TTS-HD | Kokoro-82M (HF) | Edge-TTS (gratuit) | OpenAI = meilleur rapport qualite/cout |
| **TTS dialogue/audiobook** | Dia 1.6B (HF) | OpenAI TTS | Kokoro-82M (HF) | Dia = tags non-verbaux, multi-speaker |
| **TTS haute fidelite** | Sesame CSM (HF) | Orpheus (HF) | OpenAI TTS-HD | MOS 4.7 et 4.6 |
| **Voice cloning** | XTTS-v2 (HF) | OpenVoice (HF) | F5-TTS (HF) | XTTS-v2 = 16 langues, 6s reference |
| **Musique** | MusicGen (HF) | Stable Audio (HF) | — | MusicGen = open-source, controllable |
| **Sound effects** | Tango 2 (HF) | AudioLDM2 (HF) | — | Tango 2 = 3.99 MOS, DPO-aligned |
| **Speech-to-text** | OpenAI Whisper API | Whisper Large v3 (HF) | Groq Whisper | Whisper = meilleure precision |
| **TTS rapide/draft** | Kokoro-82M (HF) | OpenAI tts-1 | Edge-TTS | Kokoro = sub-0.3s, gratuit |

**Optimisation cout** : textes courts (<500 chars) → OpenAI API, textes longs (>500 chars) → HF Spaces gratuit (Kokoro/Dia)

#### 3B — Modes Qualite

| Mode | Providers appeles | Variantes | Temps estime |
|------|-------------------|-----------|-------------|
| **draft** | 1 (primaire) | 1 | 3-10s |
| **standard** | 2 (primaire + secondaire) | 2 | 10-30s |
| **best** | 3 (tous) | 3 | 30-90s |

#### 3C — Execution

Pour chaque provider selectionne, appeler le script correspondant :

```bash
# OpenAI TTS
python "C:/Users/Alexandre collenne/.claude/skills/audio-generator/scripts/openai_tts.py" \
  --text "Texte a lire" \
  --voice "nova" \
  --model "tts-1-hd" \
  --format "mp3" \
  --speed 1.0 \
  --output "C:/tmp/audio-generator/<session>/"

# HuggingFace Spaces (Kokoro, Dia, MusicGen, Tango2, etc.)
python "C:/Users/Alexandre collenne/.claude/skills/audio-generator/scripts/hf_audio_generate.py" \
  --text "Texte a lire" \
  --space "kokoro" \
  --output "C:/tmp/audio-generator/<session>/"

# OpenAI Whisper (STT)
python "C:/Users/Alexandre collenne/.claude/skills/audio-generator/scripts/openai_stt.py" \
  --audio-file "C:/tmp/input.mp3" \
  --language "fr" \
  --format "text" \
  --output "C:/tmp/audio-generator/<session>/"
```

**Fallback cascade** : si un provider echoue → passer au suivant. Logger l'echec dans metadata.json.

### Phase 4 — Scoring Qualite (Agent `audio-quality-scorer`)

Invoquer l'agent `audio-quality-scorer` :

```markdown
## INPUT pour audio-quality-scorer
- Fichiers audio generes : [liste des fichiers]
- Texte/prompt original : [prompt utilisateur]
- Type : [classification]

## OUTPUT attendu
- Score /100 par audio (10 criteres x 10 points)
- Classement des audios
- Defauts detectes (artefacts, bruit, intonation incorrecte)
```

**Criteres de scoring** :
1. Clarte / intelligibilite (10 pts)
2. Naturalite de la voix (10 pts)
3. Absence d'artefacts (10 pts)
4. Absence de bruit (10 pts)
5. Rythme / debit adapte (10 pts)
6. Intonation / prosodie (10 pts)
7. Emotion / expressivite (10 pts)
8. Fidelite au prompt (10 pts)
9. Qualite technique (bitrate, format) (10 pts)
10. Coherence globale (10 pts)

**Seuils** :
- Score >= 75/100 → livrable
- Score 50-74 → avertissement + proposition de regenerer
- Score < 50 → regenerer automatiquement (max 2 tentatives)

### Phase 5 — Selection + Livraison

1. **Selectionner** le meilleur audio (score quality-scorer)
2. **Sauvegarder** dans `C:/tmp/audio-generator/<session>/selected_best.<format>`
3. **Generer metadata.json** :
   ```json
   {
     "session_id": "...",
     "timestamp": "2026-04-10T...",
     "user_prompt": "texte original",
     "type": "tts",
     "language": "fr",
     "mode": "standard",
     "providers_used": [
       {
         "name": "openai",
         "model": "tts-1-hd",
         "voice": "nova",
         "prompt_sent": "texte optimise",
         "params": {"speed": 1.0, "format": "mp3"},
         "files": ["openai_v1.mp3"],
         "scores": [85],
         "time_ms": 3200,
         "status": "success"
       }
     ],
     "selected": {
       "file": "openai_v1.mp3",
       "provider": "openai",
       "score": 85,
       "reason": "Meilleure naturalite, prosodie francaise correcte"
     }
   }
   ```
4. **Si appele par audio-studio** : retourner le chemin du fichier pour integration
5. **Si appele directement** : presenter l'audio + metadata a l'utilisateur

---

## PROVIDERS — DETAILS TECHNIQUES

### OpenAI TTS — via API directe

**Endpoint** : `POST https://api.openai.com/v1/audio/speech`
**Modeles** : `tts-1` (standard, rapide), `tts-1-hd` (haute qualite)
**Voix** : alloy, echo, fable, onyx, nova, shimmer
**Formats** : mp3, opus, aac, flac, wav, pcm
**Cle** : dans `ai_config.json` (provider "openai")
**Tarifs** : $15/1M chars (tts-1), $30/1M chars (tts-1-hd)
**Langues** : multilingue (auto-detection)
**Limites** : 4096 chars max par requete

### OpenAI Whisper — via API directe

**Endpoint** : `POST https://api.openai.com/v1/audio/transcriptions`
**Modeles** : `whisper-1`, `gpt-4o-transcribe`
**Formats input** : mp3, mp4, mpeg, mpga, m4a, wav, webm (max 25MB)
**Tarifs** : $0.006/minute

### Kokoro-82M (HuggingFace Space)

**Space** : `hexgrad/Kokoro-TTS`
**Architecture** : 82M params, Apache 2.0
**MOS** : 4.2 (rivalise ElevenLabs)
**Latence** : sub-0.3s
**Langues** : anglais principalement
**Forces** : ultra-rapide, gratuit, leger

### Dia 1.6B (HuggingFace Space)

**Space** : `nari-labs/Dia-1.6B`
**Architecture** : 1.6B params
**MOS** : ~4.4
**Forces** : dialogue multi-speaker, tags non-verbaux (laughs), (coughs), (gasps)
**Langues** : anglais
**Ideal pour** : audiobooks, dialogues, podcasts

### Sesame CSM (HuggingFace Space)

**Space** : `sesame/csm-1b`
**MOS** : 4.7 (meilleur open-source actuel)
**Forces** : naturalite exceptionnelle
**Langues** : anglais

### XTTS-v2 (HuggingFace Space)

**Space** : `coqui/xtts`
**Architecture** : zero-shot voice cloning, 6s reference audio
**Langues** : 16 (en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh, ja, hu, ko)
**Forces** : clonage voix multilingue, preservation emotion

### MusicGen (HuggingFace Space)

**Space** : `facebook/MusicGen`
**Architecture** : 3.9B params (Meta)
**Forces** : musique conditionnee par texte, controllable
**Duree** : jusqu'a 30s par generation

### Tango 2 (HuggingFace Space)

**Space** : `declare-lab/tango2`
**MOS** : 3.99 (meilleur SFX)
**Architecture** : DPO-aligned text-to-audio
**Forces** : sons humains, animaux, effets naturels/artificiels

---

## INTEGRATION AVEC L'ECOSYSTEME

### Appel depuis audio-studio
```
audio-studio Phase 2 (Asset Intake)
  → Detecte besoin de generation audio
  → Invoque audio-generator avec le brief
  → Recupere le fichier audio genere
  → Continue Phase 3 (Arrangement)
```

### Appel depuis deep-research
```
deep-research Phase 1 (Classification)
  → Detecte mots-cles audio generation
  → Dispatch vers audio-generator (L3 SPECIALIST)
  → audio-generator produit l'audio
  → Optionnel: audio-studio compose le livrable final (L4 DELIVERY)
```

### Appel direct
L'utilisateur dit "lis ce texte" ou "genere un audio" → audio-generator execute directement son pipeline 5 phases.

---

## ANTI-PATTERNS

| Interdit | Correct |
|----------|---------|
| Generer sans passer par audio-prompt-architect | TOUJOURS optimiser le prompt/texte |
| Utiliser un seul provider en mode standard | TOUJOURS au moins 2 providers |
| Livrer sans scoring qualite | TOUJOURS valider via audio-quality-scorer |
| Cloner une voix sans consentement | TOUJOURS --consent-confirmed |
| Ignorer les metadata | TOUJOURS sauvegarder le JSON complet |
| Hardcoder les cles API | TOUJOURS lire depuis ai_config.json |
| Envoyer un texte >4096 chars a OpenAI | TOUJOURS chunker le texte |

---

## LIVRABLE FINAL
- **Type** : audio (mp3/wav/flac)
- **Genere par** : audio-generator (scripts Python + API/HF Spaces)
- **Destination** : `C:/tmp/audio-generator/<session>/` + metadata JSON
- **Aval optionnel** : audio-studio pour composition multi-pistes

## CHAINAGE ARBORESCENCE
- **Amont** : deep-research (entree unique) → brainstorming → audio-generator
- **Aval** : audio-studio (L4 DELIVERY), qa-pipeline (L5 QA)

## CROSS-LINKS

| Contexte | Skill a invoquer |
|----------|-----------------|
| Composition multi-pistes | `audio-studio` (L4) |
| Scoring qualite | `qa-pipeline` (L5) |
| Generation d'images pour accompagner | `image-generator` (L3) |
| Rapport PDF des resultats | `pdf-report-pro` (L4) |
| Envoi email du livrable | `send_report.py` |
| Feedback utilisateur | `feedback-loop` (L6) |
| Retex post-session | `retex-evolution` (L6) |

## EVOLUTION

Apres chaque utilisation :
1. **Trigger accuracy** : le skill s'est-il active correctement ? Si < 80% → revoir description
2. **Output quality** : score moyen audio-quality-scorer. Si < 75 → ajuster routing table
3. **Provider reliability** : tracker les echecs par provider → ajuster les priorites
4. **Nouveaux providers** : surveiller les Spaces HF emergents (MOS > 4.5) → ajouter au routing
5. **Enregistrer via** `retex-evolution` : `--quality X --tools-used "audio-generator" --notes "..."`

## MONITORING

```
[AUDIO-GEN] Phase 1 — Brief analyse : type={type}, langue={lang}, mode={mode}
[AUDIO-GEN] Phase 2 — Prompt rewrite : {provider} → {longueur} chars
[AUDIO-GEN] Phase 3 — Generation : {provider} → {status} en {time}ms
[AUDIO-GEN] Phase 4 — Score : {file} → {score}/100
[AUDIO-GEN] Phase 5 — Selected : {best_file} ({provider}, score={score})
```
