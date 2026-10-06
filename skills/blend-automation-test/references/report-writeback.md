# One authoritative report and checkpoint evidence

Read [the shared contract](../../../shared/automation-testing.md) and [generator report guidance](../../blend-generate-test-spec/references/test-report.md). Choose the user's supplied XLSX **or** native Google Sheets as the authoritative report for this run. If both were supplied without a clear choice, inspect their identities/history and resolve the material choice before writing; do not auto-sync. One writer owns results and images.

## Binding and preservation

Verify source/report schema, design revision, feature ID, Case/Variant IDs and checkpoint ownership before every write. Never hard-code RC-001 rows or derive a target from a screenshot filename. Actual uses checkpoint-keyed literal observations (`CP-result: score 29 is marked red; displayed count is 1.`), while status is independently entered for the variant. Derived case status and summary formulas remain untouched.

Keep formulas, source prose, merges, navigation, validations, other results and existing images. Text starting `=` is literal data, not a formula. Accepted annotated screenshots have genuine reviewed EvidenceRecords from [run artifacts](output.md); pending/unreviewed or wrong-identity images never enter the report. Each image has a descriptive human-readable title above it, identifying the situation/stage and actual observation; use supplied title or a faithful observation-based caption. Images are directly embedded below their titles and stacked vertically, never a URL substitute. Keep technical checkpoint identity in metadata; customer2.5 prose should include only details needed to execute, understand or verify the check. Image labels/notes explain observed checkpoint evidence, not invented approval or a blanket PASS.

Outside the case matrix, content is vertically centered. Case-matrix content is top-left aligned with 4 px spacing above each data row. XLSX uses one purposeful 3 pt (4 px) model-owned matrix_padding row immediately before each matrix data row; this is presentation spacing, not another case/result, unused evidence reserve or duplicated content. Do not add newline padding to values or number formats. Right-aligned values retain native indent 1. Native Sheets instead uses actual 4 px top/bottom and 8 px left/right padding; do not duplicate the XLSX spacer and native padding. Overview titles remain plain text with full-cell hyperlinks; body keywords retain selective rich-text bold. Verify both navigation and spacing after native save/reopen/import.

## XLSX helper

Use [update_report.py](../../blend-generate-test-spec/scripts/update_report.py), resolved from this reference, with an available Python interpreter and already declared dependencies. No installation follows from a missing dependency. It provides:

```text
python update_report.py --source-dir DESIGN --report REPORT.xlsx --language vi --bindings
python update_report.py --source-dir DESIGN --report REPORT.xlsx --language vi --run-dir RUN
```

The first command is read-only. The second reads a JSON value from stdin and updates the same file. For legacy sources without a Feature ID field, append `--feature-id VERIFIED-ID` to both commands; obtain that ID from verified context, not a guessed slug. Use `--language ja` only for the matching JA report.

Payload:

```json
{
  "identity": {
    "design_revision": "<frozen revision>",
    "feature_id": "<verified ID>",
    "case_id": "<existing Case ID>",
    "variant_id": "<existing Variant ID>",
    "run_id": "<current Run ID>"
  },
  "status": "PASS",
  "actual": "CP-result: <actual observation>\nCP-after: <actual observation>",
  "evidence": [],
  "run_metadata": {"build": "<observed build>", "environment": "<test environment>", "tester": "<actual actor>", "period": "<actual timestamp with offset>"}
}
```

This is a shape example, not an execution record. `evidence` must contain accepted EvidenceRecords when screenshot checkpoints exist; its empty example does not satisfy PASS. Customer2.5 accepts an optional reader-language `title` on each EvidenceRecord; when absent the writer uses `observed_note`. Write a title describing the situation/stage and actual observation, without internal tooling details. `observed_note` retains the truthful English screenshot observation. Include only genuinely available optional run metadata. For new reports PASS requires a keyed observation for every checkpoint and reviewed evidence for every screenshot checkpoint. Export/inspection truth is evaluated by the agent, not by a nonempty string or writer exit code.

`--bindings` returns revision/feature/schema/sheet and a variants map with exact status/actual cells, checkpoint definitions/picture rows and evidence capacity. In customer2.5.0, core conditions/actions/Expected/Actual/Status remain visible, and only evidence rows use one initially collapsed group per TC. Missing evidence shows one localized no-image line without a large reserved blank area. Each image title is above its image and each image preserves original bytes/aspect ratio. Use the returned binding and the writer's supported growth/capacity; no user image URL is required. Use only returned current bindings and model-owned evidence capacity. Never insert arbitrary rows, shrink unreadably or move images into the next TC. Capacity refusal retains pending evidence as a disclosed layout gap.

