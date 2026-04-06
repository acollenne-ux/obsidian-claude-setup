---
name: project-analysis
description: "Analyse complète d'un projet avant tout développement : contraintes, architecture, stack recommandé. Use when: before any development, project planning, tech stack selection. Triggers: 'créer', 'développer', 'nouveau projet', 'architecture'."
argument-hint: "description du projet à analyser"
allowed-tools: WebSearch, WebFetch, mcp__duckduckgo-search__search, Bash, Read
---

## RÈGLE UNIVERSELLE — LIRE L'INTÉGRALITÉ DU SKILL AVANT D'AGIR

**OBLIGATOIRE : Avant d'exécuter quoi que ce soit, tu DOIS :**
1. Lire l'INTÉGRALITÉ de ce fichier SKILL.md (pas juste le début)
2. Comprendre chaque section, chaque règle, chaque contrainte
3. Respecter ce skill À LA LETTRE — ne rien sauter, ne rien simplifier

**Ne JAMAIS commencer l'exécution sans avoir lu et compris TOUT le skill.**

---

# Skill : Analyse de Projet Avant Développement

## Objectif
Avant tout code, comprendre en profondeur le projet, ses contraintes réelles, ce que font les professionnels, et planifier l'approche optimale. Cela évite les erreurs de conception coûteuses et produit un résultat de niveau professionnel dès le premier coup.

## Processus obligatoire

### PHASE 1 — Identification du contexte

Identifie immédiatement :
- **Plateforme cible** : TradingView, web, mobile, desktop, API, CLI, bot, SaaS...
- **Langage imposé ou libre** : Pine Script, Python, JavaScript, TypeScript, Rust...
- **Environnement d'exécution** : navigateur, serveur, local, cloud, exchange API...
- **Utilisateur final** : l'utilisateur lui-même, des clients, usage interne...

### PHASE 2 — Contraintes techniques réelles (CRITIQUE)

Recherche et liste les limites CONCRÈTES de la plateforme cible. Exemples :

**TradingView / Pine Script :**
- Max ~500 lignes de code recommandées (pas de limite stricte mais performance dégradée)
- Max 64 `plot()` par script
- Max 500 barres pour `request.security()` en history
- Pas d'accès réseau externe (pas d'API calls externes)
- Pas de persistance de données entre sessions
- Délai d'exécution max par barre
- Limites sur les tableaux (`array.size` max ~100 000 éléments)
- Différences v5 vs v4 (toujours utiliser v5)

**APIs Exchange (Binance, Crypto.com, etc.) :**
- Rate limits (req/min, poids par endpoint)
- Websocket vs REST selon le use case
- Authentification HMAC-SHA256
- Testnet disponible pour les tests

**Web (React, Next.js, etc.) :**
- SEO constraints si SSG/SSR requis
- Bundle size limits
- CORS si API externe
- Hosting constraints (Vercel, Cloudflare...)

**Python scripts :**
- Memory limits si 4 GB RAM (utilisateur sur 4 GB RAM)
- Compatibilité Python 3.13

Utilise **WebSearch / DuckDuckGo** pour trouver les contraintes actuelles si incertain.

### PHASE 3 — Recherche des meilleures pratiques

Effectue une recherche web ciblée :
```
[plateforme] + [type de projet] + "best practices" OR "professional" OR "tutorial" site:github.com OR medium.com OR tradingview.com
```

Identifie :
- Les patterns utilisés par les développeurs professionnels
- Les librairies/frameworks standards du domaine
- Les pièges et erreurs communes à éviter
- Des exemples open source de référence

### PHASE 4 — Architecture & Plan

Propose une architecture claire :

```
PROJET : [nom]
LANGAGE : [langage] v[version]
PLATEFORME : [cible]

COMPOSANTS :
├── [composant 1] — rôle
├── [composant 2] — rôle
└── [composant 3] — rôle

CONTRAINTES IDENTIFIÉES :
⚠️ [contrainte 1]
⚠️ [contrainte 2]

APPROCHE PROFESSIONNELLE :
→ [pattern recommandé]
→ [librairie recommandée]

RISQUES :
🔴 [risque critique]
🟡 [risque modéré]
```

