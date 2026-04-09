#!/usr/bin/env python3
"""
N8N local setup automation.

1. Cree le compte owner via /rest/owner/setup
2. Genere une API key via /rest/api-keys
3. Met a jour les 2 fichiers de config Claude (Desktop + Code)

Usage:
    python n8n_local_setup.py [--host http://localhost:5678]
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path

DEFAULT_HOST = "http://localhost:5678"
OWNER_EMAIL = "admin@local.dev"
OWNER_PASSWORD = "ClaudeN8n2026!"
OWNER_FIRSTNAME = "Alex"
OWNER_LASTNAME = "Local"

DESKTOP_CONFIG = Path(os.environ["APPDATA"]) / "Claude" / "claude_desktop_config.json"
CODE_CONFIG = Path.home() / ".claude.json"


def wait_for_ready(host: str, timeout: int = 120) -> bool:
    """Attend que /healthz reponde 200."""
    start = time.time()
    url = f"{host}/healthz"
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(2)
    return False


def make_opener():
    cj = CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)), cj


def post_json(opener, url: str, payload: dict, extra_headers: dict | None = None):
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with opener.open(req, timeout=20) as r:
            body = r.read().decode("utf-8")
            return r.status, body, dict(r.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return e.code, body, dict(e.headers)


def get_json(opener, url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with opener.open(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace"), dict(e.headers)


def setup_owner(opener, host: str) -> tuple[bool, str]:
    """Cree l'owner. Retourne (created, message)."""
    url = f"{host}/rest/owner/setup"
    payload = {
        "email": OWNER_EMAIL,
        "firstName": OWNER_FIRSTNAME,
        "lastName": OWNER_LASTNAME,
        "password": OWNER_PASSWORD,
    }
    status, body, _ = post_json(opener, url, payload)
    if status in (200, 201):
        return True, "owner created"
    if status == 400 and "already" in body.lower():
        return False, "owner already exists"
    if status == 404:
        # Endpoint different selon version. Essayer alternatives.
        for alt in ("/rest/owner", "/rest/users", "/rest/me/setup"):
            s2, b2, _ = post_json(opener, f"{host}{alt}", payload)
            if s2 in (200, 201):
                return True, f"owner created via {alt}"
        return False, f"setup endpoint not found (last body: {body[:200]})"
    return False, f"setup failed status={status} body={body[:300]}"


def login(opener, host: str) -> tuple[bool, str]:
    """Login en tant qu'owner."""
    url = f"{host}/rest/login"
    payload = {"emailOrLdapLoginId": OWNER_EMAIL, "password": OWNER_PASSWORD}
    status, body, _ = post_json(opener, url, payload)
    if status in (200, 201):
        return True, "logged in"
    # Fallback: ancienne structure
    payload2 = {"email": OWNER_EMAIL, "password": OWNER_PASSWORD}
    status, body, _ = post_json(opener, url, payload2)
    if status in (200, 201):
        return True, "logged in (legacy payload)"
    return False, f"login failed status={status} body={body[:300]}"


def create_api_key(opener, host: str) -> tuple[str | None, str]:
    """Cree une API key. Retourne (key, message)."""
    # Essais en cascade : endpoints differents selon versions n8n
    candidates = [
        ("/rest/api-keys", {"label": "claude-mcp"}),
        ("/rest/me/api-keys", {"label": "claude-mcp"}),
        ("/rest/api-keys", {"label": "claude-mcp", "scopes": ["*"]}),
        ("/rest/me/api-keys", {"label": "claude-mcp", "scopes": ["*"]}),
    ]
    for path, payload in candidates:
        url = f"{host}{path}"
        status, body, _ = post_json(opener, url, payload)
        if status in (200, 201):
            try:
                data = json.loads(body)
                # Plusieurs structures possibles
                key = (
                    data.get("data", {}).get("apiKey")
                    or data.get("data", {}).get("rawApiKey")
                    or data.get("apiKey")
                    or data.get("rawApiKey")
                )
                if key:
                    return key, f"key created via {path}"
                # Sinon : retourner toute la reponse pour inspection
                return None, f"key endpoint OK but no apiKey field: {body[:300]}"
            except Exception as e:
                return None, f"json parse error: {e}"
    return None, f"no api key endpoint worked (last status={status} body={body[:200]})"


def update_config(path: Path, api_url: str, api_key: str) -> bool:
    if not path.exists():
        print(f"  [skip] {path} introuvable")
        return False
    raw = path.read_text(encoding="utf-8")
    try:
        cfg = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  [erreur] JSON invalide dans {path}: {e}")
        return False
    # Backup
    backup = path.with_suffix(path.suffix + f".bak_{int(time.time())}")
    backup.write_text(raw, encoding="utf-8")
    # MAJ
    mcp_servers = cfg.get("mcpServers") or {}
    n8n_entry = mcp_servers.get("n8n-mcp")
    if not n8n_entry:
        print(f"  [skip] n8n-mcp absent de {path}")
        return False
    env = n8n_entry.setdefault("env", {})
    env["N8N_API_URL"] = api_url
    env["N8N_API_KEY"] = api_key
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [ok] {path} mis a jour (backup: {backup.name})")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default=DEFAULT_HOST)
    args = ap.parse_args()

    print(f"[1/5] Wait for n8n at {args.host}/healthz ...")
    if not wait_for_ready(args.host):
        print("  [erreur] n8n n'a pas demarre dans les 120s")
        sys.exit(1)
    print("  [ok] n8n ready")

    opener, _ = make_opener()

    print("[2/5] Setup owner ...")
    created, msg = setup_owner(opener, args.host)
    print(f"  {'[ok]' if created else '[info]'} {msg}")

    print("[3/5] Login ...")
    ok, msg = login(opener, args.host)
    if not ok:
        print(f"  [erreur] {msg}")
        sys.exit(2)
    print(f"  [ok] {msg}")

    print("[4/5] Create API key ...")
    key, msg = create_api_key(opener, args.host)
    if not key:
        print(f"  [erreur] {msg}")
        sys.exit(3)
    print(f"  [ok] {msg}")
    print(f"  API key (first 20 chars): {key[:20]}...")

    api_url = f"{args.host}/api/v1"

    print("[5/5] Update Claude configs ...")
    update_config(DESKTOP_CONFIG, api_url, key)
    update_config(CODE_CONFIG, api_url, key)

    # Save key to a local file for reference
    secret_file = Path.home() / ".claude" / "skills" / "n8n-management" / ".n8n_local_key.txt"
    secret_file.parent.mkdir(parents=True, exist_ok=True)
    secret_file.write_text(
        f"N8N_API_URL={api_url}\nN8N_API_KEY={key}\nN8N_OWNER_EMAIL={OWNER_EMAIL}\nN8N_OWNER_PASSWORD={OWNER_PASSWORD}\n",
        encoding="utf-8",
    )
    print(f"\n[done] Cles sauvegardees dans {secret_file}")
    print(f"       URL : {api_url}")
    print(f"       KEY : {key[:20]}...")


if __name__ == "__main__":
    main()
