---
name: financial-analysis-framework
description: "Framework d'analyse financière institutionnel complet. Classification obligatoire en 8 types d'actifs. 15 dimensions + 10 analyses complémentaires. Use when: analyzing stocks, companies, financial assets. Triggers: 'analyse action', 'valorisation', 'fundamental analysis'."
---

# Financial Analysis Framework — Analyse Institutionnelle Complète

<HARD-GATE>
JAMAIS d'analyse sans :
1. Classification de l'actif en 8 types (Growth, Micro-cap, Cyclique, Défensif, REIT, Crypto, Obligation, ETF)
2. Minimum 3 sources de données fraîches (Alpha Vantage, FMP, WebSearch)
3. Minimum 3 méthodes de valorisation croisées
4. Scénarios bull/base/bear OBLIGATOIRES
</HARD-GATE>

## POSTURE

Tu es un **analyste financier institutionnel**. Tu ne te bases que sur des **données tangibles et à jour**. Jamais d'hallucination, jamais de donnée obsolète. Tu cherches l'entreprise qui va croître de manière exponentielle tout en limitant le risque au maximum.

---

## ÉTAPE 0 — CLASSIFICATION DE L'ACTIF (OBLIGATOIRE)

**On ne peut PAS analyser Microsoft, IEVA Group et Murapol de la même manière.**
Toujours identifier le type AVANT de commencer.

```
FICHE ACTIF — [ticker / nom]

Classe d'actif     : Action | Crypto | Obligation | ETF/Fonds | Commodité
Capitalisation     : Mega-cap (>200B) | Large (10-200B) | Mid (2-10B) | Small (250M-2B) | Micro (<250M) | Nano (<50M)
Style              : Growth | Value | Dividend/Income | Blend
Cycle              : Cyclique | Défensif | Mixte
Secteur GICS       : [Tech, Santé, Finance, Immobilier, Énergie, Matériaux, Conso Discr., Conso Staples, Industrie, Utilities, Communication]
Sous-type spécial  : REIT | Biotech pre-revenue | SPAC | Holding | Conglomérat | IPO récente | Turnaround | Meme stock
Marché             : US (NYSE/NASDAQ) | Europe (Euronext/Xetra/LSE) | Asie | Émergent | OTC
Liquidité          : Haute (>1M vol/jour) | Moyenne (100K-1M) | Faible (<100K) | ⚠️ Très faible (<10K)
Couverture analyste: Forte (10+) | Moyenne (3-10) | Faible (1-2) | ⚠️ Aucune
```

---

## ÉTAPE 0B — ADAPTER LES MÉTRIQUES SELON LE TYPE

### TYPE A — MEGA/LARGE-CAP GROWTH (ex: MSFT, NVDA, ASML)
**Priorités :** ROIC/ROCE tendance 5 ans, TAM expansion, Rule of 40, FCF yield + croissance, moat durabilité, capital allocation, PEG ratio, parts de marché
**Ce qui compte MOINS :** dividende, book value, actifs tangibles
**Risques :** antitrust, disruption tech, compression multiple
**Valorisation :** DCF + comparables + PEG

### TYPE B — MICRO/SMALL-CAP (ex: ALIEV/IEVA, Murapol)
**Priorités :** ⚠️ Liquidité (volume, bid-ask, flottant), survie (cash burn, runway, dette/EBITDA), management (fondateur, track record), concentration clients, dilution, insider ownership, couverture analyste, croissance organique vs acquisition
**Ce qui compte MOINS :** comparables (peu de pairs), consensus (inexistant)
**Risques :** illiquidité, faillite, dilution, gouvernance, homme-clé
**Valorisation :** EV/EBITDA + NAV + DCF prudent (WACC + prime small-cap 3-5%)

### TYPE C — CYCLIQUE (ex: auto, luxe, industrie, construction)
**Priorités :** ⚠️ P/E TROMPEUR (P/E bas haut de cycle = piège), EV/EBITDA à travers le cycle, backlog, taux utilisation capacités, marge normalisée, solidité bilan (dette nette/EBITDA < 2x), sensibilité macro
**RÈGLE D'OR :** Acheter quand P/E ÉLEVÉ (bas de cycle). Vendre quand P/E BAS (haut de cycle).
**Valorisation :** EV/EBITDA normalisé + P/B + remplacement actifs

### TYPE D — DÉFENSIF / DIVIDEND (ex: utilities, pharma, conso staples)
**Priorités :** rendement dividende vs historique, CAGR dividende 5/10 ans, payout ratio (>80% = ⚠️), historique coupe dividende, prévisibilité CA, performance en récession, pricing power
**Valorisation :** DDM + P/E historique + rendement relatif vs obligations

### TYPE E — IMMOBILIER / REIT (ex: Murapol, Unibail, Vonovia)
**⚠️ NE PAS utiliser le P/E classique.**
**Priorités :** FFO/AFFO, Price/AFFO, NAV (prime/décote), taux occupation, Debt/Total Cap + LTV, ICR, cap rate, same-store NOI growth, WALT, dividend yield (AFFO-based)
**Promoteur (Murapol) = TYPE C + E | Foncière (Unibail) = TYPE D + E**

### TYPE F — CRYPTO (ex: BTC, ETH, SOL)
**⚠️ Pas de fondamentaux classiques.** Analyse technique + on-chain (adresses actives, TVL, hash rate) + tokenomics (supply, vesting, unlocks) + sentiment (LunarCrush, Fear & Greed) + corrélation BTC + activité GitHub + volume/liquidité
**Valorisation :** AT + on-chain + sentiment + comparables crypto

