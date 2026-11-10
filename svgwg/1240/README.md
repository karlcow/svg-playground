# svgwg#1240: percent-encoded fragment in a URL reference

Issue: https://github.com/w3c/svgwg/issues/1240 (split from https://github.com/w3c/svgwg/issues/1170)
Spec: https://w3c.github.io/svgwg/svg2-draft/linking.html#processingURL-target

`fill="url(#%66%6f%6f)"` finds `id="foo"` in every browser: the fragment is percent-decoded before it is compared to an id. The spec only says "a matching element". This page asks the harder case: what if the document also has an element whose id really is `%66%6f%6f`?

## Page

| page | what it asks |
|---|---|
| [probe-url-fragment-both-ids.html](probe-url-fragment-both-ids.html) | Which element `url(#%66%6f%6f)` and `<use href="#%66%6f%6f">` find when `id="foo"`, `id="%66%6f%6f"` or both exist, and whether the fragment is decoded once or twice. |

Each case is a small SVG document drawn through an `img` into a canvas. The gradient (or rect) with `id="foo"` is green, the one with `id="%66%6f%6f"` is blue, and red means nothing was found.

## Results

From the files in [results/](results/). The cell says which element was used.

| case | Safari Technology Preview 256 | Firefox 162 | Chrome 159 | WebKit trunk (MiniBrowser, 8173ee0b) | WebKit 22626.1.10 |
|---|---|---|---|---|---|
| `url(#foo)`, only `id="foo"` (control) | `foo` | `foo` | `foo` | `foo` | `foo` |
| `url(#%66%6f%6f)`, only `id="foo"` (control) | `foo` | `foo` | `foo` | `foo` | `foo` |
| `url(#bar)`, no such id (control) | nothing | nothing | nothing | nothing | nothing |
| `url(#%66%6f%6f)`, only `id="%66%6f%6f"` | nothing | nothing | nothing | nothing | nothing |
| `url(#%66%6f%6f)`, both ids, `%66%6f%6f` first | `foo` | `foo` | `foo` | `foo` | `foo` |
| `url(#%66%6f%6f)`, both ids, `foo` first | `foo` | `foo` | `foo` | `foo` | `foo` |
| `url(#%2566%256f%256f)`, both ids | `%66%6f%6f` | `%66%6f%6f` | `%66%6f%6f` | `%66%6f%6f` | `%66%6f%6f` |
| `<use href="#%66%6f%6f">`, both ids, `%66%6f%6f` first | `foo` | `foo` | `foo` | `foo` | `foo` |
| `<use href="#%66%6f%6f">`, both ids, `foo` first | `foo` | `foo` | `foo` | `foo` | `foo` |

All on 2026-11-10 except WebKit 22626.1.10 (the Safari 27.3 engine, in an embedded view, 2026-11-09). All controls passed.

Every engine decodes the fragment once and compares only the decoded text. None tries it as written first, which is what HTML does for links into an HTML document (https://html.spec.whatwg.org/multipage/browsing-the-web.html#select-the-indicated-part). So an element whose id contains `%66` can only be reached by writing the `%` as `%25`.
