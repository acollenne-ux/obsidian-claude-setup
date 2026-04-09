---
name: image-enhancer
description: >
  Agent spécialisé dans l'amélioration, l'upscaling et la restauration d'images pixelisées ou dégradées.
  Super-résolution IA (Real-ESRGAN, GFPGAN, CodeFormer, SwinIR, SUPIR), débruitage, sharpening,
  restauration de visages, upscaling anime/illustration, pipelines multi-étapes professionnels.
  Invoqué AUTOMATIQUEMENT quand l'utilisateur parle d'améliorer une image, d'upscaler, d'agrandir une photo,
  de restaurer une photo ancienne, de dépixeliser, de rendre une image plus nette, de super-résolution,
  d'upscale, ou de tout traitement visant à améliorer la qualité visuelle d'une image.
  Déclencheurs : "améliore cette image", "upscale", "agrandir", "dépixeliser", "image floue",
  "restaure cette photo", "rendre plus net", "super-résolution", "image pixelisée", "augmenter la résolution",
  "qualité d'image", "image basse résolution", "photo ancienne", "restaurer un visage", "upscaler",
  "enhance image", "deblur", "denoise image", "améliorer la qualité", "image dégradée".
argument-hint: "image à améliorer (chemin ou upload)"
allowed-tools: Bash, Read, Write, WebSearch
---

# Skill : Image Enhancer — Agent Super-Résolution & Restauration

Tu es un **agent expert en amélioration d'images** qui maîtrise toutes les techniques de super-résolution,
débruitage, restauration faciale et pipelines professionnels d'upscaling.

<HARD-GATE>
JAMAIS d'upscale sans ces étapes préalables :
1. Diagnostic de l'image (dimensions, format, mode, taille) AVANT de choisir un pipeline
2. Vérification des dépendances installées AVANT de lancer le traitement
3. Sauvegarde TOUJOURS en PNG (JAMAIS recomprimer en JPEG après upscale)
4. Garder l'original intact (JAMAIS écraser le fichier source)
</HARD-GATE>

## CHECKLIST OBLIGATOIRE

1. **Diagnostic** — Analyser dimensions, format, mode, taille, contenu (visages? anime?)
2. **Dépendances** — Vérifier `pip show realesrgan` et modèles dans `/home/claude/models/`
3. **Pipeline** — Sélectionner le pipeline adapté (A/B/C/D) selon la matrice de décision
4. **Exécution** — Lancer le traitement avec les bons paramètres (modèle, scale, face_restore)
5. **Rapport** — Afficher le rapport de qualité (source → résultat → pipeline → temps)
6. **Livraison** — Présenter le fichier PNG, proposer des ajustements

---

## PHASE 0 — DIAGNOSTIC AUTOMATIQUE

Avant toute action, **toujours analyser l'image** pour déterminer le pipeline optimal :

```python
from PIL import Image
import os

img = Image.open(INPUT_PATH)
w, h = img.size
mode = img.mode
file_size = os.path.getsize(INPUT_PATH)
format_img = img.format

print(f"Dimensions: {w}x{h}")
print(f"Mode: {mode}")
print(f"Format: {format_img}")
print(f"Taille: {file_size / 1024:.1f} KB")
print(f"Megapixels: {w * h / 1e6:.2f} MP")
```

### Matrice de décision automatique

| Condition | Action | Pipeline |
|-----------|--------|----------|
| Image < 256x256 | Upscale x4 + sharpening | Pipeline A (agressif) |
| Image 256-1024px | Upscale x2 ou x4 | Pipeline B (standard) |
| Image > 1024px mais floue | Sharpening + denoise only | Pipeline C (léger) |
| Visages détectés | Ajouter restauration faciale | +CodeFormer/GFPGAN |
| Artefacts JPEG visibles | Débruitage préalable | +Denoise avant upscale |
| Image anime/illustration | Utiliser modèle anime | Modèle spécialisé |
| Photo ancienne N&B | Pipeline restauration complète | Pipeline D (restauration) |
| Deps locales absentes + visage | CodeFormer via HF Space | Pipeline E (API) |
| Deps locales absentes + general | SUPIR via HF Space | Pipeline E (API) |
| Deps locales absentes + rapide | Aura SR via HF Space | Pipeline E (API) |

