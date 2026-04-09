---
name: stock-analysis
description: "Analyse boursière complète d'une action, portefeuille ou IPO. Use when: analyzing stocks, trading, company valuation, IPO, sector analysis. Triggers: 'action', 'trading', 'valorisation', 'IPO', 'bourse', 'ticker'."
argument-hint: "TICKER ou nom d'entreprise, timeframe optionnel"
allowed-tools: WebSearch, WebFetch, Bash
---

## RÈGLE UNIVERSELLE — LIRE L'INTÉGRALITÉ DU SKILL AVANT D'AGIR

**OBLIGATOIRE : Avant d'exécuter quoi que ce soit, tu DOIS :**
1. Lire l'INTÉGRALITÉ de ce fichier SKILL.md (pas juste le début)
2. Comprendre chaque section, chaque règle, chaque contrainte
3. Respecter ce skill À LA LETTRE — ne rien sauter, ne rien simplifier

**Ne JAMAIS commencer l'exécution sans avoir lu et compris TOUT le skill.**

---

# Skill : Analyse Boursière Approfondie

## CHECKLIST OBLIGATOIRE

Créer une tâche TodoWrite pour chaque étape :

1. **Classifier l'actif** — Identifier le type (Growth, Micro-cap, Cyclique, Défensif, REIT, Crypto, Obligation, ETF)
2. **Collecter les données** — Alpha Vantage + FMP + WebSearch (min 5 sources)
3. **Analyse fondamentale** — Métriques adaptées au type d'actif
4. **Analyse technique** — Price action, supports/résistances, tendance
5. **Valorisation** — Minimum 3 méthodes croisées
6. **Scénarios Bull/Base/Bear** — Avec probabilités et catalyseurs
7. **Synthèse et recommandation** — Score pondéré + verdict

## Déclencheurs automatiques
- Mention de ticker (ex: AAPL, TSLA, NVDA, CAC40)
- Questions sur prix, PE ratio, valorisation, cours
- Demandes d'analyse sectorielle
- Comparaison d'actions
- Mention d'IPO, introduction en bourse, cotation, S-1, prospectus

## ÉTAPE 0 — CLASSIFICATION DE L'ACTIF (AVANT toute analyse)

**OBLIGATOIRE :** Identifier le type d'actif et adapter le framework. Voir la section 1D du skill `deep-research` pour la classification complète.

```
Type détecté : [Growth | Value | Cyclique | Défensif | Dividend | REIT/Immobilier | Crypto | Obligation | ETF | **IPO/Pré-IPO**]
Cap           : [Mega >200B | Large 10-200B | Mid 2-10B | Small 250M-2B | Micro <250M]
Secteur GICS  : [Tech | Santé | Finance | Immobilier | Énergie | Matériaux | Conso | Industrie | Utilities | Comm]
Framework     : [A=Growth | B=Micro/Small | C=Cyclique | D=Défensif | E=REIT | F=Crypto | G=Obligation | H=ETF | **I=IPO**]
```

**Adaptations par type :**
- **Micro/Small-cap** : prioriser liquidité, dilution, insider %, cash burn, survie
- **Cyclique** : P/E normalisé sur le cycle, ⚠️ P/E bas ≠ sous-évalué (piège haut de cycle)
- **REIT/Immobilier** : utiliser FFO/AFFO (pas P/E), NAV, taux d'occupation
- **Crypto** : analyse technique + on-chain + sentiment (pas de fondamentaux classiques)
- **Défensif/Dividend** : DDM, payout ratio, historique dividende, performance en récession
- **Growth** : PEG, ROIC, TAM, Rule of 40, FCF yield
- **IPO** : prospectus/S-1, lock-up, underwriters, dilution, use of proceeds, 3 phases techniques → **VOIR SECTION IPO COMPLÈTE CI-DESSOUS**

## Cadre d'analyse à suivre

### 1. Données de marché (utiliser MCP LunarCrush/Crypto.com si crypto, WebSearch sinon)
- Prix actuel, variation 1j/1s/1m/1an
- Volume, capitalisation boursière
- RSI, MACD, moyennes mobiles (50j, 200j)
- Support/résistance clés
- **Si micro/small-cap** : bid-ask spread, volume moyen, flottant
- **Si IPO** : prix d'introduction vs prix actuel, performance J+1/S+1/M+1, volume relatif vs moyenne

### 2. Fondamentaux (adapter selon le type)
- Revenus, croissance (YoY, QoQ)
- Marges (brute, opérationnelle, nette)
- Free cash flow, dette nette/EBITDA
- Return on Equity, Return on Capital
- **Si cyclique** : marges normalisées sur 7-10 ans, backlog/carnet commandes
- **Si REIT** : FFO, AFFO, NOI, taux d'occupation, WALT
- **Si micro-cap** : cash burn rate, concentration clients, insider ownership
- **Si IPO** : analyser le prospectus/S-1 (voir section IPO)

### 3. Valorisation (adapter selon le type)
- **Growth** : PEG ratio, Forward P/E, DCF, Price/FCF
- **Cyclique** : EV/EBITDA normalisé, Price/Book, ⚠️ pas P/E seul
- **REIT** : Price/AFFO, NAV premium/discount, cap rate
- **Défensif** : DDM (Dividend Discount Model), P/E historique, yield relatif
- **Micro-cap** : EV/EBITDA + NAV + DCF prudent (WACC + prime 3-5%)
- **Crypto** : market cap relative, analyse technique pure
- **IPO** : comparables sectoriels P/S et EV/Revenue, DCF si cash-flow positif, prime/décote vs pairs cotés

### 4. Analyse qualitative
- Avantage concurrentiel (moat)
- Positionnement marché, parts de marché
- Management : track record, allocation capital
- Catalyseurs court terme (earnings, produits, régulation)
- **Si micro-cap** : qualité governance, risque homme-clé, alignement intérêts
- **Si IPO** : qualité des underwriters, historique du management pré-IPO, utilisation des fonds levés

