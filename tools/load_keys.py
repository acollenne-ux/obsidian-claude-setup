#!/usr/bin/env python3
"""
load_keys.py — Chargeur dynamique de clés API
Charge les clés depuis api_keys.json sans les exposer dans SKILL.md
Usage:
  python load_keys.py                  # Affiche toutes les clés disponibles (noms seulement)
  python load_keys.py get fred         # Retourne la clé API FRED
  python load_keys.py get openrouter   # Retourne la clé API OpenRouter
  python load_keys.py url fred         # Retourne la base_url FRED
  python load_keys.py export           # Exporte toutes les clés en variables d'env
  python load_keys.py curl fred        # Génère un exemple curl avec la clé
"""

import json
import os
import sys

# Chemin du fichier de clés (même dossier que ce script)
KEYS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api_keys.json")

def load_keys():
    """Charge le fichier api_keys.json"""
    if not os.path.exists(KEYS_FILE):
        print(f"ERREUR: {KEYS_FILE} introuvable", file=sys.stderr)
        sys.exit(1)
    with open(KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_key(service):
    """Retourne la clé API d'un service"""
    keys = load_keys()
    service = service.lower()
    if service in keys and isinstance(keys[service], dict):
        return keys[service].get("api_key", "Pas de clé (API gratuite)")
    # Chercher dans free_apis
    if "free_apis" in keys and service in keys["free_apis"]:
        return "API gratuite — pas de clé nécessaire"
    print(f"ERREUR: Service '{service}' inconnu", file=sys.stderr)
    print(f"Services disponibles: {', '.join(k for k in keys if not k.startswith('_'))}", file=sys.stderr)
    sys.exit(1)

def get_url(service):
    """Retourne la base_url d'un service"""
    keys = load_keys()
    service = service.lower()
    if service in keys and isinstance(keys[service], dict):
        return keys[service].get("base_url", "URL non définie")
    if "free_apis" in keys and service in keys["free_apis"]:
        return keys["free_apis"][service].get("base_url", "URL non définie")
    print(f"ERREUR: Service '{service}' inconnu", file=sys.stderr)
    sys.exit(1)

def get_service_info(service):
    """Retourne toutes les infos d'un service"""
    keys = load_keys()
    service = service.lower()
    if service in keys and isinstance(keys[service], dict):
        return keys[service]
    if "free_apis" in keys and service in keys["free_apis"]:
        return keys["free_apis"][service]
    return None

def list_services():
    """Liste tous les services disponibles"""
    keys = load_keys()
    print("=== Services API disponibles ===\n")
    for k, v in keys.items():
        if k.startswith("_"):
            continue
        if k == "free_apis":
            print("--- APIs Gratuites ---")
            for fk, fv in v.items():
                print(f"  {fk}: {fv.get('name', fk)} — {fv.get('usage', '')}")
        else:
            has_key = "api_key" in v
            status = "OK" if has_key else "gratuite"
            print(f"  {k}: {v.get('name', k)} [{status}] — {v.get('usage', '')}")

def export_env():
    """Exporte les clés en format variables d'environnement"""
    keys = load_keys()
    for k, v in keys.items():
        if k.startswith("_") or k == "free_apis":
            continue
        if isinstance(v, dict) and "api_key" in v:
            env_name = f"{k.upper()}_API_KEY"
            print(f"set {env_name}={v['api_key']}")

def main():
    if len(sys.argv) < 2:
        list_services()
        return
    cmd = sys.argv[1].lower()
    if cmd == "get" and len(sys.argv) >= 3:
        print(get_key(sys.argv[2]))
    elif cmd == "url" and len(sys.argv) >= 3:
        print(get_url(sys.argv[2]))
    elif cmd == "export":
        export_env()
    elif cmd == "info" and len(sys.argv) >= 3:
        info = get_service_info(sys.argv[2])
        if info:
            print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            print(f"Service '{sys.argv[2]}' inconnu", file=sys.stderr)
    elif cmd == "json":
        # Retourne tout le JSON (pour usage programmatique)
        keys = load_keys()
        print(json.dumps(keys, indent=2, ensure_ascii=False))
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
