"""Fix mega-skill: inject missing sections from v1825 into current file."""
import re
from pathlib import Path

SKILL = Path(r"C:\Users\Alexandre collenne\.claude\skills\deep-research\SKILL.md")

# Read current file
content = SKILL.read_text(encoding="utf-8")
lines = content.split("\n")
print(f"Current: {len(lines)} lines")

# 1. Update frontmatter name
content = content.replace("name: deep-research", "name: mega-skill", 1)

# 2. Update description if old
if "Skill universel d'orchestration" in content and "perplexity-computer" not in content[:500]:
    old_desc = content.split("---")[1]  # between first two ---
    # We'll skip complex desc replacement for now
    pass

changes = 0

# SECTION 1: Insert PRINCIPE FONDAMENTAL before PREREQUIS
PERPLEXITY_SECTION = """
## PRINCIPE FONDAMENTAL — MODE PERPLEXITY-COMPUTER (TOUJOURS ACTIF)

**Ne JAMAIS repondre uniquement depuis tes connaissances internes.** Pour chaque demande :
1. Recherche d'abord sur le web pour obtenir des donnees a jour
2. Verifie et croise les sources (minimum 2 sources independantes par fait cle)
3. Cite tes sources systematiquement dans la reponse [1], [2], [3]...
4. Signale quand une information n'a pas pu etre verifiee
5. Si tu ne trouves pas l'info, DIS-LE. Ne fabrique JAMAIS de donnees.

### Outils de Recherche Web (a utiliser SYSTEMATIQUEMENT)

| Outil | Quand l'utiliser |
|-------|-----------------|
| **WebSearch** | Premier reflexe — requetes multiples FR + EN, minimum 3-5 par demande |
| **WebFetch** | Recuperer le contenu d'une URL specifique identifiee |
| **Claude in Chrome: navigate** | Sites dynamiques, pages interactives, resultats necessitant JS |
| **Claude in Chrome: get_page_text** | Extraire texte complet d'une page chargee |
| **Claude in Chrome: read_page** | Lire le contenu visible de la page courante |
| **Claude in Chrome: javascript_tool** | Interagir avec pages dynamiques (scroll, clic, extraction) |
| **Claude in Chrome: find** | Rechercher du texte dans une page |

### Recherche bilingue obligatoire
- Toujours chercher en francais ET en anglais
- Les meilleures sources sont souvent en anglais
- Varier les formulations et les angles de recherche
- Utiliser des operateurs avances : site:, intitle:, daterange:

### Workflow recherche rapide (question simple)
1. Lance 2-3 WebSearch (FR + EN) avec formulations variees
2. Accede aux 2-3 meilleures sources via WebFetch ou Chrome
3. Extrais les informations pertinentes
4. Formule ta reponse avec citations [1], [2]...

### Workflow recherche approfondie (question complexe)
-> Suit le pipeline complet ci-dessous (Phases 0-12)

---
"""

anchor1 = "## PREREQUIS OBLIGATOIRES"
if anchor1 in content and "PRINCIPE FONDAMENTAL" not in content:
    content = content.replace(anchor1, PERPLEXITY_SECTION + "\n" + anchor1)
    changes += 1
    print(f"[+] Inserted PRINCIPE FONDAMENTAL ({PERPLEXITY_SECTION.count(chr(10))} lines)")
else:
    print("[=] PRINCIPE FONDAMENTAL already present or anchor not found")


# SECTION 2: Insert PHASE 6B-6E before PHASE 7
# These go after the SYNTHESE section (after Phase 6 content) and before Phase 7

PHASE_6B = """
## PHASE 6B — ANALYSE QUALITATIVE APPROFONDIE : MOAT & REMPARTS (EN COMPLEMENT DES 15 DIMENSIONS)

Les 15 dimensions ci-dessus couvrent le quantitatif. Cette section ajoute le **deep dive qualitatif**.

### 6B-1. Valeur Intrinseque vs Prix Marche (OBLIGATOIRE)
3 methodes : DCF multi-scenarios, EPV (Earnings Power Value), SOTP (Sum of the Parts)
Resultat obligatoire : valeur intrinseque, prix marche, marge de securite, valeur projetee 3-5 ans

### 6B-2. Comparaison Peers — Analyse de Sous/Surevaluation
Comparer EV/EBITDA, P/E Forward, P/FCF, P/B, EV/Revenue avec 3+ peers et mediane secteur

### 6B-3. Deep Dive Avantages Concurrentiels
- Switching costs (couts de changement)
- Effet de reseau (quantifier)
- Economies d'echelle
- Score chaque avantage : Tres eleve / Eleve / Moyen / Faible

### 6B-4. Monopoles, Duopoles et Barrieres a l'Entree
Parts de marche top 1/2/3, barrieres reglementaires, risque antitrust

### 6B-5. Pricing Power (CRITIQUE)
Historique hausses prix vs volume, elasticite-prix, marge brute 5+ ans

### 6B-6. Brevets et Propriete Intellectuelle
Brevets actifs, dates expiration, R&D % CA, pipeline innovation

### 6B-7. Recurrence des Revenus
Part revenus recurrents, churn rate, NRR (>120% = excellent), LTV/CAC (>3 = bon)

### 6B-8. Orientation Client et Qualite de Service
NPS, CSAT, reputation plateformes avis, taux retour

### 6B-9. Dependance aux Gros Clients (RISQUE)
% CA top 1/5/10 clients, si >10% = risque identifie, diversification geo et sectorielle

---

## PHASE 6C — GOUVERNANCE ET CAPITAL HUMAIN (ENRICHI)

### 6C-1. Sentiment Employes (Glassdoor/Indeed/Forums)
WebSearch "[entreprise] Glassdoor reviews", note globale, CEO approval, tendance
Ponderation temporelle : 0-6 mois x3, 6m-2a x2, 2-5a x1, >5a x0.5

### 6C-2. Accidentologie et Securite (secteurs industriels)
TRIR/LTIR, amendes OSHA, tendance

### 6C-3. Qualite de la Gouvernance (enrichie)
Board independance/diversite, remuneration CEO ratio, insider ownership, SBC % CA, track record guidances, controverses ESG

---

## PHASE 6D — ANALYSE MACRO PAR PAYS (entreprises multi-geographiques)

Pour les top 3-5 pays par CA, interroger FRED et OCDE :
- Phase du cycle, PIB, inflation, taux directeurs, chomage
- Sensibilite cycles : beta historique, performance en recession, correlation CA/PIB
- Previsions OCDE/FMI 12 mois

---

## PHASE 6E — M&A ET PROJETS FUTURS

### Acquisitions recentes (3-5 dernieres annees)
Logique strategique, prix paye vs valeur, integration reussie/ratee, goodwill impairment

### Pipeline futur
Nouveaux produits, expansion geographique, CAPEX (maintenance vs croissance), guidance credibilite, backlog

---
"""

