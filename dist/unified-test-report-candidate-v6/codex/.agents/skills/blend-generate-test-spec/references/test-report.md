# One editable test report

Generate one new `test-report@1.0.0` workbook per requested run/language. Enter observations in that file, check it and use the same file as the report. Its presentation is complete from the start; execution remains NOT RUN until actual results are recorded. There is no report-after-testing export.

## Generate and enter results

Resolve an interpreter with the declared dependencies; never install automatically. The [generator](../scripts/export_report.py), [canonical model](../scripts/report_model.py) and [renderer](../scripts/render_report.py) resolve their own bundled resources.

```text
python scripts/export_report.py --source-dir DESIGN --output test-report.vi.xlsx --language vi
python scripts/check_report.py --report test-report.vi.xlsx --source-dir DESIGN --language vi --phase in-progress
```

Replace `DESIGN` with the verified matching source directory. Relative paths resolve from the process cwd. VI is the default; use `ja` only for a requested JA workbook with matching JA Markdown. The generator refuses any existing output, including a file containing results. New run/revision requests use new paths; checking never regenerates the workbook. Old schemas require separate migration authorization.

Both report CLIs use UTF-8 for stdin, stdout and stderr, including on Windows with a legacy console codepage. Encode JSON stdin and decode captured output explicitly as UTF-8; no global environment or terminal setting change is required.

Templates and newly generated workbooks enable workbook-level `filterPrivacy=1`, corresponding to Excel's RemovePersonalInformation setting. No global Excel preference is changed. The setting helps prevent personal metadata being saved but is not a guarantee: the checker requires it and independently inspects the actual saved package, including all XML attributes, namespace values and decoded locators. An editor that drops the setting or adds private metadata produces a finding; the checker never cleans or replaces that workbook.

Summary contains function/scope/revision, editable run/build/environment/tester/period fields and formulas for progress, outcomes and remaining work. Tests has exactly seven columns: case/variant identity, screen/function, conditions/actions, expected, actual, status, evidence/defect. Enter observations, choose the localized status and record evidence or a reason in the indicated input cells. Each case/variant has one result location. Details is present only for essential long content or reviewed images and links to its owning test; it never duplicates actual-result input.

Keep the tester and a timezone-bearing execution time in the summary inputs; for example, `2026-10-04 09:00 +07:00` is a format example, not a recorded result. Record non-PASS reasons in the evidence/defect column beside the affected result. Sort complete result rows so identity, actual, status and evidence remain together. Summary counts and Details return links follow the stable case/variant identity; verify those associations when checking the saved report.

Preserve exact IDs, conditions, expected and literal observations. Do not translate recorded observations automatically or alter expected to match the result. NOT RUN is not PASS; FAIL/BLOCKED/SKIPPED retain defects, reasons and untested scope. Case IDs, variants within a case, projected result identities and case groups must remain unambiguous under case-insensitive matching. Collisions are rejected before generation; IDs are never silently rewritten. Keep the source design revision with the report; changed source must not silently inherit results.

## Recorded counts and case outcomes

Workbook formulas and the checker use the same minimum for a recorded PASS/FAIL judgment: the exact localized dropdown status, Confirmed expected basis, Ready preparation, actual text that remains nonempty after Unicode whitespace trimming, and an explicit evidence token on the first line of column G. That line is a standalone URL beginning with lowercase `https://`, without whitespace or control characters; its authority before `/`, `?` or `#` contains a dot with characters on both sides and no `@`. Put reasons and next actions on subsequent lines. Prose-only evidence, a URL only on a later line or a hyperlink target without the visible token does not satisfy this count rule.

These are recorded judgments, not verified access or a privacy certificate. The checker separately validates actual URLs, the whole saved package and recipient-access attestations. A token meeting the count minimum can still fail those stricter checks. Unknown expected or unavailable preparation cannot become confirmed requirement PASS.

- Recorded judgments = eligible recorded PASS + FAIL.
- Pass rate = eligible recorded PASS / recorded judgments.
- Recorded-judgment coverage = recorded judgments / all scenarios, including scenarios not yet run or not ready.
- Remaining scenarios = all scenarios minus eligible recorded PASS. A zero rate denominator displays no data, never 100%.

Case totals are separate from scenario totals. Case aggregation applies in order: any eligible recorded FAIL → FAIL; every required scenario eligible and recorded PASS → PASS; every scenario SKIPPED → SKIPPED; otherwise any BLOCKED → BLOCKED; every scenario NOT RUN → NOT RUN; other incomplete mixtures → INCOMPLETE. Thus PASS/SKIPPED is incomplete, not PASS or NOT RUN. The derived incomplete label is `Chưa đủ kết luận` / `判定未完了`; it is not an additional dropdown status. The five input states remain unchanged.

