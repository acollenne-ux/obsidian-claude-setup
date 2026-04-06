# Obsidian + Claude Code Setup

Ce projet contient la configuration complete pour connecter Obsidian a Claude Code
(CLI, Desktop et claude.ai web).

## Skills Obsidian disponibles

Les skills dans `.claude/skills/` enseignent a Claude comment manipuler les fichiers Obsidian :

- **obsidian-markdown** : Obsidian Flavored Markdown (wikilinks, embeds, callouts, properties, tags)
- **obsidian-bases** : Fichiers .base (vues dynamiques, filtres, formules, summaries)
- **json-canvas** : JSON Canvas (.canvas) pour mind maps, flowcharts, diagrammes
- **obsidian-cli** : 130+ commandes CLI Obsidian (lecture, ecriture, recherche, taches, proprietes, sync)
- **defuddle** : Extraction markdown propre depuis pages web

## MCP Obsidian

Le MCP `mcp-obsidian` (MarkusPfundstein) permet l'acces direct au vault Obsidian via l'API REST.

### Prerequis
- Obsidian Desktop v1.12.0+ ouvert
- Plugin "Local REST API" active (port 27124)
- Variable `OBSIDIAN_API_KEY` configuree

### Pour claude.ai web
Claude.ai ne peut pas acceder a localhost. Un tunnel Cloudflare est necessaire :
```bash
# Windows
start-tunnel.bat

# Linux/macOS
bash start-tunnel.sh
```
L'option `--no-tls-verify` est requise car Obsidian utilise un certificat auto-signe.

## Conventions pour les fichiers Obsidian

- Utiliser les wikilinks `[[Note]]` pour les liens internes au vault
- Utiliser le frontmatter YAML pour les proprietes (tags, aliases, cssclasses)
- Les chemins sont relatifs au vault (pas de chemins absolus)
- Extension `.md` pour les notes, `.base` pour les bases, `.canvas` pour les canvas
