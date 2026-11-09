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

From the files in [results/](results/). "yes" means the view was applied. Runs whose controls failed are not counted.

### probe-svgview-whitespace-escaping.html, November 2026

| fragment | WebKit 26.4 | Firefox 161 | Chrome 159 |
|---|---|---|---|
| `#svgView(viewBox(100,0,100,100))` | yes | yes | yes |
| `#svgView(viewBox(100, 0, 100, 100))` | yes | yes | yes |
| `#svgView(viewBox(100 0 100 100))` | yes | yes | yes |
| `#svgView( viewBox(100,0,100,100) )` | no | no | yes |
| `#svgView(viewBox(100,0,100,100) ; preserveAspectRatio(none))` | no | no | yes |
| `#%20svgView(viewBox(100,0,100,100))%20` | no | no | no |
| `#svgView(viewBox( 100,0,100,100))` | yes | yes | yes |
| `#svgView(viewBox(100,0,100,100 ))` | no | yes | no |
| `#svgView(viewBox( 100,0,100,100 ))` | no | yes | no |
| `#svgView(viewBox(100,0,100,100)%3BpreserveAspectRatio(none))` | yes | yes | yes |
| `#svgView%28viewBox(100,0,100,100)%29` | yes | yes | yes |
| `#svgView(viewBox(100%2C0%2C100%2C100))` | yes | yes | yes |
| `#svgView%28viewBox%28100%2C0%2C100%2C100%29%29` | yes | yes | yes |
| `#svgView(viewBox(100,%200,%20100,%20100))` | yes | yes | yes |
| `#svgView(%20viewBox(100,0,100,100)%20)` | no | no | yes |
| `#svgView(viewBox(100,0,100,100)%20;%20preserveAspectRatio(none))` | no | no | yes |
| `#xywh=100,0,100,100` | no | yes | no |
| `#%78ywh=100,0,100,100` | no | yes | no |

WebKit 26.4 is the system WebKit in an embedded view, 2026-11-09. Firefox 161.0 and Chrome 159.0.0.0, 2026-11-10. A Safari 27.0 run on 2026-11-10 failed its controls (no fragment applied at all, not even the plain one) and is left out until it is understood.

### probe-svgview-spaces.html, August 2026

| fragment | Safari 27.0 | Firefox 156 | Chrome 153 |
|---|---|---|---|
| `#svgView(viewBox(100,0,100,100))` | yes | yes | yes |
| `#svgView(viewBox(100, 0, 100, 100))` | yes | yes | yes |
| `#svgView(viewBox(100,%200,%20100,%20100))` | yes | yes | yes |
| `#svgView( viewBox(100,0,100,100) )` | no | no | no |
| `#svgView(%20viewBox(100,0,100,100)%20)` | no | no | no |
| `#svgView(viewBox( 100,0,100,100 ))` | no | yes | no |
| `#svgView(viewBox(100 0 100 100))` | yes | yes | yes |
| `#svgView(viewBox(100,0,100,100) ; preserveAspectRatio(none))` | no | no | no |
| `#svgView(viewBox(100,0,100,100)%20;%20preserveAspectRatio(none))` | no | no | no |
| `#%20svgView(viewBox(100,0,100,100))%20` | no | no | no |

All three on 2026-08-20.

### Changes since August

- **Chrome now accepts whitespace inside `svgView( ... )` and around `;`.** Chromium commit 03fbfba37ea89, 2026-10-14, "Allow whitespace around svgView() attributes" (crbug.com/552539605), which also made WPT `svgview-spaces.html` and `svgview-spaces-around-semicolon.html` pass. This came after the 2026-09-29 resolution, which says whitespace is not permitted there.
- Firefox 161 applies `#xywh=` media fragments, literal and encoded. Not part of this issue.

A typed space and `%20` behave the same in every browser and every position measured, so the fragment is decoded before it is read.
