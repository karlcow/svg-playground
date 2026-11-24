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

2026-11-24. Chrome Canary 160 and Firefox Nightly 163 passed the controls (ligature 34.78, two glyphs 35.77). In Safari Technology Preview 257 and the system WebKit of macOS 27.3 both references read 35.76, but not because WebKit forms no ligature: before https://github.com/WebKit/WebKit/pull/80809 and https://github.com/WebKit/WebKit/pull/80810 (after STP 257), WebKit's text DOM methods measure characters one by one. The drawing shows the ligature, so the macOS 27.3 column below is read from screenshots (`results/screenshot-2026-11-24-webkit-macos-27.3-*.png`). The WebKit trunk column is measured by the page: a MiniBrowser build of main from 2026-11-21, which has both PRs; its controls pass. The runs were made with a stricter control (1 unit) that marked Chrome and Firefox as failed; each file has `controls_passed_recomputed` with the 0.5 threshold of the current page.

| case | CSS Text 7.3 | Chrome Canary 160 | Firefox Nightly 163 | macOS 27.3 WebKit, as drawn | WebKit trunk |
|---|---|---|---|---|---|
| `<text>fi</text>` (reference) | ligature | ligature | ligature | ligature | ligature |
| `f<tspan>i</tspan>` | must not break | ligature | separate | separate | separate |
| `<tspan fill="green">` | must not break | ligature | separate | separate | separate |
| `<tspan text-decoration="underline">` | must not break | ligature | separate | separate | separate |
| `<tspan baseline-shift="0">` | must not break | ligature | separate | separate | separate |
| `<tspan style="padding-left: 10px">` | padding does not apply to `tspan` | separate | separate | separate | separate |
| `<tspan baseline-shift="10">` | must break | **ligature** | separate | separate | separate |
| `<tspan style="vertical-align: 10px">` | must break | separate | separate | separate | separate |
| `<tspan style="unicode-bidi: isolate">` | must break | separate | separate | separate | separate |
| `<tspan font-weight="bold">` | changes the glyphs | separate | separate | separate | separate |
| `<tspan x="40">` | SVG: new text chunk | separate | separate | separate | separate |
| `<tspan dx="5">` | no rule | ligature | separate | separate | separate |
| `<text dx="0 5">fi</text>` | no rule (WPT expects ligature) | ligature | ligature | **separate** | ligature |
| `<tspan rotate="10">` | no rule | ligature | separate | separate | separate |

Firefox and WebKit break at every `tspan` boundary, as the SVG 2 sentence says. The 27.3 WebKit also broke it for `dx` inside one text node; trunk keeps it, since PR 80809. Chrome follows CSS except for `baseline-shift="10"` (kept, although `vertical-align: 10px` breaks) and `padding` (breaks, although padding does not apply to SVG text).
