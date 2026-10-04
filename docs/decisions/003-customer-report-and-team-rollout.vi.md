# 003 — Báo cáo khách hàng riêng và rollout có phạm vi

## Status

Accepted — thiết kế được duyệt ngày 2026-10-03; plan và Parallel được chọn ngày 2026-10-04. Quyết định này bổ sung [001](001-blend-kit-workflow.vi.md) và [002](002-research-planning-code-review.vi.md); không thay thế schema/proof lịch sử hoặc cấp quyền active cutover/publication.

## Căn cứ

[Design 000006](../plans/2026-10-03-000006-customer-test-report-and-team-readiness-design.vi.md) D1–D4/R1–R10 và [plan 000007](../plans/2026-10-03-000007-customer-test-report-and-team-readiness-plan.vi.md). Workbook nội bộ cần traceability chi tiết; khách hàng chỉ nhận báo cáo đã đóng run nên cần đường đọc ngắn, độc lập và không lộ nội dung local.

## Quyết định

| Quyết định | Nội dung và lý do |
| --- | --- |
| D1 — bản final riêng | Giữ nguyên master/design/history; export bản customer theo requested language để giảm nội dung nội bộ mà không mất traceability gốc. |
| D2 — giữ tồn đọng | Cho phép FAIL/BLOCKED/SKIPPED với lý do, lỗi và phạm vi chưa kiểm; đóng run không biến thành whole-feature PASS. |
| D3 — evidence dùng chung | Link phải có bằng chứng khách hàng truy cập; ảnh lỗi quan trọng có review/caption. Thiếu access là delivery gap, không quyền upload/share. |
| D4 — đơn giản hóa | Hai sheet mặc định, bảy cột Results; Details chỉ khi material content/ảnh cần. Bỏ Data/setup/research/readiness/hash nội bộ nhưng giữ điều kiện quyết định kết quả. |

## Contract áp dụng

| Requirement | Tác động |
| --- | --- |
| R1 | Master và artifacts cũ bất biến; không regenerate testcase hoặc overwrite run đã thực thi. |
| R2 | File khách hàng đọc độc lập; allowlist nội dung và kiểm toàn XLSX/media để tránh private references. |
| R3 | Giữ trạng thái và tồn đọng thật; không tự chuyển status hoặc claim toàn feature PASS. |
| R4 | Closure/recipient-access xác minh bằng actual observation hoặc human attestation có nguồn; không tự tạo bằng chứng. |
| R5 | Stable Run/Case/Variant, exact expected/actual và counts/denominators tách rõ; no-data không 100%. |
| R6 | Summary/Results mặc định; Details conditional bảo toàn actor/data/steps/preservation/evidence thay vì truncate. |
| R7 | `customer-test-report@1.0.0` có exact JA/VI mappings/assets; working v1 và lịch sử giữ nguyên. |
| R8 | Review tách known contract failure khỏi unknown operational effect; closure độc lập và completeness phải có write/persist/read/consumer evidence. |
| R9 | Migration cần selected local scope, inventory/backup/disable-old/discovery/rollback; không silently activate/global edit/publish. |
| R10 | Không app tests/SQL/live DB/external writes/release như hệ quả của generate/export/review. |

## Tác động và kiểm chứng

Operation `customer-report` thuộc Test Spec hiện có, không tạo skill thứ sáu. Source templates chứa conditional layout nhưng simple output không giữ blank/hidden Details. Builder vẫn stdlib, đóng gói helper/template đầy đủ; workbook runtime dùng declared dependencies đã có. CLI cũ và internal templates không đổi.

Theo [migration guidance](../../README.vi.md#dùng-trên-máy-member), mapping legacy `generate-unit-test` → `blend-generate-test-spec`, `blend-review-task` → `blend-review-artifacts`, và same-name `blend-generate-task` cần kiểm collision. Chưa xác minh marketplace destination/schema thì không invent metadata hoặc publish.

Structural/data/package checks, actual agent semantic outputs, visual/engine proof, native Excel/accessibility, recipient access và real feature pilot là các lớp bằng chứng riêng. Source/candidate mới không chứng nhận ngược historical samples. Missing runtime/completed run/approval/access cần ghi exact gap trong validation report, không tạo proof giả để hoàn tất.

## Khi cần xem lại

Khi template family/schema, source/approval revision, privacy/evidence requirements hoặc runtime discovery thay đổi; khi actual output cho thấy mất điều kiện/oracle hoặc review certainty sai. Chỉnh policy/template phải giữ những artifact đã chạy và tạo candidate/evidence epoch mới.
