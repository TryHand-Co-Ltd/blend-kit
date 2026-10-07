"""Exclusive local run archives and a Markdown ledger; never drives a browser.

Review metadata records an actual viewer call supplied by the executing agent.
This helper checks identity/bytes/metadata, not the truth of a pixel review.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import stat

IDENTITY = ("design_revision", "feature_id", "case_id", "variant_id", "checkpoint_id", "run_id")
RUN_KEYS = ("design_revision", "feature_id", "report")
LOCAL_ZONE = timezone(timedelta(hours=7), "Asia/Saigon")


def component(value: str) -> str:
    """Validate rather than silently rename source IDs or path components."""
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", value):
        raise ValueError("Unsafe path component")
    if value.endswith(".") or value.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}:
        raise ValueError("Reserved path component")
    return value


def bounded(root: Path, path: Path) -> Path:
    root, path = root.absolute(), path.absolute()
    if not path.is_relative_to(root):
        raise ValueError("Archive target escapes its root")
    for selected in (root, *[root.joinpath(*path.relative_to(root).parts[:i]) for i in range(1, len(path.relative_to(root).parts) + 1)]):
        if selected.exists() or selected.is_symlink():
            info = selected.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
                raise ValueError("Symlink/junction archive component")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Resolved archive target escapes its root")
    return path


def text(value, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing {label}")
    return value


def offset_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(text(value, "timestamp"))
    if parsed.utcoffset() is None:
        raise ValueError("Timestamp requires an offset")
    return parsed


def records(run: Path) -> list[dict]:
    run = Path(run).absolute()
    if run.parent.parent.name != "test-output" or run.parent.parent.parent.name != "local":
        raise ValueError("Run must live under local/test-output/<feature>/<run-id>")
    run = bounded(run.parents[3], run)
    ledger = bounded(run, run / "run-summary.md")
    contents = ledger.read_text(encoding="utf-8")
    chunks = re.findall(r"^```json\n(.*?)\n```$", contents, flags=re.S | re.M)
    if len(re.findall(r"^```json$", contents, flags=re.M)) != len(chunks):
        raise ValueError("Incomplete ledger entry; inspect before resume")
    result = [json.loads(chunk) for chunk in chunks]
    if not result or result[0].get("kind") != "run":
        raise ValueError("Missing run identity")
    return result


def append_record(run: Path, record: dict) -> None:
    ledger = bounded(run, run / "run-summary.md")
    serialized = json.dumps(record, ensure_ascii=False, sort_keys=True)
    # One writer per run, as in the report contract. No hidden manifest or DB.
    with ledger.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(f"\n```json\n{serialized}\n```\n")
        stream.flush()
        __import__("os").fsync(stream.fileno())


def checkpoint_observations(run: Path, expected: dict) -> dict:
    """Read internal proof separately from the report's reader-facing Actual."""
    entries = records(run)
    for key in (*RUN_KEYS, 'run_id'):
        same = (Path(entries[0].get(key,'')).resolve()==Path(expected.get(key,'')).resolve()
                if key=='report' else entries[0].get(key)==expected.get(key))
        if not same:
            raise ValueError('Checkpoint ledger identity mismatch: '+key)
    if run.name != expected['run_id'] or run.parent.name != entries[0].get('feature_folder'):
        raise ValueError('Checkpoint ledger directory identity mismatch')
    result = {}
    for entry in entries[1:]:
        if entry.get('kind') != 'checkpoint-observations':
            continue
        for key in ('design_revision','feature_id','run_id'):
            if entry.get(key) != expected[key]:
                raise ValueError('Checkpoint observation identity mismatch: '+key)
        target = component(entry.get('case_id'))+' / '+component(entry.get('variant_id'))
        values = entry.get('observations')
        if not isinstance(values,dict):
            raise ValueError('Checkpoint observations must be an object')
        for cp,value in values.items():
            component(cp)
            text(value,cp)
        digest=entry.get('actual_sha256','')
        if not isinstance(digest,str) or not re.fullmatch(r'[a-f0-9]{64}',digest):
            raise ValueError('Checkpoint observations require Actual digest')
        result[target] = {'actual_sha256':digest,'observations':values}
    return result


