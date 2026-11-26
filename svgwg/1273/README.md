# svgwg#1273: spatial media fragments in SVG images, image pixels or viewBox units

Issue: https://github.com/w3c/svgwg/issues/1273
Spec: https://w3c.github.io/svgwg/svg2-draft/linking.html#SVGFragmentIdentifiersDefinitions
Media Fragments: https://www.w3.org/TR/media-frags/#naming-space

SVG 2 says a space segment (`#xywh=x,y,w,h`) overrides the `viewBox`, so the numbers are viewBox units. Media Fragments says they are pixels of the image, with 0,0 its top-left corner, and percent is a percentage of the image. The two readings differ when an SVG's `width`/`height` and `viewBox` use different numbers, or when the `viewBox` does not start at 0,0. This page measures which region each browser selects in those cases, how a pixel rectangle is clamped when the SVG has no natural size, and what aspect ratio an `<img>` gets after a fragment.

Related: svgwg#1113 and #1136 (percent base without a natural size, resolved; text landed in svgwg PR #1271), WebKit bug https://bugs.webkit.org/show_bug.cgi?id=333147 (aspect ratio from the wrong view).

## Page

| page | what it asks |
|---|---|
| [probe-fragment-sizing.html](probe-fragment-sizing.html) | **Regions (A, B):** each SVG is a grid of 100-unit cells, cell (i,j) filled `rgb(30+50i, 30+50j, 160)` and labelled `i,j`. The image is drawn into a 100×100 canvas and the cell under each corner (12,12), (88,12), (12,88), (88,88) names the region selected. The live `<img>` column shows the same thing. **Ratio (C):** the layout height of `<img style="width:200px">` on an SVG with only `viewBox="0 0 400 200"`, and `naturalWidth` × `naturalHeight`. |

The SVG files are made by [make-svgs.py](make-svgs.py). [figure-xywh-units.png](figure-xywh-units.png) (made by [make-figure.py](make-figure.py), rendered in WebKit) draws the two main cases: the region in image pixels and the region browsers select. Serve the folder with any static server (`python3 -m http.server`): over `file:` the canvas column is blocked in some browsers and the SVG sources are not shown.

Controls: no fragment twice (must read the full grid, identical samples); `#q`, a `<view>` element (must read the bottom-right quarter on the canvas, otherwise the canvas path drops fragments in that browser and only the live column counts); `xywh=100,100,100,100` on the image where both readings agree (tells whether `xywh` is supported); the ratio image with no fragment (must be 100 tall).

The canvas column is not usable in two cases: WebKit drops the fragment when an SVG image is drawn into a canvas (bugs https://bugs.webkit.org/show_bug.cgi?id=322167 and https://bugs.webkit.org/show_bug.cgi?id=330747), and Firefox draws the SVG with no natural size smaller than the canvas. For those, the live `<img>` column was read from a full-page screenshot with [read-screenshot.py](read-screenshot.py) (`results/screenshot-*.png`, decoded output in `*.live-img.txt`).

## Results

From the files in [results/](results/). All on 2026-11-26.

The browsers were preview builds: Firefox Nightly 163, Chrome Canary 160 with chrome://flags/#enable-experimental-web-platform-features on (Chrome's `xywh` support is behind it), Safari Technology Preview 257 (no `xywh` support), and a local MiniBrowser built with https://github.com/WebKit/WebKit/pull/82207 and "SVG spatial media fragments" turned on in Experimental Features. Region readings are from the live `<img>` column. Bold cells differ from the Media Fragments reading.

| Fragment | Image | Media Fragments | viewBox units | Firefox | Chrome | WebKit (PR) |
|---|---|---|---|---|---|---|
| `xywh=100,100,100,100` | `width="400" height="400" viewBox="0 0 400 400"` | cell 1,1 | cell 1,1 | cell 1,1 | cell 1,1 | cell 1,1 |
| `xywh=percent:0,0,100,100` | same | whole | whole | whole | whole | whole |
| `xywh=percent:50,50,50,50` | same | bottom-right quarter | bottom-right quarter | bottom-right quarter | bottom-right quarter | bottom-right quarter |
| `xywh=percent:0,0,100,100` | `width="200" height="200" viewBox="0 0 400 400"` | whole | top-left quarter | **top-left quarter** | **top-left quarter** | **top-left quarter** |
| `xywh=0,0,200,200` | same | whole | top-left quarter | **top-left quarter** | **top-left quarter** | **top-left quarter** |
| `xywh=percent:50,50,50,50` | same | bottom-right quarter | cell 1,1 | **cell 1,1** | **cell 1,1** | **cell 1,1** |
| `xywh=100,100,100,100` | same | bottom-right quarter | cell 1,1 | **cell 1,1** | **cell 1,1** | **cell 1,1** |
| `xywh=0,0,400,400` | same | whole (clamped at 200) | top-left quarter | **top-left quarter** | **top-left quarter** | **top-left quarter** |
| `xywh=0,0,100,100` | `width="400" height="400" viewBox="100 100 400 400"` | cell 1,1 | cell 0,0 | **cell 0,0** | **cell 0,0** | **cell 0,0** |
| `xywh=0,0,400,400` | `viewBox="0 0 400 400"`, no size | (no rule) | | clamped at 300 (3×3 cells) | not clamped (whole) | not clamped (whole) |
| `xywh=percent:50,50,50,50` | same | 150×150 base (SVG 2, #1136) | | **300×300 base** (cells 1,1 to 2,2) | 150×150 base (cells 0,0 to 1,1) | 150×150 base (cells 0,0 to 1,1) |

Ratio, height of `<img style="width:200px">` on `viewBox="0 0 400 200"` with `<view id="sq" viewBox="0 0 200 200">` (expected 200 with a square fragment, per SVG 2 "Intrinsic sizing properties of SVG content", which takes the ratio from the active view):

| Fragment | Firefox | Chrome | WebKit (PR) | STP 257 |
|---|---|---|---|---|
| none | 100 | 100 | 100 | 100 |
| `#sq` | 200 | 200 | **100** | **100** |
| `#svgView(viewBox(0,0,200,200))` | 200 | 200 | **100** | **100** |
| `#xywh=0,0,100,100` | 200 | 200 | **100** | 100 (not supported) |
| `#xywh=percent:0,0,50,100` | 200 | **400** | **100** | 100 (not supported) |
| `#xywh=percent:0,0,50,100`, on a URL of its own | 200 | 200 | 200 | 100 (not supported) |
| `#xywh=percent:0,0,50,100`, after `#sq` on the same URL | 200 | **400** | 200 | **200** |

The rows above the last two load the same file one after the other, so in Chrome and WebKit they share one SVG document. Chrome resolves the percent base from the view the previous `<img>` left on that document (400 instead of 200). WebKit sizes the image from the wrong view: see bug 333147.

Summary: Firefox, Chrome and WebKit (PR 82207) agree with each other on every region row, and read the numbers as viewBox units after resolving percent and clamping against the image size in CSS pixels. None follows the Media Fragments reading when the two differ.