### 5. Risques (adapter selon le type)
- Risques financiers (levier, liquidité)
- Risques opérationnels / compétitifs
- Risques macro (taux, devises, géopolitique)
- Risques réglementaires
- **Si micro-cap** : risque dilution, illiquidité, faillite, couverture analyste nulle
- **Si cyclique** : position dans le cycle, surcapacité, sensibilité PIB
- **Si REIT** : taux d'intérêt, vacance, refinancement, cycle immobilier
- **Si crypto** : volatilité extrême, régulation, hacks, rug pulls
- **Si IPO** : lock-up expiry, dilution post-IPO, insider selling, surévaluation initiale, manque d'historique

### 6. Conclusion & Thèse d'investissement
- Bull case / Base case / Bear case
- Prix cibles indicatifs (méthode adaptée au type)
- Conviction et horizon temporel recommandé
- **Score par dimension adapté au type** (pas les mêmes 15 dimensions pour tous)
- **Si IPO** : recommandation spécifique (souscrire / attendre lock-up / attendre base technique)

## Format de sortie
Utiliser des tableaux pour les données comparatives.
Toujours citer les sources et dater les données.
Distinguer FAITS (données) et INTERPRÉTATION (analyse).
Ajouter disclaimer : "Ceci n'est pas un conseil en investissement."

---

## 5B. INDICATEURS AVANCÉS (OBLIGATOIRE — calculer pour TOUTE action cotée)

**Ces indicateurs complètent l'analyse fondamentale classique. Ils sont OBLIGATOIRES pour les types A à E (Growth, Micro-cap, Cyclique, Défensif, REIT). Non applicables aux crypto/obligations/ETF.**

### A. Scores Composites (3 checks obligatoires)

**1. Piotroski F-Score (0-9) — Qualité fondamentale**

| # | Signal | Critère | Source Alpha Vantage |
|---|--------|---------|---------------------|
| 1 | Profitabilité | ROA > 0 (Net Income / Total Assets) | INCOME_STATEMENT + BALANCE_SHEET |
| 2 | Cash-flow | CFO > 0 | CASH_FLOW |
| 3 | Tendance ROA | ΔROA > 0 vs année N-1 | Calcul sur 2 ans |
| 4 | Qualité bénéfice | CFO > Net Income (cash > accruals) | CASH_FLOW vs INCOME_STATEMENT |
| 5 | Désendettement | ΔDette LT/Actifs en baisse YoY | BALANCE_SHEET |
| 6 | Liquidité | ΔCurrent ratio en hausse YoY | BALANCE_SHEET |
| 7 | Pas de dilution | Pas d'émission nette d'actions YoY | BALANCE_SHEET |
| 8 | Marge brute | ΔGross margin en hausse YoY | INCOME_STATEMENT |
| 9 | Efficience | ΔAsset turnover (CA/Actifs) en hausse YoY | INCOME_STATEMENT + BALANCE_SHEET |

**Interprétation :** 8-9 = Fondamentaux solides ✅ (Strong Buy signal) | 5-7 = Neutre | 0-4 = Détérioration 🔴

**2. Altman Z-Score — Risque de faillite**

Z = 1.2×(Working Capital/Total Assets) + 1.4×(Retained Earnings/TA) + 3.3×(EBIT/TA) + 0.6×(Market Cap/Total Liabilities) + 1.0×(Sales/TA)

| Zone | Z-Score | Signal |
|------|---------|--------|
| Safe | > 2.99 | ✅ Risque faillite très faible |
| Grey | 1.81 — 2.99 | ⚠️ Zone d'incertitude |
| Distress | < 1.81 | 🔴 Probabilité faillite élevée |

⚠️ **Non-manufacturiers** (Z'') : Z'' = 6.56×X1 + 3.26×X2 + 6.72×X3 + 1.05×X4 (seuils : >2.60 safe, <1.10 distress)
⚠️ **Ne PAS appliquer aux banques/assurances** (structure bilan incompatible)

**3. Beneish M-Score — Détection manipulation comptable**

8 variables (DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA) calculées sur 2 années consécutives.
M-Score = -4.84 + 0.920×DSRI + 0.528×GMI + 0.404×AQI + 0.892×SGI + 0.115×DEPI - 0.172×SGAI + 4.679×TATA - 0.327×LVGI

| M-Score | Signal |
|---------|--------|
| < -1.78 | ✅ Pas de signal de manipulation |
| > -1.78 | 🔴 Manipulation probable (76% détection historique) |

**Livrable obligatoire :**
```
INDICATEURS AVANCÉS — [TICKER]
Piotroski F-Score : [X]/9  → [Solide/Neutre/Détérioration]
Altman Z-Score    : [X.XX] → [Safe/Grey/Distress]
Beneish M-Score   : [X.XX] → [Clean/Manipulation probable]
```

### B. Métriques Qualité & Efficience

- **DuPont 5-Factor Decomposition** : ROE = Tax Burden × Interest Burden × EBIT Margin × Asset Turnover × Equity Multiplier
  → Identifier si le ROE est porté par la marge (sain ✅) ou par le levier financier (risqué ⚠️ si Equity Multiplier > 3x)
- **Earnings Quality Score** : Accruals Ratio = (Net Income - OCF) / Total Assets
  → Plus proche de 0 = meilleure qualité | > 10% = ⚠️ bénéfices "papier"
- **Sloan Accruals Ratio** : (ΔCA - ΔCash - ΔCL + ΔSTD + ΔTP - D&A) / Avg Total Assets
  → > 10% = ⚠️ qualité douteuse | < 5% = ✅ bonne qualité
- **Cash Conversion Cycle (CCC)** : DSO + DIO - DPO (en jours)
  → Tendance YoY : en baisse = ✅ amélioration | en hausse > 15j = ⚠️ dégradation BFR
