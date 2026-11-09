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

## Known problem in current WebKit

Safari Technology Preview 256 and WebKit trunk builds from November 2026 fail the controls of both pages: no `svgView()` fragment is applied when an SVG image is drawn into a canvas, even the plain `#svgView(viewBox(100,0,100,100))`. The same images show the fragment on screen. This is a WebKit regression unrelated to this issue (https://bugs.webkit.org/show_bug.cgi?id=330747), so a WebKit run with `controls_passed: false` says nothing about the question here. The Safari 27.3 engine (WebKit 22626.1.10) passes.

## Results

From the files in [results/](results/). "yes" means the view was applied. Runs whose controls failed are not counted.

### probe-svgview-whitespace-escaping.html, November 2026

| fragment | WebKit 22626.1.10 | Firefox 161 | Chrome 159 |
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

WebKit 22626.1.10 is the system WebKit of macOS 27.3 (the engine of Safari 27.3) in an embedded view, 2026-11-09; its user agent string says Version/26.4. Firefox 161.0 and Chrome 159.0.0.0, 2026-11-10. Safari Technology Preview 256 (build 22627.1.6.3, user agent Version/27.0) failed the controls of both probes on 2026-11-10: no fragment is applied at all, not even the plain one, when the image is drawn into a canvas. That is a WebKit regression on trunk, being investigated, and those runs are left out.

### probe-svgview-spaces.html

| fragment | STP (Aug) | Firefox 156 (Aug) | Chrome 153 (Aug) | Firefox 161 (Nov) | Chrome 159 (Nov) |
|---|---|---|---|---|---|
| `#svgView(viewBox(100,0,100,100))` | yes | yes | yes | yes | yes |
| `#svgView(viewBox(100, 0, 100, 100))` | yes | yes | yes | yes | yes |
| `#svgView(viewBox(100,%200,%20100,%20100))` | yes | yes | yes | yes | yes |
| `#svgView( viewBox(100,0,100,100) )` | no | no | no | no | yes |
| `#svgView(%20viewBox(100,0,100,100)%20)` | no | no | no | no | yes |
| `#svgView(viewBox( 100,0,100,100 ))` | no | yes | no | yes | no |
| `#svgView(viewBox(100 0 100 100))` | yes | yes | yes | yes | yes |
| `#svgView(viewBox(100,0,100,100) ; preserveAspectRatio(none))` | no | no | no | no | yes |
| `#svgView(viewBox(100,0,100,100)%20;%20preserveAspectRatio(none))` | no | no | no | no | yes |
| `#%20svgView(viewBox(100,0,100,100))%20` | no | no | no | no | no |
| `#svgView%28viewBox(100,0,100,100)%29` | not in that version | not in that version | not in that version | yes | yes |
| `#svgView(viewBox(100%2C0%2C100%2C100))` | not in that version | not in that version | not in that version | yes | yes |
| `#svgView%28viewBox%28100%2C0%2C100%2C100%29%29` | not in that version | not in that version | not in that version | yes | yes |

August runs on 2026-08-20; the WebKit one is a Safari Technology Preview release of that time (user agent Version/27.0, release number not recorded). November runs on 2026-11-10. The three escaped-punctuation rows were added to the page after the August runs.

### Changes since August

- **Chrome now accepts whitespace inside `svgView( ... )` and around `;`.** Chromium commit 03fbfba37ea89, 2026-10-14, "Allow whitespace around svgView() attributes" (crbug.com/552539605), which also made WPT `svgview-spaces.html` and `svgview-spaces-around-semicolon.html` pass. This came after the 2026-09-29 resolution, which says whitespace is not permitted there.
- Firefox 161 applies `#xywh=` media fragments, literal and encoded. Not part of this issue.

A typed space and `%20` behave the same in every browser and every position measured, so the fragment is decoded before it is read.
