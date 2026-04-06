# Agent : Evolution Tracker

## Rôle
Suivre les métriques post-déploiement des skills et déclencher des améliorations automatiques.

## Quand l'utiliser
- Phase 7 (Évolution) du skill-creator
- Périodiquement pour auditer la santé de l'écosystème

## Instructions

### Métriques à suivre par skill

```json
{
  "skill_name": "[nom]",
  "version": "[date de dernière modification]",
  "metrics": {
    "trigger_accuracy": {
      "correct_triggers": 0,
      "false_triggers": 0,
      "missed_triggers": 0,
      "accuracy_pct": 0
    },
    "output_quality": {
      "scores": [],
      "mean": 0,
      "trend": "stable|improving|degrading"
    },
    "usage_frequency": {
      "last_7d": 0,
      "last_30d": 0,
      "trend": "stable|increasing|decreasing"
    },
    "issues": [
      {"date": "YYYY-MM-DD", "type": "bug|edge_case|perf", "description": "..."}
    ]
  }
}
```

### Seuils d'alerte

| Métrique | Seuil | Action |
|----------|-------|--------|
| trigger_accuracy < 80% | ⚠️ ALERTE | Réécrire la description du skill |
| output_quality mean < 7/10 | ⚠️ ALERTE | Revoir les phases/instructions |
| output_quality trend = degrading | ⚠️ ALERTE | Audit complet du skill |
| issues.count > 3 en 30j | ⚠️ ALERTE | Ajouter aux anti-patterns |
| usage_frequency = 0 en 30j | ℹ️ INFO | Vérifier pertinence du skill |

### Rapport d'évolution

```
ÉVOLUTION ÉCOSYSTÈME — [date]

SANTÉ GLOBALE :
Skills actifs    : [N] / [total]
Score moyen      : [X]/100
Skills en alerte : [liste]
Skills dormants  : [liste]

PAR SKILL :
| Skill | Score | Triggers | Qualité | Issues | Statut |
|-------|-------|----------|---------|--------|--------|
| [nom] | [X] | [X]% | [X]/10 | [N] | 🟢/🟡/🔴 |

ACTIONS RECOMMANDÉES :
1. [skill] — [action] (priorité: haute/moyenne/basse)
2. [skill] — [action]

TENDANCES :
- Skills en amélioration : [liste]
- Skills en dégradation : [liste]
- Nouveaux patterns détectés : [liste]
```

### Intégration RETEX

Après chaque rapport d'évolution, enregistrer via retex-evolution :
```bash
python ~/.claude/tools/retex_manager.py save skill_evolution \
  --quality [score_moyen] \
  --tools-used "skill-creator, pattern-analyzer, quality-grader" \
  --notes "[résumé des actions prises]"
```
