---
name: multi-ia-router
description: "Routage intelligent multi-IA : sélection du meilleur modèle, consensus voting, fallback chains. Use when: multi-IA routing needed, consensus validation, model selection. Triggers: 'multi-ia', 'consensus', 'comparer les IA'."
---

# Multi-IA Router — Routage Intelligent et Consensus

Sélectionner la meilleure IA pour chaque sous-tâche, orchestrer le consensus voting, et gérer les fallbacks automatiques.

---

## IAs ACTIVES — Benchmarks réels (28/03/2026)

| IA | Modèles | Chat | Reason | Forces N°1 | Faiblesses |
|----|---------|------|--------|-----------|------------|
| **Gemini 2.5 Flash** | gemini-2.5-flash | 8.2s | 9.6s | **CODE 10/10**, **FINANCE 10/10**, contexte 1M | Lent en chat, verbosité x3 |
| **Mistral** | small/large/codestral | 5.2s | 9.9s | **FRANÇAIS 10/10**, macro, rapports | Code parfois bugué (sauf Codestral) |
| **Groq** | llama-3.3-70b / qwen3-32b / gpt-oss-120b | **⚡2.8s** | **⚡5.1s** | **VITESSE 10/10**, gratuit | Moins précis tâches complexes |
| **OpenRouter** | llama-3.3-70b / deepseek-r1 | 6.7s | **4.3s** | **DeepSeek-R1 le + rapide** | Chat parfois lent |
| **HuggingFace** | Llama-3.3-70B / DeepSeek-R1 | **⚡2.0s** | 19.2s | **CHAT LE + RAPIDE**, gratuit | R1 parfois vide |
| **DeepSeek** | deepseek-chat / deepseek-reasoner | ❌ | ❌ | Raisonnement natif profond | ⚠️ Solde vide |

---

## MATRICE DE ROUTAGE PAR TYPE DE TÂCHE

| Tâche | IA Primaire | IA Secondaire | IA Tertiaire | Mode |
|-------|------------|---------------|--------------|------|
| **Calcul financier** (DCF, comps) | Gemini Flash | Mistral Large | DeepSeek-R1 (OR) | Consensus 3 IAs |
| **Analyse macro FR** | Mistral Large | Gemini Flash | Groq GPT-OSS | Consensus 2+ |
| **Code Python/JS/Pine** | Gemini Flash | Mistral Codestral | Groq Qwen3 | Best-of-3 |
| **Raisonnement math/logique** | DeepSeek-R1 (OR 4.3s) | Gemini Flash | Groq Qwen3 | Best-of-2 |
| **Questions rapides / faits** | Groq Llama (2.8s) | HF Llama (2.0s) | Mistral Small | First-response |
| **Synthèse multi-docs** | Gemini Flash (1M ctx) | Mistral Large | Groq GPT-OSS | Best quality |
| **Rédaction rapport FR** | Mistral Large | Gemini Flash | HF Llama | Best quality |
| **Vérification croisée** | TOUTES en // | — | — | Consensus obligatoire |
| **Recherche académique** | HF MCP (papers) | DeepSeek-R1 | Gemini Flash | Best-of-2 |
| **Extraction données** | Gemini Flash | Mistral Large | Groq | Best quality |

---

## PROTOCOLE CURL — Appels API directs

**Récupérer les clés depuis `C:\Users\Alexandre collenne\.claude\tools\api_keys.json`.**

```bash
# === GROQ (ultra-rapide ~500 tps, gratuit) ===
curl -s -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"QUESTION"}],"temperature":0.3,"max_tokens":4096}'
# Modèles : llama-3.3-70b-versatile (chat), qwen-qwq-32b (reason), llama-3.1-8b-instant (rapide)

# === MISTRAL (N°1 français) ===
curl -s -X POST https://api.mistral.ai/v1/chat/completions \
  -H "Authorization: Bearer $MISTRAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"mistral-large-latest","messages":[{"role":"user","content":"QUESTION"}],"temperature":0.3,"max_tokens":4096}'
# Modèles : mistral-large-latest (reason), mistral-small-latest (chat), codestral-latest (code)

# === OPENROUTER (DeepSeek-R1) ===
curl -s -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek/deepseek-r1","messages":[{"role":"user","content":"QUESTION"}],"temperature":0.3,"max_tokens":4096}'

# === GOOGLE GEMINI (N°1 code + finance) ===
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"QUESTION"}]}],"generationConfig":{"temperature":0.3,"maxOutputTokens":4096}}'

# === HUGGINGFACE (chat ultra-rapide 2.0s) ===
curl -s -X POST https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct/v1/chat/completions \
  -H "Authorization: Bearer $HF_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"meta-llama/Llama-3.3-70B-Instruct","messages":[{"role":"user","content":"QUESTION"}],"temperature":0.3,"max_tokens":4096}'
```

**Script multi_ai.py (si Python disponible) :**
```bash
python "C:\Users\Alexandre collenne\.claude\tools\multi_ai.py" query "question" --mode reason --best
```

---

