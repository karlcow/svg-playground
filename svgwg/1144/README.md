# svgwg#1144: SVG fragments and the `:~:` fragment directive (CSS Linked Parameters)

Issue: https://github.com/w3c/svgwg/issues/1144
Spec: https://w3c.github.io/svgwg/svg2-draft/linking.html#SVGFragmentIdentifiers and https://drafts.csswg.org/css-link-params-1/#link-parameter-directive

CSS Linked Parameters passes values to an SVG image with a fragment directive: `image.svg#:~:param(--color:green)`. A fragment directive is cut off before the document reads its fragment, so nothing needs registering for `image/svg+xml`. What SVG 2 still has to say is what happens when both are present: `icons.svg#icon-view:~:param(--color:green)` should still select `<view id="icon-view">`. This page checks whether browsers cut the directive before matching the SVG fragment. No browser ships Linked Parameters, but the cut happens before `param()` is parsed, so it can be measured now.

**Status.** Not resolved. The proposal in the issue: one sentence in SVG fragment identifiers, saying the SVG fragment identifier is the URL's fragment after the fragment directive has been removed.

## Page

| page | what it asks |
|---|---|
| [probe-1144-fragment-directive-view.html](probe-1144-fragment-directive-view.html) | Eight fragments, each through four routes: an `iframe` load, a hash change in that `iframe`, an `<img>` drawn into a canvas, and a CSS `background-image`. |

The SVG has four squares and `<view id="v">`, which shows the orange one. One colour means a view applied, four colours mean the fragment was not matched. The `iframe` columns are read by script with `elementFromPoint()`. Script cannot read the pixels of a CSS background, so that column is read from screenshots, and so is the `<img>` column in Safari Technology Preview (see below).

Run it over http: Chrome does not let a `file://` page read a blob `iframe`.

## Results

2026-11-24, over http. Controls (no fragment, `#v`) passed in every column counted. Same result for `:~:text=foo`, one `param()` and two.

| `#v:~:param(--c:green)` | Safari Technology Preview 257 | Firefox Nightly 163 | Chrome Canary 160 | system WebKit of macOS 27.3 |
|---|---|---|---|---|
| `iframe` load | view | view | view | view |
| `iframe` hash change | **no view** | view | view | **no view** |
| `<img>` | view | view | **no view** | **no view** |
| CSS `background-image` | view | view | **no view** | **no view** |
| `#svgView(...):~:param(...)`, every route | view | view | view | view |

- Only Firefox cuts the directive before matching in every route.
- Chrome cuts it on navigation, not when the SVG is used as an image, which is the Linked Parameters case.
- WebKit misses it on a same-document navigation (hash change). For images, Safari Technology Preview cuts it, the system WebKit of macOS 27.3 (the Safari 27.3 engine; its user agent string says Version/26.4) does not: fixed on trunk by https://bugs.webkit.org/show_bug.cgi?id=328791.
- `svgView()` is never affected: text after its closing `)` is ignored.

The `<img>` and CSS columns come from screen pixels, four samples per box: [screenshot-2026-11-24-stp257-firefox163-chrome160-probe-1144.png](results/screenshot-2026-11-24-stp257-firefox163-chrome160-probe-1144.png) for the three browsers, and the two `screenshot-2026-11-24-webkit-macos-27.3-*` files for the system WebKit. In Safari Technology Preview 257 the script's canvas reading of the `<img>` failed its controls, because drawing an SVG image into a canvas ignores its view (https://bugs.webkit.org/show_bug.cgi?id=330747); the image on screen shows the view.
