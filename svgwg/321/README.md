# svgwg#321: Serialization format for path strings

Issue: https://github.com/w3c/svgwg/issues/321
Spec: https://w3c.github.io/svgwg/svg2-draft/paths.html#TheDProperty

How should path data be written out when it is read back: absolute or relative commands, which separators, with or without repeated command letters, and how many digits? The thread (2017 to 2023) has no conclusion. WPT `svg/path/property/serialization.svg` expects absolute commands in the computed value; nothing tests the number format or the syntax shortcuts discussed in the thread.

**Status.** Not resolved.

## Page

| page | what it asks |
|---|---|
| [probe-321-d-serialization.html](probe-321-d-serialization.html) | 16 path strings (number formats, and the shortcuts from the thread), each read as the computed value of the `d` attribute, and as the specified and computed value of `d: path(...)` in a style. |

All readings use `getPropertyValue("d")`, as WPT does. Controls: no `d` must give `none`; `M 0 0 L 10 10` must come back unchanged.

In WebKit the `d` property is behind the `CSSDPropertyEnabled` feature flag: on in Safari Technology Preview, off in Safari releases. Without it every reading is empty.

## Results

Only one run so far: the system WebKit of macOS 27.3 (the Safari 27.3 engine; its user agent string says Version/26.4) in an embedded view, with `CSSDPropertyEnabled` turned on, 2026-11-24. Runs in Safari Technology Preview, Firefox Nightly and Chrome Canary to come.

| input | computed | specified |
|---|---|---|
| `m100,200h400V300` | `path("M 100 200 H 500 V 300")` | `path("m 100 200 h 400 V 300")` |
| `m5,16 33,44` | `path("M 5 16 L 38 60")` | `path("m 5 16 l 33 44")` |
| `M5,16 33,44` | `path("M 5 16 L 33 44")` | same |
| `M 0 0 a10 10 0 1020 0` | `path("M 0 0 A 10 10 0 1 0 20 0")` | `path("M 0 0 a 10 10 0 1 0 20 0")` |
| `M 5 5 l 10 10 z l 1 1` | `path("M 5 5 L 15 15 Z L 6 6")` | `path("M 5 5 l 10 10 Z l 1 1")` |
| `M 0.1234567891 123456789` | `path("M 0.123457 1.23457e+8")` | same |
| `M 1e-7 0` | `path("M 1e-7 0")` | same |
| `M -0 0`, `M 10.0 20.00`, `M .5 -.5`, `M 1E2 0` | `0 0`, `10 20`, `0.5 -0.5`, `100 0` | same |

Computed values use absolute commands, specified values keep relative ones. Omitted command letters are written out, separators become single spaces, `z` becomes `Z`, and numbers keep six significant digits.

For comparison, the number format of `setPathData()` (which writes the `d` attribute) is in [../964/](../964/): Chrome writes `1e-7` as `1.00000e-7` there.
