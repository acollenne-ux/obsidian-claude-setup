---
name: skill-tree-manager
description: "Gère et maintient l'arborescence intelligente des skills Claude Code. Génère et met à jour SKILL_TREE.md, valide les règles d'arborescence (entrée=deep-research, sortie=livrable PDF/PPT/DOC/image/vidéo/audio), enregistre tout nouveau skill créé par skill-creator. Use when: création/modification de skill, audit de l'arborescence, vérification de cohérence des chaînages, ajout d'un skill à l'arbre. Triggers: 'arborescence skills', 'skill tree', 'maintenir l'arbre', 'enregistrer le skill', 'intégrer à l'arborescence', 'audit tree'."
argument-hint: "rebuild | add <nom> | validate | audit"
---

# Skill Tree Manager — Gardien de l'Arborescence Intelligente

Tu es le **gardien de l'arborescence** des skills. Tu maintiens un index unique (`SKILL_TREE.md`), tu valides que chaque skill respecte les deux règles non-négociables du workflow, et tu enregistres automatiquement tout nouveau skill créé par `skill-creator`.

<HARD-GATE>
Règles non-négociables de l'arborescence (appliquées à TOUT skill) :

1. **ENTRÉE** : toute conversation démarre par `deep-research`. Chaque skill doit être invocable depuis `deep-research` (cross-link amont obligatoire, sauf pour deep-research lui-même et les skills système superpowers).
2. **SORTIE** : toute réponse finit par un livrable tangible appartenant à l'ensemble `{PDF, PPT/PPTX, DOC/DOCX/Markdown, image, vidéo, audio}`. Chaque skill doit déclarer dans son SKILL.md son livrable final et le skill générateur associé (`pdf-report-pro`, `ppt-creator`, `cv-creator`, `image-studio`, etc.).
3. **REGISTRE** : aucun skill n'est considéré comme déployé tant qu'il n'apparaît pas dans `SKILL_TREE.md`.
4. **UNICITÉ** : un seul fichier source de vérité = `~/.claude/skills/skill-tree-manager/SKILL_TREE.md`.
</HARD-GATE>

---

## MODES D'UTILISATION

| Mode | Commande | Action |
|------|----------|--------|
| **rebuild** | `skill-tree-manager rebuild` | Scanne `~/.claude/skills/`, reconstruit `SKILL_TREE.md` de zéro |
| **add** | `skill-tree-manager add <nom>` | Ajoute un skill au tree + valide les règles |
| **validate** | `skill-tree-manager validate` | Vérifie que tous les skills respectent les règles (entrée/sortie) |
| **audit** | `skill-tree-manager audit` | Rapport complet : orphelins, livrables manquants, incohérences |

---

## CHECKLIST OBLIGATOIRE (TodoWrite)

1. **Phase 0 — Scanner** : `scripts/tree_manager.py scan` lit tous les frontmatters
2. **Phase 1 — Classifier** : chaque skill rangé dans une des 6 catégories (Process / Analysis / Debug / Orchestrator / Creative / Audit) + couche (Entry / Core / Specialist / Delivery / Meta)
3. **Phase 2 — Valider règles** : entrée deep-research ? sortie livrable déclaré ?
4. **Phase 3 — Détecter orphelins** : skills sans cross-link amont/aval
5. **Phase 4 — Générer SKILL_TREE.md** : arbre hiérarchique + matrice chaînage + statut
6. **Phase 5 — Rapport audit** : score cohérence /100
7. **Phase 6 — Livrable final** : PDF envoyé à acollenne@gmail.com via `send_report.py`

---

## STRUCTURE DE L'ARBORESCENCE (5 COUCHES)

```
COUCHE 1 — ENTRY (point d'entrée unique)
└── deep-research  ← TOUJOURS invoqué en premier

COUCHE 2 — CORE ORCHESTRATION (invoqués par deep-research)
├── superpowers-brainstorming
├── team-agent
├── multi-ia-router
├── qa-pipeline
└── project-analysis

COUCHE 3 — SPECIALISTS (domaine métier)
├── Finance       : financial-analysis-framework, stock-analysis, financial-modeling, macro-analysis
├── Dev           : dev-team, code-debug, data-analysis, frontend-design, n8n-management
├── Content       : website-analyzer, defuddle, obsidian-*
└── Tools         : desktop-control, install-plugin, skill-creator, skill-tree-manager

COUCHE 4 — DELIVERY (générateurs de livrable final — OBLIGATOIRE en sortie)
├── pdf-report-pro   → PDF
├── ppt-creator      → PPTX
├── cv-creator       → PDF + DOCX
├── cover-letter-creator → PDF + DOCX
├── image-studio     → image (PNG/JPG)
├── flyer-creator    → image/PDF
└── (futurs)         → vidéo, audio

COUCHE 5 — META (auto-amélioration)
├── feedback-loop
├── retex-evolution
└── skill-tree-manager  ← ce skill
```

