---
name: image-studio
description: SKILL OBLIGATOIRE AUTO-INVOQUÉ pour TOUTE demande de création ou modification visuelle. Studio unifié images/flyers/affiches/posters/visuels à partir d'images réelles, avec intégration Canva MCP obligatoire. Pipeline 8 phases (brief, assets, moodboard, prep, composition Canva, typo, art direction, QA). Use when: créer image, créer flyer, créer affiche, créer poster, créer visuel, créer bannière, créer post, créer carte, créer invitation, créer menu, modifier image, retoucher photo, composer visuel, monter image, faire un flyer, faire une affiche, faire un visuel, design graphique, maquette, mockup, template visuel, image marketing, image produit, image événement. Fidélité exacte au brief + goût esthétique professionnel + Canva.
---

# image-studio — Studio Visuel Unifié

**Tu es un directeur artistique + technicien image pro.** Ta mission : livrer un visuel qui répond EXACTEMENT au brief utilisateur, avec un goût esthétique professionnel, en travaillant principalement à partir d'images réelles fournies (photos, produits, personnes, lieux).

---

## HARD GATES

<HARD-GATE>
1. JAMAIS livrer sans avoir reformulé le brief et obtenu (ou posé) l'hypothèse sur les ambiguïtés critiques.
2. JAMAIS re-générer via IA une image réelle fournie par l'utilisateur (visages, produits, logos) — toujours COMPOSITER / RETOUCHER l'image originale.
3. JAMAIS livrer sans passage par l'agent `art-director` (critique esthétique + score ≥ 8/10).
4. JAMAIS livrer sans QA visuel final (lisibilité, contraste, alignements, export formats).
5. TOUJOURS capturer le résultat à chaque itération et le comparer au brief.
6. **TOUJOURS travailler avec Canva via le MCP `claude_ai_Canva`** comme moteur de composition principal. Les rendus HTML/CSS/Pillow ne sont utilisés QUE comme fallback si Canva est indisponible ou si la tâche est une retouche photo pure (non compositionnelle).
7. **TOUJOURS utiliser `gemini-cli` (Gemini 3 Pro via OAuth gratuit) comme co-moteur vision** pour : (a) analyser toute image de référence fournie par l'utilisateur (extraction palette, composition, style, typo), (b) générer la description structurée du visuel à composer dans Canva, (c) reviewer les drafts exportés par Canva avant de les envoyer à l'art-director. Claude Opus s'appuie sur Gemini 3 Pro pour tout ce qui touche à la vision et à la génération de prompts visuels, parce que Gemini bat Claude sur la perception d'images. Fallback transparent vers `multi-ia-router` (Gemini 2.5 Flash) géré par `gemini_wrapper.py`.
</HARD-GATE>

## CO-MOTEUR VISION : GEMINI 3 PRO (obligatoire)

Pour toute tâche image/visuel, appeler `gemini-cli` AVANT l'art-director via :

```bash
python "C:/Users/Alexandre collenne/.claude/skills/gemini-cli/tools/gemini_wrapper.py" \
  --prompt "<instruction vision>" \
  --image "<image_input>"
```

**Usages obligatoires dans le pipeline image-studio :**
- **Phase 1 (Brief + références)** : analyser chaque image de référence fournie → extraire palette, style, composition, typo, mood.
- **Phase 3 (Moodboard)** : générer la description structurée du moodboard (prompt Canva `generate-design-structured`).
- **Phase 5 (Composition Canva)** : enrichir les prompts Canva avec la description générée par Gemini.
- **Phase 7 (Itération critique)** : Gemini review le draft Canva exporté (critique vision) avant passage à l'art-director Claude.

**Pourquoi Gemini ?** Gemini 3 Pro a une vision supérieure à Claude Opus 4.6 sur la lecture d'images (composition, typo, palette, micro-détails). Claude garde le raisonnement stratégique et le contrôle du pipeline, Gemini fait le heavy lifting visuel.


## INTÉGRATION CANVA (OBLIGATOIRE)

Canva est le **moteur de composition principal**. Le MCP `claude_ai_Canva` fournit tous les outils nécessaires :

