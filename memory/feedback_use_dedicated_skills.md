---
name: Toujours utiliser les skills dédiés créés par l'utilisateur
description: Ne jamais bypasser les skills spécialisés (website-analyzer, etc.) au profit d'une analyse manuelle — respecter le workflow conçu par l'utilisateur
type: feedback
---

Ne JAMAIS contourner un skill dédié existant pour faire le travail manuellement avec des outils de base (WebFetch/WebSearch).

**Why:** L'utilisateur a investi du temps à créer des skills spécialisés (website-analyzer avec Playwright + 4 agents + scoring 10 dimensions). Ignorer ces skills est irrespectueux et produit un résultat inférieur.

**How to apply:**
1. Quand `deep-research` détecte un domaine (ex: "site web/audit web" → `website-analyzer`), TOUJOURS invoquer le skill dédié via `Skill` tool
2. Ne JAMAIS bypasser la phase de questions du brainstorming en se disant "l'intention est claire" — les questions sont là pour affiner et personnaliser l'analyse
3. Vérifier la matrice domaine→skills dans deep-research AVANT de commencer toute exécution manuelle
4. Incident du 06/04/2026 : analyse madam-bordeaux.fr faite manuellement au lieu d'utiliser website-analyzer
