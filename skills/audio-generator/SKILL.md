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

#### 3A — Matrice de Routage (mise a jour avril 2026)

| Type de tache | Provider primaire | Provider secondaire | Fallback | Raison |
|---|---|---|---|---|
| **TTS standard** (en/fr/multi) | Qwen3-TTS 1.7B (HF, gratuit, FR) | OpenAI TTS-HD | Kokoro-82M (HF) / Edge-TTS | Qwen3 = multi-langue + voice design + gratuit |
| **TTS dialogue/audiobook** | Dia 1.6B (HF) | Qwen3-TTS (HF) | Kokoro-82M (HF) | Dia = tags non-verbaux, multi-speaker en 1 pass |
| **TTS haute fidelite** | Qwen3-TTS 1.7B (HF) | F5-TTS (HF) | Dia 1.6B (HF) | Qwen3 1.7B = qualite + multi-langue ; F5 = MOS ~4.5 |
| **Voice cloning** | Qwen3-TTS clone (HF) | F5-TTS (HF) | OpenVoice V2 (HF) | Qwen3 = clone multi-langue ; F5 = meilleur zero-shot Apache 2.0 |
| **Musique** | Tencent SongGeneration V2 (HF, 4B) | UnlimitedMusicGen (HF) | -- | Tencent = chansons avec paroles ; MusicGen = instrumentaux illimites |
| **Sound effects** | UnlimitedMusicGen (HF) | Edge-TTS + numpy synth | -- | Tango2/AudioLDM2 DOWN ; MusicGen peut faire SFX basiques |
| **Speech-to-text** | OpenAI Whisper API | Whisper Large v3 (HF) | Groq Whisper | Whisper = meilleure precision |
| **TTS rapide/draft** | Kokoro-82M (HF) | Edge-TTS (HF/local) | OpenAI tts-1 | Kokoro = sub-0.3s, 82M params, gratuit |

**Providers DOWN avril 2026** : Sesame CSM (ConfigError), Orpheus (401), MusicGen original (numpy crash), Stable Audio (401), Tango 2 (ConfigError), AudioLDM2 (401), Fish Speech HF (torchaudio crash)

**Providers proprietaires premium** (si budget disponible) :
- Fish Audio S2 Pro : #1 TTS Arena (ELO 1339), 80+ langues, API REST, ~$0.80/h
- ElevenLabs v3 : leader qualite absolue, 70+ langues, SFX V2 48kHz
- Cartesia Sonic 3 : 40ms latence, 73% moins cher qu'ElevenLabs
- Voxtral TTS (Mistral) : 68.4% win vs ElevenLabs Flash, 9 langues dont FR, API $0.016/1K chars

**Optimisation cout** : TOUJOURS privilegier les HF Spaces gratuits (Qwen3-TTS, Dia, F5-TTS, Kokoro). OpenAI TTS-HD en seconde intention. Providers premium uniquement si demande explicite de qualite maximale.

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

## PROVIDERS — DETAILS TECHNIQUES (mise a jour avril 2026)

### TIER 1 — Gratuits / HF Spaces actifs

#### Qwen3-TTS (HuggingFace Space) — NOUVEAU, PRIORITAIRE

**Space** : `Qwen/Qwen3-TTS`
**Architecture** : 0.6B et 1.7B params, Apache 2.0
**Langues** : 10 (Auto, Chinese, English, Japanese, Korean, French, German, Spanish, Portuguese, Russian)
**Modes** : Voice Design (decrire la voix), Voice Clone (audio reference), Custom Voice (voix predefinies)
**Voix predefinies** : Aiden, Dylan, Eric, Ono_anna, Ryan, Serena, Sohee, Uncle_fu, Vivian
**Forces** : multi-mode, francais natif, voice cloning inclus, gratuit
**API HF** : `fn_index=0` (voice design), `fn_index=1` (voice clone), `fn_index=2` (custom voice)

#### Dia 1.6B (HuggingFace Space)

**Space** : `nari-labs/Dia-1.6B`
**Architecture** : 1.6B params, Apache 2.0
**MOS** : ~4.5-4.7 (surpasse CSM sur dialogues)
**Forces** : dialogue multi-speaker en 1 pass, tags non-verbaux (laughs), (coughs), (gasps), (sighs)
**Langues** : anglais
**API HF** : `api_name="/generate_audio"` avec 8 parametres (cfg_scale, temperature, top_p, etc.)
**Ideal pour** : audiobooks, dialogues, podcasts

#### F5-TTS (HuggingFace Space)

**Space** : `mrfakename/E2-F5-TTS`
**Architecture** : 336M params, Apache 2.0
**MOS** : ~4.3-4.5 ("le plus realiste open-source" — Uberduck)
**Forces** : voice cloning zero-shot excellence, flow matching, code-switching EN/ZH
**Langues** : EN, ZH natif + FR, DE, IT, JA (fine-tuned communaute)
**Modes** : TTS simple, podcast generation (2 voix), emotional speech

#### Kokoro-82M (HuggingFace Space)