### Outils Canva clés
- `search-designs` — chercher un design existant (template, précédent travail)
- `generate-design` / `generate-design-structured` — créer un nouveau design à partir d'un prompt structuré
- `create-design-from-candidate` — créer à partir d'un candidat validé
- `start-editing-transaction` → `perform-editing-operations` → `commit-editing-transaction` — éditer un design (positions, textes, couleurs, images)
- `upload-asset-from-url` — uploader les images réelles préparées (après detourage/enhance)
- `get-assets` — lister les assets disponibles
- `get-design-content` / `get-design-pages` / `get-design-thumbnail` — inspecter le rendu
- `resize-design` — adapter aux formats (A4, IG, story, print)
- `export-design` → télécharger PNG/PDF/JPG final
- `list-brand-kits` — récupérer les couleurs/fonts/logos de la marque
- `comment-on-design` / `list-comments` — collaboration

### Workflow Canva dans le pipeline

**Phase 2 bis — Brand Kit** : appeler `list-brand-kits` pour récupérer palette et fonts marque si existants.

**Phase 4 — Asset Preparation** : après detourage/enhance local, **uploader chaque asset préparé vers Canva** via `upload-asset-from-url` (ou depuis fichier local si le MCP le permet). Stocker les IDs retournés.

**Phase 5 — Composition (Canva-first)** :
1. **Template discovery** : `search-designs` avec mots-clés du brief (ex: "flyer soirée techno", "affiche concert") pour trouver un template de départ
2. **Création** : `generate-design-structured` avec :
   - type (flyer/poster/social-post/presentation)
   - dimensions exactes
   - textes obligatoires du brief
   - palette (depuis brand kit ou direction esthétique)
   - IDs des assets réels uploadés
3. **Édition fine** : `start-editing-transaction` → `perform-editing-operations` pour :
   - positionner précisément les images réelles
   - ajuster textes (taille, couleur, font, tracking)
   - appliquer la grille et les alignements
   - corriger selon instructions de l'art-director
4. **Commit** : `commit-editing-transaction`
5. **Inspection** : `get-design-thumbnail` pour envoyer au `art-director`

**Phase 7 — Itération critique** : les corrections de l'art-director sont appliquées via nouvelles `editing-transaction` Canva. Chaque version = nouveau thumbnail inspecté.

**Phase 8 — Export final** : `export-design` en PNG (haute résolution) + PDF + JPG selon brief, puis téléchargement et sauvegarde locale dans `C:/tmp/image-studio/<session>/final/`.

