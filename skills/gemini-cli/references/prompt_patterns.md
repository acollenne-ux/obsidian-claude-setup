# Templates de prompts pour Gemini 3 Pro

## Pattern 1 — Vision : screenshot chart → Pine Script

```
Analyse cette image de chart TradingView et génère un indicateur Pine Script v6 qui reproduit le comportement visuel observé.

Contraintes :
- Pine Script v6 strict
- Un seul fichier, compilable sans erreur
- Commenter chaque bloc logique
- Pas de repaint (éviter lookahead_on)
- Si un pattern est ambigu, proposer 2 variantes

Image ci-jointe.
```

## Pattern 2 — Vision : maquette → HTML/CSS

```
Convertis cette maquette en HTML + CSS Tailwind propre.

Contraintes :
- Mobile-first, responsive
- Utiliser les classes Tailwind standard (pas de custom CSS sauf nécessaire)
- Respecter la hiérarchie visuelle
- Alt text sur toutes les images
- Pas de JavaScript

Image ci-jointe.
```

## Pattern 3 — Vision : croquis → Mermaid

```
Voici un schéma dessiné à la main. Convertis-le en diagramme Mermaid.

Contraintes :
- Syntaxe Mermaid v10+
- Type le plus adapté (flowchart TD / sequenceDiagram / classDiagram / stateDiagram)
- Conserver les labels exacts du croquis
- Si un élément est illisible, signaler dans un commentaire `%%`

Image ci-jointe.
```

## Pattern 4 — Génération diagramme pure (texte)

```
Génère un diagramme Mermaid représentant [CONCEPT].

Contraintes :
- flowchart TD
- Maximum 15 nœuds (lisibilité)
- Grouper par couches avec `subgraph`
- Thème : couleurs neutres, lisible noir et blanc
- Uniquement le code Mermaid, pas d'explication
```

## Pattern 5 — Résumé long contexte

```
Voici [N] sources sur le sujet X. Produis un résumé structuré :

1. Consensus (ce qui revient dans ≥ 3 sources)
2. Points de divergence (contradictions entre sources)
3. Zones d'incertitude
4. Sources numérotées utilisées pour chaque point

Format : Markdown, sections claires, pas de bullshit marketing.

Sources :
[...]
```

## Pattern 6 — Benchmark cross-IA

```
Réponds à cette question en 3 parties :

1. Ta réponse directe (max 200 mots)
2. Les 2 alternatives que tu as écartées et pourquoi
3. Ton niveau de confiance (0-10) + ce qui te manquerait pour atteindre 10

Question : [...]
```
(Utilisé par `multi-ia-router --aggregate` pour comparer Gemini vs Claude.)

## Pattern 7 — Code review rapide

```
Review ce code. Focus uniquement sur :

1. Bugs avérés (pas stylistiques)
2. Risques de sécurité
3. Edge cases non gérés

Ignore : style, naming, micro-optim. Sois direct, pas de diplomatie.

Langage : [...]
Code :
[...]
```

## Règles générales Gemini 3

- **Français** : Gemini 3 Pro répond très bien en français, pas besoin de traduire
- **Contexte long** : ne pas hésiter à coller des docs entières (jusqu'à 1M tokens)
- **Images multiples** : supporté, jusqu'à ~3000 images par requête
- **Structured output** : demander explicitement JSON si besoin, Gemini respecte bien le schéma
- **System prompt** : moins efficace que chez Claude, préférer intégrer les instructions directement dans le user prompt
