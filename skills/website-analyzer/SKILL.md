---
name: website-analyzer
description: >
  Analyse complète de sites internet et sous-pages : esthétique, UX/UI, marketing, SEO,
  ventes/conversion, graphisme, identité de marque, performance, accessibilité, conformité,
  infrastructure technique, sécurité web, trackers et vie privée.
  Crawl automatique Playwright (screenshots + HTML + métriques + scraping technique approfondi),
  5 agents spécialisés, scoring /100 sur 12 dimensions, rapport PDF professionnel avec
  recommandations priorisées.
  
  TOUJOURS invoquer ce skill quand l'utilisateur demande d'analyser un site web, auditer un
  site internet, évaluer une page web, critiquer un design web, ou fournit une URL de site.
  Déclencheurs : "analyse ce site", "audit web", "audit site", "que penses-tu de ce site",
  "analyse site internet", "évalue ce site", "critique ce site web", "review du site",
  "analyse la page", "website audit", "site review", URL seule (détection automatique),
  /website-analyzer, /audit-web, /analyse-site
---

# Website Analyzer — Audit Web Professionnel

Skill d'analyse complète de sites internet avec crawl automatique, **5 agents spécialisés**
(dont un agent de scraping technique approfondi) et rapport PDF professionnel.

---

## RÈGLE UNIVERSELLE — LIRE L'INTÉGRALITÉ DU SKILL AVANT D'AGIR

**OBLIGATOIRE : Avant d'exécuter quoi que ce soit, tu DOIS :**
1. Lire l'INTÉGRALITÉ de ce fichier SKILL.md
2. Lire les fichiers agents dans `agents/`
3. Lire les fichiers references dans `references/`
4. Respecter ce skill À LA LETTRE

---

## PRÉREQUIS

**Dépendances Python :**
```bash
pip install playwright beautifulsoup4 Pillow
playwright install chromium
```

---

## WORKFLOW PRINCIPAL

### Étape 1 — Collecte & Configuration

**1A. Récupérer l'URL cible :**
- Si l'utilisateur fournit une URL → l'utiliser directement
- Si pas d'URL → demander : "Quelle est l'URL du site à analyser ?"

**1B. Demander le mode d'analyse :**
```
Quel type d'audit souhaitez-vous ?

A) Audit complet 360° — UX, SEO, marketing, conversion, branding, performance, accessibilité
B) Focus Marketing & Ventes — Conversion, tunnel de vente, CTA, copywriting, positionnement
C) Focus Design & Branding — Esthétique, cohérence visuelle, identité de marque, typographie

→ Choix (A/B/C) :
```

**1C. Mapping modes → agents et dimensions :**

| Mode | Agents activés | Dimensions scorées |
|------|---------------|-------------------|
| **A (360°)** | ux_ui + marketing_seo + conversion + brand + **tech_infra** | **12/12 dimensions** |
| **B (Marketing)** | marketing_seo + conversion + brand (léger) + **tech_infra** (léger) | 8 dimensions : SEO technique, Contenu, Performance, Conversion, Conformité, Identité marque, **Sécurité web, Configuration technique** |
| **C (Design)** | ux_ui + brand | 5 dimensions : Esthétique, UX/Ergonomie, Responsive, Identité marque, Accessibilité |

**1D. Options supplémentaires (optionnel) :**
- URL de concurrents pour benchmark comparatif
- Secteur d'activité (pour contextualiser les recommandations)
- Objectif principal du site (e-commerce, vitrine, SaaS, blog, institutionnel)

---

### Étape 2 — Crawl du site

Exécuter le crawler Playwright :

```bash
python "C:\Users\Alexandre collenne\.claude\skills\website-analyzer\scripts\site_crawler.py" "<URL>" --depth 2 --max-pages 50 --delay 1.5 --output "<dossier_output>"
```

**Le crawler produit :**
- `crawl_results.json` : données structurées (HTML, méta-tags, liens, métriques perf)
- `screenshots/` : captures pleine page de chaque URL crawlée
- `summary.json` : résumé du crawl (nombre de pages, arborescence, erreurs)

**Paramètres ajustables :**
- `--depth` : profondeur de crawl (défaut: 2)
- `--max-pages` : nombre max de pages (défaut: 50)
- `--delay` : délai entre pages en secondes (défaut: 1.5)
- `--timeout` : timeout global en minutes (défaut: 15)

**En cas d'échec du crawler :**
- Fallback sur WebFetch pour récupérer le HTML brut
- Pas de screenshots dans ce cas → analyse uniquement sur le code/contenu
- Signaler dans le rapport que l'analyse visuelle est limitée
- **CRITIQUE — Avertir les agents sur la qualité des données :**
  Quand les données proviennent de WebFetch (pas de rendu JS), ajouter cet avertissement
  au début du prompt de CHAQUE agent :
  ```
  ⚠️ QUALITÉ DES DONNÉES : FALLBACK WebFetch (pas de rendu JavaScript).
  Le contenu dynamique (prix, stock, filtres, carrousels, animations) peut être
  ABSENT des données mais PRÉSENT sur le site réel. Ne JAMAIS affirmer qu'un
  élément dynamique est "absent" — utiliser "non détecté dans les données
  collectées (à vérifier manuellement sur le site)".
  ```

