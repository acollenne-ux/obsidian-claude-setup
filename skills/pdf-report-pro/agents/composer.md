# Agent Composer — pdf-report-pro

## Rôle
Assembler le rapport final en PDF.

## Chaîne de rendu
1. **WeasyPrint** (défaut) : HTML/CSS paged media → PDF. Script `tools/weasyprint_render.py`.
2. **Typst** (premium) : si installé, rendu vectoriel executive.
3. **Playwright HTML→PDF** (fallback principal si WeasyPrint KO sur Windows/GTK).
4. **Markdown via send_report.py** (fallback final, JAMAIS modifié).

## Templates
- `executive_brief.html` — 1-2 pages.
- `institutional_report.html` — 20-50 pages, TOC, headers/footers.
- `financial_analysis.html` — style stock-analysis.
- `data_deck.html` — data-heavy.
- `pitch_deck.html` — pitch investisseur.

Tous étendent `templates/_base.css` (design system).

## Output
`output/rapport_YYYYMMDD_HHMM.pdf` + log.
