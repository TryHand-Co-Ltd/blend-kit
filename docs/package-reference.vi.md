# BLEND Kit — Tham khảo package và lịch sử kiểm chứng

Tài liệu dành cho người bảo trì. Cách cài và dùng nằm trong [README](../README.md). Các candidate dưới đây là những mốc kiểm chứng riêng; tên `v6` không phải version plugin đã phát hành trên marketplace.

## Private marketplace package hiện hành

Plugin hiện hành là `blend-kit@tryhand-blend-kit`, version `2.1.0`, được generate tại `dist/plugins/blend-kit`. Ba catalog dùng cùng package này:

- Codex: `.agents/plugins/marketplace.json`.
- Claude Code: `.claude-plugin/marketplace.json` và manifest package `.claude-plugin/plugin.json`.
- Cursor: `.cursor-plugin/marketplace.json`; package dùng portable Agent Plugin `plugin.json`.

```powershell
pwsh -File scripts/build-plugin-package.ps1 -Python python
pwsh -File scripts/check-plugin-package.ps1
```

Source hiện tại đăng ký 6 skills, gồm `blend-automation-test`, version `2.1.0`. Số files/digest lấy từ build/check thực tế của package canonical, không đưa digest của chính package trở lại source để tạo chu kỳ build. Các candidate profile bên dưới là lịch sử/manual distribution và không thay plugin version.

## Build từ source

Chạy từ thư mục `blend-kit`, bằng Python 3.10+ đã có sẵn. Chọn output mới trong thư mục tạm riêng khi source thay đổi; không tạo thêm candidate trong `dist/`:

```powershell
$outputPath = Join-Path ([IO.Path]::GetTempPath()) ('blend-kit-profiles-' + [guid]::NewGuid())
python scripts/build-kit.py --source . --output $outputPath --profiles codex cursor claude --check
python tests/test_kit.py --area all
```

Builder dùng stdlib, không install hoặc activate. Nó từ chối cây output có file khác bytes hoặc file ngoài inventory; không xóa cây cũ. Khi chỉ nhận gói đã build, member không cần có source để chạy các helper đã đóng gói.

Đóng gói đúng candidate bằng Python stdlib để giữ các thư mục bắt đầu bằng dấu chấm. Ví dụ sau dành cho maintainer, chạy ở kit root; không ghi đè ZIP đã có:

```powershell
$zipPath = Join-Path ([IO.Path]::GetTempPath()) ('blend-kit-profiles-' + [guid]::NewGuid() + '.zip')
if (Test-Path -LiteralPath $zipPath) { throw 'ZIP đã tồn tại; chọn tên mới.' }
python -m zipfile -c $zipPath $outputPath
if ($LASTEXITCODE -ne 0) { throw 'Tạo ZIP không thành công.' }
```

Trước khi gửi, giải nén thử và kiểm đủ ba profile/sáu skill; không đưa toàn bộ `tests/results`, `archive`, environment Python, cache hoặc cấu hình máy vào gói. Digest cây resource bên dưới không phải SHA256 của ZIP; cung cấp SHA256 riêng của ZIP thực tế qua kênh phân phối của team. Không có GitHub URL, tag phát hành hoặc marketplace ID được giả định từ tên folder.

## Source và resource base

Chỉ giữ cặp asset gốc `skills/blend-generate-test-spec/assets/test-report-block-template.{ja,vi}.xlsx`, family `test-report@2.5.0`. Không còn asset `customer/`, `legacy*`, archive workbook hoặc runtime migration. Source mới dùng 1.3.0; parser vẫn đọc nguồn1.0..1.2 mà không sửa IDs, grammar, kỳ vọng hay gaps. Mọi nguồn được hỗ trợ đều dùng report2.5; workbook phiên bản cũ bị từ chối mà không ghi lại. Các snapshot đã xóa có thể tra trong lịch sử Git, không phải dependency hiện hành.

