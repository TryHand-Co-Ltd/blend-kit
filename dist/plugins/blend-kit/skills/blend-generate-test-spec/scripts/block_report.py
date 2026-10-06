"""Two-sheet TC blocks. Source and result cells have separate, explicit roles."""
from collections import Counter
from pathlib import Path
import hashlib
import io
import re

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.worksheet.datavalidation import DataValidation

import report_model as model

# ponytail: bounded reserved space avoids reflow of existing results; an explicitly
# requested future layout version is needed above 48 reader rows.
READABLE_EVIDENCE_ROWS = 48


def evidence_width(sheet):
    return sum(int((sheet.column_dimensions[c].width or 13)*7+5) for c in 'ABCDE')-16


def customer_image_anchor(sheet, rows, position, width, height, picture):
    """Two-cell placement makes Excel collapse pictures with their owning row group."""
    from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, TwoCellAnchor
    def marker(offset):
        for row in rows:
            row_pixels = (sheet.row_dimensions[row].height or 15)*4/3
            if offset < row_pixels:
                return AnchorMarker(col=0, row=row-1, rowOff=round(offset*9525))
            offset -= row_pixels
        if abs(offset) < 1:
            return AnchorMarker(col=0, row=rows[-1])
        raise ValueError('Image exceeds customer evidence capacity')
    first, last = marker(position), marker(position+height)
    remaining = width
    for column, name in enumerate('ABCDE'):
        column_pixels = int((sheet.column_dimensions[name].width or 13)*7+5)
        if remaining < column_pixels:
            last.col, last.colOff = column, round(remaining*9525)
            break
        remaining -= column_pixels
    else:
        raise ValueError('Image exceeds customer evidence width')
    return TwoCellAnchor(editAs='twoCell', _from=first, to=last, pic=picture)


def image_size(sheet, image):
    """Read displayed dimensions from either supported native anchor."""
    from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor
    anchor = image.anchor
    if not isinstance(anchor, TwoCellAnchor):
        return anchor.ext.cx/9525, anchor.ext.cy/9525
    columns = lambda end: sum(int((sheet.column_dimensions[chr(65+c)].width or 13)*7+5) for c in range(end))
    width = columns(anchor.to.col)-columns(anchor._from.col)+(anchor.to.colOff-anchor._from.colOff)/9525
    height = sum((sheet.row_dimensions[r+1].height or 15)*4/3 for r in range(anchor._from.row,anchor.to.row))+(anchor.to.rowOff-anchor._from.rowOff)/9525
    return width, height


def reader_blank_rows(data, cards):
    """Hide empty layout gaps, while keeping every instruction and input visible."""
    return {2,3,4} | {row for card in cards for row,_,kind,_,_,_ in card['rows'] if kind=='spacer'}


def layout(data):
    """Pure current report projection; old workbook layouts are unsupported."""
    if data.report_version != model.VERSION:
        raise ValueError('Only test-report@2.5.0 is supported')
    return _readable_layout(data)


def _readable_layout(data):
    """Core is visible; only direct evidence has a single collapsed group."""
    from render_report import _chunks
    vi = data.language == 'vi'
    cards, inputs, cursor = [], {}, 5
    for case in data.cases:
        start, rows = cursor, []
        members = [record for record in data.rows if record.case_id == case['id']]
        def add(value='', kind='text', right=None, height=None, label=None):
            nonlocal cursor
            first = cursor
            for piece in _chunks(value, 104, 23):
                rows.append((cursor, piece, kind, right, height, label))
                cursor += 1
            return first
        add(case['id']+' — '+case['title'], 'title')
        status = add('Kết quả tình huống' if vi else 'ケース結果', 'case_status')
        add(case['function'], 'key_value', label='Màn hình / chức năng' if vi else '画面・機能')
        for label, value in case['preparation_items']:
            add(value, 'key_value', label=label)
        for item in case['action_items']:
            add(item['value'], 'step', label=item['label'])
        add('', 'matrix_header')
        for record in members:
            branch = case['variants'][record.variant]
            own = model.display_sentence(branch['inputs'])
            description = re.split(r'[\n;:]', own, maxsplit=1)[0].strip()
            if branch['label'] == description+' ('+record.variant+')':
                own = own[len(description):].lstrip(' ;:\n')
            if branch['action_delta'] != 'none':
                own += '\n'+('Thao tác: ' if vi else '操作: ')+model.display_sentence(branch['action_delta'])
            expected = _chunks(branch['expected'], 44, 23)
            own_parts = _chunks(own, 34, 23)
            add('', 'matrix_padding',height=3)
            row = add(branch['label'], 'matrix', right=expected[0], label=own_parts[0])
            for index in range(1,max(len(expected),len(own_parts))):
                add('', 'matrix_continuation', right=expected[index] if index<len(expected) else '',
                    label=own_parts[index] if index<len(own_parts) else '')
            inputs[record.identity] = {'status': f'E{row}', 'actual': f'D{row}', 'picture': None, 'checkpoints': {}}
        header = add('Ảnh minh chứng — Chưa có ảnh' if vi else '証拠画像 — 画像なし', 'label', height=20)
        for record in members:
            fields = inputs[record.identity]
            fields['evidence_row'] = header
            branch = case['variants'][record.variant]
            checkpoints = branch['checkpoints']
            if case.get('customer_legacy'):
                checkpoints = [{'id': '', 'artifact': 'screenshot', 'expected': branch['expected'], 'focus': branch['label']}]
            for cp in checkpoints:
                picture_rows = [add('', 'picture', height=1) for _ in range(READABLE_EVIDENCE_ROWS)] if cp['artifact']=='screenshot' else []
                binding = {**cp, 'picture_rows': picture_rows, 'label_row': header, 'compact': True, 'customer': True, 'readable': True, 'title': branch['label']}
                if picture_rows and fields['picture'] is None:
                    fields['picture'] = picture_rows[0]
                if cp['id']:
                    fields['checkpoints'][cp['id']] = binding
                else:
                    fields.update(picture_rows=picture_rows, label_row=header, note=f'A{picture_rows[0]}')
                    # Source 1.0/1.1 has no declared checkpoint grammar. This is
                    # an image owner for the existing variant result, not a new oracle.
                    fields['evidence_slots'] = {'CP-result': {**binding, 'id': 'CP-result',
                        'source_anchor': 'variant Expected / existing Steps'}}
        raw_status_cells = {token: f'B{add("", "technical_metric", label=token, height=1)}'
            for token in model.report_locale(data)['statuses']}
        add('', 'spacer', height=6)
        cards.append({'id': case['id'], 'start': start, 'status_row': status, 'rows': rows, 'members': members,
            'technical_rows': [int(value[1:]) for value in raw_status_cells.values()], 'raw_status_cells': raw_status_cells})
    return cards, inputs


