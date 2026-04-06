#!/bin/bash
# Lance un tunnel Cloudflare pour exposer l'API Obsidian à claude.ai
# Obsidian doit etre ouvert avec le plugin Local REST API actif

echo "=== Tunnel Obsidian → claude.ai ==="
echo "Obsidian Local REST API doit etre actif sur localhost:27124"
echo ""

# Verifier que l'API est accessible
if curl -s -k https://127.0.0.1:27124/ > /dev/null 2>&1; then
    echo "[OK] API Obsidian accessible"
else
    echo "[ERREUR] API Obsidian non accessible. Ouvre Obsidian d'abord."
    exit 1
fi

# Lancer cloudflared
if command -v cloudflared &> /dev/null; then
    echo "[INFO] Lancement du tunnel Cloudflare..."
    echo "[INFO] Copie l'URL affichee ci-dessous et ajoute-la dans claude.ai → Settings → MCP"
    echo ""
    cloudflared tunnel --url https://localhost:27124 --no-tls-verify
else
    echo "[ERREUR] cloudflared non installe."
    echo "  Installation: winget install Cloudflare.cloudflared"
    echo "  Ou: brew install cloudflared (macOS)"
    exit 1
fi
