---
name: layout-qa
description: "Porte de contrôle qualité visuelle obligatoire avant livraison de tout rendu (PDF, PPTX, image, flyer, diagramme). Rasterize le livrable, détecte géométriquement les overlaps/clipping/débordements via python-pptx+pdfplumber, puis invoque l'agent visual-layout-critic (Gemini 3 Pro) pour une revue vision multimodale. Verdict PASS/FIX/FAIL + boucle de correction vers le Composer. Use when: un skill de Couche 4 (pdf-report-pro, ppt-creator, flyer-creator, image-studio, cv-creator, cover-letter-creator, idea-to-diagram) vient de produire un livrable et avant tout envoi. Triggers: 'vérifier mise en page', 'contrôle visuel', 'layout qa', 'gate rendu', 'avant livraison'."
argument-hint: "<chemin_livrable> [--brief <chemin_brief>] [--max-iter 3]"
livrable: PDF
layer: L5
generator: pdf-report-pro
---

# Layout-QA — Porte de contrôle visuelle de Couche 4

Tu es la **porte de qualité visuelle obligatoire** entre un générateur de livrable (Couche 4) et l'envoi final. Aucun PDF/PPT/image/flyer/diagramme ne sort sans ton verdict `PASS`.

<HARD-GATE>
Règles non-négociables :

1. **OBLIGATOIRE avant tout envoi** de livrable visuel (email, fichier utilisateur, upload).
2. **Invoquée par le skill générateur lui-même** à la fin de son pipeline, avant le Reviewer final.
3. **Verdict impératif** : PASS → autorisé • FIX → renvoyer au Composer avec corrections précises (bbox, éléments à repositionner) • FAIL → escalade utilisateur avec screenshots annotés.
4. **Max 3 itérations** FIX → re-render → re-check. Au-delà, escalade.
5. **Fidélité au brief** : le rendu doit exprimer ce que l'utilisateur a demandé. Un contenu correct mal mis en page = FIX.
</HARD-GATE>

---

## PIPELINE 4 PHASES (TodoWrite obligatoire)

### Phase 1 — Rasterize
- Entrée : chemin du livrable (`.pdf`, `.pptx`, `.png`, `.jpg`, `.svg`)
- Script : `scripts/rasterize.py <input> --out <dir> --dpi 200`
- Sortie : 1 PNG par page/slide dans `./qa_tmp/<uuid>/page_*.png`
- Backends :
  - PDF → `pdftoppm` si dispo, sinon Playwright (render HTML→PDF→PNG)
  - PPTX → rendu HTML mock + Playwright (pattern pdf-report-pro). **LibreOffice INTERDIT** (cf. memory 2026-04-07).
  - PNG/JPG/SVG → copie directe (SVG via Playwright)

### Phase 2 — Geometric check (déterministe)
- Script : `scripts/layout_check.py <input> --brief <brief.md> --out geom.json`
- Parse : `python-pptx` pour PPTX, `pdfplumber` pour PDF
- Détections :
  - `overflow` : bbox > page bounds
  - `overlap` : intersection non déclarée entre éléments (hors groupes)
  - `clipping` : texte tronqué (anchor hors cadre)
  - `margin_violation` : distance au bord < gutter minimum (8pt baseline)
  - `zorder_suspect` : texte sous une forme opaque
  - `empty_region` : page/slide >60% vide = hiérarchie cassée
- Sortie JSON : `[{page, element_id, issue, severity: low|medium|high|critical, bbox:[x,y,w,h], suggestion}]`

### Phase 3 — Vision critique
- Invoquer l'agent **`visual-layout-critic`** (`agents/visual-layout-critic.md`)
- Entrée : PNG rasterisés + brief original + rapport géométrique Phase 2
- Moteur : `gemini_wrapper.py` existant (image-studio/idea-to-diagram)
- Analyse : clipping visuel, collisions, fidélité intention↔rendu, lisibilité, hiérarchie
- Sortie : score /100 + anomalies localisées (page, zone, correction) fusionnées avec Phase 2

### Phase 4 — Verdict & feedback loop
- Règle de décision :
  - 0 anomalie `critical` ET 0 `high` ET score vision ≥ 85 → **PASS**
  - 1+ `critical` OU score vision < 60 → **FAIL** (escalade utilisateur)
  - Sinon → **FIX**
- Si FIX :
  - Générer un rapport structuré JSON `{verdict, anomalies, corrections}` destiné au Composer du skill appelant
  - Incrémenter `iter` (max 3)
  - Invoquer le Composer avec consignes précises → re-render → retour Phase 1
- Si PASS :
  - Générer rapport d'audit visuel PDF (via `pdf-report-pro` en mode léger avec template `templates/report.html`)
  - Autoriser la livraison
- Si FAIL :
  - Annoter les screenshots (`scripts/annotate.py`)
  - Retourner à l'utilisateur avec explication et propositions

---

## INTERFACE D'APPEL (pour les skills de Couche 4)

```bash
python ~/.claude/skills/layout-qa/scripts/run_gate.py \
    --input <livrable> \
    --brief <brief.md> \
    --caller <nom_skill_appelant> \
    --max-iter 3 \
    --out-report qa_report.json
```

Code de sortie : `0=PASS`, `1=FIX`, `2=FAIL`.

Le skill appelant **DOIT** lire le JSON et agir selon le verdict.

---

## PLACE DANS L'ARBORESCENCE

**Couche 4 — Delivery Gate** (sous-groupe dédié)

```
deep-research → [Core] → [Specialist] → [Delivery generator]
                                              ↓
                                         layout-qa (GATE) ← ce skill
                                         ↑        ↓
                                         └─ FIX ──┘   (max 3)
                                              ↓ PASS
                                         livraison
```

Livrable propre : **rapport PDF d'audit visuel** + livrable original validé.

---

## CROSS-LINKS

- **Amont (skills qui m'invoquent)** : pdf-report-pro, ppt-creator, flyer-creator, image-studio, cv-creator, cover-letter-creator, idea-to-diagram
- **Outils réutilisés** : `gemini_wrapper.py`, Playwright, pdfplumber, python-pptx, pdf-report-pro (rendu rapport)
- **Aval** : feedback-loop (collecte métriques FIX/PASS), retex-evolution (amélioration continue)

---

## LIMITATIONS CONNUES

- PPTX → rasterisation via HTML mock = approximation (pas pixel-perfect PowerPoint). Suffisant pour détecter overflow/clipping majeurs.
- Gemini vision : rate limit ~60 req/min. Batch par lots de 10 pages max.
- Max 3 itérations FIX : au-delà, problème structurel → escalade plutôt que boucler.
