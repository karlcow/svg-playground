# svgwg#1257: getSubStringLength(): "if nchars is negative" cannot happen

Issue: https://github.com/w3c/svgwg/issues/1257
Spec: https://w3c.github.io/svgwg/svg2-draft/text.html#__svg__SVGTextContentElement__getSubStringLength

SVG 2 says "If charnum is greater than the highest index assigned to a character or if nchars is negative, then throw an IndexSizeError". The IDL is `getSubStringLength(unsigned long charnum, unsigned long nchars)`, and Web IDL turns -1 into 4294967295 (https://webidl.spec.whatwg.org/#abstract-opdef-converttoint), so nchars is never negative. On an empty text there is no "highest index". This page asks what browsers do in these cases.

## Page

| page | what it asks |
|---|---|
| [probe-getsubstringlength-range-checks.html](probe-getsubstringlength-range-checks.html) | 10 calls to `getSubStringLength()` and `getComputedTextLength()` on `<text>abcd</text>` and on an empty `<text>`: nchars -1, 4294967295, past the end and 0; charnum at the last character, at the count and -1. |

Ahem is embedded in the page and loaded from its bytes, so every character is 10 long. Checks: the extent of `a` is 10 x 10; controls `getSubStringLength(0, 4)` is 40, `getSubStringLength(1, 1)` is 10 and `getComputedTextLength()` is 40.

## Results

From the files in [results/](results/). All on 2026-11-17. All controls passed. The three browsers give the same answer on every row:

| call | Safari 27.0, Firefox 162, Chrome 160 |
|---|---|
| `getSubStringLength(1, -1)` (nchars is 4294967295) | 30 |
| `getSubStringLength(1, 4294967295)` | 30 |
| `getSubStringLength(1, 100)` | 30 |
| `getSubStringLength(3, -1)` | 10 |
| `getSubStringLength(2, 0)` | 0 |
| `getSubStringLength(3, 1)` | 10 |
| `getSubStringLength(4, 0)` | IndexSizeError |
| `getSubStringLength(-1, 1)` (charnum is 4294967295) | IndexSizeError |
| empty `<text>`: `getSubStringLength(0, 0)` | IndexSizeError |
| empty `<text>`: `getComputedTextLength()` | 0 |
