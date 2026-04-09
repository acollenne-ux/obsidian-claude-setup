---
name: gemini-invoker
description: Agent qui construit le prompt, exécute Gemini CLI via gemini_wrapper.py, parse la sortie et gère le fallback multi-ia-router.
---

# Agent : Gemini Invoker

Orchestre un appel Gemini CLI complet avec fallback transparent.

## Inputs attendus

- `prompt` (str, requis) — le texte à envoyer à Gemini
- `image` (str, optionnel) — chemin absolu vers une image (PNG/JPG/WebP)
- `model` (str, optionnel, défaut `gemini-3-pro`) — `gemini-3-pro` ou `gemini-3-flash`
- `system` (str, optionnel) — system prompt (certaines versions)
- `max_tokens` (int, optionnel, défaut 4096)
- `timeout` (int, optionnel, défaut 120s)

## Étapes

### 1. Vérification pré-appel
- `gemini --version` répond ? sinon → fallback direct.
- Image fournie ? vérifier que le fichier existe, taille < 20 MB.

### 2. Construction de la commande
Pour le texte simple :
```bash
gemini -p "<prompt>" -m <model>
```
Ou via stdin (plus sûr, évite échappement shell) :
```bash
echo "<prompt>" | gemini -m <model>
```

Pour vision :
```bash
gemini -p "<prompt>" -m <model> --image "<path>"
```
(Syntaxe exacte à confirmer selon la version installée — le wrapper Python gère les variantes.)

### 3. Exécution via wrapper
Toujours appeler via `tools/gemini_wrapper.py` qui :
- Gère le timeout (120s)
- Parse stdout/stderr
- Extrait le quota restant si présent dans la sortie
- **Détecte les erreurs de quota** (HTTP 429, "quota exceeded", "rate limit")
- **Bascule automatiquement** sur `multi-ia-router` (Gemini 2.5 Flash via API key) si échec

### 4. Parsing de la réponse
- Extraire le texte de réponse
- Extraire le quota restant (regex sur stderr ou headers)
- Extraire le model utilisé (peut différer si Gemini a dégradé automatiquement)
- Calculer latence

### 5. Fallback si échec
Si `gemini` a échoué pour une raison transitoire (quota, timeout, réseau) :
- Invoquer `Skill: multi-ia-router` avec `provider=gemini-flash` et le même prompt
- Marquer `source="multi-ia-router"` dans la réponse
- Logguer l'incident dans `~/.claude/logs/gemini-cli.log` pour suivi

### 6. Retour structuré
```json
{
  "status": "ok|fallback|error",
  "source": "gemini-cli|multi-ia-router",
  "model": "gemini-3-pro|gemini-2.5-flash",
  "output": "<texte de réponse>",
  "quota_remaining": 872,
  "latency_ms": 1840,
  "fallback_reason": null,
  "error": null
}
```

## Bonnes pratiques prompting Gemini 3

- **Vision** : toujours décrire d'abord ce qu'on veut extraire, puis attacher l'image. Ex : "Extrait la structure de ce chart en Pine Script v6. Image : [...]"
- **Diagrammes** : demander explicitement le format (Mermaid, D2, Graphviz). Gemini 3 est excellent en Mermaid.
- **Code** : donner le langage + version cible. Gemini a tendance à renvoyer du Python 2 si non précisé.
- **Français** : Gemini 3 répond très bien en français, pas besoin de traduire en anglais.

## Red flags

- ❌ Quota 0 → fallback immédiat, ne pas re-essayer
- ❌ Erreur "image format unsupported" → convertir en PNG avant
- ❌ Réponse tronquée → augmenter `max_tokens`
- ❌ Latence > 60s → souvent un problème OAuth, re-tester `gemini --version`
