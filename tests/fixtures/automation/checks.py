"""Archive/provenance fixture checks, not browser, image or application proof."""
import base64
import copy
import importlib.util
import hashlib
import json
from pathlib import Path
import sys
import tempfile


def rejected(call, label):
    try:
        call()
    except (ValueError, FileExistsError, OSError):
        return
    raise AssertionError(f"Invalid archive accepted: {label}")


def execution_controls(root, archive, fixture='scenario-grouping'):
    """Exercise real source/binding/writeback state; replay itself remains simulated."""
    from openpyxl import load_workbook
    scripts = root / 'skills/blend-generate-test-spec/scripts'
    sys.path.insert(0, str(scripts))
    import export_report
    import report_model
    import update_report
    source = root / 'tests/fixtures/test-spec/inputs' / fixture
    replay_root = root / 'tests/fixtures/automation/inputs/execution-controls'
    replay = json.loads((replay_root / 'observations.json').read_text(encoding='utf-8'))
    saved = json.loads((replay_root / 'saved-report.json').read_text(encoding='utf-8'))
    controls = json.loads((replay_root / 'capability-controls.json').read_text(encoding='utf-8'))
    source_hashes = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('*.md')}
    data, _ = report_model.prepare_report(source, 'vi')
    if fixture == 'compact-scenario':
        replay['identity']['design_revision'] = data.summary['revision']
    assert data.report_version == '2.5.0'
    inventory = {(row.case_id, row.variant) for row in data.rows}
    assert len(inventory) == 9 and all(not row.eligible for row in data.rows)
    assert inventory == {(r['case_id'], r['variant_id']) for r in saved['rows']}
    assert replay['live_mcp_proof'] is False and controls['parser_conformance_proof'] is False
    with tempfile.TemporaryDirectory(prefix='blend execution controls ') as folder:
        folder = Path(folder)
        report = folder / 'disposable-scenario-report.xlsx'
        export_report.export(source, report)
        binding = update_report.report_bindings(source, report)
        assert binding['schema_version'] == data.report_version
        assert binding['design_revision'] == replay['identity']['design_revision']
        assert binding['feature_id'] == replay['identity']['feature_id']
        for event in replay['events'] + replay['resume_events']:
            if 'case_id' in event:
                target = event['case_id'] + ' / ' + event['variant_id']
                assert target in binding['variants']
                if 'checkpoint_id' in event:
                    assert event['checkpoint_id'] in binding['variants'][target]['checkpoints']
        identity = {k: replay['identity'][k] for k in ('design_revision', 'feature_id', 'run_id')}
        identity.update(case_id='TC-SC-01', variant_id='lt')
        actual = 'CP-setup: threshold30 and comparator< verified.\nCP-result:29 and30 red;31 not red;total2. Observation-only Draft; disagrees with oracle; pixel evidence unavailable.'
        update_report.update_report(source, report, {'identity': identity, 'status': 'FAIL', 'actual': actual})
        # A later independent variant can still receive a truthful partial result.
        next_identity = {**identity, 'variant_id': 'le'}
        partial = 'CP-setup: threshold30 and comparator≤ verified.\nCP-result:29 and30 red;31 not red;total2. Observation pending reviewed screenshot evidence; user stopped writeback.'
        update_report.update_report(source, report, {'identity': next_identity, 'status': 'NOT RUN', 'actual': partial})
        book = load_workbook(report)
        sheet = book[binding['sheet']]
        locale = report_model.REPORT_LAYOUTS['vi']['statuses']
        for target, fields in binding['variants'].items():
            if fixture == 'compact-scenario':
                assert fields['actual_cell'].startswith('D') and fields['status_cell'].startswith('E')
                assert not sheet.row_dimensions[sheet[fields['status_cell']].row].hidden
            if target == 'TC-SC-01 / lt':
                assert sheet[fields['status_cell']].value == locale['FAIL']
                assert sheet[fields['actual_cell']].value == actual
            elif target == 'TC-SC-01 / le':
                assert sheet[fields['status_cell']].value == locale['NOT RUN']
                assert sheet[fields['actual_cell']].value == partial
            else:
                assert sheet[fields['status_cell']].value == locale['NOT RUN']
                assert sheet[fields['actual_cell']].value is None
        before = report.read_bytes()
        rejected(lambda: update_report.update_report(source, report, {'identity': next_identity, 'status': 'PASS', 'actual': partial, 'evidence': []}), 'PASS without reviewed screenshot checkpoints')
        rejected(lambda: update_report.update_report(source, report, {'identity': {**identity, 'design_revision': 'other'}, 'status': 'FAIL', 'actual': actual}), 'stale writeback')
        assert report.read_bytes() == before
        checked = report_model.prepare_report(source, 'vi')[0]
        assert all(not row.eligible for row in checked.rows), 'Observation does not promote readiness'
        # Stop/resume persists inventory and pending state without changing report rows.
        context = folder / 'context'
        feature = context / 'features/SYN-SC-controls'
        feature.mkdir(parents=True)
        (feature / 'README.md').write_text('Synthetic feature SYN-SC', encoding='utf-8')
        (feature / 'CONTEXT.md').write_text('Synthetic execution controls', encoding='utf-8')
        meta = {'design_revision': data.summary['revision'], 'feature_id': 'SYN-SC', 'report': str(report),
                'inventory': [{'case_id': case, 'variant_id': variant} for case, variant in sorted(inventory)]}
        run_dir = archive.create_run(context, 'SYN-SC-controls', meta, identity['run_id'])
        archive.append_record(run_dir, {'kind': 'stop', 'pending': 'TC-SC-02 / cancel', 'cleanup': 'TD-SC reset verified', 'pending_writeback': 'TC-SC-01 / le'})
        assert archive.resume_run(run_dir, {**meta, 'feature_folder': 'SYN-SC-controls', 'run_id': identity['run_id']})['inventory'] == meta['inventory']
        assert archive.records(run_dir)[-1]['pending_writeback'] == 'TC-SC-01 / le'
        assert report.read_bytes() == before, 'Resume must not silently replace previous failure'
    assert source_hashes == {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in source_hashes}
    return [f'{fixture}: current report{data.report_version} binding validates nine-variant inventory and synthetic replay checkpoint identities',
            'same-file failure then independent partial writeback preserves untouched NOT RUN, source eligibility and original history',
            'missing screenshot proof/stale revision reject without report mutation; stop/resume ledger keeps pending work',
            'raw event replay and capability excerpts are synthetic semantic-evaluation inputs, not actual agent/browser/native Sheets proof']


