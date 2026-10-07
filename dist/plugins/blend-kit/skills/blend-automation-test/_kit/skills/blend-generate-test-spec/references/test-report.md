# One editable report with TC blocks

The sole workbook format is `test-report@2.5.0`. New source uses `test-cases@1.3.0`; supported older source grammars, including RC-0011.1, remain read-only inputs with original IDs/oracles. Generation uses the current root asset pair; checking/writeback reject older workbook versions without rewriting. Read the [shared automation contract](../../../shared/automation-testing.md).

## Customer report 2.5

Use `export_report.py --source-dir DESIGN --output NEW.xlsx --language vi` for customer reading of the same execution workbook. Registered type is test-report, family test-report@2.5.0, VI/JA assets. Exactly two sheets: Overview and Testcases. This is the default and only workbook layout.

Each situation is understandable at one place: decisive conditions/data, concrete actions, branch-specific Expected beside Actual/Status, material timing/preservation and blocked/difference reasons. Human descriptions precede stable codes (description in Inputs, original Variant ID unchanged). Same procedure/data variations use a table; differing procedure/initial state remains independently understandable. Keep sufficient content rather than blanket shortening. No sample/review notes, preparation/readiness label or default technical appendix. Readiness/oracle/rights/eligibility and checkpoint identity/provenance stay internal; relevant technical facts appear only beside the content they help execute/understand/verify.

Outside the case matrix, content is vertically centered. Case-matrix content is top-left aligned with 4 px spacing above each data row. XLSX uses one purposeful 3 pt (4 px) model-owned matrix_padding row immediately before each matrix data row; this is presentation spacing, not another case/result, unused evidence reserve or duplicated content. Do not add newline padding to values or number formats. Right-aligned values retain native indent 1. Native Sheets instead uses actual 4 px top/bottom and 8 px left/right padding; do not duplicate the XLSX spacer and native padding. Overview titles remain plain text with full-cell hyperlinks; body keywords retain selective rich-text bold. Verify both navigation and spacing after native save/reopen/import.


Only images collapse, one initially collapsed group per TC; core never hides. Every directly embedded image has a descriptive situation/milestone/observation title immediately above it. Stack images vertically, preserve bytes/aspect ratio, and grow/reflow only model-owned areas without caption/image/next-TC overlap. No evidence URL inputs. No images means one localized no-image line and no large blank reserve. Verify save/reopen/group/anchors and actual pixels; native Sheets image collapse requires separate live proof.

Older saved workbook formats are unsupported. Do not relabel their provenance or rewrite them. No migration helper is shipped.

Complete XLSX testing/review before separately authorized native conversion/share of that same report; native formulas, navigation, images/grouping and recipient viewing require live verification. No second editable result or automatic synchronization.

## Results and identity-keyed writeback

Each variant has independent Actual/Status. Record required checkpoint observations as `checkpoint_id: observed result` lines; a generic PASS does not satisfy concrete obligations. Recorded results aggregate directly from valid status values. Missing Actual, unresolved readiness/oracle/fixtures and proof gaps remain checker findings, never an implicit replacement for recorded PASS/FAIL. Required screenshot checkpoints also need reviewed images. Only model-owned evidence rows may grow; do not insert arbitrary rows, sort individual rows, change merges or move inputs. Capacity refusal is an evidence-layout gap, never application FAIL.

Read-only binding inventory and identity-keyed same-file writeback:

```text
python scripts/update_report.py --source-dir DESIGN --report REPORT.xlsx --language vi --bindings
python scripts/update_report.py --source-dir DESIGN --report REPORT.xlsx --language vi --run-dir RUN < observation.json
```

Writeback stdin is `{identity, status, actual, evidence, run_metadata?}`. Identity is `{design_revision, feature_id, case_id, variant_id, run_id}`; status is the canonical PASS/FAIL/BLOCKED/SKIPPED/NOT RUN token, localized by the writer. Actual is literal text (even leading `=`), not a formula. `evidence` is an array of the shared `EvidenceRecord`; the writer reuses `run_artifacts.validate_evidence`, requiring archived raw/annotated digests, actual matching capture scope, matching identity and actual pixel-review-call metadata supplied after the agent opens the image. It does not invent or perform a pixel review. PASS requires every checkpoint observation and reviewed records for every screenshot checkpoint; repeated accepted images are deduplicated. Existing unrelated results, images, formulas, validations and navigation are preserved; source/report capture identities are rechecked before atomic replacement and saved data is reopened/checked.

One report belongs to one Run ID. A different run is refused rather than overwriting history. Evidence import additionally requires the run ledger's authoritative report to match the target XLSX after path resolution; local ledger report paths must be absolute, while native URI identities are compared exactly. Optional run metadata keys are run_id/build/environment/tester/period (timezone required). Sources without Feature ID require explicit `--feature-id VERIFIED-ID` for identity-keyed writes; preserve their unchanged source assertions and evidence bindings.

