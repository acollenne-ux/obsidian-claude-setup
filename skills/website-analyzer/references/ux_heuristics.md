# Heuristiques UX — Référentiel d'analyse

## Les 10 heuristiques de Nielsen (adaptées au web 2026)

### 1. Visibilité du statut système
- L'utilisateur sait-il toujours où il en est ? (breadcrumbs, menu actif, indicateurs de progression)
- Les chargements sont-ils signalés ? (spinners, skeleton screens, barres de progression)
- Les actions sont-elles confirmées ? (messages de succès, feedback visuel)

### 2. Correspondance système / monde réel
- Le langage est-il celui des utilisateurs ? (pas de jargon technique)
- Les métaphores visuelles sont-elles compréhensibles ? (icônes universelles)
- L'organisation suit-elle la logique utilisateur ? (pas la logique interne de l'entreprise)

### 3. Contrôle et liberté utilisateur
- Peut-on annuler une action ? (retour arrière, annulation de commande)
- Les sorties sont-elles clairement indiquées ? (bouton fermer, lien retour)
- L'utilisateur n'est-il pas piégé ? (pas de pop-ups bloquants sans échappatoire)

### 4. Cohérence et standards
- Les éléments similaires se comportent-ils de la même façon ?
- Les conventions web sont-elles respectées ? (logo → accueil, panier en haut à droite)
- La terminologie est-elle cohérente ? (même mot pour le même concept)

### 5. Prévention des erreurs
- Les formulaires ont-ils des validations en temps réel ?
- Les actions destructives demandent-elles confirmation ?
- Les formats attendus sont-ils indiqués ? (date, téléphone, email)

### 6. Reconnaissance plutôt que mémorisation
- Les options sont-elles visibles ? (pas de fonctions cachées)
- L'historique de navigation est-il accessible ?
- Les filtres et la recherche aident-ils à retrouver l'information ?

### 7. Flexibilité et efficacité
- Les raccourcis existent-ils pour les utilisateurs avancés ?
- La recherche interne est-elle performante ?
- Les parcours sont-ils adaptés aux différents profils d'utilisateurs ?

### 8. Design esthétique et minimaliste
- Chaque élément sert-il un objectif ? (pas de décoration gratuite)
- L'information essentielle est-elle mise en avant ?
- Le ratio signal/bruit est-il bon ?

### 9. Aide à la reconnaissance et correction des erreurs
- Les messages d'erreur sont-ils clairs et constructifs ?
- L'erreur est-elle identifiée précisément ? (quel champ, quel problème)
- Une solution est-elle proposée ?

### 10. Aide et documentation
- Une FAQ ou aide est-elle accessible ?
- Les tooltips/infobulles expliquent-ils les fonctionnalités complexes ?
- Le support est-il facilement joignable ? (chat, téléphone, email)

---

## Bonnes pratiques visuelles 2024-2026

### Typographie
- Hiérarchie : H1 > H2 > H3 > body — ratios 2:1 ou golden ratio (1.618)
- Max 2-3 familles de polices (1 titres, 1 corps, 1 accent optionnel)
- Taille minimum body : 16px desktop, 16px mobile
- Line-height : 1.4-1.6 pour le body text
- Longueur de ligne : 50-75 caractères par ligne (idéal : 66)

### Couleurs
- Palette limitée : 1 primaire, 1 secondaire, 1 accent, + neutres
- Contraste WCAG AA : 4.5:1 texte normal, 3:1 grands textes (≥18px bold ou ≥24px)
- Pas plus de 5 couleurs principales + variations
- Couleurs sémantiques : vert=succès, rouge=erreur, jaune=warning, bleu=info

### Espacement
- Système de spacing cohérent (base 4px ou 8px)
- White space ≥ 30% de la surface visible
- Padding suffisant dans les boutons (min 12px vertical, 24px horizontal)
- Marges entre sections : ≥ 48px

### Images et médias
- Formats modernes : WebP, AVIF (fallback JPEG/PNG)
- Lazy loading pour les images sous la ligne de flottaison
- Ratio cohérent dans les grilles (16:9, 4:3, 1:1)
- Texte alternatif (alt) descriptif et pertinent

### Navigation
- Menu principal : max 7 items (±2, loi de Miller)
- Profondeur max : 3 niveaux de sous-menu
- Menu sticky/fixed sur mobile pour accès rapide
- Breadcrumbs sur les pages profondes (> 2 niveaux)
- Footer avec plan du site, contact, mentions légales

### Mobile
- Touch targets : minimum 44x44px (Apple HIG) ou 48x48px (Material Design)
- Espacement entre targets : minimum 8px
- Pas de hover-only interactions (pas de tooltip au survol uniquement)
- Boutons pleine largeur sur mobile pour les CTAs principaux
- Menu hamburger avec overlay ou slide-in

---

## Checklist rapide UX (éléments à vérifier)

- [ ] Page charge en < 3 secondes
- [ ] Proposition de valeur visible sans scroller
- [ ] Navigation principale claire (≤ 7 items)
- [ ] CTA principal visible au-dessus de la ligne de flottaison
- [ ] Formulaires courts (≤ 5 champs pour un lead)
- [ ] Messages d'erreur clairs et constructifs
- [ ] Site fonctionnel sur mobile
- [ ] Contraste texte suffisant (WCAG AA)
- [ ] Images avec alt text
- [ ] Liens descriptifs (pas de "cliquez ici")
- [ ] Page 404 personnalisée avec navigation
- [ ] Favicon présent
- [ ] HTTPS actif
