#!/usr/bin/env python3
"""
run_gate.py — Orchestrateur de la porte layout-qa.

Pipeline : rasterize → layout_check → (stub) vision critique → verdict.
La phase vision réelle est confiée à l'agent visual-layout-critic côté Claude ;
ce script produit l'agrégation déterministe et le verdict géométrique.

Usage:
    python run_gate.py --input <livrable> [--brief brief.md]
                       [--caller <skill>] [--max-iter 3]
                       [--out-report qa_report.json]

Exit codes: 0=PASS, 1=FIX, 2=FAIL.
"""

import argparse
import json
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).parent
TMP_ROOT = Path.home() / ".claude" / "tmp" / "layout_qa"


def _verdict(geom: dict) -> str:
    crit = geom.get("critical", 0)
    high = geom.get("high", 0)
    if crit > 0:
        return "FAIL"
    if high > 0 or geom.get("anomaly_count", 0) > 3:
        return "FIX"
    return "PASS"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--brief", default=None)
    ap.add_argument("--caller", default="unknown")
    ap.add_argument("--max-iter", type=int, default=3)
    ap.add_argument("--out-report", default=None)
    args = ap.parse_args()

    run_id = uuid.uuid4().hex[:8]
    work = TMP_ROOT / run_id
    work.mkdir(parents=True, exist_ok=True)

    # Phase 1 — Rasterize
    ras_dir = work / "pages"
    r = subprocess.run(
        [sys.executable, str(HERE / "rasterize.py"),
         args.input, "--out", str(ras_dir)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"rasterize failed: {r.stderr}", file=sys.stderr)
        return 2

    # Phase 2 — Geometric check
    geom_path = work / "geom.json"
    subprocess.run(
        [sys.executable, str(HERE / "layout_check.py"),
         args.input,
         *(["--brief", args.brief] if args.brief else []),
         "--out", str(geom_path)],
        check=True,
    )
    geom = json.loads(geom_path.read_text(encoding="utf-8"))

    # Phase 3 — vision : réalisée par Claude côté skill (agent visual-layout-critic)
    # Ce script signale où lire les PNG.
    verdict = _verdict(geom)

    # Phase 4 — Annotate si non-PASS
    annotated_dir = None
    if verdict != "PASS":
        annotated_dir = work / "annotated"
        subprocess.run(
            [sys.executable, str(HERE / "annotate.py"),
             "--pages", str(ras_dir),
             "--anomalies", str(geom_path),
             "--out", str(annotated_dir)],
        )

    report = {
        "run_id": run_id,
        "caller": args.caller,
        "input": args.input,
        "brief": args.brief,
        "verdict": verdict,
        "geometric": geom,
        "vision_phase": "DEFERRED_TO_CLAUDE_AGENT visual-layout-critic",
        "pages_dir": str(ras_dir),
        "annotated_dir": str(annotated_dir) if annotated_dir else None,
        "max_iter": args.max_iter,
    }
    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out_report:
        Path(args.out_report).write_text(payload, encoding="utf-8")
    print(payload)

    return {"PASS": 0, "FIX": 1, "FAIL": 2}[verdict]


if __name__ == "__main__":
    sys.exit(main())
