// Build: typst compile one-pager.typ one-pager.pdf
// Edit points - only these four lines:
#let contact-email = "beattle1984@gmail.com"
#let contact-linkedin = "[FILL IN: profile URL]"
#let repo-example = "github.com/sensus-stoa/permutation-test-ml"
#let details-url = "[FILL IN: link to the detailed description]"

#set page(paper: "a4", margin: (x: 17mm, y: 15mm))
#set text(font: ("Libertinus Serif", "DejaVu Sans"), size: 10.5pt, lang: "en")
#set par(leading: 0.6em, justify: false)

#let accent = rgb("#1f3a5f")
#let bad = rgb("#b03a2e")
#let pale = rgb("#e6e6e6")

#let card(title, body) = rect(
  width: 100%, inset: 8pt, radius: 3pt,
  stroke: 0.6pt + rgb("#d5d5d5"), fill: rgb("#fafafa")
)[
  #text(size: 8.5pt, weight: "bold", fill: accent)[#title]
  #v(4pt)
  #text(size: 9.5pt)[#body]
]

#text(size: 15pt, weight: "bold", fill: accent)[
  Verifying one claim about your model
]
#v(3pt)
Evgeniy Dolgov. 15 years in backend and architecture. One person, not an agency.
#v(9pt)

#grid(
  columns: (1fr, auto, 1fr, auto, 1fr), gutter: 5pt,
  card("YOU PROVIDE", [One claim \ Code and settings \ Data, or a run on your side]),
  align(center + horizon, text(size: 13pt, fill: accent)[#sym.arrow.r]),
  card("WHAT WE DO", [We fix criteria before the run \ We reproduce the computation \ We run null-data checks]),
  align(center + horizon, text(size: 13pt, fill: accent)[#sym.arrow.r]),
  card("YOU GET", [Confirmed / not confirmed / not enough data \ Where the conclusion does not apply]),
)
#v(10pt)

#text(weight: "bold")[A typical failure.] The model showed 3% error in tests and 12% in production.
The tests fed it the actual weather for the same day. In production only the forecast
is available in advance. The model was looking into the future, and the test did not catch it.
#v(9pt)

#let marks = range(50).map(i => rect(
  width: 7pt, height: 7pt, radius: 1pt, stroke: none,
  fill: if i < 36 { bad } else { pale }
))

#grid(columns: (auto, 1fr), gutter: 12pt,
  [
    #grid(columns: 10, gutter: 2.5pt, ..marks)
    #v(3pt)
    #text(size: 8.5pt, fill: bad)[36 of 50]
  ],
  [
    #text(weight: "bold")[Why you can trust this.] In our open example, a naive check
    took pure noise for signal in 36 of 50 cases. We measured it and published it,
    along with the cases where our method does not work. How many errors our own
    procedure misses will be published before the first paid check.
  ],
)
#v(10pt)
#line(length: 100%, stroke: 0.5pt + rgb("#dddddd"))
#v(7pt)

#grid(columns: (1fr, 1fr), gutter: 12pt,
  [
    #text(weight: "bold")[Price and timeline.] Reference: 800-1200 EUR, exact price
    after a scope assessment, 3-5 business days from receiving the materials.
  ],
  [
    #text(weight: "bold")[What we do not do.] We do not train the model. We do not
    issue a certificate. We do not promise it will never break.
  ],
)
#v(9pt)
#line(length: 100%, stroke: 0.5pt + rgb("#dddddd"))
#v(6pt)
#text(size: 9pt)[
  Example: #link("https://" + repo-example)[#repo-example] - synthetic data; not yet tested on real power-sector data \
  Verification protocol: #link("https://github.com/sensus-stoa/permutation-test-ml/tree/main/trust")[https://github.com/sensus-stoa/permutation-test-ml/tree/main/trust] \
  Detailed description: #details-url \
  Contact: #contact-email · LinkedIn #contact-linkedin
]
