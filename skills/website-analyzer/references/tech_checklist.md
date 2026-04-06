# Checklist Technique — Infrastructure & Sécurité Web

## 1. Headers de sécurité HTTP (OWASP Standards 2025)

### Obligatoires (P1)
- [ ] `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- [ ] `Content-Security-Policy` — politique restrictive adaptée au site
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: DENY` ou `SAMEORIGIN`
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`

### Recommandés (P2)
- [ ] `Permissions-Policy` — restreindre caméra, micro, géolocalisation
- [ ] `Cross-Origin-Opener-Policy: same-origin`
- [ ] `Cross-Origin-Embedder-Policy: require-corp`
- [ ] `Cross-Origin-Resource-Policy: same-origin`

### À supprimer (information disclosure)
- [ ] Masquer `Server` (révèle Apache/nginx/version)
- [ ] Supprimer `X-Powered-By` (révèle PHP/Express/ASP.NET)

---

## 2. Cookies & Trackers

### Flags obligatoires sur cookies sensibles
- [ ] `Secure` — transmission uniquement en HTTPS
- [ ] `HttpOnly` — inaccessible au JavaScript
- [ ] `SameSite=Strict` ou `SameSite=Lax` — protection CSRF

### Conformité RGPD/ePrivacy
- [ ] Aucun tracker avant consentement explicite
- [ ] Bandeau cookies avec choix granulaire (accepter/refuser/paramétrer)
- [ ] Cookies analytiques = soumis au consentement (sauf Matomo exempté CNIL)
- [ ] Durée de vie cookies ≤ 13 mois (recommandation CNIL)
- [ ] Politique cookies accessible et exhaustive

---

## 3. Performance & Ressources

### Seuils de référence (Google 2025)
| Métrique | Bon | Moyen | Mauvais |
|----------|-----|-------|---------|
| LCP | < 2.5s | 2.5-4s | > 4s |
| INP | < 200ms | 200-500ms | > 500ms |
| CLS | < 0.1 | 0.1-0.25 | > 0.25 |
| TTFB | < 800ms | 800-1800ms | > 1800ms |
| Total page weight | < 1.5 MB | 1.5-3 MB | > 3 MB |
| HTTP requests | < 30 | 30-60 | > 60 |

### Optimisations requises
- [ ] Compression serveur (gzip ou brotli)
- [ ] Cache-Control avec max-age approprié (assets statiques ≥ 1 an)
- [ ] Images en formats modernes (WebP/AVIF)
- [ ] Lazy loading sur les images below the fold
- [ ] JS async/defer (pas de render-blocking)
- [ ] CSS critique inlined, reste en async
- [ ] Fonts en woff2 avec font-display: swap
- [ ] Code splitting / tree shaking sur le JS
- [ ] Preload des ressources critiques (LCP image, main font)

---

## 4. Configuration Technique

### robots.txt
- [ ] Présent à la racine du site
- [ ] Ne bloque pas les pages importantes (CSS, JS pour le rendu)
- [ ] Référence le sitemap.xml
- [ ] Bloque les pages admin/login/API

### sitemap.xml
- [ ] Présent à la racine
- [ ] À jour (toutes les pages indexables)
- [ ] Pas de pages 404/410 dans le sitemap
- [ ] Format XML valide
- [ ] Soumis à Google Search Console

### Données structurées (Schema.org)
- [ ] Organization sur la homepage
- [ ] BreadcrumbList sur les pages profondes
- [ ] Product sur les pages produits (e-commerce)
- [ ] Article sur les pages blog
- [ ] FAQ si page FAQ présente
- [ ] LocalBusiness si entreprise locale
- [ ] JSON-LD valide (tester avec Google Rich Results Test)

### HTTPS & SSL
- [ ] HTTPS forcé (redirection HTTP → HTTPS)
- [ ] Certificat valide (pas expiré, bon domaine)
- [ ] Pas de mixed content (ressources HTTP sur page HTTPS)
- [ ] TLS 1.2 minimum (TLS 1.3 recommandé)

---

## 5. Stack Technologique — Points d'attention

### CMS
| CMS | Points forts | Points faibles | Attention |
|-----|-------------|---------------|-----------|
| WordPress | Écosystème, SEO (Yoast) | Sécurité plugins, vitesse | Maintenir à jour |
| Shopify | E-commerce, sécurité | Personnalisation limitée, SEO | Liquid templates |
| Wix | Facilité | Performance, SEO, portabilité | Lock-in vendor |
| Webflow | Design, no-code | Coût, limitations dynamiques | Pricing scaling |
| Custom | Flexibilité totale | Maintenance, coût dev | Documentation ? |

### Frameworks JS
| Framework | SSR/SEO | Performance | Complexité |
|-----------|---------|-------------|------------|
| Next.js | Excellent (SSR/SSG) | Très bon | Moyen |
| Nuxt.js | Excellent (SSR/SSG) | Très bon | Moyen |
| React SPA | Mauvais (sans SSR) | Variable | Moyen |
| Vue SPA | Mauvais (sans SSR) | Variable | Faible |
| Angular | Moyen (SSR possible) | Lourd | Élevé |
| Vanilla/jQuery | Non applicable | Léger | Faible |

---

## 6. Domaines tiers courants et leur finalité

| Domaine | Finalité | Impact perf | Privacy |
|---------|----------|-------------|---------|
| google-analytics.com | Analytics | Moyen | Moyen |
| googletagmanager.com | Tag management | Moyen | Variable |
| connect.facebook.net | Tracking/Pixel | Élevé | Élevé |
| hotjar.com | Heatmaps/Session | Élevé | Élevé |
| cdn.shopify.com | CDN e-commerce | Faible | Faible |
| fonts.googleapis.com | Fonts | Moyen | Faible |
| cdn.jsdelivr.net | CDN libraries | Faible | Faible |
| crisp.chat | Chat support | Moyen | Moyen |
| intercom.io | Chat/CRM | Élevé | Moyen |
| sentry.io | Error tracking | Faible | Faible |
