"""Six-skill conformance/integration controls; not actual model/runtime proof."""
import hashlib
import json
import re
import tempfile
from pathlib import Path

from test_kit import (AREAS, SKILLS, check_identity, inventory_gaps, load_registry, mapping,
                      resource_gaps, validate_markdown, validate_output, validate_output_filename, _gate)


def rejected(call, message):
    try:
        call()
    except (ValueError, FileNotFoundError):
        return
    raise AssertionError(f"Negative control was accepted: {message}")


def check_runtime_gate(root: Path, rows) -> None:
    """Exercise asset-derived inline/block and scoped-none completion controls."""
    def completed(family, language):
        row = mapping(rows, family, language)
        text = (root / row["Template"]).read_text(encoding="utf-8")
        text = re.sub(r"<!--(?!\s*blend-template:).*?-->", "", text, flags=re.S)
        return row, re.sub(r"\{\{.*?\}\}", "Scoped synthetic value; static control only", text, flags=re.S)

    def check(row, text):
        _gate.check_output(text, row["Filename"].replace("<scope>", "score-save"),
                           rows, row["Output type"], row["Language"], root)

    for language in ("ja", "vi"):
        for family, label in (("implementation-plan", "情報源リビジョン" if language == "ja" else "Revisions nguồn"),
                              ("code-review", "独立判定" if language == "ja" else "Kết luận độc lập")):
            row, text = completed(family, language)
            check(row, text)
            assert label + ": Scoped synthetic value; static control only" in text
            rejected(lambda: check(row, text.replace(label + ": Scoped synthetic value; static control only",
                                                     label + ":\n\n| Detail | Following table cannot fill inline summary |")),
                     "inline slot replaced by later block/table")
        row, text = completed("review", language)
        headings = row["Required sections"].split(";")
        none = "確認した対象artifact範囲に指摘なし。Static review only." if language == "ja" else "Không có findings trong phạm vi artifacts đã đọc; static review only."
        text = re.sub(r"## " + re.escape(headings[1]) + r".*?\n## " + re.escape(headings[2]),
                      f"## {headings[1]}\n\n{none}\n\n## {headings[2]}", text, flags=re.S)
        check(row, text)
        rejected(lambda: check(row, text.replace(none, "")), "empty findings section masquerading as none")
        rejected(lambda: check(row, text.replace("### Inventory", "### Inventory (selected)")), "fixed Inventory renamed")
    row, text = completed("split-tasks", "vi")
    check(row, text)
    label = "**Màn hình bị ảnh hưởng:**"
    block = label + "\n\n- Scoped synthetic value; static control only"
    assert block in text
    rejected(lambda: check(row, text.replace(block, label)), "empty prescribed block/list")
    rejected(lambda: check(row, text.replace(block, label + " Scoped synthetic value; static control only")),
             "prescribed list flattened to inline summary")


