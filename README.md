# Obsidian + Claude Code — Setup complet

Configuration complète pour connecter Obsidian à Claude Code (CLI, Desktop et claude.ai).

## Contenu

### Skills (kepano + pablo-mano)
| Skill | Description |
|-------|-------------|
| `obsidian-markdown` | Obsidian Flavored Markdown, wikilinks, embeds, callouts, properties |
| `obsidian-bases` | Fichiers .base (vues dynamiques, filtres, formules) |
| `json-canvas` | JSON Canvas (mind maps, flowcharts, nodes, edges) |
| `obsidian-cli` | 130+ commandes CLI Obsidian (pablo-mano) |
| `defuddle` | Extraction markdown propre depuis pages web |

### MCP Server
- **mcp-obsidian** (MarkusPfundstein) via `uvx`
- Nécessite le plugin Obsidian **"Local REST API"** (coddingtonbear)

---

## Installation rapide

### 1. Plugin Obsidian
- Obsidian → Settings → Community plugins → Browse → "Local REST API" → Install → Enable
- Noter la **clé API** dans Settings → Local REST API

### 2. Skills (Claude Code CLI)
```bash
# Cloner et copier les skills
git clone https://github.com/Alex33140/obsidian-claude-setup.git
cp -r obsidian-claude-setup/skills/* ~/.claude/skills/
```

### 3. MCP Server (Claude Code CLI)
```bash
# Ajouter le MCP
claude mcp add mcp-obsidian -- uvx mcp-obsidian

# Configurer la clé API (remplacer YOUR_API_KEY)
# Dans ~/.claude.json, ajouter dans env du MCP :
# "OBSIDIAN_API_KEY": "YOUR_API_KEY"
```

### 4. Claude.ai (version web) — Tunnel requis

Claude.ai ne peut pas accéder à `localhost:27124`. Il faut exposer l'API via un tunnel.

#### Option A : Cloudflare Tunnel (recommandé, gratuit)
```bash
# Installer cloudflared
winget install Cloudflare.cloudflared

# Lancer le tunnel (Obsidian doit être ouvert)
cloudflared tunnel --url https://localhost:27124
```
Copier l'URL générée (ex: `https://xxxxx.trycloudflare.com`) et l'ajouter comme MCP dans claude.ai.

#### Option B : ngrok
```bash
# Installer ngrok
winget install ngrok.ngrok

# Lancer le tunnel
ngrok http https://localhost:27124
```

#### Ajouter sur claude.ai
1. Aller sur claude.ai → Settings → MCP Servers
2. Ajouter un nouveau serveur HTTP
3. URL : l'URL du tunnel (ex: `https://xxxxx.trycloudflare.com`)
4. Header Authorization : `Bearer YOUR_API_KEY`

---

## Configuration MCP complète (.claude.json)

```json
{
  "mcp-obsidian": {
    "type": "stdio",
    "command": "uvx",
    "args": ["mcp-obsidian"],
    "env": {
      "OBSIDIAN_API_KEY": "YOUR_API_KEY",
      "OBSIDIAN_HOST": "127.0.0.1",
      "OBSIDIAN_PORT": "27124"
    }
  }
}
```

## Test de connexion

```bash
curl -s -k -H "Authorization: Bearer YOUR_API_KEY" https://127.0.0.1:27124/
# Réponse attendue : {"status":"OK","authenticated":true,...}

curl -s -k -H "Authorization: Bearer YOUR_API_KEY" https://127.0.0.1:27124/vault/
# Liste les fichiers du vault
```

## Prérequis
- Obsidian Desktop v1.12.0+
- Plugin "Local REST API" activé
- Obsidian doit être **ouvert** pour que l'API fonctionne
- Python `uvx` (via `uv`) pour le MCP server
- Pour claude.ai : cloudflared ou ngrok pour le tunnel

## Sources
- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
- [pablo-mano/Obsidian-CLI-skill](https://github.com/pablo-mano/Obsidian-CLI-skill)
- [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian)
- [coddingtonbear/obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api)