---

### Étape 3 — Dispatch des agents d'analyse

Lire les données du crawl (`crawl_results.json` + `summary.json`), puis dispatcher
les agents EN PARALLÈLE selon le mode choisi.

**Chaque agent reçoit :**
- Les données du crawl (HTML, méta-tags, structure)
- Les screenshots des pages (pour analyse visuelle)
- Le fichier de référence correspondant (heuristiques, grille, checklist)
- Le mode d'analyse (A/B/C) pour adapter la profondeur
- **Le niveau de qualité des données** : `COMPLET` (crawler Playwright OK, JS rendu) ou
  `PARTIEL` (fallback WebFetch, pas de rendu JS). Si PARTIEL, chaque agent DOIT
  appliquer la règle 6/7 de son fichier .md (distinguer "non détecté" vs "absent").

**Lancer les agents avec l'outil `Agent` :**

```
Agent 1 (si mode A ou C) : UX/UI Agent
  → Lire agents/ux_ui_agent.md
  → Fournir : screenshots + HTML + references/ux_heuristics.md
  → Output attendu : scores + constats + recommandations UX/UI

Agent 2 (si mode A ou B) : Marketing/SEO Agent
  → Lire agents/marketing_seo_agent.md
  → Fournir : HTML + méta-tags + structure liens
  → Output attendu : scores + constats + recommandations SEO/Marketing

Agent 3 (si mode A ou B) : Conversion Agent
  → Lire agents/conversion_agent.md
  → Fournir : HTML + screenshots pages clés (landing, produit, checkout)
  → Output attendu : scores + constats + recommandations conversion

Agent 4 (si mode A, B ou C) : Brand Agent
  → Lire agents/brand_agent.md
  → Fournir : screenshots + HTML + references/brand_checklist.md
  → Output attendu : scores + constats + recommandations marque

Agent 5 (si mode A ou B) : Tech Infrastructure Agent
  → Lire agents/tech_infra_agent.md
  → Fournir : crawl_results.json (security_headers, technologies, resources, cookies, structured_data_details, content_metrics, contact_info) + summary.json (robots_txt, sitemap_xml) + references/tech_checklist.md
  → Output attendu : scores + constats + recommandations sur 5 sous-dimensions (Stack, Sécurité, Ressources, Trackers/Vie privée, Configuration technique)
```

**RÈGLE : Chaque agent DOIT lire son fichier .md dans agents/ ET le fichier de référence
associé AVANT de commencer son analyse.**

---

### Étape 4 — Consolidation des scores

Lire `references/scoring_grid.md` pour la grille de notation.

**Calculer le score global pondéré :**

| # | Dimension | Agent | Poids (mode A) | Poids (mode B) | Poids (mode C) |
|---|-----------|-------|----------------|----------------|----------------|
| 1 | Esthétique & Design visuel | UX/UI | 12% | — | 25% |
| 2 | UX / Ergonomie / Navigation | UX/UI | 10% | — | 25% |
| 3 | Responsive / Mobile | UX/UI | 8% | — | 15% |
| 4 | Identité de marque | Brand | 10% | 12% | 20% |
| 5 | SEO technique | Marketing | 8% | 17% | — |
| 6 | Contenu & Copywriting | Marketing | 8% | 17% | — |
| 7 | Performance (vitesse) | Marketing | 7% | 12% | — |
| 8 | Conversion & Tunnel de vente | Conversion | 10% | 17% | — |
| 9 | Accessibilité (WCAG) | UX/UI | 5% | — | 15% |
| 10 | Conformité (RGPD, mentions) | Conversion | 5% | 8% | — |
| 11 | **Sécurité & Infrastructure** | **Tech Infra** | **9%** | **9%** | — |
| 12 | **Trackers & Vie privée** | **Tech Infra** | **8%** | **8%** | — |

**Score global** = somme(score_dimension × poids) → note /100

**Échelle de notation :**
| Score | Lettre | Interprétation |
|-------|--------|---------------|
| 90-100 | A+ | Excellent — référence du secteur |
| 80-89 | A | Très bon — quelques optimisations mineures |
| 70-79 | B | Bon — axes d'amélioration identifiés |
| 60-69 | C | Correct — travail significatif nécessaire |
| 50-59 | D | Insuffisant — refonte partielle recommandée |
| < 50 | F | Critique — refonte majeure nécessaire |

---

### Étape 5 — Identification Forces / Faiblesses

**Top 5 Points Forts :**
- Dimensions avec score ≥ 8/10
- Éléments différenciants vs concurrents (si benchmark)
- Bonnes pratiques remarquables