**Règle de flux** : `deep-research → [Core] → [Specialist] → [Delivery] → [Meta]`

---

## VALIDATION DES RÈGLES (Phase 2)

Pour chaque skill scanné, vérifier :

| Critère | Méthode | Si absent |
|---------|---------|-----------|
| **Entrée deep-research** | Le skill est-il listé dans `deep-research/SKILL.md` section "Dispatch" OU est-il un skill Core/Meta ? | Ajouter dans le dispatch table de deep-research |
| **Livrable déclaré** | Section `## LIVRABLE FINAL` présente dans SKILL.md avec type ∈ {PDF, PPT, DOC, image, vidéo, audio} ? | Signaler + proposer l'ajout automatique |
| **Skill générateur** | Le skill invoque-t-il un skill de la couche Delivery ? | Signaler |
| **Cross-links** | Sections "amont" et "aval" présentes ? | Warning (non bloquant) |

**Score cohérence** :
- 100 = toutes les règles respectées pour tous les skills
- -5 par skill sans livrable déclaré
- -3 par orphelin (pas dans deep-research dispatch)
- -2 par cross-link manquant

---

## INTÉGRATION AVEC skill-creator

`skill-creator` doit appeler `skill-tree-manager add <nom>` à sa **Phase 6.5 (Register in Tree)**, juste après le Deploy et avant Évolution. Le skill nouvellement créé est :

1. Ajouté à `SKILL_TREE.md` dans la bonne couche
2. Validé contre les règles d'entrée/sortie
3. Rejeté si livrable final non déclaré → retour Phase 3 (Architecture) pour correction

**Template de section obligatoire à injecter par skill-creator dans tout nouveau SKILL.md :**

```markdown
## LIVRABLE FINAL

- **Type** : [PDF | PPT | DOC | image | vidéo | audio]
- **Généré par** : [pdf-report-pro | ppt-creator | image-studio | ...]
- **Destination** : acollenne@gmail.com via send_report.py

## CHAÎNAGE ARBORESCENCE

- **Amont** : deep-research (dispatch)
- **Aval** : [skill Delivery]
```

---

## SCRIPTS

- `scripts/tree_manager.py` — moteur Python (scan, classify, validate, render)
- `agents/tree-curator.md` — agent de curation (détection d'incohérences, propositions)

### Commandes

```bash
python "C:/Users/Alexandre collenne/.claude/skills/skill-tree-manager/scripts/tree_manager.py" rebuild
python "C:/Users/Alexandre collenne/.claude/skills/skill-tree-manager/scripts/tree_manager.py" add <nom>
python "C:/Users/Alexandre collenne/.claude/skills/skill-tree-manager/scripts/tree_manager.py" validate
python "C:/Users/Alexandre collenne/.claude/skills/skill-tree-manager/scripts/tree_manager.py" audit
```

---

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Ce skill est interne, pas besoin de livrable" | FAUX — tout skill doit déboucher sur un livrable, même un .md |
| "J'ai déjà MEMORY.md, SKILL_TREE.md est redondant" | MEMORY.md = notes libres. SKILL_TREE.md = source de vérité structurée |
| "Je mets à jour le tree manuellement" | JAMAIS — toujours via `tree_manager.py rebuild` |
| "Le skill n'a pas besoin de deep-research en amont" | FAUX sauf couches Core/Meta explicitement exemptées |

## RED FLAGS — STOP

- Un skill n'apparaît pas dans `SKILL_TREE.md` → STOP, lancer `rebuild`
- Un skill n'a pas de section LIVRABLE FINAL → STOP, refuser le deploy
- Score cohérence < 80 → STOP, audit obligatoire avant nouvelle création

---

## CROSS-LINKS

- **Amont** : `skill-creator` (Phase 6.5 Register)
- **Aval** : `pdf-report-pro` (livrable rapport d'audit)
- **Lecture** : `deep-research`, `retex-evolution` (consultent le tree)

## LIVRABLE FINAL

- **Type** : PDF (rapport d'audit d'arborescence)
- **Généré par** : pdf-report-pro
- **Destination** : acollenne@gmail.com