Hợp đồng [automation-testing](../shared/automation-testing.md) được bundle trong cả sáu consumers. Generator dùng nguồn `test-cases@1.3.0`: Expected tổng thể cụ thể, bảng Steps chỉ có thao tác, một Reset và Expected cuối riêng từng variant; checkpoint chỉ giữ mốc quan sát/capture cần thiết. Customer report2.5: exactly two sheets; material conditions/actions/branch Expected and Actual/Status remain visible; human description precedes stable code. Only embedded images expand in one initially collapsed group per TC; title above each vertically stacked image, no evidence URLs and no blank reserve. No preparation label/review notes/default technical appendix; readiness/oracle/rights/eligibility stay internal. Runtime report parser/model/block/export/check/update được lấy từ một nguồn canonical. Automation nhận bản runtime dưới `_kit/skills/blend-generate-test-spec/scripts/` cùng dependency declaration; writer có bản byte-identical của `run_artifacts.py` ngay cạnh để kiểm EvidenceRecord. Các link source tới writer được rewrite theo inventory khai báo; không yêu cầu sibling skill đã cài hoặc cache trên workstation. Generator cũng bundle validator cạnh writer. Chỉ cặp asset report2.5 canonical được đóng gói trong các consumer cần report.

Chạy `tests/test_kit.py --area automation` để kiểm các controls synthetic về archive/execution/writeback; `--area package` kiểm relocation, helper closure, version dispatch và preservation. `tests/scenarios.json` đăng ký replay semantics với raw inputs/scorer; fixture success không là actual agent, browser pixels, native Sheets hay release proof. Output cần đúng một report authoritative, nhiều ảnh ngay cùng TC, English content/note và `full_page=false` (viewport default; full page only for necessary whole-layout proof), top-right note and minimal non-overlapping highlights; skill không đổi server MCP hoặc cấu hình của nó. Grouping/ảnh trên native Sheets cần kiểm riêng ở file live khi được phép; XLSX không chứng minh native collapse. Thay đổi template này không tiếp tục migration/import/test RC-001 đang dừng.

Source duy nhất là `skills/` và `shared/`; template registry source có paths relative tới package root chứa hai thư mục đó. File validation-report template nằm ở `assets/`. Các bản `dist` là generated copies, không chỉnh sửa trực tiếp.

Style report2.5: ngoài bảng trường hợp căn giữa theo chiều dọc; trong bảng căn trên-trái, khoảng cách trên 4 px. XLSX dùng hàng `matrix_padding` 3 pt trước mỗi hàng kết quả logic, không thêm trước phần Expected nối tiếp; không padding bằng newline. Tổng quan dùng tiêu đề plain text với hyperlink toàn ô; nội dung vẫn bold từ khóa chọn lọc.

Native conversion giữ nguyên coordinates của binding: ẩn hàng `matrix_padding` XLSX rồi áp dụng padding thực 4 px trên/dưới, 8 px hai bên. Ảnh phải nằm trong ô để thu/mở cùng hàng; floating image không đạt. Link nội bộ dùng công thức `HYPERLINK("#gid=<detail-tab>&range=<target>"; "<caption>")` trên toàn ô, với separator đúng locale live. Phải kiểm computed link và bấm theo đến đúng TC; màu xanh/gạch chân hoặc `textFormat.link` không đủ chứng minh navigation. Conversion không chạy ứng dụng, nghiệm thu hoặc tự đồng bộ hai report.

Mỗi emitted skill có `SKILL.md`, own resources và `_kit/`. `_kit/shared/` chứa workflow/registry, common review policy, canonical behavioral protocol, exact MIT license và `scripts/artifact_gate.py`; `_kit/skills/<skill>/assets/` chứa dependency templates; `_kit/assets/` chứa validation template. **Registry runtime paths có prefix `_kit/` và được resolve từ thư mục chứa emitted `SKILL.md`**, không từ cwd hoặc application root. Markdown links được rewrite tới tài nguyên bundled; legacy artifact-review references vẫn resolve tới common resources. Helper nguồn dùng package root; helper bundled tự resolve owner root từ location của nó và exact registry assets. Resource duplication trong dist giữ từng skill self-contained; không tạo policy/template source thứ hai, second independent HSR body hay nested SKILL entrypoints. Package không cần source-parent checkout hoặc tests để resolve resources.