Source 1.0/1.1 has no declared checkpoints. Its binding inventory exposes a separate `evidence_slots.CP-result` for each existing variant, using its projected Expected and existing Steps/preservation as the assertion basis. Use that exact ID for image capture/writeback ownership; it is not a new source checkpoint or an additional Actual prefix requirement. Existing assertions, readiness/oracle and source bytes remain unchanged, and genuine archived/reviewed EvidenceRecords are still mandatory for image insertion.

The source workbook is self-documenting: Testcases contains one visible placeholder block labeled as a layout example, never a real testcase or result. The generator removes every preview row from its in-memory copy before projecting source cases, then replaces the template note with run instructions. Generated reports must contain zero placeholder/sample values. Template preview data never feeds counts or checker decisions.

## Presentation

Show verified relative screen routes without domain; unverified routes remain visibly unknown, and not-applicable is only for verified non-UI cases. Keep enough actor/data/configuration/trigger/observation, assertions, preservation and branch differences to execute and assess. Relevant technical facts belong beside their content, without a default technical appendix. Use vertical-center alignment outside the matrix and top-left alignment inside it, with 4 px matrix spacing and sufficient row height; never add whitespace to literals for padding.

Strip source list markers before adding one workbook bullet. Display inline technical code as native bold text with its literal characters, without adding `[]`. For example, incomplete-deleted-stale is bold without brackets, `(29)` stays `(29)`, and `*29` stays `*29`. Keep real bracket characters in arrays, JSON, regex and required payloads; remove only presentation markers, never brackets globally. Remove Markdown emphasis outside code. Do not emit literal backticks, duplicated bullets or Markdown emphasis in generated cells. Each status dropdown stays in one compact unmerged cell. Record failure/block/skip reason and next action in Actual. Overview links to complete TC blocks and separates case/variant totals. No hidden data sheet or third evidence sheet.

## Generate and enter

```text
python scripts/export_report.py --source-dir DESIGN --output NEW-REPORT.xlsx --language vi
python scripts/check_report.py --source-dir DESIGN --report NEW-REPORT.xlsx --language vi --phase in-progress
```

Use existing declared Python dependencies, never install automatically. Export refuses every existing path. Enter results in the same file; a new run/expected requires an explicitly requested new path. Checking only reads and never repairs or regenerates.

Actual, image areas and run/build/environment/tester/time start blank; status starts localized NOT RUN. Execution time includes timezone. Recorded text stays literal; pasted formulas are rejected. Non-PASS actual text includes the observed result, reason and next action. Preserve observations and do not alter expected to fit a result.

## Evidence images

Use checkpoint-owned image areas and model bindings returned by the current writer. Each descriptive title appears above its directly embedded image; accepted images preserve original bytes/aspect ratio and stack vertically inside their TC. Saved alternative text is the observed English note. Inspect annotations/highlights in the actual pixels. Arbitrary row insertion, sorting, changed merges or moved inputs are unsupported.

Inspect pixels, metadata and saved alternative text. Complete screenshot reviews have case_id, variant, saved-byte sha256, caption, reviewed_by, timezone-bearing reviewed_at and actual source; Each review requires the exact mapped checkpoint_id. Alternative text must match the designated caption. No invented image, result or attestation.

## Counts and read-only checking

Counted PASS/FAIL follows exact localized recorded status only, with no readiness, eligibility or Actual gate. PASS rate is recorded PASS / recorded PASS+FAIL; no denominator means no data. TC aggregation precedence: any FAIL => FAIL; all PASS => PASS; all SKIPPED => SKIPPED; any BLOCKED => BLOCKED; all NOT RUN => NOT RUN; otherwise in progress (Đang thực hiện / 実行中). The same rule applies to Overview totals. Missing Actual and unresolved source/readiness/oracle/evidence are validated separately; counts are execution records, not acceptance proof.

Checker compares immutable source/formulas/navigation/merges, validates inputs, metadata/privacy/relationships and image bindings. Report2.5 permits only model-owned evidence and unused reserve rows to be hidden; core criteria/Actual/Status must remain visible. Opaque unsupported package entries remain rejected in every version. Workbook privacy setting does not certify image pixels or access. Explicit clipping fails; estimated wrapping needs native visual inspection. Checking is not a render certificate.

Complete checking takes genuine JSON stdin with closure_confirmation, evidence_access and screenshots. Closure: closed_by, timezone-bearing closed_at, source, audience. Access: url, audience, verified_by, timezone-bearing verified_at, method (human-attestation or recipient-session), source. Image fields are above. Missing routes/results/reasons/closure/access/image review prevent completion. Closed reports can retain failure/skip and do not prove release.

## Native Google Sheets