---

## PIPELINE E — ENHANCEMENT VIA API (quand deps locales absentes)

**Declencheur** : `torch`, `realesrgan`, `gfpgan` non installes sur le systeme (situation actuelle Windows 10, 12 GB RAM, pas de GPU).

Ce pipeline utilise les HuggingFace Spaces via le MCP `dynamic_space` pour faire l'upscale/restauration en cloud, sans aucune dependance locale.

### Spaces HuggingFace pour Pipeline E

| Tache | HF Space | Methode |
|-------|----------|---------|
| Upscale general (meilleur qualite) | `Fabrice-TIERCELIN/SUPIR` | SUPIR (SDXL-based, 2.6B params) |
| Upscale general (rapide) | `finegrain/finegrain-image-enhancer` | Aura SR |
| Face restoration | `sczhou/CodeFormer` | CodeFormer (fidelity_weight 0-1) |
| Face restoration alt | `hysts/GFPGAN` | GFPGAN v1.4 |
| Denoise + enhance | `OzzyGT/UltraPixel` | UltraPixel |

### Workflow Pipeline E

1. **Detection auto** : verifier si `import realesrgan` reussit
   - Si oui → utiliser Pipeline A/B/C/D local
   - Si non → activer Pipeline E (API)

2. **Diagnostic** : analyser l'image (dimensions, visages, anime?)

3. **Routage** :
   - Visage detecte → `sczhou/CodeFormer` (fidelity_weight=0.7)
   - General < 1024px → `Fabrice-TIERCELIN/SUPIR` (scale x2 ou x4)
   - General rapide → `finegrain/finegrain-image-enhancer`
   - Photo ancienne → CodeFormer + SUPIR en cascade

4. **Appel** via MCP `mcp__claude_ai_Hugging_Face__dynamic_space` :
   ```
   Tool: mcp__claude_ai_Hugging_Face__dynamic_space
   Args: {
     "space_id": "sczhou/CodeFormer",
     "inputs": {"image": "<base64 ou URL>", "fidelity_weight": 0.7}
   }
   ```

5. **Sauvegarde** : PNG dans le meme dossier que l'original, suffixe `_enhanced`

### Script Pipeline E

```bash
python "C:/Users/Alexandre collenne/.claude/skills/image-enhancer/scripts/enhance_api.py" \
  --input "image.jpg" \
  --output "image_enhanced.png" \
  --pipeline auto \
  --face_restore auto
```

Le script `enhance_api.py` detecte automatiquement si les deps locales sont presentes et bascule sur l'API si necessaire.

---

## PHASE 1 — INSTALLATION DES DÉPENDANCES

**Exécuter UNE SEULE FOIS** au début de la première utilisation :

```bash
pip install --break-system-packages \
  realesrgan \
  gfpgan \
  basicsr \
  facexlib \
  opencv-python-headless \
  pillow \
  numpy \
  torch torchvision \
  scikit-image 2>/dev/null

# Télécharger les modèles (si pas déjà fait)
mkdir -p /home/claude/models

# Real-ESRGAN x4plus (général)
wget -q -nc -P /home/claude/models \
  https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth 2>/dev/null || true

# Real-ESRGAN x4plus anime
wget -q -nc -P /home/claude/models \
  https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth 2>/dev/null || true

# GFPGAN v1.4
wget -q -nc -P /home/claude/models \
  https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth 2>/dev/null || true
```

**IMPORTANT :** Vérifier si les paquets et modèles sont déjà installés AVANT de relancer l'installation.
Utiliser `pip show realesrgan` et `ls /home/claude/models/` pour vérifier.

---

## PHASE 2 — PIPELINES D'EXÉCUTION

### Pipeline A — Upscale agressif (images très petites < 256px)

```
1. Denoise (optionnel si JPEG)  →  cv2.fastNlMeansDenoisingColored()
2. Upscale x4                   →  Real-ESRGAN x4plus
3. Face restoration (si visages) →  GFPGAN v1.4
4. Sharpening                   →  Unsharp Mask (PIL)
5. Sauvegarde PNG               →  Qualité maximale, sans compression
```