Candidate customer report lịch sử từng đặt ở `dist/customer-report-candidate-v2`, 642 files/digest `819f02a9ef6050b04126ae3a7d26c5f1af97d1a7e6c5c7b100e5a4550a776319`. Candidate đầu `dist/customer-report-candidate` từng có 642 files/digest `483ab338905288a3bb4011d823814dc1992bfbe9ca614aa6c1df695aafb86b6c`; actual blind-review/semantic evidence đã chạy thuộc candidate đầu này. Các cây candidate đã bỏ khỏi working tree, bytes lịch sử được tra trong Git. V2 sửa customer exporter về URL privacy, bug-link access và bảo toàn text; source review policy/templates không thay đổi, nhưng điều đó không chứng minh universal agent parity của V2. Không repin proof cũ để chứng nhận toàn candidate mới. Xem [decision 003](../docs/decisions/003-customer-report-and-team-rollout.vi.md) về lịch sử và rollout; [decision 004](../docs/decisions/004-unified-test-report.vi.md) thay hướng hai workbook cho output mới, giữ policy review và giới hạn quyền thao tác.

Exporter của Test Spec nằm ở `scripts/export_report.py` trong emitted skill, load workbook asset từ chính location của script. Nó dùng stdlib và `openpyxl>=3.1.2,<4` đã được khai báo trong `requirements.txt`; user/agent phải resolve interpreter có dependency trước khi gọi, không tự install. Runtime Python chỉ build/check được chưa chắc export được workbook. Exporter hỗ trợ workbook VI mặc định và JA theo yêu cầu rõ; dùng `--language ja` với bộ Markdown JA. Kiểm tra ảnh cần `Pillow>=12.3,<13` đã khai báo; runtime đã kiểm phiên bản 12.3.0, không cài dependency như hệ quả. Artifact gate và builder chỉ cần Python stdlib.

Không đọc hoặc đóng gói file khóa Office bắt đầu bằng `~$`. Không ship source application/context, feature snapshots, fixture inputs/oracles, tests/results, plans, credentials, private configs, node_modules hoặc active agent settings. Canonical Bug Hunter license giữ exact bytes trong mọi emitted skill; compatibility license notice của Review Artifacts được bảo toàn.

## Workflow và kiểm tra artifact

Code Review kế thừa intended approved scope rồi pin actual base/head/merge-base và relevant working bytes; plan file list không chứng minh diff. Đọc toàn assigned changes và named consumers cần thiết; unread scope/unknown baseline phải hiện Partial/Needs evidence. Common review policy tách scope, origin, severity, confidence, completion effect; OOS introduced/worsened regression vẫn có thể block, old lines không tự là pre-existing. DB/migration checks theo thay đổi thực tế và facts đã kiểm; source review không chứng minh live schema/data, online-DDL duration hoặc release readiness.

Hai reviewer dùng [common policy](../shared/review-policy.md) và [pinned Hunter/Skeptic/Referee protocol](../shared/bug-hunter.md). Chỉ claim actual distinct native roles khi đã chạy; unavailable/prohibited delegation dùng disclosed local sequential passes (`independent: false`) hoặc UNREVIEWED nếu independence bắt buộc. Missing/malformed role output không là no-candidates/clean scan. Không Fixer, app tests, SQL, setup hoặc publication tự động.

Trước khi báo output hoàn tất, chạy [artifact gate](../shared/scripts/artifact_gate.py) trên mỗi Markdown thực sự đã lưu, với type/language/filename đúng registry. Gate đọc exact asset và kiểm family/version, H2 order, labels và **cách trình bày đã quy định trong asset**: summary inline phải có nội dung ngay cạnh label; slot block/list phải giữ nội dung phía dưới. Không đổi label/heading bằng cách thêm chú thích trong tên. Details/table phía sau không thay summary inline; scoped no-findings/no-open-questions/no-shared-fixtures chỉ thay entries được template cho phép, vẫn giữ required sections có ý nghĩa. Chạy lại sau chỉnh sửa cuối. Gate thiếu capability hoặc thất bại giữ output Draft/Blocked và BranchResult chưa hoàn tất; không tự coi planned checks là Complete.

```text
python shared/scripts/artifact_gate.py check --type implementation-plan --language ja --file <actual-saved-file> --filename plans/<scope>-implementation-plan.ja.md
python shared/scripts/artifact_gate.py capture --root <verified-input-root> --file <selected-root-relative-file> --file <another-selected-root-relative-file>
```

