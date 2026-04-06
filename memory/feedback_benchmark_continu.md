---
name: Benchmark continu des IAs à chaque demande
description: Le skill deep-research doit benchmarker toutes les IAs à chaque session pour améliorer le routage intelligent
type: feedback
---

Le skill deep-research (type Perplexity) doit TOUJOURS tester l'ensemble des IAs à la fin de chaque demande pour mettre à jour sa connaissance des forces/faiblesses de chaque IA.

**Why:** Les performances des IAs évoluent (mises à jour modèles, changements endpoints, nouveaux modèles). Un routage statique devient obsolète. Seul un benchmark continu garantit que la meilleure IA est utilisée pour chaque type de tâche.

**How to apply:** À la fin de chaque session deep-research, lancer un mini-benchmark sur la tâche en cours (`--mode research --aggregate`), comparer les réponses de toutes les IAs (qualité, vitesse, pertinence), et mettre à jour les scores RETEX + la matrice de routage dans le SKILL.md si les résultats divergent des scores actuels.