def create_run(context_root: Path, feature_folder: str, metadata: dict, run_id: str | None = None) -> Path:
    context_root = bounded(Path(context_root), Path(context_root))
    feature_folder = component(feature_folder)
    feature = bounded(context_root, context_root / "features" / feature_folder)
    if not all(bounded(context_root, feature / name).is_file() for name in ("README.md", "CONTEXT.md")):
        raise ValueError("Expected existing verified feature README and CONTEXT")
    for key in RUN_KEYS:
        text(metadata.get(key), key)
    parent = bounded(context_root, context_root / "local" / "test-output" / feature_folder)
    parent.mkdir(parents=True, exist_ok=True)
    if run_id is None:
        prefix = datetime.now(LOCAL_ZONE).strftime("%Y-%m-%d")
        for number in range(1, 1000):
            candidate = f"{prefix}-{number:03d}"
            try:
                run = bounded(context_root, parent / candidate)
                run.mkdir()
                run_id = candidate
                break
            except FileExistsError:
                continue
        else:
            raise ValueError("No available Run ID on this local date")
    else:
        component(run_id)
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-\d{3}", run_id) or int(run_id[-3:]) == 0:
            raise ValueError("Run ID must use YYYY-MM-DD-NNN")
        datetime.strptime(run_id[:10], "%Y-%m-%d")
        run = bounded(context_root, parent / run_id)
        run.mkdir()  # Exclusive: never replaces an earlier run.
    for relative in ("screenshots/raw", "screenshots/annotated", "exports"):
        bounded(run, run / relative).mkdir(parents=True)
    with bounded(run, run / "run-summary.md").open("x", encoding="utf-8") as stream:
        stream.write("# Automation run ledger\n\nAuthoritative Actual/Status live in the selected report.\n")
    append_record(run, {**metadata, "kind": "run", "feature_folder": feature_folder, "run_id": run_id,
                        "created_at": datetime.now(LOCAL_ZONE).isoformat()})
    return run


def resume_run(run: Path, expected: dict) -> dict:
    saved = records(run)[0]
    for key in (*RUN_KEYS, "feature_folder", "run_id"):
        if saved.get(key) != expected.get(key):
            raise ValueError(f"Resume identity mismatch: {key}")
    if Path(run).name != saved["run_id"] or Path(run).parent.name != saved["feature_folder"]:
        raise ValueError("Run directory identity mismatch")
    return saved


def check_identity(run: Path, identity: dict) -> dict:
    saved = records(run)[0]
    selected = {key: text(identity.get(key), key) for key in IDENTITY}
    for key in ("design_revision", "feature_id", "run_id"):
        if selected[key] != saved[key]:
            raise ValueError(f"Artifact identity mismatch: {key}")
    for key in ("case_id", "variant_id", "checkpoint_id"):
        component(selected[key])
    return selected


def viewport(value: dict) -> dict:
    if not isinstance(value, dict) or any(type(value.get(key)) is not int or value[key] <= 0 for key in ("width", "height")):
        raise ValueError("Viewport requires positive integer width and height")
    return {key: value[key] for key in ("width", "height")}


