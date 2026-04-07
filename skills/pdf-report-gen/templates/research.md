# Template RESEARCH — Brief

## Audience cible

Chercheurs, academiques, analystes de fond, equipes R&D, etudiants en master/doctorat. Lecteurs qui veulent **rigueur methodologique + sources tracables + raisonnement profond**.

## Style visuel

- **Police corps** : Cambria / Garamond (serif academique)
- **Couleurs** : sobre, tres peu de couleur (noir + bleu sobre pour liens)
- **Footnotes** : tres prominentes, style APA en bas de page
- **Citations** : `[^1]` rendues en superscript visible
- **Tables** : style "academic paper", bordures fines

## Quand l'utiliser

| Situation | Verdict |
|-----------|---------|
| Etude de fond academique | OUI |
| Litterature review | OUI |
| Memoire / these / paper | OUI |
| Etude empirique avec donnees | OUI |
| Rapport de recherche corporate (R&D) | OUI |
| Memo board | NON -> `executive` |
| Doc API | NON -> `technical` |

## Structure type

```
Cover page (titre complet + auteur + classification + date)
Abstract (10-15 lignes, autonome)
1. Introduction
   - Question de recherche
   - Hypotheses
   - Contributions
2. Etat de l'art / litterature
3. Methodologie
   - Donnees collectees
   - Outils / methodes
   - Limitations methodologiques
4. Resultats
   - Tableaux
   - Figures
   - Tests statistiques
5. Discussion
   - Interpretation
   - Limites
   - Pistes futures
6. Conclusion
Annexes
Bibliographie (style APA / IEEE)
```

## KPIs typiques (academiques)

```yaml
kpis:
  - label: N (echantillon)
    value: 1247
    sentiment: neutral
  - label: p-value
    value: <0.001
    sentiment: positive
  - label: R squared
    value: 0.84
    sentiment: positive
  - label: Sources citees
    value: 47
    sentiment: neutral
```

## Visualisations recommandees

- Scatter plots (correlations)
- Histogrammes (distributions)
- Box plots (groupes)
- Tables denses avec valeurs + std
- Mermaid `graph TD` pour le pipeline methodologique

## Sourcing OBLIGATOIRE

- **Chaque fait** doit avoir une footnote `[^N]`
- **Chaque footnote** doit avoir : auteur, annee, titre, journal/editeur, URL/DOI
- Bibliographie en fin avec **toutes** les references (pas de "et al." imprecis)
- Format APA 7e edition recommande

## Anti-patterns

- "Selon plusieurs sources..." sans citation -> reformuler avec footnotes
- Footnotes vides ("Source: internet")
- Conclusions plus larges que les donnees -> garder l'humilite scientifique
- Pas de section "limitations methodologiques"
- Citations Wikipedia non doublees par source primaire
- Affirmations causales sans p-values

## Exemple de cas d'usage

> "Etude empirique sur l'impact des publications de la Fed sur la volatilite des marches actions, periode 2010-2025, avec methodologie event study et 50+ references academiques"
