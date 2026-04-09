---
name: N8N Management — installation skills + agents + MCP
description: Stack complète n8n-management installée le 08/04/2026 — orchestrateur custom + 7 skills officiels czlonkowski + 3 agents + MCP czlonkowski/n8n-mcp connecté Desktop+Code
type: project
---

# N8N Management — 08/04/2026

## Contexte
Demande : rendre Claude capable de créer/modifier/déboguer/déployer/auditer des workflows N8N de manière professionnelle, via skills + agents + MCP.

## Stack installée

### MCP server (MODE DOCS-ONLY — version finale 08/04/2026 01:45)
- **`n8n-mcp` (czlonkowski/n8n-mcp v2.47.2)** — vainqueur sur leonardsellem/n8n-mcp-server (20 outils total, 63.6% couverture ops, 584 community nodes indexés).
- **Installé globalement** via `npm install -g n8n-mcp` (115 packages) — chemin : `C:\Users\Alexandre collenne\AppData\Roaming\npm\node_modules\n8n-mcp\dist\mcp\index.js`
- **Démarrage via `node` direct** dans les 2 configs Claude — **PAS `npx -y`** (qui timeout sur Claude Code car télécharge à chaque démarrage)
- Installé dans 2 environnements :
  - **Claude Desktop** : `C:\Users\Alexandre collenne\AppData\Roaming\Claude\claude_desktop_config.json` (backup `.bak_20260408_010418`)
  - **Claude Code** : `C:\Users\Alexandre collenne\.claude.json` (section `mcpServers.n8n-mcp`)
- Statut : `claude mcp list` → **✓ Connected** (instantané, <1s)
- Variables d'env actives : `MCP_MODE=stdio`, `LOG_LEVEL=error`, `DISABLE_CONSOLE_OUTPUT=true`, `N8N_MCP_TELEMETRY_DISABLED=true`
- **Mode docs-only assumé** : pas d'instance n8n, mais 8 outils disponibles (search_nodes, get_node, list_nodes, validate_node, validate_workflow, search_templates, get_template, tools_documentation). Claude peut **concevoir, valider et livrer du JSON** de workflow importable manuellement.
- **Pour basculer en mode live** : ajouter `N8N_API_URL` + `N8N_API_KEY` dans les env vars des 2 configs → 12 outils supplémentaires (create/update/delete/test/executions/audit/etc.)

### Échecs rencontrés (RETEX)
- ❌ **n8n self-hosted via npm** : install OK (2228 packages) mais `sqlite3` ne compile pas ses bindings natifs pour Node 24 → `SQLite package has not been found installed`. Nécessiterait `npm rebuild sqlite3` avec build-tools ou downgrade Node 22.
- ❌ **`npx -y n8n-mcp`** : fonctionne en stdio manuel mais Claude Code timeout à l'étape `initialize` (download trop lent).
- ✅ **Solution retenue** : install globale + commande `node` directe.

### Skills officiels czlonkowski/n8n-skills (7)
Clonés depuis le repo officiel et installés dans `~/.claude/skills/` :
1. `n8n-mcp-tools-expert` — utilisation des 20 outils MCP (search/get/validate/deploy)
2. `n8n-workflow-patterns` — bibliothèque de patterns (webhooks, RAG, scheduled, etc.)
3. `n8n-validation-expert` — triple validation (minimal → runtime → workflow)
4. `n8n-node-configuration` — configuration des nodes par type
5. `n8n-expression-syntax` — `{{ $json.x }}`, `$node`, `$now`, `$env`, etc.
6. `n8n-code-javascript` — patterns JS pour Code node (BUILTIN_FUNCTIONS, COMMON_PATTERNS, DATA_ACCESS, ERROR_PATTERNS)
7. `n8n-code-python` — patterns Python pour Code node

### Skill custom — `n8n-management` (orchestrateur)
**Score audit skill-creator V2 : 89/100 EXCELLENT**

Chemin : `~/.claude/skills/n8n-management/`

Structure :
```
n8n-management/
├── SKILL.md                              # 338 lignes, orchestrateur 9 phases
├── agents/
│   ├── workflow-architect.md             # Build workflow JSON depuis intention
│   ├── workflow-debugger.md              # RCA 5 Whys sur workflows en échec
│   └── workflow-validator.md             # Mode A (pre-deploy) + Mode B (audit instance)
└── references/
    ├── setup_guide.md                    # Install MCP Desktop + Code + Docker
    ├── cheatsheet.md                     # 20 nodeTypes + snippets JSON + expressions
    └── known_gaps.md                     # 12 limites MCP + 6 limites API + edge cases
```

