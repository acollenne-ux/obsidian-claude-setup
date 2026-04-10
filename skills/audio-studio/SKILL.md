---
name: audio-studio
description: "Studio audio : mixage, mastering, export pro. Use when: podcast, audiobook, jingle, mixer, mastering, montage audio, voiceover+musique."
argument-hint: "brief du livrable audio a produire"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - TodoWrite
  - Skill
  - WebSearch
  - WebFetch
---

# audio-studio — Studio Audio Unifie

Skill L4 DELIVERY pour la composition, le mixage, le mastering et l'export de livrables audio professionnels. Prend les elements bruts generes par `audio-generator` et produit des livrables finis.

---

## POSITIONNEMENT ARBORESCENCE

```
L0 deep-research
 +-- L1 brainstorming
     +-- L3 audio-generator (SPECIALIST)
         +-- L4 audio-studio (DELIVERY -- mixage + mastering + export)  <-- CE SKILL
             +-- L5 qa-pipeline
```

**Chainement amont** : deep-research, audio-generator
**Chainement aval** : qa-pipeline (validation), pdf-report-pro (si rapport accompagne)
**Livrable** : AUDIO (mp3 + wav)

**Declencheurs auto** : "cree un podcast", "compose un audiobook", "mixe ces audios", "ajoute musique de fond", "mastering", "montage audio", "jingle complet", "voiceover avec musique"

---

## HARD-GATES

<HARD-GATE>
1. **JAMAIS livrer** sans passage par l'agent `audio-art-director` (score >= 8/10 requis)
2. **TOUJOURS normaliser** le volume selon le type :
   - Podcast/voiceover : -16 LUFS
   - Musique : -14 LUFS
   - Broadcast : -23 LUFS
3. **TOUJOURS exporter** en au moins 2 formats (mp3 320kbps + wav 44.1kHz par defaut)
4. **JAMAIS mixer** sans verifier les niveaux de crete (max -1dBFS, pas de clipping)
5. **TOUJOURS sauvegarder** dans `C:/tmp/audio-studio/<session>/` avec metadata JSON
</HARD-GATE>

---

## PIPELINE 6 PHASES

### Phase 1 — Analyse du Brief

Classifier le type de livrable :

```
AUDIO STUDIO BRIEF — [titre]

Type livrable    : [podcast | audiobook | jingle | voiceover-music | composition | montage]
Duree cible      : [secondes ou minutes]
Pistes prevues   : [nombre de pistes / elements]
Format final     : [mp3 | wav | flac | ogg] (defaut: mp3 + wav)
Normalisation    : [LUFS cible selon type]
Transitions      : [crossfade | silence | cut]
```

### Phase 2 — Asset Intake

Collecter ou generer tous les elements audio :

1. **Elements fournis** : fichiers audio deja existants
2. **Elements a generer** : invoquer `audio-generator` (skill L3) pour chaque element manquant
   - Narration → audio-generator type=tts
   - Musique de fond → audio-generator type=music (Tencent SongGeneration ou UnlimitedMusicGen)
   - Effets sonores → audio-generator type=sfx (numpy synth ou MusicGen en fallback)
   - Jingle intro/outro → audio-generator type=music (UnlimitedMusicGen)
3. **Inventaire** : lister tous les assets avec duree, format, niveau

### Phase 3 — Arrangement

Definir la timeline du livrable :

```
TIMELINE — [titre]

00:00-00:05  [jingle_intro.mp3]     volume=100%  fade_in=1s
00:05-02:30  [narration.mp3]        volume=100%
00:05-02:30  [background_music.mp3] volume=15%   (sous la narration)
02:30-02:35  [sfx_transition.mp3]   volume=80%
02:35-05:00  [narration_part2.mp3]  volume=100%
02:35-05:00  [background_music.mp3] volume=15%
05:00-05:10  [jingle_outro.mp3]     volume=100%  fade_out=2s
```

Regles :
- Musique de fond sous narration : volume 10-20% (duck automatique)
- Transitions : crossfade 0.5-2s entre segments
- Silence entre sections : 0.5-1s

### Phase 4 — Mix / Master

Utiliser `audio_engine.py` pour :

```bash
# Normaliser chaque piste
python "C:/Users/Alexandre collenne/.claude/tools/audio_engine.py" normalize \
  --input "narration.mp3" --target-lufs -16 --output "narration_norm.wav"

# Mixer les pistes
python "C:/Users/Alexandre collenne/.claude/tools/audio_engine.py" mix \
  --tracks "narration_norm.wav:100,background_music.wav:15" \
  --output "mix.wav"

# Ajouter fade in/out
python "C:/Users/Alexandre collenne/.claude/tools/audio_engine.py" fade \
  --input "mix.wav" --fade-in 1.0 --fade-out 2.0 --output "mix_faded.wav"

# Concatener les segments
python "C:/Users/Alexandre collenne/.claude/tools/audio_engine.py" concat \
  --inputs "jingle_intro.wav,mix_faded.wav,jingle_outro.wav" \
  --gap 0.5 --output "final.wav"

# Verifier les cretes
python "C:/Users/Alexandre collenne/.claude/tools/audio_engine.py" info \
  --input "final.wav"
```

