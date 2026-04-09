# N8N MCP Setup Guide — Installation pas-à-pas

Guide complet pour installer et configurer le serveur MCP `n8n-mcp` (czlonkowski) dans Claude Code et Claude Desktop sous Windows.

---

## Prérequis

- Node.js >= 22.16 (vérifier : `node --version`)
- **Mode docs-only** : aucune instance requise (actuel sur le poste d'Alexandre ✅)
- **Mode live** : une instance N8N (cloud ou self-hosted) + une clé API

---

## Étape 1 — Installation du package

Installer `n8n-mcp` globalement pour un démarrage instantané (sinon `npx -y` timeout sur Claude Code) :

```bash
npm install -g n8n-mcp
```

Vérifier :
```bash
ls "C:\Users\<USER>\AppData\Roaming\npm\node_modules\n8n-mcp\dist\mcp\index.js"
```

---

## Étape 2 — Obtenir une clé API N8N (mode live uniquement)

**Cloud ET self-hosted (même procédure) :**

1. Login sur votre instance N8N
2. **Settings → n8n API**
3. **Create an API key**
4. Choisir un Label (ex: "claude-mcp") + Expiration (ex: 1 an)
5. (Enterprise uniquement) Choisir les Scopes
6. Copier la clé (format `n8n_api_xxx...`) → la garder précieusement

**Note** : la clé n'est affichée qu'une seule fois.

---

## Étape 3 — Configuration MCP

Deux emplacements selon l'usage :

### Pour Claude Desktop (chat UI)
Fichier : `%APPDATA%\Claude\claude_desktop_config.json`
Sous Windows : `C:\Users\<USER>\AppData\Roaming\Claude\claude_desktop_config.json`

### Pour Claude Code (CLI / VSCode extension)
Fichier : `~/.claude.json` (à la racine du profil utilisateur)

### Config mode `docs-only` (actuel — sans instance N8N)

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "node",
      "args": [
        "C:\\Users\\<USER>\\AppData\\Roaming\\npm\\node_modules\\n8n-mcp\\dist\\mcp\\index.js"
      ],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_MCP_TELEMETRY_DISABLED": "true"
      }
    }
  }
}
```

**Outils exposés** : `search_nodes`, `get_node`, `list_nodes`, `validate_node`, `validate_workflow`, `search_templates`, `get_template`, `tools_documentation`.

### Config mode `live` (quand une instance N8N est disponible)

Ajouter simplement 2 env vars à la config docs-only :

```json
"env": {
  "MCP_MODE": "stdio",
  "LOG_LEVEL": "error",
  "DISABLE_CONSOLE_OUTPUT": "true",
  "N8N_MCP_TELEMETRY_DISABLED": "true",
  "N8N_API_URL": "https://votre-n8n.exemple.com/api/v1",
  "N8N_API_KEY": "n8n_api_xxxxxxxxxxxxx"
}
```

**Outils supplémentaires** : `n8n_create_workflow`, `n8n_update_partial_workflow`, `n8n_delete_workflow`, `n8n_list_workflows`, `n8n_test_workflow`, `n8n_executions`, `n8n_autofix_workflow`, `n8n_audit_instance`, `n8n_health_check`, `n8n_manage_credentials`, `n8n_deploy_template`.

### Important — pourquoi `node` direct plutôt que `npx -y`

`npx -y n8n-mcp` télécharge le package à chaque démarrage → Claude Code timeout avant que le MCP ne réponde `initialize`. Le chemin direct via `node` démarre en <1s.

**Important** :
- `N8N_API_URL` = URL racine de l'instance (sans `/api/v1` — le MCP l'ajoute)
- Si vous fusionnez avec d'autres MCPs existants → conserver les autres entrées sous `mcpServers`

---

## Étape 3 — Mode "doc-only" (sans API)

Si vous n'avez pas encore d'instance n8n ou voulez juste de l'aide à la rédaction :

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true"
      }
    }
  }
}
```

