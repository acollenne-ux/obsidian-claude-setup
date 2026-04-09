#!/usr/bin/env python3
"""PostToolUse hook: rebuild SKILL_TREE.md quand un SKILL.md est modifie."""
import sys, json, subprocess, os
try:
    data = json.loads(sys.stdin.read() or "{}")
except Exception:
    sys.exit(0)

tool_input = data.get("tool_input", {})
path = tool_input.get("file_path", "") or tool_input.get("filePath", "")

# Declencher uniquement si le fichier modifie est un SKILL.md
if not path.endswith("SKILL.md") or ".claude" not in path.replace("\\", "/"):
    sys.exit(0)

# Ne pas rebuild si on est DANS skill-tree-manager (evite boucle)
if "skill-tree-manager" in path:
    sys.exit(0)

py = r"C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/python.exe"
script = r"C:/Users/Alexandre collenne/.claude/skills/skill-tree-manager/scripts/tree_manager.py"
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"
try:
    subprocess.run([py, script, "rebuild"], timeout=20, env=env,
                   capture_output=True, check=False)
except Exception:
    pass
sys.exit(0)
