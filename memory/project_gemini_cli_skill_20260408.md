---
name: Skill gemini-cli créé 08/04/2026
description: Wrapper Gemini CLI officiel pour accès gratuit Gemini 3 Pro (~1000 req/jour via OAuth), fallback auto multi-ia-router, L3 SPECIALIST utilitaire.
type: project
---

# Skill `gemini-cli` — créé 2026-04-08

**Emplacement** : `~/.claude/skills/gemini-cli/` (L3 SPECIALIST, skill utilitaire bas niveau).

**Why** : Alexandre voulait interroger Gemini 3 Pro depuis Claude Code (vision image→code, génération diagrammes, fallback quand quotas Claude tapés) **sans payer**. Antigravity était exclu (pas d'API publique, ban wave ToS sur les proxies). Solution retenue : wrapper le Gemini CLI officiel open-source de Google qui offre ~1000 req/jour de Gemini 3 Pro gratuit via login OAuth personnel, sans clé API ni facturation.

**How to apply** :
- Auto-invoqué sur triggers "gemini", "gemini 3", "fallback gemini", "vision image", "image vers code", "diagramme depuis screenshot".
- 5 phases : DETECT → INSTALL → INVOKE → FALLBACK → RETURN.
- 2 agents : `gemini-installer` (npm i + OAuth + opt-out télémétrie), `gemini-invoker` (prompt + exec + parsing).
- 3 references : `free_tier_limits`, `use_cases` (matrice Gemini vs Claude), `prompt_patterns` (7 templates).
- 1 outil : `tools/gemini_wrapper.py` — résout `gemini.cmd`, timeout 120s, parse quota, **fallback automatique vers `multi-ia-router`** (Gemini 2.5 Flash via API key) si CLI absent ou quota épuisé. Log dans `~/.claude/logs/gemini-cli.log`.

**⚠️ HARD-GATES** :
1. JAMAIS stocker le token OAuth en clair (géré par `~/.config/gemini/` chiffré).
2. JAMAIS envoyer code sensible sans `gemini config set telemetry false`.
3. JAMAIS utiliser comme livrable final — skill utilitaire bas niveau, le PDF revient au skill parent.
4. TOUJOURS fallback gracieux vers multi-ia-router.
5. JAMAIS rotation de comptes (ban cascade Google).

**Cas d'usage où Gemini 3 Pro bat Claude Opus 4.6** :
- Screenshot TradingView → Pine Script (vision supérieure)
- Photo croquis → Mermaid/D2 (reconnaissance main levée)
- Maquette Figma → HTML/CSS (UI-first)
- Résumé long contexte (1M tokens natif)
- Fallback quand quotas Claude épuisés (1000 req/jour gratuit >> quota Claude)

**Cas où rester sur Claude** : refactor complexe, debug stack trace, Pine Script from scratch (connaissance fine des limites TV), analyse financière fondamentale.

**Chaînage** : invoqué par `deep-research`, `idea-to-diagram`, `multi-ia-router`, ou direct utilisateur. **Aucun livrable PDF propre** — retour JSON au skill appelant.

**Prérequis vérification** :
```bash
node --version                                    # >= 18 ✅ (déjà installé)
npm install -g @google/gemini-cli                 # à faire une fois
gemini                                            # OAuth dans navigateur
gemini config set telemetry false                 # opt-out
python tools/gemini_wrapper.py --prompt "test"    # smoke test
```

**Intégrations optionnelles à venir** :
- `multi-ia-router` : ajouter `gemini-cli` comme provider gratuit prioritaire (avant la clé API Gemini Flash)
- `idea-to-diagram` : brancher Gemini comme moteur vision image→structure
- `deep-research` : noter dans la matrice d'allocation

**Sources** :
- https://github.com/google-gemini/gemini-cli
- https://developers.google.com/gemini-code-assist/docs/gemini-cli
- https://ai.google.dev/gemini-api/docs/quota
