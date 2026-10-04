"""Template gates and raw synthetic evidence integrity; not model bug-detection proof."""
from pathlib import Path
import csv
import difflib
import hashlib
import io
import json
import re

from test_kit import load_registry, mapping, validate_markdown, validate_output_filename


def rejected(call, control):
    try:
        call()
    except ValueError:
        return
    raise AssertionError(f"Invalid control accepted: {control}")


def role_control_result(case, required_fields):
    """Validate synthetic schema/state only; nonempty identities do not prove a run."""
    if case.get("independent_required") and not case.get("backend_available"):
        return "UNREVIEWED"

    def valid(output, role):
        if not isinstance(output, dict) or set(output) != set(required_fields):
            return False
        if any(not isinstance(output[field], str) or not output[field].strip()
               for field in required_fields if field != "independent"):
            return False
        if type(output["independent"]) is not bool or output["role"] != role:
            return False
        if output["depth"] not in ("direct-source", "evidence-only", "not-run"):
            return False
        if output["backend"] == "local-sequential" and output["independent"]:
            return False
        if case.get("independent_required") and not output["independent"]:
            return False
        return True

    hunter = case.get("Hunter")
    if not valid(hunter, "Hunter"):
        return "UNREVIEWED"
    if hunter["verdict"] == "NO_CANDIDATES" and hunter["candidate_id"] == "none":
        return "NO_CANDIDATES" if hunter["depth"] == "direct-source" else "UNREVIEWED"
    if hunter["verdict"] != "CANDIDATE" or hunter["candidate_id"] == "none":
        return "UNREVIEWED"
    for role in ("Skeptic", "Referee"):
        output = case.get(role)
        if not valid(output, role) or output["candidate_id"] != hunter["candidate_id"] or output["basis"] != hunter["basis"]:
            return "UNREVIEWED"
    # No complete positive candidate role run is supplied by these synthetic controls.
    return "UNREVIEWED"


def check_customer_readiness_packet(fixtures: Path):
    """Validate isolated raw controls, not whether an agent finds or classifies them."""
    pack = fixtures / "customer-readiness-inputs"
    pins = re.findall(r"^\| ([^|]+) \| ([a-f0-9]{64}) \|$",
                      (pack / "SNAPSHOT.md").read_text(encoding="utf-8"), re.M)
    actual = {path.relative_to(pack).as_posix() for path in pack.rglob("*")
              if path.is_file() and path.name != "SNAPSHOT.md"}
    assert actual == {name for name, _ in pins} and len(actual) == 11
    assert not any("oracle" in name or "scorer" in name or "findings" in name for name in actual)
    for name, digest in pins:
        assert hashlib.sha256((pack / name).read_bytes()).hexdigest() == digest, f"Raw drift: {name}"
    read = lambda name: (pack / name).read_text(encoding="utf-8")
    before, after = read("base/Record_m.php"), read("current/Record_m.php")
    assert "return [];" not in before
    assert after.index("use_readonly_start") < after.index("return [];") < after.index("use_readonly_end")
    controller = read("current/Record.php")
    assert controller.split("public function show", 1)[1].split("public function save", 1)[0] == read("base/Record.php").split("public function show", 1)[1].split("public function save", 1)[0]
    assert "getById" in controller.split("public function raw", 1)[1]
    assert "school_id" not in controller.split("public function raw", 1)[1]
    assert "records/raw" not in read("base/routes.php") and "records/raw" in read("current/routes.php")
    assert "in_array($method, [1, 2], true)" in controller
    assert "->save($id, $offset, $method)" in controller and "save($id, $offset, $method)" in after
    # The complete write body remains distinguishable from schema/input/read presence.
    assignment = re.search(r"update\('records', (\[[^;]+\])\);", after).group(1)
    assert "'offset' => $offset" in assignment and "$method" not in assignment
    ddl = read("current/method.sql")
    assert "method TINYINT NOT NULL" in ddl and "COMMENT" not in ddl and "UPDATE" not in ddl
    # Independent correction controls are kept here, outside the blind packet.
    comment_only = ddl.replace("NOT NULL;", "NOT NULL COMMENT 'Selected calculation method';")
    nullable_only = ddl.replace("NOT NULL", "NULL")
    assert "NOT NULL" in comment_only and "COMMENT" in comment_only
    assert "NOT NULL" not in nullable_only and "COMMENT" not in nullable_only
    assert not any("TenantController" in name for name in actual)
    assert "version" in read("environment.md") and "unknown" in read("environment.md")


