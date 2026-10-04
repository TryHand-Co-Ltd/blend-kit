"""Focused fixture dispatch and registry conformance; not agent semantic proof."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import sys
from pathlib import Path

# The historical customer-report dispatch identifier now checks the same-file report lifecycle.
AREAS = ("templates", "topics", "task", "test-spec", "review", "planning", "code-review", "customer-report", "package")
ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("blend-generate-task", "blend-generate-test-spec", "blend-review-artifacts",
          "blend-plan-implementation", "blend-review-code")


# Compatibility exports: historical proof scripts keep their original API, while
# the shipped runtime owns the single registry/conformance implementation.
_gate_spec = importlib.util.spec_from_file_location("blend_artifact_gate", ROOT / "shared/scripts/artifact_gate.py")
if _gate_spec is None or _gate_spec.loader is None:
    raise RuntimeError("Common artifact gate unavailable")
_gate = importlib.util.module_from_spec(_gate_spec)
_gate_spec.loader.exec_module(_gate)
load_registry = _gate.load_registry
mapping = _gate.mapping
validate_output_filename = _gate.validate_output_filename
check_identity = _gate.check_identity
validate_markdown = _gate.validate_markdown
validate_output = _gate.validate_output


def resource_gaps(root: Path) -> list[str]:
    """Check actual five-skill Markdown resource closure in the source package."""
    from urllib.parse import unquote, urlsplit
    gaps = []
    for name in SKILLS:
        directory = root / "skills" / name
        if not (directory / "SKILL.md").is_file():
            gaps.append(f"Missing skill: {name}")
            continue
        for path in directory.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for link in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
                parsed = urlsplit(link)
                if parsed.scheme or not parsed.path:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(root.resolve()) or not target.is_file():
                    gaps.append(f"Broken/escaping resource: {path.relative_to(root)}/{link}")
    return gaps


def fixture_identities(root: Path) -> dict[str, str]:
    """Raw writer packs/scorer truth are immutable, including failed focused runs."""
    fixture_root = root / "tests/fixtures"
    return {path.relative_to(fixture_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in fixture_root.rglob("*") if path.is_file()
            and ("inputs" in path.relative_to(fixture_root).parts
                 or "scorer-only" in path.relative_to(fixture_root).parts)}


def inventory_gaps(root: Path, rows: list[dict[str, str]]) -> list[str]:
    """Final inventory gate includes workbook identity without optional dependencies."""
    import zipfile
    import xml.etree.ElementTree as ET
    gaps = []
    for row in rows:
        path = root / row["Template"]
        if not path.is_file():
            gaps.append(f"Missing asset: {row['Template']}")
            continue
        try:
            if path.suffix == ".xlsx":
                with zipfile.ZipFile(path) as book:
                    props = ET.fromstring(book.read("docProps/custom.xml"))
                    values = {node.attrib.get("name"): next(iter(node)).text for node in props}
                    if values.get("TemplateFamily") != row["Family"] or values.get("TemplateVersion") != row["Version"]:
                        raise ValueError("Workbook template metadata mismatch")
            else:
                text = path.read_text(encoding="utf-8")
                if path.suffix == ".md":
                    validate_markdown(text, row)
                else:
                    check_identity(text, row)
        except (ValueError, OSError, KeyError, zipfile.BadZipFile, ET.ParseError, StopIteration) as error:
            gaps.append(f"Invalid asset {row['Template']}: {error}")
    return gaps


class CoreGateTests(__import__("unittest").TestCase):
    """Focused runtime regressions; immutable fixture/proof controls stay unchanged."""

    def completed(self, family, language="vi"):
        row = mapping(load_registry(ROOT), family, language)
        text = (ROOT / row["Template"]).read_text(encoding="utf-8")
        text = re.sub(r"<!--(?!\s*blend-template:).*?-->", "", text, flags=re.S)
        text = re.sub(r"\{\{.*?\}\}", "Scoped source-backed summary", text, flags=re.S)
        return row, text

    def check(self, row, text):
        _gate.check_output(text, row["Filename"].replace("<scope>", "score-save"),
                           load_registry(ROOT), row["Output type"], row["Language"], ROOT)

    def test_asset_inline_labels_and_legacy_api(self):
        row, text = self.completed("implementation-plan")
        self.check(row, text)
        drift = text.replace("Revisions nguồn: Scoped source-backed summary",
                             "Revisions nguồn:\n\nDetails below cannot fill an inline slot")
        with self.assertRaises(ValueError):
            self.check(row, drift)
        with self.assertRaises(ValueError):
            validate_output(drift, "plans/score-save-implementation-plan.vi.md", load_registry(ROOT),
                            "implementation-plan", "vi", required_fields=("Revisions nguồn",))
        for replacement in ("Revisions nguồn (selected): Scoped source-backed summary",
                            "Other: summary\n<!-- Revisions nguồn: hidden -->\n```md\nRevisions nguồn: example\n```",
                            "Revisions nguồn: {{expected identity}}"):
            with self.assertRaises(ValueError):
                self.check(row, text.replace("Revisions nguồn: Scoped source-backed summary", replacement))

    def test_no_findings_and_exact_inventory(self):
        row, text = self.completed("review")
        title = row["Required sections"].split(";")[1]
        end = row["Required sections"].split(";")[2]
        text = re.sub(r"## " + re.escape(title) + r".*?\n## " + re.escape(end),
                      f"## {title}\n\nKhông có findings trong phạm vi artifacts đã đọc; static review only.\n\n## {end}", text, flags=re.S)
        self.check(row, text)
        with self.assertRaises(ValueError):
            self.check(row, text.replace("### Inventory", "### Inventory (selected files)"))
        with self.assertRaises(ValueError):
            self.check(row, text.replace("Không có findings trong phạm vi artifacts đã đọc; static review only.", ""))

    def test_complete_wide_role_disposition(self):
        for language in ("ja", "vi"):
            row, text = self.completed("code-review", language)
            heading = row["Required sections"].split(";")[4]
            asset_section = _gate.sections((ROOT / row["Template"]).read_text(encoding="utf-8"))[heading]
            fields = [field for field, _ in _gate.template_slots(asset_section) if field != "RoleDisposition"]
            self.assertEqual(len(fields), 11)

            def table(columns, values):
                return "\n".join("| " + " | ".join(cells) + " |" for cells in (columns, ["---"] * len(columns), values))

            values = ["F1", "Hunter", "local-pass-1 completed", "local-sequential", "false",
                      "same inspected basis", "source location", "guard assessed", "CANDIDATE",
                      "direct-source", "runtime not run"]
            section = _gate.sections(text)[heading]
            actual_table = re.search(r"(?m)^\|[^\n]+\n\|[-| :]+\|\n(?:\|[^\n]+\n?)+", section).group(0)
            complete = text.replace(actual_table, table(fields, values) + "\n")
            self.check(row, complete)
            self.check(row, text)  # Existing vertical presentation remains valid.
            for columns, records in ((fields[:-1], values[:-1]), (fields, values[:-1] + [""])):
                with self.assertRaises(ValueError):
                    self.check(row, text.replace(actual_table, table(columns, records) + "\n"))
        # Case steps and data tables are not vertical Field/Value schema rows.
        self.assertEqual(_gate.template_slots("| Step | Action | Expected | Preservation |\n| 1 | [action] | [expected] | [state] |"), [])
        self.assertEqual(_gate.template_slots("| Fixture | Role | Values | Reset |\n| TD-01 | [role] | [values] | [reset] |"), [])

    def test_capture_raw_bytes_and_bounds(self):
        import tempfile
        with tempfile.TemporaryDirectory(prefix="gate bytes ") as temporary:
            root = Path(temporary)
            target = root / "saved.md"
            raw = b"\xef\xbb\xbfline\r\nnext\r\n"
            target.write_bytes(raw)
            receipts = _gate.capture_files(root, ["saved.md"])
            self.assertEqual(receipts, [{"path": "saved.md", "size": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}])
            for selected in (["../saved.md"], ["saved.md", "saved.md"], ["."], ["missing.md"]):
                with self.assertRaises((ValueError, OSError)):
                    _gate.capture_files(root, selected)
            link = root / "link.md"
            try:
                link.symlink_to(target)
            except OSError:
                return  # OS symlink permission absent; bounds/raw-byte checks still run.
            with self.assertRaises(ValueError):
                _gate.capture_files(root, ["link.md"])

    def test_each_finding_fixture_and_vertical_role(self):
        row, text = self.completed("code-review")
        heading = row["Required sections"].split(";")[2]
        finding = _gate.sections(text)[heading]
        second = finding.replace("### Scoped source-backed summary", "### F2 — second finding")
        self.check(row, text.replace(finding, finding + "\n" + second))
        incomplete = second.replace("Counter-evidence: Scoped source-backed summary\n", "")
        with self.assertRaisesRegex(ValueError, "F2.*Counter-evidence"):
            self.check(row, text.replace(finding, finding + "\n" + incomplete))

        heading = row["Required sections"].split(";")[4]
        roles = _gate.sections(text)[heading]
        table = re.search(r"(?m)^\|[^\n]+\n\|[-| :]+\|\n(?:\|[^\n]+\n?)+", roles).group(0)
        self.check(row, text.replace(table, table + "\n\n" + table))
        incomplete = table.replace("| counter_evidence | Scoped source-backed summary |\n", "")
        with self.assertRaisesRegex(ValueError, "Each vertical RoleDisposition"):
            self.check(row, text.replace(table, table + "\n\n" + incomplete))

        row, text = self.completed("test-data")
        text = re.sub(r"\[[^]\n]+\]", "Scoped source-backed summary", text)
        fixture = _gate.sections(text)[row["Required sections"].split(";")[1]]
        second = fixture.replace("Fixture: TD-01", "Fixture: TD-02")
        self.check(row, text.replace(fixture, fixture + "\n" + second))
        incomplete = second.replace("| Reset | Scoped source-backed summary |\n", "")
        with self.assertRaisesRegex(ValueError, "TD-02.*Reset"):
            self.check(row, text.replace(fixture, fixture + "\n" + incomplete))

    def test_capture_rejects_parent_swap_before_open(self):
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(prefix="gate owned swap ") as temporary:
            owned = Path(temporary)
            root = owned / "root"
            parent = root / "selected"
            parent.mkdir(parents=True)
            target = parent / "saved.md"
            target.write_bytes(b"original bytes")
            outside = owned / "outside"
            outside.mkdir()
            # Same file identity/bytes through a different parent: checking only
            # fstat against stat would miss this swap; component checks must win.
            (outside / "saved.md").hardlink_to(target)
            original_open = Path.open
            swaps = []

            def swapped_open(path, *args, **kwargs):
                if path == target and not swaps:
                    parent.rename(root / "parked")
                    try:
                        parent.symlink_to(outside, target_is_directory=True)
                        swaps.append("symlink")
                    except OSError:
                        # Directory-identity replacement also exercises the race
                        # on Windows installations without symlink permission.
                        outside.rename(parent)
                        swaps.append("directory identity")
                return original_open(path, *args, **kwargs)

            with patch.object(Path, "open", swapped_open):
                with self.assertRaises(ValueError):
                    _gate.capture_files(root, ["selected/saved.md"])
            self.assertEqual(len(swaps), 1)

    def test_source_and_relocated_bundle_resources(self):
        import tempfile
        self.assertEqual(_gate.resolve_resources(), (ROOT.resolve(), ROOT / "shared/artifact-formats.md"))
        with tempfile.TemporaryDirectory(prefix="renamed package ") as temporary:
            owner = Path(temporary) / "arbitrary skill"
            helper = owner / "_kit/shared/scripts/artifact_gate.py"
            helper.parent.mkdir(parents=True)
            (owner / "_kit/skills").mkdir()
            registry = owner / "_kit/shared/artifact-formats.md"
            registry.write_text((ROOT / "shared/artifact-formats.md").read_text(encoding="utf-8").replace("| skills/", "| _kit/skills/").replace("| assets/", "| _kit/assets/"), encoding="utf-8")
            helper.write_bytes((ROOT / "shared/scripts/artifact_gate.py").read_bytes())
            spec = importlib.util.spec_from_file_location("relocated_gate", helper)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.assertEqual(module.resolve_resources(), (owner.resolve(), registry.resolve()))
            rows = module.load_registry(*module.resolve_resources())
            row = mapping(rows, "implementation-plan", "ja")
            self.assertTrue(row["Template"].startswith("_kit/skills/"))
            relocated_asset = owner / row["Template"]
            relocated_asset.parent.mkdir(parents=True)
            source_row, text = self.completed("implementation-plan", "ja")
            relocated_asset.write_bytes((ROOT / source_row["Template"]).read_bytes())
            module.check_output(text, "plans/score-save-implementation-plan.ja.md", rows,
                                "implementation-plan", "ja", owner)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--area", choices=(*AREAS, "all"), required=True)
    args = parser.parse_args()
    areas = AREAS if args.area == "all" else (args.area,)
    failures = []
    frozen = fixture_identities(ROOT)
    # Fixture branches may import this module without creating a second harness instance.
    sys.modules.setdefault("test_kit", sys.modules[__name__])
    for area in areas:
        path = ROOT / "tests/fixtures" / area / "checks.py"
        if not path.is_file():
            failures.append(f"{area}: unavailable fixture branch {path.relative_to(ROOT)}")
            continue
        try:
            spec = importlib.util.spec_from_file_location(f"checks_{area.replace('-', '_')}", path)
            if spec is None or spec.loader is None:
                raise ValueError("Fixture branch could not be loaded")
            branch = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(branch)
            observations = branch.run(ROOT)
            if not isinstance(observations, list) or not observations or any(not isinstance(item, str) or not item for item in observations):
                raise ValueError("Fixture run must return a nonempty list of actual check observations")
            print(f"PASS focused {area}: " + "; ".join(observations))
        except Exception as error:
            failures.append(f"{area}: {type(error).__name__}: {error}")
    if fixture_identities(ROOT) != frozen:
        failures.append("Frozen raw input/scorer byte inventory changed during fixture execution")
    if args.area == "all":
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(CoreGateTests)
        result = unittest.TextTestRunner(verbosity=1).run(suite)
        if not result.wasSuccessful():
            failures.append("core artifact gate/capture regression controls failed")
        try:
            failures.extend(inventory_gaps(ROOT, load_registry(ROOT)))
        except Exception as error:
            failures.append(f"registry: {type(error).__name__}: {error}")
    else:
        try:
            pending = inventory_gaps(ROOT, load_registry(ROOT))
            if pending:
                print(f"INCOMPLETE full inventory: {len(pending)} missing/invalid assets; focused success is not complete-kit proof.")
                for item in pending:
                    print(f"  {item}")
        except Exception as error:
            failures.append(f"registry: {type(error).__name__}: {error}")
    for failure in failures:
        print(f"FAIL/UNAVAILABLE {failure}", file=sys.stderr)
    print("Structural/fixture checks only. Actual agent semantic parity and workbook render/recalculation are separate proof.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
