# Gemini CLI Free Tier — Limites connues (avril 2026)

## Ce qui est INCLUS gratuitement via OAuth perso

| Feature | Free tier CLI |
|---------|---------------|
| **Gemini 3 Pro** | ✅ ~1000 req/jour |
| Gemini 3 Flash | ✅ ~10 000 req/jour |
| Gemini 2.5 Pro | ✅ (fallback) |
| Vision (images) | ✅ |
| Contexte long (1M tokens) | ✅ |
| Tool use / function calling | ✅ |
| Streaming | ✅ (mode interactif seulement) |
| Carte bancaire exigée ? | ❌ Non |

## Quotas observés (mars 2026, communauté)

- **Gemini 3 Pro** : ~1000 requêtes/jour par compte Google perso
- **Refresh** : minuit UTC (01h00 / 02h00 heure française selon DST)
- **Comptage** : 1 requête = 1 appel API, peu importe la taille du contexte
- **Dégradation auto** : si Gemini 3 Pro est épuisé, bascule silencieuse sur Gemini 3 Flash (c'est pour ça que le wrapper log le model réellement utilisé)

## Restrictions

- ❌ **Comptes Google Workspace** : non supportés en free tier (Google force la clé API payante pour les comptes pro)
- ❌ **Rotation de comptes** : détecté par Google, ban en cascade
- ❌ **Automation massive** : si pattern bot détecté, Google impose un captcha puis bloque
- ❌ **Usage commercial redistribué** : interdit par ToS (comme Antigravity ban wave)

## Bonnes pratiques

- Utiliser un **compte Google dédié** (ex: `acollenne+gemini@gmail.com` via alias Gmail) pour isoler les quotas et limiter l'exposition télémétrie
- **Opt-out télémétrie** : `gemini config set telemetry false`
- **Logger le quota restant** après chaque appel → permet de switcher sur `multi-ia-router` quand on approche la limite
- **Re-tester les limites tous les 3 mois** — Google ajuste régulièrement les quotas free tier sans préavis

## Sources

- https://github.com/google-gemini/gemini-cli (repo officiel)
- https://developers.google.com/gemini-code-assist/docs/gemini-cli
- https://ai.google.dev/gemini-api/docs/quota
- Threads r/GoogleGeminiAI février-mars 2026