def run(root: Path) -> list[str]:
    skill_root = root / "skills/blend-review-code"
    skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    header = skill.split("---", 2)[1]
    assert re.search(r"^name: blend-review-code$", header, re.M)
    assert re.search(r"^description: \S.+$", header, re.M)
    for source in (skill_root / "SKILL.md", skill_root / "references/code-review.md"):
        text = source.read_text(encoding="utf-8")
        for relative in re.findall(r"\]\(([^)]+)\)", text):
            if "://" not in relative:
                path, _, anchor = relative.partition("#")
                target = (source.parent / path).resolve()
                assert target.is_file() and target.is_relative_to(root.resolve()), f"Broken link: {relative}"
                if anchor:
                    headings = re.findall(r"^#{1,6} (.+)$", target.read_text(encoding="utf-8"), re.M)
                    assert anchor in {re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-") for heading in headings}, f"Broken anchor: {relative}"
        assert not re.search(r"[A-Za-z]:[/\\]|localhost|127\.0\.0\.1", text)
    license_bytes = (root / "shared/bug-hunter-LICENSE.txt").read_bytes()
    assert hashlib.sha256(license_bytes).hexdigest() == "363363d8c6255e2a4e68724b3e0ea4919ee651751af2b87ddfe9986a077e5b14"
    assert not (skill_root / "references/bug-hunter.md").exists(), "Common protocol must not fork"
    rows = load_registry(root)
    labels = {
        "vi": ("Danh tính", "Nguồn và revision plan", "Base và head", "Danh tính working bytes",
               "Phạm vi nghiệp vụ dự kiến", "Thay đổi thực tế", "Inventory kiểm tra", "Findings trước",
               "Finding ID", "Yêu cầu", "Invariant", "Bằng chứng", "Actor và trigger", "Expected và actual",
               "Tác động", "Counter-evidence", "Đề xuất cập nhật", "Kiểm chứng sau sửa", "Phạm vi", "Origin",
               "Severity", "Confidence", "Ảnh hưởng hoàn thành", "Ảnh hưởng consumer", "Rủi ro DB",
               "RoleDisposition", "Kết luận độc lập", "Giới hạn"),
        "ja": ("識別情報", "参照元・計画Revision", "Base・Head", "作業内容識別", "予定業務範囲", "実差分",
               "調査一覧", "前回Findings", "Finding ID", "要求", "Invariant", "証拠", "Actor・Trigger",
               "Expected・Actual", "影響", "Counter-evidence", "更新提案", "修正後の確認", "対象範囲",
               "Origin", "Severity", "Confidence", "完了への影響", "Consumerへの影響", "DBリスク",
               "RoleDisposition", "独立判定", "限界"),
    }
    protocol = (root / "shared/bug-hunter.md").read_text(encoding="utf-8")
    role_fields = tuple(re.findall(r"^\| ([a-z_]+) \|", protocol, re.M))
    assert len(role_fields) == 11
    for language in ("ja", "vi"):
        row = mapping(rows, "code-review", language)
        template = (root / row["Template"]).read_text(encoding="utf-8")
        assert len(re.findall(r"^## ", template, re.M)) == 7
        validate_markdown(template, row, required_fields=labels[language])
        assert all(field in template for field in row["Fields"].split(","))
        for field in role_fields:
            assert re.search(r"^\| " + field + r" \| \{\{.+\}\} \|$", template, re.M)
        assert "Prior-finding ledger is required only on re-review" in template
        assert "Conditional H3 DB/migration detail is required only when affected" in template
        completed = re.sub(r"<!--(?! blend-template:).*?-->", "", template, flags=re.S)
        completed = re.sub(r"\{\{.*?\}\}", "synthetic supplied source; no runtime proof", completed, flags=re.S)
        validate_markdown(completed, row, required_fields=labels[language])
        validate_output_filename(f"score-review-code-review.{language}.md", row)
        rejected(lambda: validate_output_filename(f"../score-code-review.{language}.md", row), "escaping output")
        rejected(lambda: validate_markdown(completed.replace("code-review@1.0.0", "code-review@9.0.0"), row), "wrong family version")
        headings = row["Required sections"].split(";")
        for heading in headings:
            rejected(lambda: validate_markdown(completed.replace("## " + heading, "## Missing"), row), "missing H2")
        swapped = completed.replace("## " + headings[0], "## SWAP").replace("## " + headings[1], "## " + headings[0]).replace("## SWAP", "## " + headings[1])
        rejected(lambda: validate_markdown(swapped, row), "reordered H2")
        for field in labels[language]:
            # Remove every actual label occurrence, not a mention in schema comments.
            broken = re.sub(r"(?m)^(?:\| " + re.escape(field) + r" \|.*|" + re.escape(field) + r":.*)$", "", completed)
            rejected(lambda: validate_markdown(broken, row, required_fields=labels[language]), "missing required field")

    fixtures = Path(__file__).parent
    raw = fixtures / "inputs/implementation"
    oracle = json.loads((fixtures / "scorer-only/oracle.json").read_text(encoding="utf-8"))
    for pack in (raw, fixtures / "inputs/role-controls", fixtures / "inputs/baseline-controls"):
        assert not any(path.name == "oracle.json" for path in pack.rglob("*"))
        snapshot = (pack / "SNAPSHOT.md").read_text(encoding="utf-8")
        pins = re.findall(r"^\| ([^|]+) \| ([a-f0-9]{64}) \|$", snapshot, re.M)
        actual = {path.relative_to(pack).as_posix() for path in pack.rglob("*") if path.is_file() and path.name != "SNAPSHOT.md"}
        assert actual == {name for name, _ in pins}
        for name, digest in pins:
            path = (pack / name).resolve()
            assert path.is_relative_to(pack.resolve())
            assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"Raw drift: {name}"
    metadata = json.loads((raw / "snapshot-metadata.json").read_text(encoding="utf-8"))
    assert metadata["kind"] == "synthetic-byte-snapshots-not-observed-git"
    states = {}
    for state, pins in metadata["files"].items():
        files = {path.relative_to(raw / state).as_posix(): path for path in (raw / state).rglob("*") if path.is_file()}
        assert set(files) == set(pins)
        states[state] = {}
        for name, path in files.items():
            assert hashlib.sha256(path.read_bytes()).hexdigest() == pins[name]
            states[state][name] = path.read_text(encoding="utf-8")
    base, head, index, current = (states[name] for name in ("base", "head", "index", "current"))
    expected_diff = "".join("".join(difflib.unified_diff(base.get(name, "").splitlines(True), current.get(name, "").splitlines(True), fromfile="base/" + name, tofile="current/" + name)) for name in sorted(set(base) | set(current)))
    assert (raw / "actual.diff").read_text(encoding="utf-8") == expected_diff
    working = metadata["working"]
    assert set(working["staged"]) == {name for name in set(head) | set(index) if head.get(name) != index.get(name)}
    assert set(working["unstaged"]) == {name for name in index if index[name] != current.get(name)}
    assert set(working["untracked"]) == set(current) - set(index)
    for before, after in working["renamed"]:
        assert before in base and before not in head and after in head and base[before] == head[after]
    assert all(name in base and name not in current for name in working["deleted"])
    helper = "application/helpers/score_helper.php"
    assert "$score < $threshold" in base[helper] and "$score <= $threshold" in current[helper]
    # Concrete discriminating values, not a word-only expectation of model accuracy.
    assert [score < 80 for score in (79, 80, 81)] == [True, False, False]
    assert [score <= 80 for score in (79, 80, 81)] == [True, True, False]
    attendance = "application/controllers/AttendanceExport.php"
    assert base[attendance] == current[attendance] and "isBelow(" in current[attendance]
    assert base[helper].split("function legacyAlias", 1)[1] == current[helper].split("function legacyAlias", 1)[1]
    controller = "application/controllers/Score.php"
    model = "application/models/Record_m.php"
    assert base[model].split("public function getById", 1)[1].split("\n\t}", 1)[0] == current[model].split("public function getById", 1)[1].split("\n\t}", 1)[0]
    assert "public function rawExport" not in base[controller] and "public function rawExport" in current[controller]
    for source in (base[controller], current[controller]):
        show = source.split("public function show", 1)[1].split("\n\t}", 1)[0]
        assert show.index("school_id") < show.index("return $record") and "['year']" in show
    raw_export = current[controller].split("public function rawExport", 1)[1]
    assert "getById" in raw_export and "school_id" not in raw_export
    read = current[model].split("public function read", 1)[1].split("\n\t}", 1)[0]
    assert read.index("use_readonly_start") < read.index("return []") < read.index("use_readonly_end")
    job = current["application/controllers/ScoreJob.php"]
    assert job.index("->save(") < job.index("->read(")
    assert "return 'Calculate'" in base[controller] and "return 'Run'" in current[controller]
    rows_data = list(csv.DictReader(io.StringIO((raw / "data-shape.csv").read_text(encoding="utf-8"))))
    assert rows_data[0]["score"] == rows_data[0]["threshold"] == "80"
    assert rows_data[1]["offset"] == "" and rows_data[2]["offset"] == "7"
    keys = [(row["school_id"], row["year"], row["student_id"]) for row in rows_data]
    assert len(keys) > len(set(keys)), "Duplicate-key control must be real supplied data"
    ddl = current["application/migration/2026/score-method.sql"]
    assert "UPDATE score_records SET offset = 0;" in ddl and "WHERE" not in ddl
    assert ddl.count("ALTER TABLE score_records") == 3 and "FOREIGN KEY" in ddl and "COMMENT" not in ddl
    assert "method TINYINT NOT NULL" in ddl and "ADD UNIQUE KEY" in ddl
    for finding in oracle["findings"]:
        path, line = finding["anchor"].rsplit(":", 1)
        assert current[path].splitlines()[int(line) - 1].strip(), f"Bad scorer anchor {finding['id']}"
        assert finding["proposal"] and finding["verify"]
    scored = {finding["id"]: finding for finding in oracle["findings"]}
    assert scored["F-SHARED"]["origin"] == "INTRODUCED" and scored["F-SHARED"]["effect"] == "Regression blocker"
    assert scored["F-LEGACY"]["origin"] == "PRE_EXISTING" and scored["F-LEGACY"]["effect"] == "Follow-up"
    assert scored["F-AC-LABEL"]["severity"] == "Low" and scored["F-AC-LABEL"]["effect"] == "Task blocker"
    assert oracle["disproof"]["verdict"] == "NOT_A_BUG"
    controls = json.loads((fixtures / "inputs/role-controls/controls.json").read_text(encoding="utf-8"))
    for name, expected in oracle["role_controls"].items():
        assert role_control_result(controls["cases"][name], role_fields) == expected
    for name, case in controls["schema_cases"].items():
        assert role_control_result(case, role_fields) == "UNREVIEWED", f"Invalid role schema/state accepted: {name}"
    missing_base = json.loads((fixtures / "inputs/baseline-controls/basis.json").read_text(encoding="utf-8"))
    assert missing_base["base"] is None and missing_base["included_commits"] is None
    assert missing_base["kind"] == "synthetic-missing-base-control-not-actual-git"
    assert oracle["baseline_control"]["origin"] == "UNKNOWN"
    assert "F-LEGACY OPEN" in (raw / "prior-findings.md").read_text(encoding="utf-8")
    check_customer_readiness_packet(fixtures)
    return ["JA/VI exact seven-H2 templates and required-field/version/order negative gates",
            "shared protocol/license links and eleven inline role fields",
            "raw byte hashes, cumulative diff and separate head/index/dirty inventory verified",
            "shared regression/new caller/protective guard/pre-existing/Low AC/DB source controls intact",
            "missing-base/missing/empty/malformed/zero-candidate/independence controls isolated from scorer",
            "new blind packet byte integrity and guard/contract/independent closure/write/engine raw controls",
            "structural and synthetic controls only; no agent recall/runtime/DB/release proof"]
