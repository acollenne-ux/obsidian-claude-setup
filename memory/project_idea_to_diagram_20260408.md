---
name: Skills idea-to-diagram + diagram-toolkit (2026-04-08)
description: Création de 2 skills + 5 agents pour la synthèse visuelle pro d'idées en schémas (McKinsey/BCG/Tufte)
type: project
---

# Skills idea-to-diagram + diagram-toolkit (2026-04-08)

Deux skills créés via skill-creator v2 pour automatiser la transformation d'idées en schémas professionnels.

**Why:** L'utilisateur veut une synthèse visuelle de niveau consulting (McKinsey/BCG) sans avoir à ouvrir Figma ou diagrams.net manuellement. Objectif : texte → schéma pro en une commande.

**How to apply:** Auto-invoqué sur "schéma", "diagramme", "synthèse visuelle", "mind map", "flowchart", "visualiser idée", "résumer en schéma".

## Architecture

### `idea-to-diagram` (orchestrateur, auto-invoqué)
Pipeline 6 phases + 5 agents spécialisés :
1. `idea-extractor` → so-what + arguments (Pyramid/SCQA)
2. `structure-architect` → MECE + Rule of 3 + arbre logique
3. `diagram-type-selector` → matrice Abela (7 familles)
4. `diagram-generator` → code Mermaid/D2/Graphviz/Typst + thème
5. `visual-qa-critic` → score /100 sur 10 critères (Tufte/Cairo), seuil ≥85
6. Export SVG + PNG 2x + PDF A4 paysage + envoi email

### `diagram-toolkit` (bibliothèque technique)
- `templates/` : 10 templates (pyramid, scqa, mece-tree, matrix-2x2, c4-context, fishbone, causal-loop, roadmap, sequence, venn)
- `themes/` : 4 thèmes pro (mckinsey #002060, bcg #00543C, monochrome, dark)
- `tools/` : `render.py` (mmdc/d2/dot/typst + fallback npx), `theme_apply.py`, `validate_diagram.py`

## Frameworks encodés
- Pyramid Principle (Minto) + SCQA + MECE + Rule of 3
- Matrice décisionnelle d'Andrew Abela (intention → type)
- Data-ink ratio (Tufte), hiérarchie visuelle, ≤5 couleurs, 1 message "so-what"

## Emplacements
- `~/.claude/skills/idea-to-diagram/SKILL.md` + `agents/*.md` (5)
- `~/.claude/skills/diagram-toolkit/SKILL.md` + `templates/` + `themes/` + `tools/`

## Dépendances CLI (fallback Mermaid via npx si manquant)
- `mmdc` (@mermaid-js/mermaid-cli) — défaut
- `d2` — optionnel
- `dot` (graphviz) — optionnel
- `typst` — optionnel (publication scientifique)