### TYPE G — OBLIGATION / FIXED INCOME
**Priorités :** YTM, duration/convexité, rating crédit, spread vs souverain, probabilité défaut, couverture intérêts, clause call
**Valorisation :** Actualisation flux + spread analysis + courbe taux

### TYPE H — ETF / FONDS
**Priorités :** Composition (top holdings, secteurs, géo), TER, tracking error, liquidité (AUM, volume), alpha vs benchmark, Sharpe ratio, drawdown max

---

### INDICATEURS SECTORIELS AVANCÉS (ajouter aux métriques selon le type détecté)

**SaaS / Tech :**
| Indicateur | Formule / Description | Seuil excellent | Seuil ⚠️ | Source |
|-----------|----------------------|----------------|----------|--------|
| Rule of 40 | Revenue growth % + EBITDA margin % | > 40% | < 20% | INCOME_STATEMENT |
| NDR / NRR | Net Dollar Retention (expansion - churn) | > 120% | < 100% | Rapport annuel / WebSearch |
| CAC Payback | CAC / (ARPU × Gross Margin) en mois | < 12 mois | > 24 mois | Rapport annuel |
| LTV/CAC | Customer Lifetime Value / Coût d'acquisition | > 3x | < 1.5x | Calcul depuis rapport |
| Magic Number | Net New ARR / S&M spend trimestre précédent | > 0.75 | < 0.5 | INCOME_STATEMENT |
| Gross Margin | Marge brute (SaaS typiquement >70%) | > 75% | < 60% | INCOME_STATEMENT |

**Banques / Finance :**
| Indicateur | Formule / Description | Seuil excellent | Seuil ⚠️ | Source |
|-----------|----------------------|----------------|----------|--------|
| CET1 Ratio | Common Equity Tier 1 / RWA | > 12% | < 10% | Rapport annuel / WebSearch |
| NIM | (Intérêts perçus - Intérêts payés) / Actifs productifs | > 3% | < 1.5% | INCOME_STATEMENT |
| NPL Ratio | Non-Performing Loans / Total Loans | < 1% | > 3% | Rapport annuel |
| Cost-to-Income | Charges exploitation / PNB | < 50% | > 70% | INCOME_STATEMENT |
| LCR | Actifs liquides haute qualité / Sorties nettes 30j | > 130% | < 110% | Rapport annuel |
| PPNR | Pre-Provision Net Revenue, tendance YoY | En hausse | En baisse | INCOME_STATEMENT |

**Biotech / Pharma :**
| Indicateur | Description | Comment calculer | Source |
|-----------|------------|-----------------|--------|
| Pipeline NPV prob-weighted | Σ (NPV par phase × probabilité succès phase) | Phase I: 10%, II: 25%, III: 55%, NDA: 85% | WebSearch + rapport annuel |
| Patent cliff exposure | % CA protégé par brevets expirant < 5 ans | Identifier top 5 molécules + dates expiration | Rapport annuel + WebSearch |
| R&D Productivity | NME approuvées / R&D $ cumulé (10 ans) | Nombre nouveaux médicaments / dépenses R&D | WebSearch |
| Pipeline depth | Nb molécules Phase I / II / III + diversité thérapeutique | Compter par phase et aire thérapeutique | Pipeline tracker (rapport annuel) |

**Mining / Oil & Gas :**
| Indicateur | Formule / Description | Seuil excellent | Seuil ⚠️ | Source |
|-----------|----------------------|----------------|----------|--------|
| Reserve Life | Réserves prouvées / Production annuelle | > 15 ans | < 8 ans | Rapport annuel |
| AISC | All-In Sustaining Cost par once/baril | Quartile inférieur secteur | Quartile supérieur | Rapport annuel |
| Netback | Prix vente - royalties - coûts production - transport | En hausse YoY | En baisse > 2 trimestres | INCOME_STATEMENT |
| Reserve Replacement Ratio | Nouvelles réserves ajoutées / Production | > 100% | < 80% | Rapport annuel |
| Finding & Development Cost | Coût découverte par baril/once ajouté | En baisse vs historique | En hausse > 20% YoY | Rapport annuel |

**Retail / Distribution :**
| Indicateur | Formule / Description | Seuil excellent | Seuil ⚠️ | Source |
|-----------|----------------------|----------------|----------|--------|
| Same-Store Sales growth | Croissance CA magasins existants > 1 an | > 3% | < 0% (négatif) | Rapport trimestriel |
| Sales per sqft (ou m²) | CA / Surface de vente totale | Au-dessus médiane secteur | En baisse > 2 trimestres | Rapport annuel |
| Inventory Turnover | COGS / Stock moyen | En hausse YoY | En baisse > 2 trimestres | BALANCE_SHEET + INCOME_STATEMENT |
| E-commerce mix | % CA réalisé en ligne | En hausse + > 20% | En baisse | Rapport annuel |
| Shrinkage rate | Démarque connue + inconnue / CA | < 1.5% | > 3% | Rapport annuel |

**Insurance / Assurance :**
| Indicateur | Formule / Description | Seuil excellent | Seuil ⚠️ | Source |
|-----------|----------------------|----------------|----------|--------|
| Combined Ratio | (Sinistres + Frais) / Primes acquises | < 95% | > 100% | Rapport annuel |
| Investment Yield | Rendement portefeuille placements | Stable ou en hausse | En forte baisse YoY | Rapport annuel |
| Book Value CAGR (5 ans) | Croissance annualisée valeur comptable | > 8% | < 3% | BALANCE_SHEET |
| P/Embedded Value | Cours / Valeur intrinsèque actuarielle | < 1.0x (décote) | > 1.5x (surévalué) | WebSearch |
| Solvency II ratio | Fonds propres éligibles / SCR | > 180% | < 130% | Rapport annuel |