**Top 5 Points Faibles :**
- Dimensions avec score ≤ 5/10
- Quick wins à fort impact
- Problèmes critiques (sécurité, accessibilité, mobile)

---

### Étape 6 — Recommandations priorisées

Classer chaque recommandation selon la matrice Impact × Effort :

| Priorité | Impact | Effort | Exemples |
|----------|--------|--------|----------|
| **P1 — Quick Wins** | Fort | Faible | Fix méta-tags, ajout CTA, correction couleurs contraste |
| **P2 — Projets stratégiques** | Fort | Élevé | Refonte navigation, nouveau tunnel conversion |
| **P3 — Améliorations** | Moyen | Faible | Optimisation images, ajout breadcrumbs |
| **P4 — Backlog** | Faible | Élevé | Refonte complète design, migration technologique |

---

### Étape 7 — Génération du rapport

Utiliser le template dans `templates/audit_report_template.md` pour structurer le rapport.

Exécuter le report builder :
```bash
python "C:\Users\Alexandre collenne\.claude\skills\website-analyzer\scripts\report_builder.py" \
  --crawl-data "<dossier_output>/crawl_results.json" \
  --scores "<fichier_scores>" \
  --output "<rapport_final.md>"
```

---

### Étape 8 — Envoi PDF

Invoquer le skill `pdf-report-gen` OU envoyer directement :

```bash
python "C:\Users\Alexandre collenne\.claude\tools\send_report.py" --file "<rapport_final.md>" "Audit Web — [Nom du site]" acollenne@gmail.com
```

---

## RÈGLES CRITIQUES

1. **TOUJOURS crawler avant d'analyser** — Ne jamais analyser un site sans avoir crawlé ses pages
2. **TOUJOURS demander le mode A/B/C** — Sauf si l'utilisateur a déjà précisé ce qu'il veut
3. **TOUJOURS lire les fichiers agents/ et references/** — Chaque agent doit avoir ses instructions complètes
4. **Screenshots obligatoires** — L'analyse visuelle nécessite des captures réelles, pas du HTML brut seul
5. **Scores quantifiés** — Chaque dimension DOIT avoir un score /10 justifié par des constats précis
6. **Recommandations actionnables** — Pas de "améliorer le design" → plutôt "réduire le nombre de polices de 5 à 2, utiliser une hiérarchie typographique cohérente"
7. **Sources et preuves** — Chaque constat doit être appuyé par une observation concrète (screenshot, extrait HTML, métrique)
8. **Benchmark quand possible** — Comparer avec les standards du secteur et/ou les concurrents
9. **Pas d'hallucination** — Si une donnée n'est pas disponible (analytics, trafic), le dire explicitement
10. **Timeout** — Si le crawl dépasse 15 min, arrêter et analyser ce qui a été collecté

---

## INTÉGRATION DEEP-RESEARCH

Ce skill est invocable par `deep-research` quand le domaine détecté est "site web / audit web".

**Déclencheurs automatiques dans deep-research :**
- L'utilisateur fournit une URL de site web
- Mots-clés : "analyse site", "audit web", "que penses-tu du site", "évalue ce site"
- Demande de comparaison de sites web

**Retour à deep-research :**
- Le rapport final (Markdown) est retourné pour intégration dans le pipeline QA + PDF
- Les scores sont retournés pour le résumé exécutif de deep-research

---

## DÉPENDANCES

```bash
pip install playwright beautifulsoup4 Pillow cssutils
playwright install chromium
```

---

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Le HTML brut suffit pour analyser le design" | Sans screenshots Playwright, l'analyse visuelle est IMPOSSIBLE. Toujours crawler d'abord. |
| "Un seul agent peut tout analyser" | 5 agents spécialisés existent pour une raison. Chaque domaine a ses propres critères et heuristiques. |
| "Le site semble bon, pas besoin de scorer" | TOUJOURS scorer chaque dimension /10 avec justification. L'intuition n'est pas une métrique. |
| "Le fallback WebFetch donne les mêmes résultats" | WebFetch ne rend pas le JavaScript. Les éléments dynamiques seront ABSENTS. Toujours signaler la qualité des données. |

## RED FLAGS — STOP

- Analyse lancée sans crawl préalable → STOP, crawler d'abord
- Agent lancé sans son fichier de référence → STOP, lire agents/ et references/
- Score /10 sans constat factuel justifiant la note → STOP, documenter les preuves

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Invoqué par | `deep-research` (domaine "site web") |
| Rapport PDF | `pdf-report-gen` |
| Validation qualité | `qa-pipeline` |
| Feedback utilisateur | `feedback-loop` |
| RETEX | `retex-evolution` |

## ÉVOLUTION

Après chaque audit web :
- Si le crawler échoue sur un type de site → améliorer le script ou ajouter des headers
- Si un agent produit des scores incohérents → revoir ses heuristiques dans references/
- Si une dimension manque (ex: performance Core Web Vitals) → l'ajouter à la grille

Seuils : si fallback WebFetch > 30% des audits → améliorer la robustesse du crawler Playwright.