def run(root: Path) -> list[str]:
    helper = root / "skills/blend-automation-test/scripts/run_artifacts.py"
    spec = importlib.util.spec_from_file_location("fixture_run_artifacts", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Small synthetic bytes: metadata-valid is deliberately NOT pixel-reviewed proof.
    png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
    metadata = {"design_revision": "synthetic-r1", "feature_id": "SYN-042", "report": "disposable-report.xlsx",
                "inventory": [{"case_id": "TC-SYN-001", "variant_id": "base"}]}
    with tempfile.TemporaryDirectory(prefix="blend automation archive ") as directory:
        metadata['report'] = str(Path(directory) / 'disposable-report.xlsx')
        context = Path(directory) / "context with spaces"
        feature = context / "features/SYN-042-archive"
        feature.mkdir(parents=True)
        (feature / "README.md").write_text("Synthetic feature SYN-042", encoding="utf-8")
        (feature / "CONTEXT.md").write_text("Synthetic archival control", encoding="utf-8")
        run_dir = module.create_run(context, "SYN-042-archive", metadata, "2026-10-05-001")
        saved = {**metadata, "feature_folder": "SYN-042-archive", "run_id": run_dir.name}
        assert module.resume_run(run_dir, saved)["report"] == metadata["report"]
        for key in ("design_revision", "feature_id", "report", "feature_folder", "run_id"):
            rejected(lambda key=key: module.resume_run(run_dir, {**saved, key: "other"}), f"resume {key}")
        rejected(lambda: module.create_run(context, "SYN-042-archive", metadata, run_dir.name), "exclusive run")
        for path in ("../SYN-042-archive", "CON", "folder/child", "trailing.", "a\\b", "a:b"):
            rejected(lambda path=path: module.create_run(context, path, metadata), path)
        rejected(lambda: module.create_run(context, "missing-feature", metadata), "missing verified folder")
        source = Path(directory) / "returned.png"
        source.write_bytes(png)
        identity = {key: saved[key] for key in ("design_revision", "feature_id", "run_id")}
        identity.update(case_id="TC-SYN-001", variant_id="base", checkpoint_id="CP-result")
        capture = {"full_page": True, "viewport": {"width": 1920, "height": 1080},
                   "observed_state": "Synthetic fixture state", "annotation_present": False,
                   "captured_at": "2026-10-05T12:00:00+07:00", "capture_reference": "fixture-raw-call"}
        rejected(lambda: module.archive_capture(run_dir, source, identity, "annotated", 1,
                                              {**capture, "annotation_present": True}), "annotated before raw archive")
        raw = module.archive_capture(run_dir, source, identity, "raw", 1, capture)
        assert (run_dir / raw["path"]).read_bytes() == png == source.read_bytes()
        source.write_bytes(png + b"synthetic later capture")
        annotated_capture = {**capture, "annotation_present": True, "captured_at": "2026-10-05T12:00:01+07:00",
                             "capture_reference": "fixture-annotated-call"}
        annotated = module.archive_capture(run_dir, source, identity, "annotated", 1, annotated_capture)
        assert (run_dir / raw["path"]).read_bytes() == png, "Reused MCP source must not overwrite prior raw archive"
        assert annotated["sha256"] != raw["sha256"]
        rejected(lambda: module.archive_capture(run_dir, source, identity, "raw", 1, capture), "no overwrite")
        for invalid in ({**capture, "full_page": None}, {**capture, "full_page": 0}, {**capture, "full_page": "false"}, {**capture, "annotation_present": True},
                        {**capture, "viewport": {"width": 0, "height": 1080}},
                        {**capture, "captured_at": "2026-10-05T12:00:00"}):
            rejected(lambda invalid=invalid: module.archive_capture(run_dir, source, identity, "raw", 2, invalid), "capture metadata")
        rejected(lambda: module.archive_capture(run_dir, source, identity, "raw", 5,
                                              {**capture, "correction_attempt": 4}), "correction budget")
        fifth = module.archive_capture(run_dir, source, identity, "raw", 5, capture)
        assert fifth["sequence"] == 5, "Image ordinal is not the correction budget"
        module.archive_capture(run_dir, source, identity, "raw", 6, {**capture, "correction_attempt": 1})
        rejected(lambda: module.archive_capture(run_dir, source, identity, "raw", 7,
                                              {**capture, "correction_attempt": 1}), "reused checkpoint correction")
        rejected(lambda: module.archive_capture(run_dir, source, {**identity, "case_id": "../bad"}, "raw", 2, capture), "unsafe case ID")
        rejected(lambda: module.archive_capture(run_dir, source, {**identity, "run_id": "other"}, "raw", 2, capture), "wrong run")
        evidence = {**identity, "sequence": 1, "raw_path": raw["path"], "annotated_path": annotated["path"],
                    "raw_sha256": raw["sha256"], "annotated_sha256": annotated["sha256"],
                    "viewport": capture["viewport"], "full_page": True,
                    "assertion": "Synthetic assertion", "focus": "Synthetic region", "observed_note": "Synthetic fixture only; not product proof.",
                    "reviewed_by": "fixture-only", "reviewed_at": "2026-10-05T12:00:02+07:00",
                    "source": {"capture_tool": "fixture", "raw_capture": "fixture-raw-call", "annotated_capture": "fixture-annotated-call",
                               "annotation_method": "Synthetic metadata only", "pixel_review": {"tool": "fixture", "reference": "synthetic-control"}}}
        before = (run_dir / "run-summary.md").read_bytes()
        assert module.validate_evidence(evidence, run_dir, identity) == run_dir / annotated["path"]
        assert before == (run_dir / "run-summary.md").read_bytes(), "Validation must be read-only"
        rejected(lambda: module.validate_evidence(evidence, run_dir, {**identity, "variant_id": "wrong"}), "wrong binding")
        assert module.validate_evidence(evidence, run_dir, {**identity, "report": str(Path(metadata["report"]).resolve())}) == run_dir / annotated["path"]
        rejected(lambda: module.validate_evidence(evidence, run_dir, {**identity, "report": str(Path(directory) / "different-report.xlsx")}), "wrong authoritative report")
        rejected(lambda: module.validate_evidence(evidence, run_dir, {**identity, "report": "disposable-report.xlsx"}), "relative expected report")
        relative_run = module.create_run(context, 'SYN-042-archive', {**metadata, 'report': 'disposable-report.xlsx'}, '2026-10-05-002')
        relative_identity = {**identity, 'run_id': relative_run.name}
        try:
            module.validate_evidence({**evidence, 'run_id': relative_run.name}, relative_run, {**relative_identity, 'report': metadata['report']})
        except ValueError as error:
            assert 'absolute authoritative report paths' in str(error)
        else:
            raise AssertionError('Saved relative report must not bind an imported image to the current cwd')
        for key, value in (("full_page", False), ("raw_sha256", "bad"), ("annotated_path", "../returned.png"),
                           ("reviewed_by", ""), ("reviewed_at", "2026-10-05T11:59:00+07:00"), ("observed_note", "")):
            rejected(lambda key=key, value=value: module.validate_evidence({**evidence, key: value}, run_dir), key)
        missing_viewer = copy.deepcopy(evidence)
        missing_viewer["source"]["pixel_review"]["reference"] = ""
        rejected(lambda: module.validate_evidence(missing_viewer, run_dir), "missing viewer call")
        module.record_evidence(run_dir, evidence)
        module.append_record(run_dir, {"kind": "stop", "pending": "TC-SYN-002", "note": "Literal ```json in a string stays safe"})
        assert module.records(run_dir)[-1]["kind"] == "stop"
        assert module.records(run_dir)[-2]["kind"] == "evidence"
        tamper = run_dir / annotated["path"]
        original = tamper.read_bytes()
        tamper.write_bytes(original + b"tampered")
        rejected(lambda: module.validate_evidence(evidence, run_dir), "modified archived bytes")
        tamper.write_bytes(original)
        raw2 = module.archive_capture(run_dir, source, identity, "raw", 2, capture)
        changed_state = {**annotated_capture, "observed_state": "Different observed state"}
        annotated2 = module.archive_capture(run_dir, source, identity, "annotated", 2, changed_state)
        pair2 = {**evidence, "sequence": 2, "raw_path": raw2["path"], "annotated_path": annotated2["path"],
                 "raw_sha256": raw2["sha256"], "annotated_sha256": annotated2["sha256"]}
        rejected(lambda: module.validate_evidence(pair2, run_dir), "raw/annotated state drift")
        # Both current viewport captures and truthful legacy full-page captures remain valid.
        viewport_raw = module.archive_capture(run_dir, source, identity, "raw", 8, {**capture, "full_page": False})
        viewport_annotated = module.archive_capture(run_dir, source, identity, "annotated", 8,
                                                  {**annotated_capture, "full_page": False})
        viewport_evidence = {**evidence, "sequence": 8, "full_page": False,
                             "raw_path": viewport_raw["path"], "annotated_path": viewport_annotated["path"],
                             "raw_sha256": viewport_raw["sha256"], "annotated_sha256": viewport_annotated["sha256"]}
        assert module.validate_evidence(viewport_evidence, run_dir) == run_dir / viewport_annotated["path"]
        for invalid_scope in (True, None, 0, "false"):
            rejected(lambda invalid_scope=invalid_scope: module.validate_evidence(
                {**viewport_evidence, "full_page": invalid_scope}, run_dir), "misreported viewport scope")
        mixed_raw = module.archive_capture(run_dir, source, identity, "raw", 9, {**capture, "full_page": False})
        mixed_annotated = module.archive_capture(run_dir, source, identity, "annotated", 9, annotated_capture)
        mixed_evidence = {**evidence, "sequence": 9, "raw_path": mixed_raw["path"],
                          "annotated_path": mixed_annotated["path"], "raw_sha256": mixed_raw["sha256"],
                          "annotated_sha256": mixed_annotated["sha256"]}
        rejected(lambda: module.validate_evidence(mixed_evidence, run_dir), "raw/annotated capture scope drift")
        export = Path(directory) / "application.xlsx"
        export.write_bytes(b"Synthetic downloaded file; not real XLSX proof")
        receipt = module.archive_capture(run_dir, export, identity, "export", 1, capture)
        assert receipt["path"].startswith("exports/") and (run_dir / receipt["path"]).read_bytes() == export.read_bytes()
        # Symlink support depends on platform rights; test whenever it is available.
        linked = run_dir / "screenshots/raw/linked.png"
        try:
            linked.symlink_to(source)
        except OSError:
            pass
        else:
            rejected(lambda: module.bounded(run_dir, linked), "symlink")
        assert len(list(run_dir.glob("*.md"))) == 1 and not list(run_dir.rglob("*.json")), "One ledger, no manifest"
    return ["exclusive feature/run paths, source-preserving no-overwrite archives and SHA256 readback pass",
            "viewport and legacy full-page scope truth, raw-before-annotation, three-correction budget, offset times and resume identity controls pass",
            "read-only shared evidence validation rejects wrong bindings, digest/state drift and absent pixel-review provenance",
            "synthetic fixture metadata tests only; browser target correctness, genuine pixel review and app export verification require runtime proof"] + execution_controls(root, module) + execution_controls(root, module, 'compact-scenario')
