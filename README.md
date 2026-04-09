# Claude Code — Ecosystem complet (Skills, Agents, Tools, MCP)

Configuration complète de l'écosystème Claude Code : **54 skills**, tools Python, hooks, memory, settings.
Compatible CLI, Desktop et claude.ai web.

> Dernière sync : 09/04/2026

## Structure du repo

```
.
├── CLAUDE.md              # Instructions globales Claude Code
├── settings.json          # Configuration plugins/permissions
├── settings.local.json    # Permissions locales (machine-specific)
├── statusline.py          # Barre de statut custom (CTX%, rate limits, coûts)
├── skills/                # 54 skills (SKILL.md + references/)
├── tools/                 # Scripts Python (email, multi-IA, charts, PDF engine)
├── hooks/                 # Hooks automatiques (image studio, skill tree)
├── memory/                # Fichiers mémoire projet/feedback/reference
└── .claude/skills/        # Skills Obsidian (symlinks)
```

## Skills installés (54)

### Orchestration & Routage (8)
| Skill | Description |
|-------|-------------|
| `deep-research` | Orchestrateur principal — dispatch STANDARD/FULL, multi-skills |
| `multi-ia-router` | Routage multi-IA, consensus voting, fallback chains (6 providers) |
| `team-agent` | Orchestration d'agents parallèles |
| `adaptive-thinking-router` | Pilotage thinking.effort (low/medium/high) |
| `haiku-delegator` | Délégation tâches mécaniques vers Haiku |
| `token-economizer` | Économie de tokens reasoning-first (-70% cible) |
| `context-compressor` | Compression hiérarchique 4 niveaux |
| `prompt-cache-manager` | Prompt caching Anthropic (ephemeral + 1h TTL) |

### Développement (3)
| Skill | Description |
|-------|-------------|
| `code-debug` | Débogage avancé avec root cause analysis |
| `dev-team` | Création code/app, architecture multi-agents |
| `project-analysis` | Analyse projet avant développement |

### Skills Management (2)
| Skill | Description |
|-------|-------------|
| `skill-creator` | Création/amélioration/audit de skills (7 phases, scoring /100) |
| `skill-tree-manager` | Gestion arborescence intelligente des skills |

### Finance & Trading (4)
| Skill | Description |
|-------|-------------|
| `financial-analysis-framework` | 8 types d'actifs + 15 dimensions + bull/base/bear |
| `financial-modeling` | DCF, comps, LBO, valorisation |
| `stock-analysis` | Analyse boursière complète |
| `macro-analysis` | Macro, politique monétaire, cycles |

### Création & Médias (10)
| Skill | Description |
|-------|-------------|
| `image-studio` | Studio visuel unifié 8 phases, 5 agents, art-director |
| `image-generator` | Text-to-image multi-provider (FLUX/GPT-Image/SDXL) |
| `image-enhancer` | Upscale/restauration (Real-ESRGAN, GFPGAN) |
| `image-detourage` | Détourage IA 7 étapes (rembg + PyMatting) |
| `flyer-creator` | Flyers pro HTML/CSS + Playwright |
| `idea-to-diagram` | Synthèse visuelle (Pyramid/MECE/Abela/Tufte) |
| `diagram-toolkit` | 10 templates + 4 thèmes (McKinsey/BCG/mono/dark) |
| `layout-qa` | QA visuelle obligatoire avant livraison |
| `website-analyzer` | Audit web complet, 4 agents, 10 dimensions |
| `frontend-design` | Design frontend (plugin superpowers) |

### Documents & Rapports (6)
| Skill | Description |
|-------|-------------|
| `pdf-report-gen` | Pipeline 5 agents + Playwright + 5 templates CSS |
| `pdf-report-pro` | Rapports McKinsey/BCG/Goldman 9 phases |
| `ppt-creator` | Présentations .pptx éditables McKinsey/BCG |
| `cv-creator` | CV pro ATS-friendly (6 templates, Typst + HTML) |
| `cover-letter-creator` | Lettres de motivation (4 frameworks) |
| `gsheet-builder` | Google Sheets consulting-grade (8 phases, 5 thèmes) |

### n8n / Automation (8)
| Skill | Description |
|-------|-------------|
| `n8n-management` | Orchestrateur n8n : créer, déboguer, déployer |
| `n8n-code-javascript` | Code JavaScript dans n8n Code nodes |
| `n8n-code-python` | Code Python dans n8n Code nodes |
| `n8n-expression-syntax` | Validation syntaxe expressions n8n |
| `n8n-mcp-tools-expert` | Guide expert outils MCP n8n |
| `n8n-node-configuration` | Configuration nodes (operation-aware) |
| `n8n-validation-expert` | Interprétation erreurs validation |
| `n8n-workflow-patterns` | Patterns architecturaux workflows n8n |

