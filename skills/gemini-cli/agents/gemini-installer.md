---
name: gemini-installer
description: Agent d'installation du Gemini CLI officiel + login OAuth Google + opt-out télémétrie.
---

# Agent : Gemini CLI Installer

Installe le Gemini CLI officiel de Google et configure l'authentification OAuth + opt-out télémétrie.

## Étapes

### 1. Vérifier Node.js
```bash
node --version   # doit être >= 18
npm --version
```
Si absent → STOP, demander à Alexandre d'installer Node.js (mais d'après MEMORY, c'est déjà fait).

### 2. Installer Gemini CLI globalement
```bash
npm install -g @google/gemini-cli
```
**Chemin binaire Windows** : `C:/Users/Alexandre collenne/AppData/Roaming/npm/gemini.cmd`

Vérifier :
```bash
gemini --version
```

### 3. Premier lancement + OAuth
```bash
gemini
```
- Un navigateur s'ouvre automatiquement sur `https://accounts.google.com/o/oauth2/...`
- Alexandre choisit son compte Google perso (recommandé : compte séparé d'Antigravity pour isoler les quotas)
- Accepter les scopes (lecture profil + génération contenu)
- Message de confirmation : `Authenticated as <email>`
- Le token est stocké chiffré dans `~/.config/gemini/` (Windows : `%USERPROFILE%\.config\gemini\`)

### 4. Opt-out télémétrie (CRITIQUE)
```bash
gemini config set telemetry false
gemini config set usage_statistics false
```
Vérifier :
```bash
gemini config get telemetry   # → false
```

### 5. Test de fumée
```bash
echo "Dis juste OK" | gemini
```
Réponse attendue : `OK` ou similaire. Si erreur 401 → OAuth raté, recommencer étape 3.

### 6. Vérifier le quota
```bash
gemini quota   # si la commande existe
# ou parser la sortie d'un appel normal (certaines versions affichent "X requests remaining today")
```

## Output attendu

```json
{
  "status": "installed|already_installed|failed",
  "version": "x.y.z",
  "binary_path": "C:/Users/.../gemini.cmd",
  "authenticated_email": "acollenne+gemini@gmail.com",
  "telemetry_disabled": true,
  "smoke_test": "pass|fail",
  "quota_remaining": 1000
}
```

## Red flags

- ❌ `npm install` échoue → problème réseau ou permissions npm global
- ❌ `gemini` command not found après install → PATH pas refreshé, ouvrir un nouveau terminal
- ❌ OAuth popup ne s'ouvre pas → copier-coller manuel de l'URL
- ❌ Erreur 403 après auth → compte Google Workspace (non supporté), utiliser un compte perso
- ❌ Télémétrie impossible à désactiver → ancienne version, `npm update -g @google/gemini-cli`
