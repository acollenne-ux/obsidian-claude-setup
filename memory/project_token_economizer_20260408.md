---
name: Token Economizer Suite (08/04/2026)
description: Création de 5 skills L6 META pour économiser 70% des tokens de deep-research tout en augmentant le raisonnement d'Opus 4.6 (principe reasoning-first)
type: project
---

# Token Economizer Suite — 2026-04-08

## Contexte
Opus 4.6 est puissant mais coûteux. Objectif double : **−70% tokens** sur deep-research ET **qualité de raisonnement ≥ baseline +10%** (qa-pipeline). Principe directeur : **reasoning-first, tokens-second** — chaque token économisé est réinvesti en profondeur de raisonnement (thinking ciblé, contexte dense, délégation mécanique).

**Why:** l'utilisateur a explicitement rejeté une démarche purement d'économie — l'optimisation doit augmenter la puissance de raisonnement, pas la diminuer. Gate de non-régression obligatoire.

**How to apply:** tout skill d'optimisation deep-research doit (1) mesurer baseline, (2) dispatcher utilitaires, (3) mesurer qualité post-run, (4) rollback si régression.

## 5 skills créés (L6 META)

| Skill | Rôle | Gain typique |
|-------|------|--------------|
| `token-economizer` | Orchestrateur, entry Phase 0B, allocation matrix, gate qualité | — (méta) |
| `prompt-cache-manager` | Cache ephemeral Anthropic 1h, system+CLAUDE.md+MCP docs | −90% sur ~28k tok cachés |
| `haiku-delegator` | Route grep/parse/list/fetch vers Haiku 4.5, retour JSON ≤500 tok | −85% sur sous-tâches mécaniques |
| `context-compressor` | Compression hiérarchique FULL→SUMMARY→META→ARCHIVE + pruning + cosine ≥0.85 | −60-75% contexte |
| `adaptive-thinking-router` | Pilote `thinking.effort` low/med/high par phase, conclusion TOUJOURS high | −40-60% thinking + réinvestissement ciblé |

**Gain combiné cible** : −70% tokens + qualité ≥ baseline +10%.

## Intégration deep-research
- Hook obligatoire ajouté en **Phase 0B-bis** de `deep-research/SKILL.md` (ligne ~282).
- Backup : `deep-research/SKILL.md.bak_before_token_economizer_20260408`.
- Invocation : `Skill: token-economizer  args: complexity=<LITE|STANDARD|FULL>` après Phase 1 classification.
- Gate non-régression : mesure qa-pipeline post-run, rollback si dégradation.

## Arborescence
- Les 5 skills sont en **L6 META** (cross-cutting, infrastructure efficacité).
- Mise à jour `skill-tree-manager/SKILL_TREE.md` avec les 5 nouvelles entrées.
- Livrable déclaré : DOC (`token_savings_report.md`), généré par `pdf-report-gen`, envoyé à acollenne@gmail.com.

## Benchmark techniques (sources 2025-2026)
1. Prompt caching ephemeral 1h TTL → Anthropic docs, ngrok analysis
2. Haiku 4.5 sub-agents → Claude Code sub-agents guide
3. Compression hiérarchique → claude-mem, hierarchical-memory-middleware
4. Adaptive thinking → Anthropic extended thinking docs
5. Subagent context isolation → Claude Code docs
6. Token counting API → Anthropic docs
7. Output style concise → Claude Code best practices

## Fichiers créés/modifiés
- `~/.claude/skills/token-economizer/SKILL.md` (nouveau)
- `~/.claude/skills/prompt-cache-manager/SKILL.md` (nouveau)
- `~/.claude/skills/haiku-delegator/SKILL.md` (nouveau)
- `~/.claude/skills/context-compressor/SKILL.md` (nouveau)
- `~/.claude/skills/adaptive-thinking-router/SKILL.md` (nouveau)
- `~/.claude/skills/deep-research/SKILL.md` (hook Phase 0B-bis injecté)
- `~/.claude/skills/skill-tree-manager/SKILL_TREE.md` (5 entrées L6 ajoutées)
- `~/.claude/plans/bubbly-popping-dragonfly.md` (plan approuvé)

## Points d'attention
- **Gate de non-régression obligatoire** : jamais déployer une optimisation sans mesure qualité.
- **Haiku uniquement pour le mécanique** : JAMAIS de synthèse/arbitrage délégué.
- **Conclusion TOUJOURS thinking=high** : non négociable quel que soit le niveau de classification.
- **Stockage originaux compression** dans `~/.claude/cache/compressed/` pour rollback.

## Prochaines étapes
- Test end-to-end sur requête de référence (baseline vs optimisé)
- Audit skill-creator scoring ≥85/100 par skill
- Mesures réelles sur 10 runs pour calibrer allocation matrix
- RETEX dans `memory/feedback_token_savings.md`
