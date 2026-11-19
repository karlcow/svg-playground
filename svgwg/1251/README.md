# svgwg#1251: internal consistency of element categories

Issue: https://github.com/w3c/svgwg/issues/1251
Spec: https://w3c.github.io/svgwg/svg2-draft/render.html#TermNeverRenderedElement
Filter Effects: https://drafts.csswg.org/filter-effects-1/#FilterElement

SVG 2 splits element types into never-rendered and renderable elements. `stop`, `view`, `filter` and the elements that live inside `filter` are in neither list. Being never-rendered has one effect: `display` has no effect on the element (https://w3c.github.io/svgwg/svg2-draft/render.html#VisibilityControl). Filter Effects already says that for `filter`, on the element itself and on any ancestor. This page measures what `display: none` does today on `stop` and `filter`.

Related: [svgwg/828](../828/) measures the computed `display` of the elements that are already never-rendered.

## Page

| page | what it asks |
|---|---|
| [probe-1251-display-on-stop-filter.html](probe-1251-display-on-stop-filter.html) | Each case is one SVG document drawn through an `<img>` (data URL) into a 100×100 canvas; the page reads one pixel and names its colour. `stop`: does a `display: none` stop still count in its gradient? `filter`: does a filter with `display: none` on itself, or on an ancestor, still apply? Lime means `display: none` had no effect. |

Controls: the same gradient twice (must give the same pixels), a blue stop (must differ from lime), a gradient with no stops (must be transparent, so "nothing painted" is a measurement), the filter without `display: none` (must be lime), and a rect with no filter (must be red).

`view` is not in the page. Fragment views (`#v`) were not applied to an SVG image drawn into a canvas in WebKit, with a data URL, a blob URL or `#svgView()`, so the control failed and the cases were removed. From the engines' source, all three find the view by its id and ignore `display`.

## Results

From the files in [results/](results/). All on 2026-11-19. All controls passed.

The browsers were preview builds: Safari Technology Preview 256, Chrome Canary 160 and Firefox Nightly 162. The version numbers in the table and in the file names come from their user agent strings.

Lime is the answer if `display` has no effect. Bold cells differ from it.

| Case | Safari 27.0 | Chrome 160 | Firefox 162 |
|---|---|---|---|
| `<stop offset="0" stop-color="lime" style="display: none"/>`, only stop | lime | lime | **nothing painted** |
| same with `display="none"` as an attribute | lime | lime | **nothing painted** |
| `<stop offset="0.5" stop-color="lime" style="display: none"/><stop offset="0.5" stop-color="blue"/>`, left edge | lime | lime | **blue** |
| `<filter id="f" style="display: none"><feFlood flood-color="lime"/></filter>` on a red rect | **red** | **nothing painted** | **red** |
| `<g style="display: none"><filter id="f">…</filter></g>` on a red rect | lime | lime | **red** |

Safari and Chrome keep a hidden `stop` in its gradient; Firefox drops it. With `display: none` on the `filter` itself, no browser applies the filter: Safari and Firefox draw the rect without it, Chrome does not draw the rect. With `display: none` on an ancestor of the `filter`, Safari and Chrome apply it and Firefox does not.

Existing bugs: WebKit https://bugs.webkit.org/show_bug.cgi?id=118376, Mozilla https://bugzilla.mozilla.org/show_bug.cgi?id=376027.
