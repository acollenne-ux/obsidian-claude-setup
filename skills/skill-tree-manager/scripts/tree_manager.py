#!/usr/bin/env python3
"""
skill-tree-manager — moteur de maintenance de l'arborescence intelligente (7 couches).

Usage:
    python tree_manager.py rebuild          # reconstruit SKILL_TREE.md
    python tree_manager.py add <nom>        # ajoute un skill au tree + valide
    python tree_manager.py validate         # valide les regles entree/sortie
    python tree_manager.py audit            # rapport complet avec score /100
    python tree_manager.py migrate          # ajoute ## LIVRABLE FINAL aux skills manquants

Architecture 7 couches :
    L0 ENTRY      -> deep-research (unique)
    L1 THINK      -> brainstorming / cadrage / orchestration
    L2 RESEARCH   -> collecte multi-sources
    L3 SPECIALIST -> metier (finance, dev, n8n, web, obsidian, system)
    L4 DELIVERY   -> generateurs de livrable (PDF/PPT/image/etc.)
    L5 QA         -> validation + envoi
    L6 META       -> amelioration continue
"""
from __future__ import annotations
import sys, re, json, io
from pathlib import Path
from datetime import datetime

# Force UTF-8 stdout on Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILLS_DIR = Path.home() / ".claude" / "skills"
TREE_FILE = SKILLS_DIR / "skill-tree-manager" / "SKILL_TREE.md"

# ------------------------------------------------------------------
# ARBORESCENCE 7 COUCHES
# ------------------------------------------------------------------
LAYERS = {
    "L0_ENTRY":      ["deep-research"],
    "L1_THINK":      ["superpowers-brainstorming", "project-analysis", "team-agent"],
    "L2_RESEARCH":   ["multi-ia-router", "defuddle"],
    "L3_SPECIALIST": [
        # finance
        "stock-analysis", "financial-analysis-framework", "financial-modeling", "macro-analysis",
        # dev
        "code-debug", "dev-team", "data-analysis",
        # n8n cluster
        "n8n-management", "n8n-workflow-patterns", "n8n-node-configuration",
        "n8n-code-javascript", "n8n-code-python", "n8n-expression-syntax",
        "n8n-validation-expert", "n8n-mcp-tools-expert",
        # web
        "website-analyzer",
        # obsidian / knowledge
        "obsidian-markdown", "obsidian-bases", "obsidian-cli", "json-canvas",
        # system
        "desktop-control", "install-plugin",
        # diagrams
        "idea-to-diagram", "diagram-toolkit",
    ],
    "L4_DELIVERY":   ["pdf-report-pro", "pdf-report-gen", "ppt-creator",
                      "cv-creator", "cover-letter-creator",
                      "image-studio", "flyer-creator", "image-enhancer", "image-detourage"],
    "L5_QA":         ["qa-pipeline"],
    "L6_META":       ["feedback-loop", "retex-evolution", "skill-creator", "skill-tree-manager"],
}

# Skills exemptes de la regle "livrable obligatoire" (couches systeme)
EXEMPT_LAYERS = {"L0_ENTRY", "L1_THINK", "L2_RESEARCH", "L5_QA", "L6_META"}

DELIVERABLE_TYPES = {"pdf", "ppt", "pptx", "doc", "docx", "markdown",
                     "image", "png", "jpg", "video", "vidéo", "audio", "mp3", "mp4"}

# Mapping SPECIALIST -> (type, generateur) applique par `migrate`
DEFAULT_DELIVERABLES = {
    # finance
    "stock-analysis":               ("PDF", "pdf-report-pro"),
    "financial-analysis-framework": ("PDF", "pdf-report-pro"),
    "financial-modeling":           ("PDF", "pdf-report-pro"),
    "macro-analysis":               ("PDF", "pdf-report-pro"),
    # dev
    "code-debug":                   ("PDF", "pdf-report-pro"),
    "dev-team":                     ("PDF", "pdf-report-pro"),
    "data-analysis":                ("PDF", "pdf-report-pro"),
    # n8n cluster
    "n8n-management":               ("DOC", "pdf-report-pro"),
    "n8n-workflow-patterns":        ("DOC", "pdf-report-pro"),
    "n8n-node-configuration":       ("DOC", "pdf-report-pro"),
    "n8n-code-javascript":          ("DOC", "pdf-report-pro"),
    "n8n-code-python":              ("DOC", "pdf-report-pro"),
    "n8n-expression-syntax":        ("DOC", "pdf-report-pro"),
    "n8n-validation-expert":        ("DOC", "pdf-report-pro"),
    "n8n-mcp-tools-expert":         ("DOC", "pdf-report-pro"),
    # web / content
    "website-analyzer":             ("PDF", "pdf-report-pro"),
    # obsidian / knowledge
    "obsidian-markdown":            ("DOC", "obsidian-markdown"),
    "obsidian-bases":               ("DOC", "obsidian-bases"),
    "obsidian-cli":                 ("DOC", "obsidian-cli"),
    "json-canvas":                  ("DOC", "json-canvas"),
    # system
    "desktop-control":              ("PDF", "pdf-report-pro"),
    "install-plugin":               ("DOC", "pdf-report-pro"),
    "idea-to-diagram":              ("image", "image-studio"),
    "diagram-toolkit":              ("image", "image-studio"),
    # delivery layer (auto-reference)
    "pdf-report-pro":               ("PDF", "self"),
    "pdf-report-gen":               ("PDF", "self"),
    "ppt-creator":                  ("PPT", "self"),
    "cv-creator":                   ("PDF", "self"),
    "cover-letter-creator":         ("PDF", "self"),
    "image-studio":                 ("image", "self"),
    "flyer-creator":                ("image", "self"),
    "image-enhancer":               ("image", "self"),
    "image-detourage":              ("image", "self"),
}