def evidence_bindings(fields):
    """Declared checkpoints or the source-derived result image slot."""
    return fields['checkpoints'] or fields.get('evidence_slots', {})




def formulas(data, cards=None, inputs=None):
    """Case-level recorded counts feed Overview; never count prose as results."""
    if cards is None:
        cards, inputs = layout(data)
    sheet = "'" + model.report_locale(data)['sheets'][1] + "'!"
    states = model.report_locale(data)['statuses']
    output, case_statuses = {}, {}
    def counted(token, members):
        refs = [inputs[record.identity] for record in members]
        terms = []
        for ref in refs:
            status = sheet+ref['status']
            terms.append(f'IF(EXACT({status},"{states[token]}"),1,0)')
        return 'SUM('+','.join(terms)+')'
    for card in cards:
        members = card['members']
        for token,address in card['raw_status_cells'].items():
            output[(1,address)]='='+counted(token,members)
        passed, failed = counted('PASS', members), counted('FAIL', members)
        skipped, blocked, unrun = (counted(token, members) for token in ('SKIPPED', 'BLOCKED', 'NOT RUN'))
        status = (f'=IF({failed}>0,"{states["FAIL"]}",IF({passed}={len(members)},"{states["PASS"]}",'
                  f'IF({skipped}={len(members)},"{states["SKIPPED"]}",IF({blocked}>0,"{states["BLOCKED"]}",'
                  f'IF({unrun}={len(members)},"{states["NOT RUN"]}","{model.report_locale(data)["case_pending"]}")))))')
        output[(1, f'B{card["status_row"]}')] = status
        case_statuses[card['id']] = sheet + f'B{card["status_row"]}'
    for index, card in enumerate(cards, model.CASE_START_ROW):
        value = case_statuses[card['id']]
        output[(0, f'C{index}')] = value if value.startswith('=') else '=' + value
    output[(0, 'B16')] = f'={len(cards)}'
    output[(0, 'B17')] = f'={len(data.rows)}'
    last = cards[-1]['rows'][-1][0] if cards else 5
    def raw_count(token):
        return f'SUMIF({sheet}A5:A{last},"{token}",{sheet}B5:B{last})'
    case_status_range = f'C{model.CASE_START_ROW}:C{model.CASE_START_ROW+len(cards)-1}'
    output[(0, 'B18')] = f'=COUNTIF({case_status_range},"{states["PASS"]}")'
    output[(0, 'B19')] = f'=COUNTIF({case_status_range},"{states["FAIL"]}")'
    for token in ('BLOCKED', 'SKIPPED', 'NOT RUN'):
        output[(0, f'B{model.METRIC_ROWS[token]}')] = '=' + raw_count(token)
    output[(0, 'B23')] = '=B18+B19'
    no_data = model.report_locale(data)['no_data']
    output[(0, 'B24')] = f'=IF(B23=0,"{no_data}",B18/B23)'
    output[(0, 'B25')] = f'=IF(B16=0,"{no_data}",B23/B16)'
    output[(0, 'B26')] = '=B16-B18'
    # Count only the exact designated status cells, including invalid pasted input.
    output[(0, 'B27')] = ('=B17-SUM('+sheet+f'B5:B{last})')
    if any(len(value) > 8192 for value in output.values()):
        raise ValueError('Report exceeds Excel formula-size limit; preserve source and narrow the explicitly requested run')
    return output


