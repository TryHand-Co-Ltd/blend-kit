"""Project fixed-template BLEND Test Spec Markdown into a bundled JA/VI workbook.

No application tests, translation, source approval or spreadsheet recalculation.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

VERSION = "1.0.0"
HEADINGS = {
    "vi": {"scope-and-approach": ["Mục tiêu và căn cứ", "Phạm vi", "Chuẩn bị và cách chạy", "Coverage và gaps"],
           "test-cases": ["Quy ước và context", "Các testcase"], "test-data": ["Quy ước dữ liệu", "Fixtures"]},
    "ja": {"scope-and-approach": ["目的・根拠", "対象範囲", "準備・実行方針", "Coverage・Gaps"],
           "test-cases": ["規約・コンテキスト", "テストケース"], "test-data": ["データ規約", "Fixtures"]},
}
CASE_KEYS = ["function", "source", "priority", "basis", "readiness", "gap", "configuration", "trigger",
             "observation", "actor", "fixture", "action", "expected", "preservation", "proof", "reset"]
CASE_LABELS = {
    "vi": ["Chức năng", "Căn cứ", "Priority", "Căn cứ kỳ vọng", "Readiness", "Gap", "Cấu hình", "Kích hoạt",
           "Quan sát", "Actor và quyền", "Fixture", "Thao tác", "Expected", "Bảo toàn", "Bằng chứng", "Reset"],
    "ja": ["機能", "根拠", "Priority", "期待根拠", "Readiness", "Gap", "設定", "起動", "観測", "Actor・権限",
           "Fixture", "操作", "Expected", "維持状態", "証拠", "Reset"],
}
FIXTURE_LABELS = {"vi": ["Vai trò", "Phạm vi", "Trạng thái", "Giá trị", "Target và non-target", "Tạo", "Kiểm tra", "Reset"],
                  "ja": ["役割", "範囲", "状態", "値", "Target・non-target", "作成", "確認", "Reset"]}
SCOPE_LABELS = {"vi": [["Revision", "Nguồn", "Căn cứ research", "Baseline code", "Mode", "Giới hạn"],
                        ["Trong scope", "Ngoài scope", "Vai trò"], ["Môi trường", "Chuẩn bị", "Chọn lượt chạy", "Điều kiện bắt đầu", "Điều kiện kết thúc", "Bằng chứng"]],
                "ja": [["Revision", "Source", "Research根拠", "Code baseline", "Mode", "調査限界"],
                        ["対象", "対象外", "役割"], ["環境", "準備", "実行選択", "開始条件", "終了条件", "証拠"]]}
WORKBOOK_LOCALES = {"vi": {}, "ja": {}}


def cell_value(value: str) -> str:
    value = html.unescape(value.replace("<br>", "\n").replace("<br/>", "\n"))
    if len(value) > 32767:
        raise ValueError("Source exceeds Excel cell limit; split meaning using template steps/fixtures")
    if any(ord(ch) < 32 and ch not in "\n\t" for ch in value):
        raise ValueError("Unsupported control character")
    return value


def read_table(block: str, headers: list[str]) -> tuple[list[list[str]], str]:
    """Read one exact Markdown table; reject ragged/compound rows rather than guessing."""
    lines = block.strip().splitlines()
    if len(lines) < 2 or not lines[0].startswith("|"):
        raise ValueError(f"Missing table: {headers}")
    consumed = 0
    parsed = []
    for line in lines:
        if not line.strip().startswith("|"):
            break
        if not line.strip().endswith("|") or "\\|" in line:
            raise ValueError("Use &#124; for literal pipes and <br> for line breaks")
        row = [part.strip() for part in line.strip()[1:-1].split("|")]
        if len(row) != len(headers):
            raise ValueError("Ragged/compound Markdown table row")
        parsed.append(row)
        consumed += 1
    if parsed[0] != headers or not all(re.fullmatch(r":?-{3,}:?", value) for value in parsed[1]):
        raise ValueError(f"Table header/separator mismatch: {headers}")
    if any(not value for row in parsed[2:] for value in row):
        raise ValueError("Empty required table cell")
    return [[cell_value(value) for value in row] for row in parsed[2:]], "\n".join(lines[consumed:]).strip()


def fields(block: str, labels: list[str], *, exact: bool = True) -> tuple[dict[str, str], str]:
    rows, rest = read_table(block, ["Field", "Value"])
    actual = [row[0] for row in rows]
    if len(set(actual)) != len(actual) or (actual != labels if exact else any(item not in labels for item in actual)):
        raise ValueError(f"Required field order/membership mismatch: {labels}")
    return dict(rows), rest


def document(path: Path, family: str, language: str, *, raw: bytes | None = None) -> tuple[str, list[str]]:
    captured = path.read_bytes() if raw is None else raw
    text = captured.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    markers = [f"<!-- blend-template: {family}@{VERSION} -->"]
    if family == 'test-cases':
        markers.append('<!-- blend-template: test-cases@1.1.0 -->')
    if re.findall(r"<!--\s*blend-template:[^>]*-->", text) not in [[marker] for marker in markers]:
        raise ValueError(f"Missing/wrong template family/version: {path.name}")
    if "<!-- AUTHORING:" in text or re.search(r"\[(?:verified value|same design revision|Feature|source clause)\]", text):
        raise ValueError(f"Unfinished template: {path.name}")
    if "```" in text or "~~~" in text:
        raise ValueError("Fenced schema is unsupported; fields must be actual document content")
    titles = re.findall(r"^## (.+)$", text, re.M)
    if titles != HEADINGS[language][family]:
        raise ValueError(f"Required H2 order mismatch: {path.name}")
    sections = re.split(r"^## .+$", text, flags=re.M)[1:]
    return text, [section.strip() for section in sections]


def identifier(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", value):
        raise ValueError(f"Invalid/compound identifier: {value}")
    return value


def references(value: str, allowed: set[str]) -> list[str]:
    """Canonical bare-ID list; no deduplication, annotations or implicit separators."""
    values = value.split(", ")
    if len(set(values)) != len(values) or any(item not in allowed for item in values):
        raise ValueError("Reference list must contain distinct defined bare IDs separated by comma-space")
    return values


def parse_sources(source: Path, language: str = "vi", *, captured: dict[str, bytes] | None = None) -> dict:
    if language not in WORKBOOK_LOCALES:
        raise ValueError("Unsupported workbook language; choose ja or vi")
    texts = {}
    sections = {}
    for family in HEADINGS[language]:
        name = f"{family}.{language}.md"
        texts[family], sections[family] = document(source / name, family, language,
                                                  raw=captured[name] if captured is not None else None)
    scope = []
    for part, labels in zip(sections["scope-and-approach"][:3], SCOPE_LABELS[language]):
        data, rest = fields(part, labels)
        if rest:
            raise ValueError("Scope field sections cannot contain unprojected prose")
        scope.append(data)
    coverage_parts = re.split(r"^### (Coverage|Gaps)$", sections["scope-and-approach"][3], flags=re.M)
    if len(coverage_parts) != 5 or coverage_parts[0].strip() or coverage_parts[1::2] != ["Coverage", "Gaps"]:
        raise ValueError("Coverage/Gaps sections missing, duplicate or out of order")
    coverage, rest = read_table(coverage_parts[2], ["Clause / anchor", "Obligation / branch", "Case / variant / gap", "Rationale / proof limit"])
    if rest or not coverage:
        raise ValueError("Coverage must map source obligations")
    gaps, rest = read_table(coverage_parts[4], ["Gap ID", "Kind", "Known obligation / source", "Missing decision / proof", "Impact / next check"])
    if rest and (gaps or rest not in ("Không có gaps.", "Gapsなし。")):
        raise ValueError("Unsupported gap section tail")
    gap_ids = {identifier(row[0]) for row in gaps}
    if len(gap_ids) != len(gaps):
        raise ValueError("Duplicate gap IDs")
    for row in gaps:
        if row[1] not in ("business", "fact", "engineering", "preparation", "proof"):
            raise ValueError("Unknown gap kind")
    conventions, context_tail = fields(sections["test-cases"][0], ["Revision", "Feature", "Conventions"])
    contexts = {}
    if context_tail:
        chunks = re.split(r"^### Context: (.+)$", context_tail, flags=re.M)
        if chunks[0].strip() or len(chunks) % 2 != 1:
            raise ValueError("Unsupported context syntax")
        for context_id, block in zip(chunks[1::2], chunks[2::2]):
            identifier(context_id)
            data, rest = fields(block, CASE_LABELS[language], exact=False)
            if context_id in contexts or rest or not data or any(value.startswith("@") for value in data.values()):
                raise ValueError("Duplicate/recursive/invalid context")
            contexts[context_id] = data
    fixtures_meta, rest = fields(sections["test-data"][0], ["Revision", "Conventions"])
    if rest:
        raise ValueError("Unsupported data convention syntax")
    fixtures = []
    tail = sections["test-data"][1]
    if tail not in ("Không có fixture dùng chung.", "共通fixtureなし。"):
        chunks = re.split(r"^### Fixture: (.+)$", tail, flags=re.M)
        if chunks[0].strip() or len(chunks) == 1:
            raise ValueError("Missing fixture blocks or explicit empty-set statement")
        for fixture_id, block in zip(chunks[1::2], chunks[2::2]):
            data, rest = fields(block, FIXTURE_LABELS[language])
            if rest:
                raise ValueError("Unprojected fixture prose")
            fixtures.append({"id": identifier(fixture_id), "values": list(data.values())})
    fixture_ids = {item["id"] for item in fixtures}
    if len(fixture_ids) != len(fixtures):
        raise ValueError("Duplicate fixture IDs")
    revisions = [scope[0]["Revision"], conventions["Revision"], fixtures_meta["Revision"]]
    if len(set(revisions)) != 1:
        raise ValueError("Markdown design revisions differ")
    cases = []
    flows = re.split(r"^### Flow: (.+)$", sections["test-cases"][1], flags=re.M)
    if flows[0].strip() or len(flows) == 1:
        raise ValueError("Missing business-flow groups")
    for group, block in zip(flows[1::2], flows[2::2]):
        chunks = re.split(r"^#### (\S+) — (.+)$", block, flags=re.M)
        if chunks[0].strip() or len(chunks) == 1:
            raise ValueError("Missing case block/title")
        for offset in range(1, len(chunks), 3):
            case_id, title, body = chunks[offset:offset + 3]
            paths = re.findall(r'^\| screen_relative_path \| (.*?) \|$',body,re.M)
            if len(paths)>1:
                raise ValueError('Duplicate screen_relative_path')
            body = re.sub(r'^\| screen_relative_path \| .*? \|\n','',body,flags=re.M)
            data, rest = fields(body, CASE_LABELS[language])
            for label, value in data.items():
                if value.startswith("@CTX"):
                    try:
                        data[label] = contexts[value[1:]][label]
                    except KeyError as error:
                        raise ValueError("Unresolved same-field shared context") from error
            data = dict(zip(CASE_KEYS, data.values()))
            if data["priority"] not in ("High", "Medium", "Low") or data["basis"] not in ("Confirmed", "Proposed", "Awaiting decision"):
                raise ValueError("Unsupported priority/expected basis")
            if data["readiness"] not in ("Ready", "Draft", "Blocked"):
                raise ValueError("Unsupported readiness")
            if data["readiness"] == "Ready" and (data["gap"] != "none" or data["basis"] == "Awaiting decision"):
                raise ValueError("Ready case has unknown oracle/gap")
            if data["readiness"] != "Ready":
                references(data["gap"], gap_ids)
            if not data["fixture"].startswith("local: "):
                fixture_refs = data["fixture"].split(", ")
                if any(value not in fixture_ids for value in fixture_refs) or len(set(fixture_refs)) != len(fixture_refs):
                    raise ValueError("Unknown/compound/duplicate fixture reference")
            steps, variants = [], []
            if rest.startswith("##### Steps\n"):
                steps, rest = read_table(rest[len("##### Steps\n"):], ["Step", "Action", "Expected", "Preservation"])
                if not steps or [row[0] for row in steps] != [str(i) for i in range(1, len(steps) + 1)] or data["action"] != "@Steps" or data["expected"] != "@Steps":
                    raise ValueError("Expanded steps must be ordered and uniquely replace inline action/expected")
            elif data["action"] == "@Steps" or data["expected"] == "@Steps":
                raise ValueError("Missing Steps table")
            if rest.startswith("##### Variants\n"):
                variants, rest = read_table(rest[len("##### Variants\n"):], ["Variant", "Inputs", "Expected"])
                if not variants or len({identifier(row[0]).casefold() for row in variants}) != len(variants):
                    raise ValueError("Empty/compound or case-insensitive duplicate variants")
            if rest:
                raise ValueError("Unsupported/unprojected case prose or table")
            cases.append({"id": identifier(case_id), "title": title, "group": group, **data, "steps": steps,
                          "screen_relative_path":paths[0] if paths else 'unknown',
                          "variants": variants or [["base", data["fixture"], data["expected"]]]})
    case_ids = {case["id"] for case in cases}
    if len({value.casefold() for value in case_ids}) != len(cases):
        raise ValueError("Duplicate or case-insensitive colliding Case ID")
    variant_ids = {f'{case["id"]}:{row[0]}' for case in cases for row in case["variants"]}
    for row in coverage:
        references(row[2], case_ids | variant_ids | gap_ids)
    covered = {target.split(":")[0] for row in coverage for target in row[2].split(", ")}
    if case_ids - covered:
        raise ValueError("Case has no reverse coverage mapping")
    return {"revision": revisions[0], "texts": texts, "scope": scope, "coverage": coverage, "gaps": gaps,
            "conventions": conventions, "data_conventions": fixtures_meta["Conventions"], "fixtures": fixtures, "cases": cases}


def export(source: Path, output: Path, *, language: str = "vi") -> dict:
    from report_model import FAMILY, VERSION, REPORT_LAYOUTS, prepare_report, _unchanged, _capture
    from render_report import render_report
    import tempfile
    source, output = Path(source), Path(output)
    if output.exists():
        raise FileExistsError("Existing workbook preserved; choose a new run path")
    if output.suffix.lower() != ".xlsx":
        raise ValueError("Output must be .xlsx")
    data, captures = prepare_report(source, language)
    template = Path(__file__).resolve().parents[1] / 'assets' / REPORT_LAYOUTS[language]['template']
    captures[template] = _capture(template)
    with tempfile.TemporaryDirectory(prefix="blend-test-report-") as directory:
        candidate = Path(directory) / "report.xlsx"
        receipt = render_report(data, candidate)
        _unchanged(captures)
        raw = candidate.read_bytes()
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as stream:
            stream.write(raw)
    return {**receipt, "family": FAMILY, "version": VERSION, "language": language,
            "cases": len(set(r.case_id for r in data.rows)), "variants": len(data.rows)}


def main():
    # JSON transport is UTF-8 even when Windows launches with a legacy codepage.
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--language", choices=("ja", "vi"), default="vi")
    args = parser.parse_args()
    try:
        result = export(args.source_dir, args.output, language=args.language)
    except (ValueError, TypeError, OSError, ImportError) as error:
        parser.exit(1, f"Report generation blocked: {error}\n")
    import json
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
