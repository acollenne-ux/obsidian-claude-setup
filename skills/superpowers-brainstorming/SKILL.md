---
name: superpowers-brainstorming
description: Explorer l'intention réelle, les exigences et le design avant d'agir. Garantit qu'on répond à la bonne question. Prérequis obligatoire du mega-skill deep-research.
argument-hint: "description de la demande à explorer"
allowed-tools: WebSearch, WebFetch, Bash
---

## RÈGLE UNIVERSELLE — LIRE L'INTÉGRALITÉ DU SKILL AVANT D'AGIR

**OBLIGATOIRE : Avant d'exécuter quoi que ce soit, tu DOIS :**
1. Lire l'INTÉGRALITÉ de ce fichier SKILL.md (pas juste le début)
2. Comprendre chaque section, chaque règle, chaque contrainte
3. Respecter ce skill À LA LETTRE — ne rien sauter, ne rien simplifier

**Ne JAMAIS commencer l'exécution sans avoir lu et compris TOUT le skill.**

---

# Skill : Superpowers Brainstorming

## Rôle
Explorer en profondeur l'intention de l'utilisateur AVANT toute exécution. Ce skill garantit qu'on répond à la **bonne question**, pas juste à la question posée.

## Déclencheurs
- Invoqué automatiquement par `deep-research` avant chaque exécution
- Peut être invoqué manuellement pour toute demande complexe ou ambiguë

## ÉTAPE 1 — DÉCODAGE DE L'INTENTION

Pour chaque demande, répondre à ces questions :

```
BRAINSTORMING — [titre de la demande]

1. CE QUE L'UTILISATEUR DIT : [reformulation exacte]
2. CE QU'IL VEUT VRAIMENT : [intention profonde, au-delà des mots]
3. CE QU'IL NE DIT PAS MAIS ATTEND : [implicites, standards du domaine]
4. CONTEXTE MANQUANT : [infos nécessaires non fournies]
5. HYPOTHÈSES À VALIDER : [ce qu'on suppose]
```

## ÉTAPE 2 — EXPLORATION DES EXIGENCES

Pour chaque exigence, classifier :

| Exigence | Type | Priorité | Source |
|----------|------|----------|--------|
| [description] | Fonctionnelle / Non-fonctionnelle / Contrainte | MUST / SHOULD / COULD | Explicite / Implicite / Standard |

### Types d'exigences à explorer :

**Fonctionnelles :** Que doit faire le livrable exactement ?
- Inputs attendus, outputs attendus
- Cas nominaux ET cas limites
- Format et structure du résultat

**Non-fonctionnelles :** Comment doit-il le faire ?
- Performance (temps, volume)
- Qualité (précision, fiabilité)
- Maintenabilité (si code)
- Sécurité (si données sensibles)

**Contraintes :** Qu'est-ce qui limite les options ?
- Outils disponibles / indisponibles
- Temps imparti
- Compétences requises
- Dépendances externes

## ÉTAPE 3 — DESIGN DE LA SOLUTION

Avant d'exécuter, proposer 2-3 approches :

```
APPROCHE A — [nom]
  Description : [résumé en 1-2 phrases]
  Avantages   : [liste]
  Inconvénients: [liste]
  Outils requis: [liste]
  Temps estimé : [estimation]

APPROCHE B — [nom]
  Description : [résumé en 1-2 phrases]
  Avantages   : [liste]
  Inconvénients: [liste]
  Outils requis: [liste]
  Temps estimé : [estimation]
```

**Recommandation :** [A ou B, avec justification]


## ÉTAPE 4 — CHECKLIST PRÉ-EXÉCUTION

Avant de lancer l'exécution, vérifier :

- [ ] L'intention réelle est comprise (pas juste les mots)
- [ ] Les exigences implicites sont identifiées
- [ ] Les contraintes techniques sont listées
- [ ] L'approche recommandée est choisie
- [ ] Les outils nécessaires sont disponibles
- [ ] Les risques principaux sont anticipés
- [ ] Le format de sortie attendu est clair

## ÉTAPE 5 — QUESTIONS À POSER (si nécessaire)

Si des ambiguïtés critiques subsistent, poser les questions AVANT d'exécuter.
Limiter à 2-3 questions maximum pour ne pas bloquer le flux.

**Règle :** Si l'utilisateur a donné des autorisations permanentes et que l'ambiguïté est mineure → choisir l'option la plus probable et noter l'hypothèse. Ne poser une question que si le risque de se tromper est élevé.

## Format de sortie

Le brainstorming produit une **fiche de cadrage** qui est passée aux agents suivants (team-agent, Chef d'Orchestre). Cette fiche sert de référence tout au long de l'exécution pour vérifier l'alignement.