Older workbook formats are unsupported and refused without mutation. A run-local capture label for a supported older source maps to its exact existing assertion/anchor and unchanged oracle; it does not change source design, report version or counts.

For source 1.0/1.1, `--bindings` returns empty declared `checkpoints` and one `evidence_slots.CP-result` image owner per existing variant. Use that exact slot ID in the EvidenceRecord and run capture identity. Its `expected` is the existing projected variant Expected (including existing Steps/preservation); it introduces no source checkpoint, new oracle, or extra Actual prefix requirement. Observe all existing assertions and write truthful literal Actual normally. This slot is only the binding for reviewed result images inside report 2.5; all archive, identity, digest and pixel-review requirements still apply.

The writer validates identities/source, saved workbook and EvidenceRecords, saves a candidate, reopens/checks preservation/readback and replaces the same report only after checks pass. It rejects a report already owned by another Run ID. This structural check does not prove pixels, visible layout or spreadsheet recalculation. Reopen/render the changed block in an available spreadsheet engine, check that all images/notes remain readable and within their variant and that following cases/navigation still work. Run the matching read-only [check_report.py](../../blend-generate-test-spec/scripts/check_report.py) for in-progress checking; complete mode needs the genuine closure/access/image review inputs described in generator report guidance. Disclose unavailable render/recalculation proof.

## Native Google Sheets

Use available Sheets/Drive connector and native browser UI for the exact file authorized by the user. Do not create/convert/share a file or remove an old Evidence tab as a side effect of execution. A historical incompatible layout remains a migration gap; it is not scratch space. XLSX checks cannot certify a native Sheet.

1. Read live metadata and bounded source/ID/status/actual/evidence ranges. Ground spreadsheet/tab IDs, revision and exact Case/Variant/checkpoint labels, merges, validations and row sizes. Source-model bindings guide lookup but do not prove imported row numbers stayed the same.
2. Reconcile existing results and run identity, then update only verified result cells with literal-safe API fields. Preserve validation/formulas and derive summaries normally. Log the intended target and pending observation locally before a write.
3. Insert durable native images through currently available connector/native UI, in the same owned case/checkpoint block, below a human-readable image title. Temporary IMAGE URLs are unsupported for accepted durable evidence. Do not grant permissions to make an image work. If durable native insertion is unavailable, record pending artifacts and an explicit capability gap; a link-only substitute does not meet the image contract.
   For collapsible evidence use **Insert image in cell**, not an image over cells. Select only the reviewed screenshot from the current run and exact Case/Variant/checkpoint. Imported XLSX floating images can remain visible after collapse; test both group states and the next TC before accepting native layout. Layout repair needs its own authorization and must preserve historical evidence.
4. Keep visible labels such as `E01 — Setup`, `E02 — Result`. Prefer full-width vertical images for dense screens; side-by-side only if all needed text stays readable. Respect current reserved evidence capacity; no arbitrary row insertion, tab creation or source/layout change. In customer2.5 group only evidence rows once per TC, initially collapsed; core stays visible. Older workbook layouts are unsupported. Verify native grouping and image reveal/placement in the live file; imported XLSX grouping is not proof of native behavior.
5. Read back exact status/actual and verify image count/identity/placement as pixels in native UI, including Saved state. Collapse the owning group: every image/title row and its row number must disappear, leaving the evidence heading directly followed by the next TC. Expand it and confirm all images return beneath their titles. Thin visible reserved rows fail this check. Keep the native top/bottom 4 px and left/right 8 px cell padding; never insert whitespace into results. Check following blocks and summary/navigation. Keep file/export proof separate from a screenshot of its link.

If a connector/native write returns an unknown outcome, reread the exact target cells and inspect existing images before retry. If the intended values/digests are already present, acknowledge that saved result without duplicating images. If absent, retry only that bounded write when safe. If identity or image outcome remains ambiguous, keep a pending writeback gap and preserve both report and ledger; do not rewrite the entire report or claim success. Resume performs this same reconciliation first.

After verified writeback, record the saved target and readback/visual review references in the run ledger. Pending observations stay visibly pending. The final handoff names this single authoritative report and the precise unverified portion, without claiming a local workbook check certifies Google Sheets or a package test certifies product behavior.
