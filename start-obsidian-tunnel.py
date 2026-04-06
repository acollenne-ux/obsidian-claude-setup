"""
Lance le tunnel Cloudflare vers Obsidian et envoie l'URL par email.
Se lance automatiquement au démarrage Windows via le .vbs associé.
"""
import subprocess
import re
import time
import sys
import os

# --- Configuration ---
OBSIDIAN_API_KEY = "cf80b686546b090a1df531d73a09d7fd51820c76b86041859e63e281ed5909a2"
EMAIL = "acollenne@gmail.com"
SEND_REPORT_SCRIPT = os.path.expanduser("~/.claude/tools/send_report.py")
PYTHON_PATH = r"C:\Users\Alexandre collenne\AppData\Local\Programs\Python\Python313\python.exe"
URL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "current_tunnel_url.txt")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tunnel.log")


def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def wait_for_obsidian_api(max_wait=120):
    """Attend que l'API Obsidian soit accessible (Obsidian peut mettre du temps à démarrer)."""
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for i in range(max_wait // 5):
        try:
            req = urllib.request.Request(
                "https://127.0.0.1:27124/",
                headers={"Authorization": f"Bearer {OBSIDIAN_API_KEY}"}
            )
            resp = urllib.request.urlopen(req, timeout=5, context=ctx)
            if resp.status == 200:
                log("API Obsidian accessible")
                return True
        except Exception:
            pass
        time.sleep(5)

    log("ERREUR: API Obsidian non accessible après 2 minutes")
    return False


def start_tunnel():
    """Lance cloudflared et capture l'URL du tunnel."""
    log("Lancement du tunnel cloudflared...")

    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "https://localhost:27124", "--no-tls-verify"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Lire la sortie ligne par ligne pour trouver l'URL
    url = None
    start_time = time.time()

    while time.time() - start_time < 30:
        line = process.stdout.readline()
        if not line:
            if process.poll() is not None:
                log("ERREUR: cloudflared s'est arrêté")
                return None, None
            continue

        line = line.strip()
        # Chercher l'URL trycloudflare.com
        match = re.search(r'(https://[a-z0-9-]+\.trycloudflare\.com)', line)
        if match:
            url = match.group(1)
            log(f"URL du tunnel: {url}")
            break

    if not url:
        log("ERREUR: URL du tunnel non trouvée dans les 30 secondes")
        process.kill()
        return None, None

    return url, process


def save_url(url):
    """Sauvegarde l'URL dans un fichier pour référence."""
    with open(URL_FILE, "w", encoding="utf-8") as f:
        f.write(url)
    log(f"URL sauvegardée dans {URL_FILE}")


def send_email(url):
    """Envoie l'URL par email via send_report.py."""
    if not os.path.exists(SEND_REPORT_SCRIPT):
        log(f"send_report.py non trouvé: {SEND_REPORT_SCRIPT}")
        return False

    # Créer un fichier markdown temporaire pour le rapport
    report_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tunnel_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"""# Tunnel Obsidian actif

## URL du tunnel
```
{url}
```

## Clé API Obsidian
```
{OBSIDIAN_API_KEY}
```

## Configuration claude.ai — Copier-coller
1. Va sur **claude.ai** → Settings → Integrations → MCP Servers
2. Ajoute ou modifie le serveur Obsidian :
   - **URL** : `{url}`
   - **Header Name** : `Authorization`
   - **Header Value** : `Bearer {OBSIDIAN_API_KEY}`

## Test rapide (colle dans un terminal)
```bash
curl -s -H "Authorization: Bearer {OBSIDIAN_API_KEY}" {url}/
```

---
*Généré automatiquement le {time.strftime("%d/%m/%Y à %H:%M")}*
*Rappel : Obsidian + cloudflared doivent rester ouverts sur le PC.*
""")

    try:
        result = subprocess.run(
            [PYTHON_PATH, SEND_REPORT_SCRIPT, "--file", report_file,
             "Tunnel Obsidian - Nouvelle URL", EMAIL],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            log("Email envoyé avec succès")
            return True
        else:
            log(f"Erreur envoi email: {result.stderr}")
            return False
    except Exception as e:
        log(f"Exception envoi email: {e}")
        return False


def main():
    log("=== Démarrage tunnel Obsidian ===")

    # 1. Attendre que l'API Obsidian soit prête
    log("Attente de l'API Obsidian...")
    if not wait_for_obsidian_api():
        log("Abandon: Obsidian non disponible")
        sys.exit(1)

    # 2. Lancer le tunnel
    url, process = start_tunnel()
    if not url:
        log("Abandon: tunnel non démarré")
        sys.exit(1)

    # 3. Sauvegarder l'URL
    save_url(url)

    # 4. Envoyer par email
    send_email(url)

    log(f"Tunnel actif: {url}")
    log("Le tunnel tourne en arrière-plan. Ne fermez pas cette fenêtre.")

    # 5. Garder le processus en vie
    try:
        process.wait()
    except KeyboardInterrupt:
        log("Arrêt du tunnel (Ctrl+C)")
        process.kill()


if __name__ == "__main__":
    main()
