---
name: antigravity-mcp-bridge
description: Agent qui branche les MCP servers Claude Code existants DANS Antigravity (bridge unidirectionnel Claude → Antigravity).
---

# Agent : Antigravity MCP Bridge

Lit la config MCP de Claude Code, filtre les MCPs pertinents, génère un fichier `antigravity_mcp.json` compatible avec Antigravity, et guide l'import manuel.

## Principe

**Sens unique sûr** : on **expose** les MCPs locaux d'Alexandre à Antigravity. On **ne pilote PAS** Antigravity depuis l'extérieur (interdit ToS).

## Étapes

### 1. Lire la config Claude Code
Sources possibles (ordre de priorité) :
1. `~/.claude.json` (section `mcpServers`)
2. `%APPDATA%/Claude/claude_desktop_config.json`
3. `~/.claude/mcp.json`

Parser le JSON et extraire chaque entrée `mcpServers`.

### 2. Filtrer les MCPs pertinents pour Antigravity

**À inclure par défaut** (utiles pour coder/concevoir/rechercher) :
- `obsidian` (notes/docs)
- `github` (repos)
- `context7` (docs libs)
- `n8n-mcp` (workflows)
- `playwright` (browser control — redondant avec browser agent natif mais utile)
- `google-sheets` (données)
- `tradingview` (si présent)
- `figma` (si présent)

**À EXCLURE** :
- Tout MCP contenant `antigravity-cli`, `openclaw`, `antigravity-claude-proxy`, `antigravity-proxy` → **interdit ToS**.
- Tout MCP contenant des secrets hardcodés dans l'env (les extraire en variable Antigravity).
- MCPs internes Claude Code (desktop-control local, etc.) qui ne fonctionneraient pas depuis Antigravity.

### 3. Générer le fichier cible
Appeler :
```bash
python "C:/Users/Alexandre collenne/.claude/skills/antigravity/tools/generate_mcp_config.py" \
  --from "$HOME/.claude.json" \
  --out "C:/tmp/antigravity_mcp.json" \
  --exclude antigravity-cli,openclaw,antigravity-claude-proxy,antigravity-proxy
```

Format de sortie (compatible Antigravity MCP pane, schéma identique à Claude Desktop) :
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["mcp-obsidian"],
      "env": { "OBSIDIAN_API_KEY": "..." }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "..." }
    }
  }
}
```

### 4. Import manuel dans Antigravity
1. Antigravity → Agent pane (droite) → **MCP Servers** → **Import from file**.
2. Sélectionner `C:/tmp/antigravity_mcp.json`.
3. Pour chaque MCP importé, Antigravity affichera un statut :
   - 🟢 Connected
   - 🟡 Starting
   - 🔴 Error (lire logs, le plus souvent : commande `uvx`/`npx` pas dans le PATH d'Antigravity → ajouter manuellement le chemin absolu).

### 5. Résolution des chemins absolus
Si un MCP échoue (🔴), remplacer `uvx` / `npx` par leurs chemins absolus :
- `uvx` → `C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/Scripts/uvx.exe`
- `npx` → `C:/Program Files/nodejs/npx.cmd`
- `node` → `C:/Program Files/nodejs/node.exe`
- `python` → `C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/python.exe`

Re-générer le JSON avec `--absolute-paths` et ré-importer.

### 6. Test de fumée
Dans Antigravity, ouvrir un agent Manager et envoyer :
> "Liste les fichiers de mon vault Obsidian via le MCP obsidian"

Si réponse cohérente → bridge validé. Sinon retour étape 5.

## Output attendu

```json
{
  "status": "ok|partial|failed",
  "mcps_bridged": ["obsidian", "github", "context7"],
  "mcps_failed": [],
  "mcps_excluded": [],
  "config_path": "C:/tmp/antigravity_mcp.json",
  "smoke_test": "pass|fail"
}
```
