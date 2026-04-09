---
name: Skill image-generator 09/04
description: Nouveau skill L3 SPECIALIST text-to-image multi-provider (FLUX, GPT-Image, Nano Banana 2, SDXL) avec 3 agents et 4 scripts Python
type: project
---

Nouveau skill `image-generator` cree le 2026-04-09 pour combler le manque critique : aucun skill ne pouvait generer une image a partir d'un texte.

**Why:** Les meilleurs generateurs (Nano Banana 2 = Gemini 3.1 Flash Image, GPT-Image/DALL-E 3, FLUX, Ideogram, Recraft) offrent des capacites revolutionnaires que nos skills compositing-only n'avaient pas.

**How to apply:** Invoquer `image-generator` quand l'utilisateur demande de generer/creer/dessiner/illustrer une image IA. Le skill route automatiquement vers le meilleur provider selon le type de tache.

## Architecture

```
~/.claude/skills/image-generator/
  SKILL.md                    -- Pipeline 5 phases, matrice routage, hard-gates
  agents/
    prompt-architect.md       -- Rewriting prompts optimises par provider
    quality-scorer.md         -- Scoring qualite via Gemini vision (10 criteres /100)
    style-consistency-manager.md -- Coherence visuelle inter-images (session state JSON)
  scripts/
    image_gen_router.py       -- Routeur multi-provider CLI
    hf_generate.py            -- Wrapper HuggingFace Spaces (FLUX, SDXL)
    openai_generate.py        -- Wrapper OpenAI API (GPT-Image, DALL-E 3)
    gemini_generate.py        -- Wrapper Gemini API (Nano Banana 2)
  references/
    PROVIDERS.md              -- Doc technique providers (limites, tarifs, quirks)
```

## Matrice de routage
- Photo realiste → FLUX.1 (HF Space, gratuit)
- Texte dans l'image → GPT-Image (OpenAI API)
- Vitesse / iteration → Nano Banana 2 (Gemini API, ~3s)
- Illustration → FLUX.1 + style prompt
- Logo → GPT-Image + Canva
- Anime → SDXL anime (HF Space)

## Integrations effectuees
- `image-studio` : Phase 2ter ajoutee (AI Generation optionnelle)
- `deep-research` : dispatch table mise a jour (generation image IA)
- `image-enhancer` : Pipeline E (API) ajoute pour contourner les deps locales manquantes (SUPIR, CodeFormer, Aura SR via HF Spaces) + script `enhance_api.py`

## Recherche effectuee
- Nano Banana 2 = Gemini 3.1 Flash Image (Google), reasoning avant rendu, 4K natif
- GPT-Image = transformer unifie autoregressif + diffusion (OpenAI), meilleur texte
- FLUX = Rectified Flow Matching 12B params (Black Forest Labs), meilleur photoralisme
- Ideogram 3.0 = #1 rendu texte (~95% precision)
- Recraft V3 = generation vectorielle SVG native