LIVRABLE_TEMPLATE = """

## LIVRABLE FINAL

- **Type** : {dtype}
- **Généré par** : {gen}
- **Destination** : acollenne@gmail.com via send_report.py

## CHAÎNAGE ARBORESCENCE

- **Amont** : deep-research (entrée unique)
- **Aval** : {gen}
"""

# ------------------------------------------------------------------
# Parsing
# ------------------------------------------------------------------
def parse_frontmatter(skill_md: Path) -> dict:
    if not skill_md.exists():
        return {}
    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r'^(\w[\w-]*)\s*:\s*"?([^"]*)"?\s*$', line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip()
    fm["_body"] = text
    return fm

def classify(name: str) -> str:
    for layer, members in LAYERS.items():
        if name in members:
            return layer
    return "L3_SPECIALIST"

def detect_deliverable(body: str) -> tuple[str, str]:
    m = re.search(r"##\s*LIVRABLE FINAL(.*?)(?=\n##|\Z)", body, re.DOTALL | re.IGNORECASE)
    if not m:
        return ("", "")
    section = m.group(1).lower()
    dtype = ""
    for t in DELIVERABLE_TYPES:
        if t in section:
            dtype = t.upper()
            break
    gen_match = re.search(r"généré par\s*:?\s*\*?\*?\[?([a-z0-9\-]+)", section)
    gen = gen_match.group(1) if gen_match else ""
    return (dtype, gen)

def scan_all() -> list[dict]:
    skills = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        if ".bak" in skill_dir.name:
            continue
        md = skill_dir / "SKILL.md"
        fm = parse_frontmatter(md)
        if not fm.get("name"):
            continue
        name = fm["name"]
        body = fm.pop("_body", "")
        dtype, gen = detect_deliverable(body)
        skills.append({
            "name": name,
            "description": fm.get("description", "")[:200],
            "layer": classify(name),
            "deliverable_type": dtype,
            "deliverable_generator": gen,
            "has_deliverable": bool(dtype),
            "path": str(md),
        })
    return skills

# ------------------------------------------------------------------
# Validation + scoring
# ------------------------------------------------------------------
def validate(skills: list[dict]) -> dict:
    issues = {"no_deliverable": [], "orphan": []}
    required = [s for s in skills if s["layer"] not in EXEMPT_LAYERS]
    for s in required:
        if not s["has_deliverable"]:
            issues["no_deliverable"].append(s["name"])
    total = len(skills)
    required_n = len(required)
    conform = required_n - len(issues["no_deliverable"])
    score = int(100 * conform / required_n) if required_n else 100
    return {"score": score, "total": total, "required": required_n,
            "conform": conform, "issues": issues}

# ------------------------------------------------------------------
# Rendering
# ------------------------------------------------------------------
LAYER_LABELS = {
    "L0_ENTRY":      "L0 — ENTRY (point d'entrée unique)",
    "L1_THINK":      "L1 — THINK (brainstorming / cadrage / orchestration)",
    "L2_RESEARCH":   "L2 — RESEARCH (collecte multi-sources)",
    "L3_SPECIALIST": "L3 — SPECIALIST (métier)",
    "L4_DELIVERY":   "L4 — DELIVERY (générateurs de livrable)",
    "L5_QA":         "L5 — QA & DELIVER (validation + envoi)",
    "L6_META":       "L6 — META (amélioration continue)",
}