### Obsidian (5)
| Skill | Description |
|-------|-------------|
| `obsidian-markdown` | Obsidian Flavored Markdown (wikilinks, embeds) |
| `obsidian-bases` | Fichiers .base (vues dynamiques, filtres) |
| `obsidian-cli` | 130+ commandes CLI Obsidian |
| `json-canvas` | JSON Canvas (mind maps, flowcharts) |
| `defuddle` | Extraction markdown depuis pages web |

### Data & Système (2)
| Skill | Description |
|-------|-------------|
| `data-analysis` | Pandas, numpy, stats, visualisation |
| `desktop-control` | Contrôle bureau Windows (PyAutoGUI) |

### Qualité & Feedback (4)
| Skill | Description |
|-------|-------------|
| `qa-pipeline` | QA anti-hallucination, validation sources |
| `feedback-loop` | Collecte feedback utilisateur |
| `retex-evolution` | RETEX + benchmark IAs + amélioration continue |
| `install-plugin` | Installation plugins/MCP/skills |

### Utilitaires (2)
| Skill | Description |
|-------|-------------|
| `gemini-cli` | Wrapper Gemini CLI (~1000 req/jour gratuit via OAuth) |
| `antigravity` | Connecteur Google Antigravity free tier |

## Hooks automatiques

| Hook | Trigger | Fichier |
|------|---------|---------|
| Image Studio Auto | `UserPromptSubmit` | `hooks/image_studio_trigger.py` |
| Skill Tree Rebuild | `PostToolUse` (Write/Edit) | `hooks/skill_tree_autorebuild.py` |

## Installation

### Option 1 : Cloner et copier (CLI/Desktop)

```bash
git clone https://github.com/acollenne-ux/obsidian-claude-setup.git
cd obsidian-claude-setup

# Copier les skills
cp -r skills/* ~/.claude/skills/

# Copier les tools
cp tools/*.py ~/.claude/tools/
cp tools/*.bat ~/.claude/tools/
cp -r tools/pdf_engine ~/.claude/tools/

# Copier les hooks
mkdir -p ~/.claude/hooks
cp hooks/*.py ~/.claude/hooks/

# Copier les configs
cp CLAUDE.md ~/.claude/CLAUDE.md
cp settings.json ~/.claude/settings.json
cp statusline.py ~/.claude/statusline.py

# Copier la memory
cp memory/*.md ~/.claude/projects/*/memory/ 2>/dev/null
```

### Option 2 : Ouvrir comme projet (claude.ai web)

1. Fork ou clone ce repo
2. Ouvre-le comme projet dans claude.ai
3. Les skills dans `skills/` sont automatiquement disponibles
4. Le `CLAUDE.md` à la racine est lu automatiquement

## MCP Servers configurés

| MCP | Usage | Type |
|-----|-------|------|
| `mcp-obsidian` | Accès vault Obsidian | stdio (uvx) |
| `tradingview-mcp` | 78 outils TradingView | local (port 9222) |
| `alpha-vantage` | Données financières US | MCP |
| `google-sheets` | Google Sheets API | MCP |
| `n8n-mcp` | Automation n8n (mode docs-only) | MCP |
| Bigdata.com | Données financières | Remote (claude.ai) |
| LunarCrush | Sentiment crypto | Remote (claude.ai) |
| Crypto.com | Prix crypto live | Remote (claude.ai) |
| Context7 | Docs techniques | Remote (claude.ai) |
| Hugging Face | Papers académiques | Remote (claude.ai) |
| Figma | Design UI | Remote (claude.ai) |

## Tools Python

| Script | Usage |
|--------|-------|
| `send_report.py` | Génération PDF + envoi email |
| `multi_ai.py` | Appels multi-IA (Gemini, Mistral, Groq, etc.) |
| `chart_generator.py` | Graphiques pro (6 types) |
| `retex_manager.py` | Gestion RETEX et benchmark IAs |
| `email_trigger.py` | Bridge email → Claude Code |
| `modify_pdf.py` | Modification PDF post-génération |
| `pdf_engine/` | Moteur PDF modulaire (Playwright, Mermaid, templates) |

## Tunnel Obsidian pour claude.ai web

Pour accéder au vault Obsidian depuis claude.ai :

```bash
# Windows
start-tunnel.bat

# Linux/macOS
bash start-tunnel.sh
```

Nécessite : Obsidian ouvert + plugin "Local REST API" + cloudflared installé.

## Sources
- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
- [pablo-mano/Obsidian-CLI-skill](https://github.com/pablo-mano/Obsidian-CLI-skill)
- [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian)
