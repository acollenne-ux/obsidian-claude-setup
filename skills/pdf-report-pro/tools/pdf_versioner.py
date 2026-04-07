"""pdf_versioner.py — Versionnement sémantique des rapports

Usage: python pdf_versioner.py <pdf> <slug> [--bump major|minor|patch]
Crée ~/Documents/reports/<slug>/v<X.Y>/ avec metadata.yaml et CHANGELOG.md.
"""
from __future__ import annotations
import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml

REPORTS_ROOT = Path.home() / "Documents" / "reports"


def next_version(slug_dir: Path, bump: str) -> str:
    if not slug_dir.exists():
        return "1.0"
    versions = sorted(
        [p.name for p in slug_dir.iterdir() if p.is_dir() and p.name.startswith("v")],
        key=lambda v: tuple(int(x) for x in v[1:].split(".")),
    )
    if not versions:
        return "1.0"
    last = versions[-1][1:]
    major, minor = (int(x) for x in last.split("."))
    if bump == "major":
        return f"{major + 1}.0"
    return f"{major}.{minor + 1}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("slug")
    ap.add_argument("--bump", choices=["major", "minor"], default="minor")
    ap.add_argument("--template", default="institutional_report")
    ap.add_argument("--engine", default="typst")
    ap.add_argument("--reviewer-score", type=int, default=0)
    ap.add_argument("--accessibility-score", type=int, default=0)
    args = ap.parse_args()

    pdf = Path(args.pdf)
    if not pdf.exists():
        print(f"[ERR] PDF introuvable: {pdf}")
        sys.exit(1)

    slug_dir = REPORTS_ROOT / args.slug
    version = next_version(slug_dir, args.bump)
    target = slug_dir / f"v{version}"
    target.mkdir(parents=True, exist_ok=True)

    shutil.copy(pdf, target / "report.pdf")

    metadata = {
        "report": {
            "slug": args.slug,
            "version": version,
            "template": args.template,
            "engine": args.engine,
            "reviewer_score": args.reviewer_score,
            "accessibility_score": args.accessibility_score,
            "delivered_at": datetime.now().isoformat(timespec="seconds"),
        }
    }
    (target / "metadata.yaml").write_text(
        yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )

    changelog = slug_dir / "CHANGELOG.md"
    entry = f"\n## v{version} — {datetime.now().date()}\n- Reviewer: {args.reviewer_score}/100\n- A11y: {args.accessibility_score}/20\n"
    if changelog.exists():
        changelog.write_text(changelog.read_text(encoding="utf-8") + entry, encoding="utf-8")
    else:
        changelog.write_text(f"# Changelog — {args.slug}\n{entry}", encoding="utf-8")

    print(f"[OK] {target}")


if __name__ == "__main__":
    main()
