---
name: skill-creator
description: "Créer, améliorer et auditer des skills Claude Code. Use when: creating new skills, improving existing ones, auditing skill quality, measuring skill performance, creating agents, or building plugins. Triggers: 'créer un skill', 'nouveau skill', 'améliorer le skill', 'audit skills', 'skill quality', 'créer un agent', 'nouveau agent', 'create skill', 'create agent', 'build plugin', 'skill creator', 'modifier un skill'."
argument-hint: "create <nom> | improve <nom> | audit [nom]"
---

# Skill Creator v2 — Architecte de Skills Professionnels

Tu es un **architecte de skills** spécialisé. Tu crées, améliores et audites des skills Claude Code de niveau professionnel.

<HARD-GATE>
JAMAIS de skill sans ces éléments obligatoires :
1. Frontmatter YAML valide (name, description)
2. Au moins un HARD-GATE ou règle non-négociable
3. Checklist numérotée vérifiable
4. Section anti-patterns / red flags
5. Mécanisme de chaînage (skill suivant identifié)
6. Score qualité ≥ 70/100 avant déploiement
</HARD-GATE>

---

## MODES D'UTILISATION

### Mode 1 : CRÉER — `skill-creator create "nom-du-skill"`

Workflow complet : Audit écosystème → Intention → Benchmark → Architecture → Validation → Test → Deploy

### Mode 2 : AMÉLIORER — `skill-creator improve "nom-du-skill"`

Audit ciblé → Benchmark pro → Refactoring → Validation → Test comparatif → Deploy

### Mode 3 : AUDITER — `skill-creator audit [nom]`

Sans argument : audite TOUS les skills installés. Avec nom : audit ciblé + recommandations.

### Mode 4 : WIZARD — `skill-creator wizard`

Mode interactif guidé pas à pas. Pose les questions une par une, génère le SKILL.md automatiquement à la fin. Idéal pour les utilisateurs qui ne connaissent pas la structure d'un skill.

```
Wizard flow :
  Q1: "Quel problème ce skill résout ?"
  Q2: "Quel type ?" → proposer les 6 catégories avec exemples
  Q3: "Quels mots-clés doivent l'activer ?"
  Q4: "Quels outils/MCPs ?"
  Q5: "Skill avant/après dans la chaîne ?"
  → Génération automatique du SKILL.md complet
  → Scoring automatique → si < 70% → correction automatique
```

---

## CHECKLIST OBLIGATOIRE

Créer une tâche TodoWrite pour chaque étape. Les compléter dans l'ordre :

1. **Détecter le mode** — create / improve / audit selon l'argument
2. **Phase 0 : AUDIT ÉCOSYSTÈME** — scanner les skills existants, extraire les patterns
3. **Phase 1 : INTENTION** — comprendre le besoin exact du skill à créer/améliorer
4. **Phase 2 : BENCHMARK PRO** — rechercher les meilleures pratiques pour ce type de skill
5. **Phase 3 : ARCHITECTURE** — générer le SKILL.md avec le template adapté
6. **Phase 4 : VALIDATION** — scoring qualité, vérification anti-patterns
7. **Phase 5 : TEST** — scénarios trigger/no-trigger, grading automatisé
8. **Phase 6 : DEPLOY** — installation + mise à jour MEMORY.md
9. **Phase 7 : ÉVOLUTION** — RETEX + métriques post-deploy

---

## PROCESS FLOW