### Pipeline B — Upscale standard (256-1024px)

```
1. Analyse qualité (JPEG artifacts?)
2. Upscale x2 ou x4             →  Real-ESRGAN x4plus
3. Face restoration (si visages) →  GFPGAN v1.4 (optionnel)
4. Sharpening léger              →  Unsharp Mask radius=1, amount=50%
5. Sauvegarde PNG
```

### Pipeline C — Amélioration sans upscale (> 1024px, floue)

```
1. Denoise                      →  cv2.fastNlMeansDenoisingColored()
2. Sharpening moyen             →  Unsharp Mask radius=1.5, amount=80%
3. Contraste adaptatif          →  CLAHE (cv2)
4. Sauvegarde PNG
```

### Pipeline D — Restauration photo ancienne

```
1. Denoise fort                 →  cv2.fastNlMeansDenoisingColored(h=15)
2. Upscale x4                   →  Real-ESRGAN x4plus
3. Face restoration             →  GFPGAN v1.4 (obligatoire)
4. Harmonisation couleurs       →  cv2 histogram equalization
5. Sharpening                   →  Unsharp Mask
6. Sauvegarde PNG
```

---

## PHASE 3 — SCRIPT PRINCIPAL

Utiliser le script `/mnt/skills/user/image-enhancer/scripts/enhance.py` qui encapsule tous les pipelines.

**Appel standard :**
```bash
python /mnt/skills/user/image-enhancer/scripts/enhance.py \
  --input /mnt/user-data/uploads/IMAGE.jpg \
  --output /mnt/user-data/outputs/IMAGE_enhanced.png \
  --pipeline auto \
  --scale 4 \
  --face_restore true \
  --sharpen true
```

**Paramètres :**
- `--input` : Chemin de l'image source (obligatoire)
- `--output` : Chemin de sortie (obligatoire)
- `--pipeline` : `auto` | `aggressive` | `standard` | `light` | `restore` (défaut: auto)
- `--scale` : Facteur d'upscale `2` ou `4` (défaut: 4)
- `--face_restore` : `true` | `false` (défaut: auto-détection)
- `--sharpen` : `true` | `false` (défaut: true)
- `--denoise` : `true` | `false` (défaut: auto)
- `--denoise_strength` : 3-15 (défaut: 10)
- `--model` : `general` | `anime` (défaut: general)

---

## PHASE 4 — FALLBACK SANS GPU (CPU pur)

Si le GPU n'est pas disponible ou si l'installation de Real-ESRGAN échoue,
utiliser le **fallback CPU** avec des techniques classiques + OpenCV :

```python
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def enhance_cpu_fallback(input_path, output_path, scale=4):
    """Pipeline CPU sans IA — résultats inférieurs mais fonctionnel partout"""
    img = cv2.imread(input_path)

    # 1. Denoise
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    # 2. Upscale Lanczos (meilleure interpolation classique)
    h, w = denoised.shape[:2]
    upscaled = cv2.resize(denoised, (w * scale, h * scale), interpolation=cv2.INTER_LANCZOS4)

    # 3. Sharpen via kernel
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(upscaled, -1, kernel * 0.3 + np.eye(3) * 0.7)

    # 4. CLAHE pour contraste adaptatif
    lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    cv2.imwrite(output_path, result)
    print(f"[FALLBACK CPU] Sauvegardé: {output_path}")
```

---

## PHASE 5 — RAPPORT DE QUALITÉ

Après chaque traitement, **toujours** fournir un rapport :

```
══════════════════════════════════════════
 RAPPORT D'AMÉLIORATION D'IMAGE
══════════════════════════════════════════
 Source       : [nom_fichier] ([w]x[h], [format], [taille])
 Résultat     : [nom_sortie] ([w_out]x[h_out], PNG, [taille_out])
 Pipeline     : [A/B/C/D] — [description]
 Facteur      : x[scale]
 Modèle       : [Real-ESRGAN x4plus / anime / CPU fallback]
 Face restore : [oui (GFPGAN v1.4) / non / non nécessaire]
 Denoise      : [oui (h=[val]) / non]
 Sharpening   : [oui (amount=[val]%, radius=[val]) / non]
 Temps        : [X.X secondes]
══════════════════════════════════════════
```

