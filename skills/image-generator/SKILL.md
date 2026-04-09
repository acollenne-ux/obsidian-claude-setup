---
name: image-generator
description: "Generation d'images IA text-to-image multi-provider. Route vers FLUX, GPT-Image, Nano Banana 2, SDXL selon le type de tache. Use when: generer une image, creer une illustration, image IA, text-to-image, genere moi une image, dessine, illustre, cree un visuel IA, image from text, AI image, generate image. JAMAIS utilise pour retoucher/modifier une photo reelle existante (-> image-studio/image-enhancer)."
argument-hint: "prompt de generation ou brief visuel"
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
  - "mcp__claude_ai_Canva__generate-design"
  - "mcp__claude_ai_Canva__generate-design-structured"
  - "mcp__claude_ai_Canva__export-design"
---

# image-generator — Generation d'Images IA Multi-Provider

Skill L3 SPECIALIST pour la generation d'images a partir de prompts textuels. Route intelligemment vers le meilleur provider selon le type de tache.

---

## POSITIONNEMENT ARBORESCENCE

```
L0 deep-research
 +-- L1 brainstorming
     +-- L3 image-generator (SPECIALIST -- generation IA text-to-image)  <-- CE SKILL
         +-- L4 image-studio (DELIVERY -- composition + export final)
```

**Declencheurs auto** : "genere une image", "cree une illustration", "text-to-image", "image IA", "dessine", "illustre", "genere moi", "cree un visuel IA", "generate image", "AI art", "image from text", "cree une photo de", "imagine"

---

## HARD-GATES

<HARD-GATE>
1. **JAMAIS regenerer une image reelle** fournie par l'utilisateur (faces, logos, produits) -- deleguer a `image-studio`/`image-enhancer`
2. **TOUJOURS passer par l'agent `prompt-architect`** avant d'envoyer le prompt au provider
3. **TOUJOURS sauvegarder** dans `C:/tmp/image-generator/<session>/` avec metadata JSON
4. **TOUJOURS declarer** le provider utilise et le prompt exact dans les metadata
5. **TOUJOURS proposer au moins 2 variantes** en mode standard/best (1 seule en draft)
6. **TOUJOURS valider via `quality-scorer`** avant livraison (sauf mode draft)
7. **Si multi-images dans une session** : TOUJOURS activer `style-consistency-manager`
</HARD-GATE>

---

## PIPELINE 5 PHASES

### Phase 1 — Analyse du Brief

Analyser la demande et classifier :

```
BRIEF ANALYSE — [titre]

Type d'image     : [photo | illustration | text-in-image | logo | anime | abstract | diagram]
Style desire     : [realiste | artistique | minimaliste | retro | futuriste | corporate | ...]
Texte a inclure  : [oui/non — si oui, texte exact verbatim]
Resolution cible : [512 | 1024 | 2048 | 4096] (defaut: 1024)
Ratio            : [1:1 | 16:9 | 9:16 | 4:3 | 3:2 | custom]
Mood/atmosphere  : [warm | cold | moody | bright | ethereal | dramatic | ...]
References       : [images de reference fournies ? Si oui, les analyser via Gemini vision]
Mode qualite     : [draft | standard | best] (defaut: standard)
```

**Classification automatique du type :**
| Mots-cles detectes | Type |
|---------------------|------|
| photo, realiste, photograph | photo |
| illustration, dessin, draw, artwork | illustration |
| texte, affiche, poster, soldes, titre, typographie | text-in-image |
| logo, icone, embleme, badge | logo |
| anime, manga, cartoon | anime |
| abstrait, pattern, texture, fond | abstract |

### Phase 2 — Prompt Rewriting (Agent `prompt-architect`)

Invoquer l'agent `prompt-architect` :

```markdown
## INPUT pour prompt-architect
- Brief brut : [prompt utilisateur]
- Type : [classification Phase 1]
- Style : [style desire]
- Texte a inclure : [si applicable]
- Provider cible : [determine par la matrice de routage]
- Images de reference : [analyse Gemini si fournies]

## OUTPUT attendu
- Prompt optimise pour le provider
- Prompt negatif (si FLUX/SDXL)
- Parametres techniques (CFG, steps, scheduler, resolution)
```

### Phase 3 — Routage + Generation

#### 3A — Matrice de Routage

