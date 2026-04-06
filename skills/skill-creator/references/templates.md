# Templates de Skills par Domaine

Ces templates sont des squelettes à adapter. Chaque section marquée `[...]` doit être remplie.

---

## Template 1 : PROCESS (workflow séquentiel)

**Exemples** : brainstorming, TDD, writing-plans

```markdown
---
name: [nom-kebab]
description: "[Action] [quand]. Use when [trigger]. Triggers: '[mots-clés]'."
---

# [Nom] — [Sous-titre]

[1-2 phrases définissant le rôle de l'IA]

<HARD-GATE>
JAMAIS [action interdite] AVANT [prérequis].
[Règle non-négociable 1]
[Règle non-négociable 2]
</HARD-GATE>

## Checklist

Créer une tâche TodoWrite pour chaque étape :

1. **[Étape 1]** — [description courte]
2. **[Étape 2]** — [description courte]
3. **[Étape 3]** — [description courte]
...

## Process Flow

\`\`\`dot
digraph [nom] {
    "[Étape 1]" [shape=box];
    "[Décision?]" [shape=diamond];
    "[État terminal]" [shape=doublecircle];
    "[Étape 1]" -> "[Décision?]";
    "[Décision?]" -> "[Étape 2]" [label="oui"];
    "[Décision?]" -> "[Étape 1]" [label="non"];
    "[Étape 2]" -> "[État terminal]";
}
\`\`\`

## Phase 1 — [Nom]
[Instructions impératives]

## Phase 2 — [Nom]
[Instructions impératives]

## Phase N — [Nom]
[Instructions impératives]

## Anti-patterns

| Excuse | Réalité |
|--------|---------|
| "[rationalisation 1]" | [pourquoi c'est faux] |
| "[rationalisation 2]" | [pourquoi c'est faux] |

## Red Flags — STOP

- [Signal d'arrêt 1]
- [Signal d'arrêt 2]

## Cross-links

- Avant : `[skill amont]`
- Après : `[skill aval]`
```

---

## Template 2 : ANALYSIS (multi-dimensionnel)

**Exemples** : financial-analysis-framework, stock-analysis

```markdown
---
name: [nom-kebab]
description: "[Analyse de quoi]. Use when [trigger]. Triggers: '[mots-clés]'."
---

# [Nom] — [Sous-titre]

## POSTURE
Tu es un [rôle expert]. Tu analyses [domaine] selon [N] dimensions.

<HARD-GATE>
JAMAIS d'analyse sans :
1. Classification de l'objet analysé
2. Minimum [N] sources
3. Identification des limitations
</HARD-GATE>

## ÉTAPE 0 — CLASSIFICATION (OBLIGATOIRE)

| Type | Caractéristiques | Métriques prioritaires |
|------|-----------------|----------------------|
| [Type A] | [desc] | [métriques] |
| [Type B] | [desc] | [métriques] |

## ÉTAPE 1 — [Dimension 1]
[Instructions d'analyse]

## ÉTAPE 2 — [Dimension 2]
[Instructions d'analyse]

## ÉTAPE N — SYNTHÈSE OBLIGATOIRE

| Scénario | Probabilité | [Métrique clé] | Catalyseur |
|----------|-------------|----------------|------------|
| Bull | [X]% | [valeur] | [événement] |
| Base | [X]% | [valeur] | [événement] |
| Bear | [X]% | [valeur] | [événement] |

## Matrice de pondération

| Critère | [Type A] | [Type B] | [Type C] |
|---------|----------|----------|----------|
| [Dim 1] | x[poids] | x[poids] | x[poids] |
| [Dim 2] | x[poids] | x[poids] | x[poids] |

## Anti-patterns
[table excuse/réalité]

## Cross-links
[skills amont/aval]
```

---

## Template 3 : DEBUG (diagnostic/résolution)

**Exemples** : code-debug, systematic-debugging

```markdown
---
name: [nom-kebab]
description: "[Diagnostic de quoi]. Use when [trigger]. Triggers: '[mots-clés]'."
---

# [Nom] — [Sous-titre]

## RÈGLE UNIVERSELLE
LIRE L'INTÉGRALITÉ DE L'ERREUR AVANT D'AGIR.

<HARD-GATE>
JAMAIS de fix sans :
1. Avoir reproduit le problème
2. Avoir identifié la root cause
3. Avoir vérifié que le fix ne casse rien d'autre
</HARD-GATE>

## Arbre de décision

| Symptôme | Cause probable | Action |
|----------|---------------|--------|
| [symptôme 1] | [cause] | [action] |
| [symptôme 2] | [cause] | [action] |

## Phase 1 — Investigation
[Instructions]

## Phase 2 — Hypothèses
[Instructions avec niveaux de confiance]

## Phase 3 — Fix
[Instructions]

## Phase 4 — Vérification
[Checklist de vérification]

## Système de confiance

| Niveau | Définition | Action requise |
|--------|-----------|---------------|
| ÉLEVÉ | Reproduit + root cause identifiée | Fix direct |
| MOYEN | Hypothèse solide, pas reproduit | Test d'abord |
| FAIBLE | Intuition seulement | Investigation supplémentaire |
| SPÉCULATIF | Aucune donnée | NE PAS agir, collecter d'abord |

## Anti-patterns
[table excuse/réalité]

## Cross-links
[skills amont/aval]
```

