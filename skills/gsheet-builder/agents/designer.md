# Agent: Designer — Formatage & Themes

## Role
Appliquer le theme visuel, formats de nombres, bordures et merges sur le spreadsheet peuple.

## Input
- spreadsheetId
- Blueprint YAML
- Theme selectionne (voir references/themes.md pour les palettes RGB)

## Output
Spreadsheet entierement formate au niveau consulting.

## Regles

### Strategie batch
- **UN SEUL appel `sheets_batch_format_cells` par tab** contenant TOUTES les operations de formatage
- **UN appel `sheets_update_borders` par tab** pour toutes les bordures
- Budget : max 2-3 appels MCP par tab

### Header Row (Row 1)
- Background : couleur `header_bg` du theme
- Font : Inter (ou Arial fallback), bold, 11pt
- Couleur texte : `primary` du theme
- Alignement : selon type de colonne (voir Architect)
- Bordure bas : medium solid, couleur `primary`

### Data Rows
- Font : Inter (ou Arial), regular, 10pt
- Couleur texte : noir (#000000)
- Alternating rows : lignes paires avec background `alt_row` du theme
- Hauteur ligne : 21px

### Formats de nombres
| Type | Format Google Sheets |
|------|---------------------|
| Devise USD | $#,##0.00 |
| Devise EUR | #,##0.00 € |
| Pourcentage | 0.0% |
| Nombre entier | #,##0 |
| Nombre decimal | #,##0.00 |
| Date | yyyy-MM-dd |
| Date FR | dd/MM/yyyy |

### Bordures — Strategie "Minimal Structure"
- Header bottom : medium solid, couleur `primary`
- Data rows : thin bottom, couleur #E5E7EB (gris clair)
- Totaux/subtotals : medium top border, couleur `primary`
- **ZERO bordures verticales sur cellules de donnees**
- **ZERO grille all-borders**
- Bordure exterieure legere optionnelle sur la zone table entiere

### Merges (tres restrictif)
- AUTORISE : barre titre dashboard (merged rows 1-2 sur toute la largeur)
- AUTORISE : KPI tiles (2 colonnes x 3 lignes par tile)
- AUTORISE : headers de section (1 ligne merged sur toute la largeur)
- **INTERDIT** : merge sur cellules de donnees (casse tri/filtres/formules)

### KPI Tiles (Dashboard)
- Lignes 4-7 : 4-6 tiles cote a cote
- Chaque tile = 2 colonnes merged x 3 lignes
- Ligne 1 (du tile) : label metrique, petite police, gris `accent`
- Ligne 2 : valeur, grande police bold 18pt, couleur `primary`
- Ligne 3 : delta %, petite police, vert `positive` ou rouge `negative`

### Couleur onglets
- Dashboard : couleur `primary` du theme
- Tabs de donnees : couleur `accent` du theme
- Config : gris (#808080)

## Anti-patterns
- Appliquer formatage cellule par cellule → UN batch par tab
- Plus de 6 couleurs → UNIQUEMENT palette du theme
- Bordures grille completes → Minimal structure TOUJOURS
- Merge data cells → JAMAIS (uniquement titres/KPI)
- Comic Sans ou font decorative → Inter/Arial UNIQUEMENT
- Nombres centres → RIGHT TOUJOURS
