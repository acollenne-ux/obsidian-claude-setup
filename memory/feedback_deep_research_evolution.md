---
name: Deep-research doit toujours evoluer et appeler superpowers + team-agent
description: Le skill deep-research doit TOUJOURS invoquer superpowers et team-agent, et TOUJOURS s'auto-améliorer après chaque session
type: feedback
---

Le skill deep-research doit TOUJOURS :
1. Appeler le skill `superpowers` (brainstorming, dispatching-parallel-agents) pour maximiser la qualité
2. Appeler le skill `team-agent` pour orchestrer une équipe d'agents spécialisés en parallèle
3. S'auto-améliorer après CHAQUE session (Phase 11 obligatoire, pas optionnelle)

**Why:** L'utilisateur veut que deep-research soit un vrai orchestrateur type Perplexity Pro, pas juste un skill de recherche basique. La combinaison deep-research + superpowers + team-agent donne les meilleurs résultats.

**How to apply:**
- À chaque invocation de deep-research : invoquer superpowers:brainstorming AVANT de planifier
- À chaque invocation de deep-research : invoquer team-agent pour dispatcher les agents en parallèle
- À chaque fin de session : Phase 11 OBLIGATOIRE — modifier le SKILL.md pour intégrer les améliorations
- Ne jamais livrer sans avoir fait évoluer le skill si une amélioration est identifiée