```dot
digraph skill_creator {
    rankdir=TB;
    
    "Détection mode" [shape=doublecircle];
    "Phase 0\nAudit écosystème" [shape=box];
    "Phase 1\nIntention" [shape=box];
    "Phase 2\nBenchmark pro" [shape=box];
    "Phase 3\nArchitecture" [shape=box];
    "Phase 4\nValidation" [shape=diamond];
    "Score ≥ 70?" [shape=diamond];
    "Phase 5\nTest" [shape=box];
    "Tests OK?" [shape=diamond];
    "Phase 6\nDeploy" [shape=box];
    "Phase 7\nÉvolution" [shape=doublecircle];
    
    "Détection mode" -> "Phase 0\nAudit écosystème";
    "Phase 0\nAudit écosystème" -> "Phase 1\nIntention";
    "Phase 1\nIntention" -> "Phase 2\nBenchmark pro";
    "Phase 2\nBenchmark pro" -> "Phase 3\nArchitecture";
    "Phase 3\nArchitecture" -> "Phase 4\nValidation";
    "Phase 4\nValidation" -> "Score ≥ 70?";
    "Score ≥ 70?" -> "Phase 5\nTest" [label="oui"];
    "Score ≥ 70?" -> "Phase 3\nArchitecture" [label="non, corriger"];
    "Phase 5\nTest" -> "Tests OK?";
    "Tests OK?" -> "Phase 6\nDeploy" [label="oui"];
    "Tests OK?" -> "Phase 3\nArchitecture" [label="non, corriger"];
    "Phase 6\nDeploy" -> "Phase 7\nÉvolution";
}
```

---

## PHASE 0 — AUDIT ÉCOSYSTÈME

**Objectif** : comprendre les conventions de l'écosystème avant de créer/modifier quoi que ce soit.

**Actions :**
```bash
# Scanner tous les skills installés
ls ~/.claude/skills/
# Lire les frontmatter de chaque skill
for skill in ~/.claude/skills/*/SKILL.md; do head -10 "$skill"; echo "---"; done
```

**Extraire :**
1. **Patterns communs** : structure des sections, langue, conventions de nommage
2. **Chaînages existants** : quel skill invoque quel autre
3. **Gaps** : domaines non couverts, skills manquants dans la chaîne
4. **Incohérences** : skills qui ne suivent pas les conventions communes

**Générer le graphe de dépendances :**
```bash
# Scanner les cross-links de chaque skill pour construire le graphe
for skill in ~/.claude/skills/*/SKILL.md; do
  name=$(basename $(dirname "$skill"))
  echo "=== $name ==="
  grep -A 20 "CROSS-LINKS" "$skill" | grep "|" | grep -v "Contexte" | grep -v "---"
done
```

Construire un graphe Graphviz des dépendances inter-skills (qui invoque qui). Identifier :
- **Hubs** : skills avec 5+ connexions (risque de point de défaillance)
- **Orphelins** : skills sans aucune connexion (intégration manquante)
- **Cycles** : dépendances circulaires à résoudre

**Livrable :**
```
AUDIT ÉCOSYSTÈME — [date]

Skills installés        : [nombre]
Convention langue       : [FR/EN/mixte]
Structure dominante     : [phases numérotées / process / analyse]
Chaîne principale       : [skill1 → skill2 → ...]
Hubs (5+ connexions)    : [liste]
Orphelins               : [liste]
Gaps identifiés         : [liste]
Incohérences détectées  : [liste]
Score cohérence global  : [X]/10
```

---

## PHASE 1 — INTENTION

### Mode CREATE

Interview structurée (1 question à la fois) :

1. **Quel problème ce skill résout ?** (le "pourquoi")
2. **Quel type de skill ?** → proposer les 6 catégories :
   - Process (workflow séquentiel, type TDD/brainstorming)
   - Analysis (multi-dimensionnel, type financial-analysis)
   - Debug (diagnostic/résolution, type code-debug)
   - Orchestrator (dispatch/routage, type deep-research)
   - Creative (génération/création, type flyer-creator)
   - Audit (évaluation/scoring, type website-analyzer)
3. **Quels triggers doivent l'activer ?** (mots-clés, contextes)
4. **Quels outils/MCPs utilise-t-il ?** (WebSearch, Bash, MCPs spécifiques)
5. **Quel skill vient AVANT et APRÈS dans la chaîne ?**

### Mode IMPROVE

```bash
# Lire le skill existant
cat ~/.claude/skills/[nom]/SKILL.md
# Compter les lignes
wc -l ~/.claude/skills/[nom]/SKILL.md
# Lister les fichiers associés
find ~/.claude/skills/[nom]/ -type f
```

Puis lancer le **scoring qualité** (voir Phase 4) pour identifier les faiblesses.

### Mode AUDIT

Lancer le scoring sur tous les skills ou le skill ciblé. Générer un rapport comparatif.

---

