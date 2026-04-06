#!/usr/bin/env python3
"""
Agent Spécialisé de Détourage — "DetourAgent"

Agent intelligent qui orchestre le pipeline de détourage avec :
1. Analyse automatique de l'image (type de sujet, fond, complexité)
2. Choix adaptatif des paramètres optimaux
3. Exécution du pipeline multi-passes si nécessaire
4. Vérification qualité automatique (halo, trous, préservation)
5. Auto-correction ciblée des défauts détectés
6. Rapport de qualité détaillé

Usage:
    python detour_agent.py <input> <output> [options]
    python detour_agent.py <input_dir> <output_dir> --batch  (traitement par lots)

Options:
    --quality low|medium|high|max   Niveau de qualité (défaut: high)
    --bg-color R,G,B               Couleur de fond à supprimer (auto-détection si omis)
    --preserve-holes                Forcer la conservation des trous intérieurs
    --max-passes N                  Nombre max de passes correctives (défaut: 3)
    --batch                         Traitement par lots d'un dossier
    --report                        Générer un rapport de qualité détaillé
    --verbose / -v                  Mode verbeux
"""

import argparse
import gc
import io
import json
import os
import sys
import time
import numpy as np
import cv2
from PIL import Image
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, Tuple, List, Dict


# ═══════════════════════════════════════════════════════════════════════════
# STRUCTURES DE DONNÉES
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ImageAnalysis:
    """Résultat de l'analyse préliminaire de l'image."""
    width: int = 0
    height: int = 0
    megapixels: float = 0.0
    bg_color: Tuple[int, int, int] = (255, 255, 255)
    bg_type: str = "white"              # white, light, dark, colored, complex
    bg_uniformity: float = 0.0          # 0-1, uniformité du fond
    subject_type: str = "generic"       # person, product, equipment, fine_detail
    has_white_elements: bool = False    # chaussures blanches, vêtements blancs...
    has_holes: bool = False             # trous dans le sujet (disques, grilles...)
    has_fine_edges: bool = False        # cheveux, fils, bords fins
    complexity: str = "medium"          # low, medium, high
    recommended_model: str = "isnet-general-use"
    recommended_matting_size: int = 512
    recommended_erode: int = 8
    recommended_dilate: int = 12
    recommended_hole_threshold: int = 1500


@dataclass
class QualityReport:
    """Rapport de qualité du détourage."""
    total_pixels: int = 0
    visible_pixels: int = 0
    transparent_pixels: int = 0
    semi_transparent_pixels: int = 0
    halo_pixels: int = 0               # pixels blancs visibles en bordure
    halo_severity: str = "none"        # none, light, moderate, severe
    interior_white_blobs: int = 0
    subject_preserved_pct: float = 0.0
    edge_smoothness: float = 0.0       # 0-1
    overall_score: float = 0.0         # 0-10
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    pass_number: int = 1


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 1 — ANALYSEUR D'IMAGE
# ═══════════════════════════════════════════════════════════════════════════