| Type de tache | Provider primaire | Provider secondaire | Fallback | Raison |
|---|---|---|---|---|
| **photo** (realiste) | FLUX.1-dev (HF) | GPT-Image (OpenAI) | Nano Banana 2 (Gemini) | FLUX = meilleur photoralisme flow matching |
| **text-in-image** | GPT-Image (OpenAI) | Nano Banana 2 (Gemini) | FLUX.1 (HF) | GPT-Image = meilleur suivi texte (unification modale) |
| **illustration** | FLUX.1-dev (HF) | SDXL (HF) | GPT-Image (OpenAI) | FLUX + style prompt = versatile |
| **logo** | GPT-Image (OpenAI) | Canva generate-design | SDXL (HF) | Precision + editabilite |
| **anime** | SDXL anime (HF) | FLUX (HF) | GPT-Image (OpenAI) | Checkpoints anime specialises |
| **abstract** | FLUX.1 (HF) | SDXL (HF) | Nano Banana 2 (Gemini) | Creativite maximale |
| **fast** (any) | Nano Banana 2 (Gemini) | FLUX Schnell (HF) | SDXL Turbo (HF) | NB2 = ~3s, Schnell = ~5s |

#### 3B — Modes Qualite

| Mode | Providers appeles | Variantes/provider | Total images | Temps estime |
|------|-------------------|--------------------|-------------|-------------|
| **draft** | 1 (primaire) | 1 | 1 | 5-15s |
| **standard** | 2 (primaire + secondaire) | 2 | 4 | 15-45s |
| **best** | 3 (tous) | 3-4 | 9-12 | 45-120s |

#### 3C — Execution

Pour chaque provider selectionne, appeler le script correspondant :

```bash
# FLUX / SDXL via HuggingFace
python "C:/Users/Alexandre collenne/.claude/skills/image-generator/scripts/hf_generate.py" \
  --prompt "<prompt optimise>" \
  --negative "<prompt negatif>" \
  --space "black-forest-labs/FLUX.1-schnell" \
  --size 1024 \
  --variants 2 \
  --output "C:/tmp/image-generator/<session>/"

# GPT-Image / DALL-E via OpenAI
python "C:/Users/Alexandre collenne/.claude/skills/image-generator/scripts/openai_generate.py" \
  --prompt "<prompt optimise>" \
  --model "dall-e-3" \
  --size "1024x1024" \
  --quality "hd" \
  --style "natural" \
  --variants 2 \
  --output "C:/tmp/image-generator/<session>/"

# Nano Banana 2 via Gemini
python "C:/Users/Alexandre collenne/.claude/skills/image-generator/scripts/gemini_generate.py" \
  --prompt "<prompt optimise>" \
  --model "gemini-2.0-flash-exp" \
  --size "1024x1024" \
  --variants 2 \
  --output "C:/tmp/image-generator/<session>/"
```

**Parallelisation** : lancer les providers en parallele (Agent tool, background=true) quand possible.

**Fallback cascade** : si un provider echoue (timeout, rate limit, erreur) → passer au suivant automatiquement. Logger l'echec dans metadata.json.

### Phase 4 — Scoring Qualite (Agent `quality-scorer`)

Invoquer l'agent `quality-scorer` :

```markdown
## INPUT pour quality-scorer
- Images generees : [liste des fichiers PNG]
- Prompt original : [prompt utilisateur]
- Prompt optimise : [prompt envoye au provider]
- Type : [classification]

## OUTPUT attendu
- Score /100 par image (10 criteres x 10 points)
- Classement des images
- Justification du choix
- Defauts detectes (artefacts, incoherences, texte illisible)
```

**Seuil de qualite** :
- Score >= 75/100 → livrable
- Score 50-74 → avertissement + proposition de regenerer
- Score < 50 → regenerer automatiquement (max 2 tentatives)

### Phase 5 — Selection + Livraison

1. **Selectionner** la meilleure image (score quality-scorer)
2. **Sauvegarder** le resultat final dans `C:/tmp/image-generator/<session>/selected_best.png`
3. **Generer metadata.json** :
   ```json
   {
     "session_id": "...",
     "timestamp": "2026-04-09T...",
     "user_prompt": "prompt original",
     "type": "photo",
     "mode": "standard",
     "providers_used": [
       {
         "name": "flux",
         "space": "black-forest-labs/FLUX.1-schnell",
         "prompt_sent": "prompt optimise FLUX",
         "negative_prompt": "...",
         "params": {"cfg": 7.5, "steps": 28, "size": "1024x1024"},
         "variants": ["flux_v1.png", "flux_v2.png"],
         "scores": [82, 78],
         "time_ms": 12340,
         "status": "success"
       }
     ],
     "selected": {
       "file": "flux_v1.png",
       "provider": "flux",
       "score": 82,
       "reason": "Meilleur photoralisme, composition equilibree"
     },
     "style_state": null
   }
   ```