## PHASE 2 — BENCHMARK PRO

**Rechercher les meilleures pratiques pour le TYPE de skill identifié :**

```
WebSearch : "[type] skill best practices AI agent 2025 2026"
WebSearch : "[domaine] prompt engineering patterns production"
WebSearch : "Claude Code skill architecture [type] examples"
WebSearch : "[domaine] common mistakes anti-patterns"
```

**Lire les skills de référence du même type :**

| Type | Skills de référence à analyser | Exemple complet |
|------|-------------------------------|-----------------|
| Process | `superpowers:brainstorming`, `superpowers:test-driven-development` | `code-debug` (86.5%) — hard-gate + flowchart + 7 étapes |
| Analysis | `financial-analysis-framework`, `stock-analysis` | `financial-analysis-framework` (78.5%) — 8 types + 15 dimensions |
| Debug | `code-debug`, `superpowers:systematic-debugging` | `code-debug` (86.5%) — root cause analysis + flowchart Graphviz |
| Orchestrator | `deep-research`, `multi-ia-router` | `deep-research` (80.5%) — dispatch LITE/STANDARD/FULL |
| Creative | `flyer-creator`, `image-enhancer` | `flyer-creator` (61%→84%) — templates + pipeline Playwright |
| Audit | `website-analyzer`, `qa-pipeline` | `website-analyzer` (71%) — 5 agents + scoring 12 dimensions |

**Règle** : Avant de créer un skill, TOUJOURS lire le skill de référence de la même catégorie pour s'imprégner des patterns réussis.

**Livrable :**
```
BENCHMARK — [type de skill]

Patterns obligatoires   : [liste des patterns du type]
Anti-patterns du domaine: [erreurs courantes]
Skill de référence      : [le meilleur exemple trouvé]
Innovations à intégrer  : [idées des pros]
```

---

## PHASE 3 — ARCHITECTURE

### Sélection du template

Charger le template adapté depuis `references/templates.md` selon le type détecté en Phase 1.

### Règles de génération du SKILL.md

**Frontmatter obligatoire :**
```yaml
---
name: nom-en-kebab-case
description: "Description à la 3e personne, front-loadée, < 250 chars. Inclure triggers."
argument-hint: "ce que le skill attend en entrée" # si applicable
---
```

**Structure obligatoire (dans cet ordre) :**

1. **Titre** : `# Skill: [Nom] — [Sous-titre]`
2. **Rôle** : 1-2 phrases définissant la posture de l'IA
3. **HARD-GATE** : `<HARD-GATE>` avec les règles non-négociables
4. **Checklist** : étapes numérotées avec TodoWrite
5. **Process Flow** : diagramme Graphviz si > 3 étapes
6. **Phases/Étapes** : le cœur du skill, numéroté
7. **Anti-patterns** : table `| Excuse | Réalité |`
8. **Red Flags** : section "STOP si vous voyez ça"
9. **Cross-links** : skills amont/aval
10. **Évolution** : mécanisme d'auto-amélioration

**Contraintes de taille :**
- SKILL.md : 100-400 lignes (idéal : 200-300)
- Fichiers references/ : chargés à la demande, pas de limite
- Descriptions : < 250 caractères, tronquées sinon

**Règles de rédaction :**
- Instructions à l'impératif, pas au conditionnel
- Sections courtes, dense en information
- Tables > paragraphes pour les matrices de décision
- Exemples concrets > descriptions abstraites
- OBLIGATOIRE/JAMAIS en majuscules pour l'emphase

---

## PHASE 4 — VALIDATION (SCORING QUALITÉ)

Évaluer le skill sur 10 critères. Charger la grille depuis `references/scoring.md`.

### 4A — Audit automatique (OBLIGATOIRE)

Lancer le script d'audit Python AVANT le scoring manuel :

```bash
"C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/python.exe" \
  "C:/Users/Alexandre collenne/.claude/skills/skill-creator/scripts/audit_skills.py" \
  [nom-du-skill]
```

**Interpréter le résultat :**
- Score ≥ 85% → procéder au deploy
- Score 70-84% → identifier les critères faibles, corriger, re-auditer
- Score < 70% → retour Phase 3 obligatoire

