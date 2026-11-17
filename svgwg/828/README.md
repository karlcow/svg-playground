# svgwg#828: UA stylesheet `display: none` with importance on never-rendered elements

Issue: https://github.com/w3c/svgwg/issues/828 (also https://github.com/w3c/svgwg/issues/810)
Spec fix: https://github.com/w3c/svgwg/pull/1250
Spec: https://w3c.github.io/svgwg/svg2-draft/render.html#TermNeverRenderedElement

SVG 2 said in 9 sentences that `defs`, `symbol`, `title`, `desc`, `metadata`, `marker`, the paint servers, `script` and `style` get `display: none` from the user agent style sheet, "and this declaration must have importance over any other CSS rule or presentation attribute". If a browser did that, `getComputedStyle(el).display` would be `none` for these elements whatever the author writes. The rules were removed from the UA style sheet in March 2026 (https://github.com/w3c/svgwg/pull/1071), and #1250 rewords the sentences as "never-rendered element".

## Page

| page | what it asks |
|---|---|
| [probe-ua-display-none-importance.html](probe-ua-display-none-importance.html) | `getComputedStyle(el).display` and `getClientRects().length` for 10 elements, each in 4 cases: no styling, author `display: inline !important`, `display="inline"`, `style="display: inline"`. |

Each element sits in a small inline `<svg>` in the HTML page. Controls: an HTML `title` must compute to `none` (a UA rule does show in computed style), a `g` with `display="none"` must compute to `none` and one with an author `!important` rule to `block` (author rules and attributes reach SVG elements), a `rect` must have a client rect, and one case runs twice.

## Results

From the files in [results/](results/). `getComputedStyle(el).display` with no author styling. The spec text before #1250 expects `none` everywhere.

| element | Safari 27.0 | Firefox 162 | Chrome 160 |
|---|---|---|---|
| `defs` | inline | inline | inline |
| `title` | **none** | inline | inline |
| `desc` | inline | inline | inline |
| `metadata` | inline | inline | inline |
| `marker` | inline | inline | inline |
| `linearGradient` | inline | inline | inline |
| `radialGradient` | inline | inline | inline |
| `pattern` | inline | inline | inline |
| `script` | inline | **none** | inline |
| `style` | inline | **none** | inline |

All on 2026-11-14. All controls passed.

In the three other cases (author `!important`, `display` attribute, `style` attribute) every browser returns `inline` for every element, including the bold ones: those `none` values come from plain UA rules (`title` in WebKit's `svg.css`, `script, style` in Gecko's `svg.css`), not from `!important` ones. `getClientRects()` is empty for all 10 elements in all cases and all browsers, so none of them is rendered, whatever `display` computes to.

The runs were made before the folder moved here, so the `probe` field inside them says `svgwg-new-ua-display-none-importance`.
