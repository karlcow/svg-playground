# svgwg#1170: whitespace and percent-encoding in svgView() fragments

Issue: https://github.com/w3c/svgwg/issues/1170
Spec: https://w3c.github.io/svgwg/svg2-draft/linking.html#SVGFragmentIdentifiersDefinitions

SVG 2 says "Spaces are allowed in fragment specifications" and that fragment identifiers "may be url-escaped". These pages check what browsers actually accept in a fragment such as `picture.svg#svgView(viewBox(100,0,100,100))`.

**Status.** Spaces: resolved on 2026-09-29 (https://www.w3.org/2026/09/29-svg-minutes.html). Whitespace is allowed only inside a parameter list, where the attribute's own grammar allows it, and nowhere else in the fragment. Escaping: not discussed yet.

## Pages

| page | what it asks |
|---|---|
| [probe-svgview-spaces.html](probe-svgview-spaces.html) | Each place a space can sit, measured on its own, and the same with the space written `%20`. |
| [probe-svgview-whitespace-escaping.html](probe-svgview-whitespace-escaping.html) | The same positions, plus leading and trailing whitespace inside `viewBox(...)` split apart, plus punctuation written percent-encoded (`%3B`, `%28`, `%29`, `%2C`, and all of them at once). |

Both draw a 200 by 200 SVG of four coloured squares through an `img`, with the fragment added to its URL. One colour left means the view was applied, four colours mean the fragment was ignored.

## Results

From the files in [results/](results/). "yes" means the view was applied.

| fragment | Safari 27.0 | Firefox 156.0 | Chrome 153 | WebKit 26.4 |
|---|---|---|---|---|
| `#svgView(viewBox(100,0,100,100))` (control) | yes | yes | yes | yes |
| `#svgView(viewBox(100, 0, 100, 100))` | yes | yes | yes | yes |
| `#svgView(viewBox(100 0 100 100))` | yes | yes | yes | yes |
| `#svgView(viewBox( 100,0,100,100))` | | | | yes |
| `#svgView(viewBox(100,0,100,100 ))` | | | | no |
| `#svgView(viewBox( 100,0,100,100 ))` | no | yes | no | no |
| `#svgView( viewBox(100,0,100,100) )` | no | no | no | no |
| `#svgView(viewBox(100,0,100,100) ; preserveAspectRatio(none))` | no | no | no | no |
| `#%20svgView(viewBox(100,0,100,100))%20` | no | no | no | no |
| `#svgView(viewBox(100,%200,%20100,%20100))` | yes | yes | yes | yes |
| `#svgView(%20viewBox(100,0,100,100)%20)` | no | no | no | no |
| `#svgView(viewBox(100,0,100,100)%20;%20preserveAspectRatio(none))` | no | no | no | no |
| `#svgView(viewBox(100,0,100,100)%3BpreserveAspectRatio(none))` | | | | yes |
| `#svgView%28viewBox(100,0,100,100)%29` | | | | yes |
| `#svgView(viewBox(100%2C0%2C100%2C100))` | | | | yes |
| `#svgView%28viewBox%28100%2C0%2C100%2C100%29%29` | | | | yes |

The first three browser columns are `probe-svgview-spaces.html`, 2026-08-20. The WebKit 26.4 column is `probe-svgview-whitespace-escaping.html`, 2026-11-09, run in an embedded WebKit view (system WebKit, not Safari Technology Preview). Empty cells have not been measured yet: running the second page in Firefox and Chrome fills them.

A typed space and `%20` behave the same everywhere they were both measured, so the fragment is decoded before it is read.
