# ⚠️ BAN WAVE Google Antigravity — Ce qu'il NE FAUT JAMAIS faire

## Contexte

En **février 2026**, Google a mené une **vague de bans massifs** sur les comptes utilisant des outils tiers qui ré-exposaient Antigravity à l'extérieur (principalement via des proxies OpenAI-compatible).

**Cible principale** : `OpenClaw` (outil qui transformait Antigravity en backend pour d'autres IDE).
**Résultat** : comptes Google bannis sans préavis ni appel. Le créateur d'OpenClaw a abandonné et rejoint OpenAI.
**Raison officielle Google** : *"usage of Antigravity servers to power a non-Antigravity product"*.

## Liste NOIRE absolue

**JAMAIS installer, utiliser, ou recommander** :

| Outil | GitHub | Statut |
|-------|--------|--------|
| `openclaw` | retiré | BANNI, creator parti chez OpenAI |
| `antigravity-claude-proxy` | badrisnarayanan/antigravity-claude-proxy | Risque ban |
| `antigravity-cli` | krmslmz/antigravity-cli | Risque ban |
| `antigravity-proxy` | frieser/antigravity-proxy | Risque ban |

**Règle générale** : tout outil qui **expose un endpoint OpenAI-compatible pointant vers Antigravity** est interdit ToS.

## Ce qui est AUTORISÉ

✅ Utiliser Antigravity **comme IDE de bureau normal** (ouvrir l'app, coder dedans, parler à l'agent Manager).
✅ **Brancher des MCP servers dans Antigravity** (sens Claude → Antigravity, ce que fait ce skill).
✅ Sélectionner Claude Opus 4.6 **via le menu natif d'Antigravity** (pas via un proxy).
✅ Copier-coller manuellement du code entre Claude Code et Antigravity.

## Ce qui est INTERDIT

❌ Installer un proxy qui fait passer Antigravity pour une API OpenAI.
❌ Utiliser un script Python qui scrape l'UI Antigravity pour récupérer les réponses.
❌ Automatiser des milliers de requêtes via un compte free tier.
❌ Partager le compte Google avec d'autres personnes.
❌ Contourner les quotas par rotation de comptes.

## Que faire si on soupçonne un ban ?

1. Vérifier la connexion Antigravity : si erreur auth → probablement banni.
2. Consulter le compte Google : https://myaccount.google.com → Security → Recent activity.
3. Si banni : formulaire d'appel https://antigravity.google/support (whitelist possible au cas par cas selon GitHub issues, pas garanti).
4. **Ne PAS créer un deuxième compte** → ban en cascade possible.

## Sources

- https://venturebeat.com/orchestration/google-clamps-down-on-antigravity-malicious-usage-cutting-off-openclaw-users
- https://github.com/badrisnarayanan/antigravity-claude-proxy/issues/277
- https://antigravity.google/terms