class ImageAnalyzer:
    """Analyse l'image source pour déterminer les paramètres optimaux."""

    def analyze(self, image_path: str, verbose: bool = True) -> ImageAnalysis:
        """Analyse complète de l'image source."""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Impossible de lire : {image_path}")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]
        analysis = ImageAnalysis(width=w, height=h, megapixels=w * h / 1e6)

        self._analyze_background(img_rgb, analysis)
        self._analyze_subject(img_rgb, analysis)
        self._recommend_params(analysis)

        if verbose:
            self._print_analysis(analysis)

        return analysis

    def _analyze_background(self, img: np.ndarray, a: ImageAnalysis):
        """Détecte le type et la couleur du fond."""
        h, w = img.shape[:2]

        # Échantillonner les bords (20px de chaque côté)
        margin = min(20, h // 10, w // 10)
        edges = np.concatenate([
            img[:margin, :].reshape(-1, 3),      # haut
            img[-margin:, :].reshape(-1, 3),      # bas
            img[:, :margin].reshape(-1, 3),       # gauche
            img[:, -margin:].reshape(-1, 3),      # droite
        ])

        mean_color = np.mean(edges, axis=0).astype(int)
        std_color = np.std(edges, axis=0)
        a.bg_color = tuple(mean_color)
        a.bg_uniformity = 1.0 - min(np.mean(std_color) / 128.0, 1.0)

        brightness = np.mean(mean_color)
        if brightness > 230 and a.bg_uniformity > 0.6:
            a.bg_type = "white"
        elif brightness > 200 and a.bg_uniformity > 0.5:
            a.bg_type = "light"
        elif brightness < 50 and a.bg_uniformity > 0.7:
            a.bg_type = "dark"
        elif a.bg_uniformity > 0.6:
            a.bg_type = "colored"
        else:
            a.bg_type = "complex"

    def _analyze_subject(self, img: np.ndarray, a: ImageAnalysis):
        """Analyse le type de sujet et ses caractéristiques."""
        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Détection d'éléments blancs dans le sujet (zone centrale)
        center = img[h // 4:3 * h // 4, w // 4:3 * w // 4]
        center_gray = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
        white_ratio = np.sum(center_gray > 230) / center_gray.size
        a.has_white_elements = white_ratio > 0.05

        # Détection de bords fins via Canny
        edges = cv2.Canny(gray, 50, 150)
        thin_edges = cv2.Canny(gray, 100, 200)
        edge_ratio = np.sum(thin_edges > 0) / thin_edges.size
        a.has_fine_edges = edge_ratio > 0.03

        # Détection de trous : régions de fond encerclées par le sujet
        # Segmentation rapide par seuillage Otsu
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closed = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kernel, iterations=3)
        inv_closed = cv2.bitwise_not(closed)
        flood = inv_closed.copy()
        fm = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(flood, fm, (0, 0), 128)
        potential_holes = np.sum(flood == 255)
        a.has_holes = potential_holes > 500

        # Estimation de la complexité
        complexity_score = 0
        if a.has_white_elements and a.bg_type in ("white", "light", "colored"):
            complexity_score += 3  # Blanc sur blanc = très difficile
        if a.has_holes:
            complexity_score += 2  # Trous = difficile
        if a.has_fine_edges:
            complexity_score += 1
        if a.bg_type == "complex":
            complexity_score += 2
        if a.bg_uniformity < 0.8:
            complexity_score += 1  # Fond pas parfaitement uniforme

        # Blanc-sur-blanc = toujours complexe
        if a.has_white_elements and a.bg_type in ("white", "light", "colored"):
            complexity_score += 2
        if complexity_score <= 1:
            a.complexity = "low"
        elif complexity_score <= 3:
            a.complexity = "medium"
        else:
            a.complexity = "high"

        # Classification du sujet
        if a.has_fine_edges and not a.has_holes:
            a.subject_type = "person"
        elif a.has_holes:
            a.subject_type = "equipment"
        elif white_ratio < 0.02 and edge_ratio < 0.02:
            a.subject_type = "product"
        else:
            a.subject_type = "generic"

    def _recommend_params(self, a: ImageAnalysis):
        """Recommande les paramètres optimaux selon l'analyse."""
        # Modèle — isnet-general-use minimum, u2net seulement si explicitement demandé
        if a.complexity == "high" or a.megapixels > 2:
            a.recommended_model = "isnet-general-use"  # birefnet si mémoire suffisante
        else:
            a.recommended_model = "isnet-general-use"  # TOUJOURS isnet minimum

        # Taille de matting — 512 minimum pour qualité acceptable
        if a.complexity == "high":
            a.recommended_matting_size = 640
        elif a.complexity == "low":
            a.recommended_matting_size = 512
        else:
            a.recommended_matting_size = 512

        # Trimap
        if a.subject_type == "person":
            a.recommended_erode = 5
            a.recommended_dilate = 18
        elif a.subject_type == "equipment":
            a.recommended_erode = 8
            a.recommended_dilate = 15  # Large pour ne pas couper les barres/poignées
        elif a.subject_type == "product":
            a.recommended_erode = 8
            a.recommended_dilate = 10
        else:
            a.recommended_erode = 8
            a.recommended_dilate = 12

        # Seuil des trous
        if a.has_holes:
            a.recommended_hole_threshold = 2000
        else:
            a.recommended_hole_threshold = 1000

    def _print_analysis(self, a: ImageAnalysis):
        print("╔══════════════════════════════════════════════╗")
        print("║        ANALYSE D'IMAGE — DetourAgent        ║")
        print("╠══════════════════════════════════════════════╣")
        print(f"║ Dimensions    : {a.width}×{a.height} ({a.megapixels:.1f} Mpx)")
        print(f"║ Fond          : {a.bg_type} (uniformité {a.bg_uniformity:.0%})")
        print(f"║ Couleur fond  : RGB({a.bg_color[0]}, {a.bg_color[1]}, {a.bg_color[2]})")
        print(f"║ Type sujet    : {a.subject_type}")
        print(f"║ Blanc sur sujet: {'OUI ⚠' if a.has_white_elements else 'non'}")
        print(f"║ Trous/ouvertures: {'OUI ⚠' if a.has_holes else 'non'}")
        print(f"║ Bords fins    : {'OUI' if a.has_fine_edges else 'non'}")
        print(f"║ Complexité    : {a.complexity.upper()}")
        print("╠══════════════════════════════════════════════╣")
        print(f"║ Modèle recommandé : {a.recommended_model}")
        print(f"║ Matting size      : {a.recommended_matting_size}px")
        print(f"║ Trimap erode/dilate: {a.recommended_erode}/{a.recommended_dilate}")
        print(f"║ Seuil trous       : {a.recommended_hole_threshold}px")
        print("╚══════════════════════════════════════════════╝")


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 2 — MOTEUR DE DÉTOURAGE (réutilise le pipeline du skill)
# ═══════════════════════════════════════════════════════════════════════════

class DetourageEngine:
    """Moteur d'exécution du pipeline de détourage."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def log(self, msg):
        if self.verbose:
            print(f"  {msg}")

    def run(self, input_path: str, output_path: str,
            analysis: ImageAnalysis, quality: str = "high") -> np.ndarray:
        """Exécute le pipeline complet et retourne le résultat RGBA."""

        img_pil = Image.open(input_path).convert("RGB")
        img_np = np.array(img_pil)
        h, w = img_np.shape[:2]
        img_norm = img_np.astype(np.float64) / 255.0

        # ── Étape 1 : Segmentation ──
        print("  ▸ Segmentation IA...")
        mask = self._segmentation(input_path, analysis.recommended_model)

        # ── Étape 2 : Trous + reconnexion ──
        print("  ▸ Classification des trous...")
        mask_bin = self._classify_holes(mask, h, w, analysis.recommended_hole_threshold)
        del mask; gc.collect()



        # ── Étape 3 : Trimap ──
        print("  ▸ Trimap adaptatif...")
        trimap = self._trimap(mask_bin, img_np,
                              analysis.recommended_erode,
                              analysis.recommended_dilate,
                              analysis.bg_type)

        # ── Étape 4 : Alpha Matting ──
        if quality == "low":
            print("  ▸ Masque binaire (qualité low)...")
            alpha = mask_bin.astype(np.float64) / 255.0
            foreground = img_norm
        else:
            print("  ▸ Alpha matting KNN...")
            alpha, img_s, alpha_s = self._alpha_matting(
                img_norm, trimap, analysis.recommended_matting_size)

            # ── Étape 5 : Décontamination ──
            if quality in ("high", "max"):
                print("  ▸ Décontamination couleur...")
                foreground = self._decontaminate(img_s, alpha_s, (w, h), img_norm, alpha)
                del img_s, alpha_s
            else:
                foreground = img_norm
                del img_s, alpha_s

        gc.collect()

        # ── Étape 6 : Nettoyage ──
        print("  ▸ Nettoyage morphologique...")
        alpha_u8 = self._cleanup(alpha)

        # ── Étape 7 : Assemblage ──
        print("  ▸ Assemblage RGBA...")
        fg_u8 = (foreground * 255).astype(np.uint8)
        result = np.dstack([fg_u8, alpha_u8])

        # ── Étape 7b : Détourage intérieur (trous dans disques, ouvertures) ──
        print("  ▸ Détourage intérieur (trous des objets)...")
        result = self._remove_interior_white(result, img_np)

        result_img = Image.fromarray(result, "RGBA")
        result_img.save(output_path, "PNG")

        return result

    def _segmentation(self, path, model):
        from rembg import remove, new_session
        models = [model, "isnet-general-use", "u2net"]
        seen = set()
        models = [m for m in models if not (m in seen or seen.add(m))]
        for m in models:
            try:
                session = new_session(m)
                with open(path, "rb") as f:
                    data = f.read()
                mask_bytes = remove(data, session=session, only_mask=True)
                mask = np.array(Image.open(io.BytesIO(mask_bytes)).convert("L"))
                self.log(f"Modèle {m} OK — mask {mask.shape}")
                del session, data, mask_bytes; gc.collect()
                return mask
            except Exception as e:
                self.log(f"Modèle {m} échoué: {e}")
                gc.collect()
        raise RuntimeError("Aucun modèle disponible")

    def _classify_holes(self, mask, h, w, threshold):
        mask_bin = (mask > 127).astype(np.uint8) * 255
        inv = cv2.bitwise_not(mask_bin)
        flood = inv.copy()
        fm = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(flood, fm, (0, 0), 128)
        interior = (flood == 255).astype(np.uint8) * 255
        nl, lab, stats, _ = cv2.connectedComponentsWithStats(interior)
        patched, kept = 0, 0
        for i in range(1, nl):
            if stats[i, cv2.CC_STAT_AREA] < threshold:
                mask_bin[lab == i] = 255
                patched += 1
            else:
                kept += 1
        self.log(f"Trous: {patched} bouchés, {kept} conservés")
        return mask_bin

    def _reconnect_non_white_objects(self, mask_bin, img_rgb):
        """Reconnecte les objets non-blancs au sujet principal.
        Technique clé : si un objet coloré (barre, disque) n'est pas dans le masque
        mais est connecté au sujet par des pixels non-blancs, l'ajouter."""
        from scipy import ndimage
        h, w = img_rgb.shape[:2]
        subject_core = mask_bin > 127

        # Tous les pixels non-blancs sont potentiellement du sujet
        r, g, b = img_rgb[:,:,0], img_rgb[:,:,1], img_rgb[:,:,2]
        is_not_white = ~((r > 230) & (g > 230) & (b > 230))

        # Trouver les composantes connexes non-blanches
        non_white_labeled, n_nw = ndimage.label(is_not_white)
        added = 0
        for label_id in range(1, n_nw + 1):
            component = non_white_labeled == label_id
            size = np.sum(component)
            overlap = np.sum(component & subject_core)
            # Si connecté au sujet OU assez gros pour être un objet réel
            if overlap > 0 or size > 500:
                new_pixels = np.sum(component & ~subject_core)
                if new_pixels > 0:
                    mask_bin[component] = 255
                    added += new_pixels

        # Dilatation minimale pour combler les micro-gaps
        if added > 0:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            mask_bin = cv2.dilate(mask_bin, kernel, iterations=1)
            self.log(f"Reconnexion: {added} pixels ajoutés au sujet")

        return mask_bin

    def _trimap(self, mask_bin, img_rgb, erode, dilate, bg_type):
        h, w = mask_bin.shape
        k_e = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * erode + 1,) * 2)
        k_d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * dilate + 1,) * 2)
        eroded = cv2.erode(mask_bin, k_e)
        dilated = cv2.dilate(mask_bin, k_d)
        trimap = np.full((h, w), 128, dtype=np.uint8)
        trimap[eroded >= 254] = 255
        trimap[dilated <= 1] = 0
        # Adaptation blanc-sur-blanc
        if bg_type in ("white", "light"):
            gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            wh = gray > 220
            unk = trimap == 128
            trimap[(wh & unk & (mask_bin > 127))] = 255
            trimap[(wh & unk & (mask_bin <= 127))] = 0
        n_unk = np.sum(trimap == 128)
        self.log(f"Trimap: {n_unk} pixels inconnus ({n_unk / (h * w) * 100:.1f}%)")
        return trimap

    def _alpha_matting(self, img_norm, trimap, matting_size):
        from pymatting import estimate_alpha_knn
        h, w = img_norm.shape[:2]
        scale = min(1.0, matting_size / max(h, w))
        nw, nh = int(w * scale), int(h * scale)
        img_s = cv2.resize(img_norm, (nw, nh))
        tri_s = cv2.resize(trimap.astype(np.float64) / 255.0, (nw, nh),
                           interpolation=cv2.INTER_NEAREST)
        self.log(f"Matting à {nw}×{nh}...")
        alpha_s = estimate_alpha_knn(img_s, tri_s)
        alpha = cv2.resize(alpha_s, (w, h), interpolation=cv2.INTER_LINEAR)
        return np.clip(alpha, 0, 1), img_s, alpha_s

    def _decontaminate(self, img_s, alpha_s, orig_size, img_norm, alpha):
        try:
            from pymatting import estimate_foreground_ml
            fg_s = estimate_foreground_ml(img_s, alpha_s)
            fg = cv2.resize(fg_s, orig_size, interpolation=cv2.INTER_LINEAR)
            return np.clip(fg, 0, 1)
        except Exception:
            self.log("Fallback décontamination manuelle")
            a_safe = np.where(alpha > 0.01, alpha, 1.0)
            fg = (img_norm - (1.0 - alpha[:, :, np.newaxis]) * 1.0) / a_safe[:, :, np.newaxis]
            return np.clip(fg, 0, 1)

    def _remove_interior_white(self, result, original_rgb):
        """Supprime les zones blanches à l'intérieur du sujet.
        Détecte les blobs blancs enclos (non connectés au fond transparent)
        et les rend transparents — ex: trous dans les disques de poids."""
        r, g, b, a = result[:,:,0], result[:,:,1], result[:,:,2], result[:,:,3]
        h, w = result.shape[:2]

        # Identifier les pixels blancs visibles
        is_white_visible = (r > 230) & (g > 230) & (b > 230) & (a > 200)

        # Labéliser les composantes connexes blanches
        n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            is_white_visible.astype(np.uint8))

        removed = 0
        for i in range(1, n_labels):
            component = labels == i
            ys, xs = np.where(component)
            size = len(ys)

            if size < 20:
                continue

            y_min, y_max = ys.min(), ys.max()
            x_min, x_max = xs.min(), xs.max()

            # Touche le bord de l'image = fond extérieur, ignorer
            if y_min == 0 or y_max == h - 1 or x_min == 0 or x_max == w - 1:
                continue

            # Protéger la zone chaussures/chaussettes (bas 30%)
            y_center = np.mean(ys)
            if y_center > h * 0.72:
                continue

            # Protéger le texte de la casquette (très haut, petit)
            if y_center < h * 0.15 and size < 200:
                continue

            # Ce blob est un trou intérieur → rendre transparent
            if size > 50:
                result[component, 3] = 0
                removed += 1

        self.log(f"Trous intérieurs: {removed} zones rendues transparentes")
        return result

    def _cleanup(self, alpha):
        a_u8 = (alpha * 255).astype(np.uint8)
        k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        a_u8 = cv2.morphologyEx(a_u8, cv2.MORPH_OPEN, k3)
        a_u8 = cv2.GaussianBlur(a_u8, (3, 3), 0)
        _, thr = cv2.threshold(a_u8, 10, 255, cv2.THRESH_BINARY)
        nl, cl, st, _ = cv2.connectedComponentsWithStats(thr)
        if nl > 1:
            sizes = st[1:, cv2.CC_STAT_AREA]
            largest = np.argmax(sizes) + 1
            a_u8[cl != largest] = 0
            self.log(f"Plus grand composant: {sizes[largest - 1]}px")
        return a_u8


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 3 — VÉRIFICATEUR DE QUALITÉ
# ═══════════════════════════════════════════════════════════════════════════

