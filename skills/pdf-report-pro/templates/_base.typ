// _base.typ — Design system institutionnel pdf-report-pro v2
// Baseline grid 8pt, typo Inter/Source Serif 4, palette WCAG AA

#let primary = rgb("#0B3D91")  // institutional blue
#let accent  = rgb("#E63946")  // alert red
#let ink     = rgb("#1A1A1A")
#let ink2    = rgb("#4A4A4A")
#let rule    = rgb("#B0B0B0")
#let bg      = rgb("#F5F5F5")

// Baseline 8pt — toutes les tailles sont multiples de 8
#let base = 8pt
#let leading = 1.4

#let institutional(
  title: none,
  subtitle: none,
  author: "Alexandre Collenne",
  audience: "Board",
  version: "1.0",
  date: datetime.today(),
  classification: "Confidential",
  body
) = {
  set document(title: title, author: author)
  set page(
    paper: "a4",
    margin: (x: 2.5cm, y: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(8pt, fill: ink2)
        #title #h(1fr) #classification
        #line(length: 100%, stroke: 0.5pt + rule)
      ]
    },
    footer: context [
      #set text(8pt, fill: ink2)
      #line(length: 100%, stroke: 0.5pt + rule)
      v#version #h(1fr) #counter(page).display() / #counter(page).final().first()
    ]
  )
  set text(font: ("Inter", "Helvetica", "Arial"), size: 10pt, fill: ink, lang: "fr")
  set par(leading: leading * 0.5em, justify: true, first-line-indent: 0pt)
  show heading.where(level: 1): it => {
    set text(font: ("Source Serif 4", "Georgia"), size: 24pt, weight: "semibold", fill: primary)
    block(above: 24pt, below: 16pt, it.body)
  }
  show heading.where(level: 2): it => {
    set text(size: 14pt, weight: "semibold", fill: primary)
    block(above: 16pt, below: 8pt, it.body)
  }
  show heading.where(level: 3): it => {
    set text(size: 11pt, weight: "semibold", fill: ink)
    block(above: 12pt, below: 4pt, it.body)
  }

  // COVER
  align(center + horizon)[
    #text(32pt, weight: "bold", fill: primary, font: ("Source Serif 4", "Georgia"))[#title] \
    #v(8pt)
    #text(14pt, fill: ink2)[#subtitle] \
    #v(48pt)
    #grid(columns: 2, gutter: 32pt,
      align(left)[#text(9pt, fill: ink2)[Audience]\ #text(11pt)[#audience]],
      align(left)[#text(9pt, fill: ink2)[Date]\ #text(11pt)[#date.display("[day]/[month]/[year]")]]
    )
    #v(16pt)
    #text(8pt, fill: accent)[#classification — Version #version]
  ]
  pagebreak()

  body
}

// Action title (titre Minto avec verbe + chiffre)
#let action-title(t) = heading(level: 2, t)

// KPI bloc
#let kpi(label, value, delta: none) = box(
  fill: bg, inset: 12pt, radius: 4pt,
  stack(spacing: 4pt,
    text(8pt, fill: ink2, label),
    text(20pt, weight: "bold", fill: primary, value),
    if delta != none { text(9pt, fill: accent, delta) }
  )
)

// Source citation [N]
#let src(n) = super(text(fill: primary, weight: "bold", str(n)))
