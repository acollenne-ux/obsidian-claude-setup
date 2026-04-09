#!/usr/bin/env python
"""UserPromptSubmit hook: force image-studio invocation for any visual creation/modification request."""
import json, sys, re

try:
    data = json.load(sys.stdin)
    prompt = (data.get("prompt") or "").lower()
except Exception:
    sys.exit(0)

# Keywords déclenchant image-studio
PATTERNS = [
    r"\b(cr[ée]e?r?|fai[st]?|g[ée]n[ée]re?r?|modifie?r?|retouche?r?|compose?r?)\b.{0,40}\b("
    r"image|photo|flyer|affiche|poster|visuel|banni[èe]re|post|carte|invitation|menu|"
    r"mockup|maquette|template|design graphique|montage|compositing)\b",
    r"\b(design|graphique)\b.{0,20}\b(flyer|affiche|poster|visuel)\b",
    r"\bretouche\b",
    r"\bd[ée]toure?r?\b",
]

if any(re.search(p, prompt) for p in PATTERNS):
    msg = (
        "INSTRUCTION OBLIGATOIRE : Cette demande concerne la création/modification "
        "d'un visuel. Tu DOIS invoquer le skill `image-studio` via le tool Skill "
        "AVANT toute autre action. image-studio utilise Canva MCP comme moteur "
        "principal et suit un pipeline 8 phases avec art-director critique."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": msg
        }
    }))
sys.exit(0)
