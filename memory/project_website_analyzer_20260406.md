---
name: Website Analyzer skill v2.0
description: Skill website-analyzer v2.0 — 5 agents (dont tech_infra scraping), 12 dimensions, scoring pondéré, rapport PDF
type: project
---

Skill `website-analyzer` v2.0 — mis à jour le 06/04/2026 avec agent de scraping technique.

**Architecture :** ~16 fichiers dans `~/.claude/skills/website-analyzer/`
- `SKILL.md` : workflow 8 étapes, 3 modes (A=360°, B=Marketing, C=Design)
- `agents/` : **5 agents** (ux_ui, marketing_seo, conversion, brand, **tech_infra**)
- `references/` : scoring_grid (**12 dimensions** + pondération), ux_heuristics, brand_checklist, **tech_checklist**
- `scripts/` : site_crawler.py (Playwright, **scraping technique approfondi**), report_builder.py
- `templates/` : audit_report_template.md (v2.0, 12 dimensions)

**Ajouts v2.0 (06/04/2026) — Agent Tech Infrastructure :**
- **Crawler enrichi** : 8 nouvelles fonctions d'extraction (detect_technologies, extract_resources_breakdown, extract_structured_data_details, extract_content_metrics, extract_security_headers, extract_cookies, extract_social_links, extract_contact_info) + collecte robots.txt et sitemap.xml
- **Agent tech_infra_agent.md** : analyse 5 sous-dimensions (Stack technique, Sécurité web, Ressources & Optimisation, Trackers & Vie privée, Configuration technique)
- **tech_checklist.md** : référentiel OWASP 2025, seuils Google 2025, checklist complète
- **12 dimensions** au lieu de 10 : +Sécurité & Infrastructure (9%), +Trackers & Vie privée (8%)
- **Détection technologique** : 11 CMS, 12 frameworks JS, 19 analytics/trackers, 10 CDN
- **Données collectées en plus** : HTTP security headers, resources breakdown (Performance API), structured data JSON-LD content, content metrics (word count, text-to-HTML ratio), cookies analysis, social links, contact info

**Intégration :** deep-research dispatch auto sur "audit web / analyse site / URL". Tech Infra agent activé en modes A (360°) et B (Marketing).

**Why:** Les 4 agents existants ne couvraient pas la couche technique invisible (sécurité, stack, trackers, cookies, resources). L'ajout comble cette lacune critique pour des audits de niveau professionnel.

**How to apply:** Invoquer automatiquement quand l'utilisateur fournit une URL ou demande une analyse de site web.
