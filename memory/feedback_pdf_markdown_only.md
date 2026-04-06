---
name: PDF toujours en Markdown jamais en HTML
description: Le contenu envoye a send_report.py doit TOUJOURS etre du Markdown pur, jamais du HTML
type: feedback
---

Le script send_report.py attend du **Markdown**, pas du HTML. Les balises HTML (<h1>, <table>, <div>, etc.) ne sont pas interpretees et rendent le PDF illisible.

**Why:** Le PDF envoye le 28/03/2026 (analyse ALIEV) etait illisible car le contenu etait en HTML brut au lieu de Markdown. L'utilisateur a signale le probleme.

**How to apply:**
- TOUJOURS utiliser #, ##, ### pour les titres
- TOUJOURS utiliser | col | col | pour les tableaux
- TOUJOURS utiliser **gras** pour l'emphase
- JAMAIS de <h1>, <table>, <div>, <b>, <tr>, <td>, &euro;, &mdash;, etc.
- Tester mentalement la lisibilite avant d'envoyer
