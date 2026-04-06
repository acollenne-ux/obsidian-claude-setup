---
name: Obsidian skills et MCP installés
description: 5 skills Obsidian (kepano + pablo-mano) + MCP mcp-obsidian installés le 06/04/2026
type: project
---

## Installation Obsidian — 06/04/2026

### MCP Server
- `mcp-obsidian` (MarkusPfundstein) ajouté via `claude mcp add mcp-obsidian -- uvx mcp-obsidian`
- Nécessite plugin Obsidian **"Local REST API"** + clé API dans env `OBSIDIAN_API_KEY`
- Port par défaut : 27124
- **Status : en attente de la clé API utilisateur**

### Skills Kepano (github.com/kepano/obsidian-skills)
- `obsidian-markdown` (5.5 KB) — Obsidian Flavored Markdown, wikilinks, embeds, callouts, properties
- `obsidian-bases` (13.4 KB) — Fichiers .base, vues dynamiques, filtres, formules
- `json-canvas` (7.9 KB) — JSON Canvas, nodes, edges, groups, mind maps
- `defuddle` (1.2 KB) — Extraction markdown propre depuis pages web

### Skill Pablo Mano (github.com/pablo-mano/Obsidian-CLI-skill)
- `obsidian-cli` (13.7 KB) — 130+ commandes CLI Obsidian (fichiers, notes, recherche, propriétés, tâches, liens, plugins, sync)
- Nécessite Obsidian Desktop v1.12.0+ avec CLI activé (Settings → Command line interface)
- Remplace le CLI de kepano (3.3 KB) car beaucoup plus complet

**Why:** L'utilisateur veut intégrer Obsidian comme base de connaissances connectée à Claude Code.
**How to apply:** Utiliser les skills obsidian-* automatiquement quand l'utilisateur travaille avec des fichiers .md Obsidian, .base, ou .canvas. Le MCP permet lecture/écriture directe dans le vault.