### PHASE 5 — Sélection des skills & connecteurs

Identifie quels skills et connecteurs Claude Code utiliser pour la réalisation :

| Besoin | Skill/Connecteur |
|--------|-----------------|
| Code complexe multi-fichiers | `dev-team` |
| Interface web design | `frontend-design` |
| Analyse financière intégrée | `stock-analysis` / `macro-analysis` |
| Recherche documentaire | `mcp__claude_ai_Context7__` |
| Données marché temps réel | `mcp__alpha-vantage__` / `mcp__claude_ai_Crypto_com__` |
| Déploiement | `mcp__claude_ai_Vercel__` |
| Tests navigateur | `mcp__playwright__` |

### PHASE 6 — Validation avec l'utilisateur

Avant de coder, présente un résumé concis :

```
## Analyse : [nom du projet]

**Langage/Stack** : [choix + justification]
**Contraintes clés** : [les 2-3 plus importantes]
**Approche** : [résumé de l'architecture]
**Skills utilisés** : [liste]

Confirmes-tu ? Je commence le développement.
```

Si le projet est simple et les contraintes claires, cette validation peut être implicite (un court résumé sans attendre de réponse).

### PHASE 7 — Exécution

Lance les skills appropriés dans l'ordre logique. Pour les projets complexes, utilise `dev-team` qui orchestre plusieurs agents en parallèle (architecture + implémentation + sécurité + tests).

## Règles importantes

- Ne jamais commencer à coder avant d'avoir identifié les contraintes de la plateforme
- Toujours rechercher sur internet ce qui se fait professionnellement (ne pas réinventer)
- Si la plateforme a des limites strictes (plots, lignes, calls), les mentionner AVANT de coder
- Adapter la complexité du projet à la RAM disponible (4 GB sur cette machine)
- Préférer les solutions économes en ressources pour les scripts locaux
- Mentionner si une solution cloud serait plus adaptée

## Cas spéciaux

### TradingView / Pine Script
Toujours vérifier sur pine-script-docs ou TradingView community si une feature existe avant de l'implémenter. Beaucoup de fonctions Python n'existent pas en Pine Script. Consulter `mcp__claude_ai_Context7__` pour la doc Pine Script v5.

### Bots de trading
Toujours proposer un mode paper trading / testnet avant le live. Mentionner les risques financiers. Recommander des stops et safeguards.

### Applications avec données financières
Vérifier les rate limits des APIs utilisées. Proposer un système de cache si les appels sont fréquents.

### Scripts Python lourds
Attention à la RAM (4 GB). Préférer le traitement par chunks, éviter de charger de gros datasets en mémoire.


## BENCHMARK TECHNO MULTI-IA
Avant de recommander une stack :
1. Gemini Flash : évaluer les options techniques (N°1 code 10/10)
2. Mistral Large : analyser en français les avantages/inconvénients
3. Croiser les réponses → choisir la stack avec le meilleur consensus
WebSearch "[framework] vs [alternative] production 2026 benchmark" pour chaque choix.

## PATTERNS RECHERCHE SPÉCIALISÉS PAR DOMAINE
| Domaine | Recherches obligatoires |
|---------|------------------------|
| Web app | "[framework] performance benchmark 2026", "[framework] scalability production" |
| Mobile | "React Native vs Flutter vs native 2026", "[framework] app store performance" |
| Data/ML | "best ML framework production 2026", "[use case] architecture pattern" |
| DevOps | "best CI/CD pipeline 2026", "[cloud] vs [cloud] cost comparison" |
| API | "REST vs GraphQL vs gRPC 2026", "[framework] API performance" |

## RISK ASSESSMENT STRUCTURÉ
Pour chaque projet, évaluer :
| Catégorie | Risque | Probabilité | Impact | Mitigation |
|-----------|--------|-------------|--------|------------|
| Technique | [ex: choix techno inadapté] | Faible/Moyen/Élevé | Faible/Moyen/Élevé | [plan B] |
| Business | [ex: scope creep] | | | |
| Timeline | [ex: dépendances externes] | | | |
| Humain | [ex: compétences manquantes] | | | |
| Sécurité | [ex: données sensibles] | | | |