class QualityChecker:
    """Vérifie la qualité du détourage et identifie les défauts."""

    def check(self, result: np.ndarray, original: np.ndarray,
              pass_number: int = 1) -> QualityReport:
        """Analyse la qualité du résultat RGBA."""
        h, w = result.shape[:2]
        r, g, b, a = result[:, :, 0], result[:, :, 1], result[:, :, 2], result[:, :, 3]

        report = QualityReport(pass_number=pass_number)
        report.total_pixels = h * w
        report.visible_pixels = int(np.sum(a > 0))
        report.transparent_pixels = int(np.sum(a == 0))
        report.semi_transparent_pixels = int(np.sum((a > 10) & (a < 240)))

        # Détection du halo : pixels blancs visibles en bordure du sujet
        visible = a > 0
        eroded = cv2.erode(visible.astype(np.uint8), np.ones((5, 5), np.uint8))
        border = visible & ~eroded.astype(bool)
        white_border = border & (r > 220) & (g > 220) & (b > 220) & (a > 100)
        report.halo_pixels = int(np.sum(white_border))

        halo_ratio = report.halo_pixels / max(np.sum(border), 1)
        if halo_ratio < 0.05:
            report.halo_severity = "none"
        elif halo_ratio < 0.15:
            report.halo_severity = "light"
        elif halo_ratio < 0.30:
            report.halo_severity = "moderate"
        else:
            report.halo_severity = "severe"

        # Blobs blancs intérieurs
        white_visible = (r > 235) & (g > 235) & (b > 235) & (a > 200)
        white_interior = white_visible & eroded.astype(bool)
        n_wl, wl = cv2.connectedComponents(white_interior.astype(np.uint8))
        # Filtrer les petits blobs (< 100px)
        large_blobs = 0
        for i in range(1, n_wl):
            if np.sum(wl == i) > 100:
                large_blobs += 1
        report.interior_white_blobs = large_blobs

        # Préservation du sujet (comparaison avec l'original)
        orig_gray = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        non_white_orig = orig_gray < 210  # Seuil plus permissif (peau claire ok)
        non_white_preserved = non_white_orig & (a > 100)
        report.subject_preserved_pct = np.sum(non_white_preserved) / max(np.sum(non_white_orig), 1) * 100

        # Lissage des bords
        if np.sum(border) > 0:
            border_alpha = a[border]
            smoothness = np.std(border_alpha.astype(float)) / 128.0
            report.edge_smoothness = min(smoothness, 1.0)
        else:
            report.edge_smoothness = 0.0

        # Score global (0-10)
        score = 10.0
        if report.halo_severity == "light":
            score -= 1
        elif report.halo_severity == "moderate":
            score -= 2.5
        elif report.halo_severity == "severe":
            score -= 4
        if report.interior_white_blobs > 0:
            score -= min(report.interior_white_blobs * 0.5, 2)
        if report.subject_preserved_pct < 95:
            score -= (95 - report.subject_preserved_pct) * 0.1
        score = max(0, score)
        report.overall_score = round(score, 1)

        # Issues et suggestions
        if report.halo_severity in ("moderate", "severe"):
            report.issues.append(f"Halo blanc {report.halo_severity} ({report.halo_pixels}px)")
            report.suggestions.append("Passe corrective : érosion ciblée des bords blancs")
        if report.interior_white_blobs > 0:
            report.issues.append(f"{report.interior_white_blobs} blobs blancs intérieurs")
            report.suggestions.append("Passe corrective : suppression des blobs blancs isolés")
        if report.subject_preserved_pct < 90:
            report.issues.append(f"Sujet partiellement coupé ({report.subject_preserved_pct:.0f}%)")
            report.suggestions.append("Élargir le trimap (augmenter dilate)")

        return report

    def print_report(self, report: QualityReport):
        print("╔══════════════════════════════════════════════╗")
        print(f"║      RAPPORT QUALITÉ — Passe {report.pass_number:<14}  ║")
        print("╠══════════════════════════════════════════════╣")
        print(f"║ Score global     : {report.overall_score}/10")
        sev = {"none": "✅ Aucun", "light": "⚠️  Léger", "moderate": "🟠 Modéré", "severe": "🔴 Sévère"}
        print(f"║ Halo blanc       : {sev.get(report.halo_severity)} ({report.halo_pixels}px)")
        print(f"║ Blobs intérieurs : {report.interior_white_blobs}")
        print(f"║ Sujet préservé   : {report.subject_preserved_pct:.1f}%")
        print(f"║ Semi-transparents: {report.semi_transparent_pixels}")
        print(f"║ Lissage bords    : {report.edge_smoothness:.2f}")
        if report.issues:
            print("╠══════════════════════════════════════════════╣")
            for issue in report.issues:
                print(f"║ ⚠ {issue}")
        if report.suggestions:
            print("╠══════════════════════════════════════════════╣")
            for sug in report.suggestions:
                print(f"║ → {sug}")
        print("╚══════════════════════════════════════════════╝")


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 4 — CORRECTEUR AUTOMATIQUE
# ═══════════════════════════════════════════════════════════════════════════

