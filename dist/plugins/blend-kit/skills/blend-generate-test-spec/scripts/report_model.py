"""Canonical editable test-report schema and source projection; no execution or access attestation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import ipaddress
import math
from pathlib import Path
import re
import unicodedata
from urllib.parse import parse_qsl, unquote, urlsplit

import export_report as working

VERSION = "2.0.0"
REPORT_LAYOUTS = {
    "vi": {
        "template": "test-report-block-template.vi.xlsx",
        "sheets": ("Tổng quan", "Testcases"),
        "title": "Báo cáo kiểm thử",
        "block_title": "Kiểm thử chi tiết",
        "headers": (),
        "detail_headers": ("Mã kiểm thử", "Nội dung", "Chi tiết"),
        "detail_link": "Xem chi tiết", "evidence_link": "Bằng chứng", "bug_link": "Lỗi",
        "no_data": "Chưa có dữ liệu", "partial": "Đã đóng lượt chạy; còn lỗi hoặc phạm vi chưa được xác nhận đạt.",
        "evaluated": "Các biến thể trong thiết kế này đã được xác nhận đạt; không khẳng định toàn bộ chức năng đã được bao phủ.",
        "observation": "Chỉ là quan sát; kỳ vọng hoặc điều kiện kiểm chưa được xác nhận.",
        "out_of_scope": "Ngoài phạm vi lượt chạy", "reason": "Lý do / tồn đọng", "executed": "Thực hiện",
        "labels": {"run_id": "Lượt chạy", "feature": "Chức năng", "build": "Build", "environment": "Môi trường", "period": "Thời gian", "scope": "Phạm vi", "excluded": "Ngoài phạm vi", "limitations": "Giới hạn", "conclusion": "Kết luận", "open_items": "Tồn đọng / bước tiếp theo", "cases": "Số testcase", "variants": "Số biến thể", "selected_variants": "Biến thể trong lượt chạy", "evaluated_variants": "Biến thể có kết luận hợp lệ", "pass_rate": "Tỷ lệ PASS / biến thể có kết luận", "completion_rate": "Tỷ lệ có kết luận / biến thể xác nhận trong scope", "case_statuses": "Kết quả testcase", "variant_statuses": "Trạng thái biến thể"},
        "parts": {"configuration": "Cấu hình", "trigger": "Kích hoạt", "observation": "Vị trí quan sát", "actor": "Vai trò / quyền", "inputs": "Dữ liệu", "action": "Thao tác", "expected": "Kết quả mong đợi", "preservation": "Bảo toàn", "steps": "Bước", "actual": "Thực tế", "evidence": "Bằng chứng"},
    },
    "ja": {
        "template": "test-report-block-template.ja.xlsx",
        "sheets": ("概要", "テストケース"),
        "title": "テスト結果報告書",
        "block_title": "テストケース詳細",
        "headers": (),
        "detail_headers": ("テストID", "項目", "詳細"),
        "detail_link": "詳細を確認", "evidence_link": "証拠", "bug_link": "不具合",
        "no_data": "データなし", "partial": "実行を終了しました。未解決の不具合、または合格を確認できていない範囲があります。",
        "evaluated": "本設計の全バリエーションで合格を確認しました。機能全体の網羅を保証するものではありません。",
        "observation": "観測記録のみ。期待結果または実行条件が未確定です。",
        "out_of_scope": "今回の実行対象外", "reason": "理由・残存事項", "executed": "実施",
        "labels": {"run_id": "実行ID", "feature": "機能", "build": "ビルド", "environment": "環境", "period": "実施期間", "scope": "対象範囲", "excluded": "対象外", "limitations": "制限事項", "conclusion": "結論", "open_items": "残存事項・次の対応", "cases": "ケース数", "variants": "バリエーション数", "selected_variants": "実行対象のバリエーション数", "evaluated_variants": "有効な判定のあるバリエーション数", "pass_rate": "合格率 / 有効な判定", "completion_rate": "判定完了率 / 対象内の確定バリエーション", "case_statuses": "ケース別状態", "variant_statuses": "バリエーション別状態"},
        "parts": {"configuration": "設定", "trigger": "起動", "observation": "確認箇所", "actor": "役割・権限", "inputs": "入力データ", "action": "操作", "expected": "期待結果", "preservation": "維持状態", "steps": "手順", "actual": "実際の結果", "evidence": "証拠"},
    },
}
for _layout in REPORT_LAYOUTS.values():
    _layout.update(header_row=4, start_row=5, detail_header_row=4, detail_start_row=5, summary_start_row=4)
REPORT_LAYOUTS["vi"]["labels"].update(passed_variants="Biến thể được xác nhận PASS", confirmed_variants="Biến thể xác nhận trong scope")
REPORT_LAYOUTS["ja"]["labels"].update(passed_variants="有効な合格バリエーション数", confirmed_variants="対象内の確定バリエーション数")
REPORT_LAYOUTS["ja"]["font"] = "Yu Gothic"
REPORT_LAYOUTS["vi"]["font"] = "Arial"


@dataclass(frozen=True)
class ClosureConfirmation:
    closed_by: str
    closed_at: str
    source: str
    # Exact intended recipients, not the agent's authenticated account.
    audience: str


@dataclass(frozen=True)
class EvidenceAccess:
    url: str
    audience: str
    verified_by: str
    verified_at: str
    method: str  # human-attestation or recipient-session
    source: str


def required(value, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing text: {field}")
    # Markdown decoding belongs only to working.parse_sources. Excel observations
    # and the resulting parsed design are already literal values, not HTML input.
    if len(value) > 32767:
        raise ValueError(f"Text exceeds Excel cell limit: {field}")
    if any(ord(char) < 32 and char not in "\n\t" for char in value):
        raise ValueError(f"Unsupported control character: {field}")
    return value


def timestamp(value, field: str) -> datetime:
    parsed = datetime.fromisoformat(required(value, field).replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"Timestamp requires timezone: {field}")
    return parsed


def shared_url(value: str, field: str) -> str:
    value = required(value, field)
    if any(char.isspace() for char in value):
        raise ValueError(f"Use a sole shared HTTPS URL without surrounding prose: {field}")
    # Inspect encoded components without rewriting the approved URL. Neither
    # percent-encoded locators nor encoded credential names may enter .rels.
    decoded = value
    for _ in range(5):
        if any(ord(char) < 32 for char in decoded):
            raise ValueError(f"Encoded control character in report URL: {field}")
        url = urlsplit(decoded)
        host = (url.hostname or "").lower()
        if url.scheme != "https" or not host or url.username or url.password or "." not in host or host in ("localhost",) or host.endswith((".local", ".localhost", ".internal")):
            raise ValueError(f"Evidence requires a shared HTTPS URL: {field}")
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            pass
        else:
            if not address.is_global:
                raise ValueError(f"Private evidence address: {field}")
        if PRIVATE.search(decoded):
            raise ValueError(f"Private/internal locator in report URL: {field}")
        if any(re.search(r"token|secret|password|signature|credential|api[_-]?key", name, re.I)
               for part in (url.query, url.fragment) for name, _ in parse_qsl(part, keep_blank_values=True)):
            raise ValueError(f"Credential-bearing URL: {field}")
        next_decoded = unquote(decoded)
        if next_decoded == decoded:
            break
        decoded = next_decoded
    else:
        raise ValueError(f"Excessive URL encoding cannot be validated: {field}")
    return value


PRIVATE = re.compile(r"(?<![\w])(?:[A-Za-z]:[\\/]|\\\\|file:|localhost\b|127\.0\.0\.1|~/|/(?:Users|home|tmp|private|mnt|var|opt|etc|root|workspace|Volumes)/)|(?:\.agents|\.codex|blend-context|docker-codeigniter)[\\/]|(?:\b(?:research|sources|application|tests|docs)/[^\s]+)|(?:\b[^\s/]+\.(?:md|sql|php|py)(?:\b|#))", re.I)


def url_spans(value: str):
    """Keep complete literal URL tokens; punctuation never truncates a locator."""
    return re.finditer(r"(?:https?|file)://\S+", value, re.I)


def public_text(value: str, field: str, *, dummy_input: bool = False) -> str:
    value = required(value, field)
    # Explicit source-authorized dummy inputs retain their meaning. They are not
    # evidence locators and cannot exempt actual results, notes, URLs or metadata.
    scan = value
    if dummy_input:
        scan = re.sub(r"\[dummy-input: [^\]\n]+\]", "(intentional test input)", scan)
    if PRIVATE.search(unquote(scan)) or re.search(r"@(?:Steps|CTX-)|sha256:|<!--|^\s*\|.*\|\s*$", scan, re.M):
        raise ValueError(f"Private/internal reference in report field: {field}")
    if re.search(r"\b(?:password|secret|access[_-]?token|api[_-]?key)\s*[:=]\s*\S+", scan, re.I):
        raise ValueError(f"Potential credential in report field: {field}")
    for match in url_spans(scan):
        shared_url(match.group(), field)
    return value


def display_lines(value: str, width: int) -> int:
    """Shared display contract: JA full-width glyphs occupy two Latin units."""
    return sum(max(1, math.ceil(sum(2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
                                    for char in line) / width)) for line in value.split("\n"))


def _records(value, cls):
    if isinstance(value, cls):
        return value
    if not isinstance(value, dict):
        raise ValueError(f"Expected {cls.__name__} object")
    try:
        record = cls(**value)
    except TypeError as error:
        raise ValueError(f"Invalid {cls.__name__} fields") from error
    return record


def _capture(path: Path) -> tuple[bytes, tuple]:
    stat = path.stat()
    raw = path.read_bytes()
    after = path.stat()
    identity = (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns)
    if identity != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise ValueError("Input changed while captured")
    return raw, identity


def _unchanged(captures: dict[Path, tuple[bytes, tuple]]) -> None:
    for path, (raw, identity) in captures.items():
        current, current_identity = _capture(path)
        if current != raw or current_identity != identity:
            raise ValueError("Input identity/content changed during operation")


def _read_text(cell, field: str, *, optional=False) -> str:
    if cell.data_type == "f":
        raise ValueError(f"Untrusted formula in recorded field: {field}")
    if optional and cell.value is None:
        return ""
    if optional and isinstance(cell.value, str) and not cell.value.strip():
        return cell.value
    if isinstance(cell.value, datetime) and field == "executed at":
        return cell.value.isoformat()
    return required(cell.value, field)


FAMILY = "test-report"
SUMMARY_FIELDS = {"feature": 4, "revision": 5, "run_id": 6, "build": 7,
                  "environment": 8, "tester": 9, "period": 10, "scope": 11,
                  "excluded": 12, "limitations": 13, "preparation": 14}
INPUT_FIELDS = ("run_id", "build", "environment", "tester", "period")
METRIC_ROWS = {"cases": 16, "variants": 17, "PASS": 18, "FAIL": 19,
               "BLOCKED": 20, "SKIPPED": 21, "NOT RUN": 22,
               "evaluated": 23, "pass_rate": 24, "completion_rate": 25,
               "outstanding": 26, "invalid": 27}
CASE_HEADER_ROW = 29
CASE_START_ROW = 30
for _language, _locale in REPORT_LAYOUTS.items():
    _locale["statuses"] = dict(zip(("PASS", "FAIL", "BLOCKED", "SKIPPED", "NOT RUN"),
        ("Đạt", "Không đạt", "Bị chặn", "Không thực hiện", "Chưa thực hiện") if _language == "vi" else
        ("合格", "不合格", "実行不可", "実行省略", "未実行")))
    _locale["labels"].update(revision="Phiên bản kiểm thử" if _language == "vi" else "テスト設計版",
                            tester="Người thực hiện" if _language == "vi" else "実施者")
    _locale['labels']['period'] = 'Thời điểm thực hiện (kèm múi giờ)' if _language == 'vi' else '実施日時（タイムゾーン付き）'
    _locale['labels']['build'] = 'Phiên bản ứng dụng' if _language == 'vi' else 'アプリケーション版'
    _locale['labels']['run_id'] = 'Lần kiểm thử' if _language == 'vi' else 'テスト実行ID'
    _locale['case_pending'] = 'Chưa đủ kết luận' if _language == 'vi' else '判定未完了'
    _locale["instructions"] = ("Chọn trạng thái, ghi kết quả thực tế và thêm ảnh tại vùng trống khi cần. Với Không đạt, Bị chặn hoặc Không thực hiện, ghi rõ lý do và bước tiếp theo trong Kết quả thực tế."
        if _language == "vi" else "状態と実際の結果を記録し、必要な場合は空欄に画像を追加します。不合格・実行不可・実行省略では、実際の結果に理由と次の対応を記載します。")
    _locale['metric_labels'] = dict(zip(METRIC_ROWS,
        ('Số TC', 'Số biến thể', 'TC PASS', 'TC FAIL', 'Biến thể bị chặn',
         'Biến thể không thực hiện', 'Biến thể chưa thực hiện', 'TC đã đánh giá',
         'Tỷ lệ PASS theo TC', 'Tiến độ theo TC', 'TC chưa PASS', 'Trạng thái biến thể không hợp lệ')
        if _language == 'vi' else
        ('ケース数', 'バリエーション数', '対象条件を満たす合格判定数', '対象条件を満たす不合格判定数', '実行不可数', '実行省略数', '未実行数',
         '対象条件を満たす合否判定数', '合格数 / 対象条件を満たす合否判定数', '対象条件を満たす合否判定数 / 全バリエーション数', '合格未確認数', '無効な状態数')))


@dataclass(frozen=True)
class ReportRow:
    case_id: str
    variant: str
    screen_function: str
    conditions: str
    expected: str
    eligible: bool
    screen_preview: str = ''
    conditions_preview: str = ''
    expected_preview: str = ''

    @property
    def identity(self):
        return f"{self.case_id} / {self.variant}"


@dataclass(frozen=True)
class ReportData:
    language: str
    summary: dict[str, str]
    rows: tuple[ReportRow, ...]
    cases: tuple[dict, ...] = ()

    def __post_init__(self):
        case_ids = {row.case_id for row in self.rows}
        if len({value.casefold() for value in case_ids}) != len(case_ids):
            raise ValueError('Case IDs collide under Excel case-insensitive matching')
        if len({row.identity.casefold() for row in self.rows}) != len(self.rows):
            raise ValueError('Projected variant identities collide under Excel case-insensitive matching')


# Unicode White_Space accepted by Python str.strip; CLEAN handles the ASCII
# controls. This is a count predicate only: original observations stay literal.
COUNT_WHITESPACE = ' \u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000'


def _excel_without_whitespace(expression):
    value = f'CLEAN({expression})'
    for character in COUNT_WHITESPACE:
        value = f'SUBSTITUTE({value},"{character}","")'
    return value


def recorded_decision_inputs(actual: str, evidence: str) -> bool:
    """Recorded count minimum; URL privacy and recipient access remain separate checks."""
    first = evidence.split('\n', 1)[0]
    if not actual.strip() or not first.startswith('https://') or any(ch.isspace() or ord(ch) < 32 for ch in first):
        return False
    authority = re.split(r'[/\?#]', first[8:], maxsplit=1)[0]
    return '@' not in authority and re.search(r'.+\..+', authority) is not None


def summary_formulas(data: ReportData) -> dict[str, str]:
    """Only visible input rows drive counts; identity selectors survive row sorting."""
    locale = REPORT_LAYOUTS[data.language]
    sheet = "'" + locale["sheets"][1] + "'!"
    start, end = locale["start_row"], max(locale["start_row"], locale["start_row"] + len(data.rows) - 1)
    ranges = {col: f"{sheet}${col}${start}:${col}${end}" for col in "AEFG"}
    statuses = locale["statuses"]
    def count(token, rows=None, judged=False):
        selected = data.rows if rows is None else rows
        if judged:
            selected = [row for row in selected if row.eligible]
        if not selected:
            return '0'
        # A one-ID mask is Boolean, unlike an addition of masks; SUMPRODUCT
        # requires explicit numeric coercion in both cases.
        mask = '--(' + '+'.join(f'({ranges["A"]}="{row.identity}")' for row in selected) + ')'
        terms = ([] if rows is None and not judged else [mask]) + [f'--EXACT({ranges["F"]},"{statuses[token]}")']
        if judged:
            first = f'LEFT({ranges["G"]},FIND(CHAR(10),{ranges["G"]}&CHAR(10))-1)'
            # Query/fragment delimiters also terminate the authority. Padding
            # makes FIND(start=9) safe for empty/not-yet-entered evidence cells.
            separated = f'SUBSTITUTE(SUBSTITUTE({first},"?","/"),"#","/")'
            host = f'MID({separated},9,FIND("/",{separated}&"/////////",9)-9)'
            terms += [f'--(LEN({_excel_without_whitespace(ranges["E"])})>0)',
                      f'--EXACT(LEFT({first},8),"https://")',
                      f'--(LEN({_excel_without_whitespace(first)})=LEN({first}))',
                      f'--ISNUMBER(SEARCH("?*.?*",{host}))', f'--ISERROR(SEARCH("@",{host}))']
        return 'SUMPRODUCT(' + ','.join(terms) + ')'
    formulas = {"B17": f"=COUNTA({ranges['A']})"}
    for token in statuses:
        formulas[f"B{METRIC_ROWS[token]}"] = '=' + count(token, judged=token in ('PASS', 'FAIL'))
    formulas.update(B16=f'=COUNTA(A{CASE_START_ROW}:A{max(CASE_START_ROW, CASE_START_ROW + len(set(r.case_id for r in data.rows)) - 1)})',
                    B23="=B18+B19", B24=f'=IF(B23=0,"{locale["no_data"]}",B18/B23)',
                    B25=f'=IF(B17=0,"{locale["no_data"]}",B23/B17)',
                    B26="=B17-B18", B27=f'=B17-SUM({",".join(count(t) for t in statuses)})')
    for index, case_id in enumerate(dict.fromkeys(r.case_id for r in data.rows), CASE_START_ROW):
        rows = [r for r in data.rows if r.case_id == case_id]
        passing, failing = count('PASS', rows, True), count('FAIL', rows, True)
        skipped, blocked, unrun = count('SKIPPED', rows), count('BLOCKED', rows), count('NOT RUN', rows)
        formulas[f"B{index}"] = (f'=IF({failing}>0,"{statuses["FAIL"]}",'
            f'IF({passing}={len(rows)},"{statuses["PASS"]}",IF({skipped}={len(rows)},"{statuses["SKIPPED"]}",'
            f'IF({blocked}>0,"{statuses["BLOCKED"]}",IF({unrun}={len(rows)},"{statuses["NOT RUN"]}","{locale["case_pending"]}")))))')
    if any(len(value) > 8192 for value in formulas.values()):
        raise ValueError("Report exceeds Excel formula length; split the requested run scope explicitly")
    return formulas


def detail_backlink_formula(identity: str, data: ReportData) -> str:
    locale = REPORT_LAYOUTS[data.language]
    sheet = "'" + locale['sheets'][1] + "'"
    start = locale['start_row']
    end = max(start, start + len(data.rows) - 1)
    return f'=HYPERLINK("#{sheet}!A"&(MATCH("{identity}",{sheet}!$A${start}:$A${end},0)+{start - 1}),"{identity}")'


def prepare_report(source: Path, language="vi"):
    if language not in REPORT_LAYOUTS:
        raise ValueError("Unsupported language; choose ja or vi")
    paths = [source / f"{family}.{language}.md" for family in working.HEADINGS[language]]
    other = "ja" if language == "vi" else "vi"
    companions = [source / f"{family}.{other}.md" for family in working.HEADINGS[other]]
    if any(p.exists() for p in companions):
        if not all(p.exists() for p in companions):
            raise ValueError("Partial JA/VI source trio")
        paths += companions
    captures = {path: _capture(path) for path in paths}
    captured = {path.name: value[0] for path, value in captures.items()}
    design = working.parse_sources(source, language, captured=captured)
    if len(paths) == 6:
        companion = working.parse_sources(source, other, captured=captured)
        def identities(item):
            return (item['revision'], [(c['id'], [v[0] for v in c['variants']], c['priority'], c['basis'], c['readiness'], c['gap'], c.get('screen_relative_path','unknown'),
                'local:' if c['fixture'].startswith('local: ') else c['fixture']) for c in item['cases']],
                [f['id'] for f in item['fixtures']], [(g[0], g[1]) for g in item['gaps']], [r[2] for r in item['coverage']])
        if identities(design) != identities(companion):
            raise ValueError("JA/VI identity/state parity mismatch")
    return project_report(design, language), captures


def excerpt(value, limit=140):
    """A visibly incomplete source excerpt, never a replacement assertion."""
    first = next((line.strip() for line in value.splitlines() if line.strip()), '')
    if len(first) > limit:
        return first[:limit].rsplit(' ', 1)[0] + '…'
    return first + ('…' if len(value.splitlines()) > 1 else '')


def screen_path(value, language):
    if value == 'unknown':
        return 'Chưa xác minh' if language == 'vi' else '未確認'
    if value == 'not-applicable':
        return 'Không áp dụng' if language == 'vi' else '該当なし'
    value = public_text(value, 'screen_relative_path')
    parsed = urlsplit(value)
    if not value.startswith('/') or value.startswith('//') or parsed.netloc or parsed.scheme or any(c.isspace() for c in value) or '..' in unquote(parsed.path).split('/'):
        raise ValueError('screen_relative_path must be a verified relative screen URL without domain')
    return value


LIST_MARKER = re.compile(r'^(?:[-+*•])\s+')
INLINE_CODE = re.compile(r'`([^`\n]+)`')


def display_markup(value):
    """Convert Markdown-only emphasis into stable plain spreadsheet notation."""
    value = str(value)
    pieces = []
    cursor = 0
    for match in INLINE_CODE.finditer(value):
        pieces.append(value[cursor:match.start()].replace('**', '').replace('`', ''))
        # Preserve every byte inside inline code. Literal stars such as **24
        # are business data, not Markdown emphasis.
        pieces.append('[' + match.group(1) + ']')
        cursor = match.end()
    pieces.append(value[cursor:].replace('**', '').replace('`', ''))
    return ''.join(pieces)


def markdown_leak(value):
    """True only for presentation Markdown, not literal stars in [code]."""
    value = str(value)
    outside_code = re.sub(r'\[[^\]\n]*\]', '', value)
    return '`' in value or '**' in outside_code


def strip_list_marker(value):
    """Remove source list syntax before the workbook adds its own bullet."""
    return LIST_MARKER.sub('', str(value).strip(), count=1)


def concise_lines(value, *, dummy_input=False):
    """Readable bullets without duplicating source list markers."""
    value = public_text(value, 'display text', dummy_input=dummy_input)
    value = value.replace('; ', ';\n')
    return '\n'.join('• ' + display_sentence(part) for part in value.splitlines() if part.strip())


def display_sentence(value):
    """Sentence case for reader text; identifiers and punctuation remain literal."""
    value = strip_list_marker(display_markup(value))
    if value.startswith(('[', '/', 'http://', 'https://')):
        return value
    for index, char in enumerate(value):
        if char.isalpha():
            return value[:index] + (char.upper() if char.islower() else char) + value[index + 1:]
    return value


def numbered_lines(value, field):
    """Keep explicit source numbering together with its instruction/assertion."""
    value = public_text(value, field)
    result = []
    for line in value.splitlines():
        match = re.match(r'^(\d+)\.\s*(.*)$', line.strip())
        result.append((match.group(1) + '.', display_sentence(match.group(2))) if match else ('•', display_sentence(line)))
    return [(label, text) for label, text in result if text]


def step_label(value, language):
    number = str(value).removesuffix('.')
    return ('Step ' if language == 'vi' else 'ステップ ') + number


def project_report(design, language):
    locale = REPORT_LAYOUTS[language]
    parts = locale['parts']
    fixtures = {f['id']: f['values'] for f in design['fixtures']}
    gap_records = {gap[0]: gap for gap in design['gaps']}
    rows, cards = [], []
    for case in design['cases']:
        common_inputs = case['fixture'][7:] if case['fixture'].startswith('local: ') else '\n'.join(
            '\n'.join(f'{label}: {value}' for label,value in zip(working.FIXTURE_LABELS[language],fixtures[name]))
            for name in case['fixture'].split(', '))
        preparation_items = [
            ('Cấu hình' if language=='vi' else '設定', concise_lines(case['configuration'])),
            ('Vai trò / quyền' if language=='vi' else '役割・権限', concise_lines(case['actor'])),
            ('Dữ liệu test' if language=='vi' else 'テストデータ', concise_lines(common_inputs,dummy_input=True)),
        ]
        generic_trigger = ('Thực hiện đúng thao tác và biến thể dưới đây; ' if language=='vi' else '下記の操作とバリエーションを実施し、')
        trigger_display = case['trigger'][len(generic_trigger):] if case['trigger'].startswith(generic_trigger) else case['trigger']
        if trigger_display.strip():
            preparation_items.append(('Trigger' if language=='vi' else 'トリガー', concise_lines(trigger_display)))
        gap_text=[]
        if case['gap']!='none':
            for name in case['gap'].split(', '):
                gap_text.append(name+': '+public_text(gap_records[name][3],'gap'))
        if gap_text:
            preparation_items.append(('Blocker' if language=='vi' else '未完了事項', concise_lines('\n'.join(gap_text))))
        raw_actions = ([(step_label(n,language),public_text(action,'step action')) for n,action,_,_ in case['steps']]
                       if case['steps'] else [(step_label(label,language) if label[0].isdigit() else label,text)
                                              for label,text in numbered_lines(case['action'],'action')])
        action_items=[]
        for label,action in raw_actions:
            action_items.append({'label':label,'value':display_sentence(action)})
        # Reset remains operational, but appears as the final technical step instead of a separate footer.
        action_items.append({'label':'Reset' if language=='vi' else 'リセット','value':display_sentence(public_text(case['reset'],'reset'))})
        expected_items=[]
        if case['steps']:
            preserved=[]
            for number,_,value,preserve in case['steps']:
                expected_items.append((str(number)+'.',concise_lines(value)))
                if preserve not in preserved:
                    preserved.append(preserve)
            for preserve in preserved:
                expected_items.append(('Giữ nguyên' if language=='vi' else '維持',concise_lines(preserve)))
        else:
            expected_items.extend(numbered_lines(case['expected'],'expected'))
        expected_items.append(('Giữ nguyên' if language=='vi' else '維持',concise_lines(case['preservation'])))
        generic_observation = ('Quan sát nơi nêu trong thủ tục/expected; ' if language=='vi' else '手順・期待結果に記載した確認箇所で、')
        observation_display = case['observation'][len(generic_observation):] if case['observation'].startswith(generic_observation) else case['observation']
        if observation_display.strip():
            expected_items.append(('Quan sát tại' if language=='vi' else '確認箇所',concise_lines(observation_display)))
        path = case.get('screen_relative_path','unknown')
        screen_path(path,language)
        cards.append({'id':case['id'],'title':display_markup(public_text(case['title'],'title')),
                      'function':display_markup(public_text(case['function'],'function')),
                      'screen_relative_path':path,'preparation_items':preparation_items,'action_items':action_items,'expected_items':expected_items,
                      'expected_source':case['expected'],'proof':public_text(case['proof'],'proof'),'reset':public_text(case['reset'],'reset'),
                      'fixture_source':case['fixture'],
                      'variants':{v[0]:(public_text(v[1],'variant inputs',dummy_input=True),public_text(v[2],'variant expected')) for v in case['variants']}})
        for variant in case['variants']:
            blocks = [(parts[k], public_text(case[k], k)) for k in ('configuration', 'trigger', 'observation', 'actor')]
            inputs = case['fixture'][7:] if case['fixture'].startswith('local: ') else '\n'.join(
                '\n'.join(f'{label}: {value}' for label, value in zip(working.FIXTURE_LABELS[language], fixtures[name]))
                for name in case['fixture'].split(', '))
            if variant[0] != 'base' or variant[1] != case['fixture']:
                inputs += '\n' + variant[1]
            blocks.append((parts['inputs'], public_text(inputs, 'inputs', dummy_input=True)))
            if case['steps']:
                actions = '\n'.join(f'{n}. {public_text(action, "step action")}' for n, action, _, _ in case['steps'])
                expected = '\n'.join(f'{n}. {public_text(value, "step expected")}\n{parts["preservation"]}: {public_text(preserve, "step preservation")}' for n, _, value, preserve in case['steps'])
                if variant[2] != '@Steps':
                    expected += '\n' + variant[2]
            else:
                actions = public_text(case['action'], 'action')
                expected = public_text(case['expected'], 'expected')
                if variant[2] != case['expected']:
                    expected += '\n' + variant[2]
            expected += f'\n{parts["preservation"]}: ' + public_text(case['preservation'], 'preservation')
            conditions = '\n'.join(f'{label}: {value}' for label, value in blocks) + f'\n{parts["action"]}: {actions}'
            conditions += '\n' + ('Khôi phục: ' if language == 'vi' else '復元: ') + public_text(case['reset'], 'reset')
            conditions += '\n' + parts['evidence'] + ': ' + public_text(case['proof'], 'proof')
            eligible = case['basis'] == 'Confirmed' and case['readiness'] == 'Ready'
            basis = ({'Confirmed': 'Đã xác nhận', 'Proposed': 'Đề xuất', 'Awaiting decision': 'Chờ xác nhận'} if language == 'vi' else
                     {'Confirmed': '確定', 'Proposed': '提案', 'Awaiting decision': '確認待ち'})[case['basis']]
            readiness = ({'Ready': 'Sẵn sàng', 'Draft': 'Đang chuẩn bị', 'Blocked': 'Bị chặn'} if language == 'vi' else
                         {'Ready': '実行可能', 'Draft': '準備中', 'Blocked': '実行不可'})[case['readiness']]
            conditions += '\n' + ('Kỳ vọng: ' if language == 'vi' else '期待結果: ') + basis
            conditions += '\n' + ('Chuẩn bị: ' if language == 'vi' else '実行準備: ') + readiness
            if not eligible:
                conditions += '\n' + locale['observation']
            if case['gap'] != 'none':
                for gap_id in case['gap'].split(', '):
                    gap = gap_records[gap_id]
                    conditions += '\n' + ('Khoảng trống: ' if language == 'vi' else '未完了事項: ')
                    conditions += public_text(gap[3] + '\n' + gap[4], 'gap decision and impact')
            title = public_text(case['group'] + ' — ' + case['function'] + '\n' + case['title'], 'screen/function')
            condition_preview = (f'Chuẩn bị: {readiness}\nKỳ vọng: {basis}\nDữ liệu (trích): {excerpt(variant[1], 65)}\nThao tác (trích): {excerpt(actions, 110)}'
                                 if language == 'vi' else
                                 f'実行準備: {readiness}\n期待結果: {basis}\n入力データ（抜粋）: {excerpt(variant[1], 45)}\n操作（抜粋）: {excerpt(actions, 65)}')
            expected_preview = ('Kỳ vọng: ' if language == 'vi' else '期待結果: ') + basis + '\n' + excerpt(expected, 180 if language == 'vi' else 100)
            rows.append(ReportRow(case['id'], variant[0], title, conditions, public_text(expected, 'expected'), eligible,
                                  excerpt(case['function'], 70 if language == 'vi' else 35) + '\n' + excerpt(case['title'], 80 if language == 'vi' else 45),
                                  condition_preview, expected_preview))
    labels = working.SCOPE_LABELS[language]
    readiness_counts = {state: sum(case['readiness'] == state for case in design['cases']) for state in ('Ready', 'Draft', 'Blocked')}
    preparation = (f"Ready: {readiness_counts['Ready']} · Draft: {readiness_counts['Draft']} · Blocked: {readiness_counts['Blocked']}\n"
                   "Tính theo TC, độc lập với execution status. Mỗi biến thể có status, actual và ảnh riêng."
                   if language == 'vi' else
                   f"実行可能: {readiness_counts['Ready']} · 準備中: {readiness_counts['Draft']} · 実行不可: {readiness_counts['Blocked']}\n"
                   "ケース単位の準備状況であり、実行結果とは別です。各ケースのバリエーションごとに結果と証拠を記録します。")
    summary = {'feature': public_text(design['conventions']['Feature'], 'feature'), 'revision': public_text(design['revision'], 'revision'),
        'preparation': preparation,
        'scope': public_text(design['scope'][1][labels[1][0]], 'scope'),
        'excluded': public_text(design['scope'][1][labels[1][1]], 'excluded'),
        'limitations': public_text(design['scope'][0][labels[0][5]], 'limitations')}
    if design['gaps']:
        summary['limitations'] += '\n' + (
            f"{len(design['gaps'])} khoảng trống được giữ trong Điều kiện kiểm thử của các testcase tương ứng."
            if language == 'vi' else
            f"{len(design['gaps'])}件の未完了事項を対応するテストケースの準備に記載しています。")
        referenced = {gap_id for case in design['cases'] if case['gap'] != 'none'
                      for gap_id in case['gap'].split(', ')}
        for gap in design['gaps']:
            if gap[0] not in referenced:
                summary['limitations'] += '\n' + public_text(gap[3] + '\n' + gap[4], 'unassigned gap')
    for index, label in ((1, 'Chuẩn bị' if language == 'vi' else '準備'),
                         (3, 'Điều kiện bắt đầu' if language == 'vi' else '開始条件'),
                         (4, 'Điều kiện kết thúc' if language == 'vi' else '終了条件')):
        summary['scope'] += '\n' + label + ': ' + public_text(design['scope'][2][labels[2][index]], 'run prerequisite')
    missing = sum(case['screen_relative_path']=='unknown' for case in cards)
    if missing:
        summary['limitations'] += '\n' + (f'{missing} testcase chưa có URL màn hình tương đối được xác minh.' if language=='vi' else f'{missing}ケースの画面相対URLが未確認です。')
    summary = {key: display_markup(value) for key, value in summary.items()}
    return ReportData(language, summary, tuple(rows), tuple(cards))
