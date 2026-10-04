"""Planning asset conformance and raw fixture integrity; not agent behavior proof."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from test_kit import load_registry, mapping, validate_markdown, validate_output_filename


# One localized label per registry semantic field, in identical order for JA/VI.
LABELS = {
    "ja": ("状態", "識別情報", "情報源リビジョン", "レビュー判定", "承認根拠", "承認範囲",
           "コード基準", "Research依存", "維持する動作", "手順ID", "結果", "ファイル・シンボル",
           "開始条件", "契約", "担当範囲", "依存", "拘束条件", "AC対応", "検証コマンド",
           "検証状態", "リスク", "最終確認", "実行権限"),
    "vi": ("Trạng thái", "Danh tính", "Revisions nguồn", "Kết quả review", "Căn cứ phê duyệt",
           "Phạm vi đã duyệt", "Baseline code", "Phụ thuộc Research", "Bảo toàn", "Mã bước",
           "Kết quả", "Files và symbols", "Điều kiện bắt đầu", "Contracts", "Ownership", "Phụ thuộc",
           "Nghĩa vụ binding", "Ánh xạ AC", "Commands kiểm chứng", "Trạng thái kiểm chứng",
           "Rủi ro", "Kiểm tra cuối", "Quyền thực thi"),
}
OPTIONAL = {
    "ja": ("既存指摘の扱い", "並列化計画", "DB・移行"),
    "vi": ("Xử lý findings trước đó", "Kế hoạch song song", "DB và migration"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rejected(call, reason: str) -> None:
    try:
        call()
    except (ValueError, AssertionError):
        return
    raise AssertionError(f"Negative control accepted: {reason}")


def check_h3(text: str, predicates: dict[str, bool]) -> None:
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    headings = re.findall(r"^### (.+)$", body, flags=re.M)
    for heading, needed in predicates.items():
        if headings.count(heading) != int(needed):
            raise ValueError(f"Conditional H3 predicate violated: {heading}")


def approved_current(inputs: Path, text: str, selected_scope: str) -> bool:
    """Fixture-only comparison: captured approval must be real before currentness."""
    scope = re.search(r"^- Scope: (.+)$", text, re.M)
    if not scope or scope.group(1) != selected_scope:
        return False
    for label in ("Approval source", "Role", "Date", "Identity"):
        if not re.search(r"^- " + label + r": \S.+$", text, re.M):
            raise ValueError(f"Approval reference lacks {label}")
    rows = []
    for line in text.splitlines():
        if not line.startswith("| common/"):
            continue
        cells = [value.strip() for value in line.strip("|").split("|")]
        if len(cells) != 4:
            raise ValueError("Malformed approval reference row")
        current, captured, revision, digest = cells
        for relative in (current, captured):
            target = (inputs / relative).resolve()
            if not target.is_relative_to(inputs.resolve()) or not target.is_file():
                raise ValueError("Missing/escaping approval artifact")
        if not re.fullmatch(r"[0-9a-f]{64}", digest) or sha(inputs / captured) != digest:
            raise ValueError("Approval hash does not match its actual captured artifact")
        if revision not in (inputs / captured).read_text(encoding="utf-8"):
            raise ValueError("Approval revision absent from captured artifact")
        rows.append(sha(inputs / current) == digest)
    if len(rows) != 2:
        raise ValueError("Expected exactly Split/AC approval references")
    return all(rows)


def run(root: Path) -> list[str]:
    fixture = Path(__file__).parent
    inputs = fixture / "inputs"
    before = {path.relative_to(inputs).as_posix(): sha(path)
              for path in inputs.rglob("*") if path.is_file()}
    rows = load_registry(root)
    for language in ("ja", "vi"):
        row = mapping(rows, "implementation-plan", language)
        assert row["Family"] == "implementation-plan" and row["Version"] == "1.0.0"
        assert len(row["Fields"].split(",")) == len(LABELS[language])
        asset = root / row["Template"]
        text = asset.read_text(encoding="utf-8")
        # Ignore instructions; actual labels must be in the asset's document body.
        body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        body = "<!-- blend-template: implementation-plan@1.0.0 -->\n" + body
        validate_markdown(body, row, required_fields=LABELS[language])
        assert re.findall(r"^## (.+)$", body, re.M) == row["Required sections"].split(";")
        validate_output_filename(f"plans/SYN-PL-02-A-title-save-implementation-plan.{language}.md", row)
        for invalid in (f"tasks/SYN-PL-02-A-title-save-implementation-plan.{language}.md",
                        f"plans/../title-save-implementation-plan.{language}.md",
                        f"plans/<scope>-implementation-plan.{language}.md",
                        f"D:/private/title-save-implementation-plan.{language}.md"):
            rejected(lambda invalid=invalid: validate_output_filename(invalid, row), "nonportable/routing")
        rejected(lambda: validate_markdown(body.replace("implementation-plan@1.0.0", "implementation-plan@2.0.0"), row), "wrong family version")
        for label in LABELS[language]:
            empty = re.sub(r"^(- " + re.escape(label) + r":).*$", r"\1", body, flags=re.M)
            rejected(lambda empty=empty: validate_markdown(empty, row, required_fields=LABELS[language]), "required localized field empty")
        heading = row["Required sections"].split(";")[-1]
        rejected(lambda: validate_markdown(body.replace("## " + heading, "## Other"), row), "required H2 omitted")
        absent = {heading: False for heading in OPTIONAL[language]}
        check_h3(body, absent)
        for heading in OPTIONAL[language]:
            present = body + f"\n### {heading}\nSynthetic conformance control only.\n"
            check_h3(present, {**absent, heading: True})
            rejected(lambda present=present: check_h3(present, absent), "conditional H3 outside predicate")
            rejected(lambda heading=heading: check_h3(body, {**absent, heading: True}), "required conditional H3 omitted")

    skill = root / "skills/blend-plan-implementation"
    entrypoint = (skill / "SKILL.md").read_text(encoding="utf-8")
    assert entrypoint.startswith("---\nname: blend-plan-implementation\ndescription: ")
    metadata = entrypoint.split("---", 2)[1]
    assert re.search(r"^description: \S.+$", metadata, re.M), "Empty discovery description"
    for path in skill.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for relative in re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", text):
            assert (path.parent / relative).resolve().is_file(), f"Broken resource link: {path.name}/{relative}"
        assert not re.search(r"[A-Za-z]:[\\/]|localhost|127\.0\.0\.1", text), "Private workstation reference in skill"

    oracle = json.loads((fixture / "scorer-only/oracle.json").read_text(encoding="utf-8"))
    assert not (inputs / "scorer-only").exists(), "Scorer truth exposed as writer input"
    assert set(oracle["cases"]) == {path.name for path in (inputs / "cases").iterdir() if path.is_dir()}
    for case, expected in oracle["cases"].items():
        directory = inputs / "cases" / case
        assert (directory / "request.md").is_file()
        approval = directory / "approval.md"
        actual = approved_current(inputs, approval.read_text(encoding="utf-8"), expected["scope"]) if approval.exists() else False
        assert actual == expected["approved"], f"Fixture approval/currentness mismatch: {case}"
    current = (inputs / "cases/current/approval.md").read_text(encoding="utf-8")
    rejected(lambda: approved_current(inputs, re.sub(r"[0-9a-f]{64}", "0" * 64, current), "title-save"), "fabricated approval hash")
    assert not approved_current(inputs, current, "title-save+archive"), "Approval extended to another scope"
    stale = (inputs / "cases/stale-approval/approval.md").read_text(encoding="utf-8")
    assert not approved_current(inputs, stale, "title-save"), "Old approved AC grants current AC approval"

    feature = inputs / "common/features/SYN-PL-02-notice-title"
    ac = (feature / "docs/acceptance-criteria.vi.md").read_text(encoding="utf-8")
    context = (feature / "CONTEXT.md").read_text(encoding="utf-8")
    review = (feature / "docs/artifact-review.vi.md").read_text(encoding="utf-8")
    assert set(re.findall(r"^- (AC-[A-Z]\d):", ac, re.M)) == {"AC-T1", "AC-T2", "AC-T3", "AC-A1"}
    assert "Q-ARCH-1" in context and "no prerequisite" in context
    assert "F-P-01: NEEDS_EVIDENCE" in review and "Review PASS is not" in review
    application = inputs / "common/application-source"
    composer = json.loads((application / "composer.json").read_text(encoding="utf-8"))
    commands = composer["scripts"]["lint"]
    assert composer["require"]["php"] == ">=8.2"
    for command in commands:
        assert command.startswith("php -l ") and (application / command[len("php -l "):]).is_file()
    assert not (application / "vendor").exists() and not (application / "tests").exists()
    controller = (application / "application/controllers/Notice.php").read_text(encoding="utf-8")
    model = (application / "application/models/NoticeStore.php").read_text(encoding="utf-8")
    assert "findOwned" in controller and "function show" in controller and "trim(" not in controller
    assert "'school_id' => $schoolId, 'owner_id' => $ownerId" in model
    assert "update('notices', ['title' => $title])" in model
    assert before == {path.relative_to(inputs).as_posix(): sha(path)
                      for path in inputs.rglob("*") if path.is_file()}, "Raw inputs changed during checks"
    return ["paired 1.0.0 planning assets: six exact H2s, 23 localized fields, portable filenames/resource links",
            "negative version/field/H2/routing and all conditional H3 predicate controls",
            "five raw approval cases: captured SHA-256 valid, stale/current/scope/missing distinctions; scorer isolated",
            "raw synthetic source/AC/review/code/toolchain seams and byte preservation checked",
            "static fixture proof only; actual plan-only decisions/readability/JA-VI semantics remain runtime proof"]
