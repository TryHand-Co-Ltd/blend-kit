"""Focused same-file editable-report controls, with synthetic input only."""
from pathlib import Path
import importlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET


def load_domain(root):
    scripts = root / 'skills/blend-generate-test-spec/scripts'
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    return importlib.import_module('report_model')


def fixture(root, work, language='vi', *, simple=False):
    model = load_domain(root)
    source = work / "design"
    shutil.copytree(root / "tests/fixtures/test-spec/inputs/valid", source)
    if simple:
        # Keep source template grammar and exact provenance, with one short case.
        for lang in ("ja", "vi"):
            path = source / f"test-cases.{lang}.md"
            text = path.read_text(encoding="utf-8")
            start = text.index("#### TC-SYN-01")
            end = text.index("#### TC-SYN-02")
            text = text[:start] + text[end:text.index("#### TC-SYN-03")]
            replacements = {
                "Settings at synthetic editor": "A", "POST /eligibility/preview verified fixture route": "Preview",
                "Readback preview and non-target record": "Preview", "Visitor without owner permission": "Visitor",
                "Send preview request as visitor; readback as owner": "Preview", "TD-01": "local: score=59",
            }
            for old, new in replacements.items():
                text = text.replace(old, new)
            path.write_text(text, encoding="utf-8")
            scope = source / f"scope-and-approach.{lang}.md"
            lines = scope.read_text(encoding="utf-8").splitlines()
            lines = [line for line in lines if not line.startswith(("| SPEC:S1 |", "| SPEC:S3 |", "| SPEC:S4 |", "| G-01 |", "| G-02 |"))]
            scope.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report = work / 'report.xlsx'
    model.working.export(source, report, language=language)
    delivery = {'closure_confirmation': {'closed_by': 'Synthetic QA', 'closed_at': '2026-10-04T10:00:00+00:00',
        'source': 'Synthetic closure control', 'audience': 'Synthetic recipient'},
        'evidence_access': [{'url': 'https://evidence.example.com/synthetic/run-01', 'audience': 'Synthetic recipient',
        'verified_by': 'Synthetic QA', 'verified_at': '2026-10-04T10:10:00+00:00',
        'method': 'human-attestation', 'source': 'Synthetic access control'}], 'screenshots': []}
    return model, source, report, delivery


def complete_inputs(book, model, language):
    locale = model.REPORT_LAYOUTS[language]
    summary, results = [book[name] for name in locale['sheets'][:2]]
    values = {'run_id': 'SYN-01', 'build': 'Synthetic build', 'environment': 'Synthetic isolated environment',
              'tester': 'Synthetic QA', 'period': '2026-10-04T09:00:00+00:00'}
    for key, value in values.items():
        summary.cell(model.SUMMARY_FIELDS[key], 2, value)
    for row in range(locale['start_row'], results.max_row + 1):
        if results.cell(row, 1).value:
            results.cell(row, 5, 'Synthetic observed result')
            results.cell(row, 6, locale['statuses']['PASS'])
            results.cell(row, 7, 'https://evidence.example.com/synthetic/run-01')


def save_synthetic(book, path):
    # openpyxl drops filterPrivacy; emulate the native writer retaining this setting.
    from render_report import serialize_report
    Path(path).write_bytes(serialize_report(book))