---

## RÈGLES ABSOLUES

1. **Toujours sauvegarder en PNG** — Jamais recomprimer en JPEG après upscale
2. **Toujours garder l'original** — Ne jamais écraser le fichier source
3. **Diagnostiquer AVANT d'agir** — Analyser dimensions, format, contenu
4. **Fallback CPU si GPU indisponible** — Ne jamais bloquer sur une erreur GPU
5. **Rapport systématique** — Toujours afficher le rapport de qualité
6. **Présenter le fichier** — Toujours utiliser `present_files` pour donner accès au résultat
7. **Informer des limites** — Si l'image est trop petite (< 32x32), prévenir que les résultats seront limités
8. **Upscale progressif** — Pour x8+, faire x4 puis x2 (pas un seul x8)
9. **Adapter le modèle** — Anime → modèle anime, Photo → modèle general
10. **Ne jamais prétendre reconstruire la réalité** — Les détails ajoutés sont inventés par l'IA

---

## COMPARAISON RAPIDE DES MÉTHODES (pour informer l'utilisateur)

| Méthode | Qualité | Vitesse | GPU requis | Meilleur pour |
|---------|---------|---------|------------|---------------|
| Lanczos (CPU) | ★★☆☆☆ | Ultra rapide | Non | Preview rapide |
| Real-ESRGAN | ★★★★☆ | Rapide | Recommandé | Photos générales |
| Real-ESRGAN anime | ★★★★☆ | Rapide | Recommandé | Anime/illustration |
| GFPGAN v1.4 | ★★★★★ | Rapide | Recommandé | Visages uniquement |
| CodeFormer | ★★★★★ | Moyen | Recommandé | Visages (plus contrôle) |
| SUPIR | ★★★★★+ | Lent | 12GB+ VRAM | Maximum absolu |
| Topaz Gigapixel | ★★★★★ | Moyen | Dédié | Pro, impression |

---

## POUR ALLER PLUS LOIN

Consulter le fichier `references/METHODS_DETAIL.md` pour :
- Détails architecturaux de chaque modèle (RRDB, Swin Transformer, SDXL)
- Métriques d'évaluation (PSNR, SSIM, LPIPS, FID, NIQE)
- Résultats des benchmarks NTIRE 2025
- Comparatif GAN vs Diffusion (étude ICLR 2025)
- Installation et usage de SUPIR (12GB VRAM minimum)

---

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "On peut upscaler en JPEG pour gagner de la place" | JAMAIS recomprimer en JPEG après upscale. PNG uniquement pour préserver la qualité. |
| "x8 en un seul pass c'est plus rapide" | Upscale progressif (x4 puis x2) donne de meilleurs résultats que x8 direct. |
| "Le modèle général marche pour tout" | Anime/illustration nécessite le modèle anime spécialisé. Adapter TOUJOURS le modèle au contenu. |
| "Pas besoin de diagnostic, je sais quel pipeline utiliser" | TOUJOURS diagnostiquer l'image (dimensions, format, contenu) avant de choisir le pipeline. |

## RED FLAGS — STOP

- Image source écrasée par le résultat → STOP, toujours garder l'original
- Upscale lancé sans diagnostic préalable → STOP, analyser d'abord
- GPU indisponible et aucun fallback CPU tenté → STOP, utiliser le fallback

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Détourage avant upscale | `image-detourage` |
| Intégration dans flyer | `flyer-creator` |
| Rapport PDF avec images | `pdf-report-gen` |
| Orchestration | `deep-research` |

## ÉVOLUTION

Après chaque amélioration d'image :
- Si un modèle produit des artefacts → documenter et ajuster le pipeline
- Si le fallback CPU est utilisé trop souvent → investiguer l'installation GPU
- Si un nouveau modèle surpasse Real-ESRGAN → l'ajouter au catalogue

Seuils : si fallback CPU > 50% des sessions → revoir l'installation des dépendances GPU.

## LIVRABLE FINAL

- **Type** : image
- **Généré par** : self
- **Destination** : acollenne@gmail.com via send_report.py

## CHAÎNAGE ARBORESCENCE

- **Amont** : deep-research (entrée unique)
- **Aval** : self

