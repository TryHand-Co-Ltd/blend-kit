"""Build self-contained BLEND skills without installing or publishing them.

Only declared skill resources and registered templates are distributed.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
import posixpath
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

SKILLS = ("blend-generate-task", "blend-generate-test-spec", "blend-review-artifacts",
          "blend-plan-implementation", "blend-review-code", "blend-automation-test")
PROFILES = {"codex": ".agents/skills", "cursor": ".cursor/skills", "claude": ".claude/skills"}
RESOURCE_DIRS = ("assets", "references", "scripts")
ALLOWED_SUFFIXES = {".md", ".txt", ".sql", ".xlsx", ".py"}
REPORT_RUNTIME_SCRIPTS = ("report_model.py", "block_report.py", "render_report.py", "export_report.py", "check_report.py", "update_report.py")
REPORT_OWNER = "skills/blend-generate-test-spec"
EVIDENCE_HELPER = "skills/blend-automation-test/scripts/run_artifacts.py"
FORBIDDEN_PARTS = {".git", ".codex", "node_modules", "__pycache__", "tests", "results", "plans"}
LINKS = re.compile(r"\]\(([^)\n]+)\)")
PRIVATE = re.compile(r"(?i)(?:\b[A-Z]:[\\/]|file://|(?:https?://localhost\b|\blocalhost:\d+\b)|127\.0\.0\.1|(?<![A-Za-z])(?:/Users/|/home/|/mnt/[a-z]/)|-----BEGIN [A-Z ]*PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,})")


def safe_path(root: Path, relative: str) -> Path:
    value = Path(relative)
    if value.is_absolute() or ".." in value.parts or "\\" in relative:
        raise ValueError(f"Unsafe resource path: {relative}")
    path = root / value
    current = root
    for part in value.parts:
        current = current / part
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise ValueError(f"Resource/output link is not permitted: {relative}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Resource escapes its root: {relative}")
    return path


def read_registry(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("| Output type |")), None)
    if start is None:
        raise ValueError("Missing TemplateRegistry")
    columns = [cell.strip() for cell in lines[start].strip("|").split("|")]
    required = {"Output type", "Filename", "Language", "Template", "Family", "Version",
                "Required sections", "Fields", "Optional / conditional rule", "Validation"}
    if set(columns) != required or len(columns) != len(required):
        raise ValueError("Invalid TemplateRegistry columns")
    rows = []
    keys = set()
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        values = [cell.strip() for cell in line.strip("|").split("|")]
        if len(values) != len(columns) or not all(values):
            raise ValueError("Invalid/empty TemplateRegistry row")
        row = dict(zip(columns, values))
        key = row["Output type"], row["Language"]
        if key in keys or not re.fullmatch(r"\d+\.\d+\.\d+", row["Version"]):
            raise ValueError(f"Duplicate mapping or invalid version: {key}")
        keys.add(key)
        rows.append(row)
    if not rows:
        raise ValueError("Empty TemplateRegistry")
    for kind in {row["Output type"] for row in rows}:
        pair = {row["Language"]: row for row in rows if row["Output type"] == kind}
        if kind not in {"sql-investigation", "validation-report"}:
            if set(pair) != {"ja", "vi"}:
                raise ValueError(f"Missing bilingual template pair: {kind}")
            fields = ("Family", "Version", "Fields", "Optional / conditional rule", "Validation")
            for field in fields:
                if pair["ja"][field] != pair["vi"][field]:
                    raise ValueError(f"Bilingual schema mismatch: {kind}/{field}")
    return rows


def workbook_metadata(data: bytes, language: str, layout: dict) -> tuple[dict[str, str | None], list[str]]:
    import io
    with zipfile.ZipFile(io.BytesIO(data)) as book:
        props = ET.fromstring(book.read("docProps/custom.xml"))
        metadata = {node.attrib.get("name", ""): next(iter(node)).text for node in props}
        xml = ET.fromstring(book.read("xl/workbook.xml"))
        sheets = [node.attrib["name"] for node in xml.findall("{*}sheets/{*}sheet")]
        if any(name.startswith("xl/externalLinks/") for name in book.namelist()):
            raise ValueError("External workbook dependency is not portable")
        for name in book.namelist():
            if name.endswith((".xml", ".rels")) and PRIVATE.search(book.read(name).decode("utf-8")):
                raise ValueError(f"Private path/value in workbook: {name}")
        strings = []
        if "xl/sharedStrings.xml" in book.namelist():
            strings = ["".join(node.itertext()) for node in ET.fromstring(book.read("xl/sharedStrings.xml"))]
        # The current VI report uses localized detail-tab names.
        expected_sheets = ("Tổng quan", "Kiểm thử") if (
            metadata.get("TemplateVersion") == "2.4.0" and language == "vi"
        ) else layout["sheets"]
        if metadata.get("Language") != language or sheets not in (list(expected_sheets[:2]), list(expected_sheets)):
            raise ValueError("Report language/sheet schema mismatch")
        for index, key, anchor in ((2, "headers", "header_row"), (3, "detail_headers", "detail_header_row")):
            if index > len(sheets):
                continue
            if not layout[key]:
                continue
            xml_sheet = ET.fromstring(book.read(f"xl/worksheets/sheet{index}.xml"))
            matching = []
            for row in xml_sheet.findall("{*}sheetData/{*}row"):
                values = []
                for cell in row:
                    value = "".join(cell.itertext())
                    values.append(strings[int(value)] if cell.attrib.get("t") == "s" else value)
                if tuple(values) == tuple(layout[key]):
                    matching.append(row.attrib["r"])
            if matching != [str(layout[anchor])]:
                raise ValueError("Report core schema headers mismatch")
        return metadata, sheets


def report_layouts(source: Path) -> dict:
    """Read canonical literal layouts/anchors without optional runtime dependencies."""
    path = safe_path(source, "skills/blend-generate-test-spec/scripts/report_model.py")
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    matches = [node.value for node in tree.body if isinstance(node, ast.Assign)
               and any(isinstance(target, ast.Name) and target.id == "REPORT_LAYOUTS" for target in node.targets)]
    if len(matches) != 1:
        raise ValueError("Report layout definition unavailable")
    layouts = ast.literal_eval(matches[0])
    if set(layouts) != {"ja", "vi"}:
        raise ValueError("Report layout language pair unavailable")
    # Canonical common anchors are assigned by this literal update, not copied here.
    for node in tree.body:
        if (isinstance(node, ast.For) and isinstance(node.target, ast.Name)
                and isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Attribute)
                and isinstance(node.iter.func.value, ast.Name)
                and node.iter.func.value.id == "REPORT_LAYOUTS" and node.iter.func.attr == "values"):
            for statement in node.body:
                if (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
                        and isinstance(statement.value.func, ast.Attribute)
                        and isinstance(statement.value.func.value, ast.Name)
                        and statement.value.func.value.id == node.target.id
                        and statement.value.func.attr == "update" and not statement.value.args):
                    anchors = {item.arg: ast.literal_eval(item.value) for item in statement.value.keywords}
                    for layout in layouts.values():
                        layout.update(anchors)
    for layout in layouts.values():
        if not all(isinstance(layout.get(key), int) for key in ("header_row", "detail_header_row")):
            raise ValueError("Canonical report anchors unavailable")
    return layouts


def validate_template(data: bytes, row: dict[str, str], layouts: dict | None = None) -> None:
    if row["Template"].endswith(".xlsx"):
        if row["Family"] != "test-report" or row["Version"] != "2.4.0":
            raise ValueError("Unsupported workbook family")
        if layouts is None:
            layouts = report_layouts(Path(__file__).resolve().parents[1])
        metadata, sheets = workbook_metadata(data, row["Language"], layouts[row["Language"]])
        if metadata.get("TemplateFamily") != row["Family"] or metadata.get("TemplateVersion") != row["Version"]:
            raise ValueError("Workbook family/version mismatch")
        return
    text = data.decode("utf-8-sig").replace("\r\n", "\n")
    identities = re.findall(r"(?:<!--|--)\s*blend-template:\s*([a-z-]+)@(\d+\.\d+\.\d+)", text)
    if identities != [(row["Family"], row["Version"])]:
        raise ValueError(f"Template identity mismatch: {row['Template']}")
    schema = re.search(r"Required schema: ([a-z_,]+)\.", text)
    if schema and schema.group(1) != row["Fields"]:
        raise ValueError(f"Template declared field schema differs from registry: {row['Template']}")
    required = row["Required sections"].split(";")
    if required != ["-"]:
        headings = re.findall(r"^## (.+)$", text, flags=re.M)
        positions = []
        for heading in required:
            if headings.count(heading) != 1:
                raise ValueError(f"Missing/duplicate template section: {heading}")
            positions.append(headings.index(heading))
        if positions != sorted(positions):
            raise ValueError("Template section order mismatch")


def frontmatter(data: bytes, name: str) -> tuple[str, str]:
    text = data.decode("utf-8-sig")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError(f"Missing SKILL frontmatter: {name}")
    fields = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(":")
        if not separator or key in fields or key not in {"name", "description"}:
            raise ValueError(f"Unsupported/duplicate SKILL metadata: {name}")
        fields[key] = value.strip()
    if fields.get("name") != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(f"SKILL name does not match its directory: {name}")
    description = fields.get("description", "")
    if not description or len(description) > 1024 or len(name) > 64:
        raise ValueError(f"Invalid SKILL description/name length: {name}")
    return description, text[match.end():]


def resource_files(root: Path, relative: str) -> list[str]:
    directory = safe_path(root, relative)
    if not directory.is_dir():
        raise ValueError(f"Missing required resource directory: {relative}")
    paths = []
    for parent, dirs, names in os.walk(directory, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name != "__pycache__")
        names = [name for name in names if not name.startswith("~$")]
        for name in dirs + names:
            path = Path(parent) / name
            safe_path(root, path.relative_to(root).as_posix())
        for name in sorted(names):
            path = Path(parent) / name
            if path.suffix == ".pyc":
                continue
            if path.suffix not in ALLOWED_SUFFIXES or any(part in FORBIDDEN_PARTS or part.startswith(".") for part in path.relative_to(root).parts):
                raise ValueError(f"Unapproved resource: {path.relative_to(root)}")
            paths.append(path.relative_to(root).as_posix())
    return paths


def normalize(data: bytes) -> bytes:
    return data.decode("utf-8-sig").replace("\r\n", "\n").encode("utf-8")


def validate_links(files: dict[str, bytes], markdown: str) -> None:
    text = files[markdown].decode("utf-8-sig")
    for value in LINKS.findall(text):
        target = value.strip().strip("<>")
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        target = urllib.parse.unquote(target.split("#", 1)[0])
        if not target:
            continue
        if ":" in target or target.startswith(("/", "\\")):
            raise ValueError(f"Nonportable local link: {markdown}: {value}")
        parts = list(Path(markdown).parent.parts)
        for part in target.split("/"):
            if part == "..":
                if not parts:
                    raise ValueError(f"Link escapes skill: {markdown}: {value}")
                parts.pop()
            elif part not in {"", "."}:
                parts.append(part)
        if "/".join(parts) not in files:
            raise ValueError(f"Missing local resource: {markdown}: {value}")


def prepare_skill(source: Path, name: str, rows: list[dict[str, str]]) -> dict[str, bytes]:
    files = {}
    layouts = report_layouts(source)
    own = f"skills/{name}"
    selected = [f"{own}/SKILL.md", "shared/workflow.md", "shared/artifact-formats.md",
                "shared/review-policy.md", "shared/bug-hunter.md", "shared/bug-hunter-LICENSE.txt",
                "shared/scripts/artifact_gate.py", "shared/automation-testing.md"]
    if name in {"blend-generate-test-spec", "blend-automation-test"}:
        for filename in REPORT_RUNTIME_SCRIPTS:
            relative = f"{REPORT_OWNER}/scripts/{filename}"
            if not safe_path(source, relative).is_file():
                raise ValueError(f"Missing Test Spec report runtime: {relative}")
            selected.append(relative)
        selected.append(f"{REPORT_OWNER}/requirements.txt")
        helper = safe_path(source, EVIDENCE_HELPER)
        if not helper.is_file():
            raise ValueError("Missing evidence validation runtime")
        helper_target = "scripts/run_artifacts.py" if name == "blend-generate-test-spec" else f"_kit/{REPORT_OWNER}/scripts/run_artifacts.py"
        files[helper_target] = helper.read_bytes()
        if name == "blend-automation-test":
            selected.append(f"{REPORT_OWNER}/references/test-report.md")
    for directory in RESOURCE_DIRS:
        path = safe_path(source, f"{own}/{directory}")
        if path.exists():
            selected += resource_files(source, f"{own}/{directory}")
    requirement = f"{own}/requirements.txt"
    if safe_path(source, requirement).exists():
        selected.append(requirement)
    elif name == "blend-generate-test-spec":
        raise ValueError("Test Spec exporter dependency declaration is missing")
    selected += [row["Template"] for row in rows]
    targets = {relative: relative[len(own) + 1:] if relative.startswith(own + "/") else "_kit/" + relative
               for relative in selected}
    for relative in dict.fromkeys(selected):
        path = safe_path(source, relative)
        if not path.is_file():
            raise ValueError(f"Missing source resource: {relative}")
        data = path.read_bytes()
        is_template = any(row["Template"] == relative for row in rows)
        target = targets[relative]
        # Registry dependencies include exact template copies from every owner.
        if is_template:
            files["_kit/" + relative] = data
        if path.suffix == ".md" and not is_template:
            data = normalize(data)
            text = data.decode("utf-8")
            # Rewrite links from declared source resources, including cross-skill
            # report helpers; emitted skills never require sibling installation.
            def emitted_link(match):
                value = match.group(1)
                path, marker, fragment = value.strip().strip("<>").partition("#")
                source_target = posixpath.normpath(posixpath.join(posixpath.dirname(relative), path))
                if source_target not in targets:
                    return match.group(0)
                emitted = posixpath.relpath(targets[source_target], posixpath.dirname(target) or ".")
                return "](" + emitted + (marker + fragment if marker else "") + ")"
            text = LINKS.sub(emitted_link, text)
            if relative == "shared/artifact-formats.md":
                for row in rows:
                    text = text.replace("| " + row["Template"] + " |", "| _kit/" + row["Template"] + " |")
                source_base = "In source, package root is the directory containing `shared/` and `skills/`."
                text = text.replace(source_base, "In this distribution, package root is the directory containing this skill's `SKILL.md`; registry resources are under `_kit/`. Source registry paths have been rewritten to this emitted root.")
            if target == "SKILL.md":
                text += "\nDistribution resource base: the directory containing this `SKILL.md`. Shared policy and registry are bundled under `_kit/shared/`; registry paths resolve from this skill root. Invocation by skill name uses the separate installed entrypoint; no nested entrypoint is bundled.\n"
            data = text.encode("utf-8")
        files[target] = data
    frontmatter(normalize(files["SKILL.md"]), name)
    runtime_rows = read_registry(files["_kit/shared/artifact-formats.md"].decode("utf-8"))
    for row in runtime_rows:
        if row["Template"] not in files:
            raise ValueError(f"Unresolved emitted registry path: {row['Template']}")
        validate_template(files[row["Template"]], row, layouts)
    for relative, data in files.items():
        if Path(relative).suffix != ".xlsx" and PRIVATE.search(data.decode("utf-8-sig")):
            raise ValueError(f"Private path/value in resource: {relative}")
        if Path(relative).suffix == ".md":
            validate_links(files, relative)
    return files


def verify_tree(root: Path, expected: dict[str, bytes]) -> None:
    actual = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    if actual != set(expected):
        raise ValueError("Built inventory differs from declared resources")
    for relative, data in expected.items():
        if safe_path(root, relative).read_bytes() != data:
            raise ValueError(f"Built resource changed: {relative}")


def build(source: Path, output: Path, profiles: list[str], check: bool = False) -> int:
    source = source.resolve(strict=True)
    # Refuse symlink/junction output components before resolve loses their identity.
    output = Path(os.path.abspath(output))
    for component in [output, *output.parents]:
        if component.is_symlink() or (hasattr(component, "is_junction") and component.is_junction()):
            raise ValueError("Output root/ancestor cannot be a link")
    output = output.resolve()
    if output == source or source.is_relative_to(output) or any(output.is_relative_to(source / directory) for directory in ("skills", "shared", "assets", "scripts", "tests", "docs")):
        raise ValueError("Output collides with source resources")
    if len(set(profiles)) != len(profiles) or not profiles or any(name not in PROFILES for name in profiles):
        raise ValueError("Invalid/duplicate profiles")
    registry_path = safe_path(source, "shared/artifact-formats.md")
    rows = read_registry(registry_path.read_text(encoding="utf-8-sig"))
    prepared = {name: prepare_skill(source, name, rows) for name in SKILLS}
    expected = {}
    for profile in profiles:
        for name, files in prepared.items():
            base = f"{profile}/{PROFILES[profile]}/{name}"
            expected.update({f"{base}/{relative}": data for relative, data in files.items()})
    # Preflight every collision before writing anything. Never delete or overwrite.
    for relative, data in expected.items():
        destination = safe_path(output, relative)
        if destination.exists() and (not destination.is_file() or destination.read_bytes() != data):
            raise ValueError(f"Existing output differs; use a new output directory: {relative}")
    if output.exists():
        for path in output.rglob("*"):
            relative = path.relative_to(output).as_posix()
            safe_path(output, relative)
            if path.is_file() and relative not in expected:
                raise ValueError(f"Unrelated existing output preserved; choose a new output directory: {relative}")
    for relative, data in expected.items():
        destination = safe_path(output, relative)
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(data)
    if check:
        verify_tree(output, expected)
    digest = hashlib.sha256(b"".join(relative.encode() + hashlib.sha256(data).digest() for relative, data in sorted(expected.items()))).hexdigest()
    print(f"Built {len(SKILLS)} skills / {len(profiles)} profiles / {len(expected)} files; source parity and resource closure checked. SHA256={digest}")
    print("Package checks only; installation, marketplace compatibility and actual agent semantic parity are not proven.")
    return len(expected)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--profiles", choices=tuple(PROFILES), nargs="+", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        build(args.source, args.output, args.profiles, args.check)
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, ET.ParseError, StopIteration) as error:
        print(f"FAIL package: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
