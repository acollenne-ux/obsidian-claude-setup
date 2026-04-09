---
name: Clés API IA externes
description: Emplacement des clés API pour les IAs externes utilisées par multi_ai.py et le skill deep-research
type: reference
---

Les clés API sont stockées dans `C:\Users\Alexandre collenne\.claude\tools\ai_config.json`.

Providers actifs (28 mars 2026, benchmarkés) :
- **Gemini** : gemini-2.5-flash, **N°1 code+finance** (10/10), chat 8.2s, reason 9.6s, contexte 1M tokens
- **Mistral** : small (chat 5.2s) + large (reason 9.9s), **N°1 français** (10/10), macro, rédaction
- **Groq** : llama-3.3-70b (chat), qwen3-32b (reason), gpt-oss-120b (large), **N°1 vitesse** ~500tps, 2.8s
- **OpenRouter** : deepseek-r1 (reason 4.3s le + rapide), llama-3.3-70b (chat), 200+ modèles
- **HuggingFace** : 2 tokens actifs dans `ai_config.json` (clé primaire `hf_RWke...Voci`) + ancienne (`hf_MDHY...uBXE` — invalide sur whoami mais fonctionne sur inference). Endpoint migré vers `router.huggingface.co/hf-inference/` (ancien `api-inference.huggingface.co` retourne 410). Llama-3.3-70B (chat **2.0s**), DeepSeek-R1 (reason), FLUX.1-schnell (image gen)
- **DeepSeek** : solde vide — recharger sur platform.deepseek.com

Providers inactifs :
- **OpenAI** : clé existante mais désactivée
- **xAI/Grok** : clé existante mais crédits manquants
- **GitHub Models** : placeholder, nécessite PAT
