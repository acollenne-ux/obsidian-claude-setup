---
name: Deep-research FULL — pipeline strict, zéro raccourci
description: En mode FULL (ou par défaut), deep-research DOIT exécuter toutes les couches L1→L6, multi-IA, double livrable PDF+PPT, QA. Aucun raccourci pragmatique toléré.
type: feedback
---

**Règle :** Quand deep-research est invoqué (surtout en mode FULL), TOUTES les couches de l'arborescence 7 doivent être exécutées sans exception :

- **L1 THINK** : `superpowers:brainstorming` + `project-analysis` (si code) + `team-agent`
- **L3 SPECIALIST 1er passage (cadrage)** : skills métier définissent les données à chercher AVANT L2
- **L2 RESEARCH** : `multi-ia-router` (consensus Gemini + Mistral + Groq + DeepSeek) OBLIGATOIRE, WebSearch ≥8, WebFetch, MCPs pertinents (Bigdata.com, MT Newswires, Alpha Vantage/FMP pour finance)
- **L3 SPECIALIST 2e passage (analyse)** : skills métier consomment la recherche, aller-retours L3↔L2 si lacunes
- **L4 DELIVERY DOUBLE** : `pdf-report-pro` (pipeline 9 phases, PAS `send_report.py` direct) **ET** `ppt-creator` (deck .pptx éditable) en parallèle
- **L5 QA** : `qa-pipeline` + `layout-qa` (verdict PASS requis, max 3 itérations)
- **L6 META** : `feedback-loop` + `retex-evolution`

**Interdits absolus en mode FULL :**
- Bypasser `multi-ia-router` sous prétexte de rapidité
- Livrer un PDF sans PPT (sauf override utilisateur explicite dans le message courant)
- Appeler `send_report.py` directement au lieu du pipeline `pdf-report-pro`
- Skipper `qa-pipeline` / `layout-qa`
- Skipper les boucles L3↔L2 (recherche à l'aveugle)
- Sauter `retex-evolution` en fin de session

**Why:** Incident 2026-04-09 sur analyse Indra Sistemas — mode FULL validé par l'utilisateur, mais j'ai sauté multi-ia-router, brainstorming, team-agent, specialists finance, ppt-creator, qa-pipeline, layout-qa et retex-evolution. Arbitrage pragmatique erroné après que 2 sous-agents aient échoué (pas d'accès web). L'utilisateur a détecté et demandé correction complète. Qualité > rapidité, toujours.

**How to apply:**
- Dès que deep-research est invoqué, créer un TodoWrite explicite avec une ligne par couche L1→L6 obligatoire, et ne JAMAIS marquer `completed` une couche si un skill obligatoire a été sauté.
- Si un outil échoue (agent sans web, MCP down), ne pas compenser en sautant des couches — relancer avec un outil alternatif (WebSearch direct, autre MCP, multi-ia-router).
- Si contrainte technique force un skip réel, le signaler explicitement à l'utilisateur dans la réponse AVANT livraison.
- Checklist de vérification finale avant d'envoyer la réponse : "Ai-je invoqué multi-ia-router ? ppt-creator ? qa-pipeline ? layout-qa ? retex-evolution ?" — si une réponse est NON en mode FULL → corriger avant de livrer.