def build(data):
    from render_report import _text, _height, _jump, _finish
    locale = model.report_locale(data)
    path = model.template_path(data)
    book = load_workbook(path, rich_text=True)
    if book.sheetnames != list(locale['sheets']) or {p.name:p.value for p in book.custom_doc_props} != {'TemplateFamily':model.FAMILY,'TemplateVersion':data.report_version,'Language':data.language}:
        raise ValueError('Block template identity or sheets mismatch')
    summary, tests = book.worksheets
    from openpyxl.packaging.custom import StringProperty
    if data.feature_id:
        book.custom_doc_props.append(StringProperty(name='FeatureID',value=data.feature_id))
    book.custom_doc_props.append(StringProperty(name='DesignRevision',value=data.summary['revision']))
    # The source template contains a visible illustrative block for humans.
    # It is presentation-only and must never leak into a generated report.
    for merged in list(tests.merged_cells.ranges):
        if merged.min_row >= locale['start_row']:
            tests.unmerge_cells(str(merged))
    if tests.max_row >= locale['start_row']:
        tests.delete_rows(locale['start_row'], tests.max_row - locale['start_row'] + 1)
    for row in list(tests.row_dimensions):
        if row >= locale['start_row']:
            del tests.row_dimensions[row]
    tests.data_validations.dataValidation = []
    tests.conditional_formatting._cf_rules.clear()
    _text(tests['A1'], locale['block_title'])
    tests['A1'].font = Font(name=locale['font'], size=16, bold=True, color='172033')
    _text(tests['A2'], locale['instructions'])
    instructions = 'Đọc bối cảnh, thao tác và kỳ vọng; ghi thực tế/kết quả từng trường hợp. Mỗi biến thể khôi phục dữ liệu ban đầu độc lập. Mở nhóm hàng để xem ảnh và chi tiết.' if data.language=='vi' else '前提・操作・期待結果を確認し、条件ごとに実際の結果を記録します。各条件は初期データから独立して実行し、画像・詳細は行グループを展開して確認します。'
    if any(case.get('customer_legacy') for case in data.cases):
        instructions += ' Tham chiếu “tab Evidence” trong quan sát cũ nay nằm tại Ảnh minh chứng của TC.' if data.language=='vi' else '旧記録の「Evidence」シート参照は、該当ケースの証拠画像欄に移されています。'
    _text(tests['A2'], instructions)
    _text(tests['A2'], '')
    _text(summary['A2'], '')
    tests['A2'].font = Font(name=locale['font'], size=10, color='475569')
    tests.merge_cells('A2:E2')
    tests.row_dimensions[2].height = 42
    tests.row_dimensions[2].height = max(42, model.display_lines(tests['A2'].value, 112)*14+6)
    # Keep the validation cell compact. The remaining columns preserve the
    # total content width used by long conditions/actions and screen details.
    for column, width in (('A', 23), ('B', 24), ('C', 26), ('D', 14), ('E', 45)):
        tests.column_dimensions[column].width = width
    for column,width in (('A',24),('B',35),('C',45),('D',35),('E',19)):
        tests.column_dimensions[column].width=width
    cards, inputs = layout(data)
    merged_rows = set()
    def merge_row(value):
        """Emitted rows are disjoint; avoid openpyxl's scan of every prior range."""
        from openpyxl.worksheet.merge import MergedCellRange
        merged = MergedCellRange(tests, value)
        if merged.min_row != merged.max_row or merged.min_row < locale['start_row'] or merged.min_row in merged_rows:
            raise ValueError('Generated row merge is not disjoint')
        merged_rows.add(merged.min_row)
        tests.merged_cells.ranges.add(merged)
        tests._clean_merge_range(merged)
    thin = Side(style='thin', color='D9E2EC')
    if data.language == 'ja':
        for key,label in model.COMPACT_JA_METRIC_LABELS.items():
            row=model.METRIC_ROWS[key]
            _text(summary.cell(row,1),label,emphasis=False)
            _height(summary,row,(label,''),(26,105))
    for key, row in model.SUMMARY_FIELDS.items():
        value = '' if key in model.INPUT_FIELDS else data.summary.get(key, '')
        _text(summary.cell(row,2), value,emphasis=False)
        _height(summary,row,(summary.cell(row,1).value or '',value),(26,105))
        if key in model.INPUT_FIELDS:
            summary.cell(row,2).fill=PatternFill('solid',fgColor='F8FAFC')
            summary.cell(row,2).protection=Protection(locked=False)
    for index,card in enumerate(cards,model.CASE_START_ROW):
        case = next(case for case in data.cases if case['id']==card['id'])
        _text(summary.cell(index,1),card['id'],emphasis=False)
        _text(summary.cell(index,2),model.display_markup(case['title']),emphasis=False)
        _jump(summary.cell(index,2),tests.title,card['start'])
        _height(summary,index,(card['id'],case['title']),(26,83))
        for row,value,kind,right,height,label in card['rows']:
            # Titles already have whole-cell bold/white styling. Excel does not
            # consistently inherit that color across partial inline rich runs.
            _text(tests.cell(row,1),value,emphasis=kind!='title')
            if kind in ('matrix','matrix_header','matrix_continuation'):
                if kind == 'matrix_header':
                    headings = ((1,'Trường hợp'),(2,'Dữ liệu / thao tác riêng'),(3,'Kết quả mong đợi'),(4,'Kết quả thực tế'),(5,'Đánh giá')) if data.language=='vi' else ((1,'条件'),(2,'データ・個別操作'),(3,'期待結果'),(4,'実際の結果'),(5,'結果'))
                    for column,value in (headings):
                        _text(tests.cell(row,column),value)
                        tests.cell(row,column).font=Font(name=locale['font'],size=11,bold=True,color='172033')
                else:
                    _text(tests.cell(row,2),label or '')
                    _text(tests.cell(row,3),right)
                    if kind=='matrix':
                        _text(tests.cell(row,4),'')
                        tests.cell(row,4).protection=Protection(locked=False)
                        tests.cell(row,4).number_format='@'
                        tests.cell(row,4).fill=PatternFill('solid',fgColor='F8FAFC')
            elif kind == 'matrix_padding':
                for column in (4,5):
                    tests.cell(row,column).fill=PatternFill('solid',fgColor='F8FAFC')
            elif kind in ('status','case_status'):
                # Status always lives in the compact B cell. It must stay
                # unmerged so Excel/Google Sheets anchor the popup beside it.
                pass
            elif kind=='screen':
                _text(tests.cell(row,1),'Màn hình / chức năng' if data.language=='vi' else '画面・機能')
                tests.cell(row,1).font=Font(name=locale['font'],size=11,bold=True,color='172033')
                _text(tests.cell(row,2),value)
                tests.cell(row,2).font=Font(name=locale['font'],size=11,bold=True,color='172033')
                merge_row(f'B{row}:C{row}')
                _text(tests.cell(row,4),'Đường dẫn' if data.language=='vi' else '相対URL')
                tests.cell(row,4).font=Font(name=locale['font'],size=11,bold=True,color='172033')
                _text(tests.cell(row,5),right)
            elif kind in ('key_value','expected_item','technical','technical_metric'):
                _text(tests.cell(row,1),label or '•')
                tests.cell(row,1).font=Font(name=locale['font'],size=11,bold=True,color='172033')
                merge_row(f'B{row}:E{row}')
                _text(tests.cell(row,2),value)
            elif kind=='step':
                _text(tests.cell(row,1),label)
                tests.cell(row,1).font=Font(name=locale['font'],size=11,bold=True,color='172033')
                merge_row(f'B{row}:E{row}')
                _text(tests.cell(row,2),value)
            else:
                merge_row(f'A{row}:E{row}')
            if kind in ('title','section','label','variant','technical_heading','evidence_label'):
                tests.cell(row,1).font=Font(name=locale['font'],size=14 if kind=='title' else 11,bold=True,color='172033')
                tests.cell(row,1).alignment=Alignment(vertical='center',wrap_text=True)
            if kind in ('status','case_status'):
                tests.cell(row,1).font=Font(name=locale['font'],size=11,bold=True,color='172033')
                tests.cell(row,1).alignment=Alignment(vertical='center',wrap_text=True)
                if kind == 'title':
                    for column in range(1,6):
                        tests.cell(row,column).fill=PatternFill('solid',fgColor='E8EEF5')
                    tests.cell(row,1).font=Font(name=locale['font'],size=13,bold=True,color='172033')
                    tests.cell(row,6).fill=PatternFill('solid',fgColor='E8EEF5')
                tests.row_dimensions[row].height=max(tests.row_dimensions[row].height or 0,34)
            if kind=='section':
                for column in range(1,6):
                    tests.cell(row,column).fill=PatternFill('solid',fgColor='E8EEF5')
                tests.row_dimensions[row].height=max(tests.row_dimensions[row].height or 0,28)
            if kind == 'variant':
                for column in range(1,6):
                    tests.cell(row,column).fill=PatternFill('solid',fgColor='F8FAFC')
            if kind in ('input','picture'):
                tests.cell(row,1).fill=PatternFill('solid',fgColor='F8FAFC')
                tests.cell(row,1).protection=Protection(locked=False)
                tests.cell(row,1).number_format='@'
                for column in range(1,6):
                    tests.cell(row,column).border=Border(top=thin,bottom=thin,left=thin if column==1 else Side(),right=thin if column==5 else Side())
            if kind in ('screen','key_value','expected_item','step','status','case_status'):
                for column in range(1,6):
                    tests.cell(row,column).border=Border(bottom=thin)
            for column in range(1,6):
                cell = tests.cell(row,column)
                if cell.value is not None:
                    cell.alignment=Alignment(horizontal=cell.alignment.horizontal,vertical='center',wrap_text=True)
            if kind == 'screen':
                _height(tests,row,(value,right or ''),(38,38))
            elif kind in ('key_value','expected_item','step'):
                _height(tests,row,(value,),(104,))
            else:
                _height(tests,row,(value,),(112,))
            if height:
                tests.row_dimensions[row].height=height
            values,widths = ((value or '',label or '',right or ''),(24,35,45)) if kind in ('matrix','matrix_continuation') else ((value or '',),(104 if kind in ('key_value','expected_item','step','technical') else 112,))
            if kind in ('key_value','expected_item','step','technical'):
                values,widths=(label or '',value or ''),(23,104)
            widths = tuple(width-3 for width in widths)
            _height(tests,row,values,widths,line_height=14,padding=6)
            tests.row_dimensions[row].height=max(20, max(model.display_lines(v,w) for v,w in zip(values,widths))*14+6)
            if kind == 'matrix_header':
                tests.row_dimensions[row].height=max(28,max(model.display_lines(tests.cell(row,c).value,w)
                    for c,w in zip(range(1,6),(21,32,42,32,16)))*14+6)
            if kind == 'title':
                tests.row_dimensions[row].height=max(28,tests.row_dimensions[row].height)
            if height is not None:
                tests.row_dimensions[row].height=height
            if kind in ('technical','technical_metric','picture','evidence_label','evidence_note'):
                tests.row_dimensions[row].hidden=True
                tests.row_dimensions[row].outlineLevel=1
            if kind == 'technical_heading':
                tests.row_dimensions[row].collapsed=True
            if kind=='label' and value in ('Ảnh minh chứng — mở nhóm hàng để xem','証拠画像 — 行グループを展開して確認'):
                tests.row_dimensions[row].collapsed=True
            if kind == 'technical_metric':
                tests.row_dimensions[row].outlineLevel=0
                _text(tests.cell(row,1), label)
            if kind == 'label' and value in ('Ảnh minh chứng — Chưa có ảnh','証拠画像 — 画像なし'):
                tests.row_dimensions[row].collapsed=False
            if kind == 'picture':
                tests.row_dimensions[row].outlineLevel=0
            if kind == 'title':
                for column in range(1,6):
                    tests.cell(row,column).fill=PatternFill('solid',fgColor='17324D')
                tests.cell(row,1).font=Font(name=locale['font'],size=13,bold=True,color='FFFFFF')
            for column in range(1,6):
                tests.cell(row,column).alignment=Alignment(vertical='top',wrap_text=True)
    validation=DataValidation(type='list',formula1='"'+','.join(locale['statuses'].values())+'"',allow_blank=False)
    validation.showErrorMessage=True
    tests.add_data_validation(validation)
    for fields in inputs.values():
        _text(tests[fields['status']],locale['statuses']['NOT RUN'])
        tests[fields['status']].fill=PatternFill('solid',fgColor='F8FAFC')
        tests[fields['status']].protection=Protection(locked=False)
        validation.add(fields['status'])
    for (index,address),formula in formulas(data,cards,inputs).items():
        book.worksheets[index][address]=formula
        book.worksheets[index][address].font=Font(name=locale['font'],size=11,color='172033')
        book.worksheets[index][address].alignment=Alignment(vertical='center',wrap_text=True)
    for sheet in (summary,tests):
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value is not None:
                    cell.alignment=Alignment(horizontal='left' if sheet is tests else cell.alignment.horizontal,
                        vertical='top',wrap_text=True,
                        indent=1 if sheet is tests else 0)
    _finish(summary,'C',model.CASE_START_ROW+len(cards)-1)
    _finish(tests,'E',cards[-1]['rows'][-1][0] if cards else 4)
    summary.auto_filter.ref = f'A{model.CASE_HEADER_ROW}:C{model.CASE_START_ROW+len(cards)-1}'
    # A column boundary inside merged customer headers fails native Sheets conversion.
    summary.freeze_panes = 'A2'
    tests.freeze_panes='A2'
    from openpyxl.worksheet.views import Selection
    for sheet in (summary,tests):
        # freeze_panes appends selections when a template already has panes.
        sheet.sheet_view.selection = [Selection(pane='bottomLeft',activeCell='A2',sqref='A2')]
    for row in reader_blank_rows(data,cards):
        tests.row_dimensions[row].hidden=True
    for row in (2,14,28):
        if all(summary.cell(row,column).value in (None,'') for column in range(1,4)):
            summary.row_dimensions[row].hidden=True
    tests.sheet_properties.outlinePr.summaryBelow=False
    tests.page_setup.orientation='portrait'
    tests.page_setup.paperSize=tests.PAPERSIZE_A3
    book.active=0
    from render_report import apply_reader_spacing
    apply_reader_spacing(book)
    return book