## CHECKLIST PRÉ-PROJET OBLIGATOIRE
Avant de coder :
- [ ] Objectif clair et mesurable défini
- [ ] Stack techno validée (benchmark multi-IA)
- [ ] Architecture documentée (diagramme)
- [ ] Risques identifiés et mitigations prévues
- [ ] Environnement de dev prêt (dépendances, configs)
- [ ] Tests prévus (unit, integration, e2e)
- [ ] Plan de déploiement défini
- [ ] Estimation effort réaliste

## ESTIMATION EFFORT/TIMELINE
| Complexité | Critères | Durée estimée |
|-----------|----------|---------------|
| Simple | 1 fichier, logique linéaire, pas d'API | 15-30 min |
| Moyenne | 2-5 fichiers, API simple, tests basiques | 1-3 heures |
| Complexe | 5-15 fichiers, multi-API, auth, DB | 3-8 heures |
| Majeur | 15+ fichiers, architecture distribuée | 1-3 jours |
Ajuster : +50% si techno inconnue, +30% si contraintes sécurité.

## SYSTÈME DE CONFIANCE
| Niveau | Critère | Marqueur |
|--------|---------|----------|
| ÉLEVÉ | Stack validée + benchmark pro | ✓✓✓ |
| MOYEN | Stack connue, pas de benchmark | ✓✓ |
| FAIBLE | Stack nouvelle, risques | ✓ |
| SPÉCULATIF | Prototype exploratoire | ~ |


## MATRICE DE FALLBACK — PROJECT ANALYSIS
| Outil principal | Fallback 1 | Fallback 2 |
|----------------|------------|------------|
| Context7 MCP (docs) | WebSearch "[lib] documentation official" | WebFetch doc site |
| Gemini Flash (benchmark) | Mistral Large | DeepSeek-R1 |
| WebSearch (stack comparison) | WebFetch benchmarks sites | Groq validation rapide |
| dev-team (implémentation) | Code direct Gemini | Prototype minimal |

## CHECKLIST OBLIGATOIRE

Créer une tâche TodoWrite pour chaque étape :

1. **Comprendre le besoin** — Quel problème résoudre, pour qui, quelles contraintes
2. **Benchmark pro** — WebSearch des meilleures pratiques pour ce type de projet
3. **Choix de stack** — Langage, framework, DB, hébergement avec justification
4. **Architecture** — Schéma des composants, flux de données, API
5. **Limitations** — Identifier les contraintes techniques, rate limits, edge cases
6. **Plan d'implémentation** — Étapes ordonnées avec dépendances
7. **Dispatch** — Vers `dev-team` avec le plan validé

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "C'est un petit script, pas besoin d'analyse" | Même un script a des contraintes (OS, dépendances, encoding). Analyser TOUJOURS. |
| "Je connais la stack, pas besoin de benchmark" | Les stacks évoluent. Vérifier les best practices 2026 avant de recommander. |
| "L'architecture viendra pendant le développement" | L'architecture se décide AVANT. Refactorer coûte 10x plus cher que planifier. |
| "On verra les limitations plus tard" | Les limitations découvertes tard = temps perdu. Les identifier en amont. |

## RED FLAGS — STOP

- Code commencé sans analyse préalable → STOP
- Stack recommandé sans benchmark → STOP
- Pas de mention des limitations → STOP

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Après analyse | `dev-team` (implémentation) |
| Frontend | `frontend-design` |
| Planification | `superpowers:writing-plans` |
| Validation | `qa-pipeline` |
| Collecte données | `deep-research` |

## ÉVOLUTION

Après chaque analyse de projet :
- Si la stack recommandée était inadaptée → ajuster les critères de sélection
- Si une limitation non prévue est apparue → l'ajouter dans le référentiel
- Si le benchmark était incomplet → enrichir les sources de comparaison

Seuils : si > 2 projets ont nécessité un changement de stack → revoir la méthodologie de sélection.
