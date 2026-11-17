# svgwg#1258: getRotationOfChar() is defined as the advance direction, but engines and WPT return the glyph's rotation

Issue: https://github.com/w3c/svgwg/issues/1258 (the `emoji_then_x` case also serves https://github.com/w3c/svgwg/issues/537)
Spec: https://w3c.github.io/svgwg/svg2-draft/text.html#__svg__SVGTextContentElement__getRotationOfChar

SVG 2 defines the result as "the angle in degrees that represents the direction of the cluster's advance", taking into account "the direction of the character". Read literally, that is 180 for right-to-left text and 90 for an upright glyph in vertical text. The sentence is the one getEndPositionOfChar uses, where the advance direction is what is wanted. SVG 1.1 returned the glyph's rotation, without the turn added by glyph-orientation.

## Page

| page | what it asks |
|---|---|
| [probe-getrotationofchar-readings.html](probe-getrotationofchar-readings.html) | `getRotationOfChar(index)` in 18 cases: right-to-left text, vertical text (upright, sideways, `text-orientation`, `glyph-orientation-vertical`), a `textPath` drawn right to left, and composed characters (a combining accent, Hebrew niqqud, a Devanagari vowel sign, the two halves of an emoji) measured on their second index. Each row gives what three readings predict: the glyph's rotation, the advance direction (SVG 2 read literally) and SVG 1.1. |

Controls: horizontal `A` is 0 and `rotate="30"` is 30. Rotation does not depend on font metrics, so the page uses system fonts.

## Results

From the files in [results/](results/). All on 2026-11-17. All controls passed.

| `getRotationOfChar(index)` | glyph | advance | SVG 1.1 | Safari 27.0 | Firefox 162 | Chrome 160 |
|---|---|---|---|---|---|---|
| `<text direction="rtl">&#x05E9;</text>` | 0 | 180 | 0 | 0 | 0 | 0 |
| `<text direction="rtl" unicode-bidi="bidi-override">A</text>` | 0 | 180 | 0 | 0 | 0 | 0 |
| `<text direction="rtl" rotate="30">&#x05E9;</text>` | 30 | 210 | 30 | 30 | 30 | 30 |
| `月` in `writing-mode: vertical-rl` (upright) | 0 | 90 | 0 | 0 | 0 | 0 |
| `M` in `writing-mode: vertical-rl` (sideways) | 90 | 90 | 0 | 90 | 90 | 90 |
| `M` with `text-orientation: upright` | 0 | 90 | 0 | 0 | 0 | 0 |
| `M` with `glyph-orientation-vertical="0deg"` | 0 | 90 | 0 | 0 | **90** | **90** |
| `月` with `glyph-orientation-vertical="90deg"` | 90 | 90 | 0 | 90 | **0** | **0** |
| `A` on a `textPath` drawn right to left | 180 | 180 | 180 | 180 | 180 | 180 |
| U+0301 in `<text rotate="0 45 10">E&#x0301;X</text>`, index 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `X` in the same text, index 2 | 10 | 10 | 10 | 10 | 10 | 10 |
| U+0301 after a sideways `E` in vertical text, index 1 | 90 | 90 | 0 | 90 | 90 | 90 |
| U+05B8 in `<text direction="rtl" rotate="0 45">&#x05E9;&#x05B8;</text>`, index 1 | 0 | 180 | 0 | 0 | 0 | 0 |
| U+093E in `<text rotate="0 45">&#x0930;&#x093E;</text>`, index 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| second code unit of the emoji in `<text rotate="20 45 10">&#x1F600;X</text>`, index 1 | 20 | 20 | 20 | 20 | 20 | 20 |
| `X` in the same text, index 2 (`rotate` numbered by code point, as the spec says) | 45 | 45 | 45 | 45 | **10** | 45 |

All three browsers return the glyph's rotation. Firefox and Chrome ignore the `glyph-orientation-vertical` attribute, so they report the default orientation. The last row is about how `rotate` values are numbered (svgwg#537): Safari and Chrome by code point, as the spec says since 2018, Firefox by UTF-16 code unit.

The result files predict 10 for that last row: the first version of the page assumed `rotate` counts UTF-16 code units. The spec counts code points ("For the purposes of mapping text positioning attributes, the index is measured in Unicode code points", https://w3c.github.io/svgwg/svg2-draft/text.html#TermAddressableCharacter), so 45 is right. The page in this folder is fixed; the measured values in the files are unchanged.
