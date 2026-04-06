---
name: Session 28/03/2026 — Upgrades majeurs deep-research + multi-IA + classification actifs
description: Benchmark des 6 IAs, matrice de routage intelligent, classification 8 types d'actifs, fix providers, statusline 7d timer, Phase 10B benchmark continu
type: project
---

## Session du 28 mars 2026 — Résumé complet

### 1. BENCHMARK MULTI-IA (tests réels effectués)

6 providers testés sur 4 types de tâches (DCF financier, code Python, analyse macro FR, math/raisonnement) :

| IA | Chat | Reason | N°1 en... | Faiblesses |
|----|------|--------|-----------|------------|
| Gemini 2.5 Flash | 8.2s | 9.6s | **Code 10/10, Finance 10/10** (DCF parfait) | Verbosité x3 |
| Mistral Large | — | 9.9s | **Français 10/10**, macro, rédaction | Code parfois bugué (lambda auto-référence) |
| Mistral Small | 5.2s | — | Réponses concises rapides | Pas assez profond |
| Groq (Llama/Qwen3/GPT-OSS) | **2.8s** | **5.1s** | **Vitesse 10/10** (~500 tps) | Moins précis sur complexe |
| OpenRouter (DeepSeek-R1) | 6.7s | **4.3s** | **Raisonnement** (AIME 79.8%) | **14.3% hallucinations** |
| HuggingFace (Llama/R1) | **2.0s** | 19.2s | **Chat le + rapide** | R1 parfois vide |
| DeepSeek natif | ❌ | ❌ | Raisonnement profond | Solde vide |

**Why:** Les performances IA changent constamment. Un routage basé sur des benchmarks réels (pas théoriques) garantit la meilleure qualité.

**How to apply:** Consulter la matrice de routage dans deep-research SKILL.md section 3B pour choisir l'IA optimale par type de tâche.

### 2. FICHIERS MODIFIÉS

**ai_config.json** — 3 corrections :
- HuggingFace : `api-inference.huggingface.co` → `router.huggingface.co` (ancien déprécié, erreur 410)
- OpenRouter : `anthropic/claude-sonnet-4` → `deepseek/deepseek-r1` (gratuit)
- Groq : `deepseek-r1-distill-llama-70b` (décommissionné) → `qwen/qwen3-32b` (reason) + `openai/gpt-oss-120b` (large)

**statusline.py** — Timer 7d ajouté :
- Le compteur 7d affiche maintenant `↺Xh XXm` avant reset, identique au 5h

**deep-research SKILL.md** — 4 ajouts majeurs :
1. **Section 1D** : Classification de l'actif (8 types : Growth, Micro-cap, Cyclique, Défensif, REIT, Crypto, Obligation, ETF) avec framework d'analyse spécifique et pièges à éviter pour chaque type
2. **Section 3B** : Matrice de routage intelligent des IAs (10 types de tâches → IA optimale benchmarkée) + alertes critiques (hallucinations R1, verbosité Gemini, etc.)
3. **Section 2A** : Table des IAs avec benchmarks réels (vitesse, scores, forces/faiblesses)
4. **Phase 10B** : Benchmark continu obligatoire à chaque session (tester toutes les IAs, comparer, mettre à jour routage)

**stock-analysis SKILL.md** — Étape 0 ajoutée :
- Classification obligatoire de l'actif avant toute analyse
- Sections 1-6 adaptées par type (métriques différentes selon Growth/Cyclique/REIT/Crypto/etc.)

**rapport_comparaison_ia.md** — Rapport complet créé par l'agent de benchmark (envoyé en PDF)

### 3. RÈGLES CLÉS ÉTABLIES

- **Routage IA par domaine** : Finance→Gemini, Français→Mistral, Raisonnement→DeepSeek-R1, Vitesse→Groq/HF
- **Classification actifs obligatoire** : 8 types avec métriques spécifiques, ne jamais analyser tous les actifs pareil
- **Piège cycliques** : P/E bas en haut de cycle = piège (acheter quand P/E élevé)
- **REIT** : utiliser FFO/AFFO, jamais P/E classique
- **Micro-cap** : prioriser liquidité, dilution, insider %, survie
- **Benchmark continu** : Phase 10B à chaque session pour améliorer le routage
- **Deep-research = toujours** : invoqué pour TOUTES les demandes

### 4. MÉMOIRES CRÉÉES

- `feedback_benchmark_continu.md` — Tester toutes les IAs à chaque demande
- `project_session_20260328_upgrades.md` — Ce fichier (récapitulatif session)
