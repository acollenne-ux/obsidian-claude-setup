"""
retex_manager.py — Gestionnaire de RETEX (Retour d'Experience).
Enregistre et lit les lecons apprises de chaque analyse pour s'ameliorer en continu.

Usage :
  python retex_manager.py read [task_type]        # lire les lecons pour un type de tache
  python retex_manager.py write <json_data>       # enregistrer une nouvelle lecon
  python retex_manager.py summary                 # resume global des performances
  python retex_manager.py best-tools <task_type>  # meilleurs outils pour ce type
"""
import sys, json, argparse
from pathlib import Path
from datetime import datetime

RETEX_PATH = Path(__file__).parent.parent / "skills" / "deep-research" / "retex.json"

def load():
    if not RETEX_PATH.exists():
        return {"sessions": [], "tool_scores": {}, "agent_scores": {}, "patterns": {}}
    with open(RETEX_PATH, encoding="utf-8") as f:
        return json.load(f)

def save(data):
    RETEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RETEX_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def write_retex(entry: dict):
    """Enregistre une nouvelle session RETEX."""
    data = load()
    entry["timestamp"] = datetime.now().isoformat()
    data["sessions"].append(entry)

    # Mettre a jour les scores outils
    for tool, result in entry.get("tool_results", {}).items():
        if tool not in data["tool_scores"]:
            data["tool_scores"][tool] = {"uses": 0, "successes": 0, "failures": 0, "avg_quality": 0}
        s = data["tool_scores"][tool]
        s["uses"] += 1
        if result.get("success"):
            s["successes"] += 1
        else:
            s["failures"] += 1
        q = result.get("quality", 5)
        s["avg_quality"] = round((s["avg_quality"] * (s["uses"]-1) + q) / s["uses"], 2)

    # Mettre a jour les patterns par type de tache
    task_type = entry.get("task_type", "general")
    if task_type not in data["patterns"]:
        data["patterns"][task_type] = {"best_tools": [], "worst_tools": [], "tips": []}

    save(data)
    print(f"RETEX enregistre : {entry.get('task_type', 'general')} — {entry.get('summary', '')[:60]}")

def read_retex(task_type=None):
    """Lit les lecons pour un type de tache."""
    data = load()
    sessions = data["sessions"]
    if task_type:
        sessions = [s for s in sessions if s.get("task_type") == task_type]

    if not sessions:
        print(f"Aucun RETEX pour : {task_type or 'toutes les taches'}")
        return

    print(f"\n=== RETEX : {task_type or 'Global'} ({len(sessions)} sessions) ===\n")
    for s in sessions[-5:]:  # 5 dernieres sessions
        print(f"[{s['timestamp'][:10]}] {s.get('task_type','?')} — {s.get('summary','')[:80]}")
        if s.get("what_worked"):
            print(f"  + Ce qui a marche : {s['what_worked']}")
        if s.get("what_failed"):
            print(f"  - Ce qui a echoue : {s['what_failed']}")
        if s.get("improvement"):
            print(f"  => Amelioration : {s['improvement']}")
        print()

def best_tools(task_type=None):
    """Retourne les meilleurs outils par score de qualite."""
    data = load()
    scores = data["tool_scores"]
    if not scores:
        print("Pas encore de donnees de performance.")
        return

    sorted_tools = sorted(scores.items(), key=lambda x: x[1]["avg_quality"], reverse=True)
    print(f"\n=== Meilleurs outils (qualite moyenne) ===\n")
    for tool, s in sorted_tools[:10]:
        rate = round(s["successes"] / s["uses"] * 100) if s["uses"] else 0
        print(f"  {tool:25} qualite:{s['avg_quality']:.1f}/10  succes:{rate}%  utilisations:{s['uses']}")

def summary():
    """Resume global."""
    data = load()
    n = len(data["sessions"])
    print(f"\n=== RETEX Global : {n} sessions enregistrees ===")
    print(f"Types de taches : {list(data['patterns'].keys())}")
    best_tools()

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")

    r = subparsers.add_parser("read")
    r.add_argument("task_type", nargs="?")

    w = subparsers.add_parser("write")
    w.add_argument("json_data")

    subparsers.add_parser("summary")

    b = subparsers.add_parser("best-tools")
    b.add_argument("task_type", nargs="?")

    args = parser.parse_args()

    if args.cmd == "read":
        read_retex(args.task_type)
    elif args.cmd == "write":
        entry = json.loads(args.json_data)
        write_retex(entry)
    elif args.cmd == "summary":
        summary()
    elif args.cmd == "best-tools":
        best_tools(args.task_type)
    else:
        summary()

if __name__ == "__main__":
    main()
