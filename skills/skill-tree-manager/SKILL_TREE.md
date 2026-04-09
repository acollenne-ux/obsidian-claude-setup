# SKILL_TREE.md — Arborescence Intelligente des Skills

**Généré** : 2026-04-09 19:20  
**Total skills** : 54  
**Requis (non-exemptés)** : 43  
**Conformes** : 40  
**Score cohérence** : 93/100

## Règles d'arborescence (non-négociables)

1. **ENTRÉE** : toute conversation démarre par `deep-research`
2. **SORTIE** : toute réponse finit par un livrable (PDF, PPT, DOC, image, vidéo, audio)

```
L0 deep-research → L1 THINK → L2 RESEARCH → L3 SPECIALIST → L4 DELIVERY → L5 QA → L6 META
```

## L0 — ENTRY (point d'entrée unique)

| Skill | Livrable | Généré par | Description |
|-------|----------|------------|-------------|
| `deep-research` | — | — | Orchestrateur léger qui classe la complexité, détecte les domaines, et dispatche |

## L1 — THINK (brainstorming / cadrage / orchestration)

| Skill | Livrable | Généré par | Description |
|-------|----------|------------|-------------|
| `project-analysis` | — | — | Analyse complète d'un projet avant tout développement : contraintes, architectur |
| `superpowers-brainstorming` | — | — | Explorer l'intention réelle, les exigences et le design avant d'agir. Garantit q |
| `team-agent` | — | — | Orchestre une équipe d'agents spécialisés en parallèle pour les tâches multi-dom |

## L2 — RESEARCH (collecte multi-sources)

| Skill | Livrable | Généré par | Description |
|-------|----------|------------|-------------|
| `defuddle` | — | — | Extract clean markdown content from web pages using Defuddle CLI, removing clutt |
| `multi-ia-router` | — | — | Routage intelligent multi-IA : sélection du meilleur modèle, consensus voting, f |

## L3 — SPECIALIST (métier)