**Frontmatter SKILL.md** :
```yaml
name: n8n-management
description: "Orchestrateur N8N : créer, modifier, déboguer, déployer et auditer des workflows. Triggers: 'n8n', 'workflow n8n', 'automatiser', 'webhook', 'agent IA n8n', 'déboguer workflow', 'déployer workflow', 'audit n8n', 'no-code', 'RAG n8n'."
argument-hint: "create <objectif> | debug <workflow_id> | audit | deploy <template> | improve <workflow_id>"
allowed-tools: [Bash, WebSearch, WebFetch, Read, Write, Edit, TodoWrite, Agent, "mcp__n8n-mcp__*"]
```

**9 phases** : Preflight → Intention → Pattern matching → Discovery → Build via agents → Validation → Deploy → Test → Documentation+PDF.

**HARD-GATE 6 règles non négociables** :
1. JAMAIS d'opération destructive sans validation
2. TOUJOURS `validate_workflow` avant `n8n_create_workflow`
3. TOUJOURS préférer `n8n_update_partial_workflow` à `n8n_update_full_workflow` (préserve historique)
4. TOUJOURS `get_node` avant de configurer un node inconnu
5. TOUJOURS tester en sandbox avant prod si workflow `active=true`
6. TOUJOURS générer PDF synthèse + email après livraison majeure

## Agents (3)

### `workflow-architect`
Build workflow JSON depuis brief → workflow déployable. Protocole 8 étapes : read brief → select pattern → discovery par node → configure → validation incrémentale → connections → validation finale → livrable.

### `workflow-debugger`
RCA sur workflows en échec via méthodologie **5 Whys**. Protocole 7 étapes. Tableau de classification des erreurs : Schema mismatch, Authentication, Rate limit, Timeout, Invalid config, Connection, Data type, Webhook test vs prod, Memory, Logic. Toujours propose 2-3 fix alternatives rangés par impact/risque.

### `workflow-validator`
- **Mode A** : validation pre-deploy d'un workflow (12 critères sécurité)
- **Mode B** : audit complet de l'instance (10 dimensions scoring)
- Triple validation : `validate_node` minimal → runtime → `validate_workflow`

## Limites identifiées (`references/known_gaps.md`)

### MCP n8n-mcp (12)
- Couverture 63.6% des opérations
- 12% community nodes non vérifiés
- `n8n_autofix_workflow` règle ~40% des cas
- Pagination obligatoire >1000 executions
- `validate_workflow` ne détecte pas les erreurs runtime d'expression
- `n8n_update_full_workflow` casse l'historique d'exécution
- Telemetry activée par défaut (désactivée via env var)
- ...

### API REST n8n (6)
- OAuth2 managed indisponible en self-hosted
- API key sans scope (sauf Enterprise)
- Pas de WebSocket pour executions live
- Variables par instance (pas par workflow)
- ...

### AI/LangChain nodes (5)
- `@n8n/n8n-nodes-langchain.*` typeVersion non stable → `get_node` systématique
- Memory token-based limité par fenêtre LLM
- Vector Store nodes nécessitent store externe (Pinecone, Qdrant)
- Streaming response non supporté en webhook responseMode

## Patterns workflow couverts (5)
1. **Webhook Processing** — Webhook → IF → HTTP → Response
2. **HTTP API Integration** — Schedule → HTTP → Set → Postgres
3. **Database Sync** — Trigger → SplitInBatches → Postgres → GoogleSheets
4. **AI Agent / RAG** — Webhook → Agent (langchain) + memory + tools + vector store
5. **Scheduled Reporting** — ScheduleTrigger → Multiple HTTPs → Code → Slack/Email

## Vérifications post-installation
- ✅ `claude mcp list` → `n8n-mcp: ✓ Connected`
- ✅ 8 skills `n8n-*` visibles dans le pool de skills (7 officiels + n8n-management)
- ✅ Skill audit : 89/100 EXCELLENT (skill-creator V2)
- ⏳ Test live : nécessite remplacement des placeholders `N8N_API_URL` + `N8N_API_KEY`

## Prochaines étapes pour Alexandre
1. Remplacer `N8N_API_URL=REMPLACER_PAR_URL_INSTANCE_N8N` par l'URL réelle de l'instance n8n (cloud ou self-hosted)
2. Remplacer `N8N_API_KEY=REMPLACER_PAR_CLE_API_N8N` par la clé API (générée dans Settings → API de n8n)
3. Redémarrer Claude Desktop pour recharger la config
4. Tester avec : "crée-moi un workflow n8n qui ..."

## Sources clés
- czlonkowski/n8n-mcp (GitHub)
- czlonkowski/n8n-skills (GitHub)
- N8N API REST docs (`/api/v1`)
- Model Context Protocol spec (Anthropic)