**Space** : `hexgrad/Kokoro-TTS`
**Architecture** : 82M params, Apache 2.0, base StyleTTS2
**MOS** : 4.2 (#1 open-source a taille comparable)
**Latence** : RTF 0.03 GPU (10s audio en 0.3s)
**Langues** : 8 (EN-US, EN-GB, FR, JA, KO, ZH, +)
**Voix** : 54 voix, 10 voicepacks
**Forces** : ultra-rapide, ultra-leger, ONNX browser

#### OpenVoice V2 (HuggingFace Space)

**Space** : `myshell-ai/OpenVoiceV2`
**Licence** : MIT
**Langues** : 6 (en, zh, ja, ko, es, fr)
**Forces** : voice cloning cross-lingue zero-shot
**API** : style + audio reference + speed

#### Tencent SongGeneration V2 (HuggingFace Space) — NOUVEAU

**Space** : `tencent/SongGeneration`
**Architecture** : 4B params (V2, mars 2026)
**Forces** : chansons completes avec paroles (lyrics tags : [verse], [chorus], [bridge])
**Genres** : Pop, Rock, Jazz, Hip-Hop, Electronic, Classical, R&B, Country, Folk, Latin, Metal
**API** : lyric + description + genre + cfg_coef + temperature

#### UnlimitedMusicGen (HuggingFace Space) — NOUVEAU

**Space** : `Surn/UnlimitedMusicGen`
**Architecture** : MusicGen (Meta) avec extension duree illimitee via overlap
**Forces** : instrumentaux sans limite de duree, modeles small/medium/large/melody
**API** : `api_name="/predict_simple"` avec model, text, duration, topk, temperature, overlap

#### Edge-TTS (HuggingFace Space + local)

**Space** : `innoai/Edge-TTS-Text-to-Speech`
**Local** : `pip install edge-tts` (gratuit, sans API key)
**Langues** : 50+ langues, centaines de voix Microsoft
**Forces** : zero-cost, ultra-rapide, voix naturelles Microsoft
**Ideal pour** : fallback universel, drafts, textes longs

### TIER 2 — Payants / APIs proprietaires

#### OpenAI TTS — via API directe

**Endpoint** : `POST https://api.openai.com/v1/audio/speech`
**Modeles** : `tts-1` (standard), `tts-1-hd` (haute qualite), `gpt-4o-mini-tts` (steerable)
**Voix** : alloy, echo, fable, onyx, nova, shimmer (+ 12 voix gpt-4o-mini-tts)
**Tarifs** : $15/1M chars (tts-1), $30/1M chars (tts-1-hd)
**Limites** : 4096 chars max par requete

#### Fish Audio S2 Pro (API REST) — NOUVEAU

**API** : REST API (fish.audio)
**ELO** : 1339 (TTS Arena V1 #1), 81.88% EmergentTTS win rate
**Langues** : 80+ (cross-lingual)
**Forces** : #1 Audio Turing Test, voice cloning 15-30s
**Tarifs** : Gratuit (limite), Plus $5.50/mo, Pro $37.50/mo (~$0.80/h)

#### Voxtral TTS — Mistral (API) — NOUVEAU

**API** : Mistral API ($0.016/1K chars)
**Architecture** : 4B params, open-weight CC BY-NC
**Win rate** : 68.4% vs ElevenLabs Flash v2.5
**Langues** : 9 (en, fr, de, es, nl, pt, it, hi, ar)
**Latence** : 70ms TTFA, streaming
**Forces** : rival ElevenLabs, francais natif excellent

#### ElevenLabs v3 (API)

**ELO** : 1179 (TTS Arena #2)
**Langues** : 70+
**Forces** : leader qualite absolue, SFX V2 48kHz, voice cloning pro
**Tarifs** : Free 10K credits/mois, Starter $5, Pro $99, Scale $330/mo

#### Cartesia Sonic 3 (API)

**Latence** : 40ms (Turbo)
**Langues** : 15
**Forces** : ultra-low latency, emotion tags, 73% moins cher qu'ElevenLabs

### TIER 3 — DOWN / En panne (avril 2026)

| Space | Statut | Erreur |
|-------|--------|--------|
| `sesame/csm-1b` | DOWN | ConfigError ZeroGPU |
| `canopylabs/orpheus-tts` | DOWN | 401 Unauthorized |
| `facebook/MusicGen` | DOWN | RuntimeError numpy |
| `stabilityai/stable-audio-open-1.0` | DOWN | 401 Unauthorized |
| `declare-lab/tango2` | DOWN | ConfigError ZeroGPU |
| `haoheliu/audioldm2-text2audio` | DOWN | 401 Unauthorized |
| `fishaudio/fish-speech-1` | DOWN | RuntimeError torchaudio |

**Note** : PlayHT a ferme (acquis par Meta, API arretee 31/12/2025). Coqui (XTTS-v2) a ferme en dec 2025 (modele encore disponible mais non maintenu).

### OpenAI Whisper — via API directe

**Endpoint** : `POST https://api.openai.com/v1/audio/transcriptions`
**Modeles** : `whisper-1`, `gpt-4o-transcribe`
**Formats input** : mp3, mp4, mpeg, mpga, m4a, wav, webm (max 25MB)
**Tarifs** : $0.006/minute

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
