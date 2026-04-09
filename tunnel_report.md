# Tunnel Obsidian actif

## URL du tunnel

https://arbitrary-sierra-routing-apr.trycloudflare.com

## Cle API Obsidian

cf80b686546b090a1df531d73a09d7fd51820c76b86041859e63e281ed5909a2

## Configuration claude.ai

1. Va sur claude.ai - Settings - Integrations - MCP Servers
2. Ajoute ou modifie le serveur Obsidian :
   - URL : https://arbitrary-sierra-routing-apr.trycloudflare.com
   - Header Name : Authorization
   - Header Value : Bearer cf80b686546b090a1df531d73a09d7fd51820c76b86041859e63e281ed5909a2

## Test rapide (colle dans un terminal)

curl -s -H "Authorization: Bearer cf80b686546b090a1df531d73a09d7fd51820c76b86041859e63e281ed5909a2" https://arbitrary-sierra-routing-apr.trycloudflare.com/

---

Genere automatiquement le 09/04/2026 a 08:39

Rappel : Obsidian + cloudflared doivent rester ouverts sur le PC.
