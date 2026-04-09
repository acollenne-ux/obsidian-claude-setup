# Recettes MCP pour Antigravity

Recettes JSON prêtes à copier-coller dans l'import MCP d'Antigravity.
**Toutes ces recettes sont le sens SAFE : Claude → Antigravity (bridge unidirectionnel).**

## Structure attendue par Antigravity

Identique à Claude Desktop :
```json
{
  "mcpServers": {
    "<nom>": {
      "command": "<exe>",
      "args": ["..."],
      "env": { "KEY": "VALUE" }
    }
  }
}
```

## Recettes

### 1. Obsidian (notes)
```json
"obsidian": {
  "command": "C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/Scripts/uvx.exe",
  "args": ["mcp-obsidian"],
  "env": {
    "OBSIDIAN_API_KEY": "<copier depuis ~/.claude.json>",
    "OBSIDIAN_HOST": "127.0.0.1",
    "OBSIDIAN_PORT": "27124"
  }
}
```
**Prérequis** : Obsidian Desktop lancé + plugin "Local REST API" actif.

### 2. GitHub
```json
"github": {
  "command": "C:/Program Files/nodejs/npx.cmd",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "<PAT depuis ~/.claude.json>"
  }
}
```

### 3. Context7 (docs libs)
```json
"context7": {
  "command": "C:/Program Files/nodejs/npx.cmd",
  "args": ["-y", "@upstash/context7-mcp"]
}
```

### 4. n8n-mcp (docs-only mode)
```json
"n8n-mcp": {
  "command": "C:/Program Files/nodejs/node.exe",
  "args": ["C:/Users/Alexandre collenne/AppData/Roaming/npm/node_modules/n8n-mcp/dist/mcp/index.js"]
}
```
**Note** : mode `docs-only` (pas d'instance n8n live), identique à la config Claude Code.

### 5. Google Sheets
```json
"google-sheets": {
  "command": "C:/Program Files/nodejs/npx.cmd",
  "args": ["-y", "@xing5/mcp-google-sheets"],
  "env": {
    "GOOGLE_APPLICATION_CREDENTIALS": "C:/Users/Alexandre collenne/.claude/credentials/claude-sheets-service-account.json"
  }
}
```

### 6. Playwright (redondant mais utile)
```json
"playwright": {
  "command": "C:/Program Files/nodejs/npx.cmd",
  "args": ["-y", "@playwright/mcp"]
}
```

### 7. TradingView (si setup local)
```json
"tradingview": {
  "command": "C:/Program Files/nodejs/node.exe",
  "args": ["C:/Users/Alexandre collenne/.claude/mcp/tradingview-mcp/dist/index.js"],
  "env": {
    "TV_CHROME_PORT": "9222"
  }
}
```
**Prérequis** : TradingView Desktop lancé avec debug port 9222.

## Recettes INTERDITES (ne JAMAIS utiliser)

```json
// ❌ BAN WAVE — proxy ré-exposant Antigravity
"antigravity-proxy": { ... }
"openclaw": { ... }
"antigravity-cli": { ... }
```

## Troubleshooting

| Symptôme | Cause probable | Fix |
|----------|----------------|-----|
| 🔴 "Command not found" | `uvx`/`npx` pas dans PATH d'Antigravity | Utiliser chemins absolus (cf. recettes) |
| 🔴 "Module not found" | Package pas installé globalement | `npm install -g <package>` ou `uv tool install <package>` |
| 🔴 Auth error | Env vars manquantes | Copier depuis `~/.claude.json` |
| 🟡 "Starting..." bloqué | Service externe pas lancé (Obsidian, TradingView) | Lancer le service puis "Restart MCP" |
| 🟢 Connected mais outils invisibles | Cache Antigravity | Redémarrer Antigravity |
