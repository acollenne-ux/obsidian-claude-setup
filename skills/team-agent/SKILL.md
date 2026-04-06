---
name: team-agent
description: "Orchestre une équipe d'agents spécialisés en parallèle pour les tâches multi-domaines. Use when: complex multi-domain tasks, parallel agent coordination. Triggers: 'équipe agents', 'multi-domaine', 'agents parallèles'."
  - Projets nécessitant plusieurs spécialistes simultanément
  - Quand deep-research a besoin de coordination inter-agents
  - Situations où les agents doivent se passer des informations entre eux
  - /team, /team-agent, /orchestre
---

## RÈGLE UNIVERSELLE — LIRE L'INTÉGRALITÉ DU SKILL AVANT D'AGIR

**OBLIGATOIRE : Avant d'exécuter quoi que ce soit, tu DOIS :**
1. Lire l'INTÉGRALITÉ de ce fichier SKILL.md (pas juste le début)
2. Comprendre chaque section, chaque règle, chaque contrainte
3. Respecter ce skill À LA LETTRE — ne rien sauter, ne rien simplifier

**Ne JAMAIS commencer l'exécution sans avoir lu et compris TOUT le skill.**

---

# Team Agent — Maître d'Œuvre Multi-Agents

Tu es le **maître d'œuvre**. Tu ne produis pas toi-même le contenu final — tu conçois l'équipe, assignes les rôles, coordonnes les échanges, arbitres les conflits, et assembles la réponse finale à partir des outputs de tes agents.

---

## Principe fondamental

**Un agent = une expertise = un contexte isolé.**

Chaque agent reçoit exactement ce dont il a besoin, ni plus, ni moins. Il ne connaît pas le travail des autres sauf si tu lui transmets explicitement des informations pertinentes. C'est toi, le maître d'œuvre, qui gères les flux d'information entre eux.

---

## Phase 1 — Conception de l'équipe

Analyse la demande et construis l'équipe optimale :

### Catalogue des agents disponibles

| Rôle | Agent / Skill |
|------|--------------|
| Développeur principal | `dev-team` |
| Analyste financier | `stock-analysis` |
| Économiste macro | `macro-analysis` |
| Modélisateur financier | `financial-modeling` |
| Analyste de données | `data-analysis` |
| Debugger | `systematic-debugging` (Superpowers) + `code-debug` |
| Designer frontend | `frontend-design` |
| Chercheur web | WebSearch + WebFetch (multi-requêtes parallèles) |
| Chercheur académique | Hugging Face papers |
| Spécialiste docs | Context7 |
| Revieweur de code | `requesting-code-review` (Superpowers) |
| Planificateur | `writing-plans` (Superpowers) |
| Vérificateur | `verification-before-completion` (Superpowers) |

### Définir pour chaque agent
1. **Sa mission précise** : une phrase claire sur ce qu'il doit produire
2. **Son contexte** : uniquement les informations dont il a besoin
3. **Son output attendu** : format et niveau de détail
4. **Ses dépendances** : doit-il attendre le résultat d'un autre agent ?

---

## Phase 2 — Plan de coordination

Avant de dispatcher, établis le graphe de dépendances :

```
Agents indépendants (peuvent tourner en parallèle) :
  ├── Agent A : [mission]
  ├── Agent B : [mission]
  └── Agent C : [mission]

Agents séquentiels (dépendent d'un output précédent) :
  └── Agent D : [mission] ← nécessite output de Agent A
      └── Agent E : [mission] ← nécessite output de Agent D
```

**Règle** : paralléliser au maximum. Ne séquencer que si une vraie dépendance logique l'impose.

---

## Phase 3 — Dispatch des agents

Lancer tous les agents indépendants en même temps via `dispatching-parallel-agents` (Superpowers).

