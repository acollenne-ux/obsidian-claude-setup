# Memory — Alexandre collenne

## Skills pdf-report-pro & ppt-creator (testés 2026-04-07)
- Les deux skills sont fonctionnels end-to-end sur ce poste.
- pdf-report-pro : pipeline HTML → Playwright `page.pdf()` (WeasyPrint KO sur Windows, fallback auto via `tools/weasyprint_render.py`).
- ppt-creator : `tools/build_templates.py` génère les 5 templates `.pptx` ; `tools/pptx_builder.py` produit les decks (bug import `pptx.dgm.color` corrigé).
- **pptx → pdf : LibreOffice INTERDIT.** Solution retenue = rendu HTML parallèle du deck + Playwright `page.pdf()` (option A). Sinon livraison `.pptx` seul.
- Démos validées : `C:\tmp\demo_pdf_report_pro.pdf` (75 KB) + `C:\tmp\demo_ppt_creator.pptx` (37 KB, 5 slides).

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
- Skills installés: stock-analysis, macro-analysis, dev-team, install-plugin, project-analysis, financial-modeling, code-debug, data-analysis, desktop-control (mars 2026), image-detourage, image-enhancer, flyer-creator (05/04/2026), website-analyzer (06/04/2026), obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle (06/04/2026), skill-creator v2 (06/04/2026), gsheet-builder (09/04/2026), image-generator (09/04/2026)
- MCP Obsidian: `mcp-obsidian` via uvx (nécessite plugin Obsidian "Local REST API" + clé API)
- PyAutoGUI v0.9.54 installé sur Python 3.13 (contrôle bureau Windows)

## Architecture Skills (refactorisée 04/04/2026)

### Orchestrateur principal
- `deep-research` — Orchestrateur léger (~374 lignes) qui classe la complexité (LITE/STANDARD/FULL), détecte les domaines, et dispatche vers les skills spécialisés ci-dessous

