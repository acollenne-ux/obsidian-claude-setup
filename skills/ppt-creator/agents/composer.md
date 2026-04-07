# Agent Composer — ppt-creator

## Rôle
Assembler le .pptx éditable.

## Moteurs
1. **python-pptx** (principal) via `tools/pptx_builder.py` — sortie .pptx éditable.
2. **Marp CLI** (draft rapide) — Markdown → .pptx.
3. **Canva MCP** via `image-studio` (premium).

## Templates
Générés par `tools/build_templates.py` :
- `executive_deck` (5-10 slides)
- `institutional_deck` (20+)
- `financial_analysis_deck`
- `data_deck`
- `pitch_deck` (15 slides Sequoia/YC)

## Export
- `.pptx` toujours.
- `.pdf` (optionnel) via rendu HTML parallèle + Playwright `page.pdf()`. LibreOffice INTERDIT sur ce poste.
- Fallback : notification au Reviewer.