### Fallback (non-Canva)
Utiliser HTML/CSS/Playwright ou Pillow UNIQUEMENT si :
- Canva MCP indisponible (erreur authentification, réseau)
- Retouche photo pure sans composition (exposition, couleurs d'une seule image)
- L'utilisateur demande explicitement "sans Canva"

Dans tous les autres cas → **Canva obligatoire**.

---

## PHILOSOPHIE

- **Fidélité > créativité libre** : le brief est sacré. On interprète esthétiquement mais on ne dévie pas.
- **Images réelles préservées** : les photos fournies sont la matière première. On détoure, enhance, compose — on ne régénère pas.
- **Goût pro** : hiérarchie visuelle, respiration, grille, contraste WCAG AA min, typographie hiérarchisée, palette cohérente, alignements pixel-perfect.
- **Itération critique** : un premier jet n'est jamais final. Art director review → corrections → re-render.

---

## PIPELINE 8 PHASES

### Phase 1 — Brief Parsing (agent `brief-analyst`)

Extraire du message utilisateur :
```
BRIEF STRUCTURÉ
- Type livrable    : [flyer / affiche / poster / retouche / composition / bannière / visuel produit]
- Format           : [A4 portrait / 1080x1080 / 1920x1080 / custom]
- Intention        : [promouvoir / annoncer / décorer / vendre / informer]
- Public cible     : [jeune / pro / famille / luxe / grand public]
- Ton              : [élégant / fun / minimaliste / luxueux / street / corporate]
- Texte obligatoire: [titres, dates, lieu, prix, CTA, mentions légales]
- Images fournies  : [liste + chemins + rôle de chacune]
- Références       : [styles / marques / moodboard cités]
- Palette imposée  : [couleurs, logo corporate]
- Contraintes      : [pas de tel élément, marge X, zone safe]
- Livrable final   : [PNG/JPG/PDF, résolution, DPI]

SCORE CLARTÉ: X/10
AMBIGUÏTÉS: [liste]
HYPOTHÈSES POSÉES: [choix automatique pour chaque ambiguïté]
```

Si clarté < 5/10 → poser UNE question bloquante max. Sinon, poser des hypothèses et continuer.

### Phase 2 — Asset Intake (agent `asset-curator`)

Pour chaque image réelle fournie par l'utilisateur :
1. **Lire l'image avec l'outil Read** (vision Claude) pour comprendre son contenu
2. Documenter :
   ```
   ASSET #N
   - Chemin        : [path]
   - Contenu       : [description vision : sujet, fond, angle, éclairage]
   - Qualité       : [résolution px, netteté, bruit, JPEG artifacts]
   - Couleurs dom. : [palette extraite]
   - Rôle dans composition : [sujet principal / fond / secondaire / texture]
   - Pré-traitement nécessaire : [detourage / enhance / crop / color correct / recadrage]
   - Zone safe du sujet : [bounding box approximative]
   ```
3. Lancer pré-traitement via les skills existants :
   - Fond à retirer → invoquer skill **`image-detourage`**
   - Basse résolution / flou → invoquer skill **`image-enhancer`**
   - Exposition/couleurs → Pillow `ImageEnhance` (Brightness, Contrast, Color, Sharpness)

### Phase 2ter — AI Generation (skill `image-generator`) — OPTIONNEL

**Declencheur** : le brief demande un visuel SANS images reelles fournies, OU le brief necessite des visuels supplementaires generes par IA (fonds, illustrations, elements graphiques).

**Si active** :
1. Invoquer le skill `image-generator` avec le brief analyse en Phase 1
2. Specifier le type (photo/illustration/text-in-image/logo/anime/abstract)
3. Specifier le mode qualite (draft/standard/best)
4. Recuperer l'image generee comme "asset genere" dans le pipeline
5. Continuer normalement vers Phase 3 (Moodboard) avec cet asset

**Quand NE PAS activer** :
- L'utilisateur a fourni toutes les images necessaires
- Le brief est une retouche/modification d'image existante
- Le brief est une composition pure de photos reelles

**Integration** :
```
image-studio Phase 2 (Asset Intake)
  → Detecte besoin de generation IA
  → Invoque: Skill("image-generator", args="<brief>")
  → Recupere: C:/tmp/image-generator/<session>/selected_best.png
  → Traite comme ASSET #N dans le pipeline
  → Continue Phase 3
```

### Phase 3 — Moodboard & Direction (agent `art-director` — mode exploration)

Proposer **2 directions esthétiques** cohérentes avec le brief :
```
DIRECTION A — [nom, ex: "Minimaliste éditorial"]
  - Palette       : [3-5 couleurs hex]
  - Typographies  : [2 fonts : titre + corps, avec justification]
  - Grille        : [12 col / 3 col / golden ratio]
  - Mood          : [adjectifs]
  - Références pro: [noms de marques/affiches]

DIRECTION B — [nom, ex: "Poster street graphique"]
  ...

RECOMMANDATION: A (raison)
```

Si l'utilisateur n'est pas là pour valider → choisir la direction la plus alignée au brief et noter le choix.

### Phase 4 — Asset Preparation

Exécuter concrètement :
- Detourage via `rembg` (script Python) ou skill `image-detourage`
- Enhance via Real-ESRGAN / GFPGAN si visages
- Color grading Pillow : `ImageEnhance.Color`, `Contrast`, `Brightness`
- Crop intelligent sur sujet détecté
- Convert RGBA et sauvegarde intermédiaire dans `C:/tmp/image-studio/<session>/assets/`

### Phase 5 — Composition (agent `compositor`)

**Choix du moteur selon le type de livrable :**

| Livrable | Moteur | Pourquoi |
|----------|--------|----------|
| Flyer / Affiche / Poster | **HTML + CSS + Playwright** (capture) | Typographie pro, responsive, CSS Grid, alignements pixel-perfect |
| Retouche photo pure | **Pillow + OpenCV** | Manipulation pixel, filtres, layers |
| Compositing (produit sur fond) | **Pillow RGBA paste** + shadows | Préserve l'image réelle |
| Bannière web | HTML + CSS | Idem flyer |
| Post Instagram | HTML + CSS OU Pillow | Selon complexité |

**Template HTML/CSS de base pour flyer** (à adapter) :
```html
<!DOCTYPE html>
<html><head><style>
  @import url('https://fonts.googleapis.com/css2?family=<TITLE_FONT>:wght@700;900&family=<BODY_FONT>:wght@400;500&display=swap');
  body { margin:0; font-family: '<BODY_FONT>', sans-serif; }
  .page { width: 2480px; height: 3508px; /* A4 300dpi */
          background: <BG>; position:relative; overflow:hidden; }
  .hero-img { position:absolute; /* positionner l'image réelle détourée */ }
  .title { font-family:'<TITLE_FONT>'; font-size: 240px; line-height:0.9;
           letter-spacing:-0.02em; color:<TEXT>; }
  .subtitle { font-size: 64px; font-weight: 500; }
  .meta { position:absolute; bottom:120px; font-size:48px; }
  /* grille 12 colonnes, marges 180px */
</style></head>
<body><div class="page">
  <img class="hero-img" src="file:///C:/tmp/image-studio/<session>/assets/hero_cutout.png">
  <h1 class="title">...</h1>
  <p class="subtitle">...</p>
  <div class="meta">date · lieu · prix</div>
</div></body></html>
```

Rendu via Playwright :
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width":2480,"height":3508}, device_scale_factor=1)
    page.goto(f"file:///{html_path}")
    page.wait_for_load_state("networkidle")
    page.screenshot(path=out_path, full_page=True, omit_background=False)
    b.close()
```

### Phase 6 — Typography & Layout Rules (checklist pro obligatoire)

- [ ] Hiérarchie : titre ≥ 3x taille corps
- [ ] Max 2 familles de fonts (3 si vraiment justifié)
- [ ] Contraste texte/fond ≥ 4.5:1 (WCAG AA)
- [ ] Tracking titre : -0.02em à -0.04em ; corps : 0
- [ ] Line-height titre : 0.9-1.1 ; corps : 1.4-1.6
- [ ] Marges : respect zone safe (≥ 5% des bords pour print)
- [ ] Alignements : grille 12 col ou baseline visible
- [ ] Respiration : ≥ 30% de whitespace
- [ ] Palette : 1 dominante + 1 accent + neutres (règle 60/30/10)
- [ ] Point focal clair en 1 seconde (test du squint)

### Phase 7 — Art Director Review (agent `art-director` — mode critique)

Capturer le rendu et l'**analyser avec Vision** (Read tool sur PNG). Grille d'évaluation /10 :

```
REVIEW V<N>
1. Fidélité au brief         : /10  [détails]
2. Hiérarchie visuelle       : /10
3. Lisibilité texte          : /10
4. Contraste & couleurs      : /10
5. Qualité des images réelles: /10
6. Typographie               : /10
7. Alignements & grille      : /10
8. Respiration / whitespace  : /10
9. Cohérence esthétique      : /10
10. Impact émotionnel        : /10

SCORE TOTAL: X/100

PROBLÈMES IDENTIFIÉS:
- [problème 1 + correction exacte]
- [problème 2 + correction exacte]

VERDICT: [LIVRABLE / ITÉRER]
```

**Si score < 80/100 → itérer.** Max 4 itérations. Chaque itération applique les corrections exactes.

### Phase 8 — QA Visuel Final (agent `qa-visual`)

- [ ] Rendu final capture + vision pass
- [ ] Export dans tous les formats demandés (PNG, JPG, PDF)
- [ ] Résolutions : 300 DPI pour print, 72 DPI web
- [ ] Test contraste WCAG (script Python colorsys)
- [ ] Sauvegarde finale dans `C:/tmp/image-studio/<session>/final/`
- [ ] Log session : brief, assets, direction choisie, scores d'itération, fichiers produits

---

## AGENTS SPÉCIALISÉS

Fichiers dans `agents/` :
- `brief-analyst.md` — Phase 1
- `asset-curator.md` — Phase 2
- `art-director.md` — Phases 3 & 7 (double rôle)
- `compositor.md` — Phase 5
- `qa-visual.md` — Phase 8

Invoquer via le tool `Agent` (subagent_type: general-purpose) avec le contenu du fichier agent comme prompt système.

---

## INVOCATION DES SKILLS EXISTANTS

`image-studio` **compose** les skills existants plutôt que de les remplacer :
- `image-detourage` → appelé en Phase 4 pour les cutouts
- `image-enhancer` → appelé en Phase 4 pour upscale/restoration
- `flyer-creator` → référence pour templates CSS (patterns réutilisables)

---

## WORKFLOW TYPE — Exemple "Flyer événement à partir de 3 photos réelles"

```
1. brief-analyst → structure le brief (titre, date, lieu, ton, format A3)
2. asset-curator → analyse les 3 photos (sujet, qualité, rôle)
   - photo1 : portrait DJ → detourage + enhance GFPGAN (visage)
   - photo2 : foule → fond texturé, légère désaturation
   - photo3 : logo club → garder intact
3. art-director (exploration) → propose 2 directions, choisit "poster rave rétro"
4. asset-prep → exécute detourage + enhance + color grade
5. compositor → HTML/CSS (grille 12 col, fonts Bebas Neue + Inter)
   - Playwright capture 2480x3508 @300dpi
6. typography check → valide contraste, hiérarchie
7. art-director (critique) → review vision, score 72/100
   → problèmes : titre trop petit, DJ mal positionné, contraste date faible
   → itération v2 : corrections appliquées → score 88/100 ✅
8. qa-visual → export PNG + PDF, log session
```

---

## OUTILS TECHNIQUES (Python)

```python
# Detourage
from rembg import remove  # ou subprocess image-detourage skill

# Enhancement
# subprocess: realesrgan-ncnn-vulkan OR GFPGAN CLI

# Compositing + filtres
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import cv2, numpy as np

# Rendu HTML haute résolution
from playwright.sync_api import sync_playwright

# Contraste WCAG
def contrast_ratio(rgb1, rgb2):
    def lum(c):
        c = [x/255 for x in c]
        c = [(x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4) for x in c]
        return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
    l1, l2 = lum(rgb1), lum(rgb2)
    return (max(l1,l2)+0.05)/(min(l1,l2)+0.05)
```

---

## SORTIE ATTENDUE

Toujours livrer :
1. Les fichiers finaux (chemins absolus)
2. Le log de session (brief structuré, direction, scores d'itération)
3. Un récapitulatif en français des décisions esthétiques prises
4. PDF de compte-rendu via `send_report.py` si analyse ou livraison importante

---

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Le brief est clair, je saute la Phase 1" | Non. TOUJOURS reformuler. |
| "Je génère une image IA du produit" | JAMAIS. L'image réelle fournie est sacrée. |
| "Le premier rendu est bien, pas besoin d'art-director" | NON. Toujours review critique. |
| "Pillow suffit pour un flyer" | Pour du texte typographié pro → HTML/CSS/Playwright. Pillow ne gère pas la typographie pro (kerning, ligatures, feature settings). |
| "Contraste OK à l'œil" | Calcule le ratio WCAG. |
| "Une seule direction esthétique proposée" | Toujours 2 en Phase 3. |

## LIVRABLE FINAL

- **Type** : image
- **Généré par** : self
- **Destination** : acollenne@gmail.com via send_report.py

## CHAÎNAGE ARBORESCENCE

- **Amont** : deep-research (entrée unique)
- **Aval** : self


---

## ÉVOLUTION

Ce skill s'auto-améliore via RETEX. Après chaque session :

**Métriques à tracker** :
- Score art-director moyen (cible : ≥ 85/100 au 1er jet)
- Nombre d'itérations moyen avant PASS (cible : ≤ 2)
- Taux d'utilisation Canva vs fallback HTML (cible : >80% Canva)
- Motifs de FIX récurrents → enrichir la checklist Phase 6

**Actions d'amélioration** :
- Si score < 80 récurrent → revoir les templates HTML/CSS de base
- Si itérations > 3 récurrent → renforcer Phase 1 (brief parsing)
- Si fallback HTML > 30% → diagnostiquer les erreurs Canva MCP
- Nouveau pattern esthétique validé → l'ajouter dans les références art-director

```bash
python "C:/Users/Alexandre collenne/.claude/tools/retex_manager.py" save image_studio \
  --quality [score] --tools-used "[Canva,Playwright,Pillow]" --notes "[leçons]"
```

## DELIVERY GATE — layout-qa (OBLIGATOIRE)

**Avant tout envoi du livrable final**, ce skill DOIT invoquer la porte `layout-qa` :

```bash
python ~/.claude/skills/layout-qa/scripts/run_gate.py \
    --input <livrable> \
    --brief <brief.md> \
    --caller <nom-de-ce-skill> \
    --max-iter 3 \
    --out-report qa_report.json
```

- Exit `0` (PASS) → envoi autorisé (email, téléchargement utilisateur)
- Exit `1` (FIX) → lire `qa_report.json`, appliquer les corrections au Composer, re-rendre, re-invoquer layout-qa (max 3 itérations)
- Exit `2` (FAIL) → escalade utilisateur avec les PNG annotés (`annotated_dir`)

La phase vision multimodale est assurée par l'agent `visual-layout-critic` côté Claude après l'exécution déterministe du script. Aucun livrable ne sort sans verdict PASS.
