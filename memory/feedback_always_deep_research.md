---
name: Toujours utiliser deep-research
description: Le skill deep-research doit être invoqué en PREMIER pour TOUTE demande, avant les skills spécialisés
type: feedback
---

Toujours invoquer le skill `deep-research` (type Perplexity, orchestration multi-agents) pour TOUTES les demandes, sans exception.

**Why:** L'utilisateur veut que chaque réponse bénéficie de la recherche approfondie multi-sources et de l'orchestration intelligente du skill deep-research, pas juste des skills spécialisés individuels. C'est son outil principal de recherche.

**How to apply:**
- Invoquer `deep-research` EN PREMIER avant tout autre skill (stock-analysis, macro-analysis, etc.)
- deep-research doit orchestrer la recherche et déterminer quels autres skills/connecteurs utiliser
- Ne jamais sauter cette étape, même si un skill spécialisé semble suffisant
- Cela s'applique à toutes les demandes : analyse boursière, macro, code, recherche générale
