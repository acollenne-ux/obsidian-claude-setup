---
name: retex-evolution
description: "RETEX + benchmark continu des IAs + amélioration continue des skills. Use when: recording lessons learned, benchmarking AI models, improving skills after use. Triggers: 'retex', 'leçons', 'amélioration', 'benchmark IA'."
---

# RETEX & Evolution — Apprentissage + Amélioration Continue

Enregistrer les leçons, benchmarker les IAs, et améliorer les skills pour la prochaine session.

---

## PHASE 10 — RETEX : ENREGISTRER LES LEÇONS

**⚠️ Le RETEX DOIT être exécuté en suivant ce skill. Ne JAMAIS produire un RETEX manuellement hors framework.**

### Rapport d'incidents (OBLIGATOIRE à chaque session)

1. **Incidents** : tous les problèmes (outils en échec, rate limits, données manquantes)
2. **Solutions** : comment chaque incident a été résolu (fallback, workaround)
3. **Améliorations proposées** : modifications à implémenter
4. **Améliorations implémentées** : modifications réellement faites
5. Sauvegarder en mémoire ET inclure dans le PDF de clôture

### Commande RETEX

```bash
python "C:\Users\Alexandre collenne\.claude\tools\retex_manager.py" write '{
  "task_type": "[stock_analysis|code|research|macro|crypto|general]",
  "summary": "[description courte]",
  "tool_results": {
    "WebSearch": {"success": true, "quality": 8},
    "mistral": {"success": true, "quality": 9},
    "chart_generator": {"success": true, "quality": 8}
  },
  "what_worked": "[ce qui a bien fonctionné]",
  "what_failed": "[ce qui a échoué et pourquoi]",
  "improvement": "[ce qu'il faudra faire différemment]",
  "quality_final": 8,
  "time_minutes": 5
}'
```

---

## PHASE 10B — BENCHMARK CONTINU DES IAs

**Objectif :** Tester TOUTES les IAs sur la tâche réelle pour mettre à jour le routage.

### Protocole

**Étape 1 — Lancer le benchmark :**
```bash
python "C:\Users\Alexandre collenne\.claude\tools\multi_ai.py" query "[question-clé]" --mode reason --aggregate
```
Ou utiliser le protocole curl du skill `multi-ia-router`.

**Étape 2 — Évaluer chaque IA :**
```
BENCHMARK SESSION — [date] — [type de tâche]

| IA | Temps | Qualité /10 | Pertinence /10 | Erreurs | Score final |
|----|-------|-------------|----------------|---------|-------------|
| Gemini Flash | Xs | /10 | /10 | [détail] | /10 |
| Mistral Large | Xs | /10 | /10 | [détail] | /10 |
| Groq | Xs | /10 | /10 | [détail] | /10 |
| OpenRouter/R1 | Xs | /10 | /10 | [détail] | /10 |
| HuggingFace | Xs | /10 | /10 | [détail] | /10 |

Meilleure IA : [nom] (score [X]/10)
Surprise vs routage actuel : [oui/non]
```

**Étape 3 — Enregistrer dans RETEX :**
```bash
python "C:\Users\Alexandre collenne\.claude\tools\retex_manager.py" write <task_type> "Benchmark [date]: [IA gagnante] score [X]/10 sur [type]."
```

**Étape 4 — Mettre à jour le routage SI écart significatif :**
Si une IA surperforme de +2 points sur un type de tâche → modifier `multi-ia-router/SKILL.md` :
1. Modifier la table de routage
2. Mettre à jour les scores
3. Documenter : `"[date] : [IA X] promue N°1 pour [type] (ancien: [IA Y])"`

**Règle :** Ne modifier que sur écarts confirmés sur 2+ sessions.

**Types à tracker :** `stock_analysis`, `code`, `research`, `macro`, `crypto`, `math`, `french_writing`, `summarization`, `data_extraction`

---

## PHASE 11 — AMÉLIORATION CONTINUE

### 11-LITE (3 minutes, OBLIGATOIRE après CHAQUE livraison)

1. Lister les 2-3 lacunes principales
2. Les enregistrer dans le RETEX
3. Si score importance ≥ 7/10 → planifier 11-FULL
4. Sinon → session terminée

```
RETEX LITE — [titre] — [date]
✓ Résultat OK / ✗ Problème : [description]
Leçon (1 ligne) : [si applicable]
Temps total : [X]s
```

**Amélioration in-session :** Si une tâche échoue → leçon appliquée immédiatement à la suivante.

### 11-FULL (20 minutes, SI importance ≥ 7/10)

#### 11A — Bilan de session

```
BILAN SESSION — [titre] — [date]

1. LACUNES
   □ Quel agent/skill/IA aurait produit un meilleur résultat ?
   □ Quelle information non trouvée (et pourquoi) ?
   □ Quel outil a sous-performé (< 7/10) ?
   □ Quelle phase trop longue ou médiocre ?
   □ Quelle question sans réponse satisfaisante ?

2. SIGNAUX D'AMÉLIORATION
   □ Output manquant de profondeur → besoin agent spécialisé ?
   □ Outils en doublon → besoin coordination ?
   □ Source manquante systématiquement → besoin MCP ?
   □ Chef d'Orchestre réattribue beaucoup → plan mal structuré ?
   □ QA détecte hallucinations → besoin plus de sources ?

3. VERDICT
   - Critiques : [lacunes majeures impactant la qualité]
   - Souhaitables : [améliorations non critiques]
   - Aucune : [si tout OK]
```