def archive_capture(run: Path, source: Path, identity: dict, kind: str, sequence: int, metadata: dict) -> dict:
    identity = check_identity(run, identity)
    if kind not in ("raw", "annotated", "export") or type(sequence) is not int or sequence < 1:
        raise ValueError("Invalid archive kind/sequence")
    correction = metadata.get("correction_attempt", 0)
    if kind != "export":
        if type(correction) is not int or not 0 <= correction <= 3:
            raise ValueError("Evidence correction budget exceeded")
        if kind == "raw" and correction and any(item.get("kind") == "capture" and item.get("artifact_kind") == "raw"
                                                and item.get("correction_attempt") == correction
                                                and all(item.get(key) == value for key, value in identity.items())
                                                for item in records(run)):
            raise ValueError("Correction attempt already used for this checkpoint")
        if type(metadata.get("full_page")) is not bool:
            raise ValueError("Screenshot captures require an explicit boolean full_page scope")
        viewport(metadata.get("viewport"))
        text(metadata.get("observed_state"), "observed state")
        if metadata.get("annotation_present") is not (kind == "annotated"):
            raise ValueError("Raw must precede annotation; annotated must include it")
        if kind == "annotated" and not any(item.get("kind") == "capture" and item.get("artifact_kind") == "raw"
                                          and item.get("sequence") == sequence
                                          and all(item.get(key) == value for key, value in identity.items())
                                          for item in records(run)):
            raise ValueError("Archive the raw capture before annotating")
    offset_time(metadata.get("captured_at"))
    text(metadata.get("capture_reference"), "actual capture reference")
    source = bounded(Path(source).parent, Path(source))
    payload = source.read_bytes()
    if not payload:
        raise ValueError("Empty returned artifact")
    if kind != "export" and not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Screenshot is not a PNG")
    suffix = source.suffix.lower() if kind == "export" else ".png"
    if not re.fullmatch(r"\.[a-z0-9]{1,10}", suffix):
        raise ValueError("Unsafe export extension")
    name = "__".join(identity[key] for key in ("case_id", "variant_id", "checkpoint_id")) + f"__{sequence:02d}{suffix}"
    relative = f"exports/{name}" if kind == "export" else f"screenshots/{kind}/{name}"
    target = bounded(Path(run), Path(run) / relative)
    if any(item.get("kind") == "capture" and item.get("path", "").casefold() == relative.casefold() for item in records(run)):
        raise FileExistsError("Artifact name already archived")
    with target.open("xb") as stream:
        stream.write(payload)
    digest = hashlib.sha256(payload).hexdigest()
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest or hashlib.sha256(source.read_bytes()).hexdigest() != digest:
        raise ValueError("Source/archive digest changed; preserve files and inspect")
    receipt = {**metadata, **identity, "kind": "capture", "artifact_kind": kind, "sequence": sequence,
               "path": relative, "sha256": digest, "size": len(payload), "correction_attempt": correction}
    append_record(Path(run), receipt)
    return receipt


