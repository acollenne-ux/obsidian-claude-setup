# Référence détaillée — Méthodes de Super-Résolution

## Table des matières
1. Architectures GAN détaillées
2. Modèles de diffusion
3. Transformers pour SR
4. Métriques d'évaluation
5. Benchmarks NTIRE 2025
6. Installation SUPIR (avancé)
7. Comparatif GAN vs Diffusion
8. Troubleshooting courant

---

## 1. Architectures GAN détaillées

### RRDB (Residual-in-Residual Dense Block)
Brique fondamentale d'ESRGAN et Real-ESRGAN.
- 3 Dense Blocks empilés dans chaque Residual Block
- Chaque Dense Block : 5 couches convolutionnelles avec connexions denses
- Pas de Batch Normalization (cause des artefacts)
- Scaling factor β = 0.2 sur les connexions résiduelles

### Real-ESRGAN — Pipeline de dégradation haute-ordre
```
Couche 1 : blur → resize → noise → JPEG compression
Couche 2 : blur → resize → noise → JPEG compression (sinc filter)
```
Chaque couche échantillonne aléatoirement ses paramètres pour simuler
les dégradations réelles (compression multiple, transmission réseau, etc.)

### AESRGAN (2025)
- Ajoute des modules d'attention explicites dans les RRDB
- Channel Attention pour sélectionner les features discriminantes
- Spatial Attention pour focaliser sur les régions haute-fréquence
- Résultats : +0.15 dB PSNR sur CelebA pour les visages

---

## 2. Modèles de diffusion pour SR

### Processus de diffusion
```
Diffusion directe : x_0 → x_1 → ... → x_T (bruit gaussien progressif)
Diffusion inverse : x_T → x_{T-1} → ... → x_0 (débruitage progressif)
```

### SUPIR (Scaling-UP Image Restoration)
- Base : Stable Diffusion XL (SDXL), 2.6 milliards de paramètres
- Dataset : 20 millions d'images HR avec annotations textuelles
- Innovation : contrôle par prompts textuels positifs ET négatifs
- Negative prompts recommandés : "blurry, low quality, noise, artifacts"
- Positive prompts : "high quality, sharp, detailed, 4K"
- Restoration-guided sampling pour préserver la fidélité
- VRAM minimum : 12 GB (avec Juggernaut-XL-v9 comme base)
- Installation : voir section 6

### DiffBIR
- Combine un module de restauration (SwinIR) avec un module de génération (SD)
- Étape 1 : SwinIR nettoie et pré-restaure l'image
- Étape 2 : ControlNet Tile guide la diffusion pour ajouter les détails
- Meilleur pour la restauration "blind" (dégradation inconnue)

### StableSR
- Utilise SD 2.1 avec un module de contrôle spécialisé SR
- Nécessite le checkpoint v2-1_512-ema-pruned
- Problème connu : décalage de couleurs (corrigé par Wavelet Color Fix)
- Tiled Diffusion nécessaire pour les grandes images

---

## 3. Transformers pour SR

### SwinIR (Swin Transformer)
- Fenêtres glissantes (shifted windows) pour self-attention local
- 6 RSTB (Residual Swin Transformer Blocks) par défaut
- Taille de fenêtre : 8×8
- Embedding dimension : 180
- Nombre de heads : 6
- Modèles : SR classique, SR légère, débruitage, suppression artefacts JPEG

### CAAT (Channel Attention and Transformer, 2025)
- Alterne couches CNN et Swin Transformer
- Channel attention injectée dans les deux branches
- Résultats x4 sur Urban100 : +0.09 dB PSNR vs meilleurs concurrents
- Résultats x4 sur Manga109 : +0.30 dB PSNR
- 51% moins de paramètres que SwinIR
- 68% moins de FLOPs (195.6G vs 612.6G pour 1280×720)

### Mamba-SR (State Space Models)
- Alternative au self-attention avec complexité linéaire O(n) vs O(n²)
- Scalable pour les très grandes images
- Adopté par plusieurs équipes au NTIRE 2025

---

## 4. Métriques d'évaluation

### PSNR (Peak Signal-to-Noise Ratio)
```
PSNR = 10 × log10(MAX² / MSE)
```
- MAX = 255 pour images 8-bit
- Plus haut = meilleur (typiquement 25-35 dB pour SR x4)
- Standard pour les benchmarks mais mauvais indicateur de qualité perceptuelle

### SSIM (Structural Similarity Index)
```
SSIM(x,y) = [l(x,y)]^α × [c(x,y)]^β × [s(x,y)]^γ
```
- l = luminance, c = contraste, s = structure
- Range : 0 à 1, plus haut = meilleur
- Meilleur que PSNR pour la qualité structurelle