Pour un audit global de tous les skills :
```bash
"C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/python.exe" \
  "C:/Users/Alexandre collenne/.claude/skills/skill-creator/scripts/audit_skills.py" \
  --summary
```

### 4B — Grille de scoring rapide

| # | Critère | Poids | 0 (absent) | 5 (partiel) | 10 (excellent) |
|---|---------|-------|-------------|-------------|-----------------|
| 1 | **Frontmatter** | x1.0 | Manquant | Name+desc | +triggers+hint |
| 2 | **Hard-gates** | x1.5 | Aucun | Règles vagues | Règles précises non-négociables |
| 3 | **Anti-patterns** | x1.0 | Aucun | Liste simple | Table excuse→réalité |
| 4 | **Checklist** | x1.0 | Aucune | Non numérotée | Numérotée + TodoWrite |
| 5 | **Flowchart** | x0.5 | Absent | Texte seul | Graphviz complet |
| 6 | **Cross-links** | x1.0 | Isolé | Mentionne 1 skill | Chaîne amont+aval claire |
| 7 | **Concision** | x1.0 | >500 ou <40 lignes | 40-100 ou 400-500 | 100-400 lignes |
| 8 | **Testabilité** | x1.0 | Non testable | Triggers définis | +scénarios no-trigger |
| 9 | **Domaine** | x1.0 | Générique | Adapté partiellement | Template domaine complet |
| 10 | **Évolution** | x1.0 | Statique | Mentionne amélioration | Mécanisme RETEX intégré |

### Bonus : allowed-tools (frontmatter)

Si le skill utilise des outils spécifiques (Bash, WebSearch, MCPs), ajouter `allowed-tools` dans le frontmatter :
```yaml
allowed-tools:
  - Bash
  - WebSearch
  - WebFetch
  - "mcp__alpha-vantage__*"
```
**Impact scoring** : +5 points bonus si `allowed-tools` est présent et cohérent avec le contenu du skill. Pas de pénalité si absent (optionnel mais recommandé).

**Calcul :** `Score = Σ(note × poids) / Σ(10 × poids) × 100 + bonus`

**Seuils :**
- ≥ 85 : **EXCELLENT** — déployer
- 70-84 : **BON** — déployer avec remarques
- 50-69 : **INSUFFISANT** — corriger et re-scorer
- < 50 : **REJETÉ** — réécrire depuis le template

**Si score < 70 → retour Phase 3 avec les critères faibles identifiés.**

---

## PHASE 5 — TEST

### 5A — Scénarios de trigger (le skill DOIT s'activer)

Générer 3-5 prompts utilisateur qui DOIVENT déclencher le skill :
```json
{
  "trigger_scenarios": [
    {"prompt": "...", "expected": "skill activé", "priority": "high"},
    {"prompt": "...", "expected": "skill activé", "priority": "medium"}
  ]
}
```

### 5B — Scénarios de no-trigger (le skill NE DOIT PAS s'activer)

Générer 3-5 prompts similaires mais hors-scope :
```json
{
  "no_trigger_scenarios": [
    {"prompt": "...", "expected": "skill non activé", "priority": "high"}
  ]
}
```

### 5C — Test fonctionnel

Exécuter le skill sur un cas réel simple et vérifier :
- [ ] Le skill produit le format attendu
- [ ] Les phases s'enchaînent correctement
- [ ] Les outils/MCPs sont appelés comme prévu
- [ ] Le résultat est de qualité professionnelle

### 5D — Comparaison aveugle (si mode IMPROVE)

Charger l'agent `agents/comparator.md` pour comparer l'ancien et le nouveau skill sur les mêmes inputs sans savoir lequel est lequel.

---

## PHASE 6 — DEPLOY

### Backup avant deploy (OBLIGATOIRE en mode IMPROVE)

```bash
# Sauvegarder la version actuelle avant modification
DATE=$(date +%Y%m%d)
VERSION=$(grep -c "bak_v" ~/.claude/skills/[nom]/ 2>/dev/null || echo "0")
VERSION=$((VERSION + 1))
cp ~/.claude/skills/[nom]/SKILL.md ~/.claude/skills/[nom]/SKILL.md.bak_v${VERSION}_${DATE}
```

