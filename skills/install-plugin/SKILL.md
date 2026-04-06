---
name: install-plugin
description: Installation facile de plugins, MCP servers et skills pour Claude Code. Guide l'utilisateur à travers l'installation de n'importe quel plugin du marketplace ou MCP server. Invoqué avec /install-plugin.
argument-hint: "nom du plugin ou service à connecter"
user-invocable: true
allowed-tools: Bash, Read, Write, WebSearch
---

## RÈGLE UNIVERSELLE — LIRE L'INTÉGRALITÉ DU SKILL AVANT D'AGIR

**OBLIGATOIRE : Avant d'exécuter quoi que ce soit, tu DOIS :**
1. Lire l'INTÉGRALITÉ de ce fichier SKILL.md (pas juste le début)
2. Comprendre chaque section, chaque règle, chaque contrainte
3. Respecter ce skill À LA LETTRE — ne rien sauter, ne rien simplifier

**Ne JAMAIS commencer l'exécution sans avoir lu et compris TOUT le skill.**

---

# Skill : Installation Facile de Plugins

Quand invoqué, identifier ce que l'utilisateur veut installer et l'installer automatiquement.

## Catalogue des plugins populaires

### Depuis le marketplace officiel (`/plugin install`)
| Commande | Description |
|----------|-------------|
| `/plugin install code-review` | Review de code automatique |
| `/plugin install feature-dev` | Développement de features guidé |
| `/plugin install pr-review-toolkit` | Analyse complète des PRs |
| `/plugin install security-guidance` | Guidance sécurité intégrée |
| `/plugin install agent-sdk-dev` | Développement d'agents SDK |
| `/plugin install skill-creator` | Créateur de skills assisté |
| `/plugin install frontend-design` | Design frontend guidé |

### MCP Servers — Données Financières
```bash
# Alpha Vantage (stocks, forex, crypto)
claude mcp add --transport http alpha-vantage https://mcp.alphavantage.co/mcp
# Nécessite : clé API sur alphavantage.co (plan gratuit disponible)

# Yahoo Finance via MCP
npx -y @modelcontextprotocol/server-fetch
```

### MCP Servers — Développement
```bash
# GitHub
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
# (nécessite token GitHub)

# Playwright (automatisation navigateur)
claude mcp add playwright npx -y @playwright/mcp@latest

# PostgreSQL
claude mcp add postgres npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/mydb"

# Filesystem avancé
claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /path/to/dir
```

### MCP Servers — Productivité
```bash
# Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Slack
claude mcp add --transport http slack https://mcp.slack.com/sse

# Linear (gestion de projet)
claude mcp add --transport http linear https://mcp.linear.app/sse

# Brave Search
claude mcp add brave-search npx -y @modelcontextprotocol/server-brave-search
```

## Procédure d'installation automatique

Quand l'utilisateur demande un plugin :

1. **Identifier** : Plugin marketplace ou MCP server externe ?
2. **Vérifier** : Le plugin existe-t-il déjà ? (`/plugin list` ou `/mcp list`)
3. **Installer** : Exécuter la commande appropriée
4. **Configurer** : Demander les clés API si nécessaires
5. **Tester** : Vérifier que l'installation fonctionne
6. **Documenter** : Expliquer comment utiliser le plugin installé

## Installation manuelle d'un skill personnel

```bash
mkdir -p ~/.claude/skills/mon-skill
cat > ~/.claude/skills/mon-skill/SKILL.md << 'EOF'
---
name: mon-skill
description: Description pour que Claude sache quand l'utiliser automatiquement
argument-hint: [argument]
---
# Instructions du skill
...
EOF
```

## Commandes utiles
```bash
/plugin          # Lister les plugins installés
/plugin install  # Browser le marketplace
/mcp             # Lister les MCP servers
claude mcp list  # Via CLI
```


## TESTS POST-INSTALLATION AUTOMATIQUES
Après chaque installation :
1. Vérifier que le MCP/skill apparaît dans la liste active
2. Tester un appel simple (health check)
3. Si le test échoue → rollback + signaler
4. Si le test réussit → documenter dans RETEX
Pattern test : appeler l'outil le plus basique du MCP pour vérifier la connexion.

