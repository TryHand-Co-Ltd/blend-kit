# BLEND Kit — scenario testing and automation contract

Read this contract when designing Test Spec, projecting/checking its report, or executing `blend-automation-test`. [Workflow](workflow.md) owns discovery/authority; [artifact formats](artifact-formats.md) owns template/resource mapping. This contract owns the shared design, execution and evidence semantics. Installed tool capabilities must be discovered in the current runtime; package metadata is not runtime proof.

## Ownership and compatibility

`blend-generate-test-spec` designs, finalizes or explicitly refreshes cases, fixtures, coverage and a blank report. `blend-automation-test` consumes a frozen design and one authoritative XLSX **or** native Google Sheets report, performs the requested scope and records observations. Execution never silently groups cases, changes Expected, migrates a report, seeds a database, fixes application code, installs tools or publishes results. A new generator format does not authorize migrating existing documents/results.

| Source schema | Matching report | Dispatch |
| --- | --- | --- |
| `test-cases@1.3.0` | `test-report@2.5.0` | Current authored source, concrete variant outcomes and meaningful checkpoints. |
| Supported `test-cases@1.0.0` / `1.1.0` / `1.2.0`, including RC-0011.1 | `test-report@2.5.0` | Read-only source grammar; preserve existing case/variant IDs, oracle/readiness and gaps. |

Scope/data stay `1.0.0`. Saved workbook provenance must be exactly report2.5; older workbooks fail closed without mutation. No legacy workbook assets or migration command are shipped. Source compatibility does not imply workbook compatibility or source rewrite authorization.

Sources without design checkpoint IDs use a run-local capture label grounded in the exact existing step/assertion and recorded with its source anchor and unchanged oracle. The label binds evidence only; it never creates a new design checkpoint, count or Expected obligation. Preserve Case/Variant identity and missing-proof gaps during resume.

## Source grammar: test-cases@1.3.0

Use the existing localized H2/Flow/Case/Context grammar, field ordering, escaped pipes `&#124;`, line breaks `<br>`, exact `TD` references and gap semantics. The conventions table is exactly `Revision`, `Feature`, `Feature ID`, `Conventions`; Feature ID is the verified source ID, not its title or folder slug. Case fields retain 1.1.0 order except required neutral `Execution lane` immediately after `Priority`. Lane is exactly one of `Browser`, `Integration`, `DB`, `Security`, `Performance`; differing required seams can be separately mapped in scope. Do not describe DB/fault-injection proof as screenshot-only browser proof.

Every new case has one objective, common preparation and an ordered Steps table. Case `Thao tác` / `操作` is exactly `@Steps`; case `Expected` is a concrete overall TC outcome, including material timing/preservation obligations. After its Field table, emit these three tables in order with neutral headings/headers shared across JA/VI:

```text
##### Steps
| Step | Action |
##### Variants
| Variant | Inputs | Action delta | Expected |
##### Checkpoints
| Variant | Checkpoint | Step | Stage | Expected | Focus | Artifact |
```

