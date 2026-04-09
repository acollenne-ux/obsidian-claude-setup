#!/usr/bin/env python3
"""
generate_mcp_config.py

Lit la config MCP de Claude Code (~/.claude.json ou claude_desktop_config.json)
et genere un fichier compatible avec l'import MCP d'Antigravity.

Securite :
- Exclut par defaut tous les proxies tiers interdits par les ToS Google (ban wave 02/2026).
- Option --absolute-paths pour resoudre uvx/npx/node/python en chemins absolus Windows.

Usage:
    python generate_mcp_config.py \\
        --from "C:/Users/Alexandre collenne/.claude.json" \\
        --out  "C:/tmp/antigravity_mcp.json" \\
        [--exclude name1,name2] \\
        [--include-only name1,name2] \\
        [--absolute-paths]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

FORBIDDEN = {
    "antigravity-cli",
    "antigravity-claude-proxy",
    "antigravity-proxy",
    "openclaw",
}

DEFAULT_INCLUDE = {
    "obsidian",
    "mcp-obsidian",
    "github",
    "context7",
    "n8n-mcp",
    "google-sheets",
    "playwright",
    "tradingview",
    "figma",
    "duckduckgo-search",
}

WINDOWS_ABSOLUTE_PATHS = {
    "uvx": r"C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/Scripts/uvx.exe",
    "uv": r"C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/Scripts/uv.exe",
    "npx": r"C:/Program Files/nodejs/npx.cmd",
    "npm": r"C:/Program Files/nodejs/npm.cmd",
    "node": r"C:/Program Files/nodejs/node.exe",
    "python": r"C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/python.exe",
    "python3": r"C:/Users/Alexandre collenne/AppData/Local/Programs/Python/Python313/python.exe",
}


def load_claude_config(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"[ERREUR] Config introuvable : {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"[ERREUR] JSON invalide dans {path} : {e}")


def extract_mcp_servers(config: dict) -> dict:
    """Cherche mcpServers a la racine OU dans projects/*/mcpServers."""
    servers: dict = {}
    if isinstance(config.get("mcpServers"), dict):
        servers.update(config["mcpServers"])
    projects = config.get("projects", {})
    if isinstance(projects, dict):
        for proj in projects.values():
            if isinstance(proj, dict) and isinstance(proj.get("mcpServers"), dict):
                for name, entry in proj["mcpServers"].items():
                    servers.setdefault(name, entry)
    return servers


def is_forbidden(name: str, entry: dict) -> bool:
    lower_name = name.lower()
    if any(bad in lower_name for bad in FORBIDDEN):
        return True
    blob = json.dumps(entry, ensure_ascii=False).lower()
    return any(bad in blob for bad in FORBIDDEN)


def resolve_absolute(entry: dict) -> dict:
    cmd = entry.get("command")
    if not cmd:
        return entry
    base = os.path.basename(str(cmd)).lower()
    for tool, abs_path in WINDOWS_ABSOLUTE_PATHS.items():
        if base == tool or base == f"{tool}.exe" or base == f"{tool}.cmd":
            if Path(abs_path).exists():
                entry = dict(entry)
                entry["command"] = abs_path
            break
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="src", required=True, help="Chemin vers ~/.claude.json")
    parser.add_argument("--out", dest="dst", required=True, help="Fichier de sortie JSON")
    parser.add_argument("--exclude", default="", help="Noms MCP a exclure (virgules)")
    parser.add_argument("--include-only", default="", help="Whitelist stricte (virgules). Si vide, include par defaut.")
    parser.add_argument("--absolute-paths", action="store_true", help="Resoudre uvx/npx/node/python en chemins absolus")
    parser.add_argument("--all", action="store_true", help="Inclure tous les MCPs (sauf forbidden), ignore la whitelist")
    args = parser.parse_args()

    src = Path(args.src).expanduser()
    dst = Path(args.dst).expanduser()

    exclude = {x.strip() for x in args.exclude.split(",") if x.strip()}
    include_only = {x.strip() for x in args.include_only.split(",") if x.strip()}

    config = load_claude_config(src)
    servers = extract_mcp_servers(config)
    if not servers:
        sys.exit("[ERREUR] Aucun mcpServers trouve dans la config.")

    kept: dict = {}
    excluded_forbidden: list = []
    excluded_user: list = []
    excluded_not_whitelisted: list = []

    for name, entry in servers.items():
        if is_forbidden(name, entry):
            excluded_forbidden.append(name)
            continue
        if name in exclude:
            excluded_user.append(name)
            continue
        if not args.all:
            whitelist = include_only or DEFAULT_INCLUDE
            if not any(w in name.lower() for w in whitelist):
                excluded_not_whitelisted.append(name)
                continue
        if args.absolute_paths:
            entry = resolve_absolute(entry)
        kept[name] = entry

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps({"mcpServers": kept}, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[OK] {len(kept)} MCPs ecrits dans : {dst}")
    for name in kept:
        print(f"  + {name}")
    if excluded_forbidden:
        print(f"[BAN] {len(excluded_forbidden)} MCPs interdits ToS exclus : {excluded_forbidden}")
    if excluded_user:
        print(f"[USER] {len(excluded_user)} MCPs exclus par --exclude : {excluded_user}")
    if excluded_not_whitelisted:
        print(f"[SKIP] {len(excluded_not_whitelisted)} MCPs hors whitelist : {excluded_not_whitelisted}")
    print("\nEtape suivante : Antigravity -> Agent pane -> MCP Servers -> Import from file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
