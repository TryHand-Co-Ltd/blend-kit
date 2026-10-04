"""Frozen reviewer resources and raw fixture integrity, not model-review accuracy."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import zipfile
import xml.etree.ElementTree as ET

from test_kit import load_registry, mapping, validate_markdown


def rejected(call, name):
    try:
        call()
    except ValueError:
        return
    raise AssertionError(f"Invalid review control accepted: {name}")


def workbook_cells(path: Path) -> dict[str, dict[str, str]]:
    """Read exact fixture cells without loading/saving or recalculating the workbook."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as archive:
        strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            strings = ["".join(item.itertext()) for item in
                       ET.fromstring(archive.read("xl/sharedStrings.xml"))]
        result = {}
        for index, name in enumerate(("Run", "Cases", "Data"), 1):
            tree = ET.fromstring(archive.read(f"xl/worksheets/sheet{index}.xml"))
            cells = {}
            for cell in tree.findall(".//m:c", ns):
                formula = cell.find("m:f", ns)
                value = cell.find("m:v", ns)
                if formula is not None:
                    content = "=" + (formula.text or "")
                elif cell.get("t") == "inlineStr":
                    content = "".join(node.text or "" for node in cell.findall(".//m:t", ns))
                elif cell.get("t") == "s" and value is not None:
                    content = strings[int(value.text)]
                else:
                    content = value.text if value is not None else ""
                cells[cell.get("r")] = content
            result[name] = cells
        return result


