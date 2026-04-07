# Template TECHNICAL — Brief

## Audience cible

Developpeurs, ingenieurs DevOps, architectes logiciels, equipes techniques. Lecteurs qui veulent **code + diagrammes + specs** precis.

## Style visuel

- **Police corps** : Inter sans-serif (lisible)
- **Police code** : JetBrains Mono / Fira Code (monospace)
- **Couleurs** : palette teal (#0EA5A4) + accents oranges pour warnings
- **Code blocks** : fond sombre, syntax highlighting Pygments
- **Callouts** : tres utilises ([!NOTE], [!WARNING], [!IMPORTANT])

## Quand l'utiliser

| Situation | Verdict |
|-----------|---------|
| Documentation API | OUI |
| Guide developpeur | OUI |
| Architecture decision record (ADR) | OUI |
| Post-mortem incident | OUI |
| Specification technique | OUI |
| RFC / proposal technique | OUI |
| Note board | NON -> `executive` |
| Etude marche | NON -> `financial` |

## Structure type

```
Cover page (titre + version SDK + classification)
1. TL;DR technique (objectif + stack + status)
2. Probleme / contexte
3. Solution proposee
4. Architecture (diagramme Mermaid graph TD)
5. Specifications detaillees
   - Modeles de donnees
   - Endpoints API (tables)
   - Schemas
6. Exemples de code (avec syntax highlighting)
7. Tests / validation
8. Limitations / edge cases
9. Migration / deploiement
10. References (RFC, liens externes)
```

## KPIs typiques (techniques)

```yaml
kpis:
  - label: Latence p95
    value: 142ms
    change: -28ms
    sentiment: positive
  - label: Throughput
    value: 12.5k req/s
    change: +18%
    sentiment: positive
  - label: Error rate
    value: 0.04%
    change: -0.12pt
    sentiment: positive
  - label: Coverage
    value: 87.3%
    change: +4.1pt
    sentiment: positive
```

## Visualisations recommandees

- **Mermaid `graph TD`** : architecture systeme
- **Mermaid `sequenceDiagram`** : flux d'appels API
- **Mermaid `stateDiagram-v2`** : machines a etats
- **Mermaid `erDiagram`** : modeles de donnees
- Code blocks denses avec langue specifiee (` ```python`, ` ```typescript`)

## Conventions code

- TOUJOURS preciser le langage du bloc code
- Commentaires inline pour expliquer les parties non triviales
- Pas de code > 30 lignes -> renvoyer en gist / annexe
- Tester les snippets avant de les inclure

## Anti-patterns

- Code sans contexte ni explication
- Architecture sans diagramme -> illisible
- Pas de section "limitations" -> developpeurs prendront le code pour acquis
- Snippets non testes
- Mermaid > 20 noeuds -> decouper en sous-diagrammes
- Pas de gestion edge cases / errors

## Exemple de cas d'usage

> "Documentation technique pour le nouveau endpoint /api/v2/payments avec architecture, schema, exemples curl + python, et migration depuis v1"