`capture` chỉ đọc từng file được chọn rõ và xuất SHA256/size của raw bytes ra stdout; giữ BOM/newlines trong identity, không tạo manifest, không enumerate inputs bổ sung. Capture source/context/confirmation/code/working bytes liên quan theo root đã xác minh, rồi đối chiếu identities với đúng scope/revision đã được duyệt. Receipt bị từ chối khi phát hiện drift ở root/ancestors/path components hoặc file đã mở trước/trong/sau lần đọc; thao tác này không khóa nguyên tử toàn bộ cây thư mục và không bảo đảm ngăn mọi concurrent mutation. Receipt chứng minh bytes đã đọc, không chứng minh approval, source authority, độ đầy đủ hoặc origin. Thiếu baseline tương đương giữ origin UNKNOWN và nêu evidence gap; không bịa hash, receipt, người/role/ngày duyệt hoặc phê duyệt giả. Legacy inputs giữ schema/bytes gốc; gate hiện hành chỉ áp dụng newly authored outputs. Source semantics, applicability của conditional sections, bilingual meaning, review disposition và workbook/SQL vẫn cần checks riêng.

## Các candidate lịch sử đã kiểm chứng

Các cây generated lịch sử bên dưới đã được bỏ khỏi working tree theo yêu cầu cleanup. Tên đường dẫn, số file và digest mô tả revision đã kiểm chứng, có thể tra trong lịch sử Git; chúng không phải đường dẫn hiện hành. Chỉ `dist/plugins/blend-kit` là package generated được giữ hiện tại. Package tests kiểm runtime/resource closure hiện hành và cặp asset report2.5 canonical, không yêu cầu snapshot cũ hoặc legacy assets.

`dist/codex`, `dist/cursor`, `dist/claude` từng là release lịch sử ba skill, có 297 files/digest `3ef339d94abaed5326547a78dc8c4c0403d54bcd4209852c50905625770ce6a3`. `dist/five-skill-candidate` từng có 564 files của candidate trước. `dist/ja-quality-candidate` từng có 597 files/digest `e87978912723258301b153b51cb24e22c55ba7a1dc5d2efc0eaa15487e2d7ff9`, đã được dùng cho bốn actual runs; kết quả đó gắn với candidate e879. `dist/ja-quality-candidate-v2` từng có 597 files/digest `94c9e075f6db1841796c92d9a7e74d97b5e2c6a80c1268dd5e50eea260e2c41b`. Candidate lịch sử `dist/ja-quality-candidate-v3` kiểm riêng từng finding/fixture/bảng RoleDisposition dọc và từ chối captured identity khi phát hiện path drift; bảng RoleDisposition ngang đủ 11 cột theo protocol vẫn hợp lệ. Bằng chứng từ candidate trước không tự chứng minh v3. Source khác bytes phải chọn output tạm mới, không overwrite gói hoặc snapshot cũ. Package controls kiểm closure/relocation/profile bytes, helper source/bundle từ cwd khác, capture raw bytes và preservation; actual runtime samples của năm skill là bước riêng.

Candidate profile lịch sử tại `dist/unified-test-report-candidate-v6` có 609 files/digest `e081363a20fb8164719212ed5854eff2089cd4abe33200589f7fc0db34269c77`. So với v5, chỉ report model, checker và hướng dẫn thay đổi trong ba profile (9 bản resource); 600 file còn lại giữ nguyên, không thêm/bớt resource. Bản sửa UTR-REV-01 giữ nguyên toàn bộ token URL tới whitespace, đối chiếu quyền truy cập theo URL đầy đủ và ngăn phần đuôi URL bị coi thành lý do lỗi. Hướng dẫn bổ sung thao tác xóa bộ lọc/hiện dòng cột trước khi kiểm tra; không nới guard hoặc đổi schema, asset, renderer hay dependencies.

Candidate số liệu trước tại `dist/unified-test-report-candidate-v5` có 609 files/digest `d9a28811c7e6a25b8cddd337d98ec13333b2b71c5723ff3e33fda46864594844`. So với v4, 84 bản resource thay đổi gồm asset, helper metric/identity và hướng dẫn liên quan; 525 resource còn lại giữ nguyên bytes, không thêm/bớt resource. Bốn helper và hai asset đóng gói khớp chính xác snapshot source của kiểm chứng native JA/VI v5b; việc đối chiếu bytes không tự thay thế kết luận của Verify Gate. Công thức workbook và checker dùng cùng điều kiện ghi nhận Đạt/Không đạt: Confirmed + Ready, actual không rỗng sau trim Unicode, trạng thái đúng nhãn và dòng đầu bằng chứng là token https:// độc lập. Các dòng sau ghi lý do/bước tiếp theo. Đây là số kết luận đã ghi nhận; kiểm quyền truy cập và riêng tư vẫn độc lập. Nhãn tổng hợp nêu đúng mẫu số; tất cả kịch bản bị bỏ qua giữ SKIPPED, kết hợp PASS/SKIPPED là chưa đủ kết luận, không thêm trạng thái nhập. Identity trùng khi so sánh không phân biệt hoa/thường bị từ chối, không tự đổi ID.