def run(root: Path) -> list[str]:
    skill_root = root / "skills/blend-review-artifacts"
    skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    header = skill.split("---", 2)[1]
    assert re.search(r"^name: blend-review-artifacts$", header, re.M)
    assert re.search(r"^description: \S.+$", header, re.M)
    for relative in re.findall(r"\]\(([^)]+)\)", skill):
        if "://" not in relative:
            path, _, anchor = relative.partition("#")
            target = (skill_root / path).resolve()
            assert target.is_file() and target.is_relative_to(root.resolve()), f"Broken reviewer resource link: {relative}"
            if anchor:
                headings = re.findall(r"^#{1,6} (.+)$", target.read_text(encoding="utf-8"), re.M)
                assert anchor in {re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-") for heading in headings}, f"Broken reviewer anchor: {relative}"
    license_bytes = (root / "shared/bug-hunter-LICENSE.txt").read_bytes()
    assert hashlib.sha256(license_bytes).hexdigest() == "363363d8c6255e2a4e68724b3e0ea4919ee651751af2b87ddfe9986a077e5b14"
    assert (skill_root / "references/bug-hunter-LICENSE.txt").read_bytes() == license_bytes
    for resource in ("review-policy", "bug-hunter"):
        pointer = (skill_root / f"references/{resource}.md").read_text(encoding="utf-8")
        assert f"../../../shared/{resource}.md" in pointer, "Legacy resource must point to common owner"
        assert f"../../shared/{resource}.md" in skill, "Reviewer omitted mandatory common resource"
    rows = load_registry(root)
    labels = {
        "vi": ("Nguồn", "Revision", "Phạm vi", "Kết luận", "Phân loại", "Bằng chứng",
               "Tình huống", "Tác động", "Đề xuất cập nhật", "Kiểm chứng sau sửa", "Giới hạn",
               "Coverage", "Checks đã chạy", "Checks chưa chạy", "Bảo toàn"),
        "ja": ("参照元", "Revision", "対象範囲", "結論", "分類", "証拠", "状況", "影響",
               "更新提案", "修正後の確認", "限界", "Coverage", "実施したChecks", "未実施Checks", "保全"),
    }
    for language in ("ja", "vi"):
        row = mapping(rows, "review", language)
        template = (root / row["Template"]).read_text(encoding="utf-8")
        validate_markdown(template, row, required_fields=labels[language])
        assert all(field in template for field in row["Fields"].split(","))
        assert "Prior-finding ledger is required only on re-review" in template
        # A completed control exercises real fields; matching H2s alone cannot pass.
        completed = re.sub(r"<!--(?! blend-template:).*?-->", "", template, flags=re.S)
        completed = re.sub(r"\{\{.*?\}\}", "synthetic inspected evidence; no runtime proof", completed, flags=re.S)
        validate_markdown(completed, row, required_fields=labels[language])
        rejected(lambda: validate_markdown(completed.replace("review@1.0.0", "review@9.0.0"), row),
                 "wrong review version")
        proposal = "Đề xuất cập nhật" if language == "vi" else "更新提案"
        rejected(lambda: validate_markdown(completed.replace(proposal + ":", "Other:"), row,
                                            required_fields=labels[language]), "missing actionable proposal")
        heading = row["Required sections"].split(";")[-1]
        rejected(lambda: validate_markdown(completed.replace("## " + heading, "## Other"), row),
                 "missing coverage/limits")

    fixture_root = Path(__file__).parent
    oracle = json.loads((fixture_root / "scorer-only/oracle.json").read_text(encoding="utf-8"))
    assert set(oracle["scenarios"]) == {"S06", "S07", "S09", "S10", "S11", "S12"}
    # Raw writer packs contain sources, supplied artifacts, requests and prior evidence only.
    for name in ("standalone", "combined", "valid-control"):
        pack = fixture_root / "inputs" / name
        assert not any(path.name == "oracle.json" for path in pack.rglob("*"))
        snapshot = (pack / "SNAPSHOT.md").read_text(encoding="utf-8")
        pins = re.findall(r"^\| ([^|]+) \| ([a-f0-9]{64}) \|$", snapshot, re.M)
        actual = {path.relative_to(pack).as_posix() for path in pack.rglob("*")
                  if path.is_file() and path.name != "SNAPSHOT.md"}
        assert {path for path, _ in pins} == actual, f"Incomplete raw snapshot: {name}"
        for relative, digest in pins:
            path = (pack / relative).resolve()
            assert path.is_relative_to(pack.resolve())
            assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"Raw fixture drift {name}/{relative}"
        spec_text = (pack / "SPEC.md").read_text(encoding="utf-8")
        assert "Synthetic" in spec_text and "strictly below" in spec_text
        assert all(f"- C{i}:" in spec_text for i in range(1, 9))
        assert "Q3 AWAITING DECISION" in (pack / "confirmation.md").read_text(encoding="utf-8")
        assert "round($score - $offset)" in (pack / "application/services/AlertService.php").read_text(encoding="utf-8")
    assert not (fixture_root / "inputs/standalone/task-artifacts").exists()
    assert (fixture_root / "inputs/combined/request-task-only.md").is_file()

    # Reuse the frozen Markdown parser to establish projection controls, not a reviewer verdict.
    parser_path = root / "skills/blend-generate-test-spec/scripts/export_report.py"
    module_spec = importlib.util.spec_from_file_location("review_projection_parser", parser_path)
    parser = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(parser)
    good_dir = fixture_root / "inputs/valid-control/test-spec"
    good = parser.parse_sources(good_dir)
    good_ja = parser.parse_sources(good_dir, "ja")
    good_cells = workbook_cells(good_dir / "test-case-report.xlsx")
    assert good["revision"] == good_ja["revision"] == good_cells["Run"]["B3"] == "design-v2"
    variants = {(case["id"], variant[0]) for case in good["cases"] for variant in case["variants"]}
    assert variants == {(good_cells["Run"].get(f"B{row}"), good_cells["Run"].get(f"C{row}"))
                        for row in range(25, 25 + len(variants))}
    assert {row[0] for row in good["cases"][0]["variants"]} == {"below", "equal", "above"}
    assert good["cases"][1]["expected"] == "79"
    assert good["cases"][-1]["readiness"] == "Blocked" and good["cases"][-1]["gap"] == "G-PREP"
    assert {row[0] for row in good["gaps"]} == {"G-ROUND", "G-PREP"}
    assert all(good_cells["Run"][f"I{row}"] == "NOT RUN" for row in range(25, 25 + len(variants)))
    assert "No data" in good_cells["Run"]["B22"]
    for language in ("ja", "vi"):
        for family in parser.HEADINGS[language]:
            filename = f"{family}.{language}.md"
            digest = hashlib.sha256((good_dir / filename).read_bytes()).hexdigest()
            assert f"{filename}: sha256:{digest}" in good_cells["Run"]["B11"]

    for name in ("standalone", "combined"):
        directory = fixture_root / "inputs" / name / "test-spec"
        flawed = parser.parse_sources(directory)
        cells = workbook_cells(directory / "test-case-report.xlsx")
        assert flawed["revision"] != cells["Run"]["B3"]
        assert flawed["cases"][1]["expected"] == "80" != cells["Cases"]["P9"]
        assert cells["Run"].get("C26", "") == "" and flawed["cases"][1]["variants"][0][0] == "fraction"
        assert cells["Run"]["I25"] == cells["Run"]["R25"] == "PASS"
        assert cells["Run"].get("K25", "") == "" and cells["Run"].get("B5", "") == ""
        assert cells["Run"]["B22"] == "1"
        assert cells["Data"]["D8"] == "saved values from another year"
        assert {row[0] for row in flawed["cases"][0]["variants"]} == {"below"}
        assert {row[0] for row in flawed["cases"][2]["variants"]} == {"admin"}
        assert flawed["cases"][-1]["source"].startswith("SPEC.md C7") and flawed["cases"][-1]["basis"] == "Confirmed"
        assert not flawed["gaps"] and flawed["cases"][-2]["readiness"] == "Ready"
        assert "non-target sentinels may also change" in (directory / "test-cases.ja.md").read_text(encoding="utf-8")
        assert "non-target sentinels unchanged" in (directory / "test-cases.vi.md").read_text(encoding="utf-8")

    ledger = (fixture_root / "inputs/combined/prior-findings.md").read_text(encoding="utf-8")
    assert all(f"F-0{i} OPEN" in ledger for i in range(1, 5))
    for finding in oracle["findings"]:
        assert finding["source"] and finding["risk"] and finding["proposal"] and finding["verification"]
        for anchor in finding["anchors"]:
            path = fixture_root / anchor["path"]
            assert path.is_file(), f"Scorer source/artifact anchor missing: {path}"
            if "cell" in anchor:
                assert anchor["sheet"] in ("Run", "Cases", "Data")
                assert re.fullmatch(r"[A-Z]+[1-9][0-9]*", anchor["cell"])
            else:
                assert 1 <= anchor["line"] <= len(path.read_text(encoding="utf-8").splitlines())

    return ["JA/VI review templates match registry schema; completed controls reject version/required proposal/coverage omissions",
            "three synthetic raw source/artifact packs pinned byte-for-byte; standalone has no Task prerequisite; Task-only/combined requests present",
            "valid shared-context/parameterized cases retain boundary/role variants, unknown oracle and preparation gaps; workbook keys/fingerprints/NOT RUN match",
            "known semantic, branch, fixture, bilingual, revision, dropped-variant and false-PASS workbook defects are present in invalid controls",
            "scorer-only clause/anchor/update oracle and stable prior-finding ledger isolated from runtime writer packs; no runtime reviewer or app tests executed"]
