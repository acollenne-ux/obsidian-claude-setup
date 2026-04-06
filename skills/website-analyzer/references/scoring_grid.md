# Grille de Scoring — Audit Web Professionnel

## Les 12 dimensions d'analyse

| # | Dimension | Agent | Description |
|---|-----------|-------|-------------|
| 1 | Esthétique & Design visuel | UX/UI | Palette, typo, imagerie, mise en page, modernité |
| 2 | UX / Ergonomie / Navigation | UX/UI | Navigation, hiérarchie info, parcours, formulaires |
| 3 | Responsive / Mobile | UX/UI | Adaptation mobile, touch targets, scroll |
| 4 | Identité de marque | Brand | Logo, cohérence visuelle, positionnement, valeurs |
| 5 | SEO technique | Marketing | Balises, URLs, maillage, sitemap, données structurées |
| 6 | Contenu & Copywriting | Marketing | Proposition de valeur, rédaction, preuve sociale |
| 7 | Performance (vitesse) | Marketing | Temps chargement, poids page, Core Web Vitals |
| 8 | Conversion & Tunnel de vente | Conversion | CTAs, tunnel, formulaires, réassurance |
| 9 | Accessibilité (WCAG) | UX/UI | Contraste, alt text, clavier, structure HTML |
| 10 | Conformité (RGPD, mentions) | Conversion | Mentions légales, CGV, cookies, confidentialité |
| **11** | **Sécurité & Infrastructure** | **Tech Infra** | **Headers sécurité, stack technique, config serveur, SSL, robots.txt, sitemap** |
| **12** | **Trackers & Vie privée** | **Tech Infra** | **Cookies, scripts tiers, analytics, consentement pré-chargement** |

---

## Pondération par mode

| Dimension | Mode A (360°) | Mode B (Marketing) | Mode C (Design) |
|-----------|---------------|--------------------|-----------------| 
| Esthétique & Design | 12% | — | 25% |
| UX / Ergonomie | 10% | — | 25% |
| Responsive / Mobile | 8% | — | 15% |
| Identité de marque | 10% | 12% | 20% |
| SEO technique | 8% | 17% | — |
| Contenu & Copywriting | 8% | 17% | — |
| Performance | 7% | 12% | — |
| Conversion & Tunnel | 10% | 17% | — |
| Accessibilité | 5% | — | 15% |
| Conformité | 5% | 8% | — |
| **Sécurité & Infrastructure** | **9%** | **9%** | — |
| **Trackers & Vie privée** | **8%** | **8%** | — |
| **TOTAL** | **100%** | **100%** | **100%** |

---

## Échelle de notation par dimension (score /10)

| Score | Niveau | Description |
|-------|--------|-------------|
| 10 | Exceptionnel | Référence du secteur, innovation, excellence |
| 9 | Excellent | Quasi parfait, best practices appliquées |
| 8 | Très bon | Très bien exécuté, détails mineurs à améliorer |
| 7 | Bon | Solide, quelques axes d'amélioration identifiés |
| 6 | Correct | Dans la moyenne, rien de remarquable |
| 5 | Passable | Fonctionnel mais perfectible sur plusieurs points |
| 4 | Insuffisant | Problèmes notables impactant l'expérience |
| 3 | Médiocre | Défauts majeurs, révision nécessaire |
| 2 | Mauvais | Fondamentalement défaillant |
| 1 | Critique | Quasi inutilisable ou totalement non conforme |

---

## Score global

**Calcul :** Score global = Σ (score_dimension × poids_dimension) × 10

**Échelle globale (/100) :**

| Score | Lettre | Interprétation | Recommandation |
|-------|--------|---------------|----------------|
| 90-100 | A+ | Excellent — référence du secteur | Optimisations mineures |
| 80-89 | A | Très bon — bien au-dessus de la moyenne | Quelques améliorations ciblées |
| 70-79 | B | Bon — axes d'amélioration identifiés | Plan d'optimisation recommandé |
| 60-69 | C | Correct — travail significatif nécessaire | Refonte partielle conseillée |
| 50-59 | D | Insuffisant — problèmes majeurs | Refonte partielle urgente |
| 0-49 | F | Critique — refonte nécessaire | Refonte majeure recommandée |

---

## Matrice de priorisation des recommandations

| Priorité | Impact | Effort | Action |
|----------|--------|--------|--------|
| **P1 — Quick Wins** | Fort (≥+1 point) | Faible (< 1 jour) | Faire immédiatement |
| **P2 — Stratégique** | Fort (≥+1 point) | Élevé (> 1 semaine) | Planifier en priorité |
| **P3 — Amélioration** | Moyen (+0.5 point) | Faible (< 1 jour) | Intégrer au fil de l'eau |
| **P4 — Backlog** | Faible (<+0.5) | Élevé (> 1 semaine) | Reporter ou ignorer |

---

## Règles de scoring

1. **Jamais de 10/10 par défaut** — un 10 signifie l'excellence absolue, à justifier
2. **Score ≤ 3 = alerte rouge** — signaler comme problème critique dans le rapport
3. **Différence > 3 points entre dimensions** — signaler le déséquilibre
4. **Arrondir au 0.5 près** — utiliser des demi-points (7.5/10) si nécessaire
5. **Justifier CHAQUE score** — minimum 2 constats (positif + négatif) par dimension
