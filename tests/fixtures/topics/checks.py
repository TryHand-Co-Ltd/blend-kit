"""Selected-topic structural/currentness controls; no agent or runtime proof."""
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path

from test_kit import check_identity, load_registry, mapping, validate_markdown, validate_output_filename


def rejected(call, name):
    try:
        call()
    except ValueError:
        return
    raise AssertionError(f"Invalid topic control accepted: {name}")


def identity(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def captured_delta(root: Path, captured: dict[str, str]) -> list[str]:
    # Fixture seam: compare selected file/dependency bytes, not all feature files.
    return [relative for relative, expected in captured.items()
            if not (root / relative).is_file() or identity(root / relative) != expected]


def run(root: Path) -> list[str]:
    base = Path(__file__).parent
    oracle = json.loads((base / "scorer-only/oracle.json").read_text(encoding="utf-8"))
    inputs = base / "inputs"
    pack = inputs / "runtime-input"
    rows = load_registry(root)
    labels = {
        "vi": ("Nguồn", "Căn cứ", "Chủ đề", "Mục đích", "Phạm vi", "Baseline code",
               "Nguồn được phép", "Tính hiện hành", "Luồng hiện tại", "Ảnh hưởng", "Phụ thuộc", "Bằng chứng"),
        "ja": ("参照元", "根拠", "主題", "目的", "対象範囲", "Code baseline",
               "許可された参照元", "現行性", "現行フロー", "影響", "依存", "証拠"),
    }
    assert len(oracle["selected_topics"]) == 2 and len(oracle["dependencies"]) == 4
    assert set(oracle["captured"]) == set(oracle["selected_topics"] + oracle["dependencies"])
    assert captured_delta(pack, oracle["captured"]) == [], "Pinned raw topic/dependency drift"
    for language in ("ja", "vi"):
        row = mapping(rows, "research", language)
        assert row["Version"] == "1.1.0"
        template = (root / row["Template"]).read_text(encoding="utf-8")
        validate_markdown(template, row, required_fields=labels[language])
        for field in row["Fields"].split(","):
            assert field in template, f"Template semantic field omitted: {field}"
        relative = next(p for p in oracle["selected_topics"] if p.endswith(f".{language}.md"))
        validate_output_filename(relative, row)
        text = (pack / relative).read_text(encoding="utf-8")
        validate_markdown(text, row, required_fields=labels[language])
        for label in labels[language]:
            missing = re.sub(r"^- " + re.escape(label) + r":.*$", f"- {label}:", text, flags=re.M)
            rejected(lambda missing=missing: validate_markdown(missing, row, required_fields=labels[language]),
                     f"empty {language} field {label}")
        rejected(lambda: validate_markdown(text.replace("research@1.1.0", "research@1.0.0"), row),
                 "legacy marker as current output")
        rejected(lambda: validate_output_filename(f"tasks/SYN-TOP-042-A/research.{language}.md", row),
                 "topic under task folder")
        for path in (f"research/<topic>.{language}.md", f"research/nested/flow.{language}.md",
                     f"research/../flow.{language}.md", f"research/flow_notes.{language}.md"):
            rejected(lambda path=path: validate_output_filename(path, row), "invalid basename")
        dep_rows = re.findall(r"^\| ([^|]+) \| ([a-f0-9]{64}) \| C-BOUNDARY \|$", text, re.M)
        assert dict(dep_rows) == {p: oracle["captured"][p] for p in oracle["dependencies"]}

    handoff = (pack / "handoff.md").read_text(encoding="utf-8")
    fields = re.findall(r"^- ([a-z_]+):", handoff, re.M)
    assert fields == ["source", "authorized_sources", "source_basis", "code_baseline",
                      "research_snapshot", "languages", "output_scope", "limitations"]
    pinned = re.findall(r"^\| ([^|]+) \| ([a-f0-9]{64}) \| threshold boundary / C-BOUNDARY \|$", handoff, re.M)
    assert dict(pinned) == oracle["captured"], "Handoff does not pin actual selected bytes/dependencies"
    assert "export-caption.vi.md" not in handoff and "Mode: design" in handoff
    for value in oracle["identity"].values():
        assert value in (pack / "README.md").read_text(encoding="utf-8")
        assert value in handoff

    with tempfile.TemporaryDirectory(prefix="blend topic relocation ") as directory:
        relocated = Path(directory) / "renamed feature with spaces"
        shutil.copytree(pack, relocated)
        assert captured_delta(relocated, oracle["captured"]) == [], "Relocation invalidated identical bytes"
        for control in oracle["controls"]:
            destination = relocated / control["destination"]
            previous = destination.read_bytes() if destination.is_file() else None
            shutil.copyfile(inputs / "changes" / control["overlay"], destination)
            assert captured_delta(relocated, oracle["captured"]) == control["changed"], control["name"]
            if control["name"] == "selected-topic-changed":
                recaptured = {**oracle["captured"], control["destination"]: identity(destination)}
                assert captured_delta(relocated, recaptured) == [], "Recaptured bytes should match even when conclusion is wrong"
                assert "score 60 là đỏ" in destination.read_text(encoding="utf-8")
                assert "Equality is not classified red" in (relocated / "sources/confirmation.md").read_text(encoding="utf-8")
                # Byte identities cannot settle this contradiction; the separate oracle requires semantic challenge.
            if previous is None:
                destination.unlink()
            else:
                destination.write_bytes(previous)
        missing = relocated / oracle["selected_topics"][0]
        missing.unlink()
        assert captured_delta(relocated, oracle["captured"]) == [oracle["selected_topics"][0]]
    assert captured_delta(pack, oracle["captured"]) == [], "Control mutated frozen fixture inputs"

    legacy = inputs / "legacy-input/research.vi.md"
    legacy_text = legacy.read_text(encoding="utf-8")
    assert identity(legacy) == oracle["legacy_identity"]
    legacy_row = {**mapping(rows, "research", "vi"), "Version": "1.0.0"}
    validate_markdown(legacy_text, legacy_row, required_fields=("Nguồn", "Căn cứ", "Phạm vi"))
    rejected(lambda: validate_markdown(legacy_text, mapping(rows, "research", "vi")), "flat legacy current output")
    sql_row = mapping(rows, "sql-investigation", "neutral")
    check_identity((root / sql_row["Template"]).read_text(encoding="utf-8"), sql_row)
    validate_output_filename("research/SYN-TOP-042-A-threshold-boundary.sql", sql_row)
    assert sql_row["Version"] == "1.0.0"
    for input_root in oracle["model_input_roots"]:
        assert not any("oracle" in p.name or "scorer-only" in p.parts for p in (base / input_root).rglob("*")), "Oracle leaked into model inputs"
    assert "C-BOUNDARY" in (pack / "sources/spec.md").read_text(encoding="utf-8")
    assert "$score < $threshold" in (pack / "Blend-source/application/models/Score.php").read_text(encoding="utf-8")
    assert "$score <= $threshold" in (inputs / "changes/Score.php").read_text(encoding="utf-8")
    assert "threshold is 55" in (inputs / "changes/confirmation.md").read_text(encoding="utf-8")
    for reference in ("review-policy", "bug-hunter"):
        path = root / f"skills/blend-review-artifacts/references/{reference}.md"
        assert f"../../../shared/{reference}.md" in path.read_text(encoding="utf-8")

    return ["JA/VI topic 1.1.0 assets and completed raw topics enforce required localized fields, sections, markers and feature-root basenames",
            "eight-field handoff pins two actual topics and four source/context/confirmation/code dependencies; renamed/spaced-root relocation preserves captured identities",
            "selected topic, confirmation, code and missing-file controls produce scoped deltas; unrelated topic addition/edit produces none; frozen inputs preserved",
            "original flat 1.0.0 control remains read-only and rejected as current output; SQL mapping stays 1.0.0; common policy/protocol pointers resolve",
            "raw synthetic model packs and separate scorer oracle retained; identity comparisons are fixture proof, not semantic agent reuse, runtime or publication proof"]
