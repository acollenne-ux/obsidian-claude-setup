# Providers de Generation d'Images IA — Reference Technique

## 1. FLUX.1 (Black Forest Labs)

**Architecture** : Rectified Flow Matching, 12B parametres, double flux attention (streams image + texte separes puis fusionnes)

**Modeles disponibles** :
| Modele | HF Space | Vitesse | Qualite | Licence |
|--------|----------|---------|---------|---------|
| FLUX.1-schnell | `black-forest-labs/FLUX.1-schnell` | ~5s | Bonne | Apache 2.0 |
| FLUX.1-dev | `black-forest-labs/FLUX.1-dev` | ~15s | Excellente | Non-commercial |
| FLUX.1-pro | API BFL uniquement | ~10s | Meilleure | Proprietaire |

**Forces** : Meilleur photoralisme 2025-2026, textures peau, flow matching previsible
**Faiblesses** : Pas de prompt negatif natif, queue HF variable, pas de ControlNet natif (en dev)

**Resolutions** : 256-1024px natif (upscale necessaire pour >1024)
**Steps** : schnell=4, dev=20-28
**CFG** : 0 (schnell), 3.5-7.5 (dev)

**Prompting** : Descriptions longues et detaillees (200-400 chars), medium explicite, tokens qualite en fin
**Tarif** : Gratuit via HF Spaces (queue), ~$0.015-$0.03/image via fal.ai

---

## 2. GPT-Image / DALL-E 3 (OpenAI)

**Architecture** :
- DALL-E 3 : unCLIP (CLIP encoder → diffusion prior → diffusion decoder GLIDE ~3.5B params)
- GPT-Image (GPT-4o natif) : transformer unifie autoregressif + diffusion hybride

**API** :
| Endpoint | Modele | Tarif |
|----------|--------|-------|
| `/v1/images/generations` | `dall-e-3` | $0.04-$0.12/image |
| `/v1/images/generations` | `gpt-image-1` | ~$5/M input + $40/M output tokens |

**Forces** : Meilleur texte dans l'image (unification modale), meilleur suivi d'instructions, prompt rewriting automatique
**Faiblesses** : Censure stricte, biais chromatique chaud, ~30s/image, cout eleve

**Resolutions** : 1024x1024, 1024x1792, 1792x1024
**Style** : "natural" (photoraliste) ou "vivid" (sature, dramatique)
**Qualite** : "standard" ou "hd"

**Prompting** : Langage naturel clair et instructif, texte verbatim entre guillemets, pas de tokens techniques
**Cle API** : `ai_config.json` → providers → openai → api_key

---

## 3. Nano Banana 2 / Gemini Image (Google)

**Architecture** : Transformer MoE distille de Gemini Pro + module diffusion, "reasoning before rendering"

**API** :
| Modele | Endpoint | Tarif |
|--------|----------|-------|
| `gemini-2.0-flash-exp` | `generativelanguage.googleapis.com/v1beta` | Gratuit (preview) |
| `gemini-3.1-flash-image-preview` | idem | $0.045-$0.15/image |

**Forces** : 4K natif, ~3-6s, coherence multi-sujets (5 personnages + 14 objets), grounding web
**Faiblesses** : Guardrails Google stricts, architecture opaque, en preview

**Resolutions** : 512, 1K, 2K, 4K
**Ratios** : 14 ratios supportes

**Prompting** : Langage naturel enrichi, contexte/intention > details techniques, Gemini raisonne seul
**Cle API** : `ai_config.json` → providers → gemini → api_key
**Appel** : `generateContent` avec `responseModalities: ["TEXT", "IMAGE"]`

---

## 4. SDXL / SD3.5 (Stability AI)

**Architecture** :
- SDXL : Latent Diffusion Model, U-Net double (base + refiner), 2 encodeurs CLIP
- SD3.5 : MMDiT-X (Multimodal Diffusion Transformer), 3 encodeurs texte (2x CLIP + T5-XXL 5B)

**HF Spaces** :
| Modele | Space | Vitesse |
|--------|-------|---------|
| SDXL base | `stabilityai/stable-diffusion-xl-base-1.0` | ~15s |
| SDXL Turbo | `stabilityai/sdxl-turbo` | ~2s |
| SD3.5 Large | `stabilityai/stable-diffusion-3.5-large` | ~20s |

**Forces** : Open-source, ControlNet + IP-Adapter natif, multi-resolution, checkpoints anime
**Faiblesses** : Qualite inferieure a FLUX/GPT-Image, prompt negatif obligatoire, plus de configuration

**Resolutions** : 512-2048px (SDXL natif 1024x1024)
**Steps** : 25-50 (Turbo: 1-4)
**CFG** : 5-9 (defaut 7)

**Prompting** : Prompt structure + negatif OBLIGATOIRE, tokens qualite, ponderation par parentheses
**Tarif** : Gratuit via HF Spaces, ~$0.03/image via API Stability

---

## 5. Autres providers (non integres, reference)

### Midjourney
- Pas d'API publique, Discord/web uniquement
- Meilleur pour l'artistique/editorial
- $10-30$/mois

### Ideogram 3.0
- #1 rendu texte (~90-95% precision)
- API via Together AI
- ~$0.04/image

### Recraft V3/V4
- Generation vectorielle native SVG
- N1 HuggingFace T2I Benchmark
- API via fal.ai (~$0.04-$0.08/image)

### Leonardo AI Phoenix
- Base FLUX, jusqu'a 5MP natif
- API disponible
- Freemium, $10-60$/mois

---

## Comparatif synthetique

| Critere | FLUX | GPT-Image | Nano Banana 2 | SDXL |
|---------|------|-----------|---------------|------|
| Photoralisme | ★★★★★ | ★★★★ | ★★★★ | ★★★ |
| Texte dans image | ★★★ | ★★★★★ | ★★★★ | ★★ |
| Vitesse | ★★★★ | ★★ | ★★★★★ | ★★★ |
| Cout | Gratuit | $$$ | $ | Gratuit |
| Controle (ControlNet) | En dev | Non | Non | ★★★★★ |
| Open source | Partiel | Non | Non | Oui |
| Suivi d'instructions | ★★★★ | ★★★★★ | ★★★★ | ★★★ |
| Resolution max | 1024 | 1792 | 4096 | 2048 |

---

## Rate limits et quotas

| Provider | Limite | Action si atteinte |
|----------|--------|--------------------|
| HF Spaces (gratuit) | Queue variable, 1-5 req/min | Patienter ou fallback |
| OpenAI (DALL-E 3) | 7 images/min (tier 1) | Fallback vers FLUX |
| Gemini (preview) | 10 req/min, 1500/jour | Fallback vers FLUX |
| Stability API | 150 req/10s | Patienter |
