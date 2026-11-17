# svgwg#1260: getNumberOfChars() returns 0 for text inside defs, symbol or pattern, but no browser does

Issue: https://github.com/w3c/svgwg/issues/1260 (the whitespace table on the same page serves https://github.com/w3c/svgwg/issues/1261)
Spec: https://w3c.github.io/svgwg/svg2-draft/text.html#__svg__SVGTextContentElement__getNumberOfChars

SVG 2's `getNumberOfChars()` returns 0 when "the element is not rendered", and that test also applies to the element the method is called on. A `<text>` inside `defs`, `symbol`, `pattern` or `clipPath` is not rendered (it is a descendant of a never-rendered element, https://w3c.github.io/svgwg/svg2-draft/render.html#Rendered-vs-NonRendered), so the spec says it has 0 characters, and a length of 0 since `getComputedTextLength()` is built on `getNumberOfChars()`. This page asks what browsers return, with composed characters as well as plain letters.

## Page

| page | what it asks |
|---|---|
| [probe-getnumberofchars-composed-never-rendered.html](probe-getnumberofchars-composed-never-rendered.html) | `getNumberOfChars()`, `getComputedTextLength()` and whether `getBBox()` is non-zero, for 7 strings (ASCII, precomposed and decomposed e acute, an emoji, a ZWJ family emoji, a flag, Devanagari RA + vowel sign AA) in 9 placements: in the document, `display="none"` on the text, inside `defs` (used and unused), under a `g` with `display="none"`, inside `clipPath`, `symbol` and `pattern` (used), and not inserted in the document. A second table measures whitespace (svgwg#1261). |

Controls: `abc` in the document has 3 characters and a length, `abc` with `display="none"` has 0, `textContent.length` matches the UTF-16 count written by hand for every string (the text reached the DOM intact), and one case is repeated. Strings are written as escapes in the source, so the file stays ASCII.

## Results

From the files in [results/](results/). All on 2026-11-17. All controls passed.

`getNumberOfChars()` for `abc`, `e` + U+0301, U+1F600 and man ZWJ woman ZWJ girl (3, 2, 2 and 8 UTF-16 code units):

| where the `<text>` is | Safari 27.0 | Firefox 162 | Chrome 160 | spec today |
|---|---|---|---|---|
| in the document | 3, 2, 2, 8 | 3, 2, 2, 8 | 3, 2, 2, 8 | 3, 2, 2, 8 |
| `display="none"` on the text | 0 | 0 | 0 | 0 |
| inside `defs`, drawn by `use` | 3, 2, 2, 8 | 3, 2, 2, 8 | 3, 2, 2, 8 | **0** |
| inside `defs`, not used | 3, 2, 2, 8 | 3, 2, 2, 8 | 3, 2, 2, 8 | **0** |
| inside `symbol`, drawn by `use` | 3, 2, 2, 8 | 3, 2, 2, 8 | 3, 2, 2, 8 | **0** |
| inside `pattern`, used as a fill | 3, 2, 2, 8 | 3, 2, 2, 8 | 3, 2, 2, 8 | **0** |
| inside `clipPath`, used as a clip | 3, 2, 2, 8 | 3, 2, 2, 8 | 3, 2, 2, 8 | **0** |
| inside `<g display="none">` | 3, 2, 2, 8 | **0** | 3, 2, 2, 8 | **0** |
| not inserted in the document | 0 | 0 | 0 | 0 |

All three browsers count UTF-16 code units, for the other three strings too (U+00E9 1, the JP flag 4, Devanagari 2). `getComputedTextLength()` gives a real length wherever the characters are counted and 0 elsewhere. Firefox returns a zero `getBBox()` for text inside `defs`, `symbol`, `pattern` and `clipPath`; Safari and Chrome return the box. Lengths differ a little between browsers because of fonts (`abc` at 20px: 31.69 in Safari, 32.37 in Firefox, 32.38 in Chrome).

The whitespace results are in [../1261/](../1261/).
