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

VERSION = "2.5.0"
CUSTOMER_VERSION = VERSION  # Compatibility name for callers; one workbook format.
REPORT_LAYOUTS = {
    "vi": {
        "template": "test-report-block-template.vi.xlsx",
        "sheets": ("Tổng quan", "Kiểm thử"),
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
    from openpyxl.cell.rich_text import CellRichText
    if isinstance(value, CellRichText):
        value = str(value)
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
    value = str(value)
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
    from openpyxl.cell.rich_text import CellRichText
    value = str(cell.value) if isinstance(cell.value, CellRichText) else cell.value
    if optional and isinstance(value, str) and not value.strip():
        return value
    if isinstance(cell.value, datetime) and field == "executed at":
        return cell.value.isoformat()
    return required(value, field)


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
    _locale['case_pending'] = 'Đang thực hiện' if _language == 'vi' else '実行中'
    _locale["instructions"] = ("Chọn trạng thái, ghi kết quả thực tế và thêm ảnh tại vùng trống khi cần. Với Không đạt, Bị chặn hoặc Không thực hiện, ghi rõ lý do và bước tiếp theo trong Kết quả thực tế."
        if _language == "vi" else "状態と実際の結果を記録し、必要な場合は空欄に画像を追加します。不合格・実行不可・実行省略では、実際の結果に理由と次の対応を記載します。")
    _locale['metric_labels'] = dict(zip(METRIC_ROWS,
        ('Số TC', 'Số biến thể', 'TC PASS', 'TC FAIL', 'Biến thể bị chặn',
         'Biến thể không thực hiện', 'Biến thể chưa thực hiện', 'TC đã đánh giá',
         'Tỷ lệ PASS theo TC', 'Tiến độ theo TC', 'TC chưa PASS', 'Trạng thái biến thể không hợp lệ')
        if _language == 'vi' else
          ('ケース数', 'バリエーション数', '対象条件を満たす合格判定数', '対象条件を満たす不合格判定数', '実行不可数', '実行省略数', '未実行数',
           '対象条件を満たす合否判定数', '合格数 / 対象条件を満たす合否判定数', '対象条件を満たす合否判定数 / 全バリエーション数', '合格未確認数', '無効な状態数')))

# 2.2 counts judgments by TC; raw execution states remain variant counts.
COMPACT_JA_METRIC_LABELS = {
    'PASS':'記録された合格ケース数', 'FAIL':'記録された不合格ケース数',
    'BLOCKED':'実行不可バリエーション数', 'SKIPPED':'実行省略バリエーション数',
    'NOT RUN':'未実行バリエーション数', 'evaluated':'合否記録のあるケース数',
    'pass_rate':'合格ケース数 / 合否記録のあるケース数',
    'completion_rate':'合否記録のあるケース数 / 全ケース数',
    'outstanding':'合格未確認ケース数', 'invalid':'無効なバリエーション状態数',
}


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
    report_version: str = VERSION
    feature_id: str = ''

    def __post_init__(self):
        case_ids = {row.case_id for row in self.rows}
        if len({value.casefold() for value in case_ids}) != len(case_ids):
            raise ValueError('Case IDs collide under Excel case-insensitive matching')
        if len({row.identity.casefold() for row in self.rows}) != len(self.rows):
            raise ValueError('Projected variant identities collide under Excel case-insensitive matching')


def template_path(data: ReportData) -> Path:
    assets = Path(__file__).resolve().parents[1] / 'assets'
    if data.report_version != VERSION:
        raise ValueError('Only test-report@2.5.0 is supported; old workbooks are preserved')
    return assets / REPORT_LAYOUTS[data.language]['template']


# Unicode White_Space accepted by Python str.strip; CLEAN handles the ASCII
# controls. This is a count predicate only: original observations stay literal.
COUNT_WHITESPACE = ' \u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000'


def _excel_without_whitespace(expression):
    value = f'CLEAN({expression})'
    for character in COUNT_WHITESPACE:
        value = f'SUBSTITUTE({value},"{character}","")'
    return value








def prepare_report(source: Path, language="vi", *, customer=True, customer_version=None):
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
            return (item['revision'], item['source_version'], item['conventions'].get('Feature ID'), [(c['id'], [v[0] for v in c['variants']], c['priority'], c['basis'], c['readiness'], c['gap'], c.get('screen_relative_path','unknown'),
                c.get('execution_lane'), [(cp[0],cp[1],cp[2],cp[3],cp[6]) for cp in c.get('checkpoints',())],
                'local:' if c['fixture'].startswith('local: ') else c['fixture']) for c in item['cases']],
                [f['id'] for f in item['fixtures']], [(g[0], g[1]) for g in item['gaps']], [r[2] for r in item['coverage']])
        if identities(design) != identities(companion):
            raise ValueError("JA/VI identity/state parity mismatch")
    data = project_report(design, language)
    if customer_version not in (None, VERSION):
        raise ValueError('Only test-report@2.5.0 is supported; old workbooks are preserved')
    return customer_report(data, design), captures


def prepare_saved_report(source, report, language='vi'):
    """Choose presentation from captured workbook provenance, not its filename."""
    from zipfile import ZipFile
    import io
    import xml.etree.ElementTree as ET
    report = Path(report)
    capture = _capture(report)
    with ZipFile(io.BytesIO(capture[0])) as archive:
        if 'docProps/custom.xml' not in archive.namelist():
            raise ValueError('Unsupported saved report provenance; only test-report@2.5.0 is supported. Original workbook preserved')
        properties = ET.fromstring(archive.read('docProps/custom.xml'))
        version = next((''.join(p.itertext()) for p in properties if p.get('name') == 'TemplateVersion'), '')
    if version != VERSION:
        raise ValueError('Unsupported saved report version '+repr(version)+'; only test-report@2.5.0 is supported. Original workbook preserved')
    data, captures = prepare_report(Path(source), language)
    captures[report] = capture
    return data, captures


def customer_report(data, design):
    """A reader projection, preserving legacy assertions and execution identities."""
    from dataclasses import replace
    vi = data.language == 'vi'
    raw_cases = {case['id']: case for case in design['cases']}
    cards = []
    for original in data.cases:
        card = dict(original)
        source = raw_cases[card['id']]
        card['priority'] = source['priority']
        card['customer_legacy'] = design['source_version'] not in ('1.2.0', '1.3.0')
        card['technical_items'] = list(card.get('technical_items', card['preparation_items']))
        card['technical_items'] += [
            ('Căn cứ' if vi else '根拠', source['source']),
            ('Bằng chứng' if vi else '証拠', source['proof']),
            ('Bảo toàn' if vi else '維持状態', source['preservation']),
            ('Reset' if vi else 'リセット', source['reset']),
        ]
        card['preparation_items'] = [(label, value) for label, value in card['preparation_items']
            if label in ('Cấu hình', '設定', 'Vai trò / quyền', '役割・権限', 'Dữ liệu test', 'テストデータ', 'Blocker', '未完了事項')]
        if vi and card['customer_legacy']:
            card['preparation_items'] = [(label, value) for label, value in card['preparation_items']
                if not (label == 'Vai trò / quyền' and value.startswith('• Dùng actor/quyền được nêu trong điều kiện;'))]
            generic_reset = 'Trước mỗi biến thể, dựng lại điều kiện/dữ liệu đầu của case bằng đường được phép; giữ các reset/fixture độc lập đã nêu trong thủ tục.'
            if source['reset'] == generic_reset:
                card['action_items'] = [item for item in card['action_items'] if item['label'] != 'Reset']
        if vi:
            card['preparation_items'] = [('Cần xác minh' if label=='Blocker' else label,
                re.sub(r'G-[A-Za-z0-9_.-]+:\s*', '', value) if label=='Blocker' else value)
                for label,value in card['preparation_items']]
            card['action_items'] = [{**item, 'label': item['label'].replace('Step ', 'Bước ', 1)} for item in card['action_items']]
        if not card['customer_legacy']:
            overall = source['expected']
            if overall == '@Checkpoints':
                overall = '\n'.join(cp[0]+' · '+cp[1]+': '+cp[4] for cp in source['checkpoints'])
            card['expected_items'] = [('Kỳ vọng chung' if vi else '共通の期待結果', display_sentence(overall))]
            if design['source_version'] == '1.2.0':
                card['variants'] = {name: {**branch, 'expected': '\n'.join(
                    cp['id']+': '+cp['expected'] for cp in branch['checkpoints'])}
                    for name, branch in card['variants'].items()}
        else:
            overall = source['expected']
            if overall == '@Steps':
                overall = '\n'.join(expected+'\n'+preserved for _, _, expected, preserved in source['steps'])
            card['expected_items'] = [('Kết quả mong đợi' if vi else '期待結果', display_sentence(overall))]
            card['variants'] = {variant: {'inputs': value[0], 'action_delta': 'none',
                'expected': ('Như kỳ vọng chung ở trên' if vi else '上記の共通期待結果と同じ')
                    if value[1] == source['expected'] else value[1], 'checkpoints': []}
                for variant, value in card['variants'].items()}
        # Readiness/authority cannot disappear behind a collapsed technical group.
        if source['basis'] != 'Confirmed' or source['readiness'] != 'Ready':
            notice = ('Kết quả ghi nhận chưa đủ điều kiện nghiệm thu: kỳ vọng hoặc chuẩn bị chưa được xác nhận.'
                if vi else '期待結果または準備が未確定のため、記録結果は受入判定を意味しません。')
            card['preparation_items'].append(('Lưu ý' if vi else '注意', notice))
        cards.append(card)
    summary = dict(data.summary)
    if vi:
        summary['limitations'] = summary['limitations'].replace('Báo cáo mới chưa thực thi.',
            'Kết quả ghi nhận và điều kiện nghiệm thu được đánh giá riêng.')
        summary['preparation'] = summary['preparation'].replace('Ready:', 'Sẵn sàng:').replace('Draft:', 'Chờ xác minh:').replace('Blocked:', 'Bị chặn:')
    result = replace(data, summary=summary, cases=tuple(cards), report_version=VERSION)
    return _readable_report(result, design)


def report_locale(data):
    locale = dict(REPORT_LAYOUTS[data.language])
    return locale


def variant_label(name, language, inputs=''):
    labels = {'lt': ('Nhỏ hơn', 'より小さい'), 'le': ('Nhỏ hơn hoặc bằng', '以下'),
        'cancel': ('Hủy xóa', '削除を取り消す'), 'delete': ('Đồng ý xóa', '削除を確定する'),
        'base': ('Trường hợp cơ bản', '基本条件')}
    if name.casefold() in labels:
        return labels[name.casefold()][language == 'ja'] + ' (' + name + ')'
    description = re.split(r'[\n;:]', inputs, maxsplit=1)[0].strip()
    if description and len(description) <= 100 and not re.search(r'(^local:|\[dummy-input:|[A-Za-z_][A-Za-z0-9_]*=)', description):
        return display_sentence(description) + ' (' + name + ')'
    return ('Trường hợp' if language == 'vi' else '条件') + ' (' + name + ')'


def _readable_report(data, design):
    """Only execution context and concrete oracles enter the reader projection."""
    from dataclasses import replace
    vi = data.language == 'vi'
    raw = {case['id']: case for case in design['cases']}
    gaps = {gap[0]: gap for gap in design['gaps']}
    generic_preservation = 'Giữ điểm, cấu hình và đối tượng không đích theo expected; chỉ thay phần thủ tục yêu cầu, không tự đổi oracle hoặc mở rộng phạm vi.'
    cards = []
    for original in data.cases:
        card = dict(original)
        source = raw[card['id']]
        card['preparation_items'] = [(label, value) for label, value in card['preparation_items']
            if label not in ('Execution lane', 'Metadata', 'Context refs','Lưu ý','注意','Cần xác minh','Blocker','未完了事項')]
        if source['gap'] != 'none':
            for name in source['gap'].split(', '):
                if gaps[name][1] != 'preparation':
                    card['preparation_items'].append(('Điều kiện còn thiếu' if vi else '未確定条件',concise_lines(gaps[name][3])))
        card['preparation_items'] = list(dict.fromkeys(card['preparation_items']))
        card['technical_items'] = []
        card['expected_items'] = []
        branches = {}
        for name, branch in card['variants'].items():
            expected = branch['expected']
            if design['source_version'] == '1.2.0':
                expected = '\n'.join(cp['expected'] for cp in branch['checkpoints'])
            if card['customer_legacy']:
                variant = next(value for value in source['variants'] if value[0] == name)
                expected = variant[2]
                if expected in ('@Steps', source['expected']):
                    expected = source['expected']
                if expected == '@Steps':
                    expected = '\n'.join(value+'\n'+preserve for _, _, value, preserve in source['steps'])
                if source['preservation'] and source['preservation'] != generic_preservation and source['preservation'] not in expected:
                    expected += '\n' + source['preservation']
            inputs, action = branch['inputs'], branch['action_delta']
            if 'Thao tác riêng: ' in inputs:
                inputs, action = inputs.split('Thao tác riêng: ',1)
                inputs = inputs.rstrip(' ;\n')
            if name.casefold() == 'base' and inputs.strip() == 'Kiểm tra toàn bộ tình huống: Toàn bộ thủ tục theo đúng thứ tự; các đối chứng cùng fixture được kiểm trong cùng lượt, không bỏ bước':
                inputs = ''
            branches[name] = {**branch, 'expected': display_sentence(expected), 'inputs':inputs,'action_delta':action,
                'label': variant_label(name, data.language, inputs)}
        if all('Thao tác riêng: ' in branch['inputs'] for branch in card['variants'].values()):
            card['action_items'] = []
        card['variants'] = branches
        cards.append(card)
    summary = dict(data.summary)
    summary['preparation'] = ''
    labels = working.SCOPE_LABELS[data.language]
    summary['scope'] = display_markup(public_text(design['scope'][1][labels[1][0]],'scope'))
    limits = design['scope'][0][labels[0][5]]
    if limits.startswith('Báo cáo mới chưa thực thi.'):
        limits = ''
    pending = sum(not row.eligible for row in data.rows)
    notice = (f'{pending} trường hợp chưa đủ điều kiện kết luận nghiệm thu. Chỉ kết luận nghiệm thu khi đã làm rõ điều kiện và có đủ bằng chứng theo testcase.' if vi else
        f'{pending}条件は受入判定の条件が未確定です。期待結果・実行条件を確定し、十分な証拠を確認してから受入判定を行ってください。') if pending else ''
    summary['limitations'] = '\n'.join(value for value in (limits,notice) if value)
    return replace(data, cases=tuple(cards), summary=summary)


def descriptive_image_title(value):
    """Office's default object description is not an evidence title."""
    value = str(value or '').strip()
    token = re.sub(r'[\s\d_-]+', '', value).casefold()
    return bool(value) and token not in ('picture','image','screenshot','photo','ảnh','hìnhảnh','画像','スクリーンショット','図')


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
    return ('Bước ' if language == 'vi' else 'ステップ ') + number


def project_report(design, language):
    locale = REPORT_LAYOUTS[language]
    parts = locale['parts']
    fixtures = {f['id']: f['values'] for f in design['fixtures']}
    gap_records = {gap[0]: gap for gap in design['gaps']}
    rows, cards = [], []
    for case in design['cases']:
        if design.get('source_version') in ('1.2.0', '1.3.0'):
            card, records = _scenario_projection(case, design, language, fixtures, gap_records)
            if design['source_version'] == '1.3.0':
                card['priority'] = case['priority']
                card['technical_items'] = card['preparation_items'] + [
                    ('Metadata', '\n'.join(key+': '+str(case[key]) for key in
                        ('group','source','priority','basis','readiness','execution_lane','gap',
                         'configuration','trigger','observation','actor','fixture','expected','proof','preservation') if key in case))]
                card['context_refs'] = case.get('context_refs',{})
                card['contexts'] = {name:design['contexts'][name] for name in
                    dict.fromkeys(value[1:] for value in card['context_refs'].values())}
                if card['context_refs']:
                    card['technical_items'].append(('Context refs', '\n'.join(key+': '+value for key,value in card['context_refs'].items())))
                    card['technical_items'].extend((name,'\n'.join(key+': '+value for key,value in values.items())) for name,values in card['contexts'].items())
                card['preparation_items'] = [(label, value) for label,value in card['preparation_items']
                    if label in ('Cấu hình','設定','Vai trò / quyền','役割・権限')]
                card['expected_items'] = [('Expected', display_sentence(public_text(case['expected'],'overall expected')))]
                for variant in case['variants']:
                    card['variants'][variant[0]]['expected'] = display_sentence(public_text(variant[3],'variant final expected'))
                records = [ReportRow(r.case_id,r.variant,r.screen_function,r.conditions,
                    card['variants'][r.variant]['expected'],r.eligible) for r in records]
            cards.append(card)
            rows.extend(records)
            continue
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
    return ReportData(language, summary, tuple(rows), tuple(cards),
        VERSION,
        design['conventions'].get('Feature ID', ''))


def _scenario_projection(case, design, language, fixtures, gaps):
    """Shared procedure once, concrete branch oracles only at their checkpoints."""
    vi = language == 'vi'
    common = case['fixture'][7:] if case['fixture'].startswith('local: ') else '\n'.join(
        '\n'.join(f'{label}: {value}' for label,value in zip(working.FIXTURE_LABELS[language],fixtures[name]))
        for name in case['fixture'].split(', '))
    fixture_label='Dữ liệu test' if vi else 'テストデータ'
    fixture_items=([(fixture_label,concise_lines(common,dummy_input=True))] if case['fixture'].startswith('local: ') else
        [(fixture_label+' · '+name,concise_lines('\n'.join(
            f'{label}: {value}' for label,value in zip(working.FIXTURE_LABELS[language],fixtures[name])),dummy_input=True))
         for name in case['fixture'].split(', ')])
    preparation = [('Cấu hình' if vi else '設定', concise_lines(case['configuration'])),
        ('Vai trò / quyền' if vi else '役割・権限', concise_lines(case['actor'])), *fixture_items,
        ('Trigger' if vi else 'トリガー', concise_lines(case['trigger'])),
        ('Execution lane', case['execution_lane'])]
    if case['gap'] != 'none':
        preparation.append(('Blocker' if vi else '未完了事項', concise_lines('\n'.join(gaps[g][3] for g in case['gap'].split(', ')))))
    actions = [{'label':step_label(n,language),'value':display_sentence(public_text(a,'step action'))} for n,a,_,_ in case['steps']]
    actions.append({'label':'Reset' if vi else 'リセット','value':display_sentence(public_text(case['reset'],'reset'))})
    shared_expected = [(step_label(n,language),concise_lines(e)) for n,_,e,_ in case['steps'] if e and e != '@Checkpoints']
    shared_expected += [(step_label(n,language)+' · '+('Giữ nguyên' if vi else '維持'),concise_lines(p)) for n,_,_,p in case['steps'] if p]
    shared_expected += [('Giữ nguyên' if vi else '維持',concise_lines(case['preservation']))]
    variants, records = {}, []
    for variant, inputs, delta, _ in case['variants']:
        cps = [{'id':cp,'step':step,'stage':stage,'expected':public_text(expected,'checkpoint expected'),
            'focus':public_text(focus,'checkpoint focus'),'artifact':artifact}
            for v,cp,step,stage,expected,focus,artifact in case['checkpoints'] if v == variant]
        variants[variant] = {'inputs':public_text(inputs,'variant inputs',dummy_input=True),
            'action_delta':public_text(delta,'variant action delta'),'checkpoints':cps}
        expected = '\n'.join(cp['id']+': '+cp['expected'] for cp in cps)
        condition = '\n'.join(label+': '+value for label,value in preparation)+'\n'+inputs+'\n'+delta
        records.append(ReportRow(case['id'],variant,case['function'],condition,expected,
            case['basis']=='Confirmed' and case['readiness']=='Ready'))
    path = case.get('screen_relative_path','unknown')
    screen_path(path,language)
    card = {'id':case['id'],'title':display_markup(public_text(case['title'],'title')),
        'function':display_markup(public_text(case['function'],'function')),'screen_relative_path':path,
        'preparation_items':preparation,'action_items':actions,'expected_items':shared_expected,
        'expected_source':case['expected'],'fixture_source':case['fixture'],'variants':variants,
        'proof':public_text(case['proof'],'proof'),'reset':public_text(case['reset'],'reset')}
    return card, records
