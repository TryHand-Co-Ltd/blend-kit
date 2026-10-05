# 007 — Report độc lập, dễ đọc cho khách hàng

> Historical record. Workbook compatibility/asset retention clauses are superseded by [decision 009](009-current-report-only.vi.md); they do not describe current support.


Ngày: 05/10/2026. Người phụ trách duyệt mockup và hướng cập nhật bằng “approve”; cho phép cài dependency đã khai báo vào môi trường riêng trong workspace. Phạm vi: source/template/package local, bộ RC-001 và bản plugin local; không cấp quyền publish, commit/push, chạy ứng dụng, ghi DB hoặc tạo/chia sẻ Google Sheets.

Khách hàng sẽ đọc link Google Sheets được chuyển từ chính XLSX sau khi kiểm thử. Report cần tự chứa bối cảnh/dữ liệu quyết định, thao tác, kết quả tổng thể cuối TC và kết quả từng trường hợp, không yêu cầu mở file testcase. Dùng block ngắn, nhãn VI/JA, cột điều hướng bằng chứng và nhóm hàng mở rộng cho ảnh/chi tiết. Expected không lặp theo từng click; các trạng thái trước/sau quyết định kết quả vẫn phải giữ.

Đăng ký `customer-test-report`, family `test-report@2.3.0`, dưới dạng projection có chủ đích từ source đã chọn. Một lượt chỉ có một workbook nhập kết quả. Source/report 1.3/2.2 và legacy giữ grammar/projection cũ; bố cục mới không tự chuyển lịch sử hoặc chứng minh coverage đã tối ưu.

RC-001 được đổi bố cục trong cùng lượt, bảo toàn ID, oracle, metadata lượt, Actual/Status và bytes của ảnh; lưu nguyên bản trước đổi. Nội dung lặp trong source được tham chiếu context chung mà không đổi nghĩa. Chưa gộp/bỏ/thêm TC nếu chưa có mapping nghĩa vụ và kiểm chứng semantic; không biến quan sát Đạt thành nghiệm thu khi source còn Draft/Blocked. Kiểm schema, parity và rendering là bằng chứng tài liệu, tách khỏi kiểm thử ứng dụng và conversion native Sheets.
