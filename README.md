# BLEND Kit

Bộ năm skill dùng chung context, workflow và templates cho dự án BLEND. Member có thể cài theo project và bắt đầu bằng một lượt thử nhỏ.

Source hiện tại dùng `test-report@2.0.0`: đúng hai sheet Tổng quan/Testcases, TC block đầy đủ, trạng thái ở dòng riêng, màn hình cạnh URL tương đối, bốn phần và vùng ảnh/kết quả trống. Case template hiện hành là `test-cases@1.1.0`; nguồn 1.0.0 lịch sử còn đọc được nhưng route thiếu phải được xác minh. Các candidate v6 trong `dist/` là gói lịch sử trước cập nhật TC block; không dùng chúng làm bản hiện hành. Build source hiện tại vào một output mới trước khi phân phối. Không tự thay active skills hoặc upload báo cáo.

**Cách cài hiện có:** copy bộ skill đã build vào project. **Private marketplace chưa được phát hành:** chưa có manifest, marketplace URL hoặc plugin ID của BLEND Kit để cài qua giao diện plugin. Hướng dẫn dưới đây dùng package thật đang có, không giả định một marketplace đã tồn tại.

| Bản source đã kiểm | Giá trị |
| --- | --- |
| Report family | `test-report@2.0.0` |
| Nội dung build tham chiếu | 5 skill, 3 profile, 612 resource files |
| Digest của cây package đã kiểm | `536bb2fac845d99b5e96e494cae286d6f40cd404631aa01533afc0445745db00` |

Digest này là identity của resource tree do builder tính, **không phải SHA256 của ZIP**. Nó áp dụng cho source hiện tại được build với đủ ba profile bằng lệnh bên dưới. Repo chưa công bố ZIP/download URL chính thức; nếu nhận package từ maintainer, vẫn phải đối chiếu checksum của chính package được giao.

```powershell
python scripts/build-kit.py --source . --output dist/tc-block-report-candidate-v7 --profiles codex cursor claude --check
```

Output phải là đường dẫn mới, chưa tồn tại. Tên `tc-block-report-candidate-v7` là tên đề xuất cho lần build từ source này; README không khẳng định thư mục đó đã được publish hoặc đính kèm release.

## Cài đặt nhanh

1. Nhận và giải nén package; tìm thư mục chứa trực tiếp `codex/`, `cursor/`, `claude/`. Nếu có toàn bộ source kit, build vào một output mới bằng lệnh trên rồi dùng chính thư mục output đó.
2. Chọn **một profile** và workspace/project sẽ mở bằng agent. Kiểm skill trùng tên trước khi copy.
3. Copy nguyên năm thư mục skill theo bảng và lệnh bên dưới, gồm cả `_kit/`, `assets/`, `references/`, `scripts/`.
4. Chuẩn bị Python/dependencies cho các helper; mở đúng workspace bằng agent.
5. Kiểm tra file, discovery và chạy smoke test. Có file trên đĩa chưa đồng nghĩa agent đã nạp đúng skill.

Các lệnh là hướng dẫn để người cài chủ động chạy. Việc đọc README hoặc build package không tự cài dependencies, thay active skills, sửa global settings hay publish.

## 1. Chuẩn bị

- Codex, Cursor hoặc Claude Code đã cài, đăng nhập và dùng được tính năng skills. Đây là hướng dẫn local; cloud/remote cần cài và kiểm trên chính môi trường chạy agent.
- Quyền đọc `blend-context`, source BLEND và ghi thư mục skill của project đã chọn. Có nhiều checkout thì cung cấp rõ bản cần dùng; không cần dùng tên folder hay ổ đĩa của tác giả.
- Python **3.10+**. Builder/artifact gate chỉ cần stdlib; tạo/kiểm workbook dùng `openpyxl>=3.1.2,<4`, xử lý ảnh dùng `Pillow>=12.3,<13` theo [requirements](skills/blend-generate-test-spec/requirements.txt).
- Các ví dụ shell dùng **PowerShell 7**. Trên macOS/Linux có thể dùng PowerShell 7 với cùng lệnh copy, hoặc copy thư mục bằng file manager theo bảng đích; lệnh Python dùng executable Python 3.10+ của máy.
- Excel hoặc spreadsheet engine để đọc/nhập kết quả và kiểm tra hiển thị. Tạo XLSX thành công không tự chứng minh công thức đã tính lại trong ứng dụng.

