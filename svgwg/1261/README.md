# svgwg#1261: getNumberOfChars(): "normalizing whitespace" is not defined, and a per-text-node count does not match browsers

Issue: https://github.com/w3c/svgwg/issues/1261
Spec: https://w3c.github.io/svgwg/svg2-draft/text.html#__svg__SVGTextContentElement__getNumberOfChars

Step 2 of `getNumberOfChars()` counts a text node's characters "after normalizing whitespace according to the value of the white-space property on its parent element", which is not defined anywhere. SVG's text layout algorithm decides which characters are addressable with CSS Text's white-space processing (collapsing, and trimming at the start and end of a line), across element boundaries: https://w3c.github.io/svgwg/svg2-draft/text.html#TextLayoutAlgorithm

## Page

The page lives with svgwg#1260: [../1260/probe-getnumberofchars-composed-never-rendered.html](../1260/probe-getnumberofchars-composed-never-rendered.html), table "Whitespace (all in the document)". The result files are in [../1260/results/](../1260/results/).

## Results

All on 2026-11-17. All controls passed. Spaces, tabs and line feeds are written as character references so they show.

| `<text>` content | text nodes, raw length | Safari 27.0 | Firefox 162 | Chrome 160 | addressable (CSS collapse and trim) |
|---|---|---|---|---|---|
| `a&#32;&#32;b` | 4 | 3 | 3 | 3 | 3 |
| `&#32;&#32;abc&#32;&#32;` | 7 | 3 | 3 | 3 | 3 |
| `&#32;&#32;&#32;` | 3 | 0 | 0 | 0 | 0 |
| **`a&#32;` then `<tspan>&#32;b</tspan>`** | **2 + 2** | **3** | **3** | **3** | **3** |
| `a&#9;b&#10;c` | 5 | **4** | 5 | 5 | 5 |
| `xml:space="preserve"`, `a&#32;&#32;b` | 4 | 4 | 4 | 4 | 4 |
| `white-space: pre`, `a&#32;&#32;b` | 4 | 4 | 4 | 4 | 4 |
| `white-space: pre`, `a&#10;b` | 3 | 3 | 3 | 3 | 3 |

The bold row separates the two readings: taken one text node at a time, `a&#32;` and `&#32;b` give 4 (each keeps its space) or 2 (each trimmed at its edges), never 3. All three browsers collapse the two spaces across the `tspan` boundary and count 3. Safari's 4 for the tab and line feed row is WebKit removing the line feed instead of turning it into a space: https://bugs.webkit.org/show_bug.cgi?id=278524
