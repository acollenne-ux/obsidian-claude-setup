#!/usr/bin/env python3
"""
Pipeline professionnel de détourage d'image.
7 étapes : Segmentation → Trous → Trimap → Alpha Matting → Décontamination → Nettoyage → Assemblage

Usage:
    python detourage.py <input_image> <output_png> [options]

Options:
    --model MODEL          Modèle rembg (birefnet-general, isnet-general-use, u2net)
    --matting-size SIZE    Taille max pour le matting (défaut: 512)
    --hole-threshold N     Seuil de taille pour boucher les trous (défaut: 1500)
    --erode SIZE           Taille d'érosion pour le trimap (défaut: 8)
    --dilate SIZE          Taille de dilatation pour le trimap (défaut: 12)
    --check-bg COLOR       Générer image de contrôle sur fond coloré (ex: "50,150,230")
    --no-decontaminate     Désactiver la décontamination couleur
    --no-matting           Désactiver le matting alpha (masque binaire uniquement)
    --verbose              Afficher les détails de chaque étape
"""

import argparse
import gc
import io
import sys
import time
import numpy as np
import cv2
from PIL import Image
from pathlib import Path


def log(msg, verbose=True):
    if verbose:
        print(f"  {msg}")


def step1_segmentation(input_path, model_name="isnet-general-use", verbose=True):
    """Étape 1 : Segmentation IA avec rembg."""
    log(f"Modèle: {model_name}", verbose)
    from rembg import remove, new_session

    # Fallback si le modèle demandé échoue (OOM)
    models_fallback = [model_name, "isnet-general-use", "u2net"]
    seen = set()
    models_fallback = [m for m in models_fallback if not (m in seen or seen.add(m))]

    mask = None
    for model in models_fallback:
        try:
            session = new_session(model)
            with open(input_path, "rb") as f:
                input_bytes = f.read()
            mask_bytes = remove(input_bytes, session=session, only_mask=True)
            mask = np.array(Image.open(io.BytesIO(mask_bytes)).convert("L"))
            log(f"Segmentation OK avec {model} — mask {mask.shape}", verbose)
            del session, input_bytes, mask_bytes
            gc.collect()
            break
        except Exception as e:
            log(f"Échec {model}: {e}, tentative suivante...", verbose)
            gc.collect()

    if mask is None:
        raise RuntimeError("Aucun modèle de segmentation n'a fonctionné")
    return mask


def step2_classify_holes(mask, small_threshold=1500, verbose=True):
    """Étape 2 : Classification des trous intérieurs via flood fill."""
    h, w = mask.shape
    mask_bin = (mask > 127).astype(np.uint8) * 255

    inv = cv2.bitwise_not(mask_bin)
    flood = inv.copy()
    flood_mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, flood_mask, (0, 0), 128)

    interior_holes = (flood == 255).astype(np.uint8) * 255
    n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(interior_holes)

    holes_patched = 0
    holes_kept = 0
    for i in range(1, n_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < small_threshold:
            mask_bin[labels == i] = 255
            holes_patched += 1
        else:
            holes_kept += 1

    log(f"Trous: {holes_patched} bouchés, {holes_kept} conservés (seuil={small_threshold}px)", verbose)
    return mask_bin


def step3_trimap(mask_bin, image_rgb, erode_size=8, dilate_size=12, verbose=True):
    """Étape 3 : Trimap adaptatif avec gestion blanc-sur-blanc."""
    h, w = mask_bin.shape
    k_e = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * erode_size + 1,) * 2)
    k_d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * dilate_size + 1,) * 2)

    eroded = cv2.erode(mask_bin, k_e)
    dilated = cv2.dilate(mask_bin, k_d)

    trimap = np.full((h, w), 128, dtype=np.uint8)
    trimap[eroded >= 254] = 255
    trimap[dilated <= 1] = 0

    # Adaptation blanc-sur-blanc
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    is_white = gray > 220
    is_unknown = trimap == 128
    trimap[(is_white & is_unknown & (mask_bin > 127))] = 255
    trimap[(is_white & is_unknown & (mask_bin <= 127))] = 0

    n_fg = np.sum(trimap == 255)
    n_bg = np.sum(trimap == 0)
    n_unk = np.sum(trimap == 128)
    pct = n_unk / (h * w) * 100
    log(f"Trimap: FG={n_fg}, BG={n_bg}, Unknown={n_unk} ({pct:.1f}%)", verbose)
    return trimap


