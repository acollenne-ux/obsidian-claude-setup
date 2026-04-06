# Règles de Design — Flyer Creator Pro

## 1. Formats et résolutions

### Dimensions standards
| Format | mm | px (300 DPI) | px (150 DPI) | Usage |
|--------|-----|-------------|-------------|-------|
| A4 Portrait | 210×297 | 2480×3508 | 1240×1754 | Standard imprimerie |
| A5 Portrait | 148×210 | 1748×2480 | 874×1240 | Compact, distribution |
| Carré | 210×210 | 2480×2480 | 1240×1240 | Réseaux sociaux |
| US Letter | 216×279 | 2551×3295 | 1276×1648 | Amérique du Nord |
| Instagram | 108×108mm | 1080×1080 | 1080×1080 | Posts Instagram |
| Story | 108×192mm | 1080×1920 | 1080×1920 | Stories Instagram |

### Marges de sécurité (print)
- Fond perdu (bleed) : 3mm / 35px à 300 DPI sur chaque côté
- Marge de sécurité : 5mm / 59px minimum depuis le bord
- Zone de texte sûre : 10mm / 118px depuis le bord

## 2. Structure des 6 zones

### Zone 1 — Header (15-20% de la hauteur)
- Titre principal en police display
- Sous-titre optionnel
- Peut contenir un logo organisateur (coin supérieur)

### Zone 2 — Visuel principal (20-30% de la hauteur)
- Image de fond ou photo d'accroche
- Overlay sombre (40-60% opacité) si texte par-dessus
- Peut fusionner avec Zone 1 pour un impact maximal

### Zone 3 — Programme / Contenu (20-30% de la hauteur)
- Informations détaillées structurées
- Horaires en grille ou liste
- Peut être en colonnes (2-3 max)

### Zone 4 — Intervenants / Personnes (10-15% de la hauteur)
- Photos circulaires en rangée
- Noms + titres en dessous
- 3-6 personnes maximum par rangée

### Zone 5 — Infos pratiques (10-15% de la hauteur)
- Date, heure, lieu avec icônes
- Téléphone, email, site web
- QR code (coin droit)

### Zone 6 — Sponsors (5-10% de la hauteur)
- Bandeau horizontal en bas
- Logos de taille homogène
- Fond contrasté (blanc ou très sombre)
- Texte "Avec le soutien de" ou "Nos partenaires" en 10pt

## 3. Traitement des images

### Image de fond
```css
/* Overlay sombre pour lisibilité */
.background-overlay {
    background: linear-gradient(
        180deg,
        rgba(0,0,0,0.7) 0%,    /* Plus sombre en haut (titre) */
        rgba(0,0,0,0.3) 50%,    /* Plus clair au milieu */
        rgba(0,0,0,0.8) 100%    /* Plus sombre en bas (texte) */
    );
}
```

### Photos de personnes
```css
.person-photo {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
```

### Logos sponsors
```css
.sponsor-logo {
    height: 45px;
    width: auto;
    object-fit: contain;
    filter: brightness(0) invert(1); /* Version blanche si fond sombre */
    opacity: 0.8;
}
```

## 4. Icônes pour contacts

Utiliser des icônes SVG inline pour les informations de contact :
- Téléphone : icône phone/call
- Email : icône envelope/mail
- Lieu : icône map-pin/location
- Date : icône calendar
- Heure : icône clock
- Web : icône globe/link

Les icônes sont disponibles dans `assets/icons/` en SVG.
Si non disponibles, utiliser des emoji Unicode : 📞 📧 📍 📅 🕐 🌐

## 5. Espacement et rythme

| Élément | Espacement minimum |
|---------|-------------------|
| Entre zones | 24px |
| Entre titre et sous-titre | 12px |
| Entre items de programme | 8px |
| Entre photos de personnes | 16px |
| Marge latérale | 40px |
| Marge haute/basse | 40px |
| Padding interne des blocs | 20px |
| Gap entre logos sponsors | 24px |

## 6. Effets visuels CSS recommandés

### Gradient d'ambiance
```css
background: linear-gradient(135deg, var(--dominant) 0%, var(--secondary) 100%);
```

### Ombre sur les cartes/blocs
```css
box-shadow: 0 8px 32px rgba(0,0,0,0.15);
```

### Flou sur image de fond
```css
filter: blur(3px);
```

### Effet de verre (glassmorphism)
```css
background: rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
border: 1px solid rgba(255,255,255,0.2);
```

### Texte avec ombre pour lisibilité
```css
text-shadow: 0 2px 8px rgba(0,0,0,0.5);
```
