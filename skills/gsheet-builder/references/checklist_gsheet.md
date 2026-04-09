# QA Checklist — Google Sheets (15 criteres, /100, seuil 85)

## Grille de scoring

| # | Critere | Max | 0 pts | Moitie | Max pts |
|---|---------|-----|-------|--------|---------|
| 1 | Frozen headers | 10 | Aucun tab avec freeze | Certains tabs | Tous les tabs data ont row 1 frozen |
| 2 | Alignement | 10 | Aleatoire | Partiellement correct | text LEFT, num RIGHT, date CENTER partout |
| 3 | Bordures minimal | 8 | All-borders grille | Bordures excessives mais pas grille | Zero verticales, header bottom + thin rows |
| 4 | Couleurs <=6 | 8 | >10 couleurs | 7-8 couleurs | <=6, toutes du theme |
| 5 | Formats nombres | 8 | Aucun format | Partiellement | Devises $, %, dates tous formates |
| 6 | Font consistante | 6 | Mix de fonts | 2 fonts | 1 seule famille (Inter ou Arial) |
| 7 | Formules OK | 10 | >3 erreurs #REF etc | 1-2 erreurs | Zero erreur visible |
| 8 | Validation donnees | 6 | Aucune | Quelques dropdowns | Dropdowns + contraintes ou applicable |
| 9 | Organisation tabs | 6 | Desordonne, pas de couleurs | Ordre OK mais pas colore | Dashboard 1er, Config dernier, tabs colores |
| 10 | Cond. formatting | 6 | Aucun | Basique (1 regle) | Traffic lights + gradients sur KPIs |
| 11 | Charts qualite | 6 | Charts sans titre | Titres mais pas axes | Titres + axes + theme + max 4 |
| 12 | Config sheet | 4 | Absent | Existe mais incomplet | Existe avec params references par formules |
| 13 | Cross-refs | 4 | Refs brutes partout | Quelques named ranges | Named ranges systematiques |
| 14 | Print-ready | 4 | Debordement horizontal | Largeurs OK mais pas optimal | Colonnes bien dimensionnees, lisible A4 |
| 15 | Professionnalisme | 4 | Typos, terminologie mixte | Quelques inconsistances | Zero typo, terminologie coherente |

**TOTAL : 100 points**

## Seuils

| Score | Verdict | Action |
|-------|---------|--------|
| >= 85 | **GO** | Proceder a la livraison (Phase 8) |
| 70-84 | **ITERATE** | Corriger les criteres defaillants, retour Phase 5 (max 2x) |
| < 70 | **ESCALATE** | Afficher problemes a l'utilisateur, demander guidance |

## Verification programmatique

### Etape 1 : Metadata
```
sheets_get_metadata → verifier :
  - frozenRowCount >= 1 sur chaque tab (critere 1)
  - Nombre de tabs, noms, couleurs (critere 9)
  - Charts presents avec titres (critere 11)
```

### Etape 2 : Echantillonnage donnees
```
sheets_get_values sur :
  - Row 1 de chaque tab (headers)
  - Rows 2-6 (premieres donnees, verifier types)
  - Plages formules (verifier 0 erreurs #REF etc)
  - Config sheet complet
```

### Etape 3 : Evaluation criteres
Attribuer score par critere selon la grille ci-dessus.

### Etape 4 : Rapport
Generer le rapport QA au format standard (voir reviewer.md).
