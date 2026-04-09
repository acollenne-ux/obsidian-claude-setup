---
name: Skill antigravity créé 08/04/2026
description: Connecteur Google Antigravity free tier, bridge MCP sens Claude Code → Antigravity, placé en L3 SPECIALIST. Inclut hard-gates anti-ban-wave.
type: project
---

# Skill `antigravity` — créé 2026-04-08

**Emplacement** : `~/.claude/skills/antigravity/` (L3 SPECIALIST, pattern identique à `n8n-management`).

**Why** : Antigravity (Google DeepMind, 18/11/2025) = IDE agentic gratuit avec Claude Opus 4.6 + Sonnet 4.5 **nativement inclus dans le free tier**. Intérêt pour Alexandre (pas de forfait payant) : second IDE pour économiser les quotas Claude Code, profiter de la Manager view multi-agents et du browser sub-agent natif, tout en réutilisant son écosystème MCP existant (Obsidian, n8n, Figma, GitHub, TradingView...).

**How to apply** :
- Le skill est auto-invoqué sur triggers "antigravity", "gemini 3 ide", "mission control", "manager view", "ide gratuit claude".
- 6 phases : DETECT → SETUP → BRIDGE → MODEL SELECT (Opus 4.6) → AUDIT → DELIVERY.
- 3 agents : `antigravity-setup`, `antigravity-mcp-bridge`, `antigravity-workflow-auditor`.
- 4 references : `free_tier_limits`, `mcp_bridge_recipes`, `ban_wave_warnings`, `claude_opus_in_antigravity`.
- 1 outil : `tools/generate_mcp_config.py` (lit `~/.claude.json`, génère `antigravity_mcp.json` filtré + exclusion proxies interdits).

**⚠️ HARD-GATES NON-NÉGOCIABLES** :
1. **JAMAIS** `antigravity-cli`, `antigravity-claude-proxy`, `openclaw`, `antigravity-proxy` → **ban wave Google février 2026** (OpenClaw banni sans appel, creator parti chez OpenAI). Ces outils ré-exposent Antigravity vers l'extérieur = violation ToS.
2. **TOUJOURS opt-out télémétrie** (Settings → Privacy) avant tout code sensible — par défaut le code sert à entraîner Gemini.
3. **TOUJOURS Claude Opus 4.6 natif** via le sélecteur Antigravity, jamais via proxy.
4. Bridge MCP = sens **unique Claude Code → Antigravity** (on expose nos MCPs à Antigravity, on ne pilote PAS Antigravity depuis l'extérieur — pas d'API REST publique de toute façon).

**Verdict d'utilité deep-research** : **moyennement utile** pour un user gratuit — vraie valeur = second IDE avec Opus 4.6 inclus + Manager view. Faible risque si on respecte les hard-gates. Re-tester trimestriellement (pricing post-preview TBD).

**Chaînage L4** : `pdf-report-pro` (rapport setup) → `qa-pipeline` → `retex-evolution`.

**Sources clés** :
- https://antigravity.google
- https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/
- https://venturebeat.com/orchestration/google-clamps-down-on-antigravity-malicious-usage-cutting-off-openclaw-users
