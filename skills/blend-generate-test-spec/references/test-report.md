# One editable report with TC blocks

`test-report@2.0.0` has exactly two localized sheets: Overview and Testcases. VI is the default. Preserve older schema/bytes/results; migration needs an explicit request.

The source workbook is self-documenting: Testcases contains one visible placeholder block labeled as a layout example, never a real testcase or result. The generator removes every preview row from its in-memory copy before projecting source cases, then replaces the template note with run instructions. Generated reports must contain zero placeholder/sample values. Template preview data never feeds counts or checker decisions.

## Layout and source

Each complete TC ID/title has a separate status row immediately below. Show screen/function beside `screen_relative_path`, a verified relative URL without domain. Use `unknown` for unverified routes, or `not-applicable` only for a verified non-UI case; never infer a route from a name. Unknown paths remain visible completion gaps.

Use four sections: test conditions, actions, expected results and actual results. Present technical labels in a bold label column and values beside them. Action labels are left-aligned localized text: `Step 1`, `Step 2`, … in VI and `ステップ 1`, `ステップ 2`, … in JA; action sentences remain normal text. Do not bold full procedural sentences. Display the final reset as the bold localized text label `Reset` / `リセット`, not an icon. Left-align all Testcases text and vertically center all visible block text, including title, labels, bullets, actions, expected, status and variant rows. Vietnamese reader text starts sentence case; verified identifiers, URLs and literals stay exact. A source list marker (`-`, `+`, `*` or `•`) is presentation syntax: strip it before adding exactly one workbook bullet. XLSX/Google Sheets does not render Markdown inline code or bold, so display `` `identifier` `` as `[identifier]`, preserve every character inside the inline-code token (for example `` `**24` `` becomes `[**24]`), and remove `**` only when it is Markdown emphasis outside code. Emit no literal backticks, Markdown emphasis markers outside bracketed technical tokens or doubled bullet markers in generated visible cells. Do not use yellow fills; editable status/actual/image and run inputs use restrained light-neutral fill plus borders. Do not show standalone readiness/expected-authority lines in every TC. Keep their semantics in source/checking. Keep decisive actor/data/configuration/trigger/observation, assertions, preservation, variant differences and the missing-proof portion of gaps. Gap impact/next-check metadata remains in source/checking. Do not show generic proof prose, per-TC eligible-count footers or back-to-overview rows.

One result location per variant. Single-variant header status is editable; multi-variant header status is derived and each variant has its own status/actual/image slot. Every status dropdown uses one compact, unmerged cell beside its label; it must not span the full content width because Excel and Google Sheets anchor the popup to that cell. The visible report has no link/defect input and no image-caption input. Record failure/block/skip reason and next action in Actual, using `[identifier]` for technical names rather than Markdown syntax. Overview links to complete TC blocks and separates case/variant totals from preparation/execution. No hidden dataset or third evidence sheet.

New `test-cases@1.1.0` sources include screen_relative_path. Frozen 1.0.0 inputs remain readable with unknown routes, without inherited results. Scope/data remain 1.0.0; JA/VI identity, routes and basis/readiness must agree.

## Generate and enter

```text
python scripts/export_report.py --source-dir DESIGN --output NEW-REPORT.xlsx --language vi
python scripts/check_report.py --source-dir DESIGN --report NEW-REPORT.xlsx --language vi --phase in-progress
```

Use existing declared Python dependencies, never install automatically. Export refuses every existing path. Enter results in the same file; a new run/expected requires an explicitly requested new path. Checking only reads and never repairs or regenerates.

Actual, image areas and run/build/environment/tester/time start blank; status starts localized NOT RUN. Execution time includes timezone. Recorded text stays literal; pasted formulas are rejected. Non-PASS actual text includes the observed result, reason and next action. Preserve observations and do not alter expected to fit a result.

## Evidence images

Anchor static PNG/JPEG at column A of the owning variant's reserved image row. Increase that row's height to fit evidence. Multiple images can share the reserved area only when their placement remains clear; each image still needs its own digest/review. The report does not show a caption field, but saved image alternative text and transient review metadata remain available for privacy/access review. Arbitrary row insertion, sorting individual rows, changed merges or moved inputs are not supported by the strict XLSX checker.

Inspect pixels, metadata and saved alternative text. Complete screenshot reviews have case_id, variant, saved-byte sha256, caption, reviewed_by, timezone-bearing reviewed_at and actual source. Alternative text must match the designated caption. No invented image, result or attestation.

## Counts and read-only checking

Counted PASS/FAIL needs Confirmed + Ready, exact localized status and actual nonempty after Unicode whitespace trimming. Screenshots are supporting evidence but are not required for the numeric count. PASS rate is eligible PASS / eligible PASS+FAIL; no denominator means no data. Any eligible FAIL makes case FAIL; every required variant eligible PASS makes PASS; all SKIPPED is SKIPPED; otherwise BLOCKED, all NOT RUN, or incomplete. PASS+SKIPPED is incomplete.

Checker compares immutable source/formulas/navigation/merges, validates inputs, metadata/privacy/relationships and image bindings. Hidden content and opaque unsupported package entries remain rejected. Workbook privacy setting does not certify image pixels or access. Explicit clipping fails; estimated wrapping needs native visual inspection. Checking is not a render certificate.

Complete checking takes genuine JSON stdin with closure_confirmation, evidence_access and screenshots. Closure: closed_by, timezone-bearing closed_at, source, audience. Access: url, audience, verified_by, timezone-bearing verified_at, method (human-attestation or recipient-session), source. Image fields are above. Missing routes/results/reasons/closure/access/image review prevent completion. Closed reports can retain failure/skip and do not prove release.

## Native Google Sheets

Prefer conversion before QA: generate blank XLSX, convert to native Sheets, verify native layout/formulas/IDs/links, then record results and add native images in that same Sheet. Avoid two result copies. Conversion/creation/sharing needs explicit external-task authorization.

The shipped checker is XLSX-only. Do not assume Excel metadata, links, wrapping or images survive conversion; native verification remains a separate gap until observed. No automatic upload, Apps Script, application tests or publication follows. Before delivery, render all changed sheets, recalculate/save/reopen in the available engine and disclose unverified native conversion/readability tests.
