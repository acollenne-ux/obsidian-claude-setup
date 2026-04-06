---
name: financial-modeling
description: >
  Modélisation financière avancée : DCF, comparable companies analysis (comps), LBO, modèles de valorisation, projections financières, analyse de bilans. Invoqué automatiquement quand l'utilisateur demande une valorisation, un modèle financier, un DCF, une analyse de comparables, un LBO, des projections de revenus/marges, ou tout travail de modélisation Excel/Python en finance. Aussi déclenché pour : "valorise cette entreprise", "fais un DCF", "compare ces entreprises", "projections financières", "calcule le fair value".
argument-hint: "entreprise ou secteur à modéliser"
allowed-tools: WebSearch, WebFetch, mcp__duckduckgo-search__search, mcp__claude_ai_Bigdata_com__bigdata_company_tearsheet, Bash
---

## RÈGLE UNIVERSELLE — LIRE L'INTÉGRALITÉ DU SKILL AVANT D'AGIR

**OBLIGATOIRE : Avant d'exécuter quoi que ce soit, tu DOIS :**
1. Lire l'INTÉGRALITÉ de ce fichier SKILL.md (pas juste le début)
2. Comprendre chaque section, chaque règle, chaque contrainte
3. Respecter ce skill À LA LETTRE — ne rien sauter, ne rien simplifier

**Ne JAMAIS commencer l'exécution sans avoir lu et compris TOUT le skill.**

---

## AUTO-SOURCING OBLIGATOIRE AVANT TOUT CALCUL
**RÈGLE : Ne JAMAIS commencer un modèle sans données réelles.**
1. FMP API (primaire) : `https://financialmodelingprep.com/api/v3/` — income-statement, balance-sheet, cash-flow, ratios, profile
2. Alpha Vantage MCP : INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW, COMPANY_OVERVIEW
3. WebSearch structuré : FinViz, Macrotrends, MarketScreener pour données complémentaires
Chaîne de fallback : FMP → Alpha Vantage → WebSearch → Zonebourse/Boursorama

---

## MÉTHODOLOGIE WACC DÉTAILLÉE
### Inputs requis avec sources :
- **Risk-Free Rate** : Treasury 10Y US (FRED DGS10) ou OAT 10Y France
- **Beta** : Source = Yahoo Finance, FinViz, ou calcul vs indice sur 5 ans
- **Equity Risk Premium** : Damodaran (NYU) annual update (~5-6% US, 7-8% émergents)
- **Cost of Debt** : taux d'intérêt moyen pondéré de la dette (rapport annuel)
- **Tax Rate** : taux d'imposition effectif (income statement)
- **D/E Ratio** : dette nette / capitalisation boursière
### Formule : WACC = (E/V × Re) + (D/V × Rd × (1-T))
### Ajustements : +1-3% prime small-cap si market cap < 2B, +1-2% prime pays si émergent

---

## VÉRIFICATION DCF VS CONSENSUS
Après chaque DCF, TOUJOURS comparer :
1. Fair value DCF calculée vs prix actuel du marché
2. Fair value DCF vs consensus analystes (TipRanks, MarketScreener, FinViz)
3. Si écart > 30% avec consensus → vérifier hypothèses (WACC trop bas ? Croissance trop optimiste ?)
4. Documenter : "Notre DCF donne X€, consensus Y€, écart Z% dû à [raison]"

---

## ANALYSE DE SENSIBILITÉ OBLIGATOIRE
Produire TOUJOURS un tableau de sensibilité :

| WACC \ Croissance | 1% | 2% | 3% | 4% | 5% |
|-------------------|------|------|------|------|------|
| 7% | X€ | X€ | X€ | X€ | X€ |
| 8% | X€ | X€ | X€ | X€ | X€ |
| 9% | X€ | **BASE** | X€ | X€ | X€ |
| 10% | X€ | X€ | X€ | X€ | X€ |
| 11% | X€ | X€ | X€ | X€ | X€ |

Mettre en gras le scénario de base. Identifier le range de fair value.

---

## ROUTAGE MULTI-IA — MODÉLISATION FINANCIÈRE
| Tâche | IA Primaire | Justification |
|-------|------------|---------------|
| Calculs DCF/comps | Gemini Flash | N°1 finance 10/10 benchmarké |
| Rédaction rapport FR | Mistral Large | N°1 français 10/10 |
| Raisonnement valorisation | DeepSeek-R1 (OpenRouter) | Thinking tokens |
| Validation rapide | Groq | 2.8s, gratuit |
| Vérification croisée | TOUTES IAs parallèle | Anti-hallucination |

