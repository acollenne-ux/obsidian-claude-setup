---
name: dev-team
description: >
  Invoqué automatiquement dès que l'utilisateur demande de créer, développer, coder,
  construire, faire ou implémenter quelque chose : une application, un site web, une API,
  un script, un dashboard, un bot, une feature, un composant, un outil, une extension,
  un jeu, un programme, un projet from scratch ou l'ajout de fonctionnalités à du code
  existant. Orchestre une équipe d'agents spécialisés en parallèle avec un niveau
  d'analyse approfondi (sécurité, performance, architecture, tests) pour produire du
  code production-ready du premier coup. Use when: creating applications, developing features, writing code, building projects. Triggers: 'créer', 'développer', 'coder', 'construire', 'implémenter'.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Agent
effort: high
context: fork
---

<HARD-GATE>
JAMAIS de code sans :
1. Avoir compris le besoin complet (pas de coding avant clarification)
2. Avoir vérifié les patterns existants du projet
3. Avoir identifié les dépendances et limitations
</HARD-GATE>

## RÈGLE UNIVERSELLE — LIRE L'INTÉGRALITÉ DU SKILL AVANT D'AGIR

**OBLIGATOIRE : Avant d'exécuter quoi que ce soit, tu DOIS :**
1. Lire l'INTÉGRALITÉ de ce fichier SKILL.md (pas juste le début)
2. Comprendre chaque section, chaque règle, chaque contrainte
3. Respecter ce skill À LA LETTRE — ne rien sauter, ne rien simplifier

**Ne JAMAIS commencer l'exécution sans avoir lu et compris TOUT le skill.**

---

# Skill : Dev Team — Équipe de développement parallèle

Quand invoqué, NE PAS coder immédiatement. Suivre ce protocole exact.

## Phase 0 : Analyse de la demande (30 secondes)

Avant tout, identifier :
- **Type de projet** : web app / API / script / site statique / mobile / CLI / lib / autre
- **Stack probable** : déduire depuis le contexte ou demander si vraiment ambigu
- **Taille** : micro (< 200 lignes) / small (< 1k) / medium (1k-10k) / large (> 10k)
- **Code existant ?** : scanner le repo courant avec Glob/Grep si pertinent

Pour les projets **micro/small** : traiter en un seul agent (pas de parallélisme inutile).
Pour les projets **medium/large** : décomposer en agents parallèles.

---

## Phase 1 : Architecture (toujours en premier)

Définir AVANT de coder :
1. **Structure des fichiers** : arborescence complète
2. **Interfaces entre modules** : types, contrats d'API internes
3. **Dépendances** : librairies choisies + justification (préférer les standards du projet existant)
4. **Points d'attention** : sécurité, perf, scalabilité dès la conception

---

## Phase 2 : Décomposition en agents parallèles (medium/large)

Lancer simultanément dans UN SEUL message :

### Agent Implémentation Core
- Coder le cœur fonctionnel
- Respecter l'architecture définie
- Nommer les fonctions/variables clairement
- Pas de commentaires inutiles, code auto-documenté

### Agent Sécurité & Qualité
Appliquer systématiquement :
- Validation de TOUTES les entrées utilisateur (Zod, Pydantic, etc.)
- Pas de secrets en dur (env vars)
- Pas d'injection SQL/commandes/XSS possibles
- Authentification/autorisation si nécessaire
- Gestion d'erreurs explicite (pas de `catch {}` vide)
- Logs utiles sans données sensibles

### Agent Tests
- Tests unitaires pour chaque fonction non-triviale
- Tests d'intégration pour les flux principaux
- Happy path + edge cases + cas d'erreur
- Mocks pour les dépendances externes
- Coverage > 80% des branches critiques

### Agent Performance & UX
- Pas de N+1 queries
- Lazy loading si pertinent
- Debounce/throttle sur les events répétés
- Loading states, error states, empty states (UI)
- Accessibilité de base (aria labels, contraste)

---

## Phase 3 : Synthèse et livraison

Après les agents parallèles :
1. **Assembler** le code de tous les agents en fichiers cohérents
2. **Vérifier** les interfaces (les agents ne se voient pas entre eux)
3. **Produire** les fichiers finaux complets (pas de "..." ou de TODO)
4. **Ajouter** les instructions de lancement en 3 lignes max

---

## Standards de code (appliqués par tous les agents)

### Toujours
- Code complet et fonctionnel — jamais de placeholder
- Gestion d'erreurs sur tous les appels réseau/filesystem
- Types explicites (TypeScript strict, Python type hints)
- Fonctions courtes (< 30 lignes), responsabilité unique

### Jamais
- Dépendances inutiles pour des choses faisables nativement
- Over-engineering (YAGNI)
- Commentaires qui répètent le code
- `any` en TypeScript sans justification
- `eval()`, `exec()`, `innerHTML =` avec data user

