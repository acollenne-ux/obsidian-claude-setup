"""
Lance Obsidian + tunnel Cloudflare automatiquement au démarrage Windows.
- Ouvre Obsidian s'il n'est pas déjà ouvert
- Ne lance qu'une seule instance du tunnel (vérifie si déjà en cours)
- Capture l'URL du tunnel et l'envoie par email avec la clé API
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
CLOUDFLARED_PATH = r"C:\Users\Alexandre collenne\AppData\Local\Microsoft\WinGet\Links\cloudflared.exe"
OBSIDIAN_PATH = r"C:\Users\Alexandre collenne\AppData\Local\Programs\Obsidian\Obsidian.exe"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
URL_FILE = os.path.join(SCRIPT_DIR, "current_tunnel_url.txt")
LOG_FILE = os.path.join(SCRIPT_DIR, "tunnel.log")
PID_FILE = os.path.join(SCRIPT_DIR, "tunnel.pid")


def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def is_process_running(name):
    """Vérifie si un processus est en cours d'exécution."""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {name}", "/NH"],
            capture_output=True, text=True, timeout=10
        )
        return name.lower() in result.stdout.lower()
    except Exception:
        return False


def is_tunnel_already_running():
    """Vérifie si une instance du tunnel tourne déjà via le PID file."""
    if not os.path.exists(PID_FILE):
        return False
    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        # Vérifier si le PID est encore actif
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
            capture_output=True, text=True, timeout=10
        )
        if "cloudflared" in result.stdout.lower():
            log(f"Tunnel déjà actif (PID {pid})")
            return True
    except Exception:
        pass
    # PID invalide, supprimer le fichier
    os.remove(PID_FILE)
    return False


def start_obsidian():
    """Lance Obsidian s'il n'est pas déjà ouvert."""
    if is_process_running("Obsidian.exe"):
        log("Obsidian déjà ouvert")
        return

    if not os.path.exists(OBSIDIAN_PATH):
        log(f"ERREUR: Obsidian non trouvé: {OBSIDIAN_PATH}")
        return

    log("Lancement d'Obsidian...")
    subprocess.Popen([OBSIDIAN_PATH], creationflags=0x00000008)  # DETACHED_PROCESS
    log("Obsidian lancé, attente du démarrage...")
    time.sleep(10)


def wait_for_obsidian_api(max_wait=120):
    """Attend que l'API Obsidian soit accessible."""
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
        [CLOUDFLARED_PATH, "tunnel", "--url", "https://localhost:27124", "--no-tls-verify"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Sauvegarder le PID
    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))

    # Lire la sortie pour trouver l'URL
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
        match = re.search(r'(https://[a-z0-9-]+\.trycloudflare\.com)', line)
        if match:
            url = match.group(1)
            log(f"URL du tunnel: {url}")
            break

    if not url:
        log("ERREUR: URL du tunnel non trouvée dans les 30 secondes")
        process.kill()
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        return None, None

    return url, process


def save_url(url):
    """Sauvegarde l'URL dans un fichier pour référence."""
    with open(URL_FILE, "w", encoding="utf-8") as f:
        f.write(url)
    log(f"URL sauvegardée dans {URL_FILE}")


def send_email(url):
    """Envoie l'URL + clé API par email via send_report.py."""
    if not os.path.exists(SEND_REPORT_SCRIPT):
        log(f"send_report.py non trouvé: {SEND_REPORT_SCRIPT}")
        return False

    report_file = os.path.join(SCRIPT_DIR, "tunnel_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"""# Tunnel Obsidian actif

## URL du tunnel

{url}

## Cle API Obsidian

{OBSIDIAN_API_KEY}

## Configuration claude.ai

1. Va sur claude.ai - Settings - Integrations - MCP Servers
2. Ajoute ou modifie le serveur Obsidian :
   - URL : {url}
   - Header Name : Authorization
   - Header Value : Bearer {OBSIDIAN_API_KEY}

## Test rapide (colle dans un terminal)

curl -s -H "Authorization: Bearer {OBSIDIAN_API_KEY}" {url}/

---

Genere automatiquement le {time.strftime("%d/%m/%Y a %H:%M")}

Rappel : Obsidian + cloudflared doivent rester ouverts sur le PC.
""")

    try:
        result = subprocess.run(
            [PYTHON_PATH, SEND_REPORT_SCRIPT,
             "Tunnel Obsidian - Nouvelle URL",
             "--file", report_file,
             EMAIL],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            log("Email envoyé avec succès")
            return True
        else:
            log(f"Erreur envoi email: {result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"Exception envoi email: {e}")
        return False


def cleanup():
    """Nettoyage à l'arrêt."""
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def main():
    log("=== Démarrage tunnel Obsidian ===")

    # 0. Vérifier si le tunnel tourne déjà
    if is_tunnel_already_running():
        log("Le tunnel tourne déjà. Arrêt du script.")
        sys.exit(0)

    # 1. Ouvrir Obsidian s'il n'est pas déjà ouvert
    start_obsidian()

    # 2. Attendre que l'API Obsidian soit prête
    log("Attente de l'API Obsidian...")
    if not wait_for_obsidian_api():
        log("Abandon: Obsidian non disponible")
        cleanup()
        sys.exit(1)

    # 3. Lancer le tunnel
    url, process = start_tunnel()
    if not url:
        log("Abandon: tunnel non démarré")
        cleanup()
        sys.exit(1)

    # 4. Sauvegarder l'URL
    save_url(url)

    # 5. Envoyer par email (URL + clé API)
    send_email(url)

    log(f"Tunnel actif: {url}")
    log("Tunnel en arrière-plan. Ne fermez pas cette fenêtre.")

    # 6. Garder le processus en vie
    try:
        process.wait()
    except KeyboardInterrupt:
        log("Arrêt du tunnel (Ctrl+C)")
        process.kill()
    finally:
        cleanup()


if __name__ == "__main__":
    main()