---

## Template 4 : ORCHESTRATOR (dispatch/routage)

**Exemples** : deep-research, multi-ia-router

```markdown
---
name: [nom-kebab]
description: "[Orchestre quoi]. Use when [trigger]. Triggers: '[mots-clés]'."
---

# [Nom] — Orchestrateur [Domaine]

Tu es un **chef d'orchestre**. Tu ne fais PAS le travail — tu dispatches.

<HARD-GATE>
JAMAIS d'exécution directe. TOUJOURS dispatcher vers le skill/agent approprié.
</HARD-GATE>

## Matrice de routage

| Détection | Skill/Agent | Priorité |
|-----------|------------|----------|
| [pattern 1] | `[skill]` | Haute |
| [pattern 2] | `[skill]` | Moyenne |
| [default] | `[fallback]` | Basse |

## Workflow

1. **Classifier** la demande
2. **Router** vers le(s) skill(s) approprié(s)
3. **Consolider** les résultats
4. **Valider** via qa-pipeline

## Gestion des erreurs

| Situation | Action |
|-----------|--------|
| Skill échoue | Fallback → [alternative] |
| Résultat vide | +2 WebSearch |
| Contradiction | Signaler les deux + position motivée |

## Anti-patterns
[table excuse/réalité]

## Cross-links
[skills amont/aval]
```

---

## Template 5 : CREATIVE (génération/création)

**Exemples** : flyer-creator, image-enhancer

```markdown
---
name: [nom-kebab]
description: "[Crée quoi]. Use when [trigger]. Triggers: '[mots-clés]'."
---

# [Nom] — [Sous-titre]

## POSTURE
Tu es un [créatif expert]. Tu produis [quoi] de qualité professionnelle.

<HARD-GATE>
JAMAIS de livraison sans :
1. Validation du brief avec l'utilisateur
2. Au moins 2 options/variantes proposées
3. Vérification qualité finale
</HARD-GATE>

## Pipeline de création

1. **Brief** — Comprendre le besoin (audience, ton, contraintes)
2. **Recherche** — Benchmark visuel/créatif (WebSearch)
3. **Prototype** — Première version rapide
4. **Feedback** — Validation utilisateur
5. **Production** — Version finale haute qualité
6. **Export** — Format(s) de sortie

## Standards de qualité

| Critère | Minimum acceptable | Excellent |
|---------|-------------------|-----------|
| [critère 1] | [minimum] | [excellent] |
| [critère 2] | [minimum] | [excellent] |

## Anti-patterns
[table excuse/réalité]

## Cross-links
[skills amont/aval]
```

---

## Template 6 : AUDIT (évaluation/scoring)

**Exemples** : website-analyzer, qa-pipeline

```markdown
---
name: [nom-kebab]
description: "[Évalue quoi]. Use when [trigger]. Triggers: '[mots-clés]'."
---

# [Nom] — [Sous-titre]

## POSTURE
Tu es un [auditeur expert]. Tu évalues [quoi] selon [N] dimensions.

<HARD-GATE>
JAMAIS de score sans :
1. Données factuelles vérifiées
2. Grille de scoring explicite
3. Recommandations actionnables
</HARD-GATE>

## Grille de scoring

| # | Dimension | Poids | 0 (critique) | 5 (moyen) | 10 (excellent) |
|---|-----------|-------|-------------|-----------|-----------------|
| 1 | [dim 1] | x[P] | [desc] | [desc] | [desc] |
| 2 | [dim 2] | x[P] | [desc] | [desc] | [desc] |

## Processus d'audit

1. **Collecte** — Rassembler les données
2. **Évaluation** — Scorer chaque dimension
3. **Analyse** — Identifier patterns et corrélations
4. **Recommandations** — Actions prioritaires classées par impact
5. **Rapport** — Synthèse structurée

## Seuils de décision

| Score | Verdict | Action |
|-------|---------|--------|
| ≥ 85 | Excellent | Maintenir |
| 70-84 | Bon | Améliorer [points faibles] |
| 50-69 | Insuffisant | Plan d'action urgent |
| < 50 | Critique | Refonte complète |

## Anti-patterns
[table excuse/réalité]

## Cross-links
[skills amont/aval]
```