def render_tree(skills: list[dict], val: dict) -> str:
    by_layer = {k: [] for k in LAYERS.keys()}
    for s in skills:
        by_layer.setdefault(s["layer"], []).append(s)

    out = []
    out.append("# SKILL_TREE.md — Arborescence Intelligente des Skills")
    out.append("")
    out.append(f"**Généré** : {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    out.append(f"**Total skills** : {val['total']}  ")
    out.append(f"**Requis (non-exemptés)** : {val['required']}  ")
    out.append(f"**Conformes** : {val['conform']}  ")
    out.append(f"**Score cohérence** : {val['score']}/100")
    out.append("")
    out.append("## Règles d'arborescence (non-négociables)")
    out.append("")
    out.append("1. **ENTRÉE** : toute conversation démarre par `deep-research`")
    out.append("2. **SORTIE** : toute réponse finit par un livrable (PDF, PPT, DOC, image, vidéo, audio)")
    out.append("")
    out.append("```")
    out.append("L0 deep-research → L1 THINK → L2 RESEARCH → L3 SPECIALIST → L4 DELIVERY → L5 QA → L6 META")
    out.append("```")
    out.append("")
    for layer in LAYERS.keys():
        out.append(f"## {LAYER_LABELS[layer]}")
        out.append("")
        items = sorted(by_layer.get(layer, []), key=lambda x: x["name"])
        if not items:
            out.append("_(vide)_")
        else:
            out.append("| Skill | Livrable | Généré par | Description |")
            out.append("|-------|----------|------------|-------------|")
            for s in items:
                dt = s["deliverable_type"] or ("—" if layer in EXEMPT_LAYERS else "[MANQUANT]")
                gen = s["deliverable_generator"] or "—"
                desc = s["description"][:80].replace("|", "\\|")
                out.append(f"| `{s['name']}` | {dt} | {gen} | {desc} |")
        out.append("")

    if val["issues"]["no_deliverable"]:
        out.append("## Skills sans livrable déclaré")
        out.append("")
        for n in val["issues"]["no_deliverable"]:
            out.append(f"- `{n}`")
        out.append("")
    return "\n".join(out)

# ------------------------------------------------------------------
# Commandes
# ------------------------------------------------------------------
def cmd_rebuild():
    skills = scan_all()
    val = validate(skills)
    TREE_FILE.parent.mkdir(parents=True, exist_ok=True)
    TREE_FILE.write_text(render_tree(skills, val), encoding="utf-8")
    print(f"[OK] SKILL_TREE.md regenerated: {TREE_FILE}")
    print(f"     {val['total']} skills ({val['required']} requis) - score {val['score']}/100")
    if val["issues"]["no_deliverable"]:
        print(f"     [WARN] {len(val['issues']['no_deliverable'])} skills sans livrable")

def cmd_add(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        print(f"[ERR] Skill {name} introuvable"); sys.exit(1)
    fm = parse_frontmatter(skill_md)
    dtype, gen = detect_deliverable(fm.get("_body", ""))
    layer = classify(name)
    if layer not in EXEMPT_LAYERS and not dtype:
        print(f"[REJECT] {name} n'a pas de section ## LIVRABLE FINAL."); sys.exit(2)
    print(f"[OK] {name} valide - couche {layer}, livrable {dtype or '-'}")
    cmd_rebuild()

def cmd_validate():
    skills = scan_all()
    val = validate(skills)
    print(json.dumps(val, indent=2, ensure_ascii=False))
    if val["score"] < 80:
        sys.exit(1)

def cmd_audit():
    skills = scan_all()
    val = validate(skills)
    print(f"=== AUDIT SKILL TREE ===")
    print(f"Total          : {val['total']}")
    print(f"Requis         : {val['required']}")
    print(f"Conformes      : {val['conform']}")
    print(f"Score          : {val['score']}/100")
    print(f"Sans livrable  : {len(val['issues']['no_deliverable'])}")
    for n in val["issues"]["no_deliverable"]:
        print(f"  - {n}")

def cmd_migrate():
    """Ajoute la section ## LIVRABLE FINAL aux skills manquants en s'appuyant sur DEFAULT_DELIVERABLES."""
    count = 0
    skipped = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or ".bak" in skill_dir.name:
            continue
        md = skill_dir / "SKILL.md"
        if not md.exists():
            continue
        name = skill_dir.name
        layer = classify(name)
        if layer in EXEMPT_LAYERS:
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"##\s*LIVRABLE FINAL", text, re.IGNORECASE):
            continue  # deja present
        if name not in DEFAULT_DELIVERABLES:
            skipped.append(name)
            continue
        dtype, gen = DEFAULT_DELIVERABLES[name]
        section = LIVRABLE_TEMPLATE.format(dtype=dtype, gen=gen)
        md.write_text(text.rstrip() + section + "\n", encoding="utf-8")
        print(f"[MIGRATE] {name} -> {dtype} via {gen}")
        count += 1
    print(f"\n[OK] {count} skills migres")
    if skipped:
        print(f"[SKIP] {len(skipped)} skills sans mapping: {skipped}")
    cmd_rebuild()

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "rebuild":    cmd_rebuild()
    elif cmd == "add" and len(sys.argv) >= 3: cmd_add(sys.argv[2])
    elif cmd == "validate": cmd_validate()
    elif cmd == "audit":    cmd_audit()
    elif cmd == "migrate":  cmd_migrate()
    else:
        print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
