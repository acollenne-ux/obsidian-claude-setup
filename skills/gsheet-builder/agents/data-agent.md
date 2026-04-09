# Agent: Data — Population & Formules

## Role
Peupler toutes les donnees, formules, dates et liens dans le spreadsheet cree en Phase 3.

## Input
- spreadsheetId (de Phase 3)
- Blueprint YAML (de Phase 1)
- Donnees sources (du brief ou des skills L3 upstream)

## Output
Spreadsheet peuple avec toutes les donnees, formules fonctionnelles, dates formatees, liens actifs.

## Regles

### Ordre de population
1. Headers (1 appel `sheets_batch_update_values` par tab)
2. Donnees statiques (1 appel `sheets_batch_update_values` par tab)
3. Config sheet (1 appel batch)
4. Formules (via `sheets_update_values` avec `valueInputOption: USER_ENTERED`)
5. Dates (via `sheets_insert_date` avec locale)
6. Liens (via `sheets_insert_link`)

### Batch obligatoire
- JAMAIS d'appel individuel pour < 10 cellules
- Grouper TOUTES les donnees d'un tab dans UN SEUL appel batch
- Budget : max 2-4 appels MCP par tab

### Formules
- TOUJOURS utiliser `valueInputOption: USER_ENTERED` pour que Google interprete les formules
- Formules autorisees : SUM, AVERAGE, COUNT, COUNTA, IF, VLOOKUP, INDEX/MATCH, ARRAYFORMULA
- References croisees : utiliser le format `='Tab Name'!A1` ou named ranges
- JAMAIS hardcoder une valeur qui devrait etre dans Config

### Formats de donnees
| Type | Format d'insertion | Exemple |
|------|-------------------|---------|
| Texte | String direct | "Apple Inc." |
| Nombre | Number sans format | 42.5 |
| Devise | Number (format applique en Phase 5) | 150.75 |
| Pourcentage | Decimal (0.15 pour 15%) | 0.15 |
| Date | Via sheets_insert_date | "2026-04-09" |
| Lien | Via sheets_insert_link | url + display text |
| Formule | String commençant par = | "=SUM(B2:B50)" |
| Booleen | TRUE/FALSE | TRUE |

### Validation
- Apres population, verifier via `sheets_get_values` sur 3-5 plages echantillon
- Confirmer : pas de cellules vides inattendues, formules resolues, types corrects

## Anti-patterns
- Appel sheets_update_values pour UNE cellule → BATCH obligatoire
- Formule avec valeur hardcodee (ex: =A2*0.2) → UTILISER =A2*Config!B3
- Oublier valueInputOption: USER_ENTERED pour formules → formule affichee en texte
- Donnees non typees (tout en string) → respecter les types natifs
