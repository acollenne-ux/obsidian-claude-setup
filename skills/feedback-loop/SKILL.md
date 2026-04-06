---
name: feedback-loop
description: "Collecte et intégration du feedback utilisateur après chaque livrable. Use when: collecting user feedback, measuring satisfaction, iterating on deliverables. Triggers: 'feedback', 'score', 'satisfaction', 'améliorer la réponse'."
---

# Feedback Loop — Agent 9 : Satisfaction Utilisateur

Zéro livrable non validé. Chaque output doit atteindre ≥ 7/10 avant d'être final.

---

## PROTOCOLE DE COLLECTE

Après chaque livrable, déclencher systématiquement :

```
FEEDBACK — [titre du livrable] — [date]

1. SCORE GLOBAL          : [X]/10 — "Ce livrable répond-il à ta demande ?"
2. PERTINENCE CONTENU    : [X]/10 — "Informations pertinentes et complètes ?"
3. QUALITÉ DE FORME      : [X]/10 — "Présentation, format, lisibilité OK ?"
4. PRÉCISION DONNÉES     : [X]/10 — "Chiffres, sources, analyses fiables et à jour ?"
5. CE QUI MANQUE         : [réponse libre]
6. CE QUI EST EN TROP    : [réponse libre]
7. PRIORITÉ CORRECTION   : "Si UNE SEULE chose à améliorer :" → [réponse libre]
```

### Adaptation au contexte

- **Analyse financière** : + "Niveaux techniques exploitables ?" + "Timing entrée/sortie clair ?"
- **Code** : + "Le code fonctionne sans erreur ?" + "Documentation suffisante ?"
- **Recherche** : + "Profondeur suffisante ?" + "Sources crédibles ?"
- **Macro** : + "Implications concrètes pour le portefeuille ?"

---

## GESTION TIMEOUT

- Timeout par défaut : 120 secondes
- Après 60s : relance "Avez-vous eu le temps d'évaluer ?"
- Après 120s : score par défaut 7/10 + flag [TIMEOUT]
- Si "plus tard" / "pas maintenant" → reporter, score temporaire 7/10
- **Jamais bloquer le workflow pour attendre le feedback**

## INFÉRENCE DE SCORE

Si réponse en texte libre au lieu de score :
- Positif ("parfait", "excellent", "super") → 9/10
- Satisfait ("bien", "ok", "correct") → 7/10
- Mitigé ("bof", "moyen", "peut mieux faire") → 5/10
- Négatif ("mauvais", "nul", "à refaire") → 3/10

Toujours confirmer : "J'ai interprété comme X/10, est-ce correct ?"

---

## SEUILS DE DÉCISION

| Score | Niveau | Action | Délai max |
|-------|--------|--------|-----------|
| **9-10** | ✅ VALIDÉ | Archiver feedback positif dans RETEX | Immédiat |
| **7-8** | ⚠️ AJUSTEMENTS | Corrections ciblées, 1 itération | < 2 min |
| **5-6** | 🟠 CORRECTIONS MAJEURES | Reprendre sections problématiques, max 2 itérations | < 5 min |
| **< 5** | 🔴 REFONTE | Retour brainstorming, réanalyse demande, max 2 itérations | < 10 min |

**Escalade : si score < 7 après 2 itérations → options à l'utilisateur (accepter / préciser / abandonner).**

---

## BOUCLE DE CORRECTION

```
CORRECTION — Itération [N] — Score actuel : [X]/10

1. DIAGNOSTIC :
   Points faibles    : [liste du feedback]
   Cause probable    : [prompt vague / source manquante / mauvaise interprétation / format]

2. PLAN DE CORRECTION :
   Action 1 : [correction] → Agent : [X]
   Action 2 : [correction] → Agent : [X]

3. EXÉCUTION : [relancer agents, injecter corrections]

4. RE-LIVRAISON + RE-FEEDBACK

5. COMPARAISON :
   Score précédent : [X]/10
   Score actuel    : [Y]/10
   Delta           : [+/-Z]
   Statut          : [AMÉLIORÉ / STAGNANT / DÉGRADÉ]
```

**Si DÉGRADÉ** → rollback version précédente, approche différente.
**Si STAGNANT après 2 itérations** → escalade.

### Détection contradictions
- Score global ≥ 8 mais critère ≤ 4 → signaler incohérence
- Scores oscillants (5→8→4) → demander précision

---

## MÉTRIQUES DE SATISFACTION

