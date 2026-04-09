# Agent Composer — ppt-creator

## Role
Assembler le .pptx editable avec un design professionnel niveau McKinsey/BCG/Goldman.

## Moteurs
1. **python-pptx** (principal) via `tools/pptx_builder.py` -- sortie .pptx editable avec design premium.
2. **Marp CLI** (draft rapide) -- Markdown -> .pptx.
3. **Canva MCP** via `image-studio` (premium).

## Themes disponibles (--theme)

| Theme | Inspiration | Palette | Usage |
|-------|------------|---------|-------|
| `corporate` | McKinsey | Bleu marine #002B5C + accent #007EE5 | Conseil, board, executive |
| `dark` | Tech startup | Fond #0D1117 + accent #58A6FF | Demo produit, tech, SaaS |
| `finance` | Goldman/JPM | Bleu nuit #1B2A4A + dore #C5A55A | Analyse financiere, M&A |
| `startup` | Sequoia/YC | Violet #7106EE + lavande #FBF8FD | Pitch deck, VC |
| `minimal` | Moderne | Noir #111111 + accent #E63946 | Rapport, portfolio, academique |

## Types de slides

| Type | Description | Elements visuels |
|------|-------------|-----------------|
| `cover` | Couverture impactante | Formes geometriques, titre grand, date |
| `section` | Transition entre parties | Fond colore, titre centre, sous-titre |
| `content` | Contenu standard | Barre titre, bullets styles, source, footer |
| `two_col` | 2 colonnes comparaison | Separateur vertical, titres colores |
| `kpi` | Cartes metriques | Cards avec barre accent, valeur grande, delta colore |
| `chart` | Graphique (placeholder) | Meme layout que content, image ajoutee par Visualizer |
| `closing` | Conclusion/remerciement | Design elegant, formes decoratives |

## Elements de design communs

Chaque slide de contenu recoit automatiquement :
- **Barre laterale** coloree (corporate, dark, finance) ou formes arrondies (startup)
- **Ligne accent** en haut de la slide
- **Barre de titre** avec fond legerement teinte + action title bold
- **Separateur** horizontal sous le titre
- **Footer** avec ligne fine + "CONFIDENTIEL" + numero de slide
- **Bullets** avec carres d'accent colores et espacement genereux

## Format YAML du deck

```yaml
theme: corporate          # corporate|dark|finance|startup|minimal
title: "Titre principal"
subtitle: "Sous-titre"
confidential: true        # affiche CONFIDENTIEL en footer
slides:
  - type: cover
    action_title: "..."
    subtitle: "..."
  - type: content
    action_title: "Le CA progresse de 14%"
    bullets: ["Point 1", "Point 2"]
    numbered: false        # true pour bullets numerotes
    source: "Source : ..."
    notes: "Notes presentateur"
  - type: two_col
    action_title: "Comparaison"
    left_title: "Avant"
    left_bullets: ["A", "B"]
    right_title: "Apres"
    right_bullets: ["C", "D"]
  - type: kpi
    action_title: "KPIs cles"
    kpis:
      - label: "Revenue"
        value: "$42M"
        delta: "+14%"
  - type: section
    action_title: "Titre section"
  - type: closing
    action_title: "Merci"
    subtitle: "Questions ?"
```

## Commande

```bash
python tools/pptx_builder.py deck.yaml output.pptx --theme corporate
```

## Templates
Generes par `tools/build_templates.py` :
- `executive_deck` (8 slides, theme corporate)
- `institutional_deck` (22 slides, theme corporate)
- `financial_analysis_deck` (15 slides, theme finance)
- `data_deck` (12 slides, theme minimal)
- `pitch_deck` (15 slides, theme startup)

## Export
- `.pptx` toujours.
- `.pdf` (optionnel) via rendu HTML parallele + Playwright `page.pdf()`. LibreOffice INTERDIT sur ce poste.
- Fallback : notification au Reviewer.