### Skills spécialisés (invoqués par deep-research)
- `multi-ia-router` — Routage IA, curl templates, consensus voting, fallback chains (6 providers)
- `financial-analysis-framework` — 8 types d'actifs + 15 dimensions + synthèse bull/base/bear
- `qa-pipeline` — Agents QA anti-hallucination, Source Validator, Confidence Scorer
- `pdf-report-gen` v2 — Pipeline 5 agents (Synthesizer/Designer/Visualizer/Composer/Reviewer) + moteur Playwright + 5 templates CSS + QC auto + Mermaid (07/04/2026)
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
- `idea-to-diagram` — AUTO sur schéma/diagramme/synthèse visuelle/mind map/flowchart (6 phases + 5 agents : extractor, architect MECE, selector Abela, generator, qa-critic Tufte)
- `diagram-toolkit` — Bibliothèque technique : 10 templates (pyramid/scqa/mece/matrix2x2/c4/fishbone/causal-loop/roadmap/sequence/venn) + 4 thèmes (mckinsey/bcg/mono/dark) + render.py multi-format
- `image-generator` — AUTO sur génération image IA/text-to-image (multi-provider FLUX/GPT-Image/Nano Banana 2/SDXL, 3 agents, routeur intelligent)

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
- [Deep-research v3 règles](feedback_deep_research_v3.md) — Pas de LITE, choix user STANDARD/FULL avant exécution, multi-skills par couche, aller-retours L3↔L2 obligatoires
- [Arbre Skills 5 couches obligatoire](feedback_arbre_skills_obligatoire.md) — Respecter intégralement l'arbre 5 couches + chaque SKILL.md ; livrable C4 obligatoire
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
- [Skill image-studio 07/04](project_image_studio_20260407.md) — Studio visuel unifié 8 phases, 5 agents, art-director critique, fidélité brief + images réelles
- [pdf-report-pro v2 07/04](project_pdf_report_pro_v2_20260407.md) — Refonte : Typst moteur principal, 9 phases, baseline grid 8pt, PDF/UA, checklist 20 critères, score 92/100
- [Respecter skills intégralement](feedback_respect_skills_integralement.md) — JAMAIS de raccourcis : toutes les phases, tous les agents, tous les outils — qualité > rapidité
- [PDF Report Gen v2 07/04](project_pdf_report_gen_v2_20260407.md) — Refonte complete pdf-report-gen : 5 agents + pdf_engine modulaire (Playwright) + 5 templates CSS + QC auto + Mermaid + modify_pdf.py
- [pdf-report-pro 07/04](project_pdf_report_pro_20260407.md) — Refonte McKinsey/BCG/Goldman, 6 phases, 5 templates HTML/CSS, WeasyPrint+Playwright, score audit 97/100
- [ppt-creator 07/04](project_ppt_creator_20260407.md) — Nouveau skill .pptx éditable McKinsey/BCG, ghost deck validé utilisateur, python-pptx, score audit 97/100
- [Skills carrière 07/04](project_career_skills_20260407.md) — cv-creator + cover-letter-creator (Typst + HTML/Playwright + JSON Resume), 6 templates CV, 4 frameworks lettres, ATS-safe
- [idea-to-diagram + diagram-toolkit 08/04](project_idea_to_diagram_20260408.md) — 2 skills + 5 agents pour synthèse visuelle pro (Pyramid/MECE/Abela/Tufte), Mermaid/D2/Graphviz/Typst, thèmes McKinsey/BCG
- [N8N Management 08/04](project_n8n_management_20260408.md) — Skill orchestrateur n8n-management (89/100) + 7 skills officiels czlonkowski + 3 agents (architect/debugger/validator) + MCP n8n-mcp **mode docs-only** (✓ Connected, install globale, démarrage via `node` direct — pas de `npx -y` qui timeout)
- [Antigravity skill 08/04](project_antigravity_skill_20260408.md) — Connecteur Google Antigravity free tier (Claude Opus 4.6 natif inclus), L3 SPECIALIST, bridge MCP unidirectionnel Claude→Antigravity, **hard-gate anti-ban-wave** (jamais antigravity-cli/openclaw/proxies tiers)
- [Gemini CLI skill 08/04](project_gemini_cli_skill_20260408.md) — Wrapper Gemini CLI officiel, ~1000 req/jour Gemini 3 Pro OAuth gratuit, fallback auto multi-ia-router
- [Gemini co-moteur vision](feedback_gemini_for_visuals.md) — OBLIGATOIRE : Claude Opus appelle Gemini 3 Pro via gemini-cli pour toute image/diagramme/visuel (hard-gates ajoutés à image-studio et idea-to-diagram)
- [Gemini CLI skill 08/04](project_gemini_cli_skill_20260408.md) — Wrapper Gemini CLI officiel Google (~1000 req/jour Gemini 3 Pro gratuit via OAuth), skill utilitaire L3, fallback auto multi-ia-router, pour vision image→code / diagrammes / fallback quand quotas Claude tapés
- [Deep-research FULL strict](feedback_deep_research_full_pipeline_strict.md) — Mode FULL = toutes couches L1→L6, multi-IA, PDF+PPT, QA, retex. Zéro raccourci. Incident Indra 09/04.
- [Token Economizer Suite 08/04](project_token_economizer_20260408.md) — 5 skills L6 (token-economizer + prompt-cache-manager + haiku-delegator + context-compressor + adaptive-thinking-router), hook Phase 0B-bis deep-research, principe reasoning-first, cible −70% tokens +qualité ≥baseline+10%
- [gsheet-builder 09/04](project_gsheet_builder_20260409.md) — Skill L4 DELIVERY Google Sheets consulting-grade, 8 phases, 5 agents, 5 themes McKinsey/Goldman, 6 templates YAML, 31 outils MCP, QA 15 critères seuil 85/100
- [image-generator 09/04](project_image_generator_20260409.md) — Skill L3 text-to-image multi-provider (FLUX/GPT-Image/Nano Banana 2/SDXL), 3 agents, 4 scripts Python, Pipeline E image-enhancer
