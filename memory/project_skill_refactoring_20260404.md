---
name: Refactorisation mega-skill deep-research
description: Le monolithe deep-research (2201 lignes) a été découpé en 7 skills modulaires orchestrés (1651 lignes total). Architecture hub-and-spoke avec orchestrateur léger.
type: project
---

Refactorisation du méga-skill `deep-research` le 04/04/2026.

**Problème :** Le monolithe de 2201 lignes (~37K tokens) saturait le contexte, contenait des redondances (matrice IA x3, fallbacks x2), et couplait des domaines indépendants.

**Solution :** 7 skills modulaires :
1. `deep-research` (orchestrateur, 374 lignes) — classifie, détecte, dispatche
2. `multi-ia-router` (168 lignes) — routage IA, curl, consensus, fallbacks
3. `financial-analysis-framework` (335 lignes) — 8 types actifs, 15 dimensions
4. `qa-pipeline` (225 lignes) — QA, sources, confiance, validation
5. `pdf-report-gen` (108 lignes) — synthèse, PDF Markdown, email
6. `feedback-loop` (183 lignes) — feedback utilisateur, boucle correction
7. `retex-evolution` (258 lignes) — RETEX, benchmark, amélioration continue

**Why:** Le chargement sélectif (seuls les skills nécessaires sont invoqués) réduit la consommation de contexte de ~37K tokens à ~5-15K selon la tâche. Chaque skill est aussi modifiable indépendamment, ce qui rend l'auto-amélioration (Phase 11) plus sûre.

**How to apply:** Le workflow ne change pas pour l'utilisateur — `deep-research` reste le point d'entrée unique. Il invoque automatiquement les sous-skills nécessaires.

**Backup :** `~/.claude/skills/deep-research/SKILL.md.bak_monolith_2201lines`
