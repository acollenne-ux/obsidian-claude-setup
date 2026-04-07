# Checklist McKinsey — pdf-report-pro v2 (20 critères)

Score pondéré /100. Seuil GO : ≥ 85.

## Contenu (Minto / pyramid principle) — 50 pts

| # | Critère | Poids | Description |
|---|---|---|---|
| 1 | Key message clair | 8 | Une seule phrase résume la conclusion en page 1 |
| 2 | Pyramid principle | 8 | Conclusion d'abord, arguments ensuite, preuves après |
| 3 | MECE | 6 | Arguments mutuellement exclusifs et collectivement exhaustifs |
| 4 | Action titles | 8 | Chaque section porte un action title 5-15 mots avec verbe |
| 5 | Flux horizontal | 6 | Lecture des seuls titres = histoire cohérente |
| 6 | Sourcing numéroté [N] | 8 | Chaque chiffre lié à une source [1]…[N] vérifiable |
| 7 | Anticipation des objections | 3 | Risques et contre-arguments traités |
| 8 | Recommandations actionnables | 3 | Owners + KPIs + dates |

## Design (Tufte + McKinsey) — 30 pts

| # | Critère | Poids | Description |
|---|---|---|---|
| 9  | Data-ink ratio Tufte | 6 | Pas de 3D, chartjunk, gradients gratuits |
| 10 | Baseline grid 8pt respecté | 4 | Marges, paddings, tailles = multiples de 4/8 |
| 11 | Cohérence visuelle | 4 | Typo, couleurs, marges homogènes |
| 12 | Charts caption + alt-text | 4 | Chaque chart a une caption descriptive ≥ 15 mots |
| 13 | Couleurs WCAG AA (contraste ≥ 4.5:1) | 4 | Audité automatiquement |
| 14 | Cover métadonnées (audience, version, classification) | 4 | YAML cover renseigné |
| 15 | Executive summary 1 page max | 4 | Auto-porteuse, lisible isolée |

## Production (qualité livrable) — 20 pts

| # | Critère | Poids | Description |
|---|---|---|---|
| 16 | Tagged PDF (PDF/UA) | 4 | Lecteurs d'écran compatibles |
| 17 | Score accessibilité ≥ 16/20 | 4 | Via `pdf_accessibility_check.py` |
| 18 | Concision (zéro remplissage) | 3 | Chaque § porte un insight |
| 19 | Zéro faute, zéro approximation | 3 | Relecture pro |
| 20 | Versionnement sémantique + archivé | 6 | Via `pdf_versioner.py`, golden PDF v1.0 |

**Score max = 100. Seuil de livraison = 85.**

## Boucle de correction
- Si score < 85 → identifier critères < 6/10 → relancer phase concernée (Synthesizer / Visualizer / Composer)
- Max 2 itérations
- Si après 2 itérations score < 85 → escalader à l'utilisateur avec gap analysis
