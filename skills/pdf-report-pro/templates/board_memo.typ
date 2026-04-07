// board_memo.typ — 1-page board memo (Bezos style)
#import "_base.typ": *

#show: institutional.with(
  title: "[TITRE — verbe + chiffre]",
  subtitle: "Board memo — décision requise",
  audience: "Board of Directors",
  version: "1.0",
  classification: "Confidential",
)

= Recommandation

[1 phrase action title — la décision recommandée avec verbe et chiffre]

= Contexte

[3-4 lignes max — situation actuelle, déclencheur]

= Options évaluées

#table(
  columns: (1fr, 2fr, 1fr, 1fr),
  stroke: 0.5pt + rule,
  inset: 8pt,
  align: (left, left, center, center),
  table.header[*Option*][*Description*][*Coût*][*Risque*],
  [A], [...], [€...], [Faible],
  [B], [...], [€...], [Moyen],
  [C — *recommandée*], [...], [€...], [Faible],
)

= Justification

- Argument 1 #src(1)
- Argument 2 #src(2)
- Argument 3 #src(3)

= Prochaines étapes

1. [Action 1 — owner — date]
2. [Action 2 — owner — date]
3. [Action 3 — owner — date]

#v(1fr)
#line(length: 100%, stroke: 0.5pt + rule)
#text(8pt, fill: ink2)[Sources : [1] ... [2] ... [3] ...]
