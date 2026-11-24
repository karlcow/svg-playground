# svgwg#634: tspan and text shaping

Issue: https://github.com/w3c/svgwg/issues/634
Spec: https://w3c.github.io/svgwg/svg2-draft/text.html#FontsGlyphs and https://drafts.csswg.org/css-text-3/#boundary-shaping

SVG 2 says "Ligature formation should not be enabled when characters are in different DOM text nodes; thus, characters separated by markup should not use ligatures." In 2019 the WG agreed to follow CSS instead, but the edit was never made. CSS Text 3, 7.3 says shaping **must** break at an inline box boundary when margin, border or padding there is non-zero, when `vertical-align` is not its initial value, or at a bidi isolation boundary, and **must not** break when nothing changes or only things that do not affect the glyphs change (such as text decoration). In CSS Inline 3, `vertical-align` is a shorthand that includes `baseline-shift`.

**Status.** Not resolved.

## Page

| page | what it asks |
|---|---|
| [probe-634-tspan-boundary-shaping.html](probe-634-tspan-boundary-shaping.html) | 14 cases of `f` and `i` split by a `tspan` (or not), each rule of CSS Text 7.3 ported to SVG, plus the SVG-only `x`, `dx` and `rotate`. |

The text uses [Lato-Medium-Liga.ttf](Lato-Medium-Liga.ttf), the WPT font with an `fi` ligature (copyright 2011-2019 tyPoland Lukasz Dziedzic, SIL Open Font License 1.1, as stated in the font). Each case's `getComputedTextLength()` is compared with `<text>fi</text>` (ligature) and the same text with `font-variant-ligatures: none` (two glyphs). The control fails when the two references are not at least 0.5 apart: the font did not load, or the browser forms no ligature.

`getSubStringLength(1, 1)` is shown for information only. In WebKit it gives wrong values across a `tspan` boundary, so it decides nothing.

## Results

2026-11-24. Chrome Canary 160 and Firefox Nightly 163 passed the controls (ligature 34.78, two glyphs 35.77). Safari Technology Preview 257 and the system WebKit of macOS 27.3 form no `fi` ligature in SVG text (both references 35.76), so they cannot answer. The runs were made with a stricter control (1 unit) that marked Chrome and Firefox as failed; each file has `controls_passed_recomputed` with the 0.5 threshold of the current page.

| case | CSS Text 7.3 | Chrome Canary 160 | Firefox Nightly 163 |
|---|---|---|---|
| `f<tspan>i</tspan>` | must not break | ligature | separate |
| `<tspan fill="green">` | must not break | ligature | separate |
| `<tspan text-decoration="underline">` | must not break | ligature | separate |
| `<tspan baseline-shift="0">` | must not break | ligature | separate |
| `<tspan style="padding-left: 10px">` | padding does not apply to `tspan` | separate | separate |
| `<tspan baseline-shift="10">` | must break | **ligature** | separate |
| `<tspan style="vertical-align: 10px">` | must break | separate | separate |
| `<tspan style="unicode-bidi: isolate">` | must break | separate | separate |
| `<tspan font-weight="bold">` | changes the glyphs | separate | separate |
| `<tspan x="40">` | SVG: new text chunk | separate | separate |
| `<tspan dx="5">` | no rule | ligature | separate |
| `<text dx="0 5">fi</text>` | no rule (WPT expects ligature) | ligature | ligature |
| `<tspan rotate="10">` | no rule | ligature | separate |

Firefox breaks at every `tspan` boundary, as the SVG 2 sentence says. Chrome follows CSS except for `baseline-shift="10"` (kept, although `vertical-align: 10px` breaks) and `padding` (breaks, although padding does not apply to SVG text).
