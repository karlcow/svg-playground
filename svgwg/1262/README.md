# svgwg#1262: remove `accessKey-value` from `begin` and `end` in SVG Animations

Issue: https://github.com/w3c/svgwg/issues/1262
Spec: https://w3c.github.io/svgwg/specs/animations/#AccessKeyValueSyntax
WebKit bug: https://bugs.webkit.org/show_bug.cgi?id=332075

SVG Animations still lists `accessKey(character)` as a `begin` and `end` value: the animation starts or ends when the user types that character. No browser does that. Firefox removed it in Firefox 59 (https://bugzilla.mozilla.org/show_bug.cgi?id=1423098). WebKit and Blink recognise the lowercase spelling `accesskey(` and never connect it to the keyboard; the spec spelling `accessKey(` is treated as an ordinary event name.

## Page

| page | what it asks |
|---|---|
| [probe-smil-accesskey.html](probe-smil-accesskey.html) | 16 automatic rows and 4 keyboard rows, each an inline `<svg>` with `<set attributeName="width" to="60">`. Parsing: does the rest of a `begin` list survive an `accessKey` value? Script events: does `new Event('accessKey(a)')` start or end the animation? Second interval: does a dead `accesskey(a)` in `end` change whether a later interval runs? Keyboard: does pressing `a` do anything? Each row gives the result predicted from the engines' source. |

Controls: `begin="1s"` starts at 1 (must not change), `begin="foo"` becomes active when `foo` is dispatched (must change), and in the keyboard section a `keydown` listener on `document` has to see the `a` key (must change). The page waits for the `load` event before inserting rows: WebKit starts the animation clock of an inline `<svg>` at load, and a row started earlier records a begin time without being drawn.

To run the keyboard rows, press "Start keyboard test", then press `a`.

## Results

From the files in [results/](results/). All on 2026-11-18. All controls passed, and every row matched the prediction from source.

| Case | Safari 27.0 | Chrome 160 | Firefox 162 |
|---|---|---|---|
| `begin="accessKey(a)"`, user presses `a` | nothing | nothing | nothing |
| `begin="accesskey(a)"`, user presses `a` | nothing | nothing | nothing |
| `begin="0s" end="accessKey(a)"`, user presses `a` | keeps running | keeps running | keeps running |
| `begin="accessKey(a); 1s"` and `begin="1s; accessKey(a)"` | start at 1s | start at 1s | start at 1s |
| `begin="accessKey(a)"`, script dispatches `new Event('accessKey(a)')` | **starts** | **starts** | nothing |
| `begin="accessKey(a) + 2s"`, same event | **starts 2s later** | **starts 2s later** | no interval |
| `begin="accesskey(a)"`, event `accesskey(a)` | nothing | nothing | nothing |
| `begin="0s" end="accessKey(a)"`, event `accessKey(a)` | **ends** | **ends** | keeps running |
| `begin="0s; 0.4s" end="accesskey(a); 0.2s"`, at 0.8s | not running | **running** | not running |
| same with `end="foo; 0.2s"` (reference) | running | running | running |
| same with `end="0.2s"` (reference) | not running | not running | not running |

A real key press does nothing anywhere. The camelCase spelling is an ordinary event name in Safari and Chrome, so a script event with that name starts or ends the animation. Chrome alone runs the second interval: Blink counts the dead lowercase condition as an end event, which allows an interval with no end.

Two more rows, `begin="ACCESSKEY(a)"` and `begin="r.accessKey(a)"`, start in Safari and Chrome and not in Firefox. That is not about `accessKey`: Firefox requires event names and element ids in `begin` and `end` to be valid XML names, so it rejects any name with parentheses. Safari and Chrome accept any string.

The WebKit patch for bug 332075 removes the condition, so a WebKit build with it differs from the predictions on three rows (`event_camel`, `event_offset`, `end_event_camel`) and matches Firefox there.