| Skill | Livrable | Généré par | Description |
|-------|----------|------------|-------------|
| `adaptive-thinking-router` | DOC | — | Pilote dynamiquement thinking.effort (low/medium/high) d'Opus 4.6 selon la compl |
| `antigravity` | PDF | — | Connecteur Google Antigravity (free tier, sans forfait payant). Guide setup, bri |
| `code-debug` | PDF | — | Débogage avancé avec root cause analysis. Use when: debugging code, fixing bugs, |
| `context-compressor` | DOC | — | Compression hiérarchique 4 niveaux (FULL→SUMMARY→META→ARCHIVE) + pruning pré-env |
| `data-analysis` | PDF | — | > |
| `desktop-control` | PDF | — | > |
| `dev-team` | PDF | — | > |
| `diagram-toolkit` | PNG | — | Bibliothèque technique de templates, thèmes et outils de rendu pour schémas prof |
| `financial-analysis-framework` | PDF | — | Framework d'analyse financière institutionnel complet. Classification obligatoir |
| `financial-modeling` | PDF | — | > |
| `gemini-cli` | PDF | — | Wrapper du Gemini CLI officiel (Google, gratuit ~1000 req/jour Gemini 3 Pro via  |
| `gsheet-builder` | [MANQUANT] | — | Cree des Google Sheets professionnels niveau consulting (McKinsey/BCG/Goldman) v |
| `haiku-delegator` | DOC | — | Délègue les tâches mécaniques (grep, parse, list, fetch, extract) à Claude Haiku |
| `idea-to-diagram` | PNG | — | Transforme toute idée, texte ou concept en schéma visuel professionnel (niveau M |
| `image-generator` | IMAGE | — | Generation d'images IA text-to-image multi-provider. Route vers FLUX, GPT-Image, |
| `install-plugin` | PDF | — | Installation facile de plugins, MCP servers et skills pour Claude Code. Guide l' |
| `json-canvas` | DOC | — | Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and conne |
| `layout-qa` | [MANQUANT] | — | Porte de contrôle qualité visuelle obligatoire avant livraison de tout rendu (PD |
| `macro-analysis` | PDF | — | Analyse macroéconomique globale - cycles économiques, politique monétaire (Fed/B |
| `n8n-code-javascript` | PDF | — | Write JavaScript code in n8n Code nodes. Use when writing JavaScript in n8n, usi |
| `n8n-code-python` | PDF | — | Write Python code in n8n Code nodes. Use when writing Python in n8n, using _inpu |
| `n8n-expression-syntax` | PDF | — | Validate n8n expression syntax and fix common errors. Use when writing n8n expre |
| `n8n-management` | PDF | — | Orchestrateur N8N : créer, modifier, déboguer, déployer et auditer des workflows |
| `n8n-mcp-tools-expert` | PDF | — | Expert guide for using n8n-mcp MCP tools effectively. Use when searching for nod |
| `n8n-node-configuration` | PDF | — | Operation-aware node configuration guidance. Use when configuring nodes, underst |
| `n8n-validation-expert` | PDF | — | Interpret validation errors and guide fixing them. Use when encountering validat |
| `n8n-workflow-patterns` | PDF | — | Proven workflow architectural patterns from real n8n workflows. Use when buildin |
| `obsidian-bases` | DOC | — | Create and edit Obsidian Bases (.base files) with views, filters, formulas, and  |
| `obsidian-cli` | DOC | — | > |
| `obsidian-markdown` | MARKDOWN | — | Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, pro |
| `prompt-cache-manager` | DOC | — | Gère le prompt caching Anthropic (ephemeral + 1h TTL) pour deep-research. Use wh |
| `stock-analysis` | PDF | — | Analyse boursière complète d'une action, portefeuille ou IPO. Use when: analyzin |
| `token-economizer` | PDF | — | Orchestrateur d'économie de tokens reasoning-first. Use when: deep-research déma |
| `website-analyzer` | PDF | — | > |

## L4 — DELIVERY (générateurs de livrable)

| Skill | Livrable | Généré par | Description |
|-------|----------|------------|-------------|
| `cover-letter-creator` | PDF | — | Crée des lettres de motivation pro personnalisées par offre (PDF+DOCX). Use when |
| `cv-creator` | PDF | — | Crée des CV professionnels esthétiques et ATS-friendly (PDF+DOCX). Use when crea |
| `flyer-creator` | IMAGE | — | > |
| `image-detourage` | IMAGE | — | > |
| `image-enhancer` | IMAGE | — | > |
| `image-studio` | IMAGE | — | SKILL OBLIGATOIRE AUTO-INVOQUÉ pour TOUTE demande de création ou modification vi |
| `pdf-report-gen` | PDF | — | Genere des rapports PDF institutionnels via pipeline 5 agents (Synthesizer/Desig |
| `pdf-report-pro` | PDF | — | Rapports PDF institutionnels McKinsey/BCG v2 — pipeline 9 phases, moteur Typst P |
| `ppt-creator` | PPT | — | Présentations .pptx éditables McKinsey/BCG via pipeline 6 phases (Strategist, St |

## L5 — QA & DELIVER (validation + envoi)

| Skill | Livrable | Généré par | Description |
|-------|----------|------------|-------------|
| `qa-pipeline` | — | — | Pipeline de contrôle qualité : QA anti-hallucination, Source Validator, Confiden |

## L6 — META (amélioration continue)

| Skill | Livrable | Généré par | Description |
|-------|----------|------------|-------------|
| `feedback-loop` | — | — | Collecte et intégration du feedback utilisateur après chaque livrable. Use when: |
| `retex-evolution` | — | — | RETEX + benchmark continu des IAs + amélioration continue des skills. Use when:  |
| `skill-creator` | PPT | — | Créer, améliorer et auditer des skills Claude Code. Use when: creating new skill |
| `skill-tree-manager` | PPT | — | Gère et maintient l'arborescence intelligente des skills Claude Code. Génère et  |

## Skills sans livrable déclaré

- `gsheet-builder`
- `image-generator`
- `layout-qa`
