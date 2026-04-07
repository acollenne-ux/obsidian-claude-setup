---
name: PDF Report Gen v2 (07/04/2026)
description: Refonte complete du skill pdf-report-gen et send_report.py — pipeline 5 agents + moteur Playwright + 5 templates + QC + Mermaid + modify_pdf
type: project
---

# Refonte pdf-report-gen v2 — 07/04/2026

## Contexte

Validation utilisateur : "vas y, implemente tout" sur la proposition deep-research benchmark professionnel PDF generation 2026 (P1+P2+P3, 5 templates, Mermaid, PDF/UA).

## Architecture livree

### Pipeline 5 agents (semantique)
Localisation : `~/.claude/skills/pdf-report-gen/agents/`
1. `synthesizer.md` — Donnees brutes -> Markdown structure (sans frontmatter)
2. `designer.md` — Choix template + frontmatter YAML (KPIs/classification/version)
3. `visualizer.md` — chart_generator + Mermaid + KPI cards
4. `composer.md` — Assemblage final du fichier .md
5. `reviewer.md` — QC post-PDF avec grille decisionnelle (qc_ok, pages, taille, ...)

### Moteur technique modulaire
Localisation : `~/.claude/tools/pdf_engine/`
- `__init__.py` — Expose render_pdf, list_templates, check_pdf_quality, parse_markdown_document
- `markdown_parser.py` (~280 l) — Parser YAML maison + extraction TOC/footnotes/sources
- `components.py` (~220 l) — HTML cover/KPIs/callouts/footnotes
- `mermaid.py` (~90 l) — Rendu mmdc + cache + fallback
- `renderer.py` (~650 l) — Pipeline MD->HTML->PDF (Playwright + WeasyPrint fallback)
- `quality_check.py` (~150 l) — 8 metriques QC (pages, taille, texte, bookmarks, lisibilite, ...)

### Templates CSS
Localisation : `~/.claude/tools/pdf_engine/templates/`
- `base.css` — Styles communs (@page, .cover-page, .kpi-dashboard, .callout, ...)
- `executive.css` — Georgia serif, aere
- `financial.css` — Dense, bleu+vert/rouge, KPI prominent
- `technical.css` — Teal, monospace, code highlight
- `research.css` — Cambria serif, footnotes APA prominentes
- `minimal.css` — Helvetica N&B strict

### Templates briefs (semantiques)
Localisation : `~/.claude/skills/pdf-report-gen/templates/`
- `executive.md`, `financial.md`, `technical.md`, `research.md`, `minimal.md`
- Chaque brief : audience, style, quand utiliser, structure, KPIs typiques, anti-patterns, exemples

### CLI léger
- `~/.claude/tools/send_report.py` v3 (refactore, 100% backward compatible)
  - Nouveaux flags : `--template`, `--no-cover`, `--check-quality`, `--pdf-ua`, `--no-email`, `--output-dir`
  - Auto-organisation `reports/AAAA-MM/`
  - `auto_select_template()` selon contenu
- `~/.claude/tools/modify_pdf.py` (NOUVEAU) — Subcommands: merge, split, extract, watermark, rotate, metadata, info

## Choix technique cle : Playwright > WeasyPrint

WeasyPrint a echoue sur Windows (`OSError: cannot load library 'libgobject-2.0-0'`) car GTK/Pango non installes. Pivot vers Playwright (deja installe v1.58.0 pour flyer-creator) :
- `detect_engine()` retourne 'playwright' en priorite, fallback 'weasyprint'
- `render_html_to_pdf_playwright()` via `sync_playwright()` + `page.pdf(format='A4', print_background=True, prefer_css_page_size=True)`
- Rendu Chromium fidele -> CSS moderne, gradients, webfonts, flexbox parfait

## Test de validation

Demo PDF genere : `C:/tmp/demo_pdf_v2.md` -> 6 pages, 239 KB, qc_ok=True, 5891 chars extractibles. Email envoye avec succes a acollenne@gmail.com.

## Backups

- `~/.claude/skills/pdf-report-gen/SKILL.md.bak_v1_20260407`
- `~/.claude/tools/send_report.py.bak_v1_20260407`

## Why
Repondre a l'instruction CLAUDE.md "envoi automatique par email en PDF — TOUJOURS" avec un niveau professionnel institutionnel : KPIs, footnotes, callouts, Mermaid, syntax highlighting, QC automatique, 5 templates differentiés.

## How to apply
- TOUJOURS utiliser `send_report.py --file rapport.md` (jamais inline)
- Choisir le template selon l'audience (cf table de decision dans Designer)
- Activer `--check-quality` pour les rapports importants
- Si echec QC -> renvoyer au Composer (jamais valider en force)
- Pour modifier un PDF existant : `modify_pdf.py [merge|split|watermark|...]`