def check_plan_review(root: Path, rows) -> None:
    """Project captured synthetic basis through actual localized plan/report fields.

    This is a structural interoperability control, never a generated model output.
    Actual intended/changed-scope and origin controls remain in code-review fixtures.
    """
    fixture = root / "tests/fixtures/planning/inputs"
    approval_path = fixture / "cases/current/approval.md"
    approval = approval_path.read_text(encoding="utf-8")
    approved = re.findall(r"^\| (common/[^|]+) \| ([^|]+) \| ([^|]+) \| ([a-f0-9]{64}) \|$", approval, re.M)
    assert len(approved) == 2
    for current, captured, revision, digest in approved:
        assert hashlib.sha256((fixture / current).read_bytes()).hexdigest() == digest
        assert hashlib.sha256((fixture / captured).read_bytes()).hexdigest() == digest
        assert revision in (fixture / captured).read_text(encoding="utf-8")
    identity = re.search(r"^- Identity: (.+)$", approval, re.M).group(1)
    scope = re.search(r"^- Scope: (.+)$", approval, re.M).group(1)
    ac = (fixture / approved[1][0]).read_text(encoding="utf-8")
    selected = re.findall(r"^- (AC-T\d):", ac, re.M)
    assert selected == ["AC-T1", "AC-T2", "AC-T3"]
    source = "; ".join(f"{path}@{revision}:sha256:{digest}" for path, _, revision, digest in approved)
    approval_identity = "approval:sha256:" + hashlib.sha256(approval_path.read_bytes()).hexdigest()
    baseline_files = sorted((fixture / "common/application-source").rglob("*.php"))
    baseline = "; ".join(f"blend:{path.relative_to(fixture / 'common/application-source').as_posix()}:sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}" for path in baseline_files)
    review_input = fixture / "common/features/SYN-PL-02-notice-title/docs/artifact-review.vi.md"
    values = (identity, source, scope + "; " + ", ".join(selected), approval_identity,
              "artifact-review:REVIEW-2:sha256:" + hashlib.sha256(review_input.read_bytes()).hexdigest(), baseline,
              "No selected topics in this approved synthetic title-save scope")
    labels = {
        "vi": (("Danh tính", "Revisions nguồn", "Phạm vi đã duyệt", "Căn cứ phê duyệt", "Kết quả review", "Baseline code", "Phụ thuộc Research"),
               ("Danh tính", "Nguồn và revision plan", "Phạm vi nghiệp vụ dự kiến")),
        "ja": (("識別情報", "情報源リビジョン", "承認範囲", "承認根拠", "レビュー判定", "コード基準", "Research依存"),
               ("識別情報", "参照元・計画Revision", "予定業務範囲")),
    }

    def replace_value(text, label, value):
        pattern = r"(?m)^(- " + re.escape(label) + r":|" + re.escape(label) + r":|\| " + re.escape(label) + r" \|).*$"
        def replace(match):
            return match.group(1) + " " + value + (" |" if match.group(1).startswith("|") else "")
        changed, count = re.subn(pattern, replace, text)
        assert count == 1, f"Actual interface label missing/ambiguous: {label}"
        return changed

    def read_value(text, label):
        matches = re.findall(r"(?m)^(?:- " + re.escape(label) + r":|" + re.escape(label) + r":|\| " + re.escape(label) + r" \|) (.+)$", text)
        if len(matches) != 1 or not matches[0].removesuffix(" |").strip():
            raise ValueError(f"Missing/ambiguous actual basis field: {label}")
        return matches[0].removesuffix(" |")

    for language, (plan_labels, report_labels) in labels.items():
        plan_row = mapping(rows, "implementation-plan", language)
        report_row = mapping(rows, "code-review", language)
        plan = (root / plan_row["Template"]).read_text(encoding="utf-8")
        report = (root / report_row["Template"]).read_text(encoding="utf-8")
        for label, value in zip(plan_labels, values):
            plan = replace_value(plan, label, value)
        plan_digest = hashlib.sha256(plan.encode("utf-8")).hexdigest()
        report_values = (values[0], "plan:sha256:" + plan_digest + "; " + "; ".join(values[1:]), values[2])
        for label, value in zip(report_labels, report_values):
            report = replace_value(report, label, value)

        def consistent(candidate_plan, candidate_report):
            if hashlib.sha256(candidate_plan.encode("utf-8")).hexdigest() != plan_digest:
                raise ValueError("Review's captured plan identity is stale")
            actual = tuple(read_value(candidate_plan, label) for label in plan_labels)
            if actual != values:
                raise ValueError("Plan changed captured approval/source/identity/scope/code/topic basis")
            actual_report = tuple(read_value(candidate_report, label) for label in report_labels)
            if actual_report != report_values:
                raise ValueError("Review did not retain exact plan content identity and selected obligations")

        consistent(plan, report)
        validate_markdown(plan, plan_row, required_fields=plan_labels)
        validate_markdown(report, report_row, required_fields=report_labels)
        rejected(lambda: consistent(plan + "\nChanged planned outcome.\n", report), "plan body drift outside basis labels")
        for index, bad in ((0, identity.replace("immediate parent SYN-PL-02", "immediate parent SYN-PL-99")),
                           (1, source.replace(approved[1][3], "0" * 64)),
                           (2, "title-save+archive; AC-T1, AC-T2, AC-T3, AC-A1"),
                           (3, "Review PASS; no explicit approval"),
                           (5, "HEAD alone; dirty bytes not captured")):
            rejected(lambda index=index, bad=bad: consistent(replace_value(plan, plan_labels[index], bad), report),
                     "changed source/parent/scope/approval/baseline")
        rejected(lambda: consistent(plan, replace_value(report, report_labels[2], "title-save; AC-T1, AC-T2")),
                 "review omitted required AC-T3")
        rejected(lambda: consistent(plan, replace_value(report, report_labels[1], source)),
                 "review lost plan identity/approval/code basis")

    protocol = (root / "shared/bug-hunter.md").read_text(encoding="utf-8")
    fields = re.findall(r"^\| ([a-z_]+) \|", protocol, re.M)
    assert fields == ["candidate_id", "role", "run_identity", "backend", "independent", "basis",
                      "evidence", "counter_evidence", "verdict", "depth", "limits"]
    for language in ("ja", "vi"):
        report = (root / mapping(rows, "code-review", language)["Template"]).read_text(encoding="utf-8")
        assert re.findall(r"^\| ([a-z_]+) \|", report, re.M) == fields
    license_bytes = (root / "shared/bug-hunter-LICENSE.txt").read_bytes()
    assert license_bytes == (root / "skills/blend-review-artifacts/references/bug-hunter-LICENSE.txt").read_bytes()
    assert hashlib.sha256(license_bytes).hexdigest() == "363363d8c6255e2a4e68724b3e0ea4919ee651751af2b87ddfe9986a077e5b14"
    for skill in SKILLS:
        entry = (root / f"skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        assert "../../shared/workflow.md" in entry and "../../shared/artifact-formats.md" in entry

    # Actual synthetic changed surfaces exceed intended Score/Record/migration surfaces.
    raw = root / "tests/fixtures/code-review/inputs/implementation"
    metadata = json.loads((raw / "snapshot-metadata.json").read_text(encoding="utf-8"))
    base, current = metadata["files"]["base"], metadata["files"]["current"]
    changed = {path: current.get(path) for path in set(base) | set(current)
               if base.get(path) != current.get(path)}
    def exact_inventory(inventory):
        if inventory != changed:
            raise ValueError("Reported actual diff does not match per-file base/current captures")
    exact_inventory(changed)
    fake = {path: digest for path, digest in changed.items() if path.endswith(("Score.php", "Record_m.php", "score-method.sql"))}
    rejected(lambda: exact_inventory(fake), "intended plan files substituted for actual diff")
    untracked = metadata["working"]["untracked"][0]
    rejected(lambda: exact_inventory({path: digest for path, digest in changed.items() if path != untracked}),
             "untracked working change omitted")
    helper = "application/helpers/score_helper.php"
    before = (raw / "base" / helper).read_text(encoding="utf-8")
    after = (raw / "current" / helper).read_text(encoding="utf-8")
    assert "$score < $threshold" in before and "$score <= $threshold" in after
    assert before.split("function legacyAlias", 1)[1] == after.split("function legacyAlias", 1)[1]
    def supported_axes(shared_origin, shared_effect, legacy_origin):
        if (shared_origin, shared_effect, legacy_origin) != ("INTRODUCED", "Regression blocker", "PRE_EXISTING"):
            raise ValueError("Finding attribution/effect contradicts inspected base/current evidence")
    supported_axes("INTRODUCED", "Regression blocker", "PRE_EXISTING")
    rejected(lambda: supported_axes("PRE_EXISTING", "Follow-up", "PRE_EXISTING"), "OOS new regression excused as old")
    rejected(lambda: supported_axes("INTRODUCED", "Regression blocker", "INTRODUCED"), "unchanged unrelated legacy defect falsely attributed")


def run(root: Path) -> list[str]:
    rows = load_registry(root)
    expected_families = {
        "research", "split-tasks", "acceptance-criteria", "business-questions",
        "database-design", "sql-investigation", "scope-and-approach", "test-cases",
        "test-data", "test-report", "review", "implementation-plan", "code-review", "validation-report",
    }
    assert {row["Family"] for row in rows} == expected_families, "Output family omitted or unapproved"
    bilingual = expected_families - {"sql-investigation", "test-report", "validation-report"}
    for family in bilingual:
        ja = mapping(rows, family, "ja")
        vi = mapping(rows, family, "vi")
        for field in ("Family", "Version", "Fields", "Optional / conditional rule", "Validation"):
            assert ja[field] == vi[field], f"Bilingual schema drift: {family}/{field}"
        assert len(ja["Required sections"].split(";")) == len(vi["Required sections"].split(";"))
        for language, row in (("ja", ja), ("vi", vi)):
            assert row["Filename"].endswith(f".{language}.md")
            assert row["Template"].endswith(f"-template.{language}.md")
    workbook_pair = [mapping(rows, "test-report", language) for language in ("ja", "vi")]
    for field in ("Family", "Version", "Fields", "Required sections", "Optional / conditional rule", "Validation"):
        assert workbook_pair[0][field] == workbook_pair[1][field], f"Report schema drift: {field}"
    for row in workbook_pair:
        assert row["Filename"] == f"test-report.{row['Language']}.xlsx"
        assert row["Template"].endswith(f"test-report-block-template.{row['Language']}.xlsx")
    active_assets = {path.name for path in (root / "skills/blend-generate-test-spec/assets").glob("*.xlsx")
                     if not path.name.startswith("~$")}
    assert active_assets == {"test-report-block-template.ja.xlsx", "test-report-block-template.vi.xlsx"}
    expected_mappings = {(family, language) for family in expected_families
                         for language in (("neutral",) if family == "sql-investigation" else
                                           ("vi",) if family == "validation-report" else ("ja", "vi"))}
    assert {(row["Output type"], row["Language"]) for row in rows} == expected_mappings
    assert len(rows) == len(expected_mappings), "Output/language mapping duplicated or omitted"
    assert {"topics", "planning", "code-review", "customer-report", "automation"}.issubset(AREAS), "New fixture dispatch group unavailable"
    assert len(SKILLS) == 6 and SKILLS[-1] == "blend-automation-test"
    rejected(lambda: mapping(rows, "unmapped-plan", "vi"), "unsupported output")
    rejected(lambda: mapping(rows, "research", "en"), "unmapped language")

    for language in ("ja", "vi"):
        row = mapping(rows, "research", language)
        validate_output_filename(f"research/score-source-mapping.{language}.md", row)
        validate_output_filename(f"research/RC-001-A-score-source-mapping.{language}.md", row)
        for invalid in (f"research.{language}.md", f"research/<topic>.{language}.md",
                        f"research/../escape.{language}.md", f"research/nested/topic.{language}.md",
                        f"/research/flow.{language}.md", f"research/.{language}.md",
                        f"research/flow_notes.{language}.md", f"C:/research/flow.{language}.md"):
            rejected(lambda invalid=invalid: validate_output_filename(invalid, row), "invalid topic path")
        row = mapping(rows, "implementation-plan", language)
        validate_output_filename(f"plans/RC-001-A-score-save-implementation-plan.{language}.md", row)
        rejected(lambda: validate_output_filename(f"tasks/id/score-implementation-plan.{language}.md", row),
                 "plan duplicated in task subtree")
        row = mapping(rows, "code-review", language)
        validate_output_filename(f"score-save-code-review.{language}.md", row)
    sql = mapping(rows, "sql-investigation", "neutral")
    validate_output_filename("research/score-source-mapping.sql", sql)
    rejected(lambda: validate_output_filename("database-design.sql", sql), "DDL misrouted as query topic")

    assert inventory_gaps(root, rows) == [], "Current registered assets missing/invalid"
    assert resource_gaps(root) == [], "Six-skill source resource closure failed"
    # Completed structural controls use the actual final assets. No model run implied.
    labels = {
        ("implementation-plan", "ja"): ("承認根拠", "承認範囲", "検証状態"),
        ("implementation-plan", "vi"): ("Căn cứ phê duyệt", "Phạm vi đã duyệt", "Trạng thái kiểm chứng"),
        ("code-review", "ja"): ("実差分", "調査一覧", "限界"),
        ("code-review", "vi"): ("Thay đổi thực tế", "Inventory kiểm tra", "Giới hạn"),
    }
    for (family, language), fields in labels.items():
        row = mapping(rows, family, language)
        headings = row["Required sections"].split(";")
        asset_text = (root / row["Template"]).read_text(encoding="utf-8")
        synthetic = re.sub(r"<!--(?! blend-template:).*?-->", "", asset_text, flags=re.S)
        synthetic = re.sub(r"\{\{.*?\}\}", "synthetic scoped value; no runtime proof", synthetic, flags=re.S)
        validate_markdown(synthetic, row, required_fields=fields)
        rejected(lambda: validate_markdown(synthetic.replace(f"{family}@1.0.0", f"{family}@9.0.0"), row),
                 "new family version drift")
        rejected(lambda: validate_markdown(synthetic.replace("## " + headings[-1], "## Other"), row),
                 "new required section omitted")
        rejected(lambda: validate_markdown(synthetic.replace(fields[0] + ": synthetic scoped value; no runtime proof", fields[0] + ":"),
                                          row, required_fields=fields), "new localized required field empty")
        # A correct family marker cannot authorize arbitrary paths, types or languages.
        filename = row["Filename"].replace("<scope>", "score-save")
        validate_output(synthetic, filename, rows, family, language, required_fields=fields)
        for invalid in (f"arbitrary.{language}.md", filename.replace(f".{language}.md", ".en.md")):
            rejected(lambda invalid=invalid: validate_output(synthetic, invalid, rows, family, language),
                     "marker-only output acceptance")
        hidden = synthetic.replace(fields[0] + ": synthetic scoped value; no runtime proof", "Other: value")
        hidden += f"\n<!--\n- {fields[0]}: hidden instruction\n-->\n```text\n- {fields[0]}: example\n```\n"
        rejected(lambda: validate_markdown(hidden, row, required_fields=fields), "comment/example masquerading as field")
        fenced_identity = synthetic.replace(f"<!-- blend-template: {family}@1.0.0 -->", "")
        fenced_identity += f"\n```md\n<!-- blend-template: {family}@1.0.0 -->\n```\n"
        rejected(lambda: validate_markdown(fenced_identity, row), "fenced example masquerading as provenance")
        optional = "Synthetic conditional evidence"
        validate_markdown(synthetic, row, conditional_sections={optional: False})
        rejected(lambda: validate_markdown(synthetic, row, conditional_sections={optional: True}),
                 "new conditional omission outside predicate")
        reversed_body = f"<!-- blend-template: {family}@1.0.0 -->\n" + "\n".join(
            f"## {heading}\nSynthetic content.\n" for heading in reversed(headings))
        rejected(lambda: validate_markdown(reversed_body, row), "new required order drift")
        with tempfile.TemporaryDirectory(prefix="blend-new-template-controls-") as directory:
            fixture_root = Path(directory)
            asset = fixture_root / row["Template"]
            assert inventory_gaps(fixture_root, [row]), "Absent planned asset accepted as complete"
            asset.parent.mkdir(parents=True)
            asset.write_text(synthetic, encoding="utf-8")
            assert inventory_gaps(fixture_root, [row]) == [], "Valid synthetic asset rejected"
            asset.write_text(synthetic.replace(f"{family}@1.0.0", f"{family}@9.0.0"), encoding="utf-8")
            assert inventory_gaps(fixture_root, [row]), "Wrong new asset identity accepted"

    inputs = Path(__file__).parent / "inputs"
    vi = mapping(rows, "research", "vi")
    ja = mapping(rows, "research", "ja")
    legacy_vi = (inputs / "research-template.vi.md").read_text(encoding="utf-8")
    legacy_ja = (inputs / "research-template.ja.md").read_text(encoding="utf-8")
    # Frozen 1.0.0 inputs remain unchanged and only validate against legacy schema.
    validate_markdown(legacy_vi, {**vi, "Version": "1.0.0"}, required_fields=("Nguồn", "Căn cứ"))
    validate_markdown(legacy_ja, {**ja, "Version": "1.0.0"}, required_fields=("Source", "Basis"))
    rejected(lambda: validate_markdown(legacy_vi, vi), "legacy snapshot used as current topic output")
    topic_labels = ("Chủ đề", "Mục đích", "Phụ thuộc", "Tính hiện hành")
    template = (root / vi["Template"]).read_text(encoding="utf-8")
    current_topic = re.sub(r"<!--(?! blend-template:).*?-->", "", template, flags=re.S)
    current_topic = re.sub(r"\{\{.*?\}\}", "synthetic question/dependency identity", current_topic, flags=re.S)
    validate_markdown(current_topic, vi, required_fields=topic_labels)
    for label in topic_labels:
        rejected(lambda label=label: validate_markdown(current_topic.replace(
            f"- {label}: synthetic question/dependency identity", f"- {label}:"),
            vi, required_fields=topic_labels), "current topic field empty")
    # Allowed omission is tested independently from required fields/sections.
    legacy_row = {**vi, "Version": "1.0.0"}
    good = legacy_vi.split("\n## Bằng chứng thực thi")[0] + "\n"
    validate_markdown(good, legacy_row, required_fields=("Nguồn", "Căn cứ"),
                      conditional_sections={"Bằng chứng thực thi": False})
    validate_markdown(legacy_vi, legacy_row, conditional_sections={"Bằng chứng thực thi": True})
    rejected(lambda: validate_markdown(good, legacy_row, conditional_sections={"Bằng chứng thực thi": True}), "omission without its predicate")
    rejected(lambda: validate_markdown(legacy_vi, legacy_row, conditional_sections={"Bằng chứng thực thi": False}), "optional content outside scope")
    rejected(lambda: validate_markdown(good.replace("research@1.0.0", "research@0.9.0"), legacy_row), "wrong version")
    rejected(lambda: validate_markdown(good.replace("<!-- blend-template: research@1.0.0 -->", ""), legacy_row), "missing identity")
    rejected(lambda: validate_markdown(good.replace("## Gaps và giới hạn", "## Other"), legacy_row), "missing required section")
    rejected(lambda: validate_markdown(good.replace("- Nguồn:", "- Unrelated:"), legacy_row,
                                      required_fields=("Nguồn",)), "missing required field")
    empty = good.replace("- Nguồn: S-SYNTHETIC, snapshot 1; synthetic identity only.", "| Nguồn |  |")
    rejected(lambda: validate_markdown(empty, legacy_row, required_fields=("Nguồn",)), "empty required table field")
    swapped = good.replace("## Phạm vi và căn cứ", "## SWAP").replace("## Gaps và giới hạn", "## Phạm vi và căn cứ").replace("## SWAP", "## Gaps và giới hạn")
    rejected(lambda: validate_markdown(swapped, legacy_row), "required order changed")

    # A temporary package tests missing assets without corrupting actual writer files.
    with tempfile.TemporaryDirectory(prefix="blend-template-controls-") as directory:
        fixture_root = Path(directory)
        research_asset = fixture_root / vi["Template"]
        gaps = inventory_gaps(fixture_root, [vi])
        assert gaps and "Missing asset:" in gaps[0], "Missing template falsely accepted"
        research_asset.parent.mkdir(parents=True)
        research_asset.write_text(template, encoding="utf-8")
        assert inventory_gaps(fixture_root, [vi]) == [], "Valid asset rejected"
        research_asset.write_text(template.replace("research@1.1.0", "research@9.0.0"), encoding="utf-8")
        assert inventory_gaps(fixture_root, [vi]), "Wrong asset version falsely accepted"

    check_plan_review(root, rows)
    check_runtime_gate(root, rows)
    scenarios = json.loads((root / "tests/scenarios.json").read_text(encoding="utf-8"))
    assert scenarios["runtime_targets"] == ["codex", "cursor", "claude"]
    assert scenarios["static_checks_satisfy_runtime_proof"] is False
    for area in ("topics", "planning", "code-review"):
        evidence = scenarios["evaluation_inputs"][area]
        assert all((root / path).is_dir() and "scorer-only" not in Path(path).parts for path in evidence["writer_roots"])
        assert (root / evidence["scorer_oracle"]).is_file()
        assert all(not (root / evidence["scorer_oracle"]).resolve().is_relative_to((root / path).resolve())
                   for path in evidence["writer_roots"])
    assert {scenario["id"] for scenario in scenarios["scenarios"]} == {f"S{i:02}" for i in range(1, 22)}
    assert len(scenarios["scenarios"]) == 21, "Duplicate runtime scenario ID"
    for area in ("test-spec-scenario-grouping", "automation"):
        evidence = scenarios["evaluation_inputs"][area]
        assert evidence["evaluation_method"]
        assert all((root / path).is_dir() and "scorer-only" not in Path(path).parts for path in evidence["writer_roots"])
    registered = {scenario["id"]: scenario for scenario in scenarios["scenarios"]}
    assert registered["S20"]["proof_kind"] == "actual-generator-semantic-evaluation"
    assert registered["S21"]["proof_kind"] == "synthetic-control-replay-not-live-browser-or-sheets"
    assert all((root / path).is_dir() for identity in ("S20", "S21") for path in registered[identity]["fixture_roots"])
    assert all(scenario["required_runtime_proof"] and scenario["oracle"]
               for scenario in scenarios["scenarios"]), "Scenario lacks actual-runtime proof oracle"
    assert {requirement for scenario in scenarios["scenarios"][:12] for requirement in scenario["requirements"]} == {f"R{i}" for i in range(1, 15)}
    assert {requirement for scenario in scenarios["scenarios"][12:16] for requirement in scenario["requirements"]} == {f"N{i}" for i in range(1, 12)}
    assert {requirement for scenario in scenarios["scenarios"][16:] for requirement in scenario["requirements"] if requirement.startswith("C")} == {f"C{i}" for i in range(1, 11)}
    assert {requirement for scenario in scenarios["scenarios"] for requirement in scenario["requirements"] if requirement.startswith("U")} == {f"U{i}" for i in range(1, 9)}
    assert {requirement for scenario in scenarios["scenarios"] for requirement in scenario["requirements"] if requirement.startswith("A")} == {f"A{i:02}" for i in range(1, 15)}
    assert {requirement for scenario in scenarios["scenarios"] for requirement in scenario["requirements"] if requirement.startswith("K")} == {f"K{i}" for i in range(15, 21)}
    validation = mapping(rows, "validation-report", "vi")
    check_identity((root / validation["Template"]).read_text(encoding="utf-8"), validation)
    return [f"{len(rows)} output/language mappings and paired semantic schema, including one active test-report@2.5.0 JA/VI workbook pair",
            "topic/plan/code-review filename patterns and new-family missing/version/order/field controls",
            "current research 1.1.0 rejects unchanged read-only legacy 1.0.0 snapshots as new outputs",
            "positive JA/VI controls and negative missing/version/section/field/order/omission controls",
            "asset-derived JA/VI inline summaries, populated block/list and scoped no-findings accepted; empty/drifted presentation rejected",
            "missing-asset and wrong-asset-version controls", "21 scenario inventory; generator semantic and explicitly synthetic automation replay registered; R1–R14, N1–N11, C1–C10, U1–U8, A01–A14 and K15–K20 coverage",
            "actual six-skill resource closure, common eleven-field roles/license, plan-to-review basis and changed-source/scope/parent/approval/AC negative controls",
            "structural controls only; source semantics and actual writer/runtime behavior not certified"]
