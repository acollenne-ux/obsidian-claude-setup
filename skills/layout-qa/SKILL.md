---
name: layout-qa
description: "Porte QA visuelle obligatoire avant livraison (PDF/PPTX/image/flyer/diagramme). Rasterize + geometric check + vision critique Gemini. Verdict PASS/FIX/FAIL + boucle correction. Use when: avant envoi livrable Couche 4."
argument-hint: "<chemin_livrable> [--brief <chemin_brief>] [--max-iter 3]"
domain: qa
livrable: PDF
layer: L5
generator: pdf-report-pro
allowed-tools:
  - Bash
  - Read
  - Write
  - Agent
---

# Layout-QA — Porte de contrôle visuelle de Couche 4

Tu es la **porte de qualité visuelle obligatoire** entre un générateur de livrable (Couche 4) et l'envoi final. Aucun PDF/PPT/image/flyer/diagramme ne sort sans ton verdict `PASS`.

<HARD-GATE>
Règles non-négociables :

1. **OBLIGATOIRE avant tout envoi** de livrable visuel (email, fichier utilisateur, upload).
2. **Invoquée par le skill générateur lui-même** à la fin de son pipeline, avant le Reviewer final. Grille de scoring obligatoire.
3. **Verdict impératif** : PASS → autorisé • FIX → renvoyer au Composer avec corrections précises (bbox, éléments à repositionner) • FAIL → escalade utilisateur avec screenshots annotés.
4. **Max 3 itérations** FIX → re-render → re-check. Au-delà, escalade. Seuil vision scoring : ≥ 85/100 pour PASS.
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
- Analyse : clipping visuel, collisions, fidélité intention↔rendu, lisibilité, hiérarchie — grille de scoring 10 dimensions
- Sortie : scoring /100 + anomalies localisées (page, zone, recommandation de correction) fusionnées avec Phase 2

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

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "C'est juste un brouillon, pas besoin de QA" | Les brouillons deviennent les livrables. TOUJOURS passer par layout-qa. |
| "Le contenu est bon, la mise en page on s'en fiche" | Un bon contenu mal mis en page = non livrable. Forme ET fond. |
| "Ça passe à l'œil, pas besoin du check géométrique" | L'œil rate les overflows de 2px qui deviennent des clippings à l'impression. |
| "3 itérations c'est trop, je livre en l'état" | Max 3 itérations = protection, pas un inconvénient. Si 3 FIX → le problème est structurel, escalader. |
| "Le skill appelant gère déjà la qualité" | Layout-qa est la SEULE porte de sortie. Le skill appelant gère le contenu, layout-qa gère le rendu. |
| "Gemini vision est overkill pour un PDF simple" | Un PDF simple peut avoir des overlaps invisibles. La vision multimodale détecte ce que le code ne peut pas. |

## TRIGGERS / NO-TRIGGERS (testabilité)

### Scénarios TRIGGER
| Prompt / Contexte | Attendu |
|-------------------|---------|
| pdf-report-pro vient de générer un PDF | layout-qa invoqué automatiquement |
| ppt-creator a fini un .pptx | layout-qa invoqué avant envoi |
| "vérifie la mise en page de ce document" | layout-qa activé |
| image-studio Phase 8 — QA final | layout-qa invoqué |

### Scénarios NO-TRIGGER
| Prompt | Skill correct |
|--------|--------------|
| "Crée un PDF sur l'analyse de Tesla" | pdf-report-pro (puis layout-qa en fin de pipeline) |
| "Améliore la qualité de cette image" | image-enhancer |
| "Analyse ce site web" | website-analyzer |

## ÉVOLUTION

Ce skill s'auto-améliore via RETEX. Après chaque session :

**Métriques à tracker** :
- Taux PASS au 1er passage (cible : >70%)
- Anomalies les plus fréquentes (overflow? clipping? margin?) → enrichir les règles géométriques
- Nombre moyen d'itérations FIX → si >2 régulier, renforcer les Composers amont

**Actions d'amélioration** :
- Nouvelle catégorie d'anomalie détectée → l'ajouter dans `layout_check.py`
- Faux positifs récurrents → ajuster les seuils de détection
- Nouveau type de livrable supporté → ajouter le backend de rasterisation

```bash
python "C:/Users/Alexandre collenne/.claude/tools/retex_manager.py" save layout_qa \
  --quality [score] --tools-used "[rasterize,layout_check,gemini_vision]" --notes "[leçons]"
```

## LIMITATIONS CONNUES

- PPTX → rasterisation via HTML mock = approximation (pas pixel-perfect PowerPoint). Suffisant pour détecter overflow/clipping majeurs.
- Gemini vision : rate limit ~60 req/min. Batch par lots de 10 pages max.
- Max 3 itérations FIX : au-delà, problème structurel → escalade plutôt que boucler.
