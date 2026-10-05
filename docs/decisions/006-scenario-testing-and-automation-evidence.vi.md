# 006 — Test Spec theo scenario và evidence automation cùng TC

> Historical record. Workbook compatibility/asset retention clauses are superseded by [decision 009](009-current-report-only.vi.md); they do not describe current support.


Ngày: 05/10/2026, Asia/Saigon. Trạng thái: hướng workflow được người phụ trách duyệt; schema và hợp đồng implementation được chốt tại quyết định này. Kiểm chứng runtime/native và quyền phát hành là các phạm vi riêng.

## Vấn đề và căn cứ

Một hành vi xuất hiện trong nhiều TC nhỏ theo loại FUNC/UI/DATA làm lặp chuẩn bị, thao tác, Expected và ảnh. Gom ID đơn thuần lại tạo TC lớn nhưng không cho biết nhánh/checkpoint nào lỗi. Runtime report 2.0.0 chỉ cho image anchor vào vùng một hàng đã dự trữ; chèn hàng hoặc thêm sheet Evidence không giữ hợp đồng checker. Probe MCP hiện hữu đã tái hiện ref cũ trên hidden node trùng ref mới, khiến screenshot báo Saved nhưng thiếu highlight. Không nâng MCP là ràng buộc đã chốt.

## Quyết định

Áp dụng [hợp đồng dùng chung](../../shared/automation-testing.md) cho generator, report và skill mới `blend-automation-test`. Một TC có một mục tiêu; shared setup/Steps viết một lần, variants dựng/reset độc lập và có oracle riêng theo checkpoint. Việc gộp/bỏ TC độc lập bắt buộc có mapping nghĩa vụ/nhánh/ID cũ; không đặt quota số TC hay bỏ nhánh quyền, lifecycle, nguồn, writer và định dạng xuất có khả năng lỗi độc lập.

Output mới dùng `test-cases@1.2.0` và `test-report@2.1.0`. Variants có Inputs/Action delta; Expected trỏ `@Checkpoints`. Checkpoints chứa Variant/Checkpoint/Step/Stage/Expected/Focus/Artifact để ghi oracle cụ thể một lần. Mỗi variant có Actual/Status riêng; checkpoint observation gắn ID trong Actual. Checkpoint không trở thành testcase giả hoặc denominator mới.

Report chỉ có Tổng quan/Overview và Testcases; nhiều ảnh nằm ngay dưới variant/checkpoint tương ứng, trong evidence area nhiều hàng. Cho phép nhãn ảnh có ý nghĩa tại vùng đó. Raw/annotated và file xuất giữ trong output local theo feature/Run ID; run-summary là ledger, không là bản report kết quả thứ hai. Một report authoritative cho mỗi run.

Mọi screenshot raw/annotated gọi full-page, viewport mặc định 1920×1080. Ảnh được đưa vào report bắt buộc highlight đúng vùng/đủ assertion, note tiếng Anh có nghĩa và được mở kiểm pixels. Full-page không chứng minh mọi vùng cuộn nội bộ. Chụp bổ sung full-page theo state/scroll nếu cần; không tự fallback viewport-only. Workaround ref collision chỉ xử lý metadata tạm, cleanup sau capture và kiểm lại.

## Tác động, tương thích và trade-off

Quyết định này thay phần layout/case output mới của [005](005-tc-block-report.vi.md): checkpoint riêng, nhiều hàng ảnh và nhãn ảnh được phép. Các invariant hai sheet, identity, no-overwrite, count eligibility, bảo toàn literal, privacy và expected/readiness/execution độc lập vẫn giữ. Không áp dụng ngược lên report cũ.

Source 1.0.0/1.1.0 vẫn chiếu/check bằng report 2.0.0 và schema gốc; giữ resource legacy đúng bytes. Đổi metadata không là migration. Report RC-001 hoặc Google Sheets có history chỉ được chuyển khi có yêu cầu riêng, mapping/backup và kiểm đủ evidence; quyết định này không sửa chúng.

