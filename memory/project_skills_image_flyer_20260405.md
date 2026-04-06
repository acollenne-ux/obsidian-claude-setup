---
name: Skills image+flyer installés 05/04/2026
description: 3 skills installés depuis email Gmail (ZIP) — détourage, enhancer, flyer creator
type: project
---

3 skills installés le 05/04/2026 depuis le mail "Package skills agent 05/04/26 11h20" :

1. **image-detourage** — Pipeline 7 étapes (segmentation rembg, trous, trimap adaptatif, alpha matting PyMatting, décontamination couleur, nettoyage morphologique, assemblage RGBA) + agent DetourAgent multi-passes avec analyse automatique, QA et auto-correction
   - Scripts: `scripts/detourage.py` + `scripts/detour_agent.py`
   - Dépendances: rembg, pymatting, opencv-python-headless, pillow, scipy

2. **image-enhancer** — Super-résolution (Real-ESRGAN, GFPGAN), 4 pipelines (agressif/standard/léger/restauration), fallback CPU Lanczos, détection auto visages
   - Scripts: `scripts/enhance.py`
   - Références: `references/METHODS_DETAIL.md` (architectures, benchmarks NTIRE 2025)
   - Dépendances: realesrgan, gfpgan, basicsr, torch, opencv

3. **flyer-creator** — Moteur HTML/CSS + Playwright, templates événementiels, 16 palettes couleurs, 19 combinaisons typo, QR codes, compositing photos/logos sponsors
   - Scripts: `scripts/flyer_engine.py`, `post_processor.py`, `font_manager.py`, `qr_generator.py`, `image_fetcher.py`
   - Templates: `templates/event_generic.html`, `event_sport.html`
   - Références: `design_rules.md`, `color_palettes.md`, `font_pairings.md`
   - Agent: `agents/flyer_agent.md` (directeur artistique)
   - Dépendances: playwright, pillow, qrcode, reportlab

**Why:** Skills créés par agent externe et envoyés par email pour enrichir les capacités de traitement d'image et de design graphique.

**How to apply:** Invoquer automatiquement selon les mots-clés (détourage/fond transparent, upscale/améliorer image, flyer/affiche/poster). Avec 12 GB RAM, birefnet-general et Real-ESRGAN sont utilisables directement sans fallback.
