// quarterly_review.typ — 10-15 page quarterly business review
#import "_base.typ": *

#show: institutional.with(
  title: "Quarterly Business Review",
  subtitle: "Q[N] [YEAR]",
  audience: "Executive Committee",
  version: "1.0",
  classification: "Internal",
)

= Executive summary

[Action title — 1 phrase verbe + chiffre]

#grid(columns: 4, gutter: 12pt,
  kpi("Revenue", "€XXM", delta: "+X%"),
  kpi("EBITDA", "€XXM", delta: "+X%"),
  kpi("NPS", "XX", delta: "+X"),
  kpi("Headcount", "XXX", delta: "+X")
)

#v(8pt)
[2-3 phrases : highlights et lowlights majeurs du trimestre.]

= Performance financière

== [Action title — chiffre]
[Analyse + chart Tufte]

== [Action title — chiffre]
[Analyse + table]

= Performance opérationnelle

== [Action title]
[Texte + visuel]

= Risques et opportunités

#table(columns: (1fr, 1fr), stroke: 0.5pt + rule, inset: 8pt,
  table.header[*Risques*][*Opportunités*],
  [- ...\ - ...\ - ...], [- ...\ - ...\ - ...]
)

= Plan d'action Q[N+1]

1. [Initiative 1 — owner — KPI]
2. [Initiative 2 — owner — KPI]
3. [Initiative 3 — owner — KPI]

= Annexe — Sources

[1] ...
[2] ...
[3] ...
