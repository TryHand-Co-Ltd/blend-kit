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

VERSION = "1.0.0"
REPORT_LAYOUTS = {
    "vi": {
        "template": "test-report-template.vi.xlsx",
        "sheets": ("Tổng quan", "Kiểm thử", "Chi tiết"),
        "title": "Báo cáo kiểm thử",
        "headers": ("Mã kiểm thử", "Màn hình / chức năng", "Điều kiện / thao tác", "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái", "Bằng chứng / lỗi"),
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
        "template": "test-report-template.ja.xlsx",
        "sheets": ("概要", "テスト", "テスト詳細"),
        "title": "テスト結果報告書",
        "headers": ("テストID", "画面・機能", "条件・操作", "期待結果", "実際の結果", "状態", "証拠・不具合"),
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
    for url in re.findall(r"(?:https?|file)://[^\s<>\])]+", scan):
        shared_url(url, field)
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
    if isinstance(cell.value, datetime) and field == "executed at":
        return cell.value.isoformat()
    return required(cell.value, field)


FAMILY = "test-report"
SUMMARY_FIELDS = {"feature": 4, "revision": 5, "run_id": 6, "build": 7,
                  "environment": 8, "tester": 9, "period": 10, "scope": 11,
                  "excluded": 12, "limitations": 13}
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
    _locale["instructions"] = ("Nhập kết quả thực tế, trạng thái và bằng chứng; mục chưa đạt cần lý do và bước tiếp theo. "
        "Mục ngoài phạm vi chọn Không thực hiện; kết quả mong đợi chưa được xác nhận không được tính đạt."
        if _language == "vi" else "実際の結果・状態・証拠を入力し、合格以外は理由と次の対応を記入します。"
        "対象外は実行省略を選び、期待結果が未確定の場合は合格に含めません。")
    _locale['metric_labels'] = dict(zip(METRIC_ROWS,
        ('Số trường hợp kiểm thử', 'Số kịch bản', 'Kịch bản ghi nhận đạt', 'Kịch bản ghi nhận không đạt', 'Kịch bản bị chặn',
         'Kịch bản không thực hiện', 'Kịch bản chưa thực hiện', 'Kịch bản đã ghi kết quả và bằng chứng',
         'Tỷ lệ đạt / kịch bản đã ghi kết quả', 'Tỷ lệ đã ghi kết quả / toàn bộ kịch bản', 'Kịch bản chưa đạt', 'Trạng thái không hợp lệ')
        if _language == 'vi' else
        ('ケース数', 'バリエーション数', '合格記録数', '不合格記録数', '実行不可数', '実行省略数', '未実行数',
         '結果・証拠の記入済数', '合格記録数 / 判定記入済数', '判定記入済数 / 全バリエーション数', '合格未確認数', '無効な状態数')))


@dataclass(frozen=True)
class ReportRow:
    case_id: str
    variant: str
    screen_function: str
    conditions: str
    expected: str
    eligible: bool

    @property
    def identity(self):
        return f"{self.case_id} / {self.variant}"


@dataclass(frozen=True)
class ReportData:
    language: str
    summary: dict[str, str]
    rows: tuple[ReportRow, ...]


def summary_formulas(data: ReportData) -> dict[str, str]:
    """Only visible input rows drive counts; identity selectors survive row sorting."""
    locale = REPORT_LAYOUTS[data.language]
    sheet = "'" + locale["sheets"][1] + "'!"
    start, end = locale["start_row"], max(locale["start_row"], locale["start_row"] + len(data.rows) - 1)
    ranges = {col: f"{sheet}${col}${start}:${col}${end}" for col in "AEFG"}
    statuses = locale["statuses"]
    def count(token, identity=None, valid=False):
        args = [ranges['F'], f'"{statuses[token]}"']
        if identity is not None:
            args += [ranges['A'], f'"{identity}"']
        if valid:
            args += [ranges['E'], '"<>"', ranges['G'], '"<>"']
        return "COUNTIFS(" + ",".join(args) + ")"
    def total(terms):
        return "SUM(" + ",".join(terms) + ")" if terms else "0"
    formulas = {"B17": f"=COUNTA({ranges['A']})"}
    for token in statuses:
        terms = [count(token, row.identity, True) for row in data.rows if row.eligible] if token in ("PASS", "FAIL") else [count(token)]
        formulas[f"B{METRIC_ROWS[token]}"] = "=" + total(terms)
    formulas.update(B16=f'=COUNTA(A{CASE_START_ROW}:A{max(CASE_START_ROW, CASE_START_ROW + len(set(r.case_id for r in data.rows)) - 1)})',
                    B23="=B18+B19", B24=f'=IF(B23=0,"{locale["no_data"]}",B18/B23)',
                    B25=f'=IF(B17=0,"{locale["no_data"]}",B23/B17)',
                    B26="=B17-B18", B27=f'=B17-SUM({",".join(count(t) for t in statuses)})')
    for index, case_id in enumerate(dict.fromkeys(r.case_id for r in data.rows), CASE_START_ROW):
        rows = [r for r in data.rows if r.case_id == case_id]
        passing = total([count("PASS", r.identity, True) for r in rows if r.eligible])
        failing = total([count("FAIL", r.identity, True) for r in rows if r.eligible])
        blocked = total([count("BLOCKED", r.identity) for r in rows])
        formulas[f"B{index}"] = (f'=IF({failing}>0,"{statuses["FAIL"]}",'
            f'IF({passing}={len(rows)},"{statuses["PASS"]}",IF({blocked}>0,"{statuses["BLOCKED"]}","{statuses["NOT RUN"]}")))')
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
            return (item['revision'], [(c['id'], [v[0] for v in c['variants']], c['priority'], c['basis'], c['readiness'], c['gap'],
                'local:' if c['fixture'].startswith('local: ') else c['fixture']) for c in item['cases']],
                [f['id'] for f in item['fixtures']], [(g[0], g[1]) for g in item['gaps']], [r[2] for r in item['coverage']])
        if identities(design) != identities(companion):
            raise ValueError("JA/VI identity/state parity mismatch")
    return project_report(design, language), captures


def project_report(design, language):
    locale = REPORT_LAYOUTS[language]
    parts = locale['parts']
    fixtures = {f['id']: f['values'] for f in design['fixtures']}
    rows = []
    for case in design['cases']:
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
            title = public_text(case['group'] + ' — ' + case['function'] + '\n' + case['title'], 'screen/function')
            rows.append(ReportRow(case['id'], variant[0], title, conditions, public_text(expected, 'expected'), eligible))
    labels = working.SCOPE_LABELS[language]
    summary = {'feature': public_text(design['conventions']['Feature'], 'feature'), 'revision': public_text(design['revision'], 'revision'),
        'scope': public_text(design['scope'][1][labels[1][0]], 'scope'),
        'excluded': public_text(design['scope'][1][labels[1][1]], 'excluded'),
        'limitations': public_text(design['scope'][0][labels[0][5]], 'limitations')}
    if design['gaps']:
        summary['limitations'] += '\n' + '\n'.join(public_text(g[3] + '\n' + g[4], 'gap decision and impact') for g in design['gaps'])
    for index, label in ((1, 'Chuẩn bị' if language == 'vi' else '準備'),
                         (3, 'Điều kiện bắt đầu' if language == 'vi' else '開始条件'),
                         (4, 'Điều kiện kết thúc' if language == 'vi' else '終了条件')):
        summary['scope'] += '\n' + label + ': ' + public_text(design['scope'][2][labels[2][index]], 'run prerequisite')
    return ReportData(language, summary, tuple(rows))