### Stack defaults (si non précisé)
- **Web full-stack** : Next.js 15 + TypeScript + Tailwind + Prisma
- **API Python** : FastAPI + Pydantic + SQLAlchemy
- **Script Python** : stdlib first, uv pour les deps
- **CLI** : Python (typer) ou Node (commander)
- **Site statique** : HTML/CSS/JS vanilla ou Astro

---

## Cas spéciaux

### Si projet déjà existant dans le repo
1. Scanner avec Glob + Grep pour comprendre la stack existante
2. S'adapter aux conventions déjà en place (pas de refactoring non demandé)
3. Vérifier les imports existants avant d'en ajouter

### Si la demande est vague
Proposer 2-3 options architecturales avec trade-offs, laisser choisir AVANT de coder.

### Si erreur lors du développement
Ne pas contourner (--no-verify, try/catch vide). Diagnostiquer et corriger.

## CODE REVIEW MULTI-IA OBLIGATOIRE
Avant livraison, le code DOIT être vérifié par au moins 2 IAs :
1. **Gemini Flash** (N°1 code 10/10) : vérification syntaxe, logique, performance
2. **DeepSeek-R1** (raisonnement) : vérification architecture, edge cases, sécurité
Si divergence entre les 2 → analyser et résoudre avant livraison.

## TESTS AUTOMATISÉS OBLIGATOIRES
TOUJOURS avant livraison :
1. **Tests unitaires** : chaque fonction critique testée
2. **Tests d'intégration** : composants connectés ensemble
3. Exécuter les tests ET vérifier que tous passent
4. Si un test échoue → fix obligatoire avant livraison
Framework par langage : pytest (Python), jest (JS), go test (Go)

## PROTOCOLE COMMUNICATION INTER-AGENTS
Format message standard entre agents :
```
[AGENT: nom] → [AGENT: destinataire]
TYPE: info | demande | alerte | livrable
CONTENU: [message structuré]
PRIORITÉ: haute | moyenne | basse
DÉPENDANCE: [ce qui est bloqué par cette communication]
```

## FALLBACK ARCHITECTURAL
| Approche initiale | Si échoue | Raison |
|------------------|-----------|--------|
| Microservices | Monolithe modulaire | Trop complexe pour le scope |
| SPA React | SSR Next.js | SEO requis |
| REST API | GraphQL | Trop de endpoints |
| SQL | NoSQL | Données non structurées |
| Cloud native | Docker local | Budget/simplicité |

## INTÉGRATION CONTEXT7 MCP
TOUJOURS utiliser Context7 pour les docs techniques :
- Vérifier la version exacte de chaque librairie
- Consulter les breaking changes récents
- Valider la syntaxe API avant utilisation

## BENCHMARK PERFORMANCE CODE
Après livraison, mesurer :
- Temps d'exécution (benchmark vs baseline)
- Utilisation mémoire
- Nombre de requêtes réseau
- Taille du bundle (frontend)
Si performance < seuil acceptable → optimiser avant livraison.

## SYSTÈME DE CONFIANCE CODE
| Niveau | Critère | Marqueur |
|--------|---------|----------|
| ÉLEVÉ | Code testé + review multi-IA | ✓✓✓ |
| MOYEN | Code logique, tests partiels | ✓✓ |
| FAIBLE | Code non testé | ✓ |
| SPÉCULATIF | Prototype/POC | ~ |

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "C'est un petit script, pas besoin d'architecture" | Même un script de 50 lignes peut avoir des edge cases. Toujours réfléchir avant de coder. |
| "Je connais ce pattern, pas besoin de vérifier" | Les conventions du PROJET priment sur les conventions générales. Toujours lire le code existant. |
| "Je vais tout coder d'un coup" | Découper en étapes. Tester chaque étape. |
| "Le code compile, c'est bon" | Compilation ≠ correction. Tester les edge cases. |
| "Pas besoin de tests pour ce changement" | Si le changement peut casser quelque chose, il a besoin d'un test. |

## RED FLAGS — STOP

- Code sans avoir lu le code existant → STOP
- Pas de gestion d'erreur → STOP
- Fichier > 300 lignes sans découpage → STOP

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Avant développement | `project-analysis` |
| Debug | `code-debug` |
| Frontend | `frontend-design` |
| Planification | `superpowers:writing-plans` |
| Tests | `superpowers:test-driven-development` |
| Review | `qa-pipeline` |
| Export | `pdf-report-gen` |

## ÉVOLUTION

Après chaque développement :
- Si un pattern se répète → créer un template réutilisable
- Si une erreur récurrente → l'ajouter aux anti-patterns
- Si un outil manque → l'ajouter dans la matrice d'outils

Seuils : si > 3 bugs dans le code produit → revoir le processus de validation.
