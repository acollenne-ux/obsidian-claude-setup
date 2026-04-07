---
name: Arbre Skills 5 couches obligatoire
description: Claude doit TOUJOURS respecter l'arbre restructuré (5 couches) et le contenu intégral de chaque SKILL.md
type: feedback
---

Claude doit OBLIGATOIREMENT respecter l'arbre restructuré des skills (5 couches) ET appliquer intégralement le contenu de chaque SKILL.md sans raccourci.

**Why:** Décision utilisateur 2026-04-07 — l'arbre 5 couches (C0 deep-research → C1 brainstorming/team-agent/multi-ia-router → C2 domaine → C3 qa-pipeline → C4 livrable obligatoire → C5 feedback/retex) est la structure officielle. Toute déviation casse la cohérence et la qualité.

**How to apply:**
- Toute conversation commence par `deep-research` (C0).
- Phases C1, C3, C5 toujours invoquées.
- C2 dispatché selon la matrice de domaine.
- **C4 obligatoire** : chaque réponse produit au moins UN livrable (PDF par défaut via `pdf-report-pro` → email acollenne@gmail.com ; sinon PPT, doc, image, vidéo, audio selon mots-clés).
- Lire et respecter chaque SKILL.md de bout en bout — jamais de raccourci, jamais sauter de phases, jamais ignorer les checklists.
- Doublons interdits : utiliser `pdf-report-pro` (pas `pdf-report-gen`), `image-studio` (pas flyer-creator/image-detourage/image-enhancer en direct), `superpowers-brainstorming` custom (pas plugin).
- Référence complète : `C:\tmp\skills_tree_restructure.md` + PDF envoyé le 2026-04-07.
