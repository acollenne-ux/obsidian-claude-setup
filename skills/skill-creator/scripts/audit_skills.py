#!/usr/bin/env python3
"""
Audit automatisé des skills Claude Code.
Score qualité sur 10 critères pondérés.

Usage:
    python audit_skills.py                    # Auditer tous les skills
    python audit_skills.py skill-name         # Auditer un skill spécifique
    python audit_skills.py --json             # Sortie JSON
    python audit_skills.py --summary          # Résumé rapide
"""

import os
import re
import sys
import json
import io
from pathlib import Path

# Fix Windows cp1252 encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SKILLS_DIR = Path.home() / ".claude" / "skills"

# Poids des critères
WEIGHTS = {
    "frontmatter": 1.0,
    "hard_gates": 1.5,
    "anti_patterns": 1.0,
    "checklist": 1.0,
    "flowchart": 0.5,
    "cross_links": 1.0,
    "concision": 1.0,
    "testability": 1.0,
    "domain": 1.0,
    "evolution": 1.0,
}

MAX_SCORE = sum(10 * w for w in WEIGHTS.values())  # 100


def read_skill(skill_path: Path) -> str:
    """Lire le contenu du SKILL.md."""
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return ""
    return skill_file.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(content: str) -> dict:
    """Extraire le frontmatter YAML."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def score_frontmatter(content: str) -> tuple[int, str]:
    """Critère 1: Frontmatter."""
    fm = parse_frontmatter(content)
    if not fm:
        return 0, "Pas de frontmatter YAML"
    if "name" not in fm or "description" not in fm:
        return 2, "Frontmatter incomplet"
    desc = fm.get("description", "")
    has_hint = "argument-hint" in fm
    if len(desc) <= 250 and has_hint:
        return 10, "Complet avec triggers et hint"
    if len(desc) <= 250:
        return 7, "Name+desc OK, <250 chars"
    return 5, f"Description trop longue ({len(desc)} chars)"


def score_hard_gates(content: str) -> tuple[int, str]:
    """Critère 2: Hard-gates."""
    has_tag = "<HARD-GATE>" in content or "<hard-gate>" in content.lower()
    imperative_words = sum(1 for w in ["JAMAIS", "TOUJOURS", "OBLIGATOIRE", "NEVER", "MUST", "ALWAYS"]
                          if w in content.upper())
    if has_tag and imperative_words >= 3:
        return 10, f"Hard-gate + {imperative_words} règles impératives"
    if has_tag:
        return 7, "Hard-gate présent"
    if imperative_words >= 2:
        return 5, f"Règles impératives ({imperative_words}) mais pas de <HARD-GATE>"
    if imperative_words >= 1:
        return 3, "Règles floues"
    return 0, "Aucun hard-gate"


def score_anti_patterns(content: str) -> tuple[int, str]:
    """Critère 3: Anti-patterns."""
    has_anti = bool(re.search(r"(?i)anti.?pattern|excuse.*réalité|excuse.*reality", content))
    has_red_flags = bool(re.search(r"(?i)red.?flag|stop.*corrig|stop.*start", content))
    has_table = bool(re.search(r"\|.*\|.*\|.*\|", content)) and has_anti
    if has_table and has_red_flags:
        return 10, "Table anti-patterns + Red Flags"
    if has_table:
        return 7, "Table anti-patterns"
    if has_anti:
        return 5, "Section anti-patterns"
    if has_red_flags:
        return 5, "Section Red Flags"
    return 0, "Aucun anti-pattern documenté"


def score_checklist(content: str) -> tuple[int, str]:
    """Critère 4: Checklist."""
    numbered = len(re.findall(r"^\d+\.\s+\*\*", content, re.MULTILINE))
    has_todo = "TodoWrite" in content or "todo" in content.lower()
    if numbered >= 3 and has_todo:
        return 10, f"Checklist {numbered} étapes + TodoWrite"
    if numbered >= 3:
        return 7, f"Checklist {numbered} étapes numérotées"
    if numbered >= 1:
        return 5, f"Checklist partielle ({numbered} étapes)"
    return 0, "Pas de checklist"


def score_flowchart(content: str) -> tuple[int, str]:
    """Critère 5: Flowchart."""
    has_graphviz = "digraph" in content or "```dot" in content
    has_mermaid = "```mermaid" in content
    if has_graphviz:
        return 10, "Diagramme Graphviz"
    if has_mermaid:
        return 8, "Diagramme Mermaid"
    has_arrows = content.count("→") + content.count("->")
    if has_arrows >= 3:
        return 5, f"Flux textuel ({has_arrows} flèches)"
    return 0, "Pas de visualisation du flux"


def score_cross_links(content: str) -> tuple[int, str]:
    """Critère 6: Cross-links."""
    skill_refs = len(re.findall(r"`[a-z][\w-]+(?::[a-z][\w-]+)?`", content))
    has_section = bool(re.search(r"(?i)cross.?link|skills?.?li[ée]|chaîn", content))
    has_table = bool(re.search(r"(?i)\|\s*(contexte|avant|après|skill)", content))
    if has_table and skill_refs >= 4:
        return 10, f"Table cross-links + {skill_refs} refs"
    if has_section and skill_refs >= 3:
        return 7, f"Section dédiée + {skill_refs} refs"
    if skill_refs >= 2:
        return 5, f"{skill_refs} références à d'autres skills"
    if skill_refs >= 1:
        return 3, f"{skill_refs} référence"
    return 0, "Skill isolé"


def score_concision(content: str) -> tuple[int, str]:
    """Critère 7: Concision."""
    lines = len(content.strip().split("\n"))
    if 100 <= lines <= 300:
        return 10, f"{lines} lignes (zone idéale)"
    if 301 <= lines <= 400 or 40 <= lines <= 99:
        return 7, f"{lines} lignes (acceptable)"
    if 401 <= lines <= 500:
        return 5, f"{lines} lignes (envisager references/)"
    if lines < 40:
        return 3, f"{lines} lignes (trop court)"
    return 2, f"{lines} lignes (trop long, décomposer)"


def score_testability(content: str) -> tuple[int, str]:
    """Critère 8: Testabilité."""
    fm = parse_frontmatter(content)
    desc = fm.get("description", "")
    has_triggers = bool(re.search(r"(?i)trigger|use when|déclenche", desc))
    has_scenarios = bool(re.search(r"(?i)no.?trigger|scénario|scenario|evals\.json", content))
    if has_triggers and has_scenarios:
        return 10, "Triggers + scénarios de test"
    if has_triggers:
        return 7, "Triggers définis dans description"
    if has_scenarios:
        return 5, "Scénarios sans triggers explicites"
    return 0, "Non testable"


def score_domain(content: str) -> tuple[int, str]:
    """Critère 9: Adaptation au domaine."""
    domain_markers = {
        "process": ["phase", "étape", "checklist", "workflow"],
        "analysis": ["dimension", "pondération", "scoring", "matrice"],
        "debug": ["root cause", "stack trace", "hypothès", "confiance"],
        "orchestrator": ["dispatch", "routage", "routing", "agent"],
        "creative": ["brief", "prototype", "variante", "export"],
        "audit": ["grille", "scoring", "seuil", "recommandation"],
    }
    detected = {}
    content_lower = content.lower()
    for domain, markers in domain_markers.items():
        count = sum(1 for m in markers if m in content_lower)
        if count >= 2:
            detected[domain] = count
    if not detected:
        return 0, "Générique, aucun domaine détecté"
    best = max(detected, key=detected.get)
    score_val = detected[best]
    if score_val >= 4:
        return 10, f"Domaine '{best}' très bien adapté ({score_val}/4 markers)"
    if score_val >= 3:
        return 7, f"Domaine '{best}' bien adapté ({score_val}/4 markers)"
    return 5, f"Domaine '{best}' partiellement adapté ({score_val}/4 markers)"


def score_evolution(content: str) -> tuple[int, str]:
    """Critère 10: Évolution."""
    has_evolution = bool(re.search(r"(?i)[ée]volution|auto.?am[ée]lior|self.?improv", content))
    has_retex = "retex" in content.lower() or "retex_manager" in content
    has_thresholds = bool(re.search(r"(?i)si\s+\w+\s*<|seuil|threshold", content))
    if has_evolution and has_retex and has_thresholds:
        return 10, "Évolution + RETEX + seuils d'action"
    if has_evolution and has_thresholds:
        return 7, "Évolution avec seuils"
    if has_evolution:
        return 5, "Section évolution présente"
    return 0, "Statique"


SCORERS = {
    "frontmatter": score_frontmatter,
    "hard_gates": score_hard_gates,
    "anti_patterns": score_anti_patterns,
    "checklist": score_checklist,
    "flowchart": score_flowchart,
    "cross_links": score_cross_links,
    "concision": score_concision,
    "testability": score_testability,
    "domain": score_domain,
    "evolution": score_evolution,
}


def audit_skill(skill_path: Path) -> dict:
    """Auditer un skill et retourner le rapport."""
    content = read_skill(skill_path)
    if not content:
        return {"error": f"SKILL.md non trouvé dans {skill_path}"}

    results = {}
    total_weighted = 0
    for criterion, scorer in SCORERS.items():
        note, detail = scorer(content)
        weighted = note * WEIGHTS[criterion]
        total_weighted += weighted
        results[criterion] = {
            "note": note,
            "poids": WEIGHTS[criterion],
            "pondéré": weighted,
            "détail": detail,
        }

    final_score = round(total_weighted / MAX_SCORE * 100, 1)

    if final_score >= 85:
        verdict = "EXCELLENT"
    elif final_score >= 70:
        verdict = "BON"
    elif final_score >= 50:
        verdict = "INSUFFISANT"
    else:
        verdict = "REJETÉ"

    lines = len(content.strip().split("\n"))
    has_refs = (skill_path / "references").exists()
    has_agents = (skill_path / "agents").exists()
    has_scripts = (skill_path / "scripts").exists()

    return {
        "name": skill_path.name,
        "lines": lines,
        "has_references": has_refs,
        "has_agents": has_agents,
        "has_scripts": has_scripts,
        "criteria": results,
        "score": final_score,
        "verdict": verdict,
    }


def print_report(report: dict):
    """Afficher le rapport d'audit."""
    if "error" in report:
        print(f"  ERREUR: {report['error']}")
        return

    print(f"\n{'='*60}")
    print(f"  AUDIT QUALITÉ — {report['name']}")
    print(f"{'='*60}")
    print(f"  Lignes: {report['lines']} | refs: {'✓' if report['has_references'] else '✗'} | agents: {'✓' if report['has_agents'] else '✗'} | scripts: {'✓' if report['has_scripts'] else '✗'}")
    print(f"{'─'*60}")
    print(f"  {'#':>2} | {'Critère':<15} | {'Poids':>5} | {'Note':>4} | {'Pond.':>5} | Détail")
    print(f"  {'─'*2}─┼─{'─'*15}─┼─{'─'*5}─┼─{'─'*4}─┼─{'─'*5}─┼─{'─'*20}")

    for i, (criterion, data) in enumerate(report["criteria"].items(), 1):
        name = criterion.replace("_", " ").title()[:15]
        print(f"  {i:>2} | {name:<15} | x{data['poids']:<4} | {data['note']:>4} | {data['pondéré']:>5.1f} | {data['détail']}")

    print(f"  {'─'*2}─┼─{'─'*15}─┼─{'─'*5}─┼─{'─'*4}─┼─{'─'*5}─┤")
    print(f"     | {'TOTAL':<15} |       |      | {report['score']:>5.1f} | {report['verdict']}")
    print(f"{'='*60}\n")

    # Points faibles
    weak = [(k, v) for k, v in report["criteria"].items() if v["note"] < 5]
    if weak:
        print("  POINTS FAIBLES :")
        for k, v in sorted(weak, key=lambda x: x[1]["note"]):
            print(f"    ⚠ {k}: {v['note']}/10 — {v['détail']}")
        print()


