#!/usr/bin/env python3
"""Claude Code statusline - context window % + rate limits + session cost"""
import sys, json, math
# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def bar(pct, width=12):
    filled = round(pct / 100 * width)
    empty = width - filled
    if pct >= 85:
        color = "\033[91m"   # red
    elif pct >= 60:
        color = "\033[93m"   # yellow
    else:
        color = "\033[92m"   # green
    reset = "\033[0m"
    return f"{color}{'█' * filled}{'░' * empty}{reset}"

def fmt_reset(epoch_secs):
    if not epoch_secs:
        return ""
    import time
    remaining = epoch_secs - time.time()
    if remaining <= 0:
        return "now"
    h = int(remaining // 3600)
    m = int((remaining % 3600) // 60)
    if h > 0:
        return f"{h}h{m:02d}m"
    return f"{m}m"

def fmt_reset_days(epoch_secs):
    if not epoch_secs:
        return ""
    import time
    remaining = epoch_secs - time.time()
    if remaining <= 0:
        return "now"
    days = remaining / 86400
    return f"{days:.1f}j".replace(".", ",")

try:
    data = json.loads(sys.stdin.read())
except:
    print("claude-code", end="")
    sys.exit(0)

parts = []

# Context window bar (always present)
ctx = data.get("context_window", {})
ctx_pct = ctx.get("used_percentage", 0) or 0
ctx_pct_int = int(ctx_pct)
parts.append(f"CTX {bar(ctx_pct_int)} {ctx_pct_int:3d}%")

# Rate limits (Pro/Max users)
rl = data.get("rate_limits", {})
five_h = rl.get("five_hour", {})
seven_d = rl.get("seven_day", {})

if five_h.get("used_percentage") is not None:
    pct = int(five_h["used_percentage"])
    reset_str = fmt_reset(five_h.get("resets_at"))
    reset_label = f" ↺{reset_str}" if reset_str else ""
    parts.append(f"5h {bar(pct, 8)} {pct:3d}%{reset_label}")

if seven_d.get("used_percentage") is not None:
    pct = int(seven_d["used_percentage"])
    reset_str_7d = fmt_reset_days(seven_d.get("resets_at"))
    reset_label_7d = f" ↺{reset_str_7d}" if reset_str_7d else ""
    parts.append(f"7d {bar(pct, 8)} {pct:3d}%{reset_label_7d}")

# Session cost
cost = data.get("cost", {})
usd = cost.get("total_cost_usd", 0) or 0
if usd > 0:
    parts.append(f"\033[36m${usd:.3f}\033[0m")

# Model
model = data.get("model", {}).get("display_name", "")
if model:
    short = model.replace("Claude ", "").replace("Sonnet", "S").replace("Opus", "O").replace("Haiku", "H")
    parts.append(f"\033[35m{short}\033[0m")

print(" │ ".join(parts), end="")
