---
name: TradingView MCP (tradesdontlie)
description: MCP TradingView Desktop local — 78 outils (charts, Pine Script, alertes, replay, screenshots) via port debug 9222
type: reference
---

## TradingView MCP Server (local)

**Repo source** : `tradesdontlie/tradingview-mcp`
**Installation locale** : `C:\Users\Alexandre collenne\.claude\tradingview-mcp\`
**Entry point** : `node src/server.js`
**Config MCP** : dans `.claude.json` → `tradingview` → `node C:\...\tradingview-mcp\src\server.js`

### Prérequis pour fonctionner
1. **TradingView Desktop** doit être installé sur le PC
2. **Lancer TradingView avec le port de débogage** :
   ```
   "C:\Program Files\TradingView\TradingView.exe" --remote-debugging-port=9222
   ```
3. Se connecter à son compte TradingView dans l'app
4. Claude Code doit tourner **en local** (pas web)

### 78 outils disponibles
| Catégorie | Outils clés |
|-----------|------------|
| Lecture chart | `quote_get`, `data_get_ohlcv`, `data_get_study_values`, `chart_get_state` |
| Pine Script | `pine_set_source`, `pine_smart_compile`, `pine_save`, `pine_get_errors` |
| Contrôle chart | `chart_set_symbol`, `chart_set_timeframe`, `chart_manage_indicator` |
| Watchlists/Alertes | `watchlist_get`, `watchlist_add`, `alert_create`, `alert_list` |
| Replay/Backtest | `replay_start`, `replay_step`, `replay_trade`, `replay_status` |
| Screenshots | `capture_screenshot`, `batch_run` (multi-symboles) |
| Dessin | `draw_shape`, `draw_list`, `draw_clear` |

### Limitation
- Ne fonctionne PAS depuis Claude Code web — uniquement en local
- TradingView Desktop doit être ouvert AVANT de lancer Claude Code
- Le port 9222 doit être libre

### Statut (05/04/2026)
- TradingView Desktop **installé** : v3.0.0.7652 (Microsoft Store / MSIX / Electron 38.2.2)
- Chemin : `C:\Program Files\WindowsApps\TradingView.Desktop_3.0.0.7652_x64__n534cwy3pjxzj\TradingView.exe`
### PROBLEME BLOQUANT — Version Microsoft Store
- La version MSIX (Store) **ne peut PAS** accepter `--remote-debugging-port=9222`
- L'exe ne démarre pas hors du conteneur MSIX (copie impossible)
- Les env vars Electron ne sont pas lues par les apps MSIX
- Le patch in-place de l'app.asar dans WindowsApps est bloqué par la protection Windows

### Solution : installer la version standalone
1. Télécharger depuis **tradingview.com/desktop/** (version .exe classique, PAS Microsoft Store)
2. Installer dans `C:\Program Files\TradingView\` ou `%LOCALAPPDATA%\TradingView\`
3. Lancer via : `launch_tradingview_debug.ps1` (dans `~/.claude/`)
4. Le MCP la détectera automatiquement via `tv_launch`

### Fallback actif
- Le MCP tradingview (tradesdontlie) est installé et connecté à Claude Code — les 78 outils sont chargés, mais ils échouent tant que TradingView n'a pas le port 9222 actif
- Script de lancement prêt : `~/.claude/launch_tradingview_debug.ps1`
