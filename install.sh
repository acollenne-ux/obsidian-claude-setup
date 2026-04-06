#!/bin/bash
# Installation automatique Obsidian + Claude Code
# Usage: bash install.sh YOUR_API_KEY

API_KEY="${1:-}"

echo "=== Installation Obsidian Skills pour Claude Code ==="

# 1. Copier les skills
SKILL_DIR="$HOME/.claude/skills"
mkdir -p "$SKILL_DIR"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for skill in obsidian-markdown obsidian-bases json-canvas obsidian-cli defuddle; do
    if [ -d "$SCRIPT_DIR/skills/$skill" ]; then
        cp -r "$SCRIPT_DIR/skills/$skill" "$SKILL_DIR/"
        echo "[OK] Skill $skill installe"
    else
        echo "[ERREUR] Skill $skill non trouve"
    fi
done

# 2. Ajouter le MCP server
if command -v claude &> /dev/null; then
    claude mcp add mcp-obsidian -- uvx mcp-obsidian
    echo "[OK] MCP mcp-obsidian ajoute"
else
    echo "[INFO] Claude CLI non trouve, MCP non ajoute automatiquement"
fi

# 3. Configurer la cle API
if [ -n "$API_KEY" ]; then
    echo ""
    echo "[INFO] Cle API fournie. Ajoute manuellement dans ~/.claude.json :"
    echo '  "env": { "OBSIDIAN_API_KEY": "'$API_KEY'" }'
    echo ""
    echo "[TEST] Verification connexion..."
    curl -s -k -H "Authorization: Bearer $API_KEY" https://127.0.0.1:27124/ | head -5
else
    echo ""
    echo "[INFO] Pas de cle API fournie."
    echo "  1. Ouvre Obsidian → Settings → Community plugins → Install 'Local REST API'"
    echo "  2. Copie la cle API dans Settings → Local REST API"
    echo "  3. Relance: bash install.sh YOUR_API_KEY"
fi

echo ""
echo "=== Installation terminee ==="