## AUTO-DÉCOUVERTE DE PLUGINS PERTINENTS
Avant chaque tâche complexe :
1. Analyser le type de tâche (finance, code, data, etc.)
2. WebSearch "Claude MCP server [domaine] best 2026"
3. WebFetch https://www.claudemcp.com/servers pour catalogue
4. Comparer avec plugins installés
5. Si plugin pertinent non installé (score utilité >= 7/10) → proposer installation

## GESTION DE VERSIONS
Pour chaque plugin installé, tracker :
- Version installée
- Date d'installation
- Dernière version disponible (vérifier périodiquement)
- Breaking changes connus
WebSearch "[plugin] changelog latest version" pour vérifications.

## ROLLBACK SI INSTALLATION ÉCHOUE
Protocole :
1. Avant install → sauvegarder état actuel (liste MCPs actifs)
2. Installer le plugin
3. Test post-install
4. Si test échoue → désinstaller + restaurer état précédent
5. Logger l'échec dans RETEX avec raison

## SCORE COMPATIBILITÉ
Avant d'installer, évaluer :
| Critère | Score /10 |
|---------|----------|
| Pertinence pour la tâche | /10 |
| Fiabilité (reviews/stars) | /10 |
| Maintenance active (dernier commit) | /10 |
| Documentation qualité | /10 |
| Compatibilité système | /10 |
**Score total /50 → Installer si >= 30/50**

## HEALTH CHECK PÉRIODIQUE
Vérifier régulièrement les plugins installés :
- MCP répond-il ? (appel test)
- API key valide ? (vérifier expiration)
- Version à jour ? (comparer)
- Toujours utile ? (score utilisation derniers 30 jours)
Si score santé < 5/10 → signaler pour désinstallation ou mise à jour.


## ROUTAGE MULTI-IA — INSTALLATION
| Tâche | IA Primaire | Justification |
|-------|------------|---------------|
| Recherche plugins | WebSearch + Gemini | Extraction structurée |
| Évaluation compatibilité | Mistral Large | Analyse FR détaillée |
| Debug installation | Gemini Flash | N°1 code |

## SYSTÈME DE CONFIANCE INSTALLATION
| Niveau | Critère | Marqueur |
|--------|---------|----------|
| ÉLEVÉ | Plugin installé + test post-install OK | ✓✓✓ |
| MOYEN | Plugin installé, test partiel | ✓✓ |
| FAIBLE | Plugin installé, pas de test | ✓ |
| SPÉCULATIF | Installation incertaine | ~ |

## MATRICE DE FALLBACK INSTALLATION
| Méthode principale | Fallback 1 | Fallback 2 |
|-------------------|------------|------------|
| /plugin install | claude mcp add | Installation manuelle |
| npm install -g | npx direct | Clone GitHub + build |
| pip install | pip install --user | Conda install |

---

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "On installe d'abord, on vérifie après" | TOUJOURS vérifier compatibilité (score /50) AVANT d'installer. Rollback coûte plus cher que prévention. |
| "Le README suffit comme documentation" | Tester post-installation est OBLIGATOIRE. Un README peut être obsolète. |
| "Pas besoin de vérifier si c'est déjà installé" | TOUJOURS vérifier `/plugin list` ou `/mcp list` avant d'installer. Doublons = conflits. |
| "Les versions n'importent pas" | Tracker les versions et vérifier les breaking changes. Un MCP obsolète peut casser silencieusement. |

## RED FLAGS — STOP

- Plugin installé sans test post-installation → STOP, tester immédiatement
- Installation sans vérification de compatibilité → STOP, évaluer le score /50 d'abord
- Clé API hardcodée dans le code → STOP, utiliser les variables d'environnement

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Découverte plugins pertinents | `deep-research` |
| Création de skills custom | `skill-creator` |
| Debug post-installation | `code-debug` |
| RETEX installation | `retex-evolution` |

## ÉVOLUTION

Après chaque installation :
- Si un plugin échoue au test → documenter la raison et le workaround
- Si un nouveau MCP server pertinent est découvert → l'ajouter au catalogue
- Si le processus d'installation est trop long → automatiser davantage

Seuils : si taux d'échec installation > 30% → revoir le protocole de vérification pré-installation.
