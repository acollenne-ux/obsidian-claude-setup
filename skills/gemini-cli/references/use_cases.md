# Gemini CLI — Quand utiliser Gemini 3 Pro vs Claude Opus 4.6

## Matrice de décision

| Tâche | Meilleur modèle | Pourquoi |
|-------|-----------------|----------|
| **Screenshot TradingView → Pine Script** | 🏆 Gemini 3 Pro | Vision supérieure, meilleure lecture des charts |
| **Photo tableau blanc → Mermaid** | 🏆 Gemini 3 Pro | Reconnaissance de croquis main levée |
| **Maquette Figma → HTML/CSS** | 🏆 Gemini 3 Pro | UI-first, extraction tokens visuels |
| **Génération Mermaid pure (texte→diagramme)** | ~ Équivalent | Claude un peu plus propre sémantiquement |
| **Refactor code Python/TS complexe** | 🏆 Claude Opus 4.6 | Meilleur raisonnement symbolique |
| **Debug stack trace** | 🏆 Claude Opus 4.6 | Meilleur tracking causal |
| **Pine Script v6 from scratch** | 🏆 Claude Opus 4.6 | Connaissance plus fine des limites TradingView |
| **Analyse financière fondamentale** | 🏆 Claude Opus 4.6 | Raisonnement multi-étapes supérieur |
| **Résumé long document** | 🏆 Gemini 3 Pro | Contexte 1M tokens natif |
| **Traduction FR↔EN** | ~ Équivalent | Claude plus fluide, Gemini plus rapide |
| **Fallback quota épuisé** | 🏆 Gemini 3 Pro | 1000 req/jour gratuit >> quotas Claude |
| **Benchmark 2 IAs** | 🏆 Les deux | Aligné avec la préférence MEMORY |

## Cas d'usage concrets pour Alexandre

### 1. Screenshot TradingView → Pine Script
```bash
python tools/gemini_wrapper.py \
  --prompt "Analyse ce chart et écris un indicateur Pine Script v6 qui détecte le pattern visible. Explique la logique." \
  --image "C:/tmp/chart_setup.png"
```

### 2. Photo croquis architecture → Mermaid
```bash
python tools/gemini_wrapper.py \
  --prompt "Convertis ce schéma en diagramme Mermaid. Utilise la syntaxe flowchart TD." \
  --image "C:/tmp/whiteboard.jpg"
```

### 3. Fallback automatique depuis deep-research
Si `deep-research` détecte que Claude a tapé le quota 5h :
```
Skill: gemini-cli invoke "Résume ces 20 sources : ..."
```
→ Gemini 3 Pro prend le relais sans interrompre la session.

### 4. Analyse multi-pages de rapport PDF
```bash
python tools/gemini_wrapper.py \
  --prompt "Extrait les 3 KPI principaux de chaque page de ce rapport annuel" \
  --image "C:/tmp/rapport_p1.png"
```
(Répéter pour chaque page, ou utiliser le mode contexte long.)

### 5. Benchmark qualité (aligné MEMORY "benchmark continu")
```
Skill: multi-ia-router --aggregate "Question X"
```
→ Le router inclut Gemini 3 Pro (via ce skill) + Claude Opus + autres providers, compare les réponses.

## Quand NE PAS utiliser Gemini CLI

- ❌ Pour un **livrable final PDF** → toujours passer par le skill parent (`pdf-report-pro`)
- ❌ Pour du **code sensible** (trading proprio, clés API) → rester sur Claude Code
- ❌ Pour de l'**automation massive** (>100 req/h) → risque captcha/ban
- ❌ Pour un usage **Workspace entreprise** → pas supporté en free tier