def step4_alpha_matting(img_norm, trimap, matting_size=512, verbose=True):
    """Étape 4 : Alpha matting via PyMatting KNN (downscalé)."""
    from pymatting import estimate_alpha_knn

    h, w = img_norm.shape[:2]
    scale = min(1.0, matting_size / max(h, w))
    nw, nh = int(w * scale), int(h * scale)

    img_s = cv2.resize(img_norm, (nw, nh))
    tri_s = cv2.resize(trimap.astype(np.float64) / 255.0, (nw, nh),
                       interpolation=cv2.INTER_NEAREST)

    log(f"Matting KNN à {nw}x{nh} (scale={scale:.2f})...", verbose)
    alpha_s = estimate_alpha_knn(img_s, tri_s)

    alpha = cv2.resize(alpha_s, (w, h), interpolation=cv2.INTER_LINEAR)
    alpha = np.clip(alpha, 0, 1)
    log(f"Alpha: range [{alpha.min():.3f}, {alpha.max():.3f}]", verbose)
    return alpha, img_s, alpha_s


def step5_foreground_estimation(img_s, alpha_s, original_size, verbose=True):
    """Étape 5 : Décontamination couleur via estimation du premier plan."""
    from pymatting import estimate_foreground_ml

    log("Estimation du premier plan (décontamination)...", verbose)
    fg_s = estimate_foreground_ml(img_s, alpha_s)

    w, h = original_size
    foreground = cv2.resize(fg_s, (w, h), interpolation=cv2.INTER_LINEAR)
    foreground = np.clip(foreground, 0, 1)
    log(f"Foreground: range [{foreground.min():.3f}, {foreground.max():.3f}]", verbose)
    return foreground


def step5_manual_decontaminate(img_norm, alpha, bg_color=1.0, verbose=True):
    """Étape 5 alternative : décontamination manuelle (sans PyMatting)."""
    log("Décontamination manuelle (inversion du compositing)...", verbose)
    alpha_safe = np.where(alpha > 0.01, alpha, 1.0)
    fg = (img_norm - (1.0 - alpha[:, :, np.newaxis]) * bg_color) / alpha_safe[:, :, np.newaxis]
    return np.clip(fg, 0, 1)


def step6_morphological_cleanup(alpha, verbose=True):
    """Étape 6 : Nettoyage morphologique + anti-aliasing."""
    alpha_u8 = (alpha * 255).astype(np.uint8)

    # Ouverture pour supprimer le bruit
    k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    alpha_u8 = cv2.morphologyEx(alpha_u8, cv2.MORPH_OPEN, k3)

    # Anti-aliasing
    alpha_u8 = cv2.GaussianBlur(alpha_u8, (3, 3), 0)

    # Garder le plus grand composant connexe
    _, thresh = cv2.threshold(alpha_u8, 10, 255, cv2.THRESH_BINARY)
    n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresh)
    if n_labels > 1:
        sizes = stats[1:, cv2.CC_STAT_AREA]
        largest = np.argmax(sizes) + 1
        removed = n_labels - 2
        alpha_u8[labels != largest] = 0
        log(f"Composant principal: {sizes[largest-1]}px, {removed} blobs supprimés", verbose)

    return alpha_u8


def step7_assemble(foreground, alpha_u8, output_path, check_bg=None, verbose=True):
    """Étape 7 : Assemblage RGBA et sauvegarde."""
    fg_u8 = (foreground * 255).astype(np.uint8)
    result = np.dstack([fg_u8, alpha_u8])
    result_img = Image.fromarray(result, "RGBA")
    result_img.save(output_path, "PNG")
    log(f"Sauvegardé: {output_path} ({result_img.size[0]}x{result_img.size[1]})", verbose)

    if check_bg:
        check_path = str(Path(output_path).with_suffix("")) + "_check.png"
        bg = Image.new("RGBA", result_img.size, (*check_bg, 255))
        composite = Image.alpha_composite(bg, result_img)
        composite.save(check_path)
        log(f"Contrôle: {check_path}", verbose)

    return result_img


