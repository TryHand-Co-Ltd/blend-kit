# Local run artifacts

Read [the shared contract](../_kit/shared/automation-testing.md) for TestRunIdentity and report ownership. Use [run_artifacts.py](../scripts/run_artifacts.py) for exclusive creation, immediate archival and byte/provenance validation. It uses the standard library and never calls a browser, edits a report, installs a tool or judges pixels.

```text
blend-context/local/test-output/<verified-feature-folder>/<YYYY-MM-DD-NNN>/
  screenshots/raw/<case>__<variant>__<checkpoint>__<sequence>.png
  screenshots/annotated/<case>__<variant>__<checkpoint>__<sequence>.png
  exports/<case>__<variant>__<checkpoint>__<sequence>.<extension>
  run-summary.md
```

Resolve the existing feature through its source ID, README and CONTEXT; never infer identity from a similar title. Pass its exact folder to the helper. Unsafe path components, reserved device names and symlink/junction targets are rejected; do not silently sanitize an identifier into a different identity. Run IDs use the user's Asia/Saigon local date, with an exclusively allocated sequence. The timestamp in an MCP filename may be UTC and is not a Run ID.

The helper keeps one Markdown ledger with fenced JSON records, not a manifest or database. The first record pins `design_revision`, `feature_id`, `feature_folder`, `run_id` and one authoritative `report`. Include build/source identity, requested scope and every requested Case/Variant in its inventory before execution. Record observations pending writeback, evidence-quality gaps, prerequisite attempts/blockers, cleanup and stop/resume points as events. Actual/Status remain authoritative in the selected report; do not make a duplicate result table here.

## Python interface

- `create_run(context_root, feature_folder, metadata, run_id=None) -> Path`: metadata requires nonempty `design_revision`, `feature_id`, `report`; additional build/scope/inventory fields are retained. The existing feature README/CONTEXT must be present. Explicit run IDs cannot overwrite a folder; default allocation uses Asia/Saigon date. Feature identity is grounded by the caller; file presence alone does not prove it.
- `resume_run(run, expected) -> dict`: expected must match all five saved run/source/report keys. Reread frozen design, live report and pending ledger observations before continuing. The function does not decide whether the source/report changed semantically.
- `archive_capture(run, returned_path, identity, kind, sequence, metadata) -> dict`: kind is `raw`, `annotated` or `export`. Use the **actual returned file path**, then archive before another screenshot. Copy exclusively, reread source/archive SHA256 and retain the original. A duplicate artifact path fails, even if bytes match. `sequence` is a positive image ordinal with no four-image cap; `correction_attempt` defaults to 0 for an original view, or 1–3 for the checkpoint's three allowed corrections. A used correction ordinal cannot be reused for another pair at the same checkpoint. Screenshots require explicit boolean `full_page` (default `false`; `true` only when the assertion requires the whole layout), `viewport={width,height}`, `observed_state`, `annotation_present` false/true for raw/annotated, offset `captured_at`, and actual `capture_reference`. Each pair must show the same state, viewport, scroll position and boolean capture scope; distinct accepted pairs may show different scroll views. Exports retain actual downloaded bytes; an empty/fake/browser-printed file cannot establish app-export proof.
- `validate_evidence(record, run_dir, identity=None) -> Path`: pure read-only validation returning the accepted annotated file path. It verifies paired archive receipts, identity, digests, viewport/capture scope, same observed state, capture/review ordering and review provenance. Report writers additionally pass `identity["report"]` to check the ledger's authoritative report: resolved paths for local files, exact strings for URIs. Store an absolute selected local-report path in run metadata so resume is independent of working directory. Report writers reuse this callable rather than copying validation logic.
- `record_evidence(run, record) -> dict`: validates then appends an EvidenceRecord after actual pixel review. A pending or rejected attempt remains a capture/event, never an accepted EvidenceRecord.
- `records(run) -> list[dict]` and `append_record(run, event)`: ledger read/append. One writer owns the run. If an entry is interrupted/corrupt or an archive was copied before ledger write failed, inspect/recover explicitly; never overwrite an earlier archive to make resume convenient.

All identity keys are required: `design_revision`, `feature_id`, `case_id`, `variant_id`, `checkpoint_id`, `run_id`. The execution workflow verifies that these actually exist in the frozen design and ReportBinding; the archive helper does not invent or resolve checkpoints. Each accepted screenshot record also contains:

```json
{
  "sequence": 1,
  "correction_attempt": 0,
  "raw_path": "screenshots/raw/TC-SYN-001__base__CP-result__01.png",
  "annotated_path": "screenshots/annotated/TC-SYN-001__base__CP-result__01.png",
  "raw_sha256": "<actual raw SHA256>",
  "annotated_sha256": "<actual annotated SHA256>",
  "viewport": {"width": 1920, "height": 1080},
  "full_page": false,
  "assertion": "Score 29 is red and displayed red count is 1",
  "focus": "Score cell and red-count total",
  "observed_note": "TC-SYN-001 / base / CP-result: score 29 is marked red; displayed count is 1.",
  "reviewed_by": "<agent or user who actually opened the pixels>",
  "reviewed_at": "<actual ISO timestamp including offset>",
  "source": {
    "capture_tool": "browser_take_screenshot",
    "raw_capture": "<actual raw capture call reference>",
    "annotated_capture": "<actual annotated capture call reference>",
    "annotation_method": "Temporary English top-right note in checked free space; native non-overlapping highlights; viewport capture",
    "pixel_review": {"tool": "<actual image viewer>", "reference": "<actual image-opening call reference>"}
  }
}
```

This example omits identity for brevity; a real record must include all six keys. No reviewer fields are auto-filled. Presence of these fields and valid hashes prove metadata consistency only; the agent must still genuinely inspect the pixels and note truth. Do not represent fixture records as human-reviewed product evidence.

## CLI

The same helper supports `create`, `resume`, `archive`, `evidence` and `event`, taking `--root` and a JSON **value** through `--json` (not a mandatory manifest file). `create` additionally takes `--feature-folder` and optional `--run-id`; `archive` takes `--source`, `--kind`, `--sequence`. See `--help` for exact arguments. Use shell-safe structured arguments/quoting; JSON serialization is not shell escaping. Python callers can use the functions directly to avoid quoting large metadata.

Archive raw before adding any note, annotated after adding note/highlight, and both before the next capture. The helper rejects mismatched states/times/receipts but cannot inspect whether the browser was truly unchanged; record the observation honestly. Keep rejected evidence and original MCP output. Do not delete raw files, rewrite an existing run or auto-sync reports. Local files may contain sensitive data: only reviewed, appropriate evidence is embedded in its matching TC/Checkpoint in Testcases.
