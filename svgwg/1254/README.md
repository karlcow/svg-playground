# svgwg#1254: selectSubString() throws when the substring reaches the last character, and builds its range on the wrong node

Issue: https://github.com/w3c/svgwg/issues/1254
Spec: https://w3c.github.io/svgwg/svg2-draft/text.html#__svg__SVGTextContentElement__selectSubString

SVG 2 says "Let end = charnum + nchars. If charnum ≥ count or end ≥ count, then throw an IndexSizeError", so a substring can never include the last character. It then builds the selection on the boundary points (text element, charnum) and (text element, end), but a DOM offset on an element counts its children, not its characters. SVG 1.1 cut nchars at the end and threw only when charnum was too large. Both rules came with the 2015 rewrite of the method in terms of the Selection API.

## Page

| page | what it asks |
|---|---|
| [probe-selectsubstring-range-limits.html](probe-selectsubstring-range-limits.html) | For 9 calls to `selectSubString()` on `<text>hello</text>` and `<text>Hello <tspan>world</tspan></text>`: does it throw, what does `getSelection().toString()` give, where do the anchor and focus sit (node and offset), and what is `getSelection().direction`. Each row says whether the result matches SVG 1.1 or SVG 2 as written. |

Controls: `selectSubString(1, 3)` must select `ell` (the method works at all), a range built by hand on the Text node must select `hello`, and `range.setStart(textElement, 4)` on an element with 2 children must throw IndexSizeError (the DOM rule alone, no SVG involved).

## Results

From the files in [results/](results/). All on 2026-11-14. All controls passed.

On `<text>hello</text>`, the three browsers give the same answer on every row:

| call | SVG 2 as written | Safari 27.0, Firefox 162, Chrome 160 |
|---|---|---|
| `selectSubString(0, 5)` | IndexSizeError | `hello` |
| `selectSubString(1, 100)` | IndexSizeError | `ello` |
| `selectSubString(4, 1)` | IndexSizeError | `o` |
| `selectSubString(1, -1)` (nchars is 4294967295) | IndexSizeError | `ello` |
| `selectSubString(0, 0)` | empty | empty |
| `selectSubString(5, 0)` | IndexSizeError | IndexSizeError |
| `selectSubString(-1, 0)` (charnum is 4294967295) | IndexSizeError | IndexSizeError |

On `<text>Hello <tspan>world</tspan></text>`:

| call | SVG 2 as written | Safari 27.0 | Firefox 162 | Chrome 160 |
|---|---|---|---|---|
| `selectSubString(1, 1)` | `world` (child offsets 1 to 2) | `e` | `e` | `e` |
| `selectSubString(4, 5)` | IndexSizeError | `o wor` | **empty** | `o wor` |

Every browser puts both ends of the selection in the Text nodes, for example (`Hello `, 4) to (`world`, 3), never on the `<text>` element. Firefox's empty selection across the `tspan` (collapsed at (`Hello `, 4)) looks like a Firefox bug, separate from the spec question.

`getSelection().direction` after a non-empty selection: `forward` in Firefox, `none` in Safari and Chrome. SVG 2 says "Set the selection's direction to forwards".
