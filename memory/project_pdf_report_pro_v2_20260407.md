---
name: pdf-report-pro v2 refactor
description: Refonte complète du skill pdf-report-pro le 07/04/2026 — Typst moteur principal, baseline grid, accessibilité PDF/UA, 9 phases, checklist 20 critères
type: project
---

# pdf-report-pro v2 — 2026-04-07

Refonte majeure du skill suite à benchmark 2026 (Typst 0.14 vs WeasyPrint vs LaTeX).

## Changements clés
- **Moteur principal** : Typst 0.14+ (PDF/UA tagged natif, 10-100× plus rapide). Fallbacks : WeasyPrint → Playwright → Markdown.
- **Pipeline** : 6 → **9 phases**. Nouveaux agents : `researcher.md` (sourcing isolé), `accessibility_auditor.md` (PDF/UA + WCAG AA), `archivist.md` (versionnement sémantique).
- **Design system v2** : baseline grid 8pt, tokens WCAG AA (`#C1121F` remplace `#E63946` trop clair), typo Inter + Source Serif 4 + JetBrains Mono.
- **Checklist Reviewer** : 15 → **20 critères**, 3 sections (Contenu 50 / Design 30 / Production 20).
- **Nouveaux outils** : `typst_render.py`, `pdf_accessibility_check.py`, `golden_pdf_test.py`, `pdf_versioner.py`.
- **Nouveaux templates Typst** : `_base.typ`, `board_memo.typ`, `quarterly_review.typ`.
- **pdf-report-gen** : archivé (DEPRECATED.md), rediriger vers pdf-report-pro.

## Score audit
92/100 EXCELLENT (vs ~87 avant).

## Dépendance externe
Typst non installé par défaut → `winget install Typst.Typst` pour activer le moteur principal. Fallback WeasyPrint/Playwright sinon.

## Why
Benchmark 2026 : Typst surclasse WeasyPrint sur perf (effondrement >100 pages), LaTeX sur vitesse et déploiement, et apporte PDF/UA tagged natif requis par l'EU Accessibility Act 2025.

## How to apply
Pour tout rapport PDF institutionnel, pdf-report-pro suit désormais 9 phases incluant Researcher (Phase 1.5), Accessibility Auditor (Phase 4.5) et Archivist (Phase 7). Moteur Typst par défaut.