Les outils `search_nodes`, `get_node`, `validate_node`, `validate_workflow`, `search_templates` fonctionnent SANS API.
Seuls les outils `n8n_*` (create, update, executions, etc.) nécessitent l'API.

---

## Étape 4 — Installation alternative via Docker

```bash
docker pull ghcr.io/czlonkowski/n8n-mcp:latest

# Puis dans claude_desktop_config.json :
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init",
        "-e", "MCP_MODE=stdio",
        "-e", "N8N_API_URL=https://votre-n8n.exemple.com",
        "-e", "N8N_API_KEY=n8n_api_xxx",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
```

**Avantages Docker** : isolation totale, pas de Node sur l'host.
**Inconvénient** : démarrage plus lent (~3s) vs npx (~1s).

---

## Étape 5 — Vérification

1. **Redémarrer Claude Desktop / Claude Code** (obligatoire après modif config)
2. Demander à Claude : *« Liste les outils mcp__n8n-mcp disponibles »*
3. Réponse attendue : liste de 20 outils dont `search_nodes`, `n8n_health_check`, `n8n_create_workflow`...
4. Tester : *« Cherche le node Slack via n8n-mcp »*
5. Réponse attendue : `nodes-base.slack` retourné par `search_nodes`

---

## Variables d'environnement complètes

| Variable | Requis | Défaut | Rôle |
|----------|--------|--------|------|
| `MCP_MODE` | Oui | — | `stdio` (obligatoire pour Claude) |
| `N8N_API_URL` | Optionnel | — | URL racine instance n8n |
| `N8N_API_KEY` | Optionnel | — | Clé API n8n |
| `LOG_LEVEL` | Non | `info` | `error` recommandé pour Claude Desktop |
| `DISABLE_CONSOLE_OUTPUT` | Non | `false` | `true` pour Claude Desktop (évite parasites stdout) |
| `WEBHOOK_SECURITY_MODE` | Non | `strict` | `moderate` si webhooks localhost |
| `AUTH_TOKEN` | Non | — | Auth pour déploiements remote (mode HTTP) |
| `N8N_MCP_TELEMETRY_DISABLED` | Non | `false` | `true` pour opt-out telemetry |

---

## Troubleshooting

### Le MCP n'apparaît pas dans Claude
- Vérifier le chemin du fichier de config (Roaming/Claude pour Desktop, ~/.claude.json pour Code)
- Vérifier que le JSON est valide (`jq . claude_desktop_config.json`)
- Redémarrer Claude COMPLÈTEMENT (fermer + relancer, pas juste recharger)

### Erreur "n8n_health_check failed"
- Vérifier `N8N_API_URL` (sans slash final, sans `/api/v1`)
- Vérifier `N8N_API_KEY` (format `n8n_api_...`)
- Tester manuellement : `curl -H "X-N8N-API-KEY: $KEY" https://votre-n8n/api/v1/workflows`

### Erreur "EACCES" ou "permission denied"
- Sous Windows : lancer cmd en Administrateur la 1ère fois
- Vérifier que `npx` peut écrire dans `%APPDATA%/npm-cache`

### Le MCP démarre mais aucun outil n'est disponible
- `MCP_MODE=stdio` est-il bien défini ? (sans guillemets dans le JSON)
- `DISABLE_CONSOLE_OUTPUT=true` est-il défini ?
- Regarder les logs Claude Desktop : `%APPDATA%/Claude/logs/`

### Webhooks localhost refusés
- Ajouter `"WEBHOOK_SECURITY_MODE": "moderate"` aux env vars

---

## Sources

- Repo officiel : https://github.com/czlonkowski/n8n-mcp
- Doc Claude Code setup : https://github.com/czlonkowski/n8n-mcp/blob/main/docs/CLAUDE_CODE_SETUP.md
- Pack skills compagnon : https://github.com/czlonkowski/n8n-skills
- N8N API auth : https://docs.n8n.io/api/authentication/
