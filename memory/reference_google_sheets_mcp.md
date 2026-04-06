---
name: Google Sheets MCP
description: MCP mcp-gsheets v1.6.0 avec service account claude-sheets sur projet Google Cloud gen-lang-client-0947498109
type: reference
---

## Google Sheets MCP

**Package** : `mcp-gsheets` v1.6.0 (installé globalement via npm)
**Binaire** : `C:\Users\Alexandre collenne\AppData\Roaming\npm\mcp-gsheets.cmd`
**Projet GCP** : `gen-lang-client-0947498109` ("googlesheet projet")
**Service Account** : `claude-sheets@gen-lang-client-0947498109.iam.gserviceaccount.com`
**Clé JSON** : `C:\Users\Alexandre collenne\.claude\google-sa-key.json`

### APIs activées
- Google Sheets API
- Google Drive API

### Utilisation
- Chaque Google Sheet doit être **partagé** avec l'email du service account (rôle Éditeur)
- Quota : 300 req/min par projet

### Note technique
- `npx -y mcp-gsheets@latest` ne fonctionne PAS sur ce PC (bug cache npx + Node v24.13.1)
- Solution : installation globale (`npm install -g mcp-gsheets`) → binaire `.cmd` direct