- Steps are exactly two columns, consecutive positive integers from 1; Action describes the concrete procedure. State the one independent Reset in its case field, rather than repeating it in the Steps table. Keep temporal/preservation criteria in the overall outcome and meaningful checkpoints.
- Variants are always explicit, including `base` for a single run. Preserve stable Variant IDs; begin Inputs with a human description followed by decisive values so customer labels show description (ID), never a bare code. Inputs resolve local values/fixtures; Action delta is `none` or unambiguous changes referring to existing step numbers, when needed. Variant Expected is the concrete final outcome for that branch, including its material preservation criteria. Never copy a multi-branch case summary or refer to `@Checkpoints`, another branch or unresolved parameters. An empty branch, compound `a/b`, previous-case dependence or unresolved parameter is invalid.
- Every variant has its required meaningful capture/inspection/export milestone(s); do not create setup/result pairs or one checkpoint per click by default. Checkpoint ID uses the existing identifier grammar `[A-Za-z][A-Za-z0-9_.-]*`, is unique case-insensitively **within its variant**, and is stable when meaning remains unchanged. Step is one existing step number. Stage is exactly `setup`, `before`, `result`, `after` or `export`; explanatory prose belongs in Expected/Focus.
- Checkpoint Expected is concrete, nonempty and source-backed for that variant; references such as `@Steps`, `@Checkpoints`, another variant or an unresolved placeholder are invalid here. Focus names the exact observable area/value that proves it, including controls needed to exclude competing interpretations. Artifact is exactly `screenshot`, `export` or `inspection`: screenshots need reviewed highlight/note; export needs the actual application file; inspection names a real non-image observation. Multiple proof types use separately identified checkpoints, not compound enum values.
- Shared context may resolve only its own field as before; tables cannot be hidden in context references. JA/VI preserve IDs, table order, lane, stage/artifact tokens and semantic meaning. No Actual, execution Status, image path or review attestation is generated into design Markdown.

Coverage continues to accept `case_id`, `case_id:variant_id` or defined gap IDs. Checkpoint mapping supplements these with `case_id:variant_id:checkpoint_id` when a specific assertion is needed; all targets must resolve. Cases/variants/checkpoints must reverse-map to an obligation/branch or preservation requirement. On an authorized refresh, record old Case/Variant → new Case/Variant/Checkpoint mapping with obligation, branch and disposition in scope; no automatic transfer of PASS or images when the oracle/state changes. Count reduction is not a coverage gate.

### Older source inputs

Older source grammars may be read only when the installed parser explicitly accepts them; they never select an older workbook or create legacy assets.

## Common identity and report binding

`TestRunIdentity = (design_revision, feature_id, case_id, variant_id, checkpoint_id, run_id)`. Revision and feature come from the verified frozen design, run ID from the exclusive run directory. For source 1.2.0/1.3.0, checkpoint_id is the design ID; for legacy sources it is the explicitly mapped run-local capture label above. No positional index, filename or row number substitutes for identity. Rows may move; IDs do not. Case/variant/checkpoint IDs must not collide under case-insensitive spreadsheet matching. Different run IDs keep their own observations and evidence history.

`ReportBinding` is a model-derived value, not a separate mandatory manifest:

| Field | Required meaning |
| --- | --- |
| design_revision, feature_id, schema_version | Exact report/source identity and matching dispatch. |
| case_id, variant_id | Existing target; never auto-created by writeback. |
| sheet, status_cell, actual_cell | Exact independently editable variant result locations obtained from source/layout and verified against the saved report. |
| checkpoints | Map checkpoint ID → stage, step, expected, focus, artifact and owned evidence-area ranges/anchors; only defined IDs can receive observations or files. |
| evidence_capacity | Current legal anchors/space and allowed model-driven expansion; only current model-owned evidence areas may expand. |

`test-report@2.5.0` is the customer projection, exactly two sheets. Core contains enough material conditions/data, concrete procedure, branch-specific Expected beside Actual/Status and blocked/difference reasons to execute, understand and verify independently. Same procedure with different data uses a table; differing procedures/initial states are separately understandable. No review/sample notes, preparation/readiness labels or default technical appendix. Metadata, readiness/oracle/rights/provenance stay internal for execution prerequisites and acceptance verification; they never gate recorded status counts. Only evidence expands: one initially collapsed group per TC, a descriptive situation/milestone/observation title above each directly embedded image, vertically stacked, original bytes/aspect ratio, no URL input. No images means one localized no-image line without a large blank area. Reflow preserves captions/image bounds, following TC and all bindings/results. Older workbooks are unsupported and rejected without rewriting. Native Sheets needs separate collapse/image verification.



Checkpoint observations are keyed by exact identity, never a generic PASS. One independent result per variant remains the sole count denominator. Accepted images stack vertically with original pixels/aspect ratio and model-owned anchors; use only current permitted evidence-area growth. Capacity refusal is a disclosed layout gap, not application FAIL. Reflow preserves bindings/navigation/formulas/merges/validation and unrelated inputs/images, then passes readback/checks.

