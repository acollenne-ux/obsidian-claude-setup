---
name: Respecter les skills dans leur intégralité
description: Ne JAMAIS prendre de raccourcis dans l'exécution des skills — exécuter TOUTES les phases, TOUS les agents, TOUS les outils prévus
type: feedback
---

Quand un skill est invoqué (notamment `deep-research`, `stock-analysis`, `financial-analysis-framework`, etc.), exécuter **l'intégralité** du protocole : toutes les phases, tous les sous-agents, tous les WebSearch/WebFetch/MCPs prévus, qa-pipeline, pdf-report-gen, feedback-loop, retex-evolution.

**Interdit :**
- Étiqueter FULL un travail de niveau STANDARD
- Sauter des phases pour "tenir le budget temps/contexte"
- Se contenter de 3-4 WebSearch quand le skill en demande 8+
- Inventer/approximer des chiffres (multiples comparables, DCF) sans les sourcer
- Abandonner après un premier échec de sous-agent sans réessayer
- Sauter qa-pipeline, multi-ia-router, feedback-loop, retex-evolution

**Why:** Le 07/04/2026, sur une analyse Thales classée FULL, j'ai livré 4 WebSearch, 0 WebFetch primaire, 0 MCP financier, 0 DCF réel, comparables approximatifs. L'utilisateur a explicitement exigé que les skills soient respectés dans leur intégralité — la qualité prime sur la rapidité, toujours.

**How to apply:** Avant de livrer une réponse issue d'un skill, vérifier que CHAQUE phase prévue a été exécutée. Si une ressource échoue (sous-agent, MCP), réessayer ou trouver un fallback — ne jamais dégrader silencieusement. Si le budget contexte est serré, le dire explicitement à l'utilisateur au lieu de livrer un travail partiel étiqueté complet.
