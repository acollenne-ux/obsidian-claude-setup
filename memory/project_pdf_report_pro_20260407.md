# Projet — pdf-report-pro (2026-04-07)

Refonte de `pdf-report-gen` en `pdf-report-pro`, skill de génération de rapports PDF niveau McKinsey/BCG/Goldman Sachs.

## Architecture
- 6 phases : Strategist → Storyliner → Synthesizer → Visualizer → Composer → Reviewer
- 5 templates HTML/CSS : `executive_brief`, `institutional_report`, `financial_analysis`, `data_deck`, `pitch_deck`
- Design system institutionnel : Inter + IBM Plex + Source Serif, primaire `#0B3D91`, accent `#E63946`, Tufte strict
- Checklist McKinsey 15 critères dans `references/checklist_mckinsey.md`

## Moteurs de rendu
1. WeasyPrint (défaut) — **KO sur Windows sans GTK**
2. Playwright HTML→PDF (fallback principal, fonctionnel)
3. Typst (premium, optionnel)
4. Markdown via `send_report.py` (fallback final, jamais modifié)

## Audit
Score : **97/100** (EXCELLENT).

## Backup
`~/.claude/skills/pdf-report-gen.bak_20260407` (original conservé).

## Déploiement
- Invocation via `deep-research` Phase 4 étape 4.
- Mot-clés : rapport, PDF, livrable, executive, institutional.

## Action utilisateur restante
Installer GTK+3 Windows pour activer WeasyPrint natif (sinon Playwright suffit).