One writer owns each report. Before writing, verify source revision and TC/variant/checkpoint binding against current saved cells. Write literals safely, including text beginning `=`; keep formula/validation/immutable source and all non-target history. Save XLSX safely then reopen/check image bindings. For native Sheets, read bounded IDs/merges/validation first, write through available connector/native UI, then verify actual pixels, bindings and Saved state. XLSX checking cannot certify native Sheets. Temporary IMAGE URLs are not durable evidence; do not silently grant sharing permissions. No auto-sync between XLSX and Sheets.

## EvidenceRecord and run output

An `EvidenceRecord` contains the six named TestRunIdentity fields, `sequence` (positive integer), `raw_path`, `annotated_path`, `raw_sha256`, `annotated_sha256`, `viewport`, `full_page`, `assertion`, `focus`, `observed_note`, `reviewed_by`, `reviewed_at` and `source`. Paths are relative to the run directory; digests are SHA256 hex. A screenshot record has both files/digests, viewport as `{"width":1920,"height":1080}` by default and the actual boolean `full_page` (default false). `observed_note` is the English text actually visible on the annotated image. Reviewer identifies the agent/user that actually opened the pixels and timestamp includes an offset. `source` is an object with `capture_tool`, `raw_capture`, `annotated_capture`, `annotation_method` and `pixel_review` (an object containing actual `tool` and `reference`). Capture receipts identify the real calls/outputs with their actual matching `full_page` value; annotation method and pixel-review reference describe actual work, not fabricated human attestation. Pending ledger records may leave review fields empty but cannot bind to accepted report evidence. Export/inspection artifacts retain their actual file/observation and checkpoint identity without claiming screenshot fields.

Local output is `blend-context/local/test-output/<verified-feature-folder>/<YYYY-MM-DD-NNN>/`, using the user's local date and an exclusively created run folder. Resume requires matching feature/revision/report/run identity. Preserve `screenshots/raw/`, `screenshots/annotated/`, `exports/` and one `run-summary.md`. Archive the actual returned MCP file immediately before the next capture, copy without overwrite and verify SHA256; never guess the output path from timestamp or delete originals automatically. Names use `<case>__<variant>__<checkpoint>__<sequence>.png` with safe validated path components. Local raw data may be sensitive; only accepted evidence suitable for the report is shared.

`run-summary.md` is a ledger, not a second result report. It records run/source/report/build/scope identity, an inventory of **every** requested variant, current checkpoint/observations/blocker or evidence-quality gap, artifact records, stop/resume point and cleanup state. Keep record identity and digests available in that ledger; no DB or separate mandatory manifest. Authoritative Actual/Status remain in the chosen report. Interrupted/not-attempted variants stay NOT RUN; ledger observations awaiting safe writeback are visibly pending, never silently lost or treated as already saved.

## Binding requirements

The following requirements are the approved planning contract; shared interfaces above specify their implementation without widening permission.

