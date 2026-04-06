# Grille de Scoring Qualité — Skills Claude Code

## 10 Critères d'évaluation

### 1. FRONTMATTER (poids x1.0)

| Score | Description |
|-------|-------------|
| 0 | Pas de frontmatter YAML |
| 2 | Frontmatter présent mais incomplet |
| 5 | `name` + `description` présents |
| 7 | + `description` < 250 chars, front-loadée |
| 10 | + `argument-hint`, triggers dans description, 3e personne |

**Vérification automatique :**
```python
import re
def check_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match: return 0
    fm = match.group(1)
    has_name = 'name:' in fm
    has_desc = 'description:' in fm
    if not has_name or not has_desc: return 2
    desc_match = re.search(r'description:\s*"([^"]*)"', fm)
    if desc_match and len(desc_match.group(1)) <= 250: return 7
    return 5
```

### 2. HARD-GATES (poids x1.5)

| Score | Description |
|-------|-------------|
| 0 | Aucun hard-gate ni règle non-négociable |
| 3 | Règles floues ("essayer de...", "il serait bien de...") |
| 5 | Règles claires mais pas dans `<HARD-GATE>` |
| 7 | `<HARD-GATE>` avec 1-2 règles précises |
| 10 | `<HARD-GATE>` avec 3+ règles précises, impératives, vérifiables |

**Critères d'un bon hard-gate :**
- Impératif ("JAMAIS", "TOUJOURS", "OBLIGATOIRE")
- Vérifiable (on peut dire oui/non objectivement)
- Actionable (dit exactement quoi faire/ne pas faire)

### 3. ANTI-PATTERNS (poids x1.0)

| Score | Description |
|-------|-------------|
| 0 | Aucune mention d'anti-patterns |
| 3 | Liste de "choses à éviter" sans justification |
| 5 | Section anti-patterns avec explications |
| 7 | Table `| Excuse | Réalité |` avec 3+ entrées |
| 10 | Table complète + section "Red Flags — STOP" séparée |

### 4. CHECKLIST (poids x1.0)

| Score | Description |
|-------|-------------|
| 0 | Pas de checklist |
| 3 | Liste non numérotée ou vague |
| 5 | Liste numérotée avec étapes claires |
| 7 | + mention de TodoWrite pour le suivi |
| 10 | + chaque étape est vérifiable (critère de complétion clair) |

### 5. FLOWCHART (poids x0.5)

| Score | Description |
|-------|-------------|
| 0 | Pas de visualisation du flux |
| 3 | Description textuelle du flux |
| 5 | Liste séquentielle claire (1→2→3) |
| 7 | Diagramme ASCII ou Mermaid |
| 10 | Graphviz `dot` avec décisions (diamond), états terminaux (doublecircle) |

**Note :** Score automatique 10 si le skill a ≤ 3 étapes linéaires (pas besoin de diagramme).

### 6. CROSS-LINKS (poids x1.0)

| Score | Description |
|-------|-------------|
| 0 | Skill complètement isolé |
| 3 | Mentionne d'autres skills dans le texte |
| 5 | Section dédiée avec 1-2 skills liés |
| 7 | Table `| Contexte | Skill |` avec amont ET aval |
| 10 | + intégration dans la chaîne existante (vérifié par audit) |

### 7. CONCISION (poids x1.0)

| Lignes | Score |
|--------|-------|
| < 40 | 3 (trop court, probablement incomplet) |
| 40-99 | 7 (acceptable pour skill simple) |
| 100-300 | 10 (zone idéale) |
| 301-400 | 7 (acceptable pour skill complexe) |
| 401-500 | 5 (à la limite, envisager references/) |
| > 500 | 2 (décomposer obligatoirement) |

### 8. TESTABILITÉ (poids x1.0)

| Score | Description |
|-------|-------------|
| 0 | Impossible de tester (pas de triggers définis) |
| 3 | Triggers implicites dans la description |
| 5 | Triggers explicites dans la description |
| 7 | + scénarios de no-trigger identifiables |
| 10 | + fichier evals.json avec cas de test formels |

### 9. DOMAINE (poids x1.0)

| Score | Description |
|-------|-------------|
| 0 | Skill générique sans adaptation au domaine |
| 3 | Quelques éléments spécifiques au domaine |
| 5 | Structure adaptée au type (process/analysis/debug/etc.) |
| 7 | Template domaine suivi + adaptations spécifiques |
| 10 | + limitations du domaine documentées + edge cases |

### 10. ÉVOLUTION (poids x1.0)

| Score | Description |
|-------|-------------|
| 0 | Statique, aucun mécanisme d'amélioration |
| 3 | Mention vague d'amélioration future |
| 5 | Section évolution avec métriques à suivre |
| 7 | + seuils d'action (si X < Y → faire Z) |
| 10 | + intégration RETEX + auto-amélioration documentée |

---

## Calcul du score final

```
Score brut = Σ(note_i × poids_i)
Score max  = Σ(10 × poids_i) = 10 × (1.0+1.5+1.0+1.0+0.5+1.0+1.0+1.0+1.0+1.0) = 100
Score final = (Score brut / Score max) × 100
```

Poids total : 10.0 → Score max brut : 100

## Verdicts

| Score | Verdict | Couleur | Action |
|-------|---------|---------|--------|
| 85-100 | **EXCELLENT** | 🟢 | Déployer immédiatement |
| 70-84 | **BON** | 🟡 | Déployer avec recommandations mineures |
| 50-69 | **INSUFFISANT** | 🟠 | Corriger les critères < 5 avant déploiement |
| 0-49 | **REJETÉ** | 🔴 | Réécrire depuis le template adapté |

## Rapport d'audit type

```
AUDIT QUALITÉ — [nom du skill]
Date : [YYYY-MM-DD]

 #  | Critère       | Poids | Note | Pondéré | Détail
----|---------------|-------|------|---------|-------
 1  | Frontmatter   | x1.0  | [N]  | [N×1.0] | [commentaire]
 2  | Hard-gates    | x1.5  | [N]  | [N×1.5] | [commentaire]
 3  | Anti-patterns | x1.0  | [N]  | [N×1.0] | [commentaire]
 4  | Checklist     | x1.0  | [N]  | [N×1.0] | [commentaire]
 5  | Flowchart     | x0.5  | [N]  | [N×0.5] | [commentaire]
 6  | Cross-links   | x1.0  | [N]  | [N×1.0] | [commentaire]
 7  | Concision     | x1.0  | [N]  | [N×1.0] | [commentaire]
 8  | Testabilité   | x1.0  | [N]  | [N×1.0] | [commentaire]
 9  | Domaine       | x1.0  | [N]  | [N×1.0] | [commentaire]
10  | Évolution     | x1.0  | [N]  | [N×1.0] | [commentaire]
----|---------------|-------|------|---------|-------
    | TOTAL         | 10.0  |      | [TOTAL] | Score: [X]/100

Verdict : [EXCELLENT/BON/INSUFFISANT/REJETÉ]

Recommandations prioritaires :
1. [critère le plus faible → action]
2. [2e critère le plus faible → action]
3. [3e critère le plus faible → action]
```
