#!/usr/bin/env python3
"""
gemini_wrapper.py

Wrapper Python pour le Gemini CLI officiel de Google.
- Resout le chemin absolu de gemini.cmd sur Windows
- Passe le prompt via stdin (evite problemes d'echappement)
- Timeout 120s par defaut
- Retourne un JSON structure
- Fallback automatique vers multi-ia-router si gemini absent/quota epuise

Usage:
    python gemini_wrapper.py --prompt "..." [--image path] [--model gemini-3-pro] [--timeout 120] [--json]

Exemples:
    # Texte seul
    python gemini_wrapper.py --prompt "Genere un diagramme Mermaid REST API"

    # Vision
    python gemini_wrapper.py --prompt "Analyse ce chart" --image "C:/tmp/chart.png"

    # Avec timeout custom et modele specifique
    python gemini_wrapper.py --prompt "..." --model gemini-3-flash --timeout 60
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

WINDOWS_GEMINI_PATHS = [
    r"C:/Users/Alexandre collenne/AppData/Roaming/npm/gemini.cmd",
    r"C:/Program Files/nodejs/gemini.cmd",
]

MULTI_IA_ROUTER_SCRIPT = r"C:/Users/Alexandre collenne/.claude/skills/multi-ia-router/tools/query_router.py"

LOG_FILE = Path(r"C:/Users/Alexandre collenne/.claude/logs/gemini-cli.log")


def log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def find_gemini_binary() -> str | None:
    # 1. shutil.which (PATH)
    for name in ("gemini", "gemini.cmd", "gemini.exe"):
        found = shutil.which(name)
        if found and Path(found).exists():
            return found
    # 2. Chemins absolus Windows connus
    for candidate in WINDOWS_GEMINI_PATHS:
        if Path(candidate).exists():
            return candidate
    return None


def parse_quota(stderr: str, stdout: str) -> int | None:
    """Cherche 'X requests remaining' dans stderr/stdout."""
    blob = (stderr or "") + "\n" + (stdout or "")
    patterns = [
        r"(\d+)\s+requests?\s+remaining",
        r"quota[:\s]+(\d+)",
        r"remaining[:\s]+(\d+)",
    ]
    for pat in patterns:
        m = re.search(pat, blob, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def is_quota_error(stderr: str, returncode: int) -> bool:
    if returncode == 0:
        return False
    blob = (stderr or "").lower()
    return any(s in blob for s in ("quota", "rate limit", "429", "too many requests", "exceeded"))


def call_gemini(binary: str, prompt: str, image: str | None, model: str, timeout: int) -> dict:
    if image:
        if not Path(image).exists():
            return {"status": "error", "error": f"Image introuvable: {image}"}
        # Gemini CLI attend la syntaxe @<path> dans le prompt (pas --image)
        prompt = f"{prompt} @{image}"
    args: list[str] = [binary, "-m", model, "-p", prompt]

    start = time.monotonic()
    try:
        proc = subprocess.run(
            args,
            input=None,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": f"Timeout apres {timeout}s", "timeout": True}
    except FileNotFoundError:
        return {"status": "error", "error": "gemini binary introuvable", "not_found": True}
    latency_ms = int((time.monotonic() - start) * 1000)

    quota = parse_quota(proc.stderr, proc.stdout)

    if proc.returncode != 0:
        return {
            "status": "error",
            "error": (proc.stderr or "unknown error").strip()[:500],
            "quota_exceeded": is_quota_error(proc.stderr, proc.returncode),
            "quota_remaining": quota,
            "latency_ms": latency_ms,
        }

    return {
        "status": "ok",
        "source": "gemini-cli",
        "model": model,
        "output": proc.stdout.strip(),
        "quota_remaining": quota,
        "latency_ms": latency_ms,
        "error": None,
    }


def fallback_multi_ia(prompt: str, image: str | None, reason: str) -> dict:
    """Bascule sur multi-ia-router (Gemini 2.5 Flash via API key)."""
    log(f"FALLBACK multi-ia-router (reason: {reason})")
    if not Path(MULTI_IA_ROUTER_SCRIPT).exists():
        return {
            "status": "error",
            "source": "fallback",
            "error": f"multi-ia-router introuvable: {MULTI_IA_ROUTER_SCRIPT}",
            "fallback_reason": reason,
        }
    args = [sys.executable, MULTI_IA_ROUTER_SCRIPT, "--provider", "gemini-flash", "--prompt", prompt]
    if image:
        args.extend(["--image", image])
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace")
        if proc.returncode == 0:
            return {
                "status": "fallback",
                "source": "multi-ia-router",
                "model": "gemini-2.5-flash",
                "output": proc.stdout.strip(),
                "fallback_reason": reason,
                "error": None,
            }
        return {
            "status": "error",
            "source": "fallback",
            "error": (proc.stderr or "router failed").strip()[:500],
            "fallback_reason": reason,
        }
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "source": "fallback", "error": str(e), "fallback_reason": reason}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prompt", required=True, help="Prompt a envoyer")
    parser.add_argument("--image", help="Chemin absolu vers une image")
    parser.add_argument("--model", default="gemini-3-pro", help="Modele (gemini-3-pro, gemini-3-flash, gemini-2.5-pro)")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout en secondes")
    parser.add_argument("--no-fallback", action="store_true", help="Desactive le fallback multi-ia-router")
    parser.add_argument("--json", action="store_true", help="Sortie JSON brute (par defaut aussi JSON)")
    args = parser.parse_args()

    binary = find_gemini_binary()
    if not binary:
        log("gemini binary introuvable")
        if args.no_fallback:
            result = {"status": "error", "error": "gemini CLI non installe", "source": "gemini-cli"}
        else:
            result = fallback_multi_ia(args.prompt, args.image, "binary_not_found")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result["status"] == "error" else 0

    result = call_gemini(binary, args.prompt, args.image, args.model, args.timeout)

    if result["status"] == "error" and not args.no_fallback:
        reason = "quota_exceeded" if result.get("quota_exceeded") else "gemini_error"
        log(f"gemini call failed: {result.get('error')}")
        result = fallback_multi_ia(args.prompt, args.image, reason)

    log(f"status={result['status']} source={result.get('source')} model={result.get('model')} latency={result.get('latency_ms')}ms")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in ("ok", "fallback") else 1


if __name__ == "__main__":
    sys.exit(main())