---

## ÉTAPE 1 — ANALYSE 15 DIMENSIONS (avec notes /10)

### Dimension 1 — MOAT & AVANTAGES CONCURRENTIELS (analyse approfondie)

**Sous-critères obligatoires :**
- **Type de moat** : réseau, switching costs, intangibles (brevets/marque), coûts, échelle
- **Barrières à l'entrée** : réglementaires, capitaux requis, expertise, réseau de distribution, brevets
- **Monopole / duopole** : l'entreprise est-elle en position dominante ? Combien de concurrents réels ?
- **Pricing power** : capacité à monter ses prix SANS perdre ses clients (test essentiel d'un vrai moat)
- **Effet de réseau** : chaque nouveau client augmente-t-il la valeur pour les autres ? (ex: Visa, Meta)
- **Revenus récurrents / abonnements** : modèle subscription (Netflix, Nespresso) → prévisibilité + stickiness
- **Brevets** : nombre, puissance, domaines couverts, durée restante, défense juridique active
- **Force et durabilité** : Fort / Moyen / Faible + justification + durabilité estimée (3/5/10+ ans)
- **Menaces** : concurrents émergents, disruption techno, substituts, régulation

### Dimension 2 — GAIN DE PARTS DE MARCHÉ
- Évolution parts de marché YoY (chiffres sourcés)
- TAM / SAM / SOM avec sources
- Benchmark vs concurrents directs
- Dynamique : en gain / stable / en perte
- Expansion géographique en cours

### Dimension 3 — SOLIDITÉ FINANCIÈRE
- Dette nette / EBITDA, couverture intérêts (ICR)
- Maturité dette, rating S&P/Moody's
- Trésorerie disponible, runway
- **Stress test** : que se passe-t-il si le CA baisse de 20% ?
- Gestion de la dette : refinancements prévus, covenants

### Dimension 4 — GOUVERNANCE D'ENTREPRISE
- Track record management : turnover direction ? Stabilité ?
- Respect des guidances passées (historique beats/misses sur 8 trimestres)
- Indépendance board, comités audit
- **Analyse employés** (OBLIGATOIRE — voir Étape 2A)
- **Taux d'accidentologie** si disponible (accidents graves = problèmes management)

### Dimension 5 — CROISSANCE D'ENTREPRISE
- Tableau CA / EBITDA / EPS / FCF / Marges sur 3-5 ans + CAGR
- Croissance **organique** vs **acquisition** (SÉPARER les deux)
- Moteurs : pricing power, volume, nouveaux marchés, nouveaux produits
- Consensus analystes vs management guidance
- **Orientation client** : qualité du service, écoute client, NPS si disponible → une entreprise customer-centric dure plus longtemps

### Dimension 6 — CARNET DE COMMANDES & VISIBILITÉ
- Backlog YoY, RPO (SaaS), NRR (Net Revenue Retention)
- Visibilité à 6 / 12 / 24 mois
- **Récurrence revenus** : % récurrent vs one-shot, modèle abonnement ?
- **Dépendance gros clients** : top 5 clients = quel % du CA ? ⚠️ Si >30% = risque
- Saisonnalité et prévisibilité

### Dimension 7 — ALIGNEMENT INTÉRÊTS & TRANSPARENCE
- Insider ownership % (fondateur, management, board)
- Hiérarchie actionnariat : qui contrôle réellement ?
- Institutionnels : top 5, mouvements récents, présence dans les indices
- **Financement par pays / type d'investisseur**
- Transactions liées / conflits d'intérêt
- Transparence communication : qualité rapports, accessibilité, réponses aux questions

### Dimension 8 — RATIO POTENTIEL / RISQUE
**Structure obligatoire (dans cet ordre) :**
1. **D'abord les RISQUES** : lister exhaustivement chaque risque avec probabilité (%) et impact (€/%)
2. **Puis les CATALYSEURS** : lister chaque catalyseur avec horizon temporel et potentiel
3. **Puis le RATIO** : potentiel haussier / risque baissier (ex: +40% / -30% = ratio 1.33)
4. **Note /10** basée sur attractivité du ratio

### Dimension 9 — MOMENT POUR ACHETER (analyse technique)
- Tendance long terme : haussière / baissière / range
- Supports et résistances clés
- RSI, MACD, MM 50j/200j
- Volumes : confirmation ou divergence
- Pattern : breakout, pullback, consolidation
- Signal : **Acheter maintenant / Attendre [niveau] / Ne pas acheter**
- **Si IPO récente** : prix d'entrée vs valorisation fondamentale, pas d'historique technique
- **Saisonnalité du cours** : patterns récurrents annuels ?

### Dimension 10 — QUALITÉ DE LA VALORISATION
**3 niveaux obligatoires :**
1. **Absolue** : PER, EV/EBITDA, FCF yield, P/B (selon secteur)
2. **Relative** : vs concurrents directs + vs historique de la société
3. **Implicite** : qu'est-ce que le marché price déjà ? Si le cours reflète le bull case → pas de marge de sécurité. Si le cours price le bear case → opportunité.

**Comparaison obligatoire :** L'entreprise est-elle sous-évaluée vs ses concurrents ? Sont-elles TOUTES sous-évaluées ? Pourquoi ? (cycle, anomalie de marché, secteur décoté ?)

### Dimension 11 — QUALITÉ DU CASH-FLOW
- FCF : montant, tendance, conversion ratio (FCF/EBITDA)
- Cash flow opérationnel vs résultat net (cohérence ou divergence)
- Capex : maintenance vs croissance
- Working capital : BFR, DSO, DPO, DIO
- Cash burn rate et runway (si négatif)
- **Owner's Earnings** = Résultat net + D&A + variations BFR - capex maintenance (formule Buffett)
- **Cash Conversion Cycle (CCC)** = DSO + DIO - DPO (en jours)
  → Tendance YoY : CCC en baisse = amélioration efficience ; CCC en hausse > 15j YoY = ⚠️ dégradation BFR
  → Comparer au CCC médian du secteur (source : WebSearch "[secteur] average cash conversion cycle")
- **Sloan Accruals Ratio** = (ΔCA - ΔCash - ΔCL + ΔSTD + ΔTP - D&A) / Avg Total Assets
  → Ratio > 10% = ⚠️ qualité bénéfices douteuse (bénéfices "papier" non soutenus par le cash)
  → Ratio < 5% = ✅ bonne qualité cash — bénéfices réels
  → Source : BALANCE_SHEET (2 années) + INCOME_STATEMENT (D&A)
- **Earnings Quality Score composite** (3 composantes) :
  (a) **Accruals ratio** = (Net Income - OCF) / Total Assets → plus proche de 0 = meilleur
  (b) **Persistance des bénéfices** : corrélation EPS année N vs EPS année N+1 sur 5 ans (>0.8 = stable ✅, <0.5 = volatile ⚠️)
  (c) **Divergence Revenue/Earnings** : si CA croît mais bénéfices stagnent ou baissent → ⚠️ compression marges ou charges exceptionnelles
- **Shareholder Yield** = Dividend yield + Buyback yield + Debt paydown yield
  → Mesure plus complète du retour actionnarial que le dividende seul
  → Source : CASH_FLOW (dividends paid + share repurchases + net debt change) / Market Cap

### Dimension 12 — QUALITÉ ALLOCATION DU CAPITAL
- Historique : investissements organiques, M&A, buybacks, dividendes
- ROI des acquisitions passées : ont-elles créé de la valeur ?
- Discipline management : achat quand c'est cher ou quand c'est value ?
- Score Janus : % capital → croissance vs retour actionnaires
- **Analyse M&A** : rachats récents/prévus, rationale stratégique, prix payé vs valeur cible

### Dimension 13 — RENDEMENT DU CAPITAL (ROIC/ROCE)
- ROIC et tendance 3-5 ans
- ROCE
- Comparaison vs WACC → l'entreprise crée-t-elle de la valeur ?
- Comparaison vs pairs secteur
- Spread ROIC - WACC = indicateur de création de valeur
- **DuPont 5-Factor Decomposition** :
  ROE = (Net Income/EBT) × (EBT/EBIT) × (EBIT/Revenue) × (Revenue/Assets) × (Assets/Equity)
  = **Tax Burden** × **Interest Burden** × **EBIT Margin** × **Asset Turnover** × **Equity Multiplier**
  → Identifier le MOTEUR principal du ROE : marge opérationnelle (sain ✅) vs levier financier (risqué ⚠️ si Equity Multiplier > 3x et en hausse)
  → Comparer la décomposition vs 3 pairs directs pour détecter les anomalies
  → Source : INCOME_STATEMENT + BALANCE_SHEET
- **CROCI (Cash Return on Capital Invested)** = Gross Cash Flow / Gross Invested Capital
  → Métrique favorite de Goldman Sachs — plus fiable que le ROIC comptable car élimine les biais d'amortissement et de goodwill
  → Gross Cash Flow = Net Income + D&A + intérêts nets d'impôt
  → Gross Invested Capital = Total Assets - Cash - Goodwill amortissements cumulés + ajustements leasing
  → CROCI > 15% = excellent ✅ | < 8% = faible ⚠️
- **Magic Formula Score (Greenblatt)** = classement par Earnings Yield (EBIT/EV) + classement par ROIC → rang combiné vs pairs
  → Plus le rang combiné est bas, plus l'entreprise est "cheap + quality"
  → Source : INCOME_STATEMENT (EBIT) + quote (EV) + calcul ROIC

### Dimension 14 — RISQUE DE DILUTION
- Nombre d'actions : évolution 3-5 ans
- Stock-based compensation : % CA, tendance
- Convertibles, warrants, options en circulation
- Augmentations de capital prévues ou probables
- Impact sur EPS et valeur par action

### Dimension 15 — OPTIONNALITÉ / CATALYSEURS DE RERATING
- Nouveaux marchés / géographies en cours d'ouverture
- Pipeline produits / innovations
- M&A potentiel (cible ou acheteur)
- Changement de narrative : ce qui pourrait faire changer d'avis le marché
- Inclusion indices, coverage analyste, événements
- **Projets futurs de l'entreprise** : stratégie annoncée, investissements planifiés

---

## ÉTAPE 2 — ANALYSES COMPLÉMENTAIRES (10 BLOCS)

### 2A — ANALYSE EMPLOYÉS & CULTURE D'ENTREPRISE

**OBLIGATOIRE. Sources à consulter :**
```
WebSearch : "[entreprise] Glassdoor avis employés"
WebSearch : "[entreprise] Indeed avis salariés"
WebSearch : "[entreprise] employee reviews complaints"
WebSearch : "[entreprise] grève manifestation syndicat"
WebSearch : "[entreprise] accident travail mortel grave"
WebSearch : "[entreprise] turnover employés démissions"
```

**Analyser :**
- **Score Glassdoor/Indeed** : note globale, tendance (amélioration ou dégradation ?)
- **Thèmes récurrents** : management toxique ? Sous-effectif ? Salaires bas ? Surcharge ?
- **Temporalité** : 10 avis négatifs il y a 10 ans ≠ 10 avis négatifs la semaine dernière
- **Taux d'accidentologie** : accidents graves = coûts élevés + problèmes management profonds
- **Mouvements sociaux** : grèves, manifestations, pétitions, procès prud'homaux
- **Impact sur le développement futur** : une culture toxique freine l'innovation et la rétention

**Livrable :**
```
ANALYSE EMPLOYÉS — [entreprise]
Score Glassdoor   : [X]/5 (tendance ↑↗→↘↓)
Score Indeed       : [X]/5
Thèmes négatifs   : [liste]
Accidentologie    : [données si trouvées]
Mouvements sociaux: [liste avec dates]
Impact estimé     : [Faible / Moyen / Élevé] sur le développement futur
```

### 2B — SWOT APPROFONDI

```
FORCES (internes)                    | FAIBLESSES (internes)
- [force 1 + justification]         | - [faiblesse 1 + justification]
- [force 2]                         | - [faiblesse 2]
                                     |
OPPORTUNITÉS (externes)              | MENACES (externes)
- [opportunité 1 + horizon]         | - [menace 1 + probabilité]
- [opportunité 2]                    | - [menace 2]
```

Ne pas se limiter aux évidences. Chercher les SWOT non consensuels (ce que le marché ne voit pas encore).

### 2C — BUSINESS MODEL (passé, présent, futur)

**Structure obligatoire :**
1. **Passé** : comment l'entreprise gagnait de l'argent il y a 5 ans ? Qu'est-ce qui a changé ?
2. **Présent** : modèle actuel, comment chaque euro de CA est généré, marges par segment
3. **Futur** : vers quoi le management oriente l'entreprise ? Nouveaux business models ? Pivots ?
4. **Durabilité** : le business model est-il réplicable ? Scalable ? Défendable ?

### 2D — RÉPARTITION VENTES & BÉNÉFICES PAR SEGMENT

```
SEGMENTS — [entreprise]

| Segment | % CA | % Bénéfice | Croissance YoY | Marge | Tendance | Projection |
|---------|------|-----------|---------------|-------|----------|------------|
| [Seg 1] | X%   | X%        | +X%           | X%    | ↑↗→↘↓   | [futur]    |
| [Seg 2] | X%   | X%        | +X%           | X%    | ↑↗→↘↓   | [futur]    |
```

**Identifier :**
- Les segments qui **surperforment** (marges élevées, croissance forte)
- Les segments qui **sous-performent** (dilutifs, en déclin)
- Les **petites pépites cachées** : petits segments à forte croissance qui pourraient devenir majeurs
- Les projets futurs dans chaque segment

### 2E — ANALYSE CONCURRENCE COMPARATIVE

```
BENCHMARK CONCURRENCE — [entreprise] vs [concurrent 1] vs [concurrent 2]

| Critère | [Entreprise] | [Concurrent 1] | [Concurrent 2] |
|---------|-------------|----------------|----------------|
| CA | | | |
| Marge EBITDA | | | |
| ROIC | | | |
| P/E | | | |
| EV/EBITDA | | | |
| Croissance CA | | | |
| Parts de marché | | | |
| Moat | | | |
| Pricing power | | | |
```

**Questions clés :**
- Qu'est-ce qui différencie l'entreprise de son secteur ?
- Apporte-t-elle quelque chose en plus ou en moins ?
- Est-elle réellement exposée aux mêmes risques ? Fait-elle quelque chose contre ?
- **Sont-elles TOUTES sous-évaluées ?** Si oui, pourquoi ? (cycle, secteur décoté, anomalie)

### 2F — ANALYSE M&A & PROJETS STRATÉGIQUES

- Rachats récents : quoi, combien, pourquoi, intégration réussie ?
- **Rachats futurs annoncés ou probables** : cibles identifiées, capacité financière
- Projets d'expansion : nouveaux marchés, nouvelles usines, nouveaux produits
- Rationale stratégique : les rachats servent-ils la vision long-terme ?
- Destruction ou création de valeur ?

### 2G — CYCLES MACRO PAR PAYS D'EXPOSITION

```
EXPOSITION MACRO — [entreprise]

| Pays/Zone | % CA | Cycle actuel | Tendance | Risque devise | Impact |
|-----------|------|-------------|----------|---------------|--------|
| [Pays 1]  | X%   | Expansion/Pic/Contraction/Creux | | | |
| [Pays 2]  | X%   | | | | |
```

- Analyser les cycles économiques des pays où l'entreprise fait le plus de CA
- Analyser les pays d'expansion prévue
- Identifier les risques devise, politiques, réglementaires par zone

### 2H — DCF APPROFONDIE

**Modèle DCF complet avec :**
1. **Projections FCF** sur 5-10 ans (justifier chaque hypothèse)
2. **WACC calculé** : coût dette (rating), coût equity (CAPM + prime risque), pondération
3. **Terminal value** : méthode Gordon Growth (quel g ?) + méthode exit multiple
4. **Analyse de sensibilité** : tableau WACC vs croissance terminale
5. **3 scénarios** : Bull / Base / Bear avec FCF différents
6. **Valeur intrinsèque par action** vs cours actuel → marge de sécurité en %

**Si IPO récente** : utiliser le prix d'entrée pour calculer les ratios et la rentabilité.

### 2I — SAISONNALITÉ

- **CA** : y a-t-il des trimestres systématiquement plus forts/faibles ?
- **Bénéfices** : idem
- **Cours boursier** : patterns saisonniers récurrents (sell in May ? Rally fin d'année ?)
- **Impact** : quand est le meilleur moment pour acheter/vendre saisonnièrement ?

### 2J — OWNER'S EARNINGS (Buffett)

```
OWNER'S EARNINGS — [entreprise] — [année]

Résultat net                    : [X] M€
+ Dépréciation & Amortissement : [X] M€
+ Variations BFR                : [X] M€
- Capex de maintenance          : [X] M€
= OWNER'S EARNINGS              : [X] M€

OE par action                   : [X] €
OE yield (OE / market cap)      : [X]%
Tendance OE sur 5 ans           : [↑↗→↘↓]
```

### 2K — SCORING COMPOSITES (Piotroski, Altman, Beneish)

**OBLIGATOIRE pour toute analyse d'action cotée (types A à E). Non applicable aux crypto/obligations/ETF.**

```
SCORING COMPOSITES — [entreprise] ([ticker]) — [année]

PIOTROSKI F-SCORE (0-9) :
| # | Critère                    | Résultat  | Score |
|---|----------------------------|-----------|-------|
| 1 | ROA > 0                    | [oui/non] | [1/0] |
| 2 | CFO > 0                    | [oui/non] | [1/0] |
| 3 | ΔROA > 0 (vs N-1)          | [oui/non] | [1/0] |
| 4 | CFO > Net Income (qualité) | [oui/non] | [1/0] |
| 5 | ΔLeverage < 0 (dette/actif)| [oui/non] | [1/0] |
| 6 | ΔCurrent Ratio > 0         | [oui/non] | [1/0] |
| 7 | ΔShares ≤ 0 (pas dilution) | [oui/non] | [1/0] |
| 8 | ΔGross Margin > 0          | [oui/non] | [1/0] |
| 9 | ΔAsset Turnover > 0        | [oui/non] | [1/0] |
| **TOTAL**                      |           | **[X]/9** |

Interprétation : 8-9 = Fondamentaux solides ✅ | 5-7 = Neutre | 0-4 = Détérioration 🔴
Source : Alpha Vantage INCOME_STATEMENT + BALANCE_SHEET + CASH_FLOW (3 dernières années)
```

```
ALTMAN Z-SCORE (risque faillite) :
Variables :
  X1 = Working Capital / Total Assets        = [X]
  X2 = Retained Earnings / Total Assets      = [X]
  X3 = EBIT / Total Assets                   = [X]
  X4 = Market Value Equity / Total Liabilities = [X]
  X5 = Sales / Total Assets                  = [X]

Z-Score = 1.2×X1 + 1.4×X2 + 3.3×X3 + 0.6×X4 + 1.0×X5 = [X.XX]

Zone : [Safe (>2.99) ✅ | Grey (1.81-2.99) ⚠️ | Distress (<1.81) 🔴]

⚠️ Variantes :
- Manufacturiers : formule originale ci-dessus
- Non-manufacturiers (Z'') : Z'' = 6.56×X1 + 3.26×X2 + 6.72×X3 + 1.05×X4 (seuils : >2.60 safe, <1.10 distress)
- NE PAS appliquer aux banques/assurances (structure bilan incompatible)
Source : BALANCE_SHEET + INCOME_STATEMENT + GLOBAL_QUOTE (market cap)
```

```
BENEISH M-SCORE (détection manipulation comptable) :
Variables (calculées sur 2 années consécutives) :
  DSRI = Days Sales Receivable Index         = [X]   (>1.0 = créances gonflées)
  GMI  = Gross Margin Index                  = [X]   (<1.0 = marge en baisse)
  AQI  = Asset Quality Index                 = [X]   (>1.0 = actifs intangibles en hausse)
  SGI  = Sales Growth Index                  = [X]   (>1.0 = croissance rapide)
  DEPI = Depreciation Index                  = [X]   (>1.0 = amortissement ralenti)
  SGAI = SGA Expense Index                   = [X]   (>1.0 = frais généraux en hausse)
  LVGI = Leverage Index                      = [X]   (>1.0 = endettement en hausse)
  TATA = Total Accruals to Total Assets      = [X]   (>0 = accruals importants)

M-Score = -4.84 + 0.920×DSRI + 0.528×GMI + 0.404×AQI + 0.892×SGI + 0.115×DEPI - 0.172×SGAI + 4.679×TATA - 0.327×LVGI

M-Score = [X.XX] → [Clean (<-1.78) ✅ | Manipulation probable (>-1.78) 🔴]
Taux de détection historique : 76% des manipulations détectées (Beneish 1999)
Source : INCOME_STATEMENT + BALANCE_SHEET (2 années consécutives minimum)
```

**Intégration dans le scoring /10 des 15 dimensions :**
| Résultat | Impact sur dimensions |
|----------|---------------------|
| Piotroski 8-9 | **+0.5** à Dimension 3 (Solidité) ET Dimension 11 (Cash-Flow) |
| Piotroski 0-4 | **-1.0** à Dimension 3 ET Dimension 11 |
| Altman Z < 1.81 | Dimension 3 (Solidité) **plafonnée à 4/10 maximum** |
| Altman Z < 1.10 (non-manuf.) | Dimension 3 **plafonnée à 2/10** + alerte rouge dans synthèse |
| Beneish M > -1.78 | Dimension 4 (Gouvernance) **plafonnée à 3/10** + 🔴 alerte manipulation |
| Les 3 scores positifs simultanément | **+0.5** bonus à la note globale finale |

### 2L — MOMENTUM FONDAMENTAL

**Applicable si couverture analyste ≥ 3 analystes. Si couverture < 3, noter "N/A — couverture insuffisante".**

```
MOMENTUM FONDAMENTAL — [entreprise] ([ticker])

EARNINGS REVISION MOMENTUM :
| Période | Nb analystes | Révisions ↑ | Révisions ↓ | Net (↑-↓) | Magnitude moy. |
|---------|-------------|------------|------------|-----------|----------------|
| 1 mois  | [X]         | [X]        | [X]        | [+/-X]    | [+/-X]%        |
| 3 mois  | [X]         | [X]        | [X]        | [+/-X]    | [+/-X]%        |

Signal : Net positif 1m ET 3m = momentum haussier ✅ | Net négatif = momentum baissier 🔴

EARNINGS SURPRISE (8 derniers trimestres) :
| Trimestre | EPS attendu | EPS réel | Surprise % | Réaction cours J+1 |
|-----------|------------|---------|-----------|-------------------|
| Q[X] [Y]  | [X]        | [X]     | [+/-X]%   | [+/-X]%           |
| ...        |            |         |           |                   |

Beat rate : [X]/8 trimestres ([Y]%)
Surprise moyenne : [+/-X]%
Signal : Beat rate > 75% = récurrence positive ✅ | < 50% = société qui déçoit ⚠️

ESTIMATE DISPERSION :
Écart-type estimations EPS FY  : [X]
Moyenne estimations EPS FY     : [X]
Dispersion ratio               : [X]% (= écart-type / moyenne × 100)
Signal : < 5% = consensus fort ✅ | 5-15% = incertitude moyenne | > 15% = forte incertitude ⚠️

SUE SCORE (Standardized Unexpected Earnings — dernier trimestre) :
Formule : SUE = (EPS actual - EPS consensus) / écart-type des surprises passées (4-8 trim.)
SUE = [X]
Signal : SUE > 2.0 = surprise positive forte ✅ | SUE < -2.0 = surprise négative forte 🔴
```

**Sources données :**
- Alpha Vantage `EARNINGS` (historical quarterly EPS + surprise)
- WebSearch "[ticker] earnings estimates revisions consensus" → TipRanks, MarketScreener, Seeking Alpha
- WebSearch "[ticker] analyst estimates dispersion" → FactSet, Bloomberg consensus

**Intégration dans le scoring /10 :**
| Résultat | Impact sur dimensions |
|----------|---------------------|
| Revision momentum net positif (1m+3m) + SUE > 1.0 | **+0.5** à Dimension 5 (Croissance) |
| Revision momentum net négatif (1m+3m) + SUE < -1.0 | **-0.5** à Dimension 5 (Croissance) |
| Dispersion > 15% | **-0.5** à Dimension 6 (Visibilité) |
| Beat rate > 75% sur 8 trimestres | **+0.3** à Dimension 4 (Gouvernance — management crédible) |
| Beat rate < 50% sur 8 trimestres | **-0.3** à Dimension 4 |

---

## ÉTAPE 3 — PONDÉRATION OPTIMALE DES NOTES

**Le coefficient de chaque dimension dépend du profil de l'utilisateur :**
L'utilisateur apprécie autant :
- Une entreprise défensive avec potentiel de croissance élevé
- Une entreprise non défensive avec potentiel de croissance bien plus élevé
- Une entreprise à fort dividende avec potentiel de croissance (ex: Murapol)

**Pondération par type d'actif :**

| Dimension | Growth | Small-cap | Cyclique | Défensif | REIT |
|-----------|--------|-----------|----------|----------|------|
| 1. Moat | x1.5 | x1.0 | x1.0 | x1.5 | x1.0 |
| 2. Parts de marché | x1.5 | x1.0 | x1.0 | x1.0 | x0.5 |
| 3. Solidité financière | x1.0 | x2.0 | x1.5 | x1.0 | x1.5 |
| 4. Gouvernance | x1.0 | x1.5 | x1.0 | x1.0 | x1.0 |
| 5. Croissance | x2.0 | x1.5 | x1.0 | x1.0 | x1.0 |
| 6. Visibilité | x1.0 | x1.5 | x1.5 | x1.5 | x1.5 |
| 7. Alignement | x1.0 | x2.0 | x1.0 | x1.0 | x1.0 |
| 8. Ratio potentiel/risque | x1.5 | x1.5 | x1.5 | x1.0 | x1.0 |
| 9. Timing technique | x0.5 | x1.0 | x1.5 | x0.5 | x0.5 |
| 10. Valorisation | x1.5 | x1.5 | x1.5 | x1.0 | x1.5 |
| 11. Cash-flow | x1.5 | x1.5 | x1.0 | x1.5 | x1.5 |
| 12. Allocation capital | x1.0 | x1.0 | x1.0 | x1.0 | x1.0 |
| 13. ROIC/ROCE | x1.5 | x1.0 | x1.0 | x1.0 | x0.5 |
| 14. Dilution | x0.5 | x2.0 | x0.5 | x0.5 | x1.0 |
| 15. Optionnalité | x1.5 | x1.5 | x1.0 | x0.5 | x0.5 |

**Calcul note globale** : Σ (note_i × coeff_i) / Σ (coeff_i)

---

## ÉTAPE 4 — SYNTHÈSE OBLIGATOIRE

```
## SYNTHÈSE — [NOM] ([TICKER]) — [TYPE D'ACTIF]

### Tableau récapitulatif
| # | Dimension | Note /10 | Coeff | Pondéré |
|---|-----------|----------|-------|---------|
| 1 | Moat & avantages concurrentiels | X/10 | xY | Z |
| ... | ... | ... | ... | ... |
| 15 | Optionnalité | X/10 | xY | Z |
| **NOTE GLOBALE PONDÉRÉE** | | | | **X.X/10** |

### Forces principales (top 3)
1. [Force + justification]
2. [Force + justification]
3. [Force + justification]

### Faiblesses principales (top 3)
1. [Faiblesse + justification]
2. [Faiblesse + justification]
3. [Faiblesse + justification]

### Valeur intrinsèque
- DCF Base Case : [X] € / action (marge sécurité : [Y]%)
- DCF Bull Case : [X] € / action
- DCF Bear Case : [X] € / action
- Owner's Earnings yield : [X]%
- Comparaison vs concurrents : [sous/sur-évalué de X%]

### Thèse d'investissement
- **Bull Case** (proba X%) : [scénario + objectif cours + horizon]
- **Base Case** (proba X%) : [scénario + objectif cours + horizon]
- **Bear Case** (proba X%) : [scénario + objectif cours + horizon]

### Recommandation finale
[ACHETER / ACCUMULER / CONSERVER / ALLÉGER / VENDRE]
Horizon : [court/moyen/long terme]
Niveau d'entrée idéal : [prix]
Stop-loss suggéré : [prix]
Conviction : [Élevée / Moyenne / Faible]
```

---

## ÉTAPE 5 — EXPORT EXCEL

Après chaque analyse, **ajouter l'entreprise au fichier Excel de suivi** :

```python
# Colonnes du fichier Excel :
# Ticker | Nom | Type (ex: "Défensif Santé", "Cyclique Énergie", "Growth Tech") |
# Note globale /10 | Cours actuel | DCF Base | Marge sécurité % |
# Recommandation | Date analyse | Forces clés | Risques clés
```

**Chemin du fichier :** `C:\Users\Alexandre collenne\Documents\analyse_actions.xlsx`
Si le fichier n'existe pas → le créer.
Si il existe → ajouter une ligne.

---

## TABLEAU RÉCAP MÉTRIQUES PAR TYPE

| Type | Métrique N°1 | Métrique N°2 | Métrique N°3 | Valorisation | Piège à éviter | Indicateurs avancés obligatoires |
|------|-------------|-------------|-------------|-------------|----------------|-------------------------------|
| Mega/Large Growth | ROIC | FCF yield | PEG | DCF + comps | P/E seul | DuPont 5-Factor, Magic Formula, CROCI, Earnings Revisions |
| Micro/Small-cap | Liquidité | Cash burn | Insider % | EV/EBITDA + NAV | Dilution/faillite | Altman Z-Score, Piotroski F-Score, Shareholder Yield |
| Cyclique | EBITDA normalisé | Backlog | Bilan | EV/EBITDA cycle | P/E bas = piège haut cycle | Altman Z-Score, CCC, Earnings Surprise, Beneish M-Score |
| Défensif/Dividend | Div. yield | Payout ratio | CAGR div. | DDM + P/E hist. | Rendement élevé = coupe | Shareholder Yield, Piotroski, DuPont (levier vs marge) |
| Immobilier/REIT | FFO/AFFO | NAV | Occupation | Price/AFFO + NAV | P/E classique | CCC, Altman Z (adapté Z''), Piotroski |
| Crypto | AT | On-chain | Sentiment | Pas de DCF | Métriques actions | N/A (pas de fondamentaux classiques) |
| Obligation | YTM | Duration | Rating | Spread analysis | Risque taux | Altman Z-Score de l'émetteur |
| ETF | TER | Tracking error | Sharpe | vs Benchmark | Frais cachés | N/A (analyse au niveau du fonds) |

## ANTI-PATTERNS — CE QU'IL NE FAUT JAMAIS FAIRE

| Excuse | Réalité |
|--------|---------|
| "C'est une action, je fais une analyse standard" | TOUJOURS classifier d'abord (Growth, Micro-cap, Cyclique, etc.). Chaque type a ses métriques. |
| "Le PER suffit pour valoriser" | Un seul ratio est INSUFFISANT. Minimum 3 méthodes de valorisation croisées. |
| "Pas de données récentes, j'utilise mes connaissances" | JAMAIS. Toujours sourcer avec des données fraîches (Alpha Vantage, FMP, WebSearch). |
| "L'analyse technique n'est pas nécessaire" | Fondamentaux + technique = vision complète. Toujours les deux. |
| "Bull/Bear/Base c'est optionnel" | Les 3 scénarios sont OBLIGATOIRES pour toute synthèse. |

## RED FLAGS — STOP

- Analyse sans classification de l'actif → STOP
- Moins de 3 sources de données → STOP
- Valorisation avec un seul ratio → STOP
- Pas de scénario bull/base/bear → STOP

## CROSS-LINKS

| Contexte | Skill à invoquer |
|----------|-----------------|
| Avant analyse | `deep-research` (collecte données multi-sources) |
| Modélisation DCF/LBO | `financial-modeling` |
| Données macro | `macro-analysis` |
| Validation qualité | `qa-pipeline` |
| Export PDF | `pdf-report-gen` |
| Feedback utilisateur | `feedback-loop` |
| RETEX | `retex-evolution` |

## ÉVOLUTION

Ce skill s'auto-améliore. Après chaque utilisation :
- Si la classification d'actif était incorrecte → ajuster les critères de classification
- Si une métrique manquait → l'ajouter dans la matrice du type concerné
- Si l'analyse était incomplète → identifier la dimension manquante

Seuils d'action :
- Score QA < 7/10 → revoir les dimensions d'analyse
- Sources < 5 → enrichir la matrice de sources par type d'actif

## LIVRABLE FINAL

- **Type** : PDF
- **Généré par** : pdf-report-pro
- **Destination** : acollenne@gmail.com via send_report.py

## CHAÎNAGE ARBORESCENCE

- **Amont** : deep-research (entrée unique)
- **Aval** : pdf-report-pro

