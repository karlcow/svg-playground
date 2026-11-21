# svgwg#1186: getPathSegmentAtLength() should tell which segment it returned

Issue: https://github.com/w3c/svgwg/issues/1186
Spec: https://w3c.github.io/svgwg/specs/paths/#__svg__SVGPathElement__getPathSegmentAtLength
Spec change: https://github.com/w3c/svgwg/pull/1268

`getPathSegmentAtLength()` returns a copy of the segment, with only `type` and `values`. To edit that segment, authors have to find it again in `getPathData()`, which fails when the path repeats a segment (common with relative commands). The SVG WG resolved on 2026-11-10 (https://www.w3.org/2026/11/10-svg-minutes.html#fc38) to add a member that gives the segment's position in the path data. PR #1268 adds an optional `index` member to `SVGPathSegment`. Only `getPathSegmentAtLength()` sets it, as the position in `getPathData()` without normalization. `getPathData()` leaves it unset and `setPathData()` ignores it.

## Page

| page | what it checks |
|---|---|
| [getPathSegmentAtLength-index.tentative.html](getPathSegmentAtLength-index.tentative.html) | 12 tests for `index`: a segment that has identical earlier segments, boundaries, clamping, arcs and H/V (the index must not follow normalization), closepath and interior MoveTo, implicit repeated commands, no `index` from `getPathData()`, `setPathData()` ignoring it, and editing the segment through `setPathData()`. |

This page is a web-platform-tests test, not a probe. It uses testharness.js and `support/getPathData-helpers.js` from `svg/path/interfaces/` in WPT, so it runs from a WPT checkout (`./wpt serve`), not from this folder. It goes to `svg/path/interfaces/` once PR #1268 has merged. The `.tentative` suffix comes off then.

## Results

No browser implements `index` yet. Firefox, which ships `getPathSegmentAtLength()`, is expected to pass only "getPathData() does not set index" and "setPathData() ignores index".