4. **Si appele par image-studio** : retourner le chemin du fichier selectionne pour integration dans le pipeline de composition
5. **Si appele directement** : afficher l'image + metadata a l'utilisateur

---

## PROVIDERS — DETAILS TECHNIQUES

### FLUX.1 (Black Forest Labs) — via HuggingFace Spaces

**Architecture** : Rectified Flow Matching, 12B params, double flux attention
**Spaces** :
- `black-forest-labs/FLUX.1-schnell` — rapide (~5s), gratuit, Apache 2.0
- `black-forest-labs/FLUX.1-dev` — qualite superieure (~15s), gratuit, non-commercial

**Forces** : photoralisme exceptionnel, textures peau, flow matching previsible
**Limites** : pas de prompt negatif natif (flow matching), queue HF variable
**Resolutions** : 512-1024px (upscale via image-enhancer si >1024 necessaire)

### GPT-Image / DALL-E 3 (OpenAI) — via API directe

**Architecture** : Transformer unifie autoregressif + diffusion (GPT-4o), unCLIP (DALL-E 3)
**Endpoint** : `POST https://api.openai.com/v1/images/generations`
**Cle** : dans `C:/Users/Alexandre collenne/.claude/tools/ai_config.json` (provider "openai")

**Forces** : meilleur texte dans l'image, meilleur suivi d'instructions, edition precise
**Limites** : censure stricte, biais chromatique chaud, ~30s/image, cout plus eleve
**Resolutions** : 1024x1024, 1024x1792, 1792x1024
**Tarifs** : $0.04 (standard) - $0.12 (HD) par image

### Nano Banana 2 / Gemini Image (Google) — via Gemini API

**Architecture** : Transformer MoE + diffusion distillee, reasoning avant rendu
**Modele API** : `gemini-2.0-flash-exp` (ou `gemini-3.1-flash-image-preview` si disponible)
**Cle** : dans `ai_config.json` (provider "gemini")

**Forces** : 4K natif, ~3-6s, coherence multi-sujets, grounding web
**Limites** : guardrails Google stricts, architecture opaque, en preview
**Resolutions** : 512, 1K, 2K, 4K
**Tarifs** : $0.045-$0.15/image

### SDXL / SD3.5 (Stability AI) — via HuggingFace Spaces

**Architecture** : MMDiT-X, 3 encodeurs texte (2x CLIP + T5-XXL)
**Spaces** :
- `stabilityai/stable-diffusion-3.5-large` — qualite
- `stabilityai/sdxl-turbo` — ultra-rapide (~2s)

**Forces** : open-source, ControlNet compatible, customisable, multi-resolution
**Limites** : qualite inferieure a FLUX/GPT-Image sur benchmarks recents
**Resolutions** : 512-2048px

---

## INTEGRATION AVEC L'ECOSYSTEME

### Appel depuis image-studio
```
image-studio Phase 2 (Asset Intake)
  → Detecte besoin de generation IA (pas de photos reelles fournies)
  → Invoque image-generator avec le brief
  → Recupere l'image generee comme "asset"
  → Continue Phase 3 (Moodboard) avec l'asset
```

### Appel depuis deep-research
```
deep-research Phase 1 (Classification)
  → Detecte mots-cles image generation
  → Dispatch vers image-generator (L3 SPECIALIST)
  → image-generator produit l'image
  → Optionnel: image-studio compose le livrable final (L4 DELIVERY)
```

### Appel direct
L'utilisateur dit "genere moi une photo de..." → image-generator execute directement son pipeline 5 phases.

---

## ANTI-PATTERNS

| Interdit | Correct |
|----------|---------|
| Generer sans passer par prompt-architect | TOUJOURS optimiser le prompt |
| Utiliser un seul provider en mode standard | TOUJOURS au moins 2 providers |
| Livrer sans scoring qualite | TOUJOURS valider via quality-scorer |
| Regenerer une photo reelle de l'utilisateur | Deleguer a image-studio/image-enhancer |
| Ignorer les metadata | TOUJOURS sauvegarder le JSON complet |
| Hardcoder les cles API | TOUJOURS lire depuis ai_config.json |

---

## MONITORING

```
[IMAGE-GEN] Phase 1 — Brief analyse : type={type}, mode={mode}
[IMAGE-GEN] Phase 2 — Prompt rewrite : {provider} → {longueur prompt} chars
[IMAGE-GEN] Phase 3 — Generation : {provider} → {status} en {time}ms
[IMAGE-GEN] Phase 4 — Score : {image} → {score}/100
[IMAGE-GEN] Phase 5 — Selected : {best_image} ({provider}, score={score})
```
