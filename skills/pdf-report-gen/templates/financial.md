# Template FINANCIAL — Brief

## Audience cible

Analystes financiers, gerants de portefeuille, traders, investisseurs avertis. Lecteurs qui veulent **chiffres + ratios + thesis** dense.

## Style visuel

- **Police** : Inter / Helvetica sans-serif (style "Bloomberg / FactSet")
- **Mise en page** : dense, multi-colonnes possibles, tableaux nombreux
- **Couleurs** : bleu marine + accents vert (positif) / rouge (negatif)
- **KPI cards** : tres visibles en haut de document
- **Footer** : ticker + date + classification

## Quand l'utiliser

| Situation | Verdict |
|-----------|---------|
| Note d'analyse boursiere | OUI |
| Pitch investissement | OUI |
| Rapport trimestriel financier | OUI |
| Comparable companies analysis | OUI |
| DCF / valorisation | OUI |
| Note strategique board | NON -> `executive` |
| Doc technique API | NON -> `technical` |

## Structure type

```
Cover page (ticker + secteur + classification)
KPI Dashboard (8 KPIs : Price, Market Cap, P/E, EPS, Revenue YoY, ...)
1. Investment thesis (3-5 bullets)
2. Resume executif
3. Contexte secteur + macro
4. Analyse fondamentale
   - Revenus, marges, cash flow
   - Bilan, dette, liquidite
5. Analyse de valorisation
   - Multiples (P/E, EV/EBITDA, P/B)
   - Comparables (peers table)
   - DCF (si pertinent)
6. Catalyseurs court terme
7. Risques (top 5)
8. Scenarios (Bull/Base/Bear avec price targets)
9. Recommandation (BUY/HOLD/SELL + price target + horizon)
Annexes (sources Bloomberg, Reuters, FMP, ...)
```

## KPIs typiques (5 a 8)

```yaml
kpis:
  - label: Price
    value: 178.50 USD
    change: +2.3%
    sentiment: positive
  - label: Market Cap
    value: 2.85T USD
    change: +1.5%
    sentiment: positive
  - label: P/E (TTM)
    value: 28.4x
    change: -0.8x
    sentiment: positive
  - label: EPS (NTM)
    value: 6.78 USD
    change: +12.4%
    sentiment: positive
  - label: Revenue YoY
    value: +18.2%
    change: +3.1pt
    sentiment: positive
  - label: FCF Margin
    value: 31.2%
    change: +1.4pt
    sentiment: positive
```

## Visualisations recommandees

- Evolution price (line, 1Y / 5Y)
- Revenue / earnings YoY (bar)
- Multiples vs peers (hbar)
- Marge progression (area)
- 1 mermaid si waterfall financier
- KPI cards generees automatiquement par frontmatter

## Sources OBLIGATOIRES

- Bloomberg, Reuters, Investing.com, Zonebourse
- FMP, Alpha Vantage (donnees structurees)
- Sec.gov / Boursorama (filings)
- Note de minimum 3 sources differentes

## Anti-patterns

- KPIs vagues sans valeur ("Croissance: forte")
- Pas de price target -> recommandation incomplete
- Pas de scenarios bull/bear -> these unilaterale
- Tableaux non sources
- Confondre EPS / FCF / EBITDA dans la meme colonne

## Exemple de cas d'usage

> "Analyse complete Apple (AAPL) avec these d'investissement, valorisation DCF, peers comparison, et price target 12 mois"