If generation reports an Excel formula-size limit, preserve the source and report the limit. Do not silently omit cases, divide the run or create extra workbooks; any different run scope requires an explicit request.

## Read-only checking

The [checker](../scripts/check_report.py) compares the report with its matching source and inspects identities, formulas, status values, observations, links and the whole saved XLSX, including properties, relationships and media. It returns findings without saving, repairing statuses, removing images or producing a replacement workbook. In-progress gaps remain visible; invalid schema, pasted status, formulas or identity changes are failures.

Before checking, clear active filters, unhide all rows/columns and save the same workbook. Rows hidden by a filter are subject to the same visibility check as manually hidden rows.

Native Excel may remove optional quotes around a simple sheet name. Checking accepts that equivalent spelling only for exact known simple sheet names outside Excel string literals; function, range, ID and literal changes remain invalid. Width-based text-height estimates appear as advisory `layout_notes`, requiring visual inspection rather than asserting clipping. Explicit-line/font minimum height and hidden-row checks still reject definite visibility problems. A successful structural check does not certify readable layout.

Native Excel can also save opaque printer-settings binary entries. Their contents are not currently supported for privacy inspection, so the checker rejects them even when the workbook privacy setting is enabled. Preserve the file and disclose this limitation; do not silently remove the binary or waive the guard to obtain a complete result.

```text
python scripts/check_report.py --report test-report.vi.xlsx --source-dir DESIGN --language vi --phase complete
```

Complete checking consumes one JSON object through structured stdin: `closure_confirmation`, `evidence_access`, `screenshots`. Use the runtime's argument-array/stdin facility, never concatenate untrusted text into shell code. These are actual typed attestations, not a persisted manifest or values generated to satisfy the checker.

| Record | Required fields |
| --- | --- |
| `closure_confirmation` | `closed_by`, timezone-bearing ISO `closed_at`, `source`, exact intended `audience` |
| `evidence_access` | Each record has `url`, exact `audience`, `verified_by`, timezone-bearing ISO `verified_at`, `method`, `source`; method is `human-attestation` or `recipient-session` |
| `screenshots` | Each record has `case_id`, `variant`, `sha256` of saved image bytes, saved alternative-text `caption`, `reviewed_by`, timezone-bearing ISO `reviewed_at`, `source` |

Supply image-review records for images actually present using the checker schema. Review image pixels for private content as well as metadata; metadata inspection cannot certify pixels. No image is silently removed. Access evidence must cover the exact shared evidence/defect URLs and intended audience. An authenticated agent alone does not prove recipient access. Missing actual results, reasons, closure, access or image review prevents a complete conclusion; it never authorizes upload, permission changes or fabricated proof.

For a reviewed image, use the canonical localized Details headers and a caption row with the exact case/variant identity, localized evidence label and caption in columns A–C; anchor the image at column C of the following row. Its saved alternative text must match that caption. Bind the screenshot review to the SHA256 of its saved `xl/media` bytes. This adds evidence to the same report and does not create another result input or workbook.

Evidence URLs must be shared HTTPS links. Decoded path/query/fragment components are checked for private locators and credentials without changing the original URL. Literal entities and intentional line breaks remain observations, not markup to decode again. Do not embed raw source files, local paths, preparation history or hidden provenance/helper datasets in the workbook.

URL tokens extend to the next whitespace or end of text. Literal parentheses, brackets and adjoining punctuation remain part of the URL for privacy checks and exact recipient-access matching; the checker never trims them to match a shorter receipt. Keep the first evidence line as the complete standalone URL and separate prose from other links with whitespace. A URL alone supplies no non-PASS reason; enter the reason and next action on subsequent lines.

## Handoff and proof limits

Use formal, direct workbook wording without references to its audience, internal copies, final export or authoring history. Reconcile every case/variant and value against source, inspect all used sheets, navigation, input cells, wrapping and print layout, and actually recalculate/save/reopen in an available spreadsheet engine. Formula strings and successful checking do not establish engine behavior, native Excel usability, actual access or application test execution.

Report the same file path, requested language, matching basis, actual checks and remaining gaps. Preserve historical workbooks, distributions, evidence and RC-001. Generation/checking does not run application tests or SQL, activate skills, publish or release anything.
