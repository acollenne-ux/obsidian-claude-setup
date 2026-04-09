---
name: Gemini 3 Pro co-moteur vision obligatoire
description: Claude Opus doit systématiquement s'appuyer sur Gemini 3 Pro (via gemini-cli) pour toute tâche image/diagramme/visuel — extraction, génération, review.
type: feedback
---

**Règle** : pour toute création ou modification d'image, diagramme, visuel, flyer, schéma, mockup, Claude Opus 4.6 doit appeler `gemini-cli` (Gemini 3 Pro OAuth gratuit, ~1000 req/jour) comme co-moteur vision AVANT de livrer.

**Why** : demande explicite Alexandre 2026-04-08 — Gemini 3 Pro a une vision supérieure à Claude Opus sur la perception d'images (composition, palette, typo, reconnaissance main levée, lecture de labels denses). Claude reste le chef d'orchestre (raisonnement stratégique, MECE, pipeline), Gemini fait le heavy lifting visuel.

**How to apply** :
- `image-studio` — Hard-Gate #7 ajouté. Gemini utilisé en Phases 1 (analyse références), 3 (moodboard), 5 (prompts Canva), 7 (review drafts).
- `idea-to-diagram` — Hard-Gate #8 ajouté. Gemini utilisé en Phase 1 (image→structure si input visuel) et Phase 4 (review SVG/PNG généré).
- Invocation : `python "C:/Users/Alexandre collenne/.claude/skills/gemini-cli/tools/gemini_wrapper.py" --prompt "..." --image "..."`.
- Fallback automatique `multi-ia-router` (Gemini 2.5 Flash API key) si CLI absent/quota épuisé — géré par le wrapper.
- **Prérequis** : Alexandre doit lancer `gemini` une fois en terminal pour compléter le login OAuth navigateur, puis `gemini config set telemetry false`. Tant que ce n'est pas fait, le wrapper fallback transparent sur multi-ia-router.
- Ne JAMAIS bypasser Gemini sur une tâche visuelle sauf fallback explicite loggé.
