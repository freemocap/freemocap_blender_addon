# Source references

Register external sources that inform implementation or consequential claims in
`references.bib`. Use stable ASCII keys and cite them beside the claim, for example
`[@vrm0Specification]`.
Use Better BibTeX-compatible braced values. Each entry needs `title`, `author`
or `editor`, `url`, `urldate` (YYYY-MM-DD), `review` and `claim`.

`review` records what was inspected: `metadata`, `abstract`, `excerpt`,
`full-text` or `source-code`. State limitations, versions and inspected sections
in `note`; do not invent publication dates or asset licensing.

The offline validator and regression tests are reused from FreeMoCap Core's
existing citation tooling. Run from this repository:

```text
python tools/check_references.py
python -m unittest discover -s tools -p test_references.py
```

Generated `.test-artifacts` and third-party dependencies are excluded. Keep useful
background entries even when not currently cited; unknown cited keys are errors.