- **Shareholder Yield** : Dividend yield + Buyback yield + Debt paydown yield
  → Mesure complète du retour actionnarial vs dividende seul

### C. Scores de Classement

- **Magic Formula (Greenblatt)** : Classement par Earnings Yield (EBIT/EV) + classement par ROIC → rang combiné. Plus le rang est bas = "cheap + quality"
- **CROCI (Cash Return on Capital Invested)** : Gross Cash Flow / Gross Invested Capital → > 15% excellent ✅ | < 8% faible ⚠️

### D. Momentum Fondamental (si couverture analyste ≥ 3)

- **Earnings Revision Momentum** : % analystes en révision haussière vs baissière (1m/3m). Net positif = momentum ✅
- **Earnings Surprise Factor** : Beat rate sur 8 trimestres. > 75% = récurrence ✅ | < 50% = déception ⚠️
- **Estimate Dispersion** : écart-type estimations / moyenne. < 5% = consensus fort ✅ | > 15% = forte incertitude ⚠️
- **SUE Score** : (EPS actual - EPS consensus) / écart-type surprises passées. > 2.0 = forte surprise positive | < -2.0 = forte surprise négative

Source : Alpha Vantage `EARNINGS` + WebSearch "[ticker] earnings estimates revisions consensus"

### E. Indicateurs Sectoriels Avancés (selon classification Étape 0)

**Si SaaS/Tech :** Rule of 40, NDR/NRR (>120% ✅, <100% ⚠️), CAC Payback (<12m ✅), LTV/CAC (>3x ✅), Magic Number (>0.75 ✅)
**Si Banque/Finance :** CET1 (>12% ✅), NIM (>3% ✅), NPL ratio (<1% ✅), Cost-to-Income (<50% ✅), LCR, PPNR
**Si Biotech/Pharma :** Pipeline NPV prob-weighted (Phase I:10%, II:25%, III:55%), patent cliff %, R&D productivity
**Si Mining/Oil :** Reserve Life (>15 ans ✅), AISC (quartile inf. ✅), netback, reserve replacement ratio (>100% ✅)
**Si Retail :** Same-store sales (>3% ✅), sales/sqft, inventory turnover, e-commerce mix
**Si Insurance :** Combined ratio (<95% ✅), investment yield, book value CAGR (>8% ✅), P/Embedded Value (<1.0x ✅)

---

### RED FLAGS — INDICATEURS AVANCÉS (applicable à TOUTE action)

| Indicateur | Seuil d'alerte | Action requise |
|-----------|---------------|---------------|
| Piotroski F-Score | ≤ 3 | 🔴 Détérioration fondamentale — réduire conviction d'un cran |
| Altman Z-Score | < 1.81 | 🔴 Risque faillite — ne pas acheter / envisager sortie |
| Beneish M-Score | > -1.78 | 🔴 Manipulation probable — investigation approfondie requise |
| Accruals Ratio | > 10% | ⚠️ Qualité bénéfices douteuse — vérifier divergence cash/earnings |
| CCC en hausse | > +15 jours YoY | ⚠️ Dégradation BFR — analyser DSO/DIO/DPO individuellement |
| Estimate Dispersion | > 15% | ⚠️ Forte incertitude — réduire taille position recommandée |
| Shareholder Yield | < 0% (négatif) | ⚠️ Destruction de valeur pour l'actionnaire |
| DuPont Equity Multiplier | > 3x et en hausse | ⚠️ ROE artificiellement gonflé par le levier |
| Earnings Beat Rate | < 50% sur 8 trim. | ⚠️ Management non crédible — réduire conviction |

**Règle :** Si **3+ red flags avancés** sont déclenchés simultanément → **downgrade automatique** de la recommandation d'un cran (ex: ACHETER → ACCUMULER, CONSERVER → ALLÉGER).

---

## TYPE I — ANALYSE D'IPO (Introduction en Bourse)

**Ce framework s'applique à TOUTE entreprise en cours d'IPO, récemment introduite (< 12 mois), ou en phase pré-IPO.**

⚠️ **PARTICULARITÉS CRITIQUES D'UNE IPO :**
- Pas ou peu d'historique boursier → l'analyse technique classique est limitée
- Asymétrie d'information massive → les insiders savent plus que le marché
- Surévaluation fréquente → 46% seulement des IPOs US ont un return positif au J+1 (Q1 2025)
- Lock-up expiry → pression vendeuse prévisible à 90-180 jours
- Hype médiatique → le bruit > le signal dans les premières semaines
- Absence de couverture analyste → peu ou pas de consensus au départ

---

### IPO-1 — ANALYSE DU PROSPECTUS / S-1 (FONDATION DE TOUTE ANALYSE IPO)