**Chaque brief d'agent doit contenir :**
- Contexte minimal nécessaire (pas l'historique complet)
- Mission claire et délimitée
- Format d'output attendu
- Contraintes spécifiques à respecter

---

## Phase 4 — Communication inter-agents

Après les premiers outputs, identifier les informations à transmettre entre agents :

**Pattern de communication :**
```
Output Agent A → extrait l'information clé → inject dans brief Agent D
Output Agent B → extrait la contrainte → communique à Agent C pour ajustement
```

Si deux agents produisent des outputs contradictoires :
1. Identifier précisément le point de conflit
2. Relancer un agent arbitre avec les deux outputs en contexte
3. Demander une résolution argumentée

---

## Phase 5 — Synthèse et cohérence

Assembler tous les outputs en une réponse unifiée :

- Vérifier la cohérence globale (pas de contradiction entre agents)
- Combler les gaps (zones non couvertes par aucun agent)
- Signaler explicitement les points où les agents divergent, avec les deux perspectives

---

## Phase 6 — Vérification finale (Superpowers)

Appliquer `verification-before-completion` sur la réponse assemblée.

Si du code est inclus → appliquer `requesting-code-review`.

**Aucune livraison sans preuve de vérification.**

---

## Format de livraison

```
## Résultat — [Sujet]

[Synthèse des agents]

---
Équipe mobilisée : [liste des agents avec leur rôle]
Communications inter-agents : [ce qui a été transmis entre agents]
Conflits résolus : [si applicable]
Vérification : [superpowers appliqués]
```

## AUTO-DÉCOUVERTE DES AGENTS DISPONIBLES
Avant d'assigner des tâches, TOUJOURS :
1. Scanner les skills disponibles dans le system-reminder
2. Identifier les MCPs actifs et leurs capacités
3. Mapper chaque sous-tâche → meilleur agent/skill/MCP
4. Si aucun agent adapté → créer un agent ad-hoc avec prompt spécialisé

## AGENT MANAGER — MONITORING SANTÉ
Surveiller en continu :
| Métrique | Seuil alerte | Action |
|----------|-------------|--------|
| Temps réponse agent | > 5 min | Relancer ou fallback |
| Qualité output | < 6/10 | Reformuler prompt + relancer |
| Taux échec | > 30% | Remplacer par agent alternatif |
| Redondance | 2 agents même tâche | Stopper le moins performant |

## FEEDBACK LOOP FORMALISÉ
Protocole de passage d'information entre agents :
1. Agent A produit output → évaluation qualité
2. Si qualité >= 7/10 → transmettre à Agent B comme input
3. Agent B reçoit output A + contexte → ajuste son travail
4. Si contradiction entre A et B → escalade au Chef d'Orchestre
Format : "Agent [A] a trouvé [résultat]. Utilise cette info pour [ta tâche]."

## FALLBACKS EXPLICITES PAR AGENT
| Agent principal | Fallback | Condition de bascule |
|----------------|----------|---------------------|
| stock-analysis | WebSearch x5 + Gemini | MCP indisponible |
| macro-analysis | FRED API + Mistral Large | Sources offline |
| dev-team | Gemini Flash seul | Agents surchargés |
| data-analysis | pandas + matplotlib direct | Outils complexes échouent |
| code-debug | Stack Overflow search + Gemini | Debug auto échoue |

## PROTOCOLE RÉSOLUTION CONFLITS
Quand 2+ agents produisent des outputs contradictoires :
1. Identifier la source de chaque affirmation
2. Vérifier quelle source est la plus fiable/récente
3. Si même fiabilité → lancer vérification croisée (3e IA)
4. Documenter la divergence et la décision prise
5. Informer l'utilisateur si l'incertitude reste élevée

## MÉTRIQUES PERFORMANCE PAR AGENT
Tracker après chaque session :
- Score qualité /10 par agent
- Temps de réponse moyen
- Taux de réattribution (combien de fois fallback activé)
- Domaines de force identifiés
Stocker dans RETEX pour optimisation future du routage.

## LOAD BALANCING
| Charge système | Max agents parallèles | Stratégie |
|---------------|----------------------|-----------|
| Normale | 5 agents | Parallélisation maximale |
| Élevée | 3 agents | Prioriser critiques |
| Très élevée | 2 agents | Séquentiel, agents clés uniquement |
| Rate limit | 1 agent | File d'attente FIFO |


## ROUTAGE MULTI-IA PAR TYPE DE TÂCHE
| Tâche orchestrée | IA Primaire | Justification |
|-----------------|------------|---------------|
| Coordination finance | Gemini Flash | N°1 calculs 10/10 |
| Coordination FR | Mistral Large | N°1 français 10/10 |
| Arbitrage contradictions | TOUTES en parallèle | Consensus voting |
| Validation rapide agents | Groq (2.8s) | Vitesse |

## SYSTÈME DE CONFIANCE ORCHESTRATION
| Niveau | Critère | Marqueur |
|--------|---------|----------|
| ÉLEVÉ | 3+ agents concordants, sources vérifiées | ✓✓✓ |
| MOYEN | 2 agents concordants | ✓✓ |
| FAIBLE | 1 agent seul, non vérifié | ✓ |
| SPÉCULATIF | Estimation sans données | ~ |
Si confiance globale < 6/10 → signaler incertitude à l'utilisateur.

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Un seul agent suffit pour cette tâche" | Si la tâche est multi-domaine, TOUJOURS dispatcher vers plusieurs agents. |
| "Les agents peuvent travailler sans coordination" | Sans chef d'orchestre, les outputs divergent. Toujours consolider. |
| "L'agent X a raison, on ignore l'agent Y" | Les contradictions entre agents doivent être SIGNALÉES, pas ignorées. |
| "Tous les agents en séquentiel" | Paralléliser les agents indépendants. Séquentiel uniquement si dépendance. |
| "Pas besoin de consolider, les résultats sont cohérents" | TOUJOURS consolider. La cohérence apparente peut masquer des lacunes. |

## RED FLAGS — STOP

- Tâche multi-domaine traitée par un seul agent → STOP
- Contradiction entre agents non signalée → STOP
- Agents lancés en séquentiel quand parallèle possible → STOP

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Invoqué par | `deep-research` (prérequis obligatoire) |
| Dispatch vers | Tous les skills domaine selon la tâche |
| Validation consolidée | `qa-pipeline` |
| Feedback | `feedback-loop` |
| RETEX | `retex-evolution` |

## ÉVOLUTION

Après chaque orchestration :
- Si un agent a échoué → identifier pourquoi et ajuster le dispatch
- Si la consolidation était faible → renforcer les critères de cohérence
- Si des agents étaient redondants → optimiser l'allocation

Seuils : confiance consolidée < 7/10 → revoir la stratégie de dispatch.
