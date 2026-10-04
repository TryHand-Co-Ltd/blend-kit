"""Read-only registered Markdown conformance and explicitly selected byte capture.

This stdlib helper ships with each skill. It does not certify source semantics,
approval, application execution or workbook projection/render/recalculation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
from pathlib import Path


def resolve_resources() -> tuple[Path, Path]:
    """Resolve only the known source or self-contained bundle structure."""
    shared = Path(__file__).resolve().parent.parent
    registry = shared / "artifact-formats.md"
    container = shared.parent
    # In source, shared/ and skills/ share a root. Bundles put the registry in
    # <owner>/_kit/shared and rewrite Template cells relative to <owner>.
    if (container / "skills").is_dir() and (container / "shared") == shared:
        first = registry.read_text(encoding="utf-8") if registry.is_file() else ""
        bundled = "| _kit/skills/" in first
        root = container.parent if bundled else container
    else:
        root = container.parent
    if not registry.is_file() or not (root / ("_kit/skills" if root != container else "skills")).is_dir():
        raise ValueError("Missing declared source/bundle registry resource structure")
    return root, registry


def load_registry(root: Path, registry_path: Path | None = None) -> list[dict[str, str]]:
    """Read the single Markdown table; reject ambiguous/escaping mappings."""
    root = root.resolve()
    registry_path = registry_path or root / "shared/artifact-formats.md"
    text = registry_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("| Output type |")), None)
    if start is None:
        raise ValueError("Template registry table is missing")
    columns = [value.strip() for value in lines[start].strip("|").split("|")]
    required = {"Output type", "Filename", "Language", "Template", "Family", "Version",
                "Required sections", "Fields", "Optional / conditional rule", "Validation"}
    if len(columns) != len(required) or set(columns) != required:
        raise ValueError("Registry columns do not match the contract")
    rows = []
    seen = set()
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        values = [value.strip() for value in line.strip("|").split("|")]
        if len(values) != len(columns) or any(not value for value in values):
            raise ValueError("Registry row has missing/ambiguous fields")
        row = dict(zip(columns, values))
        key = row["Output type"], row["Language"]
        if key in seen:
            raise ValueError(f"Duplicate output/language mapping: {key}")
        seen.add(key)
        target = (root / row["Template"]).resolve()
        if not target.is_relative_to(root) or Path(row["Template"]).is_absolute() or "\\" in row["Template"]:
            raise ValueError(f"Template escapes package: {row['Template']}")
        if not re.fullmatch(r"\d+\.\d+\.\d+", row["Version"]):
            raise ValueError(f"Invalid template version: {key}")
        rows.append(row)
    if not rows:
        raise ValueError("Template registry is empty")
    return rows


def mapping(rows: list[dict[str, str]], output_type: str, language: str) -> dict[str, str]:
    matches = [row for row in rows if row["Output type"] == output_type and row["Language"] == language]
    if len(matches) != 1:
        raise ValueError(f"Unsupported output/language: {output_type}/{language}")
    return matches[0]


def validate_output_filename(filename: str, row: dict[str, str]) -> None:
    if not filename or "\\" in filename or ":" in filename or any(part in ("", ".", "..") for part in filename.split("/")):
        raise ValueError("Output filename is not a portable relative path")
    pattern = re.escape(row["Filename"])
    for token in ("<topic>", "<scope>"):
        pattern = pattern.replace(re.escape(token), r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*")
    if re.fullmatch(pattern, filename) is None:
        raise ValueError(f"Output filename does not match {row['Filename']}")


def visible_body(text: str, *, keep_comments: bool = False) -> str:
    """Comments and complete or unterminated fences cannot supply fields."""
    if not keep_comments:
        text = re.sub(r"<!--.*?(?:-->|\Z)", "", text, flags=re.S)
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
            continue
        if match:
            fence = match.group(1)
        else:
            lines.append(line)
    return "\n".join(lines)


def check_identity(text: str, row: dict[str, str]) -> None:
    # Strip fences but preserve actual provenance comments.
    body = visible_body(text, keep_comments=True)
    pattern = r"(?:<!--|--)\s*blend-template:\s*([a-z-]+)@(\d+\.\d+\.\d+)"
    identities = re.findall(pattern, body)
    expected = (row["Family"], row["Version"])
    if identities != [expected]:
        raise ValueError(f"Missing/wrong/duplicate template identity; expected {expected}")


def field_value(line: str, field: str) -> str | None:
    clean = line.strip().replace("**", "")
    if clean.startswith("|"):
        cells = [cell.strip() for cell in clean.strip("|").split("|")]
        return cells[1] if len(cells) >= 2 and cells[0] == field else None
    clean = clean.removeprefix("- ")
    match = re.fullmatch(re.escape(field) + r"\s*[:：]\s*(.*)", clean)
    return match.group(1) if match else None


def validate_markdown(text: str, row: dict[str, str], *, required_fields: tuple[str, ...] = (),
                      conditional_sections: dict[str, bool] | None = None) -> None:
    """Compatibility structural gate; explicit localized inline labels stay strict."""
    check_identity(text, row)
    body = visible_body(text)
    headings = re.findall(r"^## ([^\n]+)$", body, flags=re.M)
    expected = row["Required sections"].split(";")
    if expected != ["-"]:
        positions = []
        for heading in expected:
            if headings.count(heading) != 1:
                raise ValueError(f"Missing/duplicate required section: {heading}")
            positions.append(headings.index(heading))
        if positions != sorted(positions):
            raise ValueError("Required sections out of template order")
    for field in required_fields:
        values = [value for line in body.splitlines() if (value := field_value(line, field)) is not None]
        if not values or any(not value.strip() for value in values):
            raise ValueError(f"Missing/empty required field: {field}")
    for heading, required_now in (conditional_sections or {}).items():
        if required_now and headings.count(heading) != 1:
            raise ValueError(f"Required conditional section omitted: {heading}")
        if not required_now and heading in headings:
            raise ValueError(f"Conditional section present outside its scope: {heading}")


def validate_output(text: str, filename: str, rows: list[dict[str, str]], output_type: str,
                    language: str, **kwargs) -> None:
    """Legacy API retained for historical proof scripts and fixture callers."""
    row = mapping(rows, output_type, language)
    validate_output_filename(filename, row)
    validate_markdown(text, row, **kwargs)


def sections(text: str) -> dict[str, str]:
    pieces = re.split(r"^## ([^\n]+)\n?", visible_body(text), flags=re.M)
    return dict(zip(pieces[1::2], pieces[2::2]))


def template_slots(section: str) -> list[tuple[str, str]]:
    """The maintained asset is the localized label/presentation schema."""
    slots = []
    lines = section.splitlines()
    for index, line in enumerate(lines):
        clean = line.strip().replace("**", "").removeprefix("- ")
        if clean.startswith("|"):
            cells = [cell.strip() for cell in clean.strip("|").split("|")]
            if len(cells) == 2 and not re.search(r"[\[{}]", cells[0]) and re.search(r"\{\{|\[[^]]+\]", cells[1]):
                slots.append((cells[0], "inline"))
        else:
            match = re.fullmatch(r"([^:：{}\[\]\n]+)[:：]\s*(.*)", clean)
            if match and (not match.group(2) or re.search(r"\{\{|\[[^]]+\]", match.group(2))):
                following = next((value.strip() for value in lines[index + 1:] if value.strip()), "")
                presentation = "inline" if match.group(2) else "list" if following.startswith("- ") else "block"
                slots.append((match.group(1).strip(), presentation))
    return list(dict.fromkeys(slots))


def explicit_none(section: str) -> bool:
    prose = "\n".join(line for line in section.splitlines() if not line.strip().startswith(("|", "#")))
    return bool(re.search(r"\bno (?:supported )?(?:findings|candidates|shared fixtures|open (?:business )?questions)\b|không có|なし|該当なし", prose, re.I))


def validate_slots(content: str, slots: list[tuple[str, str]], location: str) -> None:
    """Validate one asset-defined entry; sibling values cannot fill missing slots."""
    lines = content.splitlines()
    for field, presentation in slots:
        matches = [(i, value) for i, line in enumerate(lines) if (value := field_value(line, field)) is not None]
        if not matches:
            raise ValueError(f"Missing required exact field in {location}: {field}")
        for i, value in matches:
            if presentation == "inline":
                if not value.strip():
                    raise ValueError(f"Missing/empty inline required field: {field}")
            else:
                following = []
                for line in lines[i + 1:]:
                    if line.startswith("#") or any(field_value(line, key) is not None for key, _ in slots):
                        break
                    if line.strip():
                        following.append(line)
                if not following or (presentation == "list" and not any(re.match(r"^-\s+\S", line.strip()) for line in following)):
                    raise ValueError(f"Missing/empty block required field: {field}")


def validate_entries(content: str, schema: str, location: str) -> None:
    """Only repeated finding/question/fixture H3 entries, using their actual asset."""
    blocks = re.split(r"^### ([^\n]+)\n?", schema, flags=re.M)
    if len(blocks) < 3:
        return
    entry_slots = template_slots(blocks[2])
    optional_titles = {title for title in blocks[3::2] if not re.search(r"\{\{|\[", title)}
    entries = re.split(r"^### ([^\n]+)\n?", content, flags=re.M)
    for title, body in zip(entries[1::2], entries[2::2]):
        if title not in optional_titles:
            validate_slots(body, entry_slots, f"{location}/{title}")


def check_output(text: str, filename: str, rows: list[dict[str, str]], output_type: str,
                 language: str, resource_root: Path) -> None:
    """Before-handoff gate: registered identity/order and asset-derived filled slots."""
    row = mapping(rows, output_type, language)
    if not filename.endswith(".md"):
        raise ValueError("This gate checks Markdown only; workbook/SQL require their own gates")
    validate_output(text, filename, rows, output_type, language)
    template = (resource_root / row["Template"]).read_text(encoding="utf-8")
    validate_markdown(template, row)
    if re.search(r"\{\{.*?\}\}|TEMPLATE INSTRUCTIONS|AUTHORING:", text, re.S | re.I):
        raise ValueError("Unfilled placeholder or authoring instruction remains")
    # Reject exact bracket placeholders maintained by this asset, preserving real
    # Markdown links, literals and unchecked acceptance checklists.
    for placeholder in re.findall(r"\[[^]\n]+\]", visible_body(template)):
        if placeholder in text and not placeholder.startswith("[ ]"):
            raise ValueError(f"Unfilled template placeholder: {placeholder}")
    actual = sections(text)
    schema = sections(template)
    headings = row["Required sections"].split(";")
    conditional_entry = {"review": 1, "code-review": 2, "business-questions": 1, "test-data": 1}
    for index, heading in enumerate(headings):
        content = actual[heading]
        useful = [line for line in content.splitlines() if line.strip() and not line.lstrip().startswith(("#", "|"))]
        table_values = [line for line in content.splitlines() if line.startswith("|") and not re.fullmatch(r"[-|:\s]+", line)]
        if not useful and len(table_values) < 2:
            raise ValueError(f"Empty required section: {heading}")
        field_schema = schema[heading]
        if output_type == "test-cases" and index == 0:
            # The optional shared Context block cannot become a prerequisite;
            # cases retain the same required slots in their own H2.
            field_schema = field_schema.split("\n### ", 1)[0]
        slots = template_slots(field_schema)
        if output_type == "code-review" and index == 4:
            # The asset illustrates a vertical table, while the shared protocol
            # also permits one wide row per role. Keep its same eleven fields.
            role_fields = [field for field, _ in slots if field != "RoleDisposition"]
            lines = content.splitlines()
            wide = False
            # Validate every vertical table independently, including mixed wide
            # and vertical reports. One complete role cannot mask the next role.
            for table in re.findall(r"(?:^[ \t]*\|[^\n]+\n?)+", content, re.M):
                vertical = []
                for line in table.splitlines():
                    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                    if len(cells) == 2 and cells[0] in role_fields:
                        vertical.append(cells)
                if vertical:
                    if len(vertical) != len(role_fields) or {cells[0] for cells in vertical} != set(role_fields):
                        raise ValueError("Each vertical RoleDisposition entry must contain every exact field once")
                    if any(not cells[1] for cells in vertical):
                        raise ValueError("Each vertical RoleDisposition entry requires populated field values")
            for position, line in enumerate(lines):
                if not line.strip().startswith("|"):
                    continue
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if (len(cells) <= 2 or not set(cells).intersection(role_fields)
                        or position + 1 >= len(lines)
                        or not re.fullmatch(r"[-|:\s]+", lines[position + 1].strip())):
                    continue
                if len(cells) != len(role_fields) or set(cells) != set(role_fields):
                    raise ValueError("RoleDisposition wide table must contain every exact field once")
                records = []
                for following in lines[position + 1:]:
                    if not following.strip().startswith("|"):
                        break
                    if re.fullmatch(r"[-|:\s]+", following.strip()):
                        continue
                    records.append([cell.strip() for cell in following.strip().strip("|").split("|")])
                if not records or any(len(record) != len(role_fields) or any(not cell for cell in record) for record in records):
                    raise ValueError("RoleDisposition wide table requires populated values for every field in every row")
                wide = True
            if wide:
                slots = [(field, presentation) for field, presentation in slots if field not in role_fields]
        # Entries may be absent with an explicit scoped none statement. A finding
        # or fixture label present anywhere re-enables the full entry schema.
        if conditional_entry.get(output_type) == index and explicit_none(content) and not any(
                field_value(line, field) is not None for field, _ in slots for line in content.splitlines()):
            continue
        validate_slots(content, slots, heading)
        if conditional_entry.get(output_type) == index:
            validate_entries(content, field_schema, heading)
    # Review inventory is a prescribed fixed H3/table, not an extensible label.
    if output_type == "review":
        asset_h3 = re.findall(r"^### ([^\n]+)$", schema[headings[0]], re.M)
        for title in asset_h3:
            if not re.search(r"^### " + re.escape(title) + r"$", actual[headings[0]], re.M):
                raise ValueError(f"Missing required exact inventory heading: {title}")
            inventory = re.split(r"^### " + re.escape(title) + r"\n", actual[headings[0]], flags=re.M)[1]
            if len([line for line in inventory.splitlines() if line.startswith("|") and not re.fullmatch(r"[-|:\s]+", line)]) < 2:
                raise ValueError("Required inventory has no populated row")


def file_state(metadata: os.stat_result) -> tuple[int, ...]:
    if not metadata.st_ino:
        raise ValueError("Capture unavailable: filesystem has no stable file identity")
    return (metadata.st_dev, metadata.st_ino, metadata.st_mode,
            metadata.st_size if stat.S_ISREG(metadata.st_mode) else 0,
            metadata.st_mtime_ns if stat.S_ISREG(metadata.st_mode) else 0)


def capture_path_state(root: Path, parts: list[str]) -> list[tuple[int, ...]]:
    """Observe every pathname component, including root/ancestors, without scans."""
    paths = [*reversed(root.parents), root]
    target = root
    for part in parts:
        target = target / part
        paths.append(target)
    states = []
    for path in paths:
        metadata = path.lstat()
        reparse = getattr(metadata, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if stat.S_ISLNK(metadata.st_mode) or reparse:
            raise ValueError("Capture pathname changed or traverses a symlink/junction")
        states.append(file_state(metadata))
    if root.resolve(strict=True) != root or target.resolve(strict=True) != target or not target.is_relative_to(root):
        raise ValueError("Capture pathname no longer resolves within the verified root")
    return states


def capture_files(root: Path, selected: list[str]) -> list[dict[str, str | int]]:
    """Read explicit bytes; reject receipts on observed path/file identity drift.

    Descriptor identity is checked before reading, with component checkpoints
    before/after. Portable pathname APIs do not atomically lock a directory tree:
    this is receipt validation, not a guarantee against every adversarial open/read.
    """
    original_root = root.absolute().lstat()
    root = root.resolve(strict=True)
    if file_state(root.lstat()) != file_state(original_root) or stat.S_ISLNK(original_root.st_mode) or getattr(original_root, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
        raise ValueError("Capture root changed or is a symlink/junction")
    if not root.is_dir() or not selected or len(selected) > 512:
        raise ValueError("Capture requires a verified directory and 1..512 explicitly selected files")
    root_state = capture_path_state(root, [])
    receipts = []
    seen = set()
    for relative in selected:
        parts = relative.split("/")
        if len(parts) > 32 or "\\" in relative or ":" in relative or any(part in ("", ".", "..") for part in parts):
            raise ValueError(f"Capture path is not a bounded portable root-relative file: {relative}")
        if relative in seen:
            raise ValueError(f"Duplicate selected capture: {relative}")
        seen.add(relative)
        target = root.joinpath(*parts)
        path_state = capture_path_state(root, parts)
        if path_state[:len(root_state)] != root_state or not stat.S_ISREG(path_state[-1][2]):
            raise ValueError(f"Capture is missing, non-file or outside verified root: {relative}")
        with target.open("rb") as stream:
            before = os.fstat(stream.fileno())
            if file_state(before) != path_state[-1] or capture_path_state(root, parts) != path_state:
                raise ValueError(f"Capture opened identity/path changed before reading: {relative}")
            digest = hashlib.sha256()
            size = 0
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
                size += len(chunk)
            after = os.fstat(stream.fileno())
            if file_state(before) != file_state(after) or capture_path_state(root, parts) != path_state:
                raise ValueError(f"Capture file/path changed during reading: {relative}")
        if capture_path_state(root, parts) != path_state or size != after.st_size:
            raise ValueError(f"File changed during capture: {relative}")
        receipts.append({"path": relative, "size": size, "sha256": digest.hexdigest()})
    return receipts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="check a completed registered Markdown artifact")
    check.add_argument("--type", required=True)
    check.add_argument("--language", required=True)
    check.add_argument("--file", type=Path, required=True)
    check.add_argument("--filename", required=True, help="registry-relative output name, independent of actual storage")
    capture = sub.add_parser("capture", help="stdout receipts from explicitly selected raw file bytes")
    capture.add_argument("--root", type=Path, required=True)
    capture.add_argument("--file", action="append", required=True)
    args = parser.parse_args()
    try:
        if args.command == "capture":
            print(json.dumps({"kind": "observed-byte-capture", "files": capture_files(args.root, args.file)}, ensure_ascii=False))
        else:
            root, registry = resolve_resources()
            check_output(args.file.read_text(encoding="utf-8-sig"), args.filename, load_registry(root, registry), args.type, args.language, root)
            print("PASS — registered Markdown structure and filled asset slots; semantic/approval/runtime/workbook proof separate.")
        return 0
    except (OSError, ValueError) as error:
        print(f"Draft/Blocked — artifact gate failed or unavailable: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
