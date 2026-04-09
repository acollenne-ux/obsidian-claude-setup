---
name: Deep-research règles v3 (2026-04-08)
description: Règles strictes pour l'orchestrateur deep-research — pas de LITE, choix user STANDARD/FULL, multi-skills par couche, aller-retours L3↔L2
type: feedback
---

Règles imposées par Alexandre le 2026-04-08 pour le skill `deep-research` (appliquées dans `~/.claude/skills/deep-research/SKILL.md`) :

1. **Mode LITE SUPPRIMÉ définitivement.** Ne jamais le proposer ni l'utiliser. Seuls STANDARD et FULL existent.

2. **Choix utilisateur obligatoire avant exécution.** Après l'Agent 1 (Contexte) et l'Agent 2 (Benchmark Pro), deep-research doit présenter un cadrage court + recommandation et demander : "STANDARD ou FULL ?". Attendre la réponse avant Phase 3. Exception : si l'utilisateur l'a explicitement écrit dans son message.

3. **Multiplicité par couche.** Chaque ligne de l'arborescence 7 couches (L0→L6) peut et doit invoquer PLUSIEURS skills simultanément quand le contexte le justifie. Exemple L3 : `financial-analysis-framework` + `stock-analysis` + `macro-analysis` en parallèle.

4. **Aller-retours L3 ↔ L2 obligatoires.** La recherche (L2) n'est JAMAIS lancée à l'aveugle. Séquence :
   - L1 brainstorming → intention
   - L3 spécialistes (1er passage cadrage) → définissent les questions/données/sources à chercher
   - L2 recherche ciblée → exécute
   - L3 spécialistes (2e passage analyse) → consomment ; si lacunes, relancent L2
   - Autant de boucles que nécessaire avant L4
   C'est tout l'intérêt du brainstorming : cadrer avant de chercher.

**Why:** Alexandre veut maîtriser la profondeur (pas de mode dégradé auto), que le pipeline soit pleinement exploité (plusieurs skills en parallèle), et que la recherche soit pilotée par les experts-métier et non générique.

**How to apply:** À chaque invocation de deep-research, respecter ces 4 règles sans exception. Toute violation = à corriger immédiatement.