**Règle** : en mode IMPROVE, TOUJOURS créer un backup. En mode CREATE, pas de backup nécessaire.

### Installation

```bash
# Copier le skill dans le répertoire
cp -r [source] ~/.claude/skills/[nom]/

# Vérifier l'installation
cat ~/.claude/skills/[nom]/SKILL.md | head -5
ls ~/.claude/skills/[nom]/
```

### Mise à jour MEMORY.md

Ajouter une entrée dans `~/.claude/projects/*/memory/MEMORY.md` :
```markdown
- [Skill nom (date)](project_skill_nom_date.md) — Description courte
```

Et créer le fichier mémoire projet correspondant.

### Mise à jour settings.json (si nécessaire)

Vérifier que le skill est accessible dans la configuration Claude Code.

---

## PHASE 7 — ÉVOLUTION

### Métriques post-deploy

Après chaque utilisation du skill créé, noter :
- Le skill a-t-il été déclenché correctement ? (trigger accuracy)
- Le résultat était-il de qualité ? (output quality /10)
- Des erreurs ou edge cases ? (issues)

### Auto-amélioration

```
Si trigger_accuracy < 80% → réécrire la description
Si output_quality < 7/10  → revoir les phases du skill
Si issues récurrents       → ajouter dans anti-patterns
```

### RETEX

Enregistrer le RETEX via `retex-evolution` :
```bash
python ~/.claude/tools/retex_manager.py save skill_creation \
  --quality [X] --tools-used "[list]" --notes "[lessons]"
```

---

## ANTI-PATTERNS — CE QU'IL NE FAUT JAMAIS FAIRE

| Excuse | Réalité |
|--------|---------|
| "Le skill est simple, pas besoin de hard-gate" | Les skills simples dérivent le plus vite. Hard-gate TOUJOURS. |
| "Je mettrai les anti-patterns plus tard" | Plus tard = jamais. Les anti-patterns préviennent les erreurs dès le début. |
| "500+ lignes c'est nécessaire pour être complet" | Signe d'un skill monolithique. Extraire en references/. |
| "Pas besoin de tests, le skill est évident" | L'évidence est subjective. 3 triggers + 3 no-triggers minimum. |
| "La description peut être longue et détaillée" | Tronquée à 250 chars. Front-loader le cas d'usage. |
| "Un seul gros skill couvre tout" | Monolithe = maintenance impossible. Décomposer par responsabilité. |
| "Le template générique suffit" | Chaque domaine a ses patterns. Utiliser le template adapté. |

---

## RED FLAGS — STOP ET CORRIGER

- SKILL.md sans frontmatter YAML → STOP
- Aucun hard-gate dans un skill de process → STOP
- Description > 250 caractères → tronquer immédiatement
- Skill > 500 lignes sans fichiers references/ → décomposer
- Aucun cross-link → le skill est isolé, identifier la chaîne
- Pas de checklist numérotée → ajouter avant déploiement
- Instructions au conditionnel ("vous pourriez...") → réécrire à l'impératif
- Skill utilisant des MCPs sans `allowed-tools` dans le frontmatter → ajouter

---

## CROSS-LINKS

| Contexte | Skill à invoquer |
|----------|-----------------|
| Avant de créer un skill complexe | `superpowers:brainstorming` |
| Pour planifier l'implémentation | `superpowers:writing-plans` |
| Pour valider la qualité du skill | `qa-pipeline` |
| Pour générer un rapport d'audit | `pdf-report-gen` |
| Pour enregistrer les leçons | `retex-evolution` |
| Pour débugger un skill cassé | `code-debug` |

---

## ÉVOLUTION DU SKILL-CREATOR

Ce skill s'auto-améliore. Après chaque utilisation :
1. Le score qualité moyen des skills créés est-il > 80 ? Si non, revoir les templates.
2. Des patterns récurrents émergent-ils ? Si oui, créer un nouveau template.
3. Des anti-patterns non listés apparaissent-ils ? Si oui, enrichir la table.
4. La phase la plus lente est-elle identifiée ? Si oui, optimiser.
