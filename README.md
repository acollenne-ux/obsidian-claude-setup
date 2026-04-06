# Obsidian + Claude Code — Setup complet

Configuration complète pour connecter Obsidian à Claude Code (CLI, Desktop et claude.ai web).

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
1. Ouvre **Obsidian** → Settings → Community plugins → Browse
2. Cherche **"Local REST API"** → Install → Enable
3. Va dans Settings → Local REST API → copie la **clé API**

### 2. Skills (Claude Code CLI ou Web)

```bash
# Cloner le repo
git clone https://github.com/acollenne-ux/obsidian-claude-setup.git

# Copier les skills dans le profil Claude Code
cp -r obsidian-claude-setup/skills/* ~/.claude/skills/
```

> **Note :** Les skills sont aussi dans `.claude/skills/` du projet. Si tu ouvres ce repo dans Claude Code (CLI ou web), les skills sont automatiquement disponibles.

### 3. MCP Server (Claude Code CLI)
```bash
# Ajouter le MCP
claude mcp add mcp-obsidian -- uvx mcp-obsidian

# Configurer la clé API dans ~/.claude.json :
# "env": { "OBSIDIAN_API_KEY": "TA_CLE_API" }
```

---

## Utiliser sur claude.ai (version web)

Claude.ai ne peut pas accéder à `localhost:27124`. Il faut exposer l'API Obsidian via un **tunnel Cloudflare**.

### Étape 1 : Installer cloudflared

```bash
# Windows
winget install Cloudflare.cloudflared

# macOS
brew install cloudflared

# Linux
sudo apt install cloudflared
```

### Étape 2 : Lancer le tunnel

**Windows** (double-clic ou cmd) :
```cmd
start-tunnel.bat
```

**Linux/macOS** :
```bash
bash start-tunnel.sh
```

**Ou manuellement** :
```bash
cloudflared tunnel --url https://localhost:27124 --no-tls-verify
```

> **IMPORTANT :** L'option `--no-tls-verify` est obligatoire car Obsidian utilise un certificat auto-signé. Sans cette option, le tunnel retourne une erreur 502.

Cloudflared affiche une URL du type :
```
https://quelquechose-random.trycloudflare.com
```

### Étape 3 : Configurer sur claude.ai

1. Va sur **claude.ai** → clique sur ton profil (en bas à gauche)
2. **Settings** → **Integrations** (ou MCP Servers)
3. **Add Integration** / Add MCP Server
4. Configure :
   - **URL** : colle l'URL du tunnel (ex: `https://xxx.trycloudflare.com`)
   - **Header Name** : `Authorization`
   - **Header Value** : `Bearer TA_CLE_API`
5. Sauvegarde

### Rappels importants

- **Obsidian doit être ouvert** pour que l'API fonctionne
- **Le terminal cloudflared ne doit pas être fermé** (le tunnel s'arrête sinon)
- **L'URL change** à chaque relancement de cloudflared
- **Fonctionne sur tous les projets** claude.ai une fois configuré au niveau du compte

---

## Configuration MCP complète (.claude.json)

```json
{
  "mcp-obsidian": {
    "type": "stdio",
    "command": "uvx",
    "args": ["mcp-obsidian"],
    "env": {
      "OBSIDIAN_API_KEY": "TA_CLE_API",
      "OBSIDIAN_HOST": "127.0.0.1",
      "OBSIDIAN_PORT": "27124"
    }
  }
}
```

## Test de connexion

```bash
# Test direct (local)
curl -s -k -H "Authorization: Bearer TA_CLE_API" https://127.0.0.1:27124/
# Réponse attendue : {"status":"OK","authenticated":true,...}

# Test via tunnel
curl -s -H "Authorization: Bearer TA_CLE_API" https://xxx.trycloudflare.com/
# Même réponse attendue

# Lister les fichiers du vault
curl -s -k -H "Authorization: Bearer TA_CLE_API" https://127.0.0.1:27124/vault/
```

## Prérequis
- Obsidian Desktop v1.12.0+
- Plugin "Local REST API" activé
- Obsidian doit être **ouvert** pour que l'API fonctionne
- Python `uvx` (via `uv`) pour le MCP server en local
- Pour claude.ai web : `cloudflared` pour le tunnel

## Sources
- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
- [pablo-mano/Obsidian-CLI-skill](https://github.com/pablo-mano/Obsidian-CLI-skill)
- [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian)
- [coddingtonbear/obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api)
