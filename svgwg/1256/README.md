# svgwg#1256: "Find the typographic character for a character": wrong variable, a cut sentence, and a loop that never runs

Issue: https://github.com/w3c/svgwg/issues/1256
Spec: https://w3c.github.io/svgwg/svg2-draft/text.html#TermFindTypographicCharacterForCharacter

The helper used by `getStartPositionOfChar()`, `getEndPositionOfChar()`, `getExtentOfChar()` and `getRotationOfChar()` skips characters that "do not correspond to a typographic character". Every character is part of a typographic character, so the skip never happens, unless it was meant for characters that are not drawn. Characters after the end of a `textPath` are that case. This page asks what the four methods return for them.

## Page

| page | what it asks |
|---|---|
| [probe-textpath-undrawn-characters.html](probe-textpath-undrawn-characters.html) | `getNumberOfChars()`, and for indexes 0 to 4 `getStartPositionOfChar()`, `getEndPositionOfChar()`, `getExtentOfChar()` and `getRotationOfChar()`, on `ABCD` in 10px Ahem along a path 20 units long (A and B fit, C and D are not drawn) and along a path 100 units long (all drawn). Both texts are drawn 4 times larger next to their markup. |

Ahem is embedded in the page and loaded from its bytes. Checks: on the long path the extent of A is 10 x 10 at x 10 and `getNumberOfChars()` is 4; on the short path A starts at (10, 50) and B at (20, 50); index 4 throws IndexSizeError on both.

## Results

From the files in [results/](results/). All on 2026-11-17. All checks passed.

```
index                 0       1       2       3
character             A       B       C       D
drawn?                yes     yes     no      no       (the path ends after B)
```

| short path | Safari 27.0 | Firefox 162 | Chrome 160 |
|---|---|---|---|
| `getNumberOfChars()` | **2** | 4 | 4 |
| `getStartPositionOfChar(2)`, C | IndexSizeError | (25, 50) | (0, 0) |
| `getStartPositionOfChar(3)`, D | IndexSizeError | (25, 50) | (0, 0) |
| `getExtentOfChar(2)` | IndexSizeError | 10 x 10 at (25, 42) | 0 x 0 at (0, 0) |
| `getRotationOfChar(2)` | IndexSizeError | 0 | 0 |
| on the long path, start of C | (30, 50) | (30, 50) | (30, 50) |

Safari does not count C and D, although `getNumberOfChars()` counts characters "regardless of whether they will be rendered", so they are out of range. Firefox puts both at the end of the path. Chrome gives them no position (zeros). No browser skips from C to D.

The `reading_for_index_2` field in the three result files is wrong: that version of the page took equal values for C and D as "skipped to D", but they are equal because both are zeros (Chrome) or both sit at the end of the path (Firefox). The page in this folder is fixed; the measured values in the files are right.