class AutoCorrector:
    """Applique des corrections ciblées basées sur le rapport qualité."""

    def correct(self, result: np.ndarray, report: QualityReport,
                verbose: bool = True) -> np.ndarray:
        """Applique les corrections nécessaires."""
        corrected = result.copy()
        corrections = 0

        # Correction 1 : Halo blanc
        if report.halo_severity in ("moderate", "severe"):
            corrected = self._fix_halo(corrected, verbose)
            corrections += 1

        # Correction 2 : Blobs blancs intérieurs
        if report.interior_white_blobs > 0:
            corrected = self._fix_interior_blobs(corrected, verbose)
            corrections += 1

        if verbose:
            print(f"  → {corrections} correction(s) appliquée(s)")

        return corrected

    def _fix_halo(self, data: np.ndarray, verbose: bool) -> np.ndarray:
        """Érosion ciblée des pixels blancs en bordure."""
        if verbose:
            print("  ▸ Correction halo : érosion des bords blancs...")
        r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
        visible = a > 0

        for _ in range(2):
            eroded = cv2.erode(visible.astype(np.uint8), np.ones((3, 3), np.uint8))
            outer_edge = visible & ~eroded.astype(bool)
            white_edge = outer_edge & (r > 210) & (g > 210) & (b > 210)
            data[white_edge, 3] = 0
            visible = data[:, :, 3] > 0

        # Anti-alias final
        eroded2 = cv2.erode(visible.astype(np.uint8), np.ones((3, 3), np.uint8))
        edge2 = visible & ~eroded2.astype(bool)
        near_white = edge2 & (r > 200) & (g > 200) & (b > 200)
        data[near_white, 3] = np.clip(data[near_white, 3].astype(int) - 80, 0, 255).astype(np.uint8)

        return data

    def _fix_interior_blobs(self, data: np.ndarray, verbose: bool) -> np.ndarray:
        """Supprime les blobs blancs isolés à l'intérieur du sujet.
        Utilise la connectivité au fond transparent pour ne cibler que les
        vrais résidus de fond, pas les éléments blancs du sujet."""
        if verbose:
            print("  ▸ Correction blobs : analyse contextuelle...")
        r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
        h, w = data.shape[:2]

        white_visible = (r > 235) & (g > 235) & (b > 235) & (a > 200)
        n_wl, wl = cv2.connectedComponents(white_visible.astype(np.uint8))

        # Identifier les zones transparentes (fond) pour contexte
        is_transparent = a < 10

        removed = 0
        for i in range(1, n_wl):
            component = wl == i
            ys, xs = np.where(component)
            size = len(ys)

            if size < 80:
                continue

            # Ne pas toucher les bords de l'image
            if ys.min() == 0 or ys.max() == h - 1 or xs.min() == 0 or xs.max() == w - 1:
                continue

            y_center = np.mean(ys)
            y_min, y_max = ys.min(), ys.max()
            x_min, x_max = xs.min(), xs.max()

            # Protéger la zone chaussures (bas 30%)
            if y_center > h * 0.70:
                continue

            # Vérifier si ce blob est adjacent à du transparent (= résidu de fond)
            # Dilater le blob de 5px et checker le voisinage
            blob_mask = component.astype(np.uint8)
            dilated = cv2.dilate(blob_mask, np.ones((11, 11), np.uint8))
            neighborhood = (dilated > 0) & ~component
            adjacent_transparent = np.sum(is_transparent & neighborhood)
            adjacent_total = max(np.sum(neighborhood), 1)
            transparency_ratio = adjacent_transparent / adjacent_total

            # Supprimer si : entouré de transparent (résidu de fond)
            # OU petit blob isolé dans la zone supérieure
            if transparency_ratio > 0.3 or (size < 500 and y_center < h * 0.50):
                data[component, 3] = 0
                removed += 1

        if verbose:
            print(f"    {removed} blobs supprimés (analyse contextuelle)")
        return data


