"""Task-template controls; runtime intent/research quality is separate proof."""
import hashlib
import json
import re
from pathlib import Path

from test_kit import check_identity, load_registry, mapping, validate_markdown


def rejected(call, name):
    try:
        call()
    except ValueError:
        return
    raise AssertionError(f"Invalid task control accepted: {name}")


def run(root: Path) -> list[str]:
    rows = load_registry(root)
    families = ("research", "split-tasks", "acceptance-criteria",
                "business-questions", "database-design")
    required_labels = {
        ("research", "vi"): ("Nguồn", "Căn cứ", "Chủ đề", "Mục đích", "Phạm vi", "Tính hiện hành", "Luồng hiện tại", "Ảnh hưởng", "Phụ thuộc", "Bằng chứng"),
        ("research", "ja"): ("参照元", "根拠", "主題", "目的", "対象範囲", "現行性", "現行フロー", "影響", "依存", "証拠"),
        ("split-tasks", "vi"): ("Nguồn", "Phạm vi", "Màn hình chính", "Phạm vi thay đổi"),
        ("split-tasks", "ja"): ("参照元", "対象範囲", "メイン画面", "変更範囲"),
        ("acceptance-criteria", "vi"): ("Nguồn", "Phạm vi"),
        ("acceptance-criteria", "ja"): ("参照元", "対象範囲"),
        ("business-questions", "vi"): ("Nguồn", "Phạm vi", "Tình huống", "Điều cần quyết định", "Ảnh hưởng", "Phương án", "Đề xuất", "Câu xác nhận", "Trạng thái"),
        ("business-questions", "ja"): ("参照元", "対象範囲", "状況", "判断事項", "影響", "選択肢", "提案", "確認依頼", "状態"),
        ("database-design", "vi"): ("Nguồn", "Phạm vi", "Nhận diện", "Quan hệ", "Ràng buộc", "Đọc và ghi", "Vòng đời", "Tương thích", "Kiểm chứng"),
        ("database-design", "ja"): ("参照元", "対象範囲", "識別", "関係", "制約", "読み書き", "ライフサイクル", "互換性", "検証"),
    }
    for family in families:
        for language in ("ja", "vi"):
            row = mapping(rows, family, language)
            text = (root / row["Template"]).read_text(encoding="utf-8")
            validate_markdown(text, row, required_fields=required_labels[family, language])
            assert "Required schema:" in text, f"Missing field-schema instructions: {family}/{language}"
            for field in row["Fields"].split(","):
                assert field in text, f"Schema field absent: {family}/{language}/{field}"

    # Completed, synthetic Research controls exercise actual fields/order, not just asset headings.
    for language, labels in (("vi", ("Nguồn", "Căn cứ", "Phạm vi")),
                             ("ja", ("参照元", "根拠", "対象範囲"))):
        current_row = mapping(rows, "research", language)
        # Explicit legacy control; never relabel pinned 1.0.0 files as current output.
        row = {**current_row, "Version": "1.0.0"}
        headings = row["Required sections"].split(";")
        good = "<!-- blend-template: research@1.0.0 -->\n# Synthetic research\n"
        good += "\n## " + headings[0] + "\n"
        good += "\n".join(f"- {label}: Synthetic source snapshot 1; no observed runtime." for label in labels)
        good += "\n" + "\n".join("\n## " + heading + "\nSynthetic assessed scope; no open gaps."
                                      for heading in headings[1:]) + "\n"
        validate_markdown(good, row, required_fields=labels)
        rejected(lambda: validate_markdown(good, current_row), "legacy passed as current Research")
        rejected(lambda: validate_markdown(good.replace(labels[0] + ":", "Other:"), row,
                                            required_fields=labels), "missing source field")
        rejected(lambda: validate_markdown(good.replace("research@1.0.0", "research@9.0.0"), row), "wrong template version")
        rejected(lambda: validate_markdown(good.replace("## " + headings[-1], "## Other"), row), "missing required section")
        wrong_order = good.replace("## " + headings[0], "## SWAP").replace("## " + headings[-1], "## " + headings[0]).replace("## SWAP", "## " + headings[-1])
        rejected(lambda: validate_markdown(wrong_order, row), "wrong required order")

    sql_row = mapping(rows, "sql-investigation", "neutral")
    sql = (root / sql_row["Template"]).read_text(encoding="utf-8")
    check_identity(sql, sql_row)
    for label in ("Question", "Basis", "Parameters", "Query", "No execution", "Limitations"):
        assert f"-- {label}:" in sql, f"SQL draft field missing: {label}"
    assert "DRAFT — NOT EXECUTED" in sql and "NOT READY TO RUN" in sql
    rejected(lambda: check_identity(sql.replace("sql-investigation@1.0.0", "research@1.0.0"), sql_row), "wrong SQL family")
    rejected(lambda: mapping(rows, "database-design-ddl", "neutral"), "unmapped executable DDL output")

    inputs = Path(__file__).parent / "inputs"
    oracle = json.loads((inputs / "scorer-only/oracle.json").read_text(encoding="utf-8"))
    assert set(oracle["scenarios"]) == {"S01", "S02", "S04"}
    expected_triggers = {"S01": (False, False), "S02": (False, True), "S04": (False, False)}
    for scenario_id, case in oracle["scenarios"].items():
        pack = inputs / case["writer_pack"]
        spec = (pack / "SPEC.md").read_text(encoding="utf-8")
        context = (pack / "CONTEXT.md").read_text(encoding="utf-8")
        confirmation = (pack / "confirmation.md").read_text(encoding="utf-8")
        assert case["identity"] in spec and case["identity"] in context
        assert "synthetic" in spec.lower() and "synthetic" in confirmation.lower()
        assert all(f"- {clause}:" in spec for clause in case["clauses"]), "Scorer oracle clause lacks raw source"
        assert (case["test_spec_trigger"], case["database_design_trigger"]) == expected_triggers[scenario_id]
        assert case["preserved"] and case["source_state"] and case["trigger_reason"]
        snapshot = (pack / "SNAPSHOT.md").read_text(encoding="utf-8")
        source_hashes = re.findall(r"^\| ([^|]+) \| ([a-f0-9]{64}) \|$", snapshot, re.M)
        assert len(source_hashes) == 6, "Incomplete pinned raw source inventory"
        for relative_path, pinned_hash in source_hashes:
            source_path = (pack / relative_path).resolve()
            assert source_path.is_relative_to(pack.resolve())
            assert hashlib.sha256(source_path.read_bytes()).hexdigest() == pinned_hash, f"Snapshot drift: {relative_path}"
        assert "scorer-only/oracle.json" in snapshot and "not a Git checkout" in snapshot

    # Independent facts challenge superseded business expectations and attachment authority.
    assert "Permit past calendar dates" in (inputs / "db-change/confirmation.md").read_text(encoding="utf-8")
    assert "Always invoke the test generator" in (inputs / "negation/SPEC.md").read_text(encoding="utf-8")
    assert not any(path.name == "oracle.json" for pack in ("task-only", "db-change", "negation")
                   for path in (inputs / pack).rglob("*")), "Scorer oracle leaked into writer pack"

    return ["10 Task Markdown assets and one SQL asset match registry versions, required headings and field schema",
            "synthetic JA/VI completed Research controls reject missing source, wrong version, missing section and reordered sections",
            "SQL draft labels/no-execution metadata and unsupported-DDL mapping controls",
            "three persisted raw synthetic source packs: S01 task-only/no-DB, S02 DB-change/latest confirmation, S04 attachment instruction/negation; 18 pinned source hashes and separate clause-level scorer oracle",
            "structural proof only: semantic invocation/negation, conditional DB decisions, source fidelity and agent research quality need actual runtime evaluation"]