def run_pipeline(input_path, output_path, model="isnet-general-use",
                 matting_size=512, hole_threshold=1500,
                 erode_size=8, dilate_size=12,
                 check_bg=(50, 150, 230),
                 no_decontaminate=False, no_matting=False,
                 verbose=True):
    """Exécute le pipeline complet de détourage."""
    t0 = time.time()

    img_pil = Image.open(input_path).convert("RGB")
    img_np = np.array(img_pil)
    h, w = img_np.shape[:2]
    img_norm = img_np.astype(np.float64) / 255.0

    # Étape 1
    print("▸ Étape 1/7 — Segmentation IA")
    mask = step1_segmentation(input_path, model, verbose)

    # Étape 2
    print("▸ Étape 2/7 — Classification des trous")
    mask_bin = step2_classify_holes(mask, hole_threshold, verbose)
    del mask
    gc.collect()

    # Étape 3
    print("▸ Étape 3/7 — Trimap adaptatif")
    trimap = step3_trimap(mask_bin, img_np, erode_size, dilate_size, verbose)

    if no_matting:
        # Mode simplifié : masque binaire uniquement
        print("▸ Étapes 4-5 — Ignorées (--no-matting)")
        alpha = mask_bin.astype(np.float64) / 255.0
        foreground = img_norm
    else:
        # Étape 4
        print("▸ Étape 4/7 — Alpha matting")
        alpha, img_s, alpha_s = step4_alpha_matting(img_norm, trimap, matting_size, verbose)

        # Étape 5
        if no_decontaminate:
            print("▸ Étape 5/7 — Décontamination désactivée")
            foreground = img_norm
            del img_s, alpha_s
        else:
            print("▸ Étape 5/7 — Décontamination couleur")
            try:
                foreground = step5_foreground_estimation(img_s, alpha_s, (w, h), verbose)
                del img_s, alpha_s
            except Exception as e:
                log(f"PyMatting foreground failed ({e}), fallback manuel", verbose)
                del img_s, alpha_s
                foreground = step5_manual_decontaminate(img_norm, alpha, verbose=verbose)

    gc.collect()

    # Étape 6
    print("▸ Étape 6/7 — Nettoyage morphologique")
    alpha_u8 = step6_morphological_cleanup(alpha, verbose)

    # Étape 7
    print("▸ Étape 7/7 — Assemblage RGBA")
    result = step7_assemble(foreground, alpha_u8, output_path, check_bg, verbose)

    elapsed = time.time() - t0
    print(f"\n✓ Détourage terminé en {elapsed:.1f}s — {w}x{h} → {output_path}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Détourage professionnel d'image")
    parser.add_argument("input", help="Image source (jpg, png, webp...)")
    parser.add_argument("output", help="Image de sortie (PNG avec transparence)")
    parser.add_argument("--model", default="isnet-general-use",
                        choices=["birefnet-general", "isnet-general-use", "u2net", "u2netp"],
                        help="Modèle de segmentation")
    parser.add_argument("--matting-size", type=int, default=512,
                        help="Taille max pour le matting alpha (défaut: 512)")
    parser.add_argument("--hole-threshold", type=int, default=1500,
                        help="Seuil de taille pour les trous intérieurs (défaut: 1500)")
    parser.add_argument("--erode", type=int, default=8,
                        help="Taille d'érosion pour le trimap")
    parser.add_argument("--dilate", type=int, default=12,
                        help="Taille de dilatation pour le trimap")
    parser.add_argument("--check-bg", default="50,150,230",
                        help="Couleur RGB du fond de contrôle (ex: '50,150,230')")
    parser.add_argument("--no-check", action="store_true",
                        help="Ne pas générer l'image de contrôle")
    parser.add_argument("--no-decontaminate", action="store_true",
                        help="Désactiver la décontamination couleur")
    parser.add_argument("--no-matting", action="store_true",
                        help="Masque binaire uniquement (pas d'alpha matting)")
    parser.add_argument("--verbose", "-v", action="store_true", default=True,
                        help="Mode verbeux")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Mode silencieux")

    args = parser.parse_args()

    if args.quiet:
        args.verbose = False

    check_bg = None
    if not args.no_check and args.check_bg:
        check_bg = tuple(int(c) for c in args.check_bg.split(","))

    run_pipeline(
        input_path=args.input,
        output_path=args.output,
        model=args.model,
        matting_size=args.matting_size,
        hole_threshold=args.hole_threshold,
        erode_size=args.erode,
        dilate_size=args.dilate,
        check_bg=check_bg,
        no_decontaminate=args.no_decontaminate,
        no_matting=args.no_matting,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