Honor the user's chosen execution surface. For the approved customer workflow, complete and review testing in XLSX first, then convert that same result file to native Sheets and verify layout/formulas/IDs/links/images before sharing. When the user explicitly chooses to execute in Sheets, convert the blank XLSX and verify it before recording results there. Avoid two editable result copies. Conversion/creation/sharing needs explicit external-task authorization.

The shipped checker is XLSX-only. Do not assume Excel metadata, links, wrapping or images survive conversion; native verification remains a separate gap until observed. No automatic upload, Apps Script, application tests or publication follows. Before delivery, render all changed sheets, recalculate/save/reopen in the available engine and disclose unverified native conversion/readability tests.

Customer templates freeze only the title row and no column, so freeze boundaries never cross merged headings. XLSX two-cell anchors do not guarantee that Google Sheets hides imported pictures when rows collapse: conversion can produce floating images. Before adopting an imported report, test opening and closing an image group and inspect the following TC. Use durable **Insert image in cell** for reviewed screenshots in native Sheets; never use floating images in collapsible evidence. Preserve the original file/history before any separately authorized layout repair. A native cell-only copy excludes imported floating objects while retaining values, formulas, notes, validations and merges; restore column widths, row heights, groups and navigation and verify them live before adopting it. Preserve history separately rather than treating old screenshots as new-run evidence. Do not claim XLSX conversion alone completes this repair.

For authorized native customer layouts, use actual cell padding (top/bottom 4 px, left/right 8 px), top alignment inside the matrix, vertical-center alignment outside it and sufficient row height; never pad literal content with spaces or newlines. Keep one full-width image cell per image, with its title immediately above. Group every title/image row between the visible evidence heading and the next TC. Collapse must hide those rows completely, including their row numbers; reducing row height is not collapse. Remove unused reserve rows when rebuilding the authorized layout. Verify the heading jumps directly to the next TC and both images return on expansion.

After native cell-only copying, inspect formulas for references that still point to the old tab. Keep formula argument separators from the live native file: VI locale uses semicolons; an XLSX export uses commas and must not be replayed unchanged through the native API. Verify calculated summary values, not just formula strings. Hide unused current reserve rows completely rather than exposing thin blank rows. Confirm the selected cell again after the picker closes and verify exported image hashes and anchor rows against the accepted evidence manifest; typing a name-box address is not proof that insertion used that row.

Preserve model binding coordinates during native conversion: hide the XLSX 3 pt `matrix_padding` rows rather than deleting them, then apply actual 4 px top/bottom and 8 px left/right padding. Keep matrix/header/continuation content top-left and other content vertically centered. Overview titles remain plain full-cell links. Use native `HYPERLINK("#gid=<detail-tab>&range=<target>"; "<caption>")` formulas with the live locale separator for every TC navigation title; partial rich-text links or `textFormat.link` alone are not reliable navigation proof. Read back the computed hyperlink and follow it to the exact TC, not merely verify blue/underlined styling. Only logical matrix result rows have XLSX spacing rows; continuation chunks do not.

For native writeback, first read bounded TC/variant/checkpoint IDs, merged ranges, validation and current observations. Place multiple durable native images inside the owning Testcases checkpoint rows, never on a third sheet and never as temporary IMAGE URLs. Read back exact Actual/Status, inspect image placement and the following TC, and verify Saved state. Unknown write outcomes require rereading before retrying; no XLSX checker result certifies the native Sheet. Use only the authoritative report selected for this run, without automatic XLSX/Sheets synchronization.


## Readable execution layout 2.5

Each TC has four parts: title and recorded aggregate; explicitly labeled conditions plus a two-column Step/Common action table; the five-column variant matrix; evidence. Use short step labels (Bước 1 / ステップ 1) on the left and the concrete action on the right. Do not print a separate variant-input list before the matrix or a shared Expected section outside it.

The matrix columns are Trường hợp / Dữ liệu-thao tác riêng / Kết quả mong đợi / Kết quả thực tế / Đánh giá (localized for JA). Keep a short human description followed by the stable variant ID; put decisive data and action differences in column B and the complete branch-specific outcome in C. Actual and Status remain independent unmerged D/E cells. Never repeat a multi-branch summary in every variant or use “branch X in the procedure/Expected” as executable content. Preserve assertions, fixtures, timing, negative controls and literal values when removing redundant prose.

Use native rich-text runs to bold selected UI names, actions, operators, inline code and decisive values in body content; never bold entire sentences or emit Markdown markers. Technical identifiers use native bold without added brackets. Overview navigation titles remain plain text with a full-cell hyperlink, without partial bold runs. Plain text assembled from all runs must retain exact source literals and remains subject to privacy/immutability checks. Outside-matrix content is vertically centered; matrix content remains top-left with 4 px spacing. XLSX uses purposeful matrix_padding rows, never newline padding or unused reserve rows; only evidence collapses. Native Sheets uses textFormatRuns for body content, unchanged cell text and separately verified writeback/layout. No automatic conversion, source readiness promotion or Google Sheets overwrite follows from this format update.
