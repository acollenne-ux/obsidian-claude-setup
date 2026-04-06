---
name: Skill Creator v2
description: Skill-creator custom installé le 06/04/2026 — architecte de skills professionnels avec audit, scoring, templates et agents
type: project
---

Skill `skill-creator` v2 créé le 06/04/2026 dans `~/.claude/skills/skill-creator/`.

**Why:** Le skill-creator officiel (claude-plugins-official) était en anglais, sans intégration avec l'écosystème existant (deep-research, qa-pipeline, retex), et manquait de templates par domaine.

**How to apply:** Utiliser `skill-creator` pour toute création/amélioration de skill. 3 modes : `create`, `improve`, `audit`.

## Architecture
- `SKILL.md` (408 lignes, score 90/100) — 7 phases, hard-gates, anti-patterns, cross-links
- `references/templates.md` — 6 templates par domaine (process, analysis, debug, orchestrator, creative, audit)
- `references/scoring.md` — Grille 10 critères pondérés /100
- `agents/` — 5 agents (pattern-analyzer, quality-grader, test-generator, comparator, evolution-tracker)
- `scripts/audit_skills.py` — Script Python d'audit automatisé

## Résultat audit initial (06/04/2026)
- 28 skills audités, moyenne 43%
- Seul skill EXCELLENT : skill-creator (90%)
- deep-research seul INSUFFISANT (63%)
- 26 skills en REJETÉ (<50%) → opportunité massive d'amélioration
