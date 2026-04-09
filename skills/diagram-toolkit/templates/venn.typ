// Venn diagram — {{SO_WHAT}}
#import "@preview/cetz:0.2.2": canvas, draw

#set page(paper: "a4", flipped: true, margin: 2cm)
#align(center)[
  #text(size: 18pt, weight: "bold")[{{SO_WHAT}}]
  #v(1cm)

  #canvas({
    import draw: *
    circle((0, 0), radius: 3, stroke: rgb("{{PRIMARY}}"), fill: rgb("{{PRIMARY}}").lighten(70%))
    circle((3, 0), radius: 3, stroke: rgb("{{SECONDARY}}"), fill: rgb("{{SECONDARY}}").lighten(70%))
    content((-2, 0), [{{SET_A}}])
    content((5, 0), [{{SET_B}}])
    content((1.5, 0), [{{INTER}}])
  })
]
