# Projet — ppt-creator (2026-04-07)

Nouveau skill de génération de présentations `.pptx` éditables niveau McKinsey/BCG/Sequoia.

## Architecture
- 6 phases : Strategist → Storyliner (**ghost deck validé utilisateur**) → Synthesizer → Visualizer → Composer → Reviewer
- 5 templates : `executive_deck`, `institutional_deck`, `financial_analysis_deck`, `data_deck`, `pitch_deck`
- Règles McKinsey strictes : action title 5-15 mots, 1 slide = 1 idée, MECE, pyramid principle Minto

## Moteurs
1. **python-pptx** (principal) — installé OK (v1.0.2)
2. Marp CLI (draft)
3. Canva MCP (premium via image-studio)

## Export
- `.pptx` toujours (éditable)
- `.pdf` via LibreOffice headless si dispo
- Envoi email via `send_report.py`

## Audit
Score : **97/100** (EXCELLENT, cible 88 largement dépassée).

## Déploiement
- Invocation via `deep-research` Phase 4 étape 4bis.
- Mots-clés : présentation, slides, ppt, pptx, deck, pitch, powerpoint.

## Gate critique
Phase 2 Storyliner affiche la table Markdown du ghost deck et **ATTEND GO utilisateur** avant Phase 3. Pas de bypass.
