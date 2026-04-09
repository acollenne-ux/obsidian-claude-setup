# N8N Cheatsheet — Référence rapide pour Claude

## Les 20 nodeTypes les plus utilisés (à connaître par cœur)

| Catégorie | nodeType | Usage |
|-----------|----------|-------|
| **Trigger** | `nodes-base.webhook` | Reçoit HTTP request |
| **Trigger** | `nodes-base.scheduleTrigger` | Cron / interval |
| **Trigger** | `nodes-base.manualTrigger` | Test manuel |
| **Trigger** | `nodes-base.errorTrigger` | Catch errors workflow |
| **Action HTTP** | `nodes-base.httpRequest` | Appel API REST/GraphQL |
| **Logique** | `nodes-base.if` | Branchement conditionnel |
| **Logique** | `nodes-base.switch` | Multi-branchement |
| **Logique** | `nodes-base.merge` | Fusion de branches |
| **Logique** | `nodes-base.splitInBatches` | Boucle paginée |
| **Data** | `nodes-base.set` | Assignation de variables |
| **Data** | `nodes-base.code` | JavaScript/Python custom |
| **Data** | `nodes-base.editFields` | Mapping/renommage |
| **Data** | `nodes-base.itemLists` | Manipulation arrays |
| **Storage** | `nodes-base.postgres` | Postgres CRUD |
| **Storage** | `nodes-base.googleSheets` | Sheets read/write |
| **Storage** | `nodes-base.airtable` | Airtable CRUD |
| **Comm** | `nodes-base.slack` | Message Slack |
| **Comm** | `nodes-base.gmail` | Email Gmail |
| **AI** | `nodes-langchain.agent` | AI Agent (LangChain) |
| **AI** | `nodes-langchain.openAi` | OpenAI direct |

---

## Snippets JSON ready-to-use

### Webhook minimal
```json
{
  "id": "webhook-1",
  "name": "Webhook",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "position": [250, 300],
  "parameters": {
    "httpMethod": "POST",
    "path": "incoming-data",
    "responseMode": "lastNode",
    "options": {}
  }
}
```

### IF node
```json
{
  "id": "if-1",
  "name": "IF",
  "type": "n8n-nodes-base.if",
  "typeVersion": 2,
  "position": [450, 300],
  "parameters": {
    "conditions": {
      "options": {"caseSensitive": true, "leftValue": "", "typeValidation": "strict"},
      "conditions": [{
        "id": "cond-1",
        "leftValue": "={{ $json.amount }}",
        "rightValue": 100,
        "operator": {"type": "number", "operation": "gt"}
      }],
      "combinator": "and"
    }
  }
}
```

### Code node (JavaScript)
```json
{
  "id": "code-1",
  "name": "Code",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [650, 300],
  "parameters": {
    "language": "javaScript",
    "jsCode": "for (const item of $input.all()) {\n  item.json.processed = true;\n}\nreturn $input.all();"
  }
}
```

### AI Agent (LangChain)
```json
{
  "id": "ai-agent-1",
  "name": "AI Agent",
  "type": "@n8n/n8n-nodes-langchain.agent",
  "typeVersion": 1.7,
  "position": [850, 300],
  "parameters": {
    "agent": "toolsAgent",
    "promptType": "define",
    "text": "={{ $json.question }}"
  }
}
```

---

## Expressions n8n essentielles

| Syntaxe | Usage |
|---------|-------|
| `{{ $json.field }}` | Accéder à un champ de l'item courant |
| `{{ $json["field with space"] }}` | Champ avec espace |
| `{{ $node["NodeName"].json.field }}` | Champ d'un autre nœud |
| `{{ $items() }}` | Tous les items courants |
| `{{ $items("NodeName") }}` | Tous les items d'un autre nœud |
| `{{ $now }}` | DateTime actuel (Luxon) |
| `{{ $now.toFormat("yyyy-MM-dd") }}` | Format date |
| `{{ $env.MY_VAR }}` | Variable d'env |
| `{{ $input.first().json.x }}` | 1er item |
| `{{ $input.all().length }}` | Nombre d'items |
| `{{ $workflow.id }}` | ID du workflow |
| `{{ $execution.id }}` | ID de l'exécution |