## PROTOCOLE DE CONSENSUS VOTING (obligatoire sur données critiques)

Pour les chiffres financiers, dates, faits vérifiables et recommandations :

1. **Envoyer la MÊME question à 3 IAs minimum** (en parallèle via bash `&`)
2. **Comparer les réponses** :
   - 3/3 convergent → **CONFIANCE ÉLEVÉE** ✓✓✓
   - 2/3 convergent → **CONFIANCE MOYENNE** ✓✓ — noter la divergence
   - 0/3 convergent → **CONFIANCE FAIBLE** ✓ — vérifier via WebSearch
3. **Agréger** : prendre la réponse la plus complète parmi celles qui convergent
4. **Documenter** : noter quelles IAs ont convergé/divergé

```bash
# Consensus voting parallèle :
QUESTION="[question]"
curl -s [GROQ] -d "{...}" > /tmp/groq_resp.json &
curl -s [MISTRAL] -d "{...}" > /tmp/mistral_resp.json &
curl -s [GEMINI] -d "{...}" > /tmp/gemini_resp.json &
wait
# Comparer les 3 réponses
```

---

## FALLBACK CHAINS

Si une IA échoue (timeout >30s, erreur 429/500, réponse vide) :
1. Passer automatiquement à l'IA Secondaire
2. Si Secondaire échoue → Tertiaire
3. Si toutes échouent → WebSearch comme ultime fallback
4. Documenter l'échec dans le RETEX

| Outil principal | Fallback |
|----------------|---------|
| Gemini (quota) | Gemini Flash ou Mistral |
| Groq (rate limit) | Mistral ou HuggingFace |
| Mistral (erreur) | Groq ou Gemini |
| DeepSeek (solde vide) | Mistral Large |
| HuggingFace R1 (vide) | OpenRouter R1 |
| WebFetch (403) | WebSearch avec URL + quotes |
| multi_ai.py (Python absent) | Protocole curl direct |
| ~~Bigdata.com~~ (EXPIRÉ) | FMP API + WebSearch |

---

## ALERTES CRITIQUES PAR IA

- **DeepSeek R1 : 14.3% hallucinations** (vs 3.5% V3). TOUJOURS vérifier via 2e source.
- **Gemini 2.5 Flash : verbosité x3**. Prompts concis obligatoires.
- **DeepSeek R1 : sécurité faible** (100% taux succès attaque). Filtrer via Agent QA.
- **Llama 3.3 70B : text-only**. Router vers Gemini pour image/vidéo.
- **DeepSeek Chat : contexte 64K max**. Router vers Gemini (1M) pour docs longs.
- **HuggingFace R1 : réponses parfois vides**. Fallback vers OpenRouter R1.

---

## RÈGLES DE SÉLECTION

- **Finance/code** → Gemini Flash en primaire (10/10)
- **Français/macro/rédaction** → Mistral Large en primaire (10/10)
- **Raisonnement profond** → DeepSeek-R1 via OpenRouter (4.3s)
- **Vitesse** → Groq (2.8s) ou HuggingFace (2.0s)
- **Vérification** → TOUTES en parallèle `--aggregate`
- Mettre les IAs de raisonnement APRÈS les outils de collecte
- Paralléliser les tâches sans dépendances

---

## FORMAT DE SORTIE

```
MULTI-IA ROUTING — [titre]

IAs mobilisées    : [liste avec rôle]
Mode consensus    : [oui/non — si oui, résultat convergence]
Fallbacks activés : [liste si applicable]
Temps total       : [X]s
Qualité réponses  : [score moyen /10]
```

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Une seule IA suffit pour cette tâche" | En mode STANDARD/FULL, minimum 2 IAs pour le consensus. Une seule IA = pas de validation croisée. |
| "Claude est le meilleur pour tout" | Chaque IA a ses forces. Gemini pour le code, DeepSeek pour le raisonnement, Groq pour la vitesse. |
| "Le consensus ralentit trop" | Les appels sont en parallèle. Le surcoût est minimal vs le gain en fiabilité. |
| "Le provider est down, on abandonne" | Fallback chain OBLIGATOIRE. Si un provider échoue, passer au suivant. |
| "Les scores de routage sont fixes" | Les scores doivent évoluer avec le benchmark continu. Mettre à jour après chaque session. |

## RED FLAGS — STOP

- Réponse sans consensus quand 2+ IAs étaient disponibles → STOP
- Provider en erreur sans fallback activé → STOP
- Scores de routage jamais mis à jour → STOP

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Invoqué par | `deep-research` (Phase 4, mode STANDARD/FULL) |
| Benchmark IAs | `retex-evolution` |
| Validation résultats | `qa-pipeline` |
| Configuration clés | `reference_api_keys.md` |

## ÉVOLUTION

Après chaque session multi-IA :
- Si un provider a échoué → mettre à jour son score de fiabilité
- Si les temps de réponse ont changé → recalibrer le routage vitesse
- Si une IA a surpris (qualité inattendue) → ajuster son score domaine

Seuils : taux d'échec provider > 30% → le déprioritiser automatiquement.
