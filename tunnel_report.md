# Tunnel Obsidian actif

## URL du tunnel

https://api.trycloudflare.com

## Cle API Obsidian

cf80b686546b090a1df531d73a09d7fd51820c76b86041859e63e281ed5909a2

## Configuration claude.ai

1. Va sur claude.ai - Settings - Integrations - MCP Servers
2. Ajoute ou modifie le serveur Obsidian :
   - URL : https://api.trycloudflare.com
   - Header Name : Authorization
   - Header Value : Bearer cf80b686546b090a1df531d73a09d7fd51820c76b86041859e63e281ed5909a2

## Test rapide (colle dans un terminal)

curl -s -H "Authorization: Bearer cf80b686546b090a1df531d73a09d7fd51820c76b86041859e63e281ed5909a2" https://api.trycloudflare.com/

---

Genere automatiquement le 06/04/2026 a 16:52

Rappel : Obsidian + cloudflared doivent rester ouverts sur le PC.
