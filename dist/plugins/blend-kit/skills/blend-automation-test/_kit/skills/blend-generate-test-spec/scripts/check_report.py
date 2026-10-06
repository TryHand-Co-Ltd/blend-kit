"""Inspect the existing editable report without writing, repairing or certifying it."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import io
import json
import posixpath
from pathlib import Path
import re
import sys
from urllib.parse import unquote
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from report_model import (ClosureConfirmation, EvidenceAccess, _records,
    public_text, shared_url, url_spans, required, timestamp)


@dataclass(frozen=True)
class ScreenshotReview:
    case_id: str
    variant: str
    sha256: str
    caption: str
    reviewed_by: str
    reviewed_at: str
    source: str
    checkpoint_id: str = ''


def _formula_reference_key(value, sheet_names):
    """Excel may unquote simple sheet names; never normalize formula string literals."""
    if not isinstance(value, str):
        return value
    parts = re.split(r'("(?:[^"]|"")*")', value)
    for index in range(0, len(parts), 2):
        for name in sheet_names:
            # Only these exact names can legally lose quotes in Excel. Spaces,
            # apostrophes and punctuation keep their original strict spelling.
            if re.fullmatch(r'[^\W\d]\w*', name):
                parts[index] = re.sub(r"(?<![\w.'])" + re.escape(name) + r'!',
                                      lambda _: "'" + name + "'!", parts[index])
    return ''.join(parts)


def _xml_value(value, field):
    """Validate metadata literals, including repeated URL escaping, without echoing values."""
    if not value:
        return
    decoded = value
    for _ in range(5):
        # These are public XML schema identifiers, not evidence links. The strict
        # lexical form excludes query strings, encoded locators and credentials.
        if re.fullmatch(r'https?://(?:schemas\.openxmlformats\.org|schemas\.microsoft\.com|www\.w3\.org|purl\.oclc\.org|purl\.org)/[A-Za-z0-9._/-]+', decoded):
            from report_model import PRIVATE
            if not PRIVATE.search(decoded):
                return
        public_text(decoded, field)  # No dummy-input exception for XML attributes.
        next_decoded = unquote(decoded)
        if next_decoded == decoded:
            return
        decoded = next_decoded
    raise ValueError(f'Excessive metadata encoding cannot be validated: {field}')


def _xml_attributes(root, name, urls):
    for element in root.iter():
        tag = element.tag.rsplit('}', 1)[-1]
        for key, value in element.attrib.items():
            attribute = key.rsplit('}', 1)[-1]
            field = f'{name}:{tag}@{attribute}'
            # ContentType is a MIME identifier. Do not mistake the registered
            # application/vnd... prefix for an application source-directory path.
            if name == '[Content_Types].xml' and attribute == 'ContentType':
                if re.fullmatch(r'(?:application/(?:xml|vnd\.openxmlformats-(?:officedocument|package)\.[A-Za-z0-9.-]+(?:\+xml)?)|image/(?:png|jpeg))', value):
                    continue
                raise ValueError(f'Unsupported content type: {field}')
            _xml_value(value, field)
            if not re.fullmatch(r'https?://(?:schemas\.openxmlformats\.org|schemas\.microsoft\.com|www\.w3\.org|purl\.oclc\.org|purl\.org)/[A-Za-z0-9._/-]+', value):
                urls.update(match.group() for match in url_spans(value))


def _package(raw, data, phase, payload, gaps, *, allowed_formulas=None, image_digests=None):
    """Inspect saved relationships, metadata, text and image bytes, never strip them."""
    urls, media, captions = set(), {}, []
    from report_model import report_locale
    locale = report_locale(data)
    from block_report import layout
    cards, _ = layout(data)
    # Authorize only frozen source literals after the same reader transformation.
    # Actual cells and XML attributes retain their separate strict privacy checks.
    dummy_literals = {value for card in cards for _, text, _, right, _, label in card['rows']
        for value in (text, right, label) if isinstance(value, str) and '[dummy-input: ' in value}
    if allowed_formulas is None:
        from block_report import formulas
        allowed_formulas = {value.removeprefix('=') for value in formulas(data).values()}
    allowed_formulas.update('"' + label + '"' for label in locale['statuses'].values())
    allowed_formulas.add('"' + ','.join(locale['statuses'].values()) + '"')
    allowed_formulas = {_formula_reference_key(value, locale['sheets']) for value in allowed_formulas}
    with ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP entries")
        for name in names:
            if name.startswith(('xl/externalLinks/', 'xl/embeddings/', 'customXml/', 'xl/activeX/')) or name.endswith(('vbaProject.bin', '.vml')):
                raise ValueError(f"Unsupported workbook component: {name}")
            content = archive.read(name)
            if name.startswith('xl/media/'):
                from PIL import Image
                with Image.open(io.BytesIO(content)) as image:
                    if image.format not in ('PNG', 'JPEG') or getattr(image, 'n_frames', 1) != 1:
                        raise ValueError('Only static PNG/JPEG evidence is supported')
                    if image.getexif() or any(k not in ('dpi', 'jfif', 'jfif_version', 'jfif_unit', 'jfif_density') for k in image.info):
                        raise ValueError(f'Image metadata must be reviewed and removed in the same workbook: {name}')
                with Image.open(io.BytesIO(content)) as image:
                    image.verify()
                media[name] = hashlib.sha256(content).hexdigest()
            elif name.endswith(('.xml', '.rels')):
                root = ET.fromstring(content)
                for _, (_, namespace_uri) in ET.iterparse(io.BytesIO(content), events=('start-ns',)):
                    _xml_value(namespace_uri, f'{name}:namespace')
                _xml_attributes(root, name, urls)
                if name == 'xl/workbook.xml':
                    privacy = root.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}workbookPr')
                    if privacy is None or privacy.get('filterPrivacy') not in ('1', 'true'):
                        raise ValueError('Workbook privacy setting is not enabled: workbookPr@filterPrivacy')
                if name.endswith('.rels'):
                    for rel in root:
                        target = rel.get('Target', '')
                        if rel.get('TargetMode') == 'External':
                            urls.add(shared_url(target, name))
                        elif re.match(r'(?i)(?:https?|file):', unquote(target)):
                            raise ValueError(f'Invalid relationship target: {name}')
                        else:
                            owner = name.replace('/_rels/', '/').removesuffix('.rels')
                            base = '' if name == '_rels/.rels' else posixpath.dirname(owner)
                            resolved = posixpath.normpath(posixpath.join(base, target)) if not target.startswith('/') else target[1:]
                            if resolved not in names:
                                raise ValueError(f'Invalid or missing internal relationship: {name}')
                else:
                    # Scan complete rich strings, not individual runs: splitting a
                    # credential or private path between formatted runs is unsafe.
                    rich_nodes = set()
                    for rich in root.iter():
                        if rich.tag.rsplit('}', 1)[-1] in ('is','si'):
                            nodes = [t for t in rich.iter() if t.tag.rsplit('}',1)[-1]=='t']
                            rich_nodes.update(nodes)
                            literal = ''.join(t.text or '' for t in nodes)
                            if literal.strip():
                                dummy_input = literal in dummy_literals
                                public_text(literal, name, dummy_input=dummy_input)
                                scan = re.sub(r'\[dummy-input: [^\]\n]+\]', '', literal) if dummy_input else literal
                                urls.update(match.group() for match in url_spans(scan))
                    for element in root.iter():
                        tag = element.tag.rsplit('}', 1)[-1]
                        if tag in ('f', 'formula', 'formula1', 'formula2') and _formula_reference_key(element.text, locale['sheets']) not in allowed_formulas:
                            raise ValueError(f'Unrecognized formula in saved package: {name}')
                        # Formula text is compared against the canonical schema separately.
                        if element.text and element not in rich_nodes and tag not in ('f', 'formula', 'formula1', 'formula2'):
                            value = element.text
                            if value.strip():
                                dummy_input = name.startswith(('xl/worksheets/', 'xl/sharedStrings.xml')) and value in dummy_literals
                                public_text(value, name, dummy_input=dummy_input)
                                scan = re.sub(r'\[dummy-input: [^\]\n]+\]', '', value) if dummy_input else value
                                urls.update(match.group() for match in url_spans(scan))
                        if tag == 'cNvPr':
                            captions.append(element.get('descr') or '')
            else:
                raise ValueError(f'Unsupported binary package entry: {name}')
    for url in urls:
        shared_url(url, 'saved workbook URL')
    digests = Counter(media.values()) if image_digests is None else Counter(image_digests)
    if image_digests is not None and set(digests) != set(media.values()):
        raise ValueError('Saved media payloads differ from bound image instances')
    if phase == 'complete':
        closure = _records(payload.get('closure_confirmation'), ClosureConfirmation)
        for key in ('closed_by', 'source', 'audience'):
            required(getattr(closure, key), f'closure.{key}')
        timestamp(closure.closed_at, 'closure.closed_at')
        accesses = {}
        for item in payload.get('evidence_access', []):
            access = _records(item, EvidenceAccess)
            shared_url(access.url, 'access.url')
            for key in ('audience', 'verified_by', 'source'):
                required(getattr(access, key), f'access.{key}')
            timestamp(access.verified_at, 'access.verified_at')
            if access.audience != closure.audience or access.method not in ('human-attestation', 'recipient-session') or access.url in accesses:
                raise ValueError('Evidence access audience, method or uniqueness mismatch')
            accesses[access.url] = access
        for url in sorted(urls - accesses.keys()):
            gaps.append(f'Access not verified for link: {url}')
        reviews = [_records(item, ScreenshotReview) for item in payload.get('screenshots', [])]
        if len(reviews) != sum(digests.values()):
            gaps.append('Each embedded image requires one matching screenshot review')
        reviewed = Counter()
        identities = {(r.case_id, r.variant) for r in data.rows}
        for review in reviews:
            if (review.case_id, review.variant) not in identities or not re.fullmatch('[0-9a-f]{64}', review.sha256):
                raise ValueError('Unknown screenshot identity or invalid digest')
            for key in ('caption', 'reviewed_by', 'source'):
                required(getattr(review, key), f'screenshot.{key}')
            public_text(review.caption, 'screenshot.caption')
            timestamp(review.reviewed_at, 'screenshot.reviewed_at')
            if review.caption not in captions:
                gaps.append('Screenshot caption must match saved image alternative text')
            reviewed[review.sha256] += 1
        if reviewed != digests:
            gaps.append('Screenshot reviews do not match the saved image bytes')
    elif media:
        gaps.append('Embedded images require review before completion')
    return urls


def check_report(report: Path, source_dir: Path, language='vi', phase='in-progress', *,
                 closure_confirmation=None, evidence_access=(), screenshots=()):
    from block_report import check
    return check(report,source_dir,language,phase,closure_confirmation=closure_confirmation,evidence_access=evidence_access,screenshots=screenshots)


def main():
    # Keep encoding local to this CLI; business strings are never re-decoded.
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--language', choices=('ja', 'vi'), default='vi')
    parser.add_argument('--phase', choices=('in-progress', 'complete'), default='in-progress')
    args = parser.parse_args()
    try:
        payload = json.load(sys.stdin) if args.phase == 'complete' else {}
        if args.phase == 'complete' and (not isinstance(payload, dict) or set(payload) != {'closure_confirmation', 'evidence_access', 'screenshots'}):
            raise ValueError('Completion stdin requires closure_confirmation, evidence_access and screenshots')
        result = check_report(args.report, args.source_dir, args.language, args.phase, **payload)
    except (ValueError, TypeError, OSError, ImportError, KeyError) as error:
        parser.exit(1, f'Report check blocked: {error}\n')
    print(json.dumps(result, ensure_ascii=False))
    return 1 if args.phase == 'complete' and not result['complete'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