def run(root, scope='all'):
    model = load_domain(root)
    if model.VERSION == '2.0.0':
        spec = importlib.util.spec_from_file_location('block_controls',Path(__file__).with_name('block_checks.py'))
        controls_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(controls_module)
        return controls_module.run(root)
    from openpyxl import load_workbook
    model = load_domain(root)
    from check_report import check_report
    controls = []
    def refused(call):
        try:
            call()
        except (ValueError, TypeError, OSError):
            return
        raise AssertionError('Unsafe input accepted')
    with tempfile.TemporaryDirectory(prefix='blend-report-checks-') as directory:
        work = Path(directory)
        for language in ('ja', 'vi'):
            folder = work / language
            folder.mkdir()
            model, source, report, delivery = fixture(root, folder, language, simple=True)
            locale = model.REPORT_LAYOUTS[language]
            first = report.read_bytes()
            result = check_report(report, source, language)
            assert result['states'] == {'NOT RUN': 1} and result['passed'] == 0 and result['pass_rate'] is None
            assert report.read_bytes() == first
            result = check_report(report, source, language, 'complete', **delivery)
            assert not result['complete'] and result['gaps'] and report.read_bytes() == first
            cli_env = {**os.environ, 'PYTHONIOENCODING': 'cp1252', 'PYTHONUTF8': '0'}
            cli_command = [sys.executable, str(root / 'skills/blend-generate-test-spec/scripts/check_report.py'),
                           '--report', str(report), '--source-dir', str(source), '--language', language]
            progress = subprocess.run([*cli_command, '--phase', 'in-progress'], capture_output=True, env=cli_env, timeout=30)
            assert progress.returncode == 0, progress.stderr.decode('utf-8')
            progress_result = json.loads(progress.stdout.decode('utf-8'))
            assert any(locale['sheets'][0] in gap for gap in progress_result['gaps'])
            assert not progress.stderr and report.read_bytes() == first
            book = load_workbook(report)
            complete_inputs(book, model, language)
            save_synthetic(book, report)
            complete = report.read_bytes()
            result = check_report(report, source, language, 'complete', **delivery)
            assert result['complete'] and result['passed'] == 1 and result['pass_rate'] == 1
            assert report.read_bytes() == complete and len(list(folder.glob('*.xlsx'))) == 1
            controls.append(language + '-same-file-not-started-to-complete-read-only')
            # Literal punctuation belongs to the URL, including its access receipt.
            for url, prefix in [
                ('https://evidence.example.com/view/(1)', 'https://evidence.example.com/view/(1'),
                ('https://evidence.example.com/view/[1]', 'https://evidence.example.com/view/[1'),
                ('https://evidence.example.com/view?a=(1)&case=[2]', 'https://evidence.example.com/view?a=(1'),
                ('https://evidence.example.com/view/%25281%2529?case=%255B2%255D',
                 'https://evidence.example.com/view/%281%29?case=%5B2%5D'),
            ]:
                changed = load_workbook(io.BytesIO(complete))
                results = changed[locale['sheets'][1]]
                results['G5'] = url
                save_synthetic(changed, report)
                before = report.read_bytes()
                exact_delivery = {**delivery, 'evidence_access': [{**delivery['evidence_access'][0], 'url': url}]}
                exact = check_report(report, source, language, 'complete', **exact_delivery)
                assert exact['complete'] and exact['links'] == 1 and exact['passed'] == 1
                short_delivery = {**delivery, 'evidence_access': [{**delivery['evidence_access'][0], 'url': prefix}]}
                short = check_report(report, source, language, 'complete', **short_delivery)
                assert not short['complete'] and any('Access not verified' in gap for gap in short['gaps'])
                assert report.read_bytes() == before
                assert load_workbook(report)[locale['sheets'][1]]['G5'].value == url
                for token in ('FAIL', 'BLOCKED', 'SKIPPED', 'NOT RUN'):
                    results['F5'] = locale['statuses'][token]
                    save_synthetic(changed, report)
                    before = report.read_bytes()
                    outcome = check_report(report, source, language, 'complete', **exact_delivery)
                    assert not outcome['complete'] and any('reason and next action required' in gap for gap in outcome['gaps'])
                    assert report.read_bytes() == before
                reason = 'Lý do mẫu; kiểm tra lại sau khi sửa' if language == 'vi' else '確認結果に差異あり。修正後に再確認する。'
                results['F5'] = locale['statuses']['FAIL']
                results['G5'] = url + '\n' + reason
                results.row_dimensions[5].height = 180
                save_synthetic(changed, report)
                before = report.read_bytes()
                assert check_report(report, source, language, 'complete', **exact_delivery)['complete']
                assert report.read_bytes() == before
                assert load_workbook(report)[locale['sheets'][1]]['G5'].value == url + '\n' + reason
            controls.append(language + '-complete-url-punctuation-exact-receipts-literal-bytes-and-real-reasons')
            for url in (
                'https://evidence.example.com/view?a=(1)&token=fixture-value',
                'HTTPS://evidence.example.com/view?a=(1)&token=fixture-value',
                'https://evidence.example.com/view?a=[1]&token=fixture-value',
                'https://evidence.example.com/view?a=(1)&%2574oken=fixture-value',
                'https://evidence.example.com/view?a=[1]&%2574oken=fixture-value',
                'https://evidence.example.com/view?a=(1)&path=%252Ftmp%252Ffixture-value',
                'https://evidence.example.com/view?a=[1]&path=%252Ftmp%252Ffixture-value',
            ):
                refused(lambda: model.public_text('Evidence: ' + url, 'synthetic prose'))
                changed = load_workbook(io.BytesIO(complete))
                changed[locale['sheets'][1]]['G5'] = url
                save_synthetic(changed, report)
                before = report.read_bytes()
                refused(lambda: check_report(report, source, language, 'complete', **delivery))
                assert report.read_bytes() == before
            controls.append(language + '-credentials-and-private-locators-after-literal-punctuation-refused')
            report.write_bytes(complete)
            # Matching a Unicode evidence URL proves stdin is decoded once as UTF-8.
            localized_url = 'https://evidence.example.com/証拠/kết-quả'
            localized_delivery = {'closure_confirmation': {**delivery['closure_confirmation'],
                'closed_by': 'Người kiểm thử 山田', 'source': 'Xác nhận 終了', 'audience': 'Người nhận 受領者'},
                'evidence_access': [{**delivery['evidence_access'][0], 'url': localized_url,
                    'audience': 'Người nhận 受領者', 'verified_by': 'Người kiểm thử 山田', 'source': 'Quyền truy cập 確認'}],
                'screenshots': []}
            book[locale['sheets'][1]]['G5'] = localized_url
            save_synthetic(book, report)
            localized_bytes = report.read_bytes()
            checked = subprocess.run([*cli_command, '--phase', 'complete'],
                input=json.dumps(localized_delivery, ensure_ascii=False).encode('utf-8'),
                capture_output=True, env=cli_env, timeout=30)
            assert checked.returncode == 0, checked.stderr.decode('utf-8') + checked.stdout.decode('utf-8')
            assert json.loads(checked.stdout.decode('utf-8'))['complete'] and not checked.stderr
            assert report.read_bytes() == localized_bytes
            report.write_bytes(first)
            incomplete = subprocess.run([*cli_command, '--phase', 'complete'],
                input=json.dumps(localized_delivery, ensure_ascii=False).encode('utf-8'),
                capture_output=True, env=cli_env, timeout=30)
            assert incomplete.returncode == 1 and not json.loads(incomplete.stdout.decode('utf-8'))['complete']
            assert not incomplete.stderr and report.read_bytes() == first
            report.write_bytes(complete)
            controls.append(language + '-cp1252-cli-utf8-localized-stdin-gaps-and-outcomes')
            if language == 'ja':
                # Native Excel removes optional sheet quotes outside string literals.
                normalized = load_workbook(io.BytesIO(complete))
                for row in normalized[locale['sheets'][0]]:
                    for cell in row:
                        if cell.data_type == 'f':
                            cell.value = cell.value.replace("'テスト'!", 'テスト!')
                save_synthetic(normalized, report)
                normalized_bytes = report.read_bytes()
                assert check_report(report, source, language, 'complete', **delivery)['complete']
                assert report.read_bytes() == normalized_bytes
                for cell, old, new in [('B17', 'COUNTA', 'COUNT'), ('B17', '$A$5', '$A$6'),
                                       ('B30', 'TC-SYN-02 / base', 'TC-SYN-99 / base')]:
                    tampered = load_workbook(io.BytesIO(normalized_bytes))
                    value = tampered[locale['sheets'][0]][cell].value
                    assert old in value
                    tampered[locale['sheets'][0]][cell] = value.replace(old, new)
                    save_synthetic(tampered, report)
                    before = report.read_bytes()
                    refused(lambda: check_report(report, source, language, 'complete', **delivery))
                    assert report.read_bytes() == before
                from check_report import _formula_reference_key
                literal = '=IF(1=1,"\'テスト\'!A5","テスト!A5")'
                assert _formula_reference_key(literal, locale['sheets']) == literal
                assert _formula_reference_key(literal.replace("'テスト'!", 'テスト!'), locale['sheets']) != literal
                report.write_bytes(complete)
                controls.append('ja-native-sheet-quote-equivalence-strict-function-range-id-and-string-guards')
            for name, cell, value, hard in [
                ('invalid-pasted-status', 'F5', 'PASSED', True),
                ('missing-actual', 'E5', None, False),
                ('whitespace-actual', 'E5', '   ', False),
                ('unicode-whitespace-actual', 'E5', '\t\n\u00a0\u3000', False),
                ('missing-evidence', 'G5', None, False),
                ('prose-only-evidence', 'G5', 'Chờ bổ sung bằng chứng', False),
                ('prose-before-evidence', 'G5', 'Evidence: https://evidence.example.com/synthetic/run-01', False),
                ('unrun', 'F5', locale['statuses']['NOT RUN'], False),
                ('fail-no-reason', 'F5', locale['statuses']['FAIL'], False),
                ('blocked-no-reason', 'F5', locale['statuses']['BLOCKED'], False),
                ('skipped-no-reason', 'F5', locale['statuses']['SKIPPED'], False),
                ('altered-expected', 'D5', 'Different expected', True),
                ('missing-id', 'A5', None, True),
                ('formula-actual', 'E5', '=1+1', True),
                ('private-actual', 'E5', 'D:/private/run.txt', True),
                ('encoded-url', 'G5', 'https://evidence.example.com/?%2574oken=private', True),
                ('encoded-path', 'G5', 'https://evidence.example.com/?path=%252Ftmp%252Fresult', True),
            ]:
                changed = load_workbook(io.BytesIO(complete))
                changed[locale['sheets'][1]][cell] = value
                save_synthetic(changed, report)
                before = report.read_bytes()
                if hard:
                    refused(lambda: check_report(report, source, language, 'complete', **delivery))
                else:
                    outcome = check_report(report, source, language, 'complete', **delivery)
                    assert not outcome['complete']
                    if name in ('missing-actual', 'whitespace-actual', 'unicode-whitespace-actual', 'missing-evidence', 'prose-only-evidence', 'prose-before-evidence'):
                        assert outcome['evaluated'] == outcome['passed'] == 0 and outcome['pass_rate'] is None
                assert before == report.read_bytes()
                controls.append(language + '-' + name)
            report.write_bytes(complete)
            assert not check_report(report, source, language, 'complete', **{**delivery, 'evidence_access': []})['complete']
            changed = load_workbook(report)
            changed.worksheets[0]['B18'] = 999
            save_synthetic(changed, report)
            refused(lambda: check_report(report, source, language))
            report.write_bytes(complete)
            changed = load_workbook(report)
            changed.worksheets[0].delete_rows(30)
            save_synthetic(changed, report)
            refused(lambda: check_report(report, source, language))
            report.write_bytes(complete)
            changed = load_workbook(report)
            changed[locale['sheets'][1]].data_validations.dataValidation = []
            save_synthetic(changed, report)
            refused(lambda: check_report(report, source, language))
            report.write_bytes(complete)
            changed = load_workbook(report)
            rules = next(iter(changed[locale['sheets'][1]].conditional_formatting._cf_rules.values()))
            rules[0].formula = ['WEBSERVICE("https://evidence.example.com/exfil")']
            save_synthetic(changed, report)
            refused(lambda: check_report(report, source, language))
            report.write_bytes(complete)
            changed = load_workbook(report)
            changed.properties.description = 'D:/private/secret.txt'
            save_synthetic(changed, report)
            refused(lambda: check_report(report, source, language))
            report.write_bytes(complete)
            changed = load_workbook(report)
            changed.custom_doc_props['TemplateFamily'].value = 'test-case-report'
            save_synthetic(changed, report)
            refused(lambda: check_report(report, source, language))
            controls.append(language + '-formula-private-metadata-legacy-refusal')
            # Native absPath and arbitrary attributes are inspected in original OOXML.
            for tag, attribute, value in [
                ('{http://schemas.microsoft.com/office/spreadsheetml/2010/11/ac}absPath', 'url', 'D:/synthetic-private-directory/'),
                ('{urn:synthetic-extension}record', 'origin', '%2544%253A%252Fsynthetic-private-directory%252F'),
                ('{urn:synthetic-extension}record', 'link', 'https://evidence.example.com/?%2574oken=private'),
                ('{urn:synthetic-extension}record', 'link', 'https://evidence.example.com/view?a=(1)&token=fixture-value'),
                ('{urn:synthetic-extension}record', 'link', 'https://evidence.example.com/view?a=[1]&%2574oken=fixture-value'),
                ('{urn:synthetic-extension}record', 'note', '[dummy-input: D:/synthetic-private-directory/]'),
            ]:
                with zipfile.ZipFile(io.BytesIO(complete)) as archive:
                    entries = {name: archive.read(name) for name in archive.namelist()}
                metadata = ET.fromstring(entries['xl/workbook.xml'])
                ET.SubElement(metadata, tag, {attribute: value})
                entries['xl/workbook.xml'] = ET.tostring(metadata, encoding='utf-8', xml_declaration=True)
                with zipfile.ZipFile(report, 'w', zipfile.ZIP_DEFLATED) as archive:
                    for name, content in entries.items():
                        archive.writestr(name, content)
                before = report.read_bytes()
                try:
                    check_report(report, source, language, 'complete', **delivery)
                except ValueError as error:
                    assert 'xl/workbook.xml' in str(error)
                    assert value not in str(error) and 'synthetic-private-directory' not in str(error)
                else:
                    raise AssertionError('Private XML attribute accepted')
                assert report.read_bytes() == before
            report.write_bytes(complete)
            controls.append(language + '-native-abspath-and-arbitrary-encoded-xml-attribute-privacy')
            # The preventive flag is required, but never substitutes for the scan above.
            with zipfile.ZipFile(io.BytesIO(complete)) as archive:
                entries = {name: archive.read(name) for name in archive.namelist()}
            metadata = ET.fromstring(entries['xl/workbook.xml'])
            privacy = metadata.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}workbookPr')
            assert privacy is not None and privacy.get('filterPrivacy') == '1'
            privacy.set('filterPrivacy', '0')
            entries['xl/workbook.xml'] = ET.tostring(metadata, encoding='utf-8', xml_declaration=True)
            with zipfile.ZipFile(report, 'w', zipfile.ZIP_DEFLATED) as archive:
                for name, content in entries.items():
                    archive.writestr(name, content)
            before = report.read_bytes()
            refused(lambda: check_report(report, source, language))
            assert report.read_bytes() == before
            report.write_bytes(complete)
            # Literal source entities decode once; actual Excel text never decodes.
            literal = '  literal &lt;b&gt; <br>\t  '
            escaped = literal.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&#32;').replace('\t', '&#9;')
            for lang in ('ja', 'vi'):
                path = source / f'test-cases.{lang}.md'
                text = path.read_text(encoding='utf-8').replace('Request denied; before and after target identical', escaped)
                path.write_text(text, encoding='utf-8')
            new_report = folder / 'literal.xlsx'
            model.working.export(source, new_report, language=language)
            saved = load_workbook(new_report)
            assert saved[locale['sheets'][1]]['D5'].value.startswith(literal)
            complete_inputs(saved, model, language)
            saved[locale['sheets'][1]]['E5'] = literal
            save_synthetic(saved, new_report)
            check_report(new_report, source, language, 'complete', **delivery)
            assert load_workbook(new_report)[locale['sheets'][1]]['E5'].value == literal
            controls.append(language + '-literal-entities-whitespace-once')
            # Add reviewed evidence to this same two-sheet workbook, without regeneration.
            from PIL import Image as PILImage
            from openpyxl.drawing.image import Image
            image_path = folder / 'synthetic.png'
            PILImage.new('RGB', (16, 16), 'white').save(image_path)
            saved = load_workbook(new_report)
            details = saved.create_sheet(locale['sheets'][2])
            for col, value in enumerate(locale['detail_headers'], 1):
                details.cell(4, col, value)
            identity = saved[locale['sheets'][1]]['A5'].value
            caption = 'Synthetic evidence image'
            for col, value in enumerate((identity, locale['evidence_link'], caption), 1):
                details.cell(5, col, value)
            details.add_image(Image(image_path), 'C6')
            save_synthetic(saved, new_report)
            with zipfile.ZipFile(new_report) as archive:
                entries = {name: archive.read(name) for name in archive.namelist()}
            import hashlib
            media = next(value for name, value in entries.items() if name.startswith('xl/media/'))
            for name in entries:
                if name.startswith('xl/drawings/drawing') and name.endswith('.xml'):
                    drawing = ET.fromstring(entries[name])
                    for node in drawing.iter():
                        if node.tag.rsplit('}', 1)[-1] == 'cNvPr':
                            node.set('descr', caption)
                    entries[name] = ET.tostring(drawing, encoding='utf-8', xml_declaration=True)
            with zipfile.ZipFile(new_report, 'w', zipfile.ZIP_DEFLATED) as archive:
                for name, raw in entries.items():
                    archive.writestr(name, raw)
            case_id, variant = identity.split(' / ')
            shot = {'case_id': case_id, 'variant': variant, 'sha256': hashlib.sha256(media).hexdigest(),
                    'caption': caption, 'reviewed_by': 'Synthetic QA', 'reviewed_at': '2026-10-04T10:15:00+00:00',
                    'source': 'Synthetic image review'}
            frozen_image = new_report.read_bytes()
            assert check_report(new_report, source, language, 'complete', **{**delivery, 'screenshots': [shot]})['complete']
            refused(lambda: check_report(new_report, source, language, 'complete', **delivery))
            assert new_report.read_bytes() == frozen_image
            controls.append(language + '-same-file-reviewed-image-binding-and-no-write')
        complex_dir = work / 'complex'
        complex_dir.mkdir()
        model, source, report, delivery = fixture(root, complex_dir)
        locale = model.REPORT_LAYOUTS['vi']
        book = load_workbook(report)
        projected, _ = model.prepare_report(source, 'vi')
        assert 'Tính theo testcase' in book[locale['sheets'][0]]['B14'].value
        detail_sheet = book[locale['sheets'][2]]
        linked = 0
        for row, record in enumerate(projected.rows, locale['start_row']):
            for col, full in ((2, record.screen_function), (3, record.conditions), (4, record.expected)):
                cell = book[locale['sheets'][1]].cell(row, col)
                if cell.hyperlink:
                    assert cell.value != locale['detail_link'] and cell.value.endswith(locale['detail_link'])
                    first = int(cell.hyperlink.location.rsplit('!A', 1)[1])
                    chunks = []
                    for number in range(first, detail_sheet.max_row + 1):
                        if detail_sheet.cell(number, 1).value != model.detail_backlink_formula(record.identity, projected) or detail_sheet.cell(number, 2).value != locale['headers'][col - 1]:
                            break
                        chunks.append(detail_sheet.cell(number, 3).value)
                    assert ''.join(chunks) == full
                    linked += 1
        assert linked
        controls.append('source-excerpts-with-full-linked-content-and-independent-preparation')
        complete_inputs(book, model, 'vi')
        results = book[locale['sheets'][1]]
        for row, token in enumerate(('PASS', 'FAIL', 'SKIPPED', 'PASS', 'BLOCKED'), 5):
            results.cell(row, 6, locale['statuses'][token])
            if token != 'PASS':
                results.cell(row, 7, 'https://evidence.example.com/synthetic/run-01\nSynthetic reason; recheck after correction')
            results.row_dimensions[row].height = max(results.row_dimensions[row].height or 15,
                model.display_lines(results.cell(row, 7).value, 21) * 17 + 10)
        save_synthetic(book, report)
        outcome = check_report(report, source, 'vi', 'complete', **delivery)
        assert outcome['states'] == {'PASS': 2, 'FAIL': 1, 'SKIPPED': 1, 'BLOCKED': 1}
        assert outcome['evaluated'] == 3 and outcome['passed'] == 2 and outcome['completion_rate'] == 0.6
        # Closed mixed outcome is valid, but never falsely counted as full PASS.
        assert outcome['complete']
        # Exact native Excel AutoFit heights observed in the inspected VI PDF.
        # Wrapping estimates are advisory; they must not reject visibly fitted rows.
        for row in range(5, 10):
            results.row_dimensions[row].height = 85.5 if results.cell(row, 1).value.startswith('TC-SYN-01') else 57
        save_synthetic(book, report)
        native_sized = report.read_bytes()
        outcome = check_report(report, source, 'vi', 'complete', **delivery)
        assert outcome['complete'] and outcome['layout_notes'] and not outcome['gaps']
        assert report.read_bytes() == native_sized
        clipped = load_workbook(report)
        clipped[locale['sheets'][1]].row_dimensions[5].height = 5
        save_synthetic(clipped, report)
        clipped_bytes = report.read_bytes()
        clipped_result = check_report(report, source, 'vi', 'complete', **delivery)
        assert not clipped_result['complete'] and any('too short' in gap for gap in clipped_result['gaps'])
        assert report.read_bytes() == clipped_bytes
        clipped[locale['sheets'][1]].row_dimensions[5].hidden = True
        save_synthetic(clipped, report)
        refused(lambda: check_report(report, source, 'vi'))
        report.write_bytes(native_sized)
        controls.append('native-autofit-heights-advisory-with-clipped-and-hidden-row-negatives')
        frozen = report.read_bytes()
        # Whole-row sorting preserves source/actual associations and dynamic return links.
        from copy import copy
        original_rows = [[(results.cell(row, col).value, results.cell(row, col).data_type,
                           copy(results.cell(row, col).hyperlink)) for col in range(1, 8)] for row in range(5, 10)]
        heights = [results.row_dimensions[row].height for row in range(5, 10)]
        for row, cells, height in zip(range(5, 10), reversed(original_rows), reversed(heights)):
            for col, (value, cell_type, link) in enumerate(cells, 1):
                results.cell(row, col).value = value
                results.cell(row, col).data_type = cell_type
                results.cell(row, col).hyperlink = link
            results.row_dimensions[row].height = height
        save_synthetic(book, report)
        assert check_report(report, source, 'vi', 'complete', **delivery)['complete']
        report.write_bytes(frozen)
        book = load_workbook(report)
        results = book[locale['sheets'][1]]
        results.cell(9, 6, locale['statuses']['PASS'])
        save_synthetic(book, report)
        outcome = check_report(report, source, 'vi', 'complete', **delivery)
        assert not outcome['complete'] and outcome['passed'] == 2
        report.write_bytes(frozen)
        duplicate = load_workbook(report)
        duplicate[locale['sheets'][1]]['A6'] = duplicate[locale['sheets'][1]]['A5'].value
        save_synthetic(duplicate, report)
        refused(lambda: check_report(report, source))
        report.write_bytes(frozen)
        collision = load_workbook(report)
        collision[locale['sheets'][1]]['A6'] = collision[locale['sheets'][1]]['A5'].value.upper()
        save_synthetic(collision, report)
        before = report.read_bytes()
        refused(lambda: check_report(report, source))
        assert report.read_bytes() == before
        report.write_bytes(frozen)
        skipped = load_workbook(report)
        for row in range(5, 10):
            skipped[locale['sheets'][1]].cell(row, 6, locale['statuses']['SKIPPED'])
            skipped[locale['sheets'][1]].cell(row, 7, 'Outside this run; recheck in next run')
        save_synthetic(skipped, report)
        outcome = check_report(report, source, 'vi', 'complete', **delivery)
        assert set(outcome['case_results'].values()) == {'SKIPPED'} and outcome['evaluated'] == 0
        skipped[locale['sheets'][1]]['F5'] = locale['statuses']['PASS']
        skipped[locale['sheets'][1]]['G5'] = 'https://evidence.example.com/synthetic/run-01'
        save_synthetic(skipped, report)
        outcome = check_report(report, source, 'vi', 'complete', **delivery)
        assert outcome['case_results']['TC-SYN-01'] == 'INCOMPLETE' and outcome['passed'] == 1
        controls.append('casefold-tamper-all-skipped-and-mixed-case-aggregates')
        controls.append('mixed-variants-unresolved-expected-duplicate-inventory')
    return controls


if __name__ == '__main__':
    print('PASS:', len(run(Path(__file__).resolve().parents[3])), 'synthetic same-workbook controls')
