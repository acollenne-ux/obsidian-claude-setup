# Claude Code — Ecosystem complet (Skills, Agents, Tools, MCP)

Configuration complète de l'écosystème Claude Code : 28 skills, tools Python, memory, settings.
Compatible CLI, Desktop et claude.ai web.

## Structure du repo

```
.
├── CLAUDE.md              # Instructions globales Claude Code
├── settings.json          # Configuration plugins/permissions
├── skills/                # 28 skills (SKILL.md + references/)
├── tools/                 # Scripts Python (email, multi-IA, charts, etc.)
└── memory/                # Fichiers mémoire projet/feedback/user
```

## Skills installés (28)

### Orchestration
| Skill | Score | Description |
|-------|-------|-------------|
| `deep-research` | 80.5% | Orchestrateur principal — dispatch LITE/STANDARD/FULL |
| `multi-ia-router` | 75.0% | Routage multi-IA, consensus voting, fallback chains |
| `team-agent` | 78.0% | Orchestration d'agents parallèles |

### Développement
| Skill | Score | Description |
|-------|-------|-------------|
| `code-debug` | 86.5% | Débogage avancé avec root cause analysis |
| `dev-team` | 76.5% | Création code/app, architecture |
| `project-analysis` | 81.0% | Analyse projet avant développement |
| `skill-creator` | 90.0% | Création/amélioration/audit de skills |

### Finance & Trading
| Skill | Score | Description |
|-------|-------|-------------|
| `financial-analysis-framework` | 78.5% | 8 types d'actifs + 15 dimensions |
| `financial-modeling` | 74.0% | DCF, comps, LBO, valorisation |
| `stock-analysis` | 79.0% | Analyse boursière complète |
| `macro-analysis` | 79.0% | Macro, politique monétaire, cycles |

### Création & Médias
| Skill | Score | Description |
|-------|-------|-------------|
| `flyer-creator` | 73.0% | Flyers pro HTML/CSS + Playwright |
| `image-detourage` | 73.0% | Détourage IA 7 étapes (rembg + PyMatting) |
| `image-enhancer` | 75.5% | Upscale/restauration (Real-ESRGAN) |
| `website-analyzer` | 71.0% | Audit web complet, 4 agents, 10 dimensions |
| `frontend-design` | — | Design frontend (plugin superpowers) |

### Obsidian
| Skill | Score | Description |
|-------|-------|-------------|
| `obsidian-markdown` | 75.5% | Obsidian Flavored Markdown |
| `obsidian-bases` | 67.5% | Fichiers .base (vues dynamiques, filtres) |
| `obsidian-cli` | 70.5% | 130+ commandes CLI Obsidian |
| `json-canvas` | 77.5% | JSON Canvas (mind maps, flowcharts) |

### Data & Analyse
| Skill | Score | Description |
|-------|-------|-------------|
| `data-analysis` | 86.0% | Pandas, numpy, stats, visualisation |
| `desktop-control` | 79.0% | Contrôle bureau Windows (PyAutoGUI) |
| `defuddle` | 64.0% | Extraction markdown depuis pages web |

### Qualité & Feedback
| Skill | Score | Description |
|-------|-------|-------------|
| `qa-pipeline` | 76.0% | QA anti-hallucination, validation sources |
| `pdf-report-gen` | 76.0% | Rapports PDF Markdown + email |
| `feedback-loop` | 76.0% | Collecte feedback utilisateur |
| `retex-evolution` | 76.0% | RETEX + benchmark IAs + amélioration |
| `install-plugin` | 72.0% | Installation plugins/MCP/skills |

**Score moyen : 75.1%** (audit automatique via `scripts/audit_skills.py`)

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

# Copier le CLAUDE.md (instructions globales)
cp CLAUDE.md ~/.claude/CLAUDE.md

# Copier les settings
cp settings.json ~/.claude/settings.json
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
