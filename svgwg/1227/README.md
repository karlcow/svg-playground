# svgwg#1227: getPathData() must define how to normalize path data

Issue: https://github.com/w3c/svgwg/issues/1227
Spec: https://w3c.github.io/svgwg/specs/paths/#InterfaceSVGPathData

The SVG Paths module says `getPathData({normalize: true})` converts to `M`, `L`, `C` and `Z` "with the values adjusted accordingly", without an algorithm. The open question is how an elliptical arc becomes cubic curves: how many, and what happens with degenerate arcs.

**Status.** Not resolved. A spec PR is a TPAC action (2026-10-30).

## Page

| page | what it asks |
|---|---|
| [probe-1227-normalize-arcs.html](probe-1227-normalize-arcs.html) | Calls `getPathData({normalize: true})` on 13 `d` strings and records the segment types and values (rounded to 4 decimals). |

Controls: the method exists; `M 0 0 L 10 0` comes back unchanged; a quarter turn and three quarter turns give different numbers of curves.

## Results

From the files in [results/](results/), 2026-11-24. Chrome Canary 160 with `chrome://flags/#enable-experimental-web-platform-features` and Firefox Nightly 163 passed the controls. Safari Technology Preview 257 has no `getPathData()`.

| `d` | Chrome Canary 160 | Firefox Nightly 163 |
|---|---|---|
| `M 0 0 A 10 10 0 0 1 10 10` (quarter turn) | `M C` | `M C` |
| `M 0 0 A 10 10 0 1 0 20 0` (half turn) | `M C C` | `M C C` |
| `M 0 0 A 10 10 0 1 1 10 10` (three quarters) | `M C C C` | `M C C C` |
| `M 0 0 A 10 10 0 1 1 0.5 0` (almost a full turn) | `M C C C C` | `M C C C C` |
| `M 0 0 A 20 10 30 1 1 30 10` (x-axis rotation 30) | `M C C C` | `M C C C` |
| `M 0 0 A 1 1 0 0 1 10 0` (radii too small, scaled to 5) | `M C C` | `M C C` |
| `M 10 10 a 10 10 0 0 1 10 10` (relative) | `M C` | `M C` |
| `M 0 0 A 0 10 0 0 1 10 10` (one radius 0) | `M 0 0 L 10 10` | `M 0 0 C 5 5 5 5 10 10` |
| `M 0 0 A 0 0 0 0 1 10 10` (both radii 0) | `M 0 0 L 10 10` | `M 0 0 C 10 10 10 10 10 10` |
| `M 5 5 A 10 10 0 0 1 5 5 L 20 20` (end point is the start point) | `M 5 5 L 5 5 L 20 20` | `M 5 5 L 20 20` |

Where the types agree, the values agree too: the largest difference is 0.0001, the rounding of the probe. So both make one cubic per started quarter turn of the swept angle, with the same control points, and the x-axis rotation does not change the count. They differ only on the degenerate arcs: Chrome turns them into `L` and keeps the arc as a segment; Firefox draws a zero radius as a straight `C` and drops an arc that ends where it starts.