```
TABLEAU DE BORD — Session [date]

Livrable             | Score init | Itérations | Score final | Temps | Statut
---------------------|-----------|-----------|------------|-------|-------
[Livrable 1]         | [X]/10    | [N]       | [Y]/10     | [X]m  | ✅/⚠️/🔴

MÉTRIQUES AGRÉGÉES :
- Score moyen initial  : [X.X]/10
- Score moyen final    : [X.X]/10
- Validation 1er jet   : [X]%
- Itérations moyennes  : [X.X]
- Temps correction     : [X] min
- Taux refonte         : [X]%
```

**Objectifs cibles :**
| Métrique | Cible | Alerte |
|----------|-------|--------|
| Score moyen final | ≥ 8.0 | < 7.0 |
| Validation 1er jet | ≥ 70% | < 50% |
| Itérations moyennes | ≤ 1.5 | > 3.0 |
| Temps correction | ≤ 3 min | > 7 min |

---

## INTÉGRATION AVEC LES AUTRES SKILLS

| Skill/Agent | Communication feedback → skill |
|-------------|-------------------------------|
| **deep-research** (Agent 1 Contexte) | "Demande mal comprise. Reformulation : [...]" |
| **deep-research** (Agent 2 Benchmark) | "Benchmark insuffisant. L'utilisateur attend : [...]" |
| **deep-research** (Agent 3 Chef) | "Score < 5, escalade. Problème structurel : [...]" |
| **qa-pipeline** (Agent QA) | "Erreur factuelle signalée sur : [...]" |
| **retex-evolution** | Transmet rapport satisfaction complet |
| **qa-pipeline** (Sources) | "Sources jugées insuffisantes" |
| **qa-pipeline** (Confiance) | "Score confiance contesté sur : [...]" |

---

## RÈGLES ABSOLUES

1. **JAMAIS de livrable final sans feedback** — toujours demander le score
2. **JAMAIS ignorer un score < 7** — chaque insatisfaction = amélioration immédiate
3. **TOUJOURS comparer** score initial vs final
4. **TOUJOURS transmettre** le rapport satisfaction à retex-evolution
5. **JAMAIS plus de 2 itérations** sans escalade
6. **Le feedback prime sur tout** — "pas ce que je voulais" → arrêter, recontextualiser
7. **Adapter le détail** : utilisateur pressé → score global + priorité. Disponible → questionnaire complet.
8. **Capitaliser** : même critique 3+ fois → signaler à retex-evolution pour modification permanente

---

## TEMPLATES RAPIDES

**Alerte escalade :**
```
🔴 ESCALADE — Score [X]/10 après [N] itérations
Livrable    : [titre]
Historique  : It.1: [X] → It.2: [X]
Problème    : [décalage persistant]
Feedback    : "[citation]"
Options     : reformuler / changer approche / réallouer
```

**Bilan session :**
```
📊 BILAN FEEDBACK SESSION
- Livrables évalués : {N}
- Score moyen : {X}/10
- Validation 1er jet : {Y}%
- Points récurrents : {liste}
- Recommandation : {amélioration prochaine session}
```

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Le score utilisateur n'est pas important" | Le feedback est le SEUL indicateur de satisfaction réelle. TOUJOURS collecter. |
| "L'utilisateur n'a pas le temps de noter" | Un score /10 prend 2 secondes. Ne pas collecter = perdre des données précieuses. |
| "Le score était bas, c'est un cas isolé" | Un score < 5 est un signal d'alerte. Toujours investiguer la cause. |
| "3 itérations de correction c'est acceptable" | Maximum 2 itérations. Au-delà, le problème est structurel, pas cosmétique. |
| "Le feedback ne sert qu'à cette session" | Le feedback alimente le RETEX et améliore TOUTES les sessions futures. |

## RED FLAGS — STOP

- Livrable envoyé sans collecte de feedback → STOP
- Score < 5/10 sans escalade → STOP, investiguer
- Plus de 2 itérations de correction → STOP, problème structurel

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Invoqué par | `deep-research` (Phase 4) |
| Après livraison PDF | `pdf-report-gen` |
| Alimente | `retex-evolution` |
| Si qualité insuffisante | `qa-pipeline` |
| Métriques globales | `retex-evolution` |

## ÉVOLUTION

Après chaque collecte de feedback :
- Si score moyen < 7/10 → identifier les dimensions les plus faibles
- Si un pattern de plainte revient → l'ajouter comme règle dans le skill concerné
- Si le questionnaire est inadapté au contexte → créer un template spécialisé

Seuils : validation 1er jet < 60% → revoir le processus de production en amont.