def check(report,source,language='vi',phase='in-progress',*,closure_confirmation=None,evidence_access=(),screenshots=()):
    from check_report import _package,_formula_reference_key
    if phase not in ('in-progress','complete'):
        raise ValueError('Unknown check phase')
    data,captures=model.prepare_saved_report(Path(source),report,language)
    asset=model.template_path(data)
    captures[asset]=model._capture(asset)
    report=Path(report)
    # prepare_saved_report pins the same bytes used to select its presentation.
    raw=captures[report][0]
    book=load_workbook(io.BytesIO(raw), rich_text=True)
    pristine=build(data)
    locale=model.report_locale(data)
    if book.sheetnames!=pristine.sheetnames or {p.name:p.value for p in book.custom_doc_props}!={p.name:p.value for p in pristine.custom_doc_props}:
        raise ValueError('Unsupported block report schema')
    cards,inputs=layout(data)
    gaps,layout_notes,observations=[],[],[]
    editable={(locale['sheets'][0],f'B{model.SUMMARY_FIELDS[key]}') for key in model.INPUT_FIELDS}
    editable|={(locale['sheets'][1],fields[key]) for fields in inputs.values() for key in ('status','actual')}
    editable|={(locale['sheets'][1],fields['note']) for fields in inputs.values() if 'note' in fields}
    for fields in inputs.values():
        editable.add((locale['sheets'][1], f'A{fields["evidence_row"]}'))
        areas = [cp['picture_rows'] for cp in fields['checkpoints'].values()]
        if 'picture_rows' in fields:
            areas.append(fields['picture_rows'])
        editable.update((locale['sheets'][1], f'A{row}') for rows in areas for row in rows)
    summary,tests=book.worksheets
    for key in model.INPUT_FIELDS:
        value=model._read_text(summary[f'B{model.SUMMARY_FIELDS[key]}'],key,optional=True)
        if value:
            model.public_text(value,key)
        else:
            gaps.append(f'{summary.title}: missing {key}')
    if phase=='complete' and summary[f'B{model.SUMMARY_FIELDS["period"]}'].value:
        closed=model._records(closure_confirmation,model.ClosureConfirmation)
        if model.timestamp(summary[f'B{model.SUMMARY_FIELDS["period"]}'].value,'execution time')>model.timestamp(closed.closed_at,'closed_at'):
            raise ValueError('Execution is after closure')
    states={value:key for key,value in locale['statuses'].items()}
    for record in data.rows:
        fields=inputs[record.identity]
        actual,status=[model._read_text(tests[fields[key]],record.identity+' '+key,optional=key!='status') for key in ('actual','status')]
        if 'note' in fields:
            note = model._read_text(tests[fields['note']], record.identity+' evidence note', optional=True)
            if note:
                model.public_text(note, record.identity+' evidence note')
        if model.markdown_leak(actual):
            raise ValueError('Actual result must use spreadsheet text such as [identifier], not Markdown syntax: '+record.identity)
        if status not in states:
            raise ValueError('Invalid pasted status: '+record.identity)
        token=states[status]
        if token == 'PASS':
            missing = [cp for cp in fields['checkpoints'] if not re.search(r'(?m)^'+re.escape(cp)+r':\s*\S',actual)]
            if missing:
                gaps.append(record.identity+': missing checkpoint observations: '+', '.join(missing))
        for key,value in (('actual',actual),):
            if value.strip():
                model.public_text(value,record.identity+' '+key)
            if tests[fields[key]].hyperlink and tests[fields[key]].hyperlink.target:
                model.shared_url(tests[fields[key]].hyperlink.target,record.identity+' '+key)
            height=tests.row_dimensions[tests[fields[key]].row].height or 15
            if height<(value.count('\n')+1)*11:
                gaps.append(record.identity+': input row too short for explicit lines')
            elif model.display_lines(value,40)*17+10>height:
                layout_notes.append(record.identity+': inspect input wrapping in native engine')
        valid=token in ('PASS','FAIL') and record.eligible and bool(actual.strip())
        if token in ('PASS','FAIL') and not valid:
            gaps.append(record.identity+': confirmed/ready basis and actual result required')
        if token not in ('PASS','NOT RUN') and not actual.strip():
            gaps.append(record.identity+': actual result must include reason and next action')
        if token=='NOT RUN':
            gaps.append(record.identity+': not executed')
        observations.append((record,token,valid))
    for case in data.cases:
        if case['screen_relative_path']=='unknown':
            gaps.append(case['id']+': screen relative URL remains unverified')
    image_bindings=[]
    allowed_images={fields['picture']:(identity,fields) for identity,fields in inputs.items() if fields['picture'] is not None}
    allowed_images = {row:(identity,cp) for identity,fields in inputs.items()
        for cp in evidence_bindings(fields).values() for row in cp['picture_rows']}
    import xml.etree.ElementTree as ET
    if ET.tostring(tests.data_validations.to_tree()) != ET.tostring(pristine.worksheets[1].data_validations.to_tree()):
        raise ValueError('Changed status validation')
    occupied = []
    for sheet in book:
        pane = sheet.sheet_view.pane
        allowed_panes = {'topLeft'}
        if pane and pane.ySplit:
            allowed_panes.add('bottomLeft')
        if pane and pane.xSplit:
            allowed_panes.add('topRight')
            if pane.ySplit:
                allowed_panes.add('bottomRight')
        selections = [selection.pane or 'topLeft' for selection in sheet.sheet_view.selection]
        if len(set(selections)) != len(selections) or set(selections)-allowed_panes:
            raise ValueError('Invalid native pane selections')
        technical_rows = {r for card in cards for r in card.get('technical_rows',[])} if sheet is tests else set()
        evidence_rows = {r for fields in inputs.values() for cp in fields.get('checkpoints',{}).values()
            for r in cp['picture_rows']+([cp['label_row']] if 'label_row' in cp else [])} if sheet is tests else set()
        if sheet is tests:
            evidence_rows |= {r for fields in inputs.values() if 'picture_rows' in fields
                for r in fields['picture_rows']+[fields['label_row'], tests[fields['note']].row]}
        allowed_hidden = technical_rows | evidence_rows
        if sheet is tests:
            allowed_hidden |= reader_blank_rows(data,cards)
        if sheet is summary:
            if sheet.auto_filter.ref != pristine.worksheets[0].auto_filter.ref:
                raise ValueError('Changed customer index filter range')
            allowed_hidden = set(range(model.CASE_START_ROW,model.CASE_START_ROW+len(cards)))
            allowed_hidden |= {row for row in (2,14,28) if all(pristine.worksheets[0].cell(row,column).value in (None,'') for column in range(1,4))}
        if sheet.sheet_state!='visible' or any(d.hidden and r not in allowed_hidden for r,d in sheet.row_dimensions.items()) or any(d.hidden for d in sheet.column_dimensions.values()):
            raise ValueError('Hidden report content unsupported')
        if sheet is tests:
            headers = {fields['evidence_row'] for fields in inputs.values()}
            if any(sheet.row_dimensions[row].hidden for row in headers):
                raise ValueError('Evidence heading must remain visible')
            for row in technical_rows:
                if not sheet.row_dimensions[row].hidden or sheet.row_dimensions[row].outlineLevel:
                    raise ValueError('Internal metrics must remain hidden and outside evidence groups')
            populated_rows = set()
            for image in sheet._images:
                anchor = image.anchor
                first = anchor._from.row+1
                if first not in allowed_images or not hasattr(anchor,'to'):
                    raise ValueError('Evidence image must use its reserved TC/variant slot')
                fields = allowed_images[first][1]
                last = anchor.to.row + (1 if anchor.to.rowOff else 0)
                if last > fields['picture_rows'][-1] or first-1 not in fields['picture_rows']:
                    raise ValueError('Image endpoint exceeds customer evidence area')
                populated_rows.update(range(first-1,last+1))
            for row in evidence_rows - headers:
                expected_level = 1 if row in populated_rows else 0
                if sheet.row_dimensions[row].outlineLevel != expected_level:
                    raise ValueError('Only populated evidence rows may form the one-level group')
                if row not in populated_rows and (not sheet.row_dimensions[row].hidden or sheet.cell(row,1).value not in (None,'')):
                    raise ValueError('Unused evidence rows must remain empty and fully hidden')
        for image in sheet._images:
            anchor=image.anchor._from
            if sheet.title!=tests.title or anchor.col!=0 or anchor.row+1 not in allowed_images:
                raise ValueError('Evidence image must use its reserved TC/variant slot')
            identity,fields=allowed_images[anchor.row+1]
            case_id,variant=identity.split(' / ')
            digest=hashlib.sha256(image._data()).hexdigest()
            checkpoint_id = ''
            from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor
            if not (isinstance(image.anchor,TwoCellAnchor) and image.anchor.editAs=='twoCell'):
                raise ValueError('Customer evidence requires resize-with-cell anchors')
            checkpoint_id=fields['id']
            expected_name='BLEND|'+case_id+'|'+variant+'|'+checkpoint_id+'|'+digest
            if not image.anchor.pic or image.anchor.pic.nvPicPr.cNvPr.name != expected_name:
                raise ValueError('Evidence checkpoint identity/digest binding mismatch')
            start=fields['picture_rows'][0]
            end=fields['picture_rows'][-1]+1
            row_top=lambda row: sum((tests.row_dimensions[r].height or 15)*12700 for r in range(start,row))
            top=row_top(anchor.row+1)+anchor.rowOff
            width,height=image_size(tests,image)
            bottom=top+round(height*9525)
            if isinstance(image.anchor,TwoCellAnchor) and (image.anchor.to.row> end-1 or image.anchor.to.col>4 or image.anchor.to.colOff<0 or image.anchor.to.rowOff<0):
                raise ValueError('Image endpoint exceeds customer evidence area')
            if anchor.colOff<0 or anchor.rowOff<0 or top<0 or width<=0 or height<=0 or bottom>row_top(end)+1 or anchor.colOff+round(width*9525)>evidence_width(tests)*9525+1:
                raise ValueError('Evidence image exceeds reserved checkpoint area')
            title_row = anchor.row
            caption = tests.cell(title_row,1).value
            if title_row not in fields['picture_rows'] or not model.descriptive_image_title(caption) or caption != image.anchor.pic.nvPicPr.cNvPr.descr:
                raise ValueError('Each evidence image requires its matching title immediately above')
            for old_id,old_top,old_bottom in occupied:
                if old_id==(identity,checkpoint_id) and max(top,old_top)<min(bottom,old_bottom):
                    raise ValueError('Overlapping evidence images')
            occupied.append(((identity,checkpoint_id),top,bottom))
            image_bindings.append((case_id,variant,checkpoint_id,digest))
        original=pristine[sheet.title]
        if any((d.height or 15)>409 for d in sheet.row_dimensions.values()):
            raise ValueError('Row height exceeds Excel display limit')
        if set(str(r) for r in sheet.merged_cells.ranges)!=set(str(r) for r in original.merged_cells.ranges):
            raise ValueError('Changed block merges')
        for row in sheet.iter_rows(max_row=max(sheet.max_row,original.max_row),max_col=max(sheet.max_column,original.max_column)):
            for cell in row:
                if (sheet.title,cell.coordinate) in editable:
                    continue
                old=original[cell.coordinate]
                equal=(_formula_reference_key(cell.value,locale['sheets'])==_formula_reference_key(old.value,locale['sheets']) if cell.data_type==old.data_type=='f' else str(cell.value)==str(old.value))
                blank = cell.value in (None,'') and old.value in (None,'') and cell.data_type!='f'
                if not blank and (not equal or cell.data_type!=old.data_type):
                    raise ValueError('Changed source/formula: '+sheet.title+'!'+cell.coordinate)
                if old.hyperlink and (not cell.hyperlink or cell.hyperlink.location!=old.hyperlink.location):
                    raise ValueError('Changed navigation: '+cell.coordinate)
                if cell.comment:
                    model.public_text(cell.comment.text,'comment')
                if cell.value is not None:
                    height=sheet.row_dimensions[cell.row].height or 15
                    if height<(str(cell.value).count('\n')+1)*(cell.font.sz or 11) and not (sheet is tests and cell.row in technical_rows):
                        raise ValueError('Clipped explicit lines: '+cell.coordinate)
    if phase=='complete':
        from check_report import ScreenshotReview
        reviews=[model._records(value,ScreenshotReview) for value in screenshots]
        if Counter(image_bindings)!=Counter((r.case_id,r.variant,r.checkpoint_id,r.sha256) for r in reviews):
            raise ValueError('Screenshot review identity/digest mismatch')
        for record,token,_ in observations:
            if token == 'PASS':
                for cp in inputs[record.identity]['checkpoints'].values():
                    if cp['artifact']=='screenshot' and not any(binding[:3]==(record.case_id,record.variant,cp['id']) for binding in image_bindings):
                        gaps.append(record.identity+': missing screenshot evidence for '+cp['id'])
    allowed={value.removeprefix('=') for sheet in pristine for row in sheet for cell in row if cell.data_type=='f' for value in (cell.value,)}
    urls=_package(raw,data,phase,{'closure_confirmation':closure_confirmation,'evidence_access':evidence_access,'screenshots':screenshots},gaps,allowed_formulas=allowed,
        image_digests=[binding[3] for binding in image_bindings])
    model._unchanged(captures)
    counts=Counter(token for _,token,_ in observations)
    passed=sum(token=='PASS' and valid for _,token,valid in observations)
    evaluated=sum(valid for _,_,valid in observations)
    case_states={}
    for card in cards:
        members=[(token,valid) for record,token,valid in observations if record.case_id==card['id']]
        case_states[card['id']]=('FAIL' if any(token=='FAIL' for token,valid in members) else 'PASS' if all(token=='PASS' for token,valid in members) else 'SKIPPED' if all(token=='SKIPPED' for token,_ in members) else 'BLOCKED' if any(token=='BLOCKED' for token,_ in members) else 'NOT RUN' if all(token=='NOT RUN' for token,_ in members) else 'INCOMPLETE')
    raw_passed, raw_evaluated = counts['PASS'], counts['PASS']+counts['FAIL']
    return {'family':model.FAMILY,'version':data.report_version,'language':language,'cases':len(cards),'variants':len(data.rows),'states':dict(counts),'case_states':case_states,'passed':raw_passed,'evaluated':raw_evaluated,'pass_rate':raw_passed/raw_evaluated if raw_evaluated else None,'quality_qualified_passed':passed,'quality_qualified_evaluated':evaluated,'complete':phase=='complete' and not gaps,'read_only':True,'gaps':gaps,'layout_notes':layout_notes,'links':len(urls)}