# ═══════════════════════════════════════════════════════════════════════════
# ORCHESTRATEUR PRINCIPAL — DetourAgent
# ═══════════════════════════════════════════════════════════════════════════

class DetourAgent:
    """
    Agent principal qui orchestre le détourage de bout en bout :
    analyse → exécution → vérification → correction → livraison
    """

    def __init__(self, quality: str = "high", max_passes: int = 3,
                 verbose: bool = True):
        self.quality = quality
        self.max_passes = max_passes
        self.verbose = verbose
        self.analyzer = ImageAnalyzer()
        self.engine = DetourageEngine(verbose=verbose)
        self.checker = QualityChecker()
        self.corrector = AutoCorrector()

    def process(self, input_path: str, output_path: str,
                check_bg: Tuple[int, int, int] = (50, 150, 230)) -> QualityReport:
        """Traite une image avec le pipeline adaptatif multi-passes."""
        t0 = time.time()

        print("═" * 50)
        print("  DetourAgent — Détourage Professionnel")
        print("═" * 50)

        # ── Phase 1 : Analyse ──
        print("\n📊 PHASE 1 — Analyse de l'image")
        analysis = self.analyzer.analyze(input_path, self.verbose)

        # Ajuster les recommandations selon le niveau de qualité
        if self.quality == "max":
            analysis.recommended_matting_size = min(768, max(analysis.width, analysis.height))
        elif self.quality == "low":
            analysis.recommended_matting_size = 384

        # ── Phase 2 : Détourage initial ──
        print("\n🎯 PHASE 2 — Détourage (passe 1)")
        result = self.engine.run(input_path, output_path, analysis, self.quality)

        # Charger l'original pour comparaison
        original = np.array(Image.open(input_path).convert("RGB"))

        # ── Phase 3 : Vérification + correction en boucle ──
        best_result = result
        best_report = None

        for pass_num in range(1, self.max_passes + 1):
            print(f"\n🔍 PHASE 3 — Vérification qualité (passe {pass_num})")
            report = self.checker.check(best_result, original, pass_num)
            self.checker.print_report(report)

            if best_report is None or report.overall_score > best_report.overall_score:
                best_report = report

            # Si qualité suffisante, arrêter
            if report.overall_score >= 8.0 or not report.issues:
                print(f"\n✅ Qualité satisfaisante ({report.overall_score}/10)")
                break

            # Sinon, corriger
            if pass_num < self.max_passes:
                print(f"\n🔧 PHASE 4 — Correction automatique (passe {pass_num})")
                best_result = self.corrector.correct(best_result, report, self.verbose)

                # Sauvegarder la version corrigée
                corrected_img = Image.fromarray(best_result, "RGBA")
                corrected_img.save(output_path, "PNG")

        # ── Sauvegarde finale ──
        final_img = Image.fromarray(best_result, "RGBA")
        final_img.save(output_path, "PNG")

        # Image de contrôle
        if check_bg:
            check_path = str(Path(output_path).with_suffix("")) + "_check.png"
            bg = Image.new("RGBA", final_img.size, (*check_bg, 255))
            composite = Image.alpha_composite(bg, final_img)
            composite.save(check_path)

        elapsed = time.time() - t0

        print("\n" + "═" * 50)
        print(f"  ✓ Terminé en {elapsed:.1f}s")
        print(f"  ✓ Score final : {best_report.overall_score}/10")
        print(f"  ✓ Sortie : {output_path}")
        print("═" * 50)

        return best_report

    def process_batch(self, input_dir: str, output_dir: str,
                      check_bg: Tuple[int, int, int] = (50, 150, 230)) -> List[dict]:
        """Traite un dossier d'images."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
        images = [f for f in input_path.iterdir()
                  if f.suffix.lower() in extensions]

        print(f"\n📁 Batch : {len(images)} images à traiter")
        results = []

        for i, img_path in enumerate(images, 1):
            print(f"\n{'─' * 50}")
            print(f"  Image {i}/{len(images)} : {img_path.name}")
            print(f"{'─' * 50}")

            out = output_path / f"{img_path.stem}_detoured.png"
            try:
                report = self.process(str(img_path), str(out), check_bg)
                results.append({
                    "file": img_path.name,
                    "status": "ok",
                    "score": report.overall_score,
                    "issues": report.issues,
                })
            except Exception as e:
                print(f"  ❌ Erreur : {e}")
                results.append({
                    "file": img_path.name,
                    "status": "error",
                    "error": str(e),
                })

        # Résumé
        ok = [r for r in results if r["status"] == "ok"]
        avg_score = np.mean([r["score"] for r in ok]) if ok else 0
        print(f"\n{'═' * 50}")
        print(f"  BATCH TERMINÉ : {len(ok)}/{len(images)} réussis")
        print(f"  Score moyen : {avg_score:.1f}/10")
        print(f"{'═' * 50}")

        # Sauvegarder le rapport
        report_path = output_path / "batch_report.json"
        with open(report_path, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return results


# ═══════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="DetourAgent — Agent spécialisé de détourage professionnel")
    parser.add_argument("input", help="Image source ou dossier (avec --batch)")
    parser.add_argument("output", help="Image de sortie ou dossier (avec --batch)")
    parser.add_argument("--quality", default="high",
                        choices=["low", "medium", "high", "max"],
                        help="Niveau de qualité (défaut: high)")
    parser.add_argument("--max-passes", type=int, default=3,
                        help="Nombre max de passes correctives (défaut: 3)")
    parser.add_argument("--check-bg", default="50,150,230",
                        help="Couleur du fond de contrôle (défaut: 50,150,230)")
    parser.add_argument("--no-check", action="store_true",
                        help="Ne pas générer l'image de contrôle")
    parser.add_argument("--batch", action="store_true",
                        help="Traitement par lots d'un dossier")
    parser.add_argument("--verbose", "-v", action="store_true", default=True)
    parser.add_argument("--quiet", "-q", action="store_true")

    args = parser.parse_args()
    if args.quiet:
        args.verbose = False

    check_bg = None if args.no_check else tuple(int(c) for c in args.check_bg.split(","))

    agent = DetourAgent(
        quality=args.quality,
        max_passes=args.max_passes,
        verbose=args.verbose,
    )

    if args.batch:
        agent.process_batch(args.input, args.output, check_bg)
    else:
        agent.process(args.input, args.output, check_bg)


if __name__ == "__main__":
    main()