### Phase 5 — Art Direction (Agent `audio-art-director`)

Invoquer l'agent critique :

```markdown
## INPUT pour audio-art-director
- Fichier mix final : [chemin]
- Brief original : [resume]
- Timeline : [arrangement Phase 3]

## GRILLE D'EVALUATION (chaque critere /10)
1. Equilibre des niveaux entre pistes
2. Qualite des transitions (pas de coupures)
3. Rythme global (pacing adapte au contenu)
4. Clarte de la narration (voix pas noyee)
5. Ambiance musicale (musique soutient sans distraire)
6. Qualite technique (pas de clipping, bruit)
7. Coherence globale
8. Fidelite au brief
9. Impact emotionnel
10. Finition professionnelle

## SEUIL : score moyen >= 8/10
```

Si score < 8 : identifier les problemes, ajuster Phase 4, re-evaluer (max 3 iterations).

### Phase 6 — Export

1. **Exporter en WAV** (44.1kHz, 16-bit) : master lossless
2. **Exporter en MP3** (320kbps) : distribution
3. **Tags metadata** :
   - ID3v2 pour MP3 : titre, artiste, album, date
   - Vorbis pour OGG/FLAC si applicable
4. **Sauvegarder** :
   ```
   C:/tmp/audio-studio/<session>/
     final_master.wav
     final.mp3
     metadata.json
     timeline.json
     assets/  (tous les fichiers source)
   ```
5. **Rapport** : generer metadata.json avec tout le pipeline trace

---

## TYPES DE LIVRABLES

### Podcast
- Intro jingle (3-5s) + narration + transitions + outro
- Normalisation -16 LUFS
- Musique de fond a 10-15% sous la voix

### Audiobook
- Chapitres individuels + concatenation
- Pauses de 1-2s entre chapitres
- Voix consistante (voice-consistency-manager)

### Jingle
- Court (5-15s), musique + voix optionnelle
- Normalisation -14 LUFS
- Fade in/out 0.5s

### Voiceover + Musique
- Narration au premier plan
- Ducking automatique de la musique
- Normalisation -16 LUFS

---

## ANTI-PATTERNS

| Interdit | Correct |
|----------|---------|
| Livrer sans normalisation | TOUJOURS normaliser au LUFS cible |
| Mixer sans verifier les cretes | TOUJOURS max -1dBFS |
| Un seul format d'export | TOUJOURS mp3 + wav minimum |
| Ignorer l'art direction | TOUJOURS score >= 8/10 |
| Musique de fond trop forte | 10-20% max sous narration |

---

## LIVRABLE FINAL
- **Type** : audio (mp3 + wav)
- **Genere par** : audio-studio (audio_engine.py + ffmpeg)
- **Destination** : `C:/tmp/audio-studio/<session>/final/` + metadata JSON
- **Envoi** : acollenne@gmail.com via send_report.py (si applicable)

## CHAINAGE ARBORESCENCE
- **Amont** : deep-research → brainstorming → audio-generator → audio-studio
- **Aval** : qa-pipeline (L5 QA), pdf-report-pro (L4, si rapport accompagne)

## CROSS-LINKS

| Contexte | Skill a invoquer |
|----------|-----------------|
| Generation d'elements audio | `audio-generator` (L3) |
| Scoring qualite audio | `qa-pipeline` (L5) |
| Rapport PDF du projet audio | `pdf-report-pro` (L4) |
| Presentation du projet | `ppt-creator` (L4) |
| Envoi email | `send_report.py` |
| Feedback utilisateur | `feedback-loop` (L6) |
| Retex post-session | `retex-evolution` (L6) |

## EVOLUTION

Apres chaque utilisation :
1. **Art direction score** : si moyen < 8/10 → revoir les criteres ou le pipeline mix/master
2. **Format coverage** : tracker les formats demandes → ajouter si manquants
3. **Nouveaux templates** : si un type de livrable recurrent apparait → creer un template
4. **audio_engine.py** : si limitation ffmpeg → ajouter commandes ou outils alternatifs
5. **Enregistrer via** `retex-evolution` : `--quality X --tools-used "audio-studio" --notes "..."`

## MONITORING

```
[AUDIO-STUDIO] Phase 1 — Brief : type={type}, duree={duree}
[AUDIO-STUDIO] Phase 2 — Assets : {n} elements collectes/generes
[AUDIO-STUDIO] Phase 3 — Timeline : {n} segments, duree totale={total}
[AUDIO-STUDIO] Phase 4 — Mix/Master : LUFS={lufs}, peak={peak}dBFS
[AUDIO-STUDIO] Phase 5 — Art Direction : score={score}/10
[AUDIO-STUDIO] Phase 6 — Export : {formats} vers {output_dir}
```