## SYSTÈME DE CONFIANCE
| Niveau | Critère | Marqueur |
|--------|---------|----------|
| ÉLEVÉ | Données rapport officiel + 2 sources | ✓✓✓ |
| MOYEN | 1 source fiable (FMP/Alpha Vantage) | ✓✓ |
| FAIBLE | WebSearch non vérifié | ✓ |
| SPÉCULATIF | Estimation/projection | ~ |

---

# Skill : Modélisation Financière

## Types de modèles

### 1. DCF (Discounted Cash Flow)
Étapes :
1. Récupérer les données historiques (revenus, EBITDA, capex, working capital) via Bigdata.com ou WebSearch
2. Projeter les FCF sur 5-10 ans avec hypothèses de croissance justifiées
3. Calculer le WACC (coût des fonds propres via CAPM + coût de la dette)
4. Terminal value (Gordon Growth ou exit multiple)
5. Sensibilité sur WACC et taux de croissance terminal

**Format de sortie** : tableau Python/pandas ou markdown structuré avec les hypothèses clés

### 2. Comparable Companies (Comps)
1. Identifier 5-8 comparables sectoriels
2. Collecter multiples : EV/EBITDA, EV/Revenue, P/E, P/FCF
3. Calculer médiane et moyenne du groupe
4. Appliquer à la société cible
5. Prime/décote justifiée

### 3. LBO (Leveraged Buyout)
1. Structure capitalistique (dette/equity split)
2. Hypothèses d'entrée (prix d'achat, multiple EBITDA)
3. Projection des remboursements de dette
4. Calcul du TRI (IRR) cible sur 5 ans
5. Sensibilité sur prix d'entrée et de sortie

## Sources de données à utiliser
- `mcp__claude_ai_Bigdata_com__bigdata_company_tearsheet` : données fondamentales
- `mcp__alpha-vantage__` : données financières historiques
- WebSearch : rapports annuels, présentations investisseurs, consensus analystes

## Format de présentation
Toujours présenter :
- Les hypothèses utilisées (avec justification)
- Les résultats chiffrés
- L'analyse de sensibilité (tableau 3x3 minimum)
- La conclusion : surévalué / juste prix / sous-évalué

## Code Python (si demandé)
Utiliser pandas, numpy. Compatible Python 3.13. RAM 12 GB disponible — Monte Carlo jusqu'à 50 000 simulations OK.

---

## CHECKLIST OBLIGATOIRE

1. **Collecter les données réelles** — FMP / Alpha Vantage / WebSearch (JAMAIS inventer)
2. **Identifier le type de modèle** — DCF, Comps, LBO, ou combiné
3. **Calculer le WACC** — avec sources documentées pour chaque input
4. **Produire l'analyse de sensibilité** — tableau WACC × croissance (minimum 5×5)
5. **Comparer au consensus** — TipRanks, MarketScreener, FinViz
6. **Conclure** — surévalué / juste prix / sous-évalué avec intervalle de confiance

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Le DCF suffit seul pour valoriser" | TOUJOURS croiser DCF + Comps + consensus. Un seul modèle = biais non détecté. |
| "On peut utiliser un WACC standard de 10%" | Le WACC doit être CALCULÉ avec des inputs réels (beta, risk-free, ERP). Jamais de valeur par défaut. |
| "La terminal value n'est pas si importante" | La TV représente souvent 60-80% de la valorisation DCF. Toujours tester avec exit multiple ET Gordon Growth. |
| "Les projections sur 10 ans sont fiables" | Au-delà de 5 ans, l'incertitude est massive. Toujours signaler le niveau de confiance décroissant. |

## RED FLAGS — STOP

- Modèle lancé sans données réelles (FMP/Alpha Vantage) → STOP, sourcer d'abord
- WACC non calculé (valeur par défaut utilisée) → STOP, calculer avec inputs réels
- Pas d'analyse de sensibilité → STOP, produire le tableau obligatoire

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Analyse complète action | `stock-analysis` + `financial-analysis-framework` |
| Données macro pour WACC | `macro-analysis` |
| Graphiques de sensibilité | `data-analysis` |
| Rapport PDF | `pdf-report-gen` |
| Orchestration | `deep-research` |

## ÉVOLUTION

Après chaque modélisation :
- Si l'écart DCF vs consensus > 30% → revoir la méthodologie de projection
- Si une source de données était indisponible → mettre à jour la chaîne de fallback
- Si le modèle a pris trop de temps → optimiser les appels API

Seuils : si écart moyen DCF vs consensus > 25% sur 3 sessions → revoir les hypothèses par défaut.