def print_summary(reports: list[dict]):
    """Afficher un résumé de tous les skills."""
    print(f"\n{'='*70}")
    print(f"  RÉSUMÉ ÉCOSYSTÈME — {len(reports)} skills")
    print(f"{'='*70}")
    print(f"  {'Skill':<25} | {'Score':>6} | {'Verdict':<12} | {'Lignes':>6}")
    print(f"  {'─'*25}─┼─{'─'*6}─┼─{'─'*12}─┼─{'─'*6}")

    for r in sorted(reports, key=lambda x: x.get("score", 0), reverse=True):
        if "error" in r:
            print(f"  {r['name']:<25} | {'ERR':>6} | {'ERREUR':<12} | {'?':>6}")
        else:
            icon = {"EXCELLENT": "🟢", "BON": "🟡", "INSUFFISANT": "🟠", "REJETÉ": "🔴"}.get(r["verdict"], "⚪")
            print(f"  {r['name']:<25} | {r['score']:>5.1f}% | {icon} {r['verdict']:<10} | {r['lines']:>6}")

    scores = [r["score"] for r in reports if "score" in r]
    if scores:
        print(f"  {'─'*25}─┼─{'─'*6}─┤")
        print(f"  {'MOYENNE':<25} | {sum(scores)/len(scores):>5.1f}% |")
    print(f"{'='*70}\n")


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    summary_only = "--summary" in args
    args = [a for a in args if not a.startswith("--")]

    if args:
        # Auditer un skill spécifique
        skill_name = args[0]
        skill_path = SKILLS_DIR / skill_name
        report = audit_skill(skill_path)
        if as_json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print_report(report)
    else:
        # Auditer tous les skills
        reports = []
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                reports.append(audit_skill(skill_dir))

        if as_json:
            print(json.dumps(reports, indent=2, ensure_ascii=False))
        elif summary_only:
            print_summary(reports)
        else:
            for r in reports:
                print_report(r)
            print_summary(reports)


if __name__ == "__main__":
    main()