### LPIPS (Learned Perceptual Image Patch Similarity)
- Distance dans l'espace des features d'un réseau pré-entraîné (VGG/AlexNet)
- Plus bas = meilleur (images perceptuellement plus proches)
- Corrèle mieux avec le jugement humain que PSNR/SSIM

### FID (Fréchet Inception Distance)
- Compare les distributions statistiques des images générées vs réelles
- Utilise les features d'InceptionV3
- Plus bas = meilleur
- Nécessite un grand nombre d'images (>1000)

---

## 5. Benchmarks NTIRE 2025

### Challenge principal (x4, 286 participants, 25 équipes valides)
- Track 1 (Restoration/PSNR) : architectures hybrides CNN+Transformer dominent
- Track 2 (Perceptual) : modèles avec prior diffusion + CLIP-based losses dominent
- Insight clé : les meilleurs modèles excèlent rarement dans les deux tracks

### Challenge Efficient SR (edge/mobile)
- Baseline : EFDN (26.90 dB sur DIV2K_LSDIR_valid)
- Objectif : maintenir la qualité tout en réduisant runtime/params/FLOPs
- Techniques gagnantes : pruning, quantization, knowledge distillation, NAS

### Datasets de référence
| Dataset | Images | Résolution | Usage |
|---------|--------|-----------|-------|
| DIV2K | 800 train + 100 val + 100 test | 2K | Standard principal |
| LSDIR | 84,991 train + 1,000 val + 1,000 test | Varié | Large-scale training |
| Set5 | 5 | Varié | Benchmark rapide |
| Set14 | 14 | Varié | Benchmark rapide |
| BSD100 | 100 | 481×321 | Textures naturelles |
| Urban100 | 100 | Varié | Structures urbaines |
| Manga109 | 109 | Varié | Manga/anime |

---

## 6. Installation SUPIR (avancé, 12GB+ VRAM requis)

```bash
# Prérequis : Python 3.10+, CUDA 11.8+, 12GB+ VRAM
# NE PAS installer dans l'environnement Claude.ai (pas assez de VRAM)
# Instructions pour installation locale sur PC avec GPU

git clone https://github.com/Fanghua-Yu/SUPIR.git
cd SUPIR

# Installer les dépendances
pip install -r requirements.txt

# Télécharger les modèles (environ 13 GB au total)
# 1. SDXL base : huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
# 2. SUPIR-v0Q (qualité) ou SUPIR-v0F (fidélité)
# 3. Optionnel : Juggernaut-XL-v9 (plus léger, fonctionne sur 12GB)

# Lancer l'interface Gradio
python gradio_demo.py --use_image_slider --loading_half_params
```

---

## 7. Comparatif GAN vs Diffusion (ICLR 2025)

Étude : "Does Diffusion Beat GAN in Image Super Resolution?"

### Conditions contrôlées
- Même architecture backbone (U-Net)
- Même taille de modèle
- Même dataset d'entraînement
- Même budget de calcul

### Résultats
- GAN et Diffusion atteignent une qualité SR similaire
- Le conditionnement textuel (captions) n'a PAS d'effet significatif
- Les augmentations Real-ESRGAN ralentissent la convergence de la diffusion
- Le pre-training avec augmentations nuit à la performance sur la tâche vanilla SR

### Conclusion
La supériorité perçue de la diffusion provient de :
1. Modèles plus grands (plus de paramètres)
2. Datasets plus grands
3. Budget d'entraînement plus long
Pas du paradigme diffusion lui-même.

---

## 8. Troubleshooting courant

### "CUDA out of memory"
→ Réduire tile_size (256 au lieu de 512)
→ Utiliser half precision (--half)
→ Fermer les autres applications GPU

### "ModuleNotFoundError: No module named 'realesrgan'"
→ `pip install realesrgan basicsr facexlib`

### Image de sortie avec couleurs décalées
→ Problème courant avec StableSR/certains modèles de diffusion
→ Solution : appliquer Wavelet Color Fix ou histogram matching post-traitement

### Artefacts "waxy" (cireux) sur la peau
→ Réduire l'intensité du sharpening
→ Utiliser CodeFormer (w=0.5) au lieu de GFPGAN pour les visages
→ Ne pas upscaler au-delà de x4

### Texte illisible après upscale
→ Les upscalers IA ne reconstituent PAS le texte correctement
→ Utiliser un modèle spécialisé OCR + re-rendu, pas de l'upscaling IA
→ Topaz Gigapixel est le moins mauvais pour le texte

### Image trop petite (< 32×32)
→ Aucune méthode ne produira de résultats satisfaisants
→ Essayer SUPIR comme dernier recours (hallucine fortement)
→ Informer l'utilisateur que la reconstruction est spéculative
