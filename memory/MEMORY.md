# Memory — Alexandre collenne

## Environnement
- OS: Windows 10 Home 10.0.19045 (bash via Git Bash)
- Shell: bash (Unix syntax dans les Bash tool calls)
- Python: `C:\Users\Alexandre collenne\AppData\Local\Programs\Python\Python313\python.exe`
- Node.js: `C:\Program Files\nodejs\node.exe`
- Disque C:: ~81 GB total, ~20 GB libres après nettoyage (mars 2026)
- RAM: 12 GB total (upgrade depuis 4 GB le 05/04/2026 — birefnet et Real-ESRGAN désormais utilisables)

## Configuration Claude Code
- Statusline: `~/.claude/statusline.py` (Python, UTF-8, ANSI colors)
  - Affiche: CTX%, rate limits 5h + **7d** (avec ↺ temps restant), coût session, modèle
  - Couleurs: vert <60%, jaune 60-85%, rouge >85%
- Settings: `~/.claude/settings.json`
- Skills installés: stock-analysis, macro-analysis, dev-team, install-plugin, project-analysis, financial-modeling, code-debug, data-analysis, desktop-control (mars 2026), image-detourage, image-enhancer, flyer-creator (05/04/2026), website-analyzer (06/04/2026), obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle (06/04/2026), skill-creator v2 (06/04/2026)
- MCP Obsidian: `mcp-obsidian` via uvx (nécessite plugin Obsidian "Local REST API" + clé API)
- PyAutoGUI v0.9.54 installé sur Python 3.13 (contrôle bureau Windows)

## Architecture Skills (refactorisée 04/04/2026)

### Orchestrateur principal
- `deep-research` — Orchestrateur léger (~374 lignes) qui classe la complexité (LITE/STANDARD/FULL), détecte les domaines, et dispatche vers les skills spécialisés ci-dessous

### Skills spécialisés (invoqués par deep-research)
- `multi-ia-router` — Routage IA, curl templates, consensus voting, fallback chains (6 providers)
- `financial-analysis-framework` — 8 types d'actifs + 15 dimensions + synthèse bull/base/bear
- `qa-pipeline` — Agents QA anti-hallucination, Source Validator, Confidence Scorer
- `pdf-report-gen` — Agent Synthèse + PDF Markdown + envoi email
- `feedback-loop` — Collecte feedback utilisateur, boucle correction, métriques satisfaction
- `retex-evolution` — RETEX, benchmark IAs, amélioration continue, monitoring session

### Skills domaine (invoqués selon contexte)
- `project-analysis` — AUTO avant tout projet/code
- `stock-analysis` — AUTO sur mentions marchés/actions
- `macro-analysis` — AUTO sur mentions macro/Fed/BCE
- `dev-team` — AUTO sur création code/app
- `financial-modeling` — AUTO sur DCF/valorisation/comps/LBO
- `code-debug` — AUTO sur erreurs/bugs/stack traces
- `data-analysis` — AUTO sur datasets/graphiques/backtest
- `desktop-control` — Contrôle PC (PyAutoGUI)
- `install-plugin` — Installer plugins/MCP
- `image-detourage` — AUTO sur détourage/suppression fond/fond transparent (pipeline 7 étapes + agent multi-passes)
- `image-enhancer` — AUTO sur upscale/super-résolution/restauration images (Real-ESRGAN, GFPGAN, fallback CPU)
- `flyer-creator` — AUTO sur création flyers/affiches/posters (HTML/CSS + Playwright + post-processing Pillow)
- `website-analyzer` — AUTO sur analyse/audit sites web (Playwright crawler + 4 agents UX/Marketing/Conversion/Brand + scoring 10 dimensions + rapport PDF)
- `skill-creator` — AUTO sur création/amélioration/audit de skills (7 phases, 6 templates, 5 agents, scoring 10 critères /100, script audit Python)

### Ancien monolithe
- Backup : `~/.claude/skills/deep-research/SKILL.md.bak_monolith_2201lines`
- Remplacé par : 7 skills modulaires (1651 lignes total vs 2201 lignes monolithe)

