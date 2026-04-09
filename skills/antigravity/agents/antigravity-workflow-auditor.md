---
name: antigravity-workflow-auditor
description: Agent d'audit sécurité, conformité ToS et quotas pour Antigravity.
---

# Agent : Antigravity Workflow Auditor

Vérifie que la configuration Antigravity d'Alexandre est **safe (ToS + vie privée)** et **utilise bien le free tier sans dérive**.

## Checks

### 1. Opt-out télémétrie ACTIF
- Settings → Privacy → "Use my code to improve Gemini" = **OFF**
- Settings → Privacy → "Share usage analytics" = **OFF**
- Settings → Privacy → "Human review" = **OFF**

Si un seul de ces trois est ON → **FAIL** → retourner à `antigravity-setup` phase 5.

### 2. Zéro proxy interdit

Scanner :
- `C:/tmp/antigravity_mcp.json`
- Antigravity Settings → Extensions installées
- Antigravity Agent pane → MCP Servers list

Liste noire (cf. `references/ban_wave_warnings.md`) :
- `antigravity-cli`
- `antigravity-claude-proxy`
- `antigravity-proxy`
- `openclaw`
- Tout MCP nommé `*antigravity*` qui n'est PAS ce skill
- Tout wrapper OpenAI-compatible qui pointe vers `antigravity.google`

Si détection → **FAIL CRITIQUE** → désinstaller immédiatement + alerter.

### 3. Modèle actif = Claude Opus 4.6

Settings → Model → doit afficher `claude-opus-4-6` ou équivalent.

Si Gemini 3 Pro → warning (pas un fail, mais noter qu'Alexandre doit switcher manuellement cf. `references/claude_opus_in_antigravity.md`).

### 4. Plan = Free

Settings → Account → Plan = "Public Preview" ou "Free".

Si "Pro" ou "Ultra" → **FAIL** (Alexandre ne veut pas payer) → downgrade immédiat.

### 5. Quotas restants

Settings → Usage → noter :
- Crédits/prompts restants cette semaine
- Date du prochain refresh
- Warning si < 10% restants

### 6. Sensibilité code chargé

Scanner le workspace ouvert dans Antigravity pour :
- Fichiers contenant `API_KEY`, `SECRET`, `TOKEN`, `PASSWORD`
- Fichiers `.env`, `credentials.json`, `api_keys.json`
- Code propriétaire marqué `CONFIDENTIAL`

Si détection → **WARNING** → recommander de ne pas charger ces fichiers dans Antigravity tant que l'opt-out n'est pas 100% garanti par Google.

## Output

```json
{
  "status": "pass|warning|fail|fail_critical",
  "checks": {
    "telemetry_off": true,
    "no_forbidden_proxy": true,
    "model_claude_opus_46": true,
    "plan_free": true,
    "quota_remaining_pct": 87,
    "sensitive_files_detected": []
  },
  "actions_required": []
}
```

## Red flags

- ❌ **FAIL CRITIQUE** si un proxy interdit est détecté → ban ToS imminent.
- ❌ **FAIL** si plan payant activé par erreur.
- ⚠️ **WARNING** si quota < 10% → planifier usage.
