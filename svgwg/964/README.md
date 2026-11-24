# svgwg#964: setPathData() cases no WPT test covers

Issue: https://github.com/w3c/svgwg/issues/964 (also https://github.com/w3c/svgwg/issues/321 for the number format)
Spec: https://w3c.github.io/svgwg/specs/paths/#__svg__SVGPathData__setPathData

The SVG Paths module says only that `setPathData()` is "equivalent to calling setAttribute("d", ...) with the serialized path data". WPT `svg/path/interfaces/setPathData-*.html` already covers invalid content (unknown letter, wrong number of values, NaN, Infinity, `Z` with values, a first segment that is not a moveto, arc flags other than 0 and 1), every valid letter, empty input, MutationObserver and plain objects. This page measures five things none of those tests check.

**Status.** Not resolved. The proposal in #964 is to write the WPT behaviour into the spec.

## Page

| page | what it asks |
|---|---|
| [probe-964-setpathdata-gaps.html](probe-964-setpathdata-gaps.html) | Starting from `d="M 99 99"`, calls `setPathData()` with the input shown in each row, and records what is thrown, the `d` attribute and `getPathData()` afterwards. |

Controls: a valid list must change `d`; `setPathData(getPathData())` must not; `X` after `M` must give `M 0 0`, as WPT expects.

## Results

From the files in [results/](results/), 2026-11-24. Chrome Canary 160 with `chrome://flags/#enable-experimental-web-platform-features` and Firefox Nightly 163 passed the controls. Chrome Canary 160 without the flag and Safari Technology Preview 257 have no `setPathData()`; their runs are kept but say nothing.

| group | input | Chrome Canary 160 | Firefox Nightly 163 |
|---|---|---|---|
| 1. module grammar | `{type: "B", values: [45]}`, `"b"`, `{type: "R", values: [10, 10, 20, 0, 30, 10]}` after `M 0 0` | dropped, `d` = `M 0 0` | dropped, `d` = `M 0 0` |
| 1. markup | `d="M 0 0 B 45 L 10 10"` | `getPathData()` gives `M 0 0` | `getPathData()` gives `M 0 0` |
| 2. Web IDL | no `values`, no `type`, `values: 5`, `null`, `{}`, a `Symbol` | `TypeError`, `d` unchanged | `TypeError`, `d` unchanged |
| 2. Web IDL | `values: ["10", "20"]` | `M 10 20` | `M 10 20` |
| 2. Web IDL | `values: ["a", 0]` | `d` removed (NaN) | `d` removed (NaN) |
| 3. numbers | `0.1, 0.25` | `M 0.1 0.25` | `M 0.1 0.25` |
| 3. numbers | `-0, 0` | `M 0 0` | `M 0 0` |
| 3. numbers | `1e39, 0` (Infinity as a float) | `d` removed | `d` removed |
| 3. numbers | `1e-7, 0` | **`M 1.00000e-7 0`** | **`M 1e-7 0`** |
| 3. numbers | `0.1234567891, 123456789` | **`M 0.123457 1.23457e+8`**, then `getPathData()` gives 123457000 | **`M 0.123457 123457000`**, but `getPathData()` gives 123456792 |
| 4. arc radii | `A -10 10 0 0 1 20 20`, `A 0 0 0 0 1 20 20` | kept as written | kept as written |
| 5. after `Z` | `M 0 0 L 10 10 Z L 20 20` | kept | kept |

Neither browser accepts the bearing (`B`) or Catmull-Rom (`R`) commands that the SVG Paths module grammar still lists, in `setPathData()` or in markup. A malformed segment object throws a `TypeError` before anything changes. The only difference is how numbers are written into `d`: both keep six significant digits, Chrome then reads its own text back (so `123456789` becomes `123457000`), while Firefox keeps the exact float and its `d` text disagrees with `getPathData()`.
