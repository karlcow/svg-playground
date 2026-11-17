# svgwg#1255: getCharNumAtPosition(): the loop does not advance, skips the last character, and leaves glyph cell edges and overlaps undefined

Issue: https://github.com/w3c/svgwg/issues/1255
Spec: https://w3c.github.io/svgwg/svg2-draft/text.html#__svg__SVGTextContentElement__getCharNumAtPosition

The SVG 2 steps loop `While charnum < last` without ever increasing charnum, so read literally they never end and never look at the last character. They ask whether the point is "within the glyph cell", but "glyph cell" is not defined, and nothing says whether a point on the edge of a cell is inside it. When cells overlap, the steps keep the last match. The argument is a `DOMPointInit`, and the steps do not say what NaN, Infinity, z or w do.

## Page

| page | what it asks |
|---|---|
| [probe-getcharnumatposition-edges.html](probe-getcharnumatposition-edges.html) | `getCharNumAtPosition()` for 19 points on short texts in 10px Ahem: the centre of the last character, a one-character text, the left, top, bottom, right and shared edges of the glyph cells, two pairs of overlapping cells, a plain `{x, y}` object, no argument, NaN, Infinity, `w` not 1 and `z` not 0. Diagrams draw each text 8 times larger with its glyph cells and the tested points, labelled with this browser's answers. |

Ahem is embedded in the page and loaded from its bytes (Safari Technology Preview 256 does not show a user-installed Ahem to pages). With `font: 10px/1 Ahem`, `<text x="10" y="20">AB</text>` has A in x 10 to 20 and B in x 20 to 30, both in y 12 to 22. The page checks that `getExtentOfChar(0)` is exactly that before trusting any row.

Controls: the centre of A must give 0, a point far outside must give -1, x 29.9 must give 1 and x 30.1 must give -1.

## Results

From the files in [results/](results/). All on 2026-11-17. All controls passed.

```
        x=10                x=20                x=30
  y=12   +---------t----------+--------------------+
         |                    |                    |
         |         A          |         B          |
         l                    s                    r
         |                    |                    |
  y=22   +---------b----------+--------------------+
```

| point on `AB` | Safari 27.0 | Firefox 162 | Chrome 160 |
|---|---|---|---|
| centre of B, the last character (25, 17) | 1 | 1 | 1 |
| l, left edge (10, 17) | 0 | 0 | 0 |
| t, top edge (15, 12) | 0 | 0 | 0 |
| b, bottom edge (15, 22) | 0 | 0 | 0 |
| s, shared edge (20, 17) | **0** | 1 | 1 |
| r, right edge (30, 17) | 1 | **-1** | **2** |

Chrome's 2 is not a character of this text (it has 0 and 1).

| point (17, 17) on overlapping cells | Safari 27.0 | Firefox 162 | Chrome 160 |
|---|---|---|---|
| `<text x="10 15">AB</text>`: A 10 to 20, B 15 to 25 | 0 | 1 | 0 |
| `<text x="15 10">AB</text>`: A 15 to 25, B 10 to 20 | 0 | 1 | 0 |

Same in all three browsers:

| call | result |
|---|---|
| one-character text, centre of A | 0 |
| `{x: 15, y: 17}` (plain object) | 0 |
| no argument, on `<text x="-5" y="3">A</text>` (the default `{}` is the point 0, 0) | 0 |
| `{x: NaN, y: 17}` | -1 |
| `{x: Infinity, y: 17}` | -1 |
| `{x: 25, y: 17, w: 1.3}` (1 if w is ignored, 0 if x and y are divided by w) | 1 |
| `{x: 15, y: 17, z: 5}` | 0 |