#### 11B — Recherche de skills manquants

Pour chaque lacune critique :
```
WebSearch : "Claude MCP server [domaine manquant] 2026"
WebSearch : "Claude Code skill [type] best plugin"
WebFetch  : https://www.claudemcp.com/servers
```

| Lacune | Solution trouvée | Type | Score utilité | Action |
|--------|-----------------|------|--------------|--------|
| [lacune] | [outil/MCP] | MCP/skill | [X]/10 | Installer/Documenter |

- Score ≥ 8 → signaler pour installation
- Score 6-7 → documenter comme alternative
- Score < 6 → ignorer

#### 11C — Implémentation des modifications

Modifier les SKILL.md concernés via Edit tool :

1. Mettre à jour la matrice agents (deep-research) si nouvel outil
2. Ajuster les fallbacks (multi-ia-router) si outil échoué
3. Corriger les instructions d'un agent si dérive récurrente
4. Ajouter un tip dans les patterns RETEX

**Règle :** Ne modifier que ce qui améliore concrètement la qualité. Pas de changement cosmétique.

**Traçabilité :**
```
MODIFICATION [N] — [date]
Section modifiée  : [Skill X / Section Y]
Changement        : [description]
Déclencheur       : [lacune 11A]
Impact attendu    : [amélioration concrète]
```

#### 11D — PDF de clôture (si modifications)

```bash
# Écrire le rapport dans un fichier temporaire (Write tool)
# Puis :
python "C:\Users\Alexandre collenne\.claude\tools\send_report.py" "Deep-Research — Amélioration Continue [date]" --file rapport_cloture.md acollenne@gmail.com
```

Contenu :
- Bilan session (qualité, lacunes)
- Skills recherchés (tableau)
- Modifications implémentées
- Outils à installer
- Évolution (avant/après/prochaine session)

**Si aucune modification → noter dans RETEX, pas de PDF.**

---

## PHASE 12 — MODE SUIVI (optionnel, proposer systématiquement)

Après chaque analyse financière, PROPOSER :

```
"Veux-tu un suivi automatique de [ENTREPRISE] ?
Vérification hebdomadaire :
- Publication résultats trimestriels
- Changement consensus analyste
- Mouvement cours > 10%
- Catalyseurs identifiés déclenchés

Email de synthèse si événement détecté."
```

Si accepté → créer trigger via skill `schedule`.

---

## RÈGLE ABSOLUE — AUTO-AMÉLIORATION

**Les skills doivent TOUJOURS s'améliorer.** Après CHAQUE session :
1. **Identifier** ce qui a manqué/échoué/sous-optimal
2. **Chercher** les meilleurs outils/skills/MCP
3. **Implémenter** les améliorations dans les SKILL.md concernés
4. **Tester** les nouvelles intégrations
5. **Documenter** chaque modification avec date

---

## MONITORING — TIMING DE SESSION

### Compteur global

```
TIMING SESSION — [titre] — [date]
Phase 0-1  : [X]s ✓/⚠
Phase 2    : [X]s ✓/⚠
Phase 3    : [X]s ✓/⚠
Phase 4    : [X]s ✓/⚠
Feedback   : [X]s ✓/⚠
RETEX      : [X]s ✓/⚠
Phase 11   : [X]s ✓/⚠
TOTAL      : [X]s
Alertes    : [N] warnings, [N] criticals
```

### Bilan enrichi

```
BILAN SESSION — [titre] — [date]
Phases complétées    : {N}
Skills invoqués      : {liste}
Sources consultées   : {N}
Score qualité final  : {X}/10
Niveau complexité    : LITE / STANDARD / FULL
Upgrades effectués   : {N}
```

### Alertes basées sur tentatives
- > 3 tentatives → [WARNING]
- > 5 tentatives → [CRITICAL] envisager fallback
- Agent muet après 3 relances → escalade Chef d'Orchestre

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Le RETEX c'est optionnel" | Le RETEX est TOUJOURS exécuté en fin de session. Pas de session sans leçon. |
| "Rien à améliorer, tout a fonctionné" | Même une session parfaite a des optimisations possibles (temps, routage, sources). |
| "Le benchmark IA ralentit trop" | Le benchmark est en parallèle et enrichit les scores de routage pour les sessions futures. |
| "Les scores des IAs ne changent pas" | Les modèles évoluent, les providers changent. Les scores DOIVENT être recalibrés régulièrement. |
| "L'amélioration du skill peut attendre" | Si une lacune critique est détectée, l'amélioration FULL est obligatoire immédiatement. |

## RED FLAGS — STOP

- Session terminée sans RETEX enregistré → STOP
- Lacune critique détectée sans amélioration FULL → STOP
- Scores de routage identiques depuis > 5 sessions → STOP, recalibrer

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Invoqué par | `deep-research` (dernier skill, Phase 4) |
| Reçoit données de | `feedback-loop` (scores utilisateur) |
| Met à jour | `multi-ia-router` (scores IA) |
| Améliore | Tous les skills (via Phase 11) |
| Stockage | `retex_manager.py` |

## ÉVOLUTION

Ce skill est le méta-améliorateur. Il s'améliore lui-même :
- Si le format RETEX est inadapté → modifier le template
- Si le benchmark manque un provider → l'ajouter
- Si les améliorations de skills sont inefficaces → revoir la méthodologie Phase 11

Seuils : si score moyen des skills améliorés ne progresse pas en 3 sessions → refonte de la Phase 11.
