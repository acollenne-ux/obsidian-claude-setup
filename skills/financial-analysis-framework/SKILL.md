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

| Type | Métrique N°1 | Métrique N°2 | Métrique N°3 | Valorisation | Piège à éviter |
|------|-------------|-------------|-------------|-------------|----------------|
| Mega/Large Growth | ROIC | FCF yield | PEG | DCF + comps | P/E seul |
| Micro/Small-cap | Liquidité | Cash burn | Insider % | EV/EBITDA + NAV | Dilution/faillite |
| Cyclique | EBITDA normalisé | Backlog | Bilan | EV/EBITDA cycle | P/E bas = piège haut cycle |
| Défensif/Dividend | Div. yield | Payout ratio | CAGR div. | DDM + P/E hist. | Rendement élevé = coupe |
| Immobilier/REIT | FFO/AFFO | NAV | Occupation | Price/AFFO + NAV | P/E classique |
| Crypto | AT | On-chain | Sentiment | Pas de DCF | Métriques actions |
| Obligation | YTM | Duration | Rating | Spread analysis | Risque taux |
| ETF | TER | Tracking error | Sharpe | vs Benchmark | Frais cachés |

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