anchor2 = "## PHASE 7"
if anchor2 in content and "PHASE 6B" not in content:
    # Find exact "## PHASE 7 " (with space to avoid matching 7B)
    idx = content.find("## PHASE 7 ")
    if idx == -1:
        idx = content.find("## PHASE 7\n")
    if idx == -1:
        # Try with dash
        for pattern in ["PHASE 7 -", "PHASE 7 —", "PHASE 7\t"]:
            idx = content.find(pattern)
            if idx != -1:
                idx = content.rfind("##", 0, idx)
                break
    if idx > 0:
        content = content[:idx] + PHASE_6B + "\n" + content[idx:]
        changes += 1
        print(f"[+] Inserted PHASE 6B-6E ({PHASE_6B.count(chr(10))} lines)")
    else:
        print("[!] Could not find PHASE 7 anchor")
else:
    print("[=] PHASE 6B already present or anchor not found")


# SECTION 3: Insert PHASE 7B before PHASE 8
PHASE_7B = """
## PHASE 7B — FRAMEWORK ANALYSE MACRO-ECONOMIQUE (si demande macro/cycles)

### 7B-1. Situation Cyclique
Phase du cycle, PMI (ISM), Conference Board LEI, courbe des taux (T10Y2Y via FRED), spreads credit

### 7B-2. Politique Monetaire
Fed, BCE, BoJ, BoE, PBoC : taux actuels vs neutres, bilan BC (QT/QE), forward guidance, CME FedWatch

### 7B-3. Inflation & Prix
CPI core, PCE core (US), HICP (EU) via FRED/OCDE, breakevens TIPS, pipeline PPI->CPI

### 7B-4. Croissance & Emploi
PIB reel trimestriel, NFP, chomage (UNRATE), JOLTS, salaire horaire, consommation, investissement

### 7B-5. Liquidite & Flux de Capitaux
Conditions financieres (FCI), DXY, flux emergents vs developpes, taux reels

### 7B-6. Risques Geopolitiques & Structurels
Dettes souveraines, risques geopolitiques actifs, transitions structurelles

### 7B-7. Implications Marches
Actions (secteurs gagnants/perdants), obligations, devises, matieres premieres
Notation regime macro obligatoire : Goldilocks / Reflation / Stagflation / Deflation

### 7B-8. Requetes FRED/OCDE Systematiques
FRED : GDPC1, CPIAUCSL, FEDFUNDS, UNRATE, T10Y2Y (api_key=fe9ed495e7db1d53eac4972b2e1f76fb)
OCDE : GDP, inflation multi-pays
World Bank : pays emergents, donnees structurelles longues

---
"""

anchor3 = "## PHASE 8"
if anchor3 in content and "PHASE 7B" not in content:
    idx = content.find("## PHASE 8 ")
    if idx == -1:
        idx = content.find("## PHASE 8\n")
    if idx == -1:
        for pattern in ["PHASE 8 -", "PHASE 8 —"]:
            idx = content.find(pattern)
            if idx != -1:
                idx = content.rfind("##", 0, idx)
                break
    if idx > 0:
        content = content[:idx] + PHASE_7B + "\n" + content[idx:]
        changes += 1
        print(f"[+] Inserted PHASE 7B ({PHASE_7B.count(chr(10))} lines)")
    else:
        print("[!] Could not find PHASE 8 anchor")
else:
    print("[=] PHASE 7B already present or anchor not found")

# SAVE
if changes > 0:
    # Backup
    backup = SKILL.with_suffix(".md.bak")
    backup.write_text(SKILL.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Backup saved: {backup}")
    
    # Write fixed version
    SKILL.write_text(content, encoding="utf-8")
    final_lines = content.count("\n") + 1
    print(f"Fixed: {final_lines} lines ({changes} sections inserted)")
else:
    print("No changes needed")