Candidate quyền riêng tư trước tại `dist/unified-test-report-candidate-v4` có 609 files/digest `e5f7588fe219c85cd215fc95b06b494d555e22854f3e166f41fe94bccfb65312`. So với v3, 45 bản resource thay đổi gồm cặp asset JA/VI cùng checker, renderer và hướng dẫn; 564 resource còn lại giữ nguyên bytes, không thêm/bớt resource. Template và workbook mới bật quyền riêng tư cấp workbook `filterPrivacy=1` tương ứng RemovePersonalInformation của Excel, không đổi thiết lập toàn máy. Checker vẫn kiểm nội dung file thực tế, toàn bộ XML attributes/namespaces và locator đã giải mã; cờ này không bảo đảm file sạch. Renderer điều chỉnh bố cục Chi tiết tiếng Nhật để nội dung dài hiển thị ở kích thước mặc định. Binary printer settings do Excel thêm vẫn chưa được hỗ trợ kiểm riêng tư và bị từ chối; không tự xóa, sanitize hay nới guard.

Candidate tương thích Excel trước tại `dist/unified-test-report-candidate-v3` có 609 files/digest `b3e07d63c9ae0a7b478e61743e5e4da4735d56e861afc4c1fc81e2c57d74f673`. So với v2, chỉ checker và hướng dẫn tương ứng thay đổi trong mỗi profile; 603 resource còn lại giữ nguyên bytes, không thêm/bớt resource. Checker chấp nhận cách Excel bỏ dấu nháy tùy chọn quanh đúng tên sheet đơn giản đã biết, bên ngoài chuỗi literal; thay đổi hàm, vùng tham chiếu, ID hoặc giá trị vẫn bị từ chối. Ước lượng chiều cao theo độ rộng được trả thành ghi chú cần xem trực quan; chiều cao tối thiểu theo dòng/font và dòng bị ẩn vẫn được kiểm bắt buộc. Đây là sửa checker cho workbook đã lưu bằng Excel, không sửa generator, model, renderer, asset hoặc workbook kết quả.

Candidate UTF-8 trước tại `dist/unified-test-report-candidate-v2` có 609 files/digest `09117a9d91a92cdcf6cfc94a8880659145a02142aef8387b5f61c4232a05e281`. So với bản đầu, chỉ hai report CLI và hướng dẫn UTF-8 thay đổi trong mỗi profile; không thêm/bớt distributed resource, không thay schema, công thức, renderer hoặc asset. CLI nhận stdin và xuất stdout/stderr theo UTF-8 ngay cả khi Windows dùng codepage cũ; caller encode/decode UTF-8 rõ ràng, không cần đổi biến môi trường hay thiết lập terminal toàn máy.

Candidate đầu tại `dist/unified-test-report-candidate` từng có 609 distributed files/digest `99c549d3ff767486c0485802a2cdf3ab889188f5c61ed9fa9ed3a53573ff9aa8`. Ba file cache Python phát sinh khi kiểm chứng runtime được giữ riêng như byproducts, không phải distributed source. Bằng chứng v1 vẫn gắn với đúng bytes đó và không tự trở thành chứng nhận v2.

## Giới hạn bằng chứng

Package validation kiểm cấu trúc, resource closure, portability và byte parity. Structural/profile parity không là behavioral parity. Codex, Cursor và Claude phải chạy actual scenarios rồi đánh giá nghĩa vụ/ngoại lệ/expected/coverage theo cùng oracle; discovery thành công hoặc IDE có sẵn không thay actual Agent execution. Images và validation reports ba skill hiện có là historical evidence, không chứng minh hai skill mới; actual samples của expansion còn phải được ghi riêng trước khi claim compatibility hoặc parity.

Hiện không coi Cursor IDE hiện diện là Agent executor đã kiểm chứng. Nếu runtime executor, permissions, workbook render hoặc recalculation không khả dụng, ghi Blocked/chưa kiểm chứng trong validation report; không claim PASS và không tự cài/login. Test Spec exporter success cũng không chứng minh rendered usability hoặc formula recalculation.
