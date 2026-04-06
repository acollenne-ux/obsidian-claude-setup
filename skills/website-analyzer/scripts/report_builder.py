#!/usr/bin/env python3
"""
Report Builder — Assembles the final audit report in Markdown format.
Takes crawler data + agent scores and produces a structured Markdown report
ready for pdf-report-gen or send_report.py.

Usage:
    python report_builder.py --crawl-data <path/crawl_results.json> --summary <path/summary.json> --scores <path/scores.json> --output <rapport.md>
"""

import argparse
import json
import os
import sys
import time


def load_json(path):
    """Load a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_global_score(scores, mode="A"):
    """Calculate weighted global score based on mode."""
    weights = {
        "A": {
            "esthetique": 0.15, "ux_ergonomie": 0.12, "responsive": 0.10,
            "identite_marque": 0.12, "seo_technique": 0.10, "contenu": 0.10,
            "performance": 0.08, "conversion": 0.13, "accessibilite": 0.05,
            "conformite": 0.05,
        },
        "B": {
            "identite_marque": 0.15, "seo_technique": 0.20, "contenu": 0.20,
            "performance": 0.15, "conversion": 0.20, "conformite": 0.10,
        },
        "C": {
            "esthetique": 0.25, "ux_ergonomie": 0.25, "responsive": 0.15,
            "identite_marque": 0.20, "accessibilite": 0.15,
        },
    }

    mode_weights = weights.get(mode.upper(), weights["A"])
    total = 0
    for dim, weight in mode_weights.items():
        score = scores.get(dim, {}).get("score", 5)
        total += score * weight

    return round(total * 10, 1)  # Convert to /100


def score_to_grade(score):
    """Convert numeric score to letter grade."""
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def build_report(crawl_data, summary, scores, mode="A", site_name=""):
    """Build the complete Markdown report."""
    global_score = calculate_global_score(scores, mode)
    grade = score_to_grade(global_score)
    date = time.strftime("%d/%m/%Y")

    if not site_name:
        site_name = summary.get("base_url", "Site inconnu")

    mode_labels = {"A": "Audit complet 360°", "B": "Focus Marketing & Ventes", "C": "Focus Design & Branding"}
    mode_label = mode_labels.get(mode.upper(), "Audit complet 360°")

    # Build report
    report = []
    report.append(f"# Audit Web — {site_name}")
    report.append(f"\n**Date :** {date}")
    report.append(f"**URL :** {summary.get('base_url', 'N/A')}")
    report.append(f"**Mode d'analyse :** {mode_label}")
    report.append(f"**Pages analysées :** {summary.get('total_pages', 0)}")
    report.append(f"**Durée du crawl :** {summary.get('elapsed_seconds', 0)}s")

    # Executive Summary
    report.append("\n---\n")
    report.append("## Executive Summary")
    report.append(f"\n**Score global : {global_score}/100 ({grade})**\n")

    # Score interpretation
    if global_score >= 80:
        interpretation = "Site de bonne qualité avec quelques optimisations possibles."
    elif global_score >= 60:
        interpretation = "Site correct mais avec des axes d'amélioration significatifs."
    elif global_score >= 40:
        interpretation = "Site en dessous des standards — refonte partielle recommandée."
    else:
        interpretation = "Site avec des problèmes majeurs — refonte importante nécessaire."
    report.append(f"*{interpretation}*\n")

    # Top forces / faiblesses
    sorted_dims = sorted(scores.items(), key=lambda x: x[1].get("score", 0), reverse=True)
    forces = [d for d in sorted_dims if d[1].get("score", 0) >= 7][:5]
    faiblesses = [d for d in sorted_dims if d[1].get("score", 0) <= 5][:5]

    if forces:
        report.append("### Points forts")
        for dim, data in forces:
            report.append(f"- **{data.get('label', dim)}** : {data.get('score', 'N/A')}/10 — {data.get('summary_positive', '')}")

    if faiblesses:
        report.append("\n### Points faibles")
        for dim, data in faiblesses:
            report.append(f"- **{data.get('label', dim)}** : {data.get('score', 'N/A')}/10 — {data.get('summary_negative', '')}")

    # Scores tableau
    report.append("\n---\n")
    report.append("## Scores par dimension\n")
    report.append("| Dimension | Score | Niveau |")
    report.append("|-----------|-------|--------|")
    for dim, data in sorted_dims:
        score = data.get("score", "N/A")
        label = data.get("label", dim)
        if isinstance(score, (int, float)):
            if score >= 8:
                level = "Excellent"
            elif score >= 6:
                level = "Bon"
            elif score >= 4:
                level = "Insuffisant"
            else:
                level = "Critique"
        else:
            level = "N/A"
        report.append(f"| {label} | {score}/10 | {level} |")

    report.append(f"\n**Score global pondéré : {global_score}/100 ({grade})**")

    # Detailed analysis per dimension
    report.append("\n---\n")
    report.append("## Analyse détaillée\n")

    for dim, data in sorted_dims:
        label = data.get("label", dim)
        score = data.get("score", "N/A")
        report.append(f"### {label} — {score}/10\n")

        if data.get("positives"):
            report.append("**Points positifs :**")
            for p in data["positives"]:
                report.append(f"- {p}")
            report.append("")

        if data.get("negatives"):
            report.append("**Points négatifs :**")
            for n in data["negatives"]:
                report.append(f"- {n}")
            report.append("")

        if data.get("recommendations"):
            report.append("**Recommandations :**")
            for i, rec in enumerate(data["recommendations"], 1):
                report.append(f"{i}. {rec}")
            report.append("")

    # Site structure
    report.append("\n---\n")
    report.append("## Structure du site\n")
    report.append("| Page | Type | Profondeur | Temps chargement |")
    report.append("|------|------|-----------|-----------------|")

    for page in crawl_data[:50]:
        url = page.get("url", "N/A")
        # Shorten URL for display
        path = urlparse_path(url)
        cls = page.get("classification", "N/A")
        depth = page.get("depth", "N/A")
        load = page.get("load_time_ms", "N/A")
        load_str = f"{load}ms" if isinstance(load, (int, float)) else "N/A"
        report.append(f"| {path} | {cls} | {depth} | {load_str} |")

    # Technical summary from crawler
    if summary.get("pages_with_issues"):
        issues = summary["pages_with_issues"]
        report.append("\n### Problèmes techniques détectés\n")
        report.append(f"- Pages sans titre : {issues.get('missing_title', 0)}")
        report.append(f"- Pages sans méta-description : {issues.get('missing_meta_desc', 0)}")
        report.append(f"- Pages sans H1 : {issues.get('missing_h1', 0)}")
        report.append(f"- Pages sans canonical : {issues.get('no_canonical', 0)}")
        report.append(f"- Pages sans Open Graph : {issues.get('no_og_tags', 0)}")
        report.append(f"- Pages sans Schema.org : {issues.get('no_schema', 0)}")
        report.append(f"- Pages lentes (> 3s) : {issues.get('slow_pages', 0)}")

    # Fonts detected
    if summary.get("all_fonts"):
        report.append(f"\n### Polices détectées\n")
        for font in summary["all_fonts"]:
            report.append(f"- {font}")

    # Recommendations roadmap
    report.append("\n---\n")
    report.append("## Roadmap de recommandations\n")
    report.append("### P1 — Quick Wins (< 1 semaine)\n")
    report.append("*Recommandations à fort impact et faible effort, à implémenter immédiatement.*\n")

    p1_recs = []
    for dim, data in sorted_dims:
        for rec in data.get("recommendations", []):
            if "P1" in rec:
                p1_recs.append(f"- {rec}")
    if p1_recs:
        report.extend(p1_recs)
    else:
        report.append("- *Voir les recommandations détaillées par dimension ci-dessus.*")

    report.append("\n### P2 — Projets stratégiques (1-3 mois)\n")
    report.append("*Chantiers importants nécessitant plus de ressources.*\n")

    p2_recs = []
    for dim, data in sorted_dims:
        for rec in data.get("recommendations", []):
            if "P2" in rec:
                p2_recs.append(f"- {rec}")
    if p2_recs:
        report.extend(p2_recs)
    else:
        report.append("- *Voir les recommandations détaillées par dimension ci-dessus.*")

    report.append("\n### P3-P4 — Améliorations et backlog\n")
    report.append("*Optimisations secondaires à planifier.*\n")
    report.append("- *Voir les recommandations détaillées par dimension ci-dessus.*")

    # Footer
    report.append("\n---\n")
    report.append(f"*Rapport généré le {date} par Website Analyzer — Claude Code*")

    return "\n".join(report)


def urlparse_path(url):
    """Extract clean path from URL for display."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path = parsed.path or "/"
        return path[:60] + ("..." if len(path) > 60 else "")
    except Exception:
        return url[:60]


def main():
    parser = argparse.ArgumentParser(description="Website Audit Report Builder")
    parser.add_argument("--crawl-data", required=True, help="Path to crawl_results.json")
    parser.add_argument("--summary", required=True, help="Path to summary.json")
    parser.add_argument("--scores", required=True, help="Path to scores.json (agent results)")
    parser.add_argument("--output", default="./audit_report.md", help="Output Markdown file")
    parser.add_argument("--mode", default="A", choices=["A", "B", "C"], help="Analysis mode")
    parser.add_argument("--site-name", default="", help="Site name for the report title")

    args = parser.parse_args()

    # Load data
    crawl_data = load_json(args.crawl_data)
    summary = load_json(args.summary)
    scores = load_json(args.scores)

    # Build report
    report = build_report(crawl_data, summary, scores, args.mode, args.site_name)

    # Save
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[REPORT] Rapport généré : {args.output}")
    print(f"[REPORT] Taille : {len(report)} caractères")


if __name__ == "__main__":
    main()