def validate_evidence(evidence: dict, run_dir: Path, identity: dict | None = None) -> Path:
    """Validate bytes/provenance and return the annotated path, without writing.

    Caller must actually open/review pixels before supplying review metadata.
    The report writer reuses this function; metadata is not pixel proof.
    """
    run = Path(run_dir)
    if identity is not None and any(evidence.get(key) != identity.get(key) for key in IDENTITY):
        raise ValueError("Evidence does not match the requested TestRunIdentity")
    if identity is not None and "report" in identity:
        expected_report = text(identity["report"], "authoritative report")
        saved_report = records(run)[0]["report"]
        def is_uri(value):
            return bool(re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value) and not re.match(r"^[A-Za-z]:[\\/]", value))
        if is_uri(saved_report) or is_uri(expected_report):
            same_report = saved_report == expected_report
        else:
            if not Path(saved_report).is_absolute() or not Path(expected_report).is_absolute():
                raise ValueError("Evidence imports require absolute authoritative report paths")
            same_report = Path(saved_report).resolve() == Path(expected_report).resolve()
        if not same_report:
            raise ValueError("Evidence run belongs to another authoritative report")
    identity = check_identity(run, evidence)
    sequence = evidence.get("sequence")
    correction = evidence.get("correction_attempt", 0)
    if type(sequence) is not int or sequence < 1 or type(evidence.get("full_page")) is not bool:
        raise ValueError("Invalid evidence capture sequence/full_page")
    if type(correction) is not int or not 0 <= correction <= 3:
        raise ValueError("Evidence correction budget exceeded")
    viewport(evidence.get("viewport"))
    for key in ("assertion", "focus", "observed_note", "reviewed_by"):
        text(evidence.get(key), key)
    review_time = offset_time(evidence.get("reviewed_at"))
    source = evidence.get("source")
    if not isinstance(source, dict):
        raise ValueError("Evidence source must describe actual capture and pixel-review calls")
    for key in ("capture_tool", "raw_capture", "annotated_capture", "annotation_method"):
        text(source.get(key), key)
    review = source.get("pixel_review", {})
    text(review.get("tool"), "pixel review tool")
    text(review.get("reference"), "actual pixel review reference")
    receipts = []
    for kind in ("raw", "annotated"):
        relative = text(evidence.get(f"{kind}_path"), f"{kind} path")
        expected_parent = f"screenshots/{kind}/"
        if not relative.startswith(expected_parent) or "\\" in relative or any(part in ("", ".", "..") for part in relative.split("/")):
            raise ValueError("Evidence must use run-relative screenshot paths")
        target = bounded(Path(run), Path(run) / relative)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != evidence.get(f"{kind}_sha256"):
            raise ValueError("Evidence digest mismatch")
        matches = [item for item in records(run) if item.get("kind") == "capture" and item.get("path") == relative
                   and all(item.get(key) == value for key, value in identity.items()) and item.get("sequence") == sequence
                   and item.get("artifact_kind") == kind and item.get("sha256") == digest]
        if len(matches) != 1:
            raise ValueError("Evidence has no unique matching archive receipt")
        receipt = matches[0]
        if receipt["viewport"] != evidence["viewport"] or type(receipt.get("full_page")) is not bool or receipt["full_page"] != evidence["full_page"] or source[f"{kind}_capture"] != receipt["capture_reference"] or receipt["correction_attempt"] != correction:
            raise ValueError("Evidence capture metadata mismatch")
        if review_time < offset_time(receipt["captured_at"]):
            raise ValueError("Review cannot precede capture")
        receipts.append(receipt)
    if receipts[0]["observed_state"] != receipts[1]["observed_state"] or offset_time(receipts[0]["captured_at"]) > offset_time(receipts[1]["captured_at"]):
        raise ValueError("Raw/annotated must describe the same state in capture order")
    return bounded(run, run / evidence["annotated_path"])


def record_evidence(run: Path, evidence: dict) -> dict:
    validate_evidence(evidence, run)
    accepted = {**evidence, "kind": "evidence", "correction_attempt": evidence.get("correction_attempt", 0)}
    append_record(Path(run), accepted)
    return accepted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("create", "resume", "archive", "evidence", "event"))
    parser.add_argument("--root", type=Path, required=True, help="Context root for create; run directory otherwise")
    parser.add_argument("--feature-folder")
    parser.add_argument("--run-id")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--kind", choices=("raw", "annotated", "export"))
    parser.add_argument("--sequence", type=int)
    parser.add_argument("--json", required=True, help="JSON metadata/identity or EvidenceRecord; never a manifest path")
    args = parser.parse_args()
    payload = json.loads(args.json)
    if args.action == "create":
        result = str(create_run(args.root, args.feature_folder, payload, args.run_id))
    elif args.action == "resume":
        result = resume_run(args.root, payload)
    elif args.action == "archive":
        result = archive_capture(args.root, args.source, payload, args.kind, args.sequence, payload)
    elif args.action == "evidence":
        result = record_evidence(args.root, payload)
    else:
        records(args.root)
        if payload.get("kind") in (None, "run", "capture", "evidence"):
            raise ValueError("Event requires its own ledger kind")
        append_record(args.root, payload)
        result = payload
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
