---
name: qa-pipeline
description: "Pipeline de contrôle qualité : QA anti-hallucination, Source Validator, Confidence Scorer. Use when: validating output quality, checking for hallucinations, verifying sources. Triggers: 'validation', 'vérification', 'qualité', 'qa', 'hallucination'."
---

# QA Pipeline — Validation, Sources et Confiance

Trois agents spécialisés travaillent en séquence sur TOUS les outputs avant intégration.

---

## AGENT QA — ANTI-HALLUCINATION (proactif + réactif)

### Mode PROACTIF (avant exécution)

Avant qu'un agent exécute une tâche :
1. Analyser le prompt : "Ce prompt risque-t-il de générer une hallucination ?"
2. Signaux de risque : demande de chiffres futurs, événements non vérifiables, dates précises
3. Si risque élevé → modifier le prompt : ajouter "avec sources uniquement, signaler si non trouvé"
4. Si risque faible → laisser passer

### Mode RÉACTIF (après exécution)

Pour chaque output, appliquer ce protocole :

```
QA CHECK — [source/agent] — [résumé output]

□ Aligné avec la demande originale ?        [oui/non → justification]
□ Informations vérifiables sur ≥2 sources ? [oui/non → sources]
□ Contradictions avec d'autres outputs ?    [oui/non → détail]
□ Chiffres/dates plausibles et sourcés ?    [oui/non]
□ Inventions suspectées ?                   [oui/non → éléments suspects]
□ Déviation du sujet ?                      [oui/non → comment]

SCORE RISQUE HALLUCINATION : [X]/10
  0-3 : Fiable
  4-6 : À vérifier
  7-10 : Hallucination probable → REJETER

VERDICT : ✅ VALIDE | ⚠️ À CORRIGER (raison) | ❌ REJETER (raison)
```

### Signaux d'alerte — rejeter automatiquement si :
- Chiffre précis (prix, date, statistique) sans URL source citée
- Événement 2025-2026 affirmé avec certitude absolue
- Contradiction avec une source vérifiable déjà collectée
- Détail trop spécifique sans source (ex: "le CEO a dit X en réunion privée")
- Cohérence interne impossible (ex: "croissance +50% mais CA en baisse")

### Résolution de contradictions
1. Contradiction détectée entre 2 outputs
2. Identifier les sources de chaque version
3. Si source A plus fiable → retenir A, signaler divergence
4. Si même fiabilité → lancer WebSearch complémentaire
5. Si toujours ambigu → présenter les 2 versions à l'utilisateur

**L'Agent QA peut lancer 2 WebSearch additionnelles si un fait n'est pas sourcé.**

En cas de ❌ REJETER → signaler au Chef d'Orchestre → relancer la source avec prompt corrigé.

---

## AGENT SOURCE VALIDATOR — CITATIONS NUMÉROTÉES

Vérifier chaque fait collecté, attribuer un numéro de source, et produire des citations inline.

### Protocole

