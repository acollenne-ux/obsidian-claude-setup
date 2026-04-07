---
name: Skills carrière (CV + lettre) 07/04
description: Création des skills cv-creator et cover-letter-creator (Typst + HTML/Playwright + JSON Resume), positionnés comme Skills domaine auto-invoqués
type: project
---

# Skills Carrière — 2026-04-07

Création de deux skills jumeaux pour générer CV et lettres de motivation institutionnels.

## Why
Aucun skill carrière n'existait. Benchmark 2026 (8 WebSearch, 10 sources) → stack retenu :
JSON Resume (data) → Typst modern-cv (moteur principal ATS-safe) + HTML/CSS + Playwright (créatif) + pandoc (DOCX strict).

## How to apply
- **cv-creator** : auto-invoqué sur "CV / résumé / curriculum vitae / tailoring offre"
  - Pipeline 6 phases : parse → contexte pays → tailoring JD → template → rendu Typst/HTML → QA ATS 12 points
  - 6 templates : harvard, jakes, mckinsey, europass, modern, tech-onepage
  - Règles pays critiques (photo OUI Allemagne, NON US/UK ; longueur 1-2 pages)
- **cover-letter-creator** : auto-invoqué sur "lettre de motivation / cover letter"
  - Pipeline 5 phases : parse JD + recherche entreprise → framework (AIDA/Storytelling/Problem-Solution/Classique) → draft 250-350 mots → alignement visuel CV → rendu
  - Lit `C:\tmp\cv_<nom>.json` pour cohérence visuelle (police, palette, header)
- **Coordination** : les deux skills partagent les fonts, l'accent couleur et le header pour livrer un pack CV+lettre cohérent
- **Position arborescence** : Skills domaine (au même niveau que stock-analysis, flyer-creator, image-studio), invoqués directement OU dispatché par `deep-research` quand il détecte un contexte carrière
- **Anti-hallucination critique** : JAMAIS inventer expérience/diplôme/fait sur l'entreprise. Tailoring = reformulation, pas fabrication. À valider via `qa-pipeline`.

Sources benchmark : Harvard template, Jake's resume, AltaCV, Typst modern-cv, JSON Resume, Jobscan ATS rules, Europass 2026, ResumeAdapter cover letter format.