## Préférences utilisateur
- **OBLIGATOIRE : Toujours invoquer `deep-research` EN PREMIER pour TOUTE demande** (type Perplexity, multi-agents)
- **deep-research doit TOUJOURS appeler `superpowers` (brainstorming) + `team-agent` (agents parallèles)**
- **deep-research doit TOUJOURS s'auto-améliorer (Phase 11) après chaque session**
- **Benchmark continu** : deep-research doit tester TOUTES les IAs à chaque demande (`--aggregate`), comparer qualité/vitesse, et mettre à jour les scores de routage
- **TOUJOURS YES** : ne jamais demander confirmation sauf actions destructives irréversibles (>1 GB, push force)
- **PDF toujours en Markdown pur** : JAMAIS de HTML dans send_report.py (bug 28/03/2026)
- **PDF via --file** : Toujours utiliser `send_report.py --file rapport.md` (pas de contenu inline bash, troncature)
- **IAs externes** : 5 providers actifs + 1 solde vide dans ai_config.json :
  - Gemini 2.5 Flash (N°1 code+finance), Mistral Small/Large (N°1 français)
  - Groq llama-3.3/qwen3-32b/gpt-oss-120b (N°1 vitesse), OpenRouter deepseek-r1 (N°1 raisonnement 4.3s)
  - HuggingFace Llama-3.3/R1 (chat 2.0s le + rapide), DeepSeek (solde vide)
- **Classification actifs obligatoire** : 8 types (Growth, Micro-cap, Cyclique, Défensif, REIT, Crypto, Obligation, ETF) avec métriques spécifiques — ne JAMAIS analyser tous les actifs de la même façon
- **Sources finance** : Bloomberg, Reuters, Investing.com, Zonebourse obligatoires pour analyses
- **Auto-check Gmail** : Si clé API manquante, chercher dans Gmail avant de déclarer indisponible
- Langue: Français
- Toujours demander confirmation avant de supprimer >1 GB
- Ne pas toucher aux fichiers utilisateur (Documents, Photos)
- PowerShell inline (-Command) : éviter les $var → utiliser des .ps1 scripts à la place
  (le bash shell échappe mal les $ dans les commandes PowerShell inline)
- Chemins avec [ ] dans PowerShell: utiliser -LiteralPath et cmd /c rmdir pour les supprimer

## PC Nettoyage (mars 2026)
- SolidWorks ISO supprimé: 15.17 GB
- npm-cache, pip, caches: ~1.7 GB
- Architecte 3DHD supprimé: 0.94 GB
- Démarrage désactivé: Discord, Perplexity, OneDrive
- vm_bundles Claude (12.94 GB) conservés à la demande de l'utilisateur
- Email bridge: `start_email_trigger.vbs` dans dossier Démarrage Windows (permanent, invisible)

## Memory Files
- [PDF Markdown only](feedback_pdf_markdown_only.md) — send_report.py = Markdown, jamais HTML
- [Always deep-research](feedback_always_deep_research.md) — Toujours invoquer deep-research en premier
- [Always YES](feedback_always_yes.md) — Ne jamais demander confirmation sauf destructif
- [Deep-research evolution](feedback_deep_research_evolution.md) — Superpowers + team-agent + Phase 11 obligatoire
- [API keys reference](reference_api_keys.md) — Emplacement clés API dans ai_config.json
- [Benchmark continu](feedback_benchmark_continu.md) — Tester toutes les IAs à chaque demande pour améliorer le routage
- [Session 28/03 upgrades](project_session_20260328_upgrades.md) — Benchmark IAs, routage intelligent, classification 8 types actifs, fix providers, statusline 7d
- [Skill refactoring 04/04](project_skill_refactoring_20260404.md) — Monolithe 2201 lignes → 7 skills modulaires (1651 lignes)
- [Skills image+flyer 05/04](project_skills_image_flyer_20260405.md) — 3 skills installés depuis Gmail ZIP : image-detourage, image-enhancer, flyer-creator
- [TradingView MCP](reference_tradingview_mcp.md) — MCP tradesdontlie/tradingview-mcp local, 78 outils, port 9222
- [Google Sheets MCP](reference_google_sheets_mcp.md) — MCP mcp-gsheets, service account claude-sheets, projet gen-lang-client-0947498109
- [Website Analyzer skill 06/04](project_website_analyzer_20260406.md) — Skill audit web complet, 4 agents, Playwright crawler, 10 dimensions scoring
- [Toujours utiliser skills dédiés](feedback_use_dedicated_skills.md) — Ne JAMAIS bypasser les skills spécialisés au profit d'une analyse manuelle
- [Obsidian skills 06/04](project_obsidian_skills_20260406.md) — 5 skills kepano + CLI pablo-mano + MCP mcp-obsidian
- [Skill Creator v2 06/04](project_skill_creator_20260406.md) — Skill architecte: 7 phases, 6 templates, 5 agents, scoring /100, audit Python (score 90%)