1. Pour chaque affirmation factuelle → vérifier qu'elle a au moins 1 URL source
2. **Vérifier que la source CONTIENT RÉELLEMENT le fait affirmé** (pas juste que l'URL existe)
3. Attribuer un numéro [1], [2], [3]... à chaque source
4. Dans le texte final : "Le CA est de 43,4M EUR [1]"
5. En fin de document : liste numérotée des sources

### Score de crédibilité par source

| Score | Type de source |
|-------|---------------|
| 9-10 | Rapport officiel, SEC filing, données gouvernementales |
| 7-8 | Reuters, Bloomberg, Financial Times, sources institutionnelles |
| 5-6 | Sites spécialisés (FinViz, Seeking Alpha, Zonebourse) |
| 3-4 | Blogs, forums, articles opinion |
| 1-2 | Sources anonymes, réseaux sociaux |

### Registre des sources

```
[1] [Nom source] — [URL] — Crédibilité: [X]/10
[2] [Nom source] — [URL] — Crédibilité: [X]/10
...
```

**Section "Sources contradictoires" obligatoire si divergences détectées.**

**Sourçage en temps réel : chaque agent source ses affirmations PENDANT la collecte, pas après.**

---

## AGENT CONFIDENCE SCORER — SCORES OBJECTIFS

Attribuer un score de confiance à chaque affirmation de l'analyse finale.

### Niveaux de confiance

| Niveau | Critère | Marqueur |
|--------|---------|----------|
| **ÉLEVÉ** | 3+ sources concordantes | ✓��✓ |
| **MOYEN** | 2 sources ou source fiable unique | ✓✓ |
| **FAIBLE** | 1 source non vérifiée ou inférence | ✓ |
| **SPÉCULATIF** | Aucune source, projection/opinion | ~ |

### Critères objectifs par type d'affirmation

| Type affirmation | Sources requises pour ÉLEVÉ | Marqueur max possible |
|-----------------|---------------------------|----------------------|
| Chiffre financier | Rapport officiel + 1 source | Élevé |
| Tendance marché | 2 sources concordantes + données | Élevé |
| Opinion analyste | 3+ analystes d'accord | Élevé |
| Prévision | Consensus + modèle | Moyen max |
| Inférence logique | Raisonnement documenté | Moyen max |
| Spéculation | — | Spéculatif toujours |

### Consensus score
"X sources sur Y concordent" au lieu de juste compter les sources.

### Impact sur la recommandation finale
- Confiance globale ≥ 8/10 → recommandation ferme
- Confiance 6-7/10 → recommandation nuancée ("sous réserve de...")
- Confiance < 6/10 → pas de recommandation, signaler incertitude

**Toute affirmation FAIBLE ou SPÉCULATIF doit être signalée explicitement. Ne jamais présenter une inférence comme un fait.**

---

## BOUCLE TEST / CORRECTION / RETEST

**Chaque output doit être testé avant intégration.**

### Grille d'évaluation

| Critère | Vérification | Action si échec |
|---------|-------------|-----------------|
| **Complétude** | Répond à 100% de la question ? | Relancer prompt plus précis |
| **Exactitude** | Données cohérentes ? | Croiser avec autre source |
| **Fraîcheur** | Données récentes (2025/2026) ? | Source plus récente |
| **Sources** | Chaque affirmation sourcée ? | Ajouter citations |
| **Cohérence** | Pas de contradiction interne ? | Résoudre le conflit |

### Protocole TEST par output

```
TEST [outil/agent]
Input   : [ce qu'on a donné]
Output  : [ce qu'il a retourné]
Qualité : [1-10]
Problèmes : [liste]
Action  : [OK | CORRIGER | REJETER | FALLBACK]
```

**Si qualité < 6/10 → CORRIGER** (max 2 tentatives, puis FALLBACK).

---

## VÉRIFICATION FINALE

```
CHECKLIST VERIFICATION FINALE
[ ] Toutes les tâches du plan complétées
[ ] Tous les outputs ont score >= 6/10
[ ] Chaque affirmation clé sourcée
[ ] Contradictions identifiées et résolues
[ ] Code (si applicable) : syntaxe + logique + edge cases
[ ] Qualité globale : [X]/10
```

Si qualité < 7/10 → identifier le maillon faible → corriger → revérifier.

---

## CONTRÔLE QUALITÉ PRÉ-LIVRAISON

Auto-évaluation sur 4 critères (/10 chaque) :

```
ÉVALUATION QUALITÉ — [titre] — [date]

1. Exhaustivité  : [X]/10 — Tous les points couverts ?
2. Précision     : [X]/10 — Données sourcées et vérifiées ?
3. Clarté        : [X]/10 — Structure logique, pas d'ambiguïté ?
4. Actionnable   : [X]/10 — Recommandations concrètes ?
─────────────────────────
Score global     : [moyenne]/10
```

**Si score < 7/10 → itérer (max 2 itérations) :**
| Critère faible | Action corrective |
|---------------|-------------------|
| Exhaustivité < 7 | Relire demande, compléter points manquants |
| Précision < 7 | Ajouter sources, corriger erreurs factuelles |
| Clarté < 7 | Restructurer, ajouter titres, simplifier |
| Actionnable < 7 | Transformer observations en recommandations concrètes |

**Si score ≥ 7/10 → livrable prêt.**
**Si < 7/10 après 2 itérations → livrer avec avertissement.**

---

## FORMAT DE SORTIE

```
QA PIPELINE — [titre]

Outputs validés     : [N]/[total]
Outputs corrigés    : [N]
Outputs rejetés     : [N]
Sources numérotées  : [1] à [N]
Confidence scores   : [% ÉLEVÉ / % MOYEN / % FAIBLE / % SPÉCULATIF]
Score qualité final : [X]/10
```

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "L'output semble correct, pas besoin de QA" | L'apparence de correction est le principal vecteur d'hallucination. TOUJOURS valider. |
| "Je n'ai pas de source pour vérifier" | Pas de source = pas de claim. Signaler explicitement ce qui n'est pas vérifiable. |
| "Le score de confiance est élevé" | Un score élevé sans source vérifiable est une hallucination confiante. |
| "C'est une connaissance générale" | Même les connaissances générales évoluent. Vérifier les données factuelles. |
| "La validation prendrait trop de temps" | Une erreur non détectée coûte plus cher qu'une validation. |

## RED FLAGS — STOP

- Claim factuel sans source → STOP, trouver ou retirer
- Score confiance > 8/10 sans aucune source → STOP, c'est suspect
- Contradictions entre deux parties de la réponse → STOP, résoudre

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Invoqué par | `deep-research` (Phase 4) |
| Avant export | `pdf-report-gen` |
| Après analyse financière | `financial-analysis-framework`, `stock-analysis` |
| Feedback qualité | `feedback-loop` |
| RETEX | `retex-evolution` |
| Debug si QA échoue | `code-debug` |

## ÉVOLUTION

Après chaque validation :
- Si une hallucination est passée → renforcer le critère de détection concerné
- Si un faux positif récurrent → ajuster le seuil de confiance
- Si un nouveau type d'erreur apparaît → l'ajouter dans les patterns

Seuils :
- Taux de faux négatifs > 10% → revoir la méthodologie complète
- Score moyen de confiance > 9/10 → suspicieux, vérifier le calibrage
