---
name: Skill image-studio créé 07/04/2026
description: Studio unifié images/flyers/affiches, pipeline 8 phases avec art-director critique, fidélité brief + images réelles
type: project
---

# image-studio — Studio unifié visuel

Créé le 2026-04-07 pour unifier les 3 skills existants (image-detourage, image-enhancer, flyer-creator) sous une orchestration cohérente.

**Pipeline 8 phases :**
1. Brief parsing (agent brief-analyst)
2. Asset intake via vision (agent asset-curator)
3. Moodboard 2 directions (agent art-director mode exploration)
4. Asset prep (dispatch detourage/enhance)
5. Composition (HTML+CSS+Playwright OU Pillow/OpenCV)
6. Typography & layout rules pro (checklist WCAG)
7. Art-director critique itérative (grille /100, max 4 iters, seuil 80)
8. QA visuel final (agent qa-visual)

**5 agents :** brief-analyst, asset-curator, art-director (double rôle), compositor, qa-visual

**Règles sacrées :**
- Images réelles JAMAIS régénérées par IA (visage → GFPGAN, pas face-swap)
- Logos intacts
- Art-director OBLIGATOIRE avant livraison
- Fidélité brief > créativité libre

Emplacement : `C:/Users/Alexandre collenne/.claude/skills/image-studio/`

**Why:** Les 3 skills existants fonctionnaient en silo sans coordination, sans critique esthétique, sans compréhension unifiée du brief. Les rendus souffraient de manque de goût pro et de dérives par rapport à la demande.

**How to apply:** Invoquer `image-studio` pour TOUTE demande de création/modification d'image, flyer, affiche, poster, retouche, compositing. Les skills atomiques (detourage/enhance/flyer) restent invoquables mais comme building blocks de image-studio.