Source legacy chưa có checkpoint ID. Intake/ledger được đặt nhãn capture riêng của run, ví dụ `legacy-step-2-assertion-1`, và map về đúng step/assertion gốc với Expected nguyên vẹn. Case inline dùng `legacy-assertion-1` cùng source anchor/assertion nguyên văn. Nhãn này chỉ đi vào identity/archive evidence, không thêm checkpoint thiết kế hay denominator và không sửa source/report. Python writer legacy chỉ ghi Actual/Status; chèn ảnh cần capability native/manual đã kiểm và phải nằm trong capacity một hàng gốc. Thiếu chỗ được ghi thành giới hạn evidence, không tự chèn hàng hoặc yêu cầu migration để thực hiện archive.

Full-page có thể rất dài và thiếu vùng virtualized/horizontal. Nhiều ảnh làm report dài hơn; ưu tiên ảnh rộng, xếp dọc và nhóm theo checkpoint thay vì ép nhỏ. Các nhánh kỹ thuật dùng lane thích hợp và file/inspection proof, không ép ảnh UI chứng minh DB/performance. Artifact/tool/package success không chứng minh kết quả nghiệp vụ hoặc native Sheets.

## Kiểm chứng cần có

Review các ví dụ `<`/`≤`, cancel/confirm deletion, incomplete rule/stale form và AND all-positive/single-negative để giữ từng oracle độc lập. Legacy dispatch phải giữ fixture cũ. Report mới cần >=3 ảnh trong một variant và TC sau đó không overlap; save/reopen/check binding và kiểm trực quan. MCP probe full-page phải tái hiện/sửa ref collision và kiểm cleanup. Native Sheets cần proof riêng trên report disposable được phép; thiếu quyền/capability phải ghi đúng phần chưa nghiệm thu. Quyết định đã chốt hướng thiết kế; các proof này chưa được suy thành Passing từ nội dung tài liệu.

## Bổ sung đã duyệt — template compact ngày 05/10/2026

Người phụ trách duyệt proposal/mockup compact với “approve, update đi”. Source mới dùng `test-cases@1.3.0` chiếu `test-report@2.2.0`: Expected tổng thể một block/TC; Steps chỉ Step/Action; Variants giữ bốn cột với final Expected cụ thể mỗi nhánh. Một Reset, điều kiện/data quyết định và thao tác ngắn nằm ở core. Metadata, chuẩn bị/reset fixture và checkpoint oracle/focus giữ ở technical rows mở rộng của TC; criterion/Actual/Status luôn đọc được. Không lặp Expected/bảo toàn từng bước, copy toàn fixture hoặc quota ảnh/checkpoint mỗi click.

Matrix report 2.2 dùng A=variant, B:C=final Expected, D=Actual, E=Status unmerged. Blank Actual/hàng gọn; empty evidence một nhãn gọn với near-zero reserved height. Text populated grow đọc được; ảnh accepted chỉ grow owned area, giữ pixels/tỷ lệ/nhãn đúng, ảnh dày xếp dọc. Full-page raw/annotated, highlight chính xác, note tiếng Anh, pixel review thật, count/identity/literal/atomic/preservation/dedup/writeback guards vẫn bắt buộc.

Trade-off: chi tiết kỹ thuật cần mở nhóm hàng để xem; core giữ toàn tiêu chí tổng thể/kết quả và checkpoint cần proof không bị bỏ. Giữ nguyên source 1.2.0→report 2.1.0, source 1.0.0/1.1.0→report 2.0.0 cùng grammar/resource bytes; không relabel hoặc migration report có history. Scope/data vẫn1.0.0. Schema/projection/XLSX checks và render/recalculation chỉ chứng minh template trong phạm vi đã kiểm; native collapsed images/conversion và ứng dụng/live-provider cần bằng chứng riêng. RC-001 import/test trước đó vẫn dừng; thay template không cho phép khởi động lại.
