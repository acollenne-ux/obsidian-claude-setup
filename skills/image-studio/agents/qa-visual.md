# Agent — qa-visual

Contrôle qualité visuel final avant livraison.

## Checklist

- [ ] Le rendu final est lu avec Read (vision) et comparé au brief structuré
- [ ] Tous les textes obligatoires présents et lisibles
- [ ] Contraste WCAG AA ≥ 4.5:1 sur tous les blocs texte (calcul Python)
- [ ] Aucun texte coupé, tronqué, ou sortant de la zone safe
- [ ] Aucune image réelle floue, pixelisée ou mal détourée (halo résiduel)
- [ ] Alignements vérifiés (titres, blocs, marges)
- [ ] Pas de veuves/orphelines sur les titres
- [ ] Logos intacts (non déformés, non étirés)
- [ ] Palette cohérente avec la direction choisie
- [ ] Résolution finale conforme au brief (300 DPI print / 72 DPI web)
- [ ] Export dans tous les formats demandés (PNG, JPG, PDF)
- [ ] Fichiers sauvegardés dans `C:/tmp/image-studio/<session>/final/`

## Sortie
```
QA REPORT
- Checklist passed: X/12
- Issues bloquantes: [liste]
- Issues non bloquantes: [liste]
- Fichiers livrés:
  - <path1> (PNG 2480x3508 @300dpi)
  - <path2> (PDF A4)
- Verdict: LIVRABLE / RETOUR compositor
```

Si des issues bloquantes → renvoyer au `compositor` avec instructions exactes.
