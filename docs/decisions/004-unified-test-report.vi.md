# 004 — Một workbook kiểm thử xuyên suốt

> Historical record. Workbook compatibility/asset retention clauses are superseded by [decision 009](009-current-report-only.vi.md); they do not describe current support.


Ngày quyết định: 2026-10-04. Trạng thái: hướng và plan đã được người dùng duyệt; kiểm chứng triển khai được ghi riêng.

Căn cứ: thiết kế đã duyệt, implementation plan, D1–D4 và U1–U8.

## Quyết định

Output mới dùng duy nhất family `test-report@1.0.0`, với asset `test-report-template.ja.xlsx` và `test-report-template.vi.xlsx`. Đây là một cấu trúc và vai trò với hai ngôn ngữ. Mỗi lượt/ngôn ngữ được yêu cầu có một workbook; mặc định VI. QA nhập kết quả và sử dụng chính file đó làm báo cáo.

Workbook gồm Tổng quan và Kiểm thử, bảy cột trọng tâm; Chi tiết chỉ chứa nội dung thiết yếu dài hoặc ảnh, liên kết về đúng testcase và không tạo nơi nhập kết quả trùng lặp. Tổng quan dùng công thức từ dữ liệu nhập. Văn phong chính thức, trực tiếp, dễ hiểu ngay từ đầu; hình thức hoàn chỉnh không xác nhận kiểm thử đã hoàn tất.

Generator chỉ tạo file mới từ đúng Test Spec. Checker đọc workbook đã lưu, đối chiếu nguồn và báo thiếu sót, không sửa hoặc tạo bản thay thế. Kiểm tra hoàn tất cần kết quả và xác nhận đóng lượt/quyền xem bằng chứng thực tế. Không bịa người thực hiện, thời gian, kết quả hoặc xác nhận; chưa chạy không là đạt, mẫu số bằng không không là 100%.

## Quan hệ với quyết định trước

Quyết định này thay thế **hướng hai workbook cho output mới** trong [quyết định 003](003-customer-report-and-team-rollout.vi.md). Các quy tắc review, quyền thao tác, bảo toàn dữ liệu và cutover của 003 không thay đổi. Hai family cũ không còn là lựa chọn tạo output trong registry/package mới.

Workbook, dist, output, proof và fixture lịch sử giữ nguyên schema/bytes. Không đổi nhãn proof cũ để chứng nhận schema mới, không regenerate file đã có và không tự migrate RC-001. Migration hoặc lượt kiểm thử mới cần yêu cầu riêng.

## Phạm vi và bằng chứng

Thay đổi giới hạn ở source/template/package local và checks liên quan. Candidate mới dùng thư mục riêng chưa sử dụng; không cài, kích hoạt, publish, ghi external systems, chạy application tests hay SQL/DB.

Kiểm schema, relocation và byte parity chỉ chứng minh cấu trúc/đóng gói. Việc nhập trên cùng file, recalculation, render và bảo toàn file phải có bằng chứng mới; native Excel, quyền xem thực tế và chạy ứng dụng vẫn là các giới hạn riêng khi chưa kiểm chứng. Kết quả cuối thuộc Verify Gate của plan, không được suy ra từ quyết định này.