Không cần MCP riêng để nạp năm skill. `srcwalk`, graph tools và external research là khả năng tùy host; không tự cài thêm chỉ để đủ bộ. Agent vẫn cần quyền truy cập đúng các nguồn mà task yêu cầu.

## 2. Chọn profile và nơi cài

| Agent | Thư mục lấy từ package root | Thư mục đích dưới project root |
| --- | --- | --- |
| Codex | `codex/.agents/skills/` | `.agents/skills/` |
| Cursor | `cursor/.cursor/skills/` | `.cursor/skills/` |
| Claude Code | `claude/.claude/skills/` | `.claude/skills/` |

Đặt ở root mà bạn thực sự mở bằng agent. Với workspace chứa nhiều repo, không mặc định skill ở coordinator bên ngoài Git root sẽ được nạp khi khởi chạy trực tiếp từ repo con. Kiểm lại nguồn discovery tại đúng nơi làm việc. [Codex local skills](https://learn.chatgpt.com/docs/build-skills) và [Claude skill locations](https://code.claude.com/docs/en/skills#choose-where-skills-load) mô tả phạm vi tìm kiếm theo project và thư mục cha.

**Không copy cả ba profile vào cùng workspace một cách mặc định.** Cursor còn đọc `.agents/skills/` và các thư mục tương thích như `.claude/skills/`; nhiều bản cùng tên có thể gây nhầm nguồn. Nếu Codex và Cursor cùng dùng project, kiểm xem Cursor đã đọc được bộ `.agents/skills/` trước khi cài thêm. Khi dùng nhiều agent mà discovery bị trùng, chọn một nguồn được cả runtime hỗ trợ hoặc tách workspace; không tự tạo junction hay sửa global config để che xung đột. [Cursor skill discovery](https://prod.cursor.com/help/customization/skills).

Bộ này ưu tiên project scope. Cài user scope sẽ áp dụng rộng hơn và phải được chọn riêng; không copy package vào cache/plugin directory do agent tự quản lý.

### Copy lần đầu

Chạy cả block trong cùng một phiên PowerShell 7. Nhập đường dẫn thực tế khi được hỏi; các biến sẽ dùng lại ở những bước sau. Block từ chối ghi đè và từ chối đường dẫn skill qua symlink/junction.

```powershell
$ErrorActionPreference = 'Stop'
$packageRoot = (Resolve-Path -LiteralPath (Read-Host 'Thư mục chứa codex, cursor, claude')).Path
$projectRoot = (Resolve-Path -LiteralPath (Read-Host 'Project/workspace root cần cài')).Path
$profile = (Read-Host 'Profile: codex, cursor hoặc claude').Trim().ToLowerInvariant()
$profileRoots = @{ codex = '.agents/skills'; cursor = '.cursor/skills'; claude = '.claude/skills' }
if (-not $profileRoots.ContainsKey($profile)) { throw 'Profile không hợp lệ.' }
$skillNames = @('blend-generate-task', 'blend-generate-test-spec', 'blend-review-artifacts', 'blend-plan-implementation', 'blend-review-code')
$relativeRoot = $profileRoots[$profile]
$sourceRoot = Join-Path $packageRoot "$profile/$relativeRoot"
$targetRoot = Join-Path $projectRoot $relativeRoot
$packagePrefix = $packageRoot.TrimEnd([char[]]'\/') + [IO.Path]::DirectorySeparatorChar
if ($targetRoot.StartsWith($packagePrefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'Không cài bên trong package nguồn.' }
$partPath = $targetRoot
while ($partPath) {
    if ((Test-Path -LiteralPath $partPath) -and ((Get-Item -LiteralPath $partPath -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "Đường dẫn qua link; xác minh owner trước khi cài: $partPath"
    }
    $parentPath = Split-Path -Path $partPath -Parent
    if ($parentPath -eq $partPath) { break }
    $partPath = $parentPath
}
foreach ($name in $skillNames) {
    if (-not (Test-Path -LiteralPath (Join-Path $sourceRoot "$name/SKILL.md") -PathType Leaf)) { throw "Package thiếu skill: $name" }
    if (Test-Path -LiteralPath (Join-Path $targetRoot $name)) { throw "Đã có $name; dùng mục Cập nhật/rollback trước." }
}
foreach ($oldName in @('generate-unit-test', 'blend-review-task')) {
    if (Test-Path -LiteralPath (Join-Path $targetRoot $oldName)) { throw "Còn skill cũ $oldName; xử lý migration trước." }
}
New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
foreach ($name in $skillNames) {
    Copy-Item -LiteralPath (Join-Path $sourceRoot $name) -Destination $targetRoot -Recurse -ErrorAction Stop
}
Write-Output "Đã copy vào $targetRoot. Tiếp tục kiểm tra bên dưới."
```

Nếu copy bị lỗi giữa chừng, giữ package nguyên vẹn, kiểm các thư mục đã copy và đưa riêng chúng ra khỏi discovery trước khi thử lại. Không dùng `-Force` để merge chồng một bản cài dở hoặc một version cũ. Block trên không kiểm được tất cả nguồn user/plugin của từng agent; vẫn phải thực hiện discovery ở bước 4.

### Kiểm byte sau copy

Tiếp tục trong cùng PowerShell. Kiểm này đối chiếu từng skill với đúng profile đã nhận; nó không xác nhận nguồn tải đáng tin cậy hoặc chứng minh agent đã chạy skill.

```powershell
foreach ($name in $skillNames) {
    $from = Join-Path $sourceRoot $name
    $to = Join-Path $targetRoot $name
    $sourceFiles = @(Get-ChildItem -LiteralPath $from -File -Recurse -Force)
    $targetFiles = @(Get-ChildItem -LiteralPath $to -File -Recurse -Force)
    if ($sourceFiles.Count -ne $targetFiles.Count) { throw "Số file không khớp: $name" }
    foreach ($file in $sourceFiles) {
        $relative = [IO.Path]::GetRelativePath($from, $file.FullName)
        $copied = Join-Path $to $relative
        if (-not (Test-Path -LiteralPath $copied -PathType Leaf)) { throw "Thiếu $name/$relative" }
        if ((Get-FileHash -LiteralPath $file.FullName).Hash -ne (Get-FileHash -LiteralPath $copied).Hash) { throw "Sai bytes: $name/$relative" }
    }
}
Write-Output 'PASS: đủ năm skill và resource bytes khớp package.'
```

## 3. Chuẩn bị Python cho helper

Dùng Python đã có dependencies phù hợp, hoặc tạo venv riêng ở một thư mục mới ngoài các repo. Không cần activate venv hay thay execution policy: luôn gọi executable trong venv.

Các lệnh sau tạo environment và tải packages. Người cài chạy chủ động; nếu giao agent thực hiện, cần yêu cầu rõ việc cài dependencies. Không chạy trong lúc chỉ review tài liệu.

```powershell
$basePython = Read-Host 'Executable Python 3.10+ (python, python3 hoặc đường dẫn đầy đủ)'
& $basePython -c 'import sys; assert sys.version_info >= (3, 10); print(sys.version)'
if ($LASTEXITCODE -ne 0) { throw 'Cần Python 3.10+.' }
$venvRoot = [IO.Path]::GetFullPath((Read-Host 'Thư mục mới ngoài repo để tạo venv'))
if (Test-Path -LiteralPath $venvRoot) { throw 'Thư mục đã tồn tại; chọn nơi mới hoặc dùng interpreter có sẵn.' }
& $basePython -m venv $venvRoot
if ($LASTEXITCODE -ne 0) { throw 'Không tạo được venv.' }
$python = Join-Path $venvRoot $(if ($IsWindows) { 'Scripts/python.exe' } else { 'bin/python' })
$requirements = Join-Path $targetRoot 'blend-generate-test-spec/requirements.txt'
& $python -m pip install -r $requirements
if ($LASTEXITCODE -ne 0) { throw 'Cài dependency thất bại; chưa chuyển sang smoke test.' }
& $python -m pip check
if ($LASTEXITCODE -ne 0) { throw 'Dependency đang xung đột.' }
& $python -c 'import sys,openpyxl,PIL; print(sys.executable); print("openpyxl",openpyxl.__version__); print("Pillow",PIL.__version__)'
```

Nếu dùng interpreter có sẵn, gán `$python` bằng đường dẫn executable đó và chỉ chạy `-m pip check` cùng lệnh import/version, đối chiếu phiên bản với requirements; không tạo/cài lại khi không cần. Cung cấp đường dẫn `$python` cho agent trong phiên làm việc; không ghi đường dẫn máy vào tài liệu dùng chung. Không copy venv sang máy khác hoặc đưa venv vào Git/package.

## 4. Mở agent và xác nhận discovery

| Agent | Cách kiểm tra |
| --- | --- |
| Codex | Mở đúng project. Desktop có thể chọn skill trong composer hoặc yêu cầu bằng tên; trong CLI/IDE dùng `/skills` hoặc `$` để chọn tên; kiểm cả đường dẫn `SKILL.md`. Nếu thay đổi chưa xuất hiện, khởi động phiên mới/restart. [Hướng dẫn Codex](https://learn.chatgpt.com/docs/build-skills). |
| Cursor | Mở **Customize → Skills**, xem skill đã discover; gọi bằng `/blend-review-artifacts` hoặc chọn qua `@`. Kiểm nguồn nếu xuất hiện trùng. [Hướng dẫn Cursor](https://prod.cursor.com/docs/skills). |
| Claude Code | Mở session tại project; dùng `/skills` rồi `/blend-review-artifacts`. Thư mục skill mới chưa được nhận có thể dùng `/reload-skills` trên bản hỗ trợ, hoặc mở session mới. Personal/managed skills cùng tên có thể ưu tiên hơn project, nên phải kiểm nguồn. [Hướng dẫn Claude Code](https://code.claude.com/docs/en/skills). |

Cần thấy đúng năm tên ở mục 5. Một request kiểm discovery, không tạo tài liệu:

```text
Chỉ kiểm tra việc cài BLEND Kit. Liệt kê năm skill BLEND đã discover và đường dẫn SKILL.md thực sự được nạp. Đọc các resource mà chúng tham chiếu trong package, xác nhận resolve được. Không chạy workflow generate/review, không tạo file, không thay settings. Nếu có skill trùng hoặc không có khả năng xác minh nguồn, hãy ghi rõ.
```

Đây là kiểm nạp/resource, chưa là smoke test workflow. Đừng chấp nhận câu trả lời “đã cài” nếu agent chỉ liệt kê tên mà không xác minh nguồn thực tế.

### Smoke test trước task đầu tiên

Kiểm helper từ bản đã cài bằng interpreter vừa xác minh:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1' # Chỉ phiên shell này, tránh tạo cache trong skill.
$testSpecRoot = Join-Path $targetRoot 'blend-generate-test-spec'
$reviewRoot = Join-Path $targetRoot 'blend-review-artifacts'
& $python (Join-Path $testSpecRoot 'scripts/export_report.py') --help
if ($LASTEXITCODE -ne 0) { throw 'Generator không load được.' }
& $python (Join-Path $testSpecRoot 'scripts/check_report.py') --help
if ($LASTEXITCODE -ne 0) { throw 'Checker không load được.' }
& $python (Join-Path $reviewRoot '_kit/shared/scripts/artifact_gate.py') --help
if ($LASTEXITCODE -ne 0) { throw 'Artifact gate không load được.' }
```

Sau đó gọi **Blend Review Artifacts** bằng một bundle nhỏ đã được phép đọc:

```text
Dùng Blend Review Artifacts để review chỉ bundle Test Spec tôi chỉ định. Context root, source root và bundle path tôi cung cấp là phạm vi được phép. Trước khi review, nêu skill/resource đang dùng và căn cứ nguồn. Trả findings trong chat, không tạo report file hoặc sửa tài liệu/code, không chạy application tests/SQL và không publish. Nếu thiếu nguồn quan trọng, ghi giới hạn thay vì đoán.
```

Điền paths/scope thực trước khi gửi. Kiểm tool/file-read evidence: agent đã đọc đúng skill, template, context và phần source liên quan, rồi trả findings có căn cứ. Không dùng prompt không có bundle/identity để giả một lượt chạy thành công. Cài đặt đạt khi **bytes khớp + discovery đúng nguồn + helper load được + một workflow nhỏ thực sự hoàn tất trong phạm vi đã cấp**. Chất lượng toàn bộ năm skill vẫn cần theo dõi qua pilot thực tế.

## 5. Cách dùng năm skill

| Skill | Dùng khi nào |
| --- | --- |
| `blend-generate-task` | Có spec: research context/code, tạo Split Tasks, AC, Q&A; Database Design chỉ khi cần đổi DB. Test Spec chỉ được gọi khi prompt yêu cầu. |
| `blend-generate-test-spec` | Tạo/refresh Test Spec và một workbook JA hoặc VI; nhập kết quả vào chính workbook. Không chạy application tests. |
| `blend-review-artifacts` | Review Task, Test Spec, workbook theo nguồn và template; đề xuất cập nhật. |
| `blend-plan-implementation` | Đầu vào đã duyệt: tạo plan Draft theo feature/task; không tự triển khai. |
| `blend-review-code` | Đã triển khai: review actual diff, luồng liên quan và rủi ro DB/migration; giữ scope/origin và evidence riêng. |

Ví dụ prompt sau khi cung cấp đúng nguồn/identity:

- “Dùng Blend Generate Task cho spec này. Tạo Split Tasks và AC tiếng Nhật/Việt; không tạo Test Spec.”
- “Dùng Blend Generate Task và generate cả Test Spec cho phạm vi này.”
- “Dùng Blend Generate Test Spec độc lập. Tạo bản tiếng Nhật; đọc đúng feature/task đã xác minh.”
- “Dùng Blend Review Code cho base/head tôi chỉ định và plan đã duyệt; report cả lỗi ngoài scope, ghi rõ phân loại.”

Luồng chung: **Generate Task → Review Artifacts → duyệt đúng revision/scope → Plan Implementation → cấp quyền triển khai → Review Code**. Review PASS không thay approval; generate/review không tự cho phép thực thi SQL, publish hay release.

Mở `blend-context/AGENTS.md`, README/rules và feature context tương ứng trước khi làm việc. Skills discover roots từ workspace, paths đã cung cấp và links đã xác minh; không scan toàn ổ đĩa hay tự clone. Shared research và plans nằm ở gốc feature; tài liệu riêng task nằm trong task folder, dùng exact ID/parent. Xem [workflow](shared/workflow.md), [template registry](shared/artifact-formats.md) và [quy tắc review](shared/review-policy.md).

Báo cáo kiểm thử dùng **một template logic JA/VI, một workbook mỗi lượt/ngôn ngữ** và đúng hai sheet: Tổng quan/Testcases. Mỗi TC là block kỹ thuật với nhãn đậm, steps/assertions dạng danh sách, một status/actual/ảnh cho mỗi biến thể. Renderer bỏ marker list của Markdown trước khi thêm đúng một bullet; inline code hiển thị dạng `[identifier]` và giữ nguyên literal bên trong, ví dụ `` `**24` `` thành `[**24]`. Dropdown trạng thái nằm trong một ô compact không merge cạnh nhãn để popup không bị neo ở cuối vùng nội dung rộng. Không có dòng link/chú thích/footer trong block; lý do và bước tiếp theo của kết quả chưa đạt nằm trong actual. Công thức tự cập nhật tổng hợp. Dùng [hướng dẫn báo cáo](skills/blend-generate-test-spec/references/test-report.md) để tạo/kiểm bằng CLI và hiểu giới hạn; không tự tạo attestation để đủ gate.

## 6. Cập nhật, chuyển từ bản cũ, rollback và gỡ

| Tên đang có | Tên mới / xử lý |
| --- | --- |
| `generate-unit-test` | Thay bằng `blend-generate-test-spec` |
| `blend-review-task` | Thay bằng `blend-review-artifacts` |
| `blend-generate-task` | Cùng tên: chọn đúng nguồn để thay, không merge hai version |
| `blend-plan-implementation`, `blend-review-code` | Thêm hoặc cập nhật từ cùng package build đã xác minh |

1. **Dừng các task đang dùng bộ cũ.** Xác định đúng project/profile và nguồn project, user hoặc plugin đang cung cấp mỗi tên. Nếu nguồn là symlink/junction, xác minh đích và owner trước, không di chuyển hay copy đè qua link.
2. **Backup ngoài mọi thư mục discovery.** Sao lưu nguyên từng folder BLEND cần thay, ghi candidate/profile, source path và hash. Không backup dưới `.agents/skills`, `.cursor/skills` hoặc `.claude/skills`: bản backup có thể vẫn bị agent discover. Giữ tài liệu feature, workbook đã chạy và cấu hình không liên quan nguyên vẹn.
3. **Đưa đúng các folder cũ ra khỏi discovery** sau backup, hoặc disable đúng plugin/nguồn bằng cơ chế runtime. Không thay file trong cache do plugin manager quản lý. Với source ngoài scope được cấp, dừng và nhờ owner xử lý; không sửa toàn bộ global config.
4. **Cài bộ mới vào đích trống** theo bước 2, kiểm bytes/dependencies/discovery và smoke test lại. Không dùng copy merge/`-Force` để cập nhật tại chỗ.
5. **Rollback:** đưa đúng năm folder vừa cài ra khỏi discovery, khôi phục nguyên backup vào vị trí cũ, mở phiên mới và kiểm lại source được nạp. Nếu có thay đổi cấu hình đã được cấp quyền, khôi phục đúng phần đó. Không rollback bằng cách ghi đè workbook kết quả.
6. **Gỡ local install:** đưa đúng năm folder đã cài ra khỏi discovery và kiểm lại agent. Giữ backup trước khi xóa vĩnh viễn. Venv riêng có thể giữ hoặc gỡ riêng sau khi xác nhận không còn tác vụ dùng; không gỡ dependencies từ Python dùng chung.

Các thao tác này chỉ áp dụng bản local đã chọn. Plugin cài qua marketplace phải quản lý bằng plugin manager của runtime sau khi có bản phát hành tương ứng.

## 7. Private marketplace

Hiện BLEND Kit **chưa phải plugin marketplace**. `blend-kit` không có manifest phân phối đã xác minh, marketplace URL/ID hoặc version plugin được công bố. Vì vậy README không cung cấp một lệnh install plugin BLEND Kit giả định.

Để có hướng dẫn marketplace chạy được, maintainer cần phát hành package/manifest đúng runtime, cung cấp địa chỉ private marketplace, plugin ID/version, cách cấp quyền repo/account và quy trình update/rollback đã kiểm. Member khi đó chọn đúng nguồn đã được team xác nhận và kiểm lại discovery/smoke test như trên. Không sao chép URL/ID của plugin khác sang BLEND Kit.

[Codex Plugins](https://learn.chatgpt.com/docs/plugins), [Cursor Plugins](https://prod.cursor.com/docs/plugins) và [Claude Code plugins](https://code.claude.com/docs/en/plugins) là tài liệu nền tảng; chúng không chứng minh BLEND Kit đã được publish. Cài local ở trên không đăng ký marketplace hoặc bật plugin trên máy khác.

## 8. Xử lý lỗi thường gặp

| Hiện tượng | Kiểm tra / xử lý |
| --- | --- |
| Không thấy skill | Kiểm đúng project root/profile, đủ `SKILL.md` và resource, session/trust/policy của runtime; mở phiên mới nếu cần. Không copy thêm vào nhiều root để thử ngẫu nhiên. |
| Hai skill cùng tên hoặc hành vi vẫn cũ | Kiểm project/user/plugin và các thư mục tương thích; chọn một nguồn, backup rồi disable đúng bản cũ. |
| Không tìm thấy `_kit`, template hoặc helper | Đã copy thiếu thư mục. Đưa bản cài dở ra khỏi discovery rồi copy nguyên folder, kiểm hash lại. |
| `ModuleNotFoundError` | Xác minh agent dùng đúng `$python` trong venv và requirements của skill. Không sửa Python toàn máy để chữa sai interpreter. |
| `pip`/quyền mạng lỗi | Cài đặt dependency chưa hoàn tất; dùng kênh package của tổ chức hoặc nhờ owner cấp quyền. Không dùng môi trường thiếu deps rồi coi exporter đã sẵn sàng. |
| Output đã tồn tại | Generator cố ý không ghi đè. Với file đã có kết quả, dùng checker; chỉ tạo path mới khi thực sự có lượt/revision mới. |
| Helper báo có file ngoài inventory khi build lại | Cache/runtime byproducts có thể đã xuất hiện. Dùng output build mới; không xóa hoặc ghi đè package đang giữ evidence. |
| Lỗi ký tự JA/VI qua subprocess | Hai CLI dùng UTF-8; caller phải encode/decode UTF-8. Không đổi nội dung dữ liệu để tránh lỗi encoding. |
| Dòng/cột ẩn hoặc filter còn bật | Bỏ filter, hiện đủ dòng/cột, lưu cùng file rồi kiểm lại. Không bỏ guard. |
| Local metadata hoặc privacy flag bị mất | Kiểm chính file đã lưu và editor đã dùng. Không coi file sạch chỉ vì không thấy path trên sheet; không tự sửa hoặc tạo bản khác bằng checker. |
| `printerSettings` binary bị từ chối | Đây là giới hạn kiểm privacy hiện hành. Giữ file, báo gap và nhờ người phụ trách xem; không tự xóa phần ZIP hoặc nới checker để lấy PASS. |
| Không có nguồn/ID/approval hoặc quyền xem evidence | Cung cấp đúng nguồn/xác nhận thực; không bịa scope, hash, kết quả hay attestation. |

## 9. Kiểm chứng và tài liệu tham khảo

Source `test-report@2.0.0` hiện tại đã qua full Blend Kit suite, package build ba profile và native Excel proof hữu hạn cho layout/công thức. Các kiểm tra này chưa chứng minh agent đã cài/chạy trên máy member, quyền xem link thật, native Google Sheets import hoặc feature đã được kiểm thử. Một pilot nhỏ tại môi trường thực vẫn là bước xác nhận cuối của member.

- [Tham khảo package, build, resource layout và lịch sử](docs/package-reference.vi.md).
- [Test suite](tests/test_kit.py) để kiểm registry, generator/checker, JA/VI, package và resource closure từ source hiện tại.
- [Decision TC block hiện hành](docs/decisions/005-tc-block-report.vi.md) và [decision workflow báo cáo trước đó](docs/decisions/004-unified-test-report.vi.md).

Raw runtime transcripts, evaluation outputs và internal execution plans được giữ local, không publish trong repo vì có thể chứa đường dẫn workstation hoặc metadata của môi trường chạy. Các kết luận hiện hành phải được kiểm lại bằng test suite và package build từ source, không dựa vào raw log bị bỏ khỏi bản publish.

Đường dẫn và cơ chế discovery được đối chiếu tài liệu chính thức ngày **2026-10-04**. Tài liệu web có thể thay đổi theo runtime; kiểm nguồn đang nạp và kết quả smoke test trên bản agent thực tế thay vì chỉ dựa vào tên thư mục.