Le prospectus (S-1 aux USA, Document d'Enregistrement en Europe) est LA source primaire. **Ne jamais analyser une IPO sans avoir lu le prospectus.**

**Recherche obligatoire :**
```
WebSearch : "[entreprise] IPO prospectus S-1 filing SEC"
WebSearch : "[entreprise] IPO document enregistrement AMF" (si Europe)
WebFetch  : [URL du prospectus si trouvée — SEC EDGAR, AMF, Euronext]
```

**Éléments à extraire du prospectus :**

```
FICHE PROSPECTUS IPO — [Entreprise]

1. BUSINESS MODEL
   - Description précise de l'activité
   - Modèle de revenus : récurrent (SaaS/abo) vs one-shot vs transactionnel
   - Marchés adressés (TAM/SAM/SOM avec sources du prospectus)
   - Avantage concurrentiel revendiqué par le management
   - Clients clés et concentration (top 5 clients = quel % du CA)

2. FINANCIERS (3-5 derniers exercices si disponibles)
   - CA, croissance YoY
   - Marges brute, EBITDA, nette
   - Cash-flow opérationnel et FCF
   - Trésorerie nette / dette nette
   - Burn rate si non-rentable (mois de runway restants)

3. UTILISATION DES FONDS (USE OF PROCEEDS)
   ⚠️ SIGNAL CRITIQUE — catégoriser l'utilisation :
   - ✅ Croissance : R&D, expansion géo, nouveaux produits → POSITIF
   - ✅ Désendettement ciblé : réduction de dette coûteuse → NEUTRE/POSITIF
   - ⚠️ Fonds de roulement général (working capital) → VAGUE, demander plus de détails
   - 🔴 Racheter les parts d'investisseurs existants → RED FLAG (pas de création de valeur)
   - 🔴 "General corporate purposes" sans détail → RED FLAG (manque de vision)
```

```
4. FACTEURS DE RISQUE (section Risk Factors)
   - Lire INTÉGRALEMENT cette section — les entreprises sont légalement obligées de lister les vrais risques
   - Classer par gravité : existentiel / majeur / modéré / mineur
   - Identifier les risques spécifiques vs génériques (les génériques sont du boilerplate légal)
   - Signaux d'alerte : litiges en cours, dépendance réglementaire, concentration client extrême

5. STRUCTURE ACTIONNARIALE PRÉ/POST-IPO
   - Qui détient quoi AVANT l'IPO (fondateurs, VC, PE, employés)
   - Dilution : combien de nouvelles actions émises vs vente d'actions existantes
   - % du capital en flottant (free float) après IPO
   - Actions à droits de vote multiples (dual-class shares) → quel contrôle garde le fondateur ?
   - ESOP/stock options en circulation (dilution future potentielle)

6. TRANSACTIONS LIÉES (Related Party Transactions)
   - Contrats entre l'entreprise et ses dirigeants/actionnaires
   - Si significatifs → RED FLAG potentiel (conflits d'intérêt)
```

---

### IPO-2 — QUALITÉ DES UNDERWRITERS (Banques Introductrices)

**La réputation de l'underwriter est un signal de qualité fort.** Les banques Tier 1 ne risquent pas leur réputation sur des entreprises faibles.

**Classification des underwriters :**

| Tier | Banques | Signal | Historique moyen |
|------|---------|--------|-----------------|
| **Tier 1 (Bulge Bracket)** | Goldman Sachs, Morgan Stanley, JPMorgan, BofA | Fort signal de qualité | Meilleure performance post-IPO moyenne |
| **Tier 2 (Major)** | Citi, Barclays, Deutsche Bank, UBS, Credit Suisse | Bon signal | Performance correcte |
| **Tier 3 (Mid-Market)** | Jefferies, Piper Sandler, William Blair, Stifel | Signal neutre | Variable selon le secteur |
| **Tier 4 (Boutique/Inconnu)** | Petites banques régionales ou inconnues | ⚠️ Signal faible | Performance souvent décevante |

**Éléments à vérifier sur l'underwriter :**
- Nombre de co-leads / bookrunners (plus il y en a de Tier 1, mieux c'est)
- Track record récent : performances des 5 dernières IPOs du même underwriter
- Présence d'une option greenshoe / overallotment (stabilisation post-IPO)
- Taille du syndicat de placement

**Option Greenshoe (Overallotment) — mécanisme de stabilisation :**
- Permet aux underwriters de vendre jusqu'à 15% d'actions supplémentaires
- Si le cours baisse sous le prix d'IPO → les underwriters rachètent pour stabiliser
- Si le cours monte → ils exercent l'option et vendent les 15% supplémentaires
- **Présence d'un greenshoe = signal positif** (l'underwriter s'engage à défendre le cours)
- Absence de greenshoe = ⚠️ moins de filet de sécurité

---

### IPO-3 — VALORISATION DE L'IPO (LA QUESTION CENTRALE)

**Règle d'or : une bonne entreprise à un mauvais prix reste un mauvais investissement.**

**Méthodes de valorisation adaptées aux IPOs :**

| Méthode | Quand l'utiliser | Précaution |
|---------|-----------------|------------|
| **P/S (Price-to-Sales)** | IPO non-rentable, forte croissance | Comparer au P/S des pairs cotés au MÊME stade de maturité |
| **EV/Revenue** | SaaS, tech, forte croissance | Ajuster pour la croissance (EV/Revenue / growth rate) |
| **P/E Forward** | IPO rentable | Utiliser les projections du prospectus avec décote de prudence -20% |
| **EV/EBITDA** | IPO rentable, industriel | Comparer aux pairs du même secteur |
| **DCF** | Cash-flows prévisibles | ⚠️ Très sensible aux hypothèses — faire 3 scénarios |
| **Comparables privés** | Pré-IPO | Décote d'illiquidité de 20-30% sur les valorisations des derniers tours VC |
| **Règle du pouce** | Validation rapide | EV/Revenue < 10x pour SaaS croissance >40%, EV/Revenue < 5x pour croissance <20% |

**Grille de valorisation IPO obligatoire :**

```
VALORISATION IPO — [Entreprise]

Prix d'introduction          : [X] EUR/USD par action
Capitalisation à l'IPO       : [X] M/B
EV à l'IPO                   : [X] M/B (capi + dette - tréso)

Multiples à l'IPO :
  P/S (TTM)                  : [X]x → vs pairs : [Y]x (prime/décote de [Z]%)
  EV/Revenue (TTM)           : [X]x → vs pairs : [Y]x
  P/E Forward (si rentable)  : [X]x → vs pairs : [Y]x
  EV/EBITDA (si rentable)    : [X]x → vs pairs : [Y]x

Comparables cotés (3-5 pairs) :
| Pair | P/S | EV/Rev | P/E Fwd | Croissance CA | Marge |
|------|-----|--------|---------|---------------|-------|
| [A]  | Xx  | Xx     | Xx      | +X%           | X%    |
| [B]  | Xx  | Xx     | Xx      | +X%           | X%    |
| [C]  | Xx  | Xx     | Xx      | +X%           | X%    |

Fair value estimée :
  Scénario bull  : [X] EUR/USD (méthode : [comps optimistes / DCF agressif])
  Scénario base  : [X] EUR/USD (méthode : [comps médians])
  Scénario bear  : [X] EUR/USD (méthode : [DCF prudent / décote])

Prime/décote vs prix d'IPO : [+X% surévalué / -X% sous-évalué]
```

**⚠️ PIÈGE FRÉQUENT — IPOs surévaluées :**
- 54% des IPOs US ont un return NÉGATIF au J+1 (Q1 2025)
- Les IPOs sont souvent pricées au sommet du cycle de hype
- Biais de l'underwriter : il est rémunéré sur le montant levé → incentive à surévaluer
- Biais médiatique : couverture massive = pas un signal de qualité
- **TOUJOURS appliquer une marge de sécurité de 15-25% sur la fair value**

---

### IPO-4 — LOCK-UP PERIOD : LE RISQUE CACHÉ N°1

**Le lock-up est la période pendant laquelle les insiders (fondateurs, VC, employés) ne peuvent pas vendre leurs actions.** Son expiration est l'un des événements les plus prévisibles et impactants sur le cours.

**Données à collecter (WebSearch obligatoire) :**
```
WebSearch : "[entreprise] IPO lock-up expiration date"
WebSearch : "[entreprise] IPO insider selling lock-up"
```

**Fiche Lock-Up :**
```
LOCK-UP — [Entreprise]

Date d'IPO                    : [date]
Durée du lock-up              : [90 / 120 / 180 / 365 jours]
Date d'expiration lock-up     : [date calculée]
Jours restants avant expiry   : [X jours]

Actions bloquées (locked)     : [X] M actions ([Y]% du total)
Actions en flottant (float)   : [X] M actions ([Y]% du total)
Ratio locked/float            : [X]x → si >3x = ⚠️ pression vendeuse massive potentielle

Insiders clés soumis au lock-up :
| Insider | Rôle | Actions bloquées | % du capital | Historique de vente |
|---------|------|-----------------|-------------|-------------------|
| [Nom]   | CEO  | [X]M            | [Y]%        | [jamais vendu / a vendu à la 1ère opportunité] |
| [Nom]   | VC   | [X]M            | [Y]%        | [idem] |

Clauses spéciales :
- Early release possible ? [oui/non — conditions]
- Lock-up échelonné (staggered) ? [oui/non — dates]
- Extension possible ? [oui/non — conditions]
```

**Impact statistique du lock-up expiry :**
- En moyenne, les actions baissent de **1-3%** autour de la date d'expiration
- L'impact est PLUS fort si : ratio locked/float élevé, insiders VC (vs fondateurs), entreprise non-rentable
- L'impact est MOINDRE si : insiders fondateurs engagés long-terme, entreprise rentable, cours déjà bas

**Stratégie autour du lock-up :**
- **Si tu veux acheter** : attendre APRÈS le lock-up expiry (pression vendeuse passée = meilleur prix d'entrée)
- **Si tu détiens déjà** : hedger ou réduire la position AVANT le lock-up expiry
- **Signal insider** : si les insiders NE vendent PAS après le lock-up → signal de conviction très positif

---

### IPO-5 — DILUTION : L'ENNEMI SILENCIEUX

**La dilution est le risque n°1 des IPOs sur le moyen terme.** Chaque émission de nouvelles actions réduit ta part du gâteau.

**Sources de dilution à traquer :**

| Source | Impact | Où la trouver |
|--------|--------|--------------|
| **Actions nouvelles émises à l'IPO** | Immédiat | Prospectus — section "Dilution" |
| **Stock options employés (ESOP)** | Progressif | Prospectus — section "Compensation" |
| **Warrants** | Conditionnel | Prospectus — section "Securities" |
| **Convertibles** | Conditionnel | Prospectus — section "Debt" |
| **Augmentations de capital futures** | Potentiel | Pas dans le prospectus — évaluer le besoin |
| **Greenshoe (15% additionnel)** | Court-terme | Prospectus — section "Underwriting" |

**Calcul de dilution obligatoire :**
```
Actions pré-IPO (fully diluted)  : [X] M
+ Actions nouvelles émises IPO   : [X] M (+Y%)
+ Greenshoe si exercé            : [X] M (+Y%)
+ Stock options en circulation   : [X] M (+Y%)
+ Warrants/convertibles          : [X] M (+Y%)
= Total fully diluted post-IPO   : [X] M

Dilution totale pour un actionnaire pré-IPO : -[Y]%
Dilution potentielle future (ESOP + warrants) : -[Y]% supplémentaire
```

**⚠️ RED FLAGS dilution :**
- Dilution >30% à l'IPO sans raison de croissance claire
- ESOP >15% du capital total → compensation excessive ou rétention problématique
- Historique d'augmentations de capital répétées en pré-IPO (tours de financement très dilutifs)
- Clauses anti-dilution pour certains investisseurs mais pas pour les nouveaux actionnaires

---

### IPO-6 — LES 3 PHASES TECHNIQUES D'UNE IPO (Analyse technique adaptée)

**L'analyse technique classique ne fonctionne pas sur une IPO fraîche** (pas d'historique). À la place, utiliser le framework des 3 phases d'une IPO :

**Phase 1 — IPO Advance Phase (IPO-AP) : Jours 1-20**
- Mouvement de prix rapide et volatile juste après la cotation
- Dominé par le retail et les algorithmes, PAS par les institutionnels
- Volume très élevé puis décroissant
- **NE PAS ACHETER DANS CETTE PHASE** sauf si le prix est clairement sous la fair value
- Surveiller : gap up/down au jour 1, volume relatif, amplitude des bougies

**Phase 2 — Institutional Due Diligence Phase (I-DDP) : Semaines 3-12**
- Consolidation et construction de base : le prix se stabilise dans un range
- Les institutionnels étudient les fondamentaux avant de prendre position
- Volume décroissant = normal et sain (absorption de l'offre)
- **Formation de la "IPO Base"** — le pattern clé à surveiller :
  - Shallow Base (15-20% de profondeur) → signal fort, comme un flat base
  - Deep Base (30-35%) → similaire à un Cup & Handle, consolidation plus longue
  - Bottom Carving (>35%) → correction prolongée, accumulation lente
- **C'est la phase d'observation idéale** — collecter les données, affiner la valorisation

**Phase 3 — Institutional Advance Phase (I-AP) : Mois 3-12+**
- Les institutionnels commencent à acheter → tendance haussière plus stable
- Breakout de la IPO Base avec volume en hausse = signal d'achat technique
- La couverture analyste démarre (initiations de couverture)
- Les premiers earnings post-IPO confirment ou infirment la thèse
- **MEILLEUR MOMENT pour entrer** si les fondamentaux sont bons

**Signal d'achat technique IPO :**
```
✅ ACHETER si TOUS ces critères sont réunis :
  □ IPO Base formée (minimum 3 semaines de consolidation)
  □ Breakout au-dessus du haut de la base avec volume >150% de la moyenne
  □ Fondamentaux validés (prospectus analysé, valorisation raisonnable)
  □ Lock-up expiry passé OU suffisamment loin (>30 jours)
  □ Pas de red flags majeurs dans le prospectus

⚠️ ATTENDRE si :
  □ Toujours en Phase 1 (volatilité post-IPO)
  □ Lock-up expiry dans les 30 prochains jours
  □ Aucune base technique formée
  □ Volume en déclin constant sans stabilisation
```

---

### IPO-7 — RED FLAGS ET ANTI-PATTERNS (⚠️ CE QUI DOIT ALERTER)

**Checklist de red flags — si 3+ sont cochés, ÉVITER l'IPO :**

```
RED FLAGS IPO — [Entreprise]

PROSPECTUS & GOUVERNANCE :
□ Use of proceeds vague ("general corporate purposes") sans détail
□ Insiders vendent massivement à l'IPO (secondary offering > primary)
□ Structure dual-class avec contrôle >50% par un seul individu sans contre-pouvoir
□ Related party transactions significatives non justifiées
□ Changements récents de CEO/CFO/auditeur (<12 mois avant IPO)
□ Restatements ou rectifications comptables avant l'IPO
□ Litiges majeurs en cours mentionnés dans les risk factors

FINANCIERS :
□ Cash burn élevé sans chemin clair vers la rentabilité
□ Croissance du CA en décélération sur les 3 derniers trimestres
□ Marges en détérioration malgré la croissance
□ Concentration client extrême (1 client > 20% du CA)
□ Dépendance à un seul produit/marché
□ Working capital négatif ou tendu

VALORISATION :
□ P/S ou EV/Revenue >2x supérieur aux pairs cotés sans justification
□ IPO pricée au-dessus de la fourchette indicative initiale (signe de FOMO, pas de qualité)
□ Aucun comparable coté pertinent (marché trop niche ou inexistant)
□ Dernière valorisation privée (dernier tour VC) < prix d'IPO de >50% → inflation rapide suspecte

MARCHÉ & TIMING :
□ IPO lancée dans un marché baissier / volatil (VIX > 25)
□ Secteur en hype médiatique (IA, crypto, espace) sans fondamentaux solides
□ Plusieurs IPOs du même secteur la même semaine (saturation)
□ L'entreprise a déjà retiré une tentative d'IPO précédente

UNDERWRITERS :
□ Underwriter Tier 4 ou inconnu sans co-lead Tier 1-2
□ Pas d'option greenshoe
□ Syndicat de placement très restreint (<3 banques)

TOTAL RED FLAGS : [X] / 20
→ 0-2 : Feu vert ✅
→ 3-5 : Vigilance accrue ⚠️ — approfondir chaque red flag
→ 6+  : ÉVITER 🔴 — trop de signaux négatifs
```

---

### IPO-8 — CAS SPÉCIAL : IPO PRÉ-REVENUE / PRÉ-PROFIT

**Pour les entreprises non encore rentables (biotech, deep tech, SaaS early-stage) :**

**Métriques alternatives (le P/E ne sert à rien ici) :**
- **Burn rate mensuel** et runway (mois de trésorerie restants)
- **Cash levé à l'IPO** vs burn rate = combien de mois de survie
- **Milestones clés** : prochains résultats cliniques (biotech), contrats signés, MVP lancé
- **TAM crédible** : le marché adressable est-il réel ou théorique ?
- **Qualité du pipeline** : combien de produits en développement, à quel stade ?
- **Net Revenue Retention (NRR)** pour SaaS : >120% = excellent, <100% = ⚠️ churn
- **CAC/LTV ratio** : coût d'acquisition client vs valeur vie client

**Valorisation pré-revenue :**
- **Comparables privés** : dernière valorisation VC (mais appliquer décote 20-30%)
- **Approche milestone** : valeur = probabilité de succès × valeur en cas de succès
- **EV/Revenue projeté** : utiliser les projections Year+2 ou Year+3 du prospectus avec décote -30%
- **Sum-of-the-parts** : si multi-produits, valoriser chaque programme séparément

**⚠️ RÈGLE DE PRUDENCE :** pour une IPO pré-revenue, la probabilité d'échec est structurellement plus élevée. Toujours dimensionner la position en conséquence (taille réduite, max 2-3% du portefeuille).

---

### IPO-9 — ANALYSE DU MARCHÉ ET DU TIMING

**Le timing macro compte autant que la qualité de l'entreprise pour une IPO.**

**Indicateurs de contexte marché :**
```
WebSearch : "IPO market conditions [année] outlook"
```

| Indicateur | Favorable à l'IPO | Défavorable |
|------------|-------------------|-------------|
| **VIX** | < 20 | > 25 |
| **Tendance S&P 500 / Eurostoxx** | Haussière | Baissière |
| **Taux Fed / BCE** | Stables ou en baisse | En hausse rapide |
| **Sentiment investisseurs** | Risk-on, FOMO modéré | Risk-off, panique |
| **Pipeline IPO** | Modéré (pas de saturation) | Saturé (trop d'IPOs en même temps) |
| **Performance des IPOs récentes** | >60% en positif au J+30 | <40% en positif |
| **Fenêtre saisonnière** | Sept-Nov, Jan-Mars | Été (juil-août), fin décembre |

---

### IPO-10 — COMPORTEMENT DES INSIDERS (SIGNAL LE PLUS FIABLE)

**Ce que font les insiders est plus important que ce qu'ils disent.**

**Signaux à surveiller :**

| Comportement | Signal | Impact |
|-------------|--------|--------|
| Fondateurs gardent >80% de leurs actions | ✅ Très positif | Forte conviction |
| VC vendent une partie mais gardent >50% | ✅ Positif | Normal pour un VC, sain |
| Insiders vendent >50% de leurs actions à l'IPO | 🔴 Négatif | Cash out, pas de conviction long-terme |
| Fondateur vend 100% à l'IPO | 🔴🔴 Très négatif | Abandon du navire |
| Insiders achètent au marché après l'IPO | ✅✅ Très positif | Signal de sous-évaluation perçue |
| Vente massive au lock-up expiry | ⚠️ À contextualiser | Normal pour VC, inquiétant pour management |
| Prolongation volontaire du lock-up | ✅ Positif | Confiance dans la trajectoire |

**Recherche obligatoire :**
```
WebSearch : "[entreprise] insider transactions SEC Form 4"
WebSearch : "[entreprise] insider buying selling post IPO"
```

---

### IPO-11 — SYNTHÈSE ET RECOMMANDATION IPO

**Après toutes les sections IPO-1 à IPO-10, produire cette synthèse :**

```
## SYNTHÈSE IPO — [ENTREPRISE] — [Date d'IPO]

### Scorecard IPO
| # | Dimension | Note /10 | Commentaire clé |
|---|-----------|----------|----------------|
| 1 | Qualité du business model | /10 | [1 ligne] |
| 2 | Solidité financière | /10 | [1 ligne] |
| 3 | Utilisation des fonds | /10 | [1 ligne] |
| 4 | Qualité des underwriters | /10 | [1 ligne] |
| 5 | Valorisation vs pairs | /10 | [1 ligne] |
| 6 | Risque de dilution | /10 | [1 ligne] |
| 7 | Risque lock-up | /10 | [1 ligne] |
| 8 | Qualité du management | /10 | [1 ligne] |
| 9 | Timing marché | /10 | [1 ligne] |
| 10 | Comportement insiders | /10 | [1 ligne] |
| 11 | Red flags (inversé) | /10 | [X red flags détectés] |
| **TOTAL** | **Score IPO** | **X/10** | |

```
### Recommandation IPO

**SOUSCRIRE À L'IPO** si :
- Score IPO ≥ 7/10
- Valorisation ≤ fair value (pas de surévaluation)
- 0-2 red flags
- Underwriter Tier 1-2 avec greenshoe
- Fondateurs gardent >60% de leurs actions

**ATTENDRE APRÈS L'IPO** (stratégie recommandée par défaut) si :
- Score IPO 5-7/10
- Quelques red flags mais business solide
- Attendre : formation de la IPO Base (Phase 2) + lock-up expiry passé
- Meilleur point d'entrée probable dans les 3-6 mois post-IPO

**ÉVITER** si :
- Score IPO < 5/10
- 6+ red flags
- Surévaluation >30% vs pairs
- Insiders vendent massivement
- Underwriter Tier 4 sans greenshoe

### Thèse d'investissement IPO
- **Bull Case** (proba X%) : [scénario + objectif cours + horizon]
- **Base Case** (proba X%) : [scénario + objectif cours + horizon]
- **Bear Case** (proba X%) : [scénario + objectif cours + horizon]

### Calendrier des événements clés post-IPO
| Date | Événement | Impact potentiel |
|------|-----------|-----------------|
| J+30 | Fin de la période de quiet period → initiations analystes | Mouvement de prix |
| J+90/180 | Lock-up expiry | Pression vendeuse potentielle |
| J+[X] | Premiers earnings post-IPO | Confirmation/infirmation de la thèse |
| J+[X] | Inclusion dans un indice (si éligible) | Flux passifs positifs |
```

**Disclaimer : Ceci n'est pas un conseil en investissement. L'analyse d'IPO comporte des risques accrus liés au manque d'historique et à l'asymétrie d'information.**

---

### SOURCES DE DONNÉES IPO — Recherches WebSearch obligatoires

Pour chaque analyse d'IPO, lancer systématiquement :
```
WebSearch : "[entreprise] IPO prospectus S-1 SEC EDGAR"
WebSearch : "[entreprise] IPO pricing date valuation"
WebSearch : "[entreprise] IPO lock-up period expiration"
WebSearch : "[entreprise] IPO underwriter bookrunner lead"
WebSearch : "[entreprise] IPO insider ownership dilution"
WebSearch : "[entreprise] IPO red flags risks analysis"
WebSearch : "[entreprise] IPO vs competitors valuation multiples"
WebSearch : "[entreprise] IPO performance first day week month"
WebSearch : "[entreprise] IPO analyst coverage initiation"
WebFetch  : SEC EDGAR si US / AMF si France / Euronext si Europe
```


## ROUTAGE MULTI-IA OBLIGATOIRE
| Tâche | IA Primaire | IA Secondaire | Justification |
|-------|------------|---------------|---------------|
| Calculs financiers (DCF, comps) | Gemini Flash | Mistral Large | Gemini N°1 finance 10/10 |
| Analyse en français | Mistral Large | Gemini Flash | Mistral N°1 français 10/10 |
| Raisonnement profond | DeepSeek-R1 (OpenRouter) | Gemini Flash | Thinking tokens, 4.3s |
| Validation rapide | Groq (2.8s) | HuggingFace (2.0s) | Vitesse prioritaire |
| Vérification croisée | TOUTES en parallèle | — | Anti-hallucination |

## SOURCES OBLIGATOIRES (minimum 3 actualités + 3 données)
**Actualités :** Bloomberg, Reuters, Investing.com, Zonebourse, CNBC, Financial Times
**Données financières :** FinViz, Macrotrends, MarketScreener, TipRanks, Simply Wall St
**Données structurées :** Alpha Vantage MCP, FMP API (primaire)
**Règle :** minimum 2 sources concordantes par affirmation factuelle.

## MATRICE DE FALLBACK
| Outil principal | Fallback 1 | Fallback 2 |
|----------------|------------|------------|
| Bigdata.com (expiré) | +3 WebSearch ciblées | FMP API |
| LunarCrush (instable) | WebSearch sentiment | Yahoo Finance |
| Alpha Vantage (quota) | FMP API | WebSearch données structurées |
| DeepSeek (solde vide) | Mistral Large reason | Gemini Flash |
| FMP API (limite) | Alpha Vantage MCP | Macrotrends WebFetch |

## INTÉGRATION ALPHA VANTAGE MCP
Indicateurs techniques à consulter :
- RSI, MACD, Bandes de Bollinger, SMA 50/200, EMA, Stochastique, ADX
- COMPANY_OVERVIEW : profil + ratios clés
- INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW : fondamentaux
- EARNINGS : surprises EPS
- INSTITUTIONAL_HOLDINGS, INSIDER_TRANSACTIONS : alignement intérêts

**Indicateurs avancés — mapping sources :**

| Groupe d'indicateurs | Endpoints Alpha Vantage | Fallback FMP | Fallback WebSearch |
|---------------------|------------------------|-------------|-------------------|
| Piotroski F-Score | INCOME_STATEMENT + BALANCE_SHEET + CASH_FLOW (3 ans) | /income-statement + /balance-sheet + /cash-flow-statement | Macrotrends, SimplyWallSt |
| Altman Z-Score | BALANCE_SHEET + INCOME_STATEMENT + GLOBAL_QUOTE (market cap) | /balance-sheet + /income-statement + /profile | FinViz, GuruFocus |
| Beneish M-Score | INCOME_STATEMENT + BALANCE_SHEET (2 années consécutives) | /income-statement + /balance-sheet | GuruFocus "[ticker] m-score" |
| DuPont Decomposition | INCOME_STATEMENT + BALANCE_SHEET | /ratios | Macrotrends, SimplyWallSt |
| CCC (DSO/DIO/DPO) | BALANCE_SHEET (receivables, inventory, payables) + INCOME_STATEMENT (COGS, revenue) | /ratios | "[ticker] cash conversion cycle" |
| Shareholder Yield | CASH_FLOW (dividends, buybacks, debt change) | /cash-flow-statement | "[ticker] shareholder yield" |
| CROCI | CASH_FLOW + BALANCE_SHEET (gross invested capital) | /cash-flow-statement + /balance-sheet | "[ticker] CROCI" |
| Magic Formula | INCOME_STATEMENT (EBIT) + GLOBAL_QUOTE (EV) + ROIC | /enterprise-values + /ratios | GuruFocus Magic Formula |
| Earnings Revisions | EARNINGS | /analyst-estimates | TipRanks, MarketScreener, Seeking Alpha |
| Earnings Surprise/SUE | EARNINGS (historical quarterly) | /earnings-surprises | "[ticker] earnings surprise history" |
| Estimate Dispersion | Non disponible | /analyst-estimates (high/low/avg) | "[ticker] estimate dispersion" FactSet |
| Sectoriels | Non disponible | Selon secteur | Rapport annuel + WebSearch spécialisé |

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "C'est un ETF, pas besoin d'analyse détaillée" | Les ETF ont leurs propres métriques (TER, tracking error, composition). Adapter, pas simplifier. |
| "Le marché est bullish, pas besoin de scénario bear" | Le scénario bear est TOUJOURS obligatoire. C'est quand tout va bien qu'on oublie les risques. |
| "Les données de training suffisent" | JAMAIS. Prix, résultats, guidance changent chaque trimestre. Données fraîches OBLIGATOIRES. |
| "Un seul timeframe suffit" | Minimum 2 timeframes (court terme + long terme) pour une vision complète. |

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Framework d'analyse | `financial-analysis-framework` |
| Modélisation avancée | `financial-modeling` |
| Contexte macro | `macro-analysis` |
| Collecte données | `deep-research` |
| Validation | `qa-pipeline` |
| Export | `pdf-report-gen` |

## ÉVOLUTION

Après chaque analyse :
- Si données manquantes pour un type d'actif → enrichir les sources
- Si le scoring était mal calibré → ajuster les pondérations
- Si un edge case non couvert → l'ajouter dans les anti-patterns

Seuils : qualité < 7/10 → revoir la méthodologie pour ce type d'actif.

## LIVRABLE FINAL

- **Type** : PDF
- **Généré par** : pdf-report-pro
- **Destination** : acollenne@gmail.com via send_report.py

## CHAÎNAGE ARBORESCENCE

- **Amont** : deep-research (entrée unique)
- **Aval** : pdf-report-pro