| ID | Binding requirement |
| --- | --- |
| R01 | Không update, sửa code hoặc đổi config Playwright MCP; chỉ dùng capability được runtime hiện tại cung cấp và workaround tạm đã kiểm. |
| R02 | Raw and annotated screenshots default to `full_page=false` with adequate context; use true only when whole-layout proof needs it. Both receipts and EvidenceRecord record the real matching scope. |
| R03 | Default desktop viewport is 1920x1080; viewport/full-page does not prove internal, horizontal or virtualized content. Scroll and capture additional necessary views. |
| R04 | Accepted evidence has a short English observed note at top-right in clear space, minimal non-overlapping/non-touching highlights and sufficient assertion context; actually open pixels before acceptance. Never cover controls/data. |
| R05 | Content văn bản do agent tạo khi test và note dùng tiếng Anh có nghĩa; giữ nguyên nhãn UI, identifier và literal/payload bắt buộc của TC; report theo ngôn ngữ người dùng chọn. |
| R06 | TC, Actual, Status và nhiều ảnh evidence nằm cùng sheet Testcases; chỉ giữ Overview/Tổng quan và Testcases, không tạo sheet Evidence thứ ba. |
| R07 | Output local theo feature và Run ID trong `blend-context/local/test-output/<verified-feature-folder>/<run-id>/`; giữ raw/annotated screenshots, exports và một run-summary.md. |
| R08 | Một TC có một mục tiêu rõ; Steps có thao tác cụ thể; Expected tổng thể và checkpoint giữ oracle cần thiết; variants có dữ liệu, khác biệt thao tác và expected riêng. Shared setup viết một lần, mọi variant dựng/reset được độc lập. |
| R09 | Gộp/bỏ case độc lập chỉ sau khi map nghĩa vụ, nhánh và ID cũ sang TC/variant mới; giữ quyền, lifecycle, nguồn, writer và định dạng output có khả năng lỗi độc lập. Không đặt số lượng TC mục tiêu làm coverage gate. |
| R10 | Chạy full phạm vi được yêu cầu, theo dõi mọi variant; case trước fail không tự bỏ case sau. Chưa chạy giữ Chưa thực hiện; blocker phải có kiểm tra thực tế, actual và nguyên nhân cụ thể. |
| R11 | Không đổi Expected theo Actual, không lấy screenshot cấu hình làm bằng chứng đầu ra, không lấy ảnh browser thay file Excel/PDF thật, không gán lỗi evidence thành lỗi sản phẩm. |
| R12 | Đọc lại writeback, kiểm image binding và bố cục; giữ nguồn, formula, validation, kết quả/history khác. Một report authoritative cho mỗi run, không tự đồng bộ hai bản kết quả. |
| R13 | Generator thiết kế/finalize/refresh; automation thực thi. Không tự gộp TC, seed DB, sửa app, cài tool, migration report, install skill hoặc publish từ lệnh chạy test. |
| R14 | Caption/note phản ánh điều đã quan sát; không ghi PASS khi thiếu assertion bắt buộc. Giữ expected authority, readiness và execution độc lập, kể cả khi người dùng cho chạy để lấy observation. |
| R15 | Expected là một block kết quả tổng thể mỗi TC; final Expected cụ thể cho từng variant, không lặp Expected/bảo toàn theo bước trong core. |
| R16 | Core có ID/title, Priority/screen, điều kiện/data quyết định, actions, một Reset, Expected, Actual/Status và evidence trong Testcases; không copy toàn fixture hoặc prose chung. |
| R17 | Customer2.5 keeps identity/readiness/oracle/fixture/checkpoint metadata internal; only facts needed to execute/understand/verify appear beside related content. No old technical-row layout is supported. Core criteria/Actual/Status remain intact; recorded counts are independent of readiness and Actual, while acceptance-quality checks stay separate. |
| R18 | Blank Actual/hàng/ảnh gọn; text/ảnh accepted grow đúng vùng sở hữu, không clipping hoặc thu nhỏ khó đọc; ảnh dày xếp dọc. |
| R19 | Preserve original raw/annotated bytes, matching actual viewport/full-page scope, precise non-overlapping highlights, top-right English observed note, real pixel review and every identity/literal/atomic/preservation/dedup/writeback guard. |
| R20 | Chỉ report2.5; đọc nguồn RC-0011.1 mà không sửa grammar/oracle; từ chối workbook cũ, không migration. |

## Capture and execution consequences

Discover real MCP tools, resize to the default desktop viewport and use snapshot refs for actions. Raw precedes annotated; both captures use matching state/scope, normally `full_page=false`. Full page is only for necessary whole-layout proof. Scroll and capture additional views for internal/horizontal/virtualized regions; keep enough title/object/value context. Never invent unsupported screenshot/crop parameters or capabilities.