---

## Settings recommandés (workflow)

```json
{
  "settings": {
    "executionOrder": "v1",
    "saveExecutionProgress": true,
    "saveManualExecutions": true,
    "callerPolicy": "workflowsFromSameOwner",
    "errorWorkflow": "",
    "timezone": "Europe/Paris"
  }
}
```

---

## Patterns de connexion

### Linéaire (A → B → C)
```json
{
  "A": {"main": [[{"node": "B", "type": "main", "index": 0}]]},
  "B": {"main": [[{"node": "C", "type": "main", "index": 0}]]}
}
```

### Branchement (IF → True path / False path)
```json
{
  "IF": {
    "main": [
      [{"node": "TruePath", "type": "main", "index": 0}],
      [{"node": "FalsePath", "type": "main", "index": 0}]
    ]
  }
}
```

### Merge (A et B → Merge)
```json
{
  "A": {"main": [[{"node": "Merge", "type": "main", "index": 0}]]},
  "B": {"main": [[{"node": "Merge", "type": "main", "index": 1}]]}
}
```

### AI Agent + tools
```json
{
  "AI Agent": {
    "main": [[{"node": "Output", "type": "main", "index": 0}]],
    "ai_tool": [[{"node": "Tool1", "type": "ai_tool", "index": 0}]],
    "ai_languageModel": [[{"node": "OpenAI", "type": "ai_languageModel", "index": 0}]]
  }
}
```

---

## Erreurs fréquentes & remèdes éclair

| Erreur | Cause | Fix |
|--------|-------|-----|
| `Cannot read property 'X' of undefined` | Champ absent | Garde `{{ $json.X ?? 'default' }}` |
| `X is not a function` | typeVersion obsolète | get_node + mettre à jour typeVersion |
| `401 Unauthorized` | Credential expiré | n8n_manage_credentials → recreate |
| `429 Too Many Requests` | Rate limit | Wait node + Loop |
| `Webhook not registered` | Workflow inactif | Activer + utiliser `/webhook/` (pas test) |
| `Pinned data is stale` | Test data obsolète | Vider pinned data dans l'UI |
| `Could not find node` | name modifié, connection orpheline | Recréer la connexion |
| `Required field missing` | Default param vide | validate_node mode runtime |

---

## Limites plateforme

| Ressource | Limite | Notes |
|-----------|--------|-------|
| Items par run | ~100k | Au-delà : SplitInBatches |
| Taille payload | ~16MB | Au-delà : streaming/chunks |
| Timeout HTTP node | 300s default | Configurable jusqu'à 3600s |
| Workflows actifs (cloud Starter) | 5 | Plan supérieur si plus |
| Executions/mois (cloud Starter) | 2.5k | Plan supérieur si plus |
| Memory Code node | ~512MB | Au-delà : OOM |

---

## Outils MCP n8n-mcp — récapitulatif (20 outils)

**Doc/Validation (sans API) :**
- `tools_documentation`, `search_nodes`, `get_node`, `validate_node`, `validate_workflow`, `search_templates`, `get_template`

**Workflow Management (avec API) :**
- `n8n_create_workflow`, `n8n_get_workflow`, `n8n_update_full_workflow`, `n8n_update_partial_workflow`, `n8n_delete_workflow`, `n8n_list_workflows`, `n8n_validate_workflow`, `n8n_autofix_workflow`, `n8n_workflow_versions`, `n8n_deploy_template`

**Exécution & Admin (avec API) :**
- `n8n_test_workflow`, `n8n_executions`, `n8n_manage_credentials`, `n8n_audit_instance`, `n8n_health_check`
