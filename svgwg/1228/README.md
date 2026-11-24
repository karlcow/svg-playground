# svgwg#1228: radialGradient, negative r and fr

Issue: https://github.com/w3c/svgwg/issues/1228
Spec: https://w3c.github.io/svgwg/svg2-draft/pservers.html#RadialGradientElementRAttribute and https://w3c.github.io/svgwg/svg2-draft/pservers.html#PaintServerTemplates

SVG 2 says a negative `r` or `fr` "is an error". On 2026-10-20 the WG held `radialGradient` out of #1209 (negative values take the initial value) and asked for more tests, especially with `href` references (https://www.w3.org/2026/10/20-svg-minutes.html#602d).

**Status.** Not resolved. The proposal in the issue: a negative `r` or `fr` takes the initial value, and on a gradient using `href` a value that fails to parse is treated as not specified, so the template's value is used.

## Pages

| page | what it asks |
|---|---|
| [probe-1228-reftests.html](probe-1228-reftests.html) | Runs the two draft reftests in [wpt-drafts/](wpt-drafts/) as a reftest harness would: draws the test and its reference into a canvas and compares the pixels. |

The draft tests, both `.tentative` because they encode the proposal, not a resolution:

- [radialgradient-negative-r.tentative.svg](wpt-drafts/radialgradient-negative-r.tentative.svg): `r="-10"` must look like `r` unset (50%).
- [radialgradient-href-negative-r.tentative.svg](wpt-drafts/radialgradient-href-negative-r.tentative.svg): the template has `r="0.25"`, the referencing gradient `r="-10"`; it must look like `r="0.25"`.

Controls: the reference against itself must match; `r` unset against `r="0.25"` must differ. A sanity row compares a negative `fr` with `fr` unset, which WPT `svg/pservers/reftests/radialgradient-basic-003.svg` already expects to match.

## Results

From the files in [results/](results/), 2026-11-24. All runs passed their controls.

| case | Safari Technology Preview 257 | Firefox Nightly 163 | Chrome Canary 160 |
|---|---|---|---|
| negative `fr` (sanity) | match | match | match |
| `radialgradient-negative-r` | differs, solid gold (first stop) | match | differs, solid navy (last stop) |
| `radialgradient-href-negative-r` | differs, solid gold (first stop) | match | differs, solid navy (last stop) |

The system WebKit of macOS 27.3 (the Safari 27.3 engine; its user agent string says Version/26.4) in an embedded view gives the same results as the Safari row (`run-2026-11-24-webkit-macos-27.3-...`).

So Firefox already does what the proposal asks. Safari keeps the negative `r` and draws the first stop everywhere, Chrome keeps it and draws the last stop. This matches the 2026-10-27 measurements in the issue description.
