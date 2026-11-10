# SVG Playground

Test pages, probes and examples for issues discussed by the [SVG Working Group](https://www.w3.org/groups/wg/svg/). Clone it, open a page in a browser, compare engines, change a case, add one.

This is not [web-platform-tests](https://github.com/web-platform-tests/wpt). Pages here explore a question while it is being discussed. Once the group has decided, the tests that encode the decision go to WPT.

## Layout

One folder per issue, named after the tracker and the issue number:

```
svgwg/1170/                     https://github.com/w3c/svgwg/issues/1170
  README.md                     the question, what each page measures, results so far
  probe-<topic>.html            a page that measures one thing and reports it
  results/
    run-<date>-<browser>-<version>-<probe>.json
csswg/<number>/                 https://github.com/w3c/csswg-drafts/issues/<number>
```

- The folder name is the number only, so it does not change when the issue title does. The issue title goes in the folder's README.
- An issue that has not been filed yet has no folder. File the issue first, add the folder, then link to it from the issue (a comment or an edit).
- A page that serves several issues lives in the folder of the first one; the others link to it from their README.

## Probes

A probe is a self-contained HTML page: no server, no build step, no external scripts. Open the file directly or through any static server.

Each probe:

- has at least one control that must change and one that must not, so a broken measurement shows itself instead of passing as a result;
- shows the markup or code of each case next to its result;
- writes its result as JSON into a `<pre id="json">` block, with `probe`, `user_agent`, `engine_hint`, `character_set` and `controls_passed`;
- has Copy and Download buttons. Download names the file `run-<date>-<browser>-<version>-<probe>.json`.

## Adding results

Run the probe, download the JSON, put it in the issue's `results/` folder, and open a pull request. Add a line to the results table in the issue's README. If `controls_passed` is `false`, the run says nothing about the question: keep the file if it helps to debug, but do not count it in the table.

Say how the browser was obtained when it is not a public release (a local build, a flag turned on).

## Contributing

Contributions are welcome from anyone. See [CONTRIBUTING.md](CONTRIBUTING.md) and [LICENSE.md](LICENSE.md).
