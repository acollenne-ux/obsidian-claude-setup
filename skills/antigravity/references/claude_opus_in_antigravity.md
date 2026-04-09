# Sélectionner Claude Opus 4.6 dans Antigravity

## Pourquoi ?

Antigravity charge **Gemini 3.1 Pro** par défaut. Pour bénéficier de Claude Opus 4.6 (meilleur raisonnement code, aligné sur ce qu'Alexandre utilise dans Claude Code), il faut basculer manuellement.

**C'est gratuit et natif** — aucun proxy nécessaire.

## Procédure

### Option A : depuis le Global Settings
1. Ouvrir Antigravity.
2. Barre de titre → ⚙️ Settings (ou `Ctrl+,`).
3. Section **Model** → dropdown "Primary model".
4. Sélectionner **Claude Opus 4.6** (ou `claude-opus-4-6`).
5. Confirmer.
6. Optionnel : définir Gemini 3.1 Pro comme fallback (si quota Opus épuisé).

### Option B : par conversation
1. Ouvrir un chat Manager ou Editor.
2. En haut du chat, il y a un sélecteur de modèle (icône robot).
3. Cliquer → choisir Claude Opus 4.6.
4. Ce choix ne s'applique qu'à la conversation en cours.

### Option C : par agent (Manager view)
1. Manager view → bouton "New Agent".
2. Configuration agent → Model → Claude Opus 4.6.
3. Sauvegarder comme template.

## Vérification

Envoyer le prompt :
> "Quel modèle es-tu exactement ? Réponds avec ton model ID."

Réponse attendue : mention de `claude-opus-4-6` ou `Claude Opus 4.6` par Anthropic.

Si la réponse mentionne Gemini → le switch a échoué, recommencer.

## Quand Opus est-il épuisé ?

Si Antigravity affiche une bannière type *"Opus quota reached, fallback to Gemini 3"* :
- Soit attendre le refresh hebdomadaire.
- Soit utiliser **Claude Sonnet 4.5** (également inclus, quota séparé).
- **Ne PAS upgrader vers Pro** — Alexandre ne veut pas payer.

## Comparaison rapide des modèles disponibles

| Modèle | Force | Quand l'utiliser dans Antigravity |
|--------|-------|-----------------------------------|
| Gemini 3.1 Pro | UI, visuel, rapidité | Prototypage front, screenshots→code |
| **Claude Opus 4.6** | **Raisonnement code, refactor** | **Défaut Alexandre** |
| Claude Sonnet 4.5 | Équilibre vitesse/qualité | Fallback si Opus épuisé |
| GPT-OSS-120B | Open-source curiosité | Tests comparatifs uniquement |
