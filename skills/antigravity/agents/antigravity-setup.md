---
name: antigravity-setup
description: Agent d'installation et login Google Antigravity free tier. Gère téléchargement, install, OAuth, opt-out télémétrie.
---

# Agent : Antigravity Setup

Installe Google Antigravity (free tier, Public Preview), guide le login OAuth Google, et **impose l'opt-out télémétrie** avant toute utilisation.

## Étapes

### 1. Détection installation existante
```bash
# Windows
ls "$LOCALAPPDATA/Programs/Antigravity" 2>/dev/null && echo "INSTALLED" || echo "NOT_INSTALLED"
```
Chemins candidats :
- `%LOCALAPPDATA%\Programs\Antigravity\Antigravity.exe`
- `%PROGRAMFILES%\Antigravity\Antigravity.exe`

Si installé → aller directement étape 3.

### 2. Installation
1. Ouvrir https://antigravity.google via WebFetch pour vérifier la dernière version.
2. Télécharger l'installateur Windows : `https://antigravity.google/download` (lien réel à confirmer sur la page).
3. Demander à Alexandre de lancer l'installateur (desktop-control peut automatiser le double-clic si besoin).
4. Vérifier l'installation (cf. étape 1).

### 3. Login OAuth Google
1. Lancer Antigravity.
2. Écran d'accueil → "Sign in with Google".
3. Utiliser le compte Google d'Alexandre (le même que Gmail principal — `acollenne@gmail.com` d'après MEMORY.md ? à confirmer).
4. Accepter les scopes OAuth (lecture profil + stockage workspace Antigravity).
5. Confirmer que l'UI principale s'ouvre (Manager view visible).

### 4. Vérification free tier
1. Settings → Account → vérifier "Plan: Public Preview (Free)".
2. Quotas visibles : refresh hebdomadaire, pas de carte bancaire exigée.
3. Si un upsell vers Pro/Ultra apparaît → **ignorer, rester sur Free**.

### 5. Opt-out télémétrie (CRITIQUE)
1. Settings → Privacy & Data.
2. Décocher :
   - ❌ "Use my code and prompts to improve Gemini models"
   - ❌ "Share usage analytics"
   - ❌ "Allow human review of conversations"
3. Sauvegarder.
4. Prendre un screenshot (via `desktop-control` ou manuel) pour archive.

### 6. Vérification extensions MCP
1. Agent pane (sidebar droite) → "MCP Servers".
2. Noter qu'il est vide par défaut → prêt pour l'étape BRIDGE du skill principal.

## Output attendu

```json
{
  "status": "installed|already_installed|failed",
  "version": "x.y.z",
  "account": "acollenne@gmail.com",
  "plan": "Public Preview (Free)",
  "telemetry_opted_out": true,
  "screenshots": ["path/to/screenshot1.png", ...],
  "next_phase": "BRIDGE"
}
```

## Red flags

- ❌ Si l'installateur demande une carte bancaire → **STOP**, on ne veut pas payer.
- ❌ Si l'opt-out n'est pas possible (UI différente) → **STOP** et alerter l'utilisateur.
- ❌ Si une pop-up propose d'installer un proxy ou extension tierce (`antigravity-cli`, `openclaw`, etc.) → **REFUSER** (cf. `references/ban_wave_warnings.md`).