Place a short English observed note at top-right in clear space before final ref acquisition; if it covers UI/data, adjust the view or space without mutating application data. Verify visible targets and useful bounds. Remove duplicate/nested refs; group score+result only when the pair proves the assertion. Use separated frames only when they do not intersect or touch; otherwise use one justified union or separate views. For observed hidden-ref collision remove only temporary data-mcp-ref attributes, resnapshot and recheck. Archive raw and annotated actual returned files unchanged. Open every accepted image to inspect context, note truth/position and highlight coverage/non-overlap. Clean temporary notes/styles in finally and verify removal. Retry evidence repair at most three times per checkpoint; retain an evidence-quality gap afterwards, not product FAIL or complete PASS.

Execution inventory tracks every variant in requested scope. Reset independently; an earlier failure does not skip an unrelated later case. A real blocker needs an attempted prerequisite check and specific observed reason. Unknown oracle/preparation remains a gap. User stop ends work and records the resume point; untouched rows remain NOT RUN. Execution input tokens remain PASS/FAIL/BLOCKED/SKIPPED/NOT RUN. Recorded counts follow those statuses directly, independently of Confirmed/Ready or Actual. Aggregation precedence is any FAIL, all PASS, all SKIPPED, any BLOCKED, all NOT RUN, otherwise in progress. Checker findings for missing Actual, readiness, oracle and mandatory evidence remain separate; a recorded result is not acceptance or release proof. A run allowed for Draft observations does not approve Expected. Missing mandatory assertions/evidence prevents complete proof even if a product observation appears correct; image errors alone never establish application FAIL. Every final completion claim distinguishes structural/package checks, actual agent behavior, pixels, file-export verification and native Sheets proof.


## Readable execution layout 2.5

Each TC has four parts: title and recorded aggregate; explicitly labeled conditions plus a two-column Step/Common action table; the five-column variant matrix; evidence. Use short step labels (Bước 1 / ステップ 1) on the left and the concrete action on the right. Do not print a separate variant-input list before the matrix or a shared Expected section outside it.

The matrix columns are Trường hợp / Dữ liệu-thao tác riêng / Kết quả mong đợi / Kết quả thực tế / Đánh giá (localized for JA). Keep a short human description followed by the stable variant ID; put decisive data and action differences in column B and the complete branch-specific outcome in C. Actual and Status remain independent unmerged D/E cells. Never repeat a multi-branch summary in every variant or use “branch X in the procedure/Expected” as executable content. Preserve assertions, fixtures, timing, negative controls and literal values when removing redundant prose.

Use native rich-text runs to bold selected UI names, actions, operators and decisive values in body content; never bold every sentence/ID or emit Markdown markers. Overview navigation titles use plain text with a full-cell hyperlink, not partial rich-text emphasis that can interfere with link rendering. Plain text assembled from all runs must retain exact source literals and remains subject to privacy/immutability checks. Outside-matrix content is vertically centered; matrix content stays top-left with 4 px spacing supplied by purposeful model-owned matrix_padding rows in XLSX or actual native padding in Sheets. No newline padding, duplicated content or unused reserve noise. Only evidence collapses. Native Sheets uses textFormatRuns in body content, unchanged cell text and separately verified writeback/layout. No automatic conversion, source readiness promotion or Google Sheets overwrite follows from this format update.

Outside the case matrix, content is vertically centered. Case-matrix content is top-left aligned with 4 px spacing above each data row. XLSX uses one purposeful 3 pt (4 px) model-owned matrix_padding row immediately before each matrix data row; this is presentation spacing, not another case/result, unused evidence reserve or duplicated content. Do not add newline padding to values or number formats. Right-aligned values retain native indent 1. Native Sheets instead uses actual 4 px top/bottom and 8 px left/right padding; do not duplicate the XLSX spacer and native padding. Overview titles remain plain text with full-cell hyperlinks; body keywords retain selective rich-text bold. Verify both navigation and spacing after native save/reopen/import.
