"""
setup_free_ai.py — Configure les IA gratuites en quelques minutes.
Lance avec : python setup_free_ai.py
"""
import json, subprocess, sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "ai_config.json"

print("""
==============================================
  Configuration des IA Gratuites
==============================================

IAs a configurer (toutes GRATUITES) :

1. Groq (RECOMMANDE - rapide, illimite presque)
   -> console.groq.com -> Create API Key
   -> Donne acces : Llama 3.3 70B, DeepSeek-R1, Kimi K2

2. Gemini (Google AI Studio - tres capable)
   -> aistudio.google.com -> Get API Key
   -> Donne acces : Gemini 2.5 Pro, Flash

3. GitHub Models (GPT-4o, Llama, DeepSeek-R1 GRATUIT)
   -> github.com/settings/tokens -> New token (classic)
   -> Cocher : models:read
   -> Donne acces : GPT-4o, Llama 3.3 70B, DeepSeek-R1

4. xAI Grok (25$/mois offerts chaque mois)
   -> console.x.ai -> Create API Key
   -> Donne acces : Grok-3, Grok-3-mini

5. DeepSeek (recharger le compte)
   -> platform.deepseek.com -> Top up balance
   -> Tres peu cher : 0.27$/million tokens
""")

with open(CONFIG_PATH, encoding="utf-8") as f:
    cfg = json.load(f)

providers_to_setup = [
    ("groq", "Groq API Key", "groq"),
    ("gemini", "Gemini API Key (Google AI Studio)", "gemini"),
    ("github_models", "GitHub Personal Access Token", "github_models"),
    ("xai", "xAI API Key (Grok)", "xai"),
    ("deepseek", "DeepSeek API Key (recharger ou nouvelle cle)", "deepseek"),
    ("openai", "OpenAI API Key (optionnel, payant)", "openai"),
]

configured = []
for provider_key, label, cfg_key in providers_to_setup:
    current = cfg[cfg_key].get("api_key", "")
    is_placeholder = current.startswith("PLACEHOLDER") or current == ""
    status = "(deja configure)" if not is_placeholder else "(non configure)"

    key = input(f"\n{label} {status}\n[Entree pour passer] > ").strip()
    if key:
        cfg[cfg_key]["api_key"] = key
        cfg[cfg_key]["enabled"] = True
        configured.append(cfg_key)
        print(f"  -> {cfg_key} configure et active!")
    elif not is_placeholder:
        # Deja configure, on active au cas ou
        cfg[cfg_key]["enabled"] = True

with open(CONFIG_PATH, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)

print(f"\nConfiguration sauvegardee!")
if configured:
    print(f"Nouvelles IA activees : {', '.join(configured)}")

print("\nTest rapide des IA configurees...")
result = subprocess.run(
    [sys.executable, str(Path(__file__).parent / "multi_ai.py"), "list"],
    capture_output=True, text=True
)
print(result.stdout)

print("""
Utilisation dans deep-research :
  python multi_ai.py query "ta question" --mode research --synthesize
  python multi_ai.py query "ta question" --models groq,mistral --best
""")
