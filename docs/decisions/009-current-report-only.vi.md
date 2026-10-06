# 009 — Chỉ giữ report hiện hành

> Layout và quy tắc tổng hợp hiện hành được thay bởi [quyết định 010](010-readable-execution-report.vi.md). Nội dung phiên bản bên dưới là lịch sử.

Ngày: 06/10/2026. Trạng thái: đã được người phụ trách xác nhận.

Người phụ trách chọn **Chỉ giữ report hiện hành**, yêu cầu xóa asset legacy, archive, template cũ và bản runtime sao chép trong Test Spec; cập nhật các phần liên quan, sau đó push `main` của `blend-kit` và `blend-context`. Đây là thay đổi phạm vi hỗ trợ được xác nhận, không chỉ dọn cache.

Chỉ giữ `test-report@2.4.0`, dùng cặp asset JA/VI tại `skills/blend-generate-test-spec/assets/test-report-block-template.{ja,vi}.xlsx`. Sinh, kiểm và cập nhật kết quả dùng cùng bố cục hiện hành; workbook cũ bị từ chối mà không ghi lại. Bỏ asset legacy, bản customer trùng, archive workbook và công cụ migration. Plugin chuyển sang `2.0.0` vì bỏ khả năng hỗ trợ workbook cũ; việc này không tự tạo tag hoặc release.

Source mới vẫn dùng `test-cases@1.3.0`. Parser giữ khả năng đọc các grammar nguồn 1.0–1.2, gồm RC-0011.1, mà không đổi IDs, kỳ vọng, literal hoặc gaps. Khả năng đọc nguồn cũ không đồng nghĩa hỗ trợ workbook cũ hoặc cho phép viết lại nguồn.

RC-001 được bàn giao với 216 TC, 569 trường hợp **Chưa thực hiện**, Thực tế và thông tin lượt chạy để trống, không có ảnh minh chứng. Giữ nguyên dữ liệu, kỳ vọng, fixture IDs và giới hạn readiness/oracle; không chạy lại ứng dụng trong đợt cleanup. Tài liệu Test Spec dùng plugin đã cài thay vì giữ bản helper/runtime riêng.

Các điều khoản giữ asset/dispatch workbook cũ trong quyết định 003–008 đã được thay thế bởi quyết định này. Nội dung quyết định cũ chỉ giữ vai trò lịch sử. File/snapshot đã bỏ có thể tra trong lịch sử Git; chúng không phải dependency hiện hành.

Giữ các quy tắc bố cục, ảnh viewport, note góc trên phải, highlight không chồng và kiểm ảnh thực của quyết định 008. XLSX không chứng nhận hành vi Google Sheets; chuyển đổi cần quyền riêng và kiểm native. Yêu cầu push của người phụ trách là quyền xuất bản cho phạm vi cleanup/cập nhật này, không cấp quyền sửa ứng dụng, dữ liệu hoặc chạy automation.
