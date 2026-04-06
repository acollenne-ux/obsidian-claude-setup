---
name: pdf-report-gen
description: "Génération de rapports PDF professionnels en Markdown strict. Use when: generating PDF reports, exporting analysis results, sending reports by email. Triggers: 'pdf', 'rapport', 'report', 'envoyer par email'."
---

# PDF Report Generator — Synthèse + PDF + Email

Transformer les données brutes en document professionnel, générer le PDF et l'envoyer.

---

## AGENT SYNTHÈSE (OBLIGATOIRE avant tout PDF)

Son rôle : transformer les données collectées en un document lisible, structuré et adapté.

### Règles de l'Agent Synthèse

1. **Ne pas répéter les données brutes** — interpréter, conclure
2. **Être exhaustif sur chaque dimension** — pas de dimension bâclée
3. **Donner une note /10 à chaque dimension** avec justification courte
4. **Terminer par une recommandation claire et actionnable**
5. **Adapter le niveau de détail** : plus de texte sur les dimensions critiques

### Adaptation au type de demande

| Type | PDFs à générer | Contenu |
|------|---------------|---------|
| **Code** | 2 PDFs séparés | 1) PDF CODE : code commenté, prêt à copier. 2) PDF GUIDE : explications, install, config, tests |
| **Analyse financière** | 1 PDF exhaustif | 15 dimensions + notes /10 + synthèse (forces, faiblesses, bull/base/bear, recommandation) |
| **Recherche générale** | 1 PDF structuré | Sections claires, faits sourcés, conclusion actionnable |
| **Macro** | 1 PDF structuré | Contexte, indicateurs, impacts marchés, positionnement recommandé |

---

## FORMAT MARKDOWN — RÈGLE CRITIQUE

**Le contenu DOIT être du Markdown pur. JAMAIS de HTML.**

| Interdit | Utiliser à la place |
|----------|-------------------|
| `<h1>`, `<h2>` | `#`, `##`, `###` |
| `<table>` | `\| col1 \| col2 \|` |
| `<b>`, `<strong>` | `**gras**` |
| `<div>`, `<span>` | Rien, Markdown simple |
| `<ul>`, `<li>` | `- item` |
| `<code>` | \`\`\` blocs de code |

- Les accents français sont supportés (peuvent être remplacés par ASCII pour fiabilité)
- Longueur max par cellule de tableau : 50 caractères

---

## MÉTHODE D'ENVOI — TOUJOURS --file

**NE JAMAIS passer le contenu directement en argument bash** (troncature shell).

### Étapes obligatoires :

1. **Écrire** le contenu Markdown dans un fichier temporaire (Write tool)
2. **Envoyer** via `--file` :
```bash
python "C:\Users\Alexandre collenne\.claude\tools\send_report.py" "Titre du rapport" --file "/chemin/vers/rapport.md" acollenne@gmail.com
```
3. **Supprimer** le fichier temporaire après envoi

### Pour du code (2 PDFs) :
```bash
python "C:\Users\Alexandre collenne\.claude\tools\send_report.py" "[Nom] - CODE" --file code.md acollenne@gmail.com
python "C:\Users\Alexandre collenne\.claude\tools\send_report.py" "[Nom] - GUIDE" --file guide.md acollenne@gmail.com
```

### Persistance des PDFs :
Après génération, **copier dans `/mnt/outputs/`** pour accessibilité depuis d'autres tâches :
```bash
cp /chemin/vers/rapport.pdf /mnt/outputs/Nom_Rapport.pdf
```

---

## GRAPHIQUES (si pertinents)

```bash
python "C:\Users\Alexandre collenne\.claude\tools\chart_generator.py" <type> <json> <titre> <output.png>
```

Types disponibles : `line`, `bar`, `area`, `multi_line`, `hbar`, `scatter`

Intégrer les graphiques dans le PDF si le format le permet.

---

## FORMAT DE SORTIE

```
PDF REPORT — [titre]

Type        : [Code 2 PDFs / Analyse 1 PDF / Recherche / Macro]
Format      : Markdown pur ✓
Méthode     : --file ✓
Envoyé à    : acollenne@gmail.com
Graphiques  : [N] générés
Persistance : copié dans /mnt/outputs/ ✓
```

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Un peu de HTML pour le styling" | JAMAIS de HTML dans les PDF. Markdown pur uniquement (bug confirmé 28/03/2026). |
| "Le contenu inline en bash suffit" | TOUJOURS utiliser `--file rapport.md`. Le contenu inline est tronqué. |
| "Le PDF peut attendre" | L'utilisateur veut TOUJOURS un PDF pour les analyses importantes. Envoyer immédiatement. |
| "Pas besoin de structure, c'est court" | Même un PDF court doit avoir : titre, sections, conclusion. Professionnel = structuré. |

## RED FLAGS — STOP

- HTML détecté dans le contenu → STOP, convertir en Markdown
- Contenu passé en inline (pas --file) → STOP, écrire dans un fichier d'abord
- PDF sans titre ni structure → STOP, restructurer

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Invoqué par | `deep-research` (Phase 4) |
| Après validation | `qa-pipeline` |
| Données financières | `financial-analysis-framework`, `stock-analysis` |
| Feedback après envoi | `feedback-loop` |
| RETEX | `retex-evolution` |

## ÉVOLUTION

Après chaque génération PDF :
- Si le PDF était mal formaté → identifier la cause (HTML, inline, encoding)
- Si l'email n'a pas été reçu → vérifier send_report.py
- Si le contenu était tronqué → vérifier la méthode --file

Seuils : si > 2 PDF mal formatés → revoir le pipeline complet.
