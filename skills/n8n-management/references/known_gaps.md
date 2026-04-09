# N8N MCP — Limitations connues & workarounds

## Limitations du serveur MCP `n8n-mcp` (czlonkowski)

| # | Limitation | Impact | Workaround |
|---|------------|--------|------------|
| 1 | Couverture des opérations : 63.6% | Certaines opérations rares ne sont pas validées | Tester en sandbox avant prod |
| 2 | Community nodes : 584 indexés, 516 vérifiés | 12% non vérifiés peuvent avoir typeVersion incorrect | Vérifier manuellement avec `get_node` |
| 3 | `n8n_autofix_workflow` règle ~40% des cas | Pas de garantie de succès | Toujours valider après autofix |
| 4 | Pas de support pour les `executions` >1000 par requête | Pagination obligatoire | Boucler avec `cursor` |
| 5 | `n8n_test_workflow` n'exécute pas les credentials sandbox | Tests credentials = vraies APIs | Utiliser des credentials de test isolées |
| 6 | `validate_workflow` ne détecte pas les erreurs runtime d'expression | Faux positif "OK" | Toujours `n8n_test_workflow` après |
| 7 | `n8n_update_full_workflow` casse l'historique d'exécution | Perte de traçabilité | Préférer `n8n_update_partial_workflow` |
| 8 | Docker stdio nécessite `-i` flag | Sinon timeout MCP | Bien copier la commande de setup_guide.md |
| 9 | Webhooks localhost refusés en mode `strict` | Workflows locaux KO | `WEBHOOK_SECURITY_MODE=moderate` |
| 10 | Mode `sql.js` (fallback) consomme 150-200 MB RAM | Lent | Installer `better-sqlite3` natif |
| 11 | Telemetry activée par défaut | Données envoyées à czlonkowski | `N8N_MCP_TELEMETRY_DISABLED=true` |
| 12 | `n8n_deploy_template` peut échouer si template a des nodes manquants | Deploy incomplet | Lire le template avant + installer les community nodes |

---

## Limitations de l'API REST n8n elle-même

| # | Limitation | Impact | Workaround |
|---|------------|--------|------------|
| 1 | OAuth2 managed indisponible en self-hosted | Doit créer custom OAuth app | Suivre doc Google/etc. |
| 2 | API key sans scope (sauf Enterprise) | Tout-ou-rien | Plan Enterprise pour scopes |
| 3 | Rate limit non documenté | Risque 429 si bombardé | Implémenter backoff côté client |
| 4 | Pas de WebSocket pour les executions live | Polling obligatoire | `n8n_executions` toutes les Xs |
| 5 | Credentials ne peuvent pas être exportées en clair | Migration manuelle | Recréer manuellement sur la nouvelle instance |
| 6 | Variables sont par instance, pas par workflow | Pas de scoping | Préfixer les noms (`WORKFLOW_X_VAR`) |

---

## Limitations spécifiques aux nœuds AI/LangChain

| # | Limitation | Impact | Workaround |
|---|------------|--------|------------|
| 1 | `@n8n/n8n-nodes-langchain.*` change rapidement | typeVersion non stable | get_node systématique |
| 2 | Memory token-based limité par fenêtre du LLM | Truncation possible | Memory `bufferWindow` plus court |
| 3 | Vector Store nodes nécessitent un store externe (Pinecone, Qdrant) | Setup additionnel | Documenter dans `references/` du workflow |
| 4 | Tool calling : pas tous les LLM supportés | Erreur silencieuse | Vérifier compat dans la doc OpenAI/Anthropic |
| 5 | Streaming response non supporté en webhook responseMode | Latence perçue | `responseMode: "lastNode"` + UI loader |

---

## Edge cases à anticiper

### Webhooks
- `/webhook/` (prod) ≠ `/webhook-test/` (dev) — toujours vérifier l'URL utilisée
- Webhooks consomment 1 execution même si erreur 500 dans le workflow → coûts cloud
- Certains reverse proxies (Cloudflare) buffer les requêtes → timeout côté client

### Cron / Schedule
- Timezone du nœud ≠ timezone du serveur → toujours expliciter
- Cron sur instance cloud Starter limité à 1/h minimum
- Si workflow tourne >intervalle → exécutions empilées (Loop trap)

### Code nodes
- Pas d'accès `process.env` directement → utiliser `$env.X`
- Pas de `require()` (Function isolated) → utiliser nodes-base.code mode "Run Once for Each Item"
- `setTimeout`/`setInterval` interdits → toujours synchrone

### Database nodes
- Postgres : connexion poolée mais pas de pre-warming
- Google Sheets : limite 60 req/min/projet → backoff
- Airtable : 5 req/sec/base → backoff

---

## Quand contacter l'utilisateur

Forcer un STOP et demander à Alexandre si :
1. Le MCP `n8n-mcp` n'est pas chargé dans la session courante
2. `N8N_API_URL` n'est pas configuré (ou URL invalide)
3. Une opération destructive est sur le point de modifier un workflow `active=true`
4. Un workflow utilise un community node non vérifié
5. Un workflow utilise plus de 5000 items en mémoire (risque OOM)
6. Une credential serait stockée en clair dans le JSON
