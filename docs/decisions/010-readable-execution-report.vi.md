# Report thực hiện dễ đọc và tổng hợp trực tiếp

Ngày: 06/10/2026. Trạng thái: Đã duyệt; cập nhật local, chưa phát hành.

## Vấn đề và quyết định

Danh sách biến thể phía trên bảng lặp tên và dữ liệu trong bảng; Expected của nhiều nhánh còn lặp toàn bộ kết quả đa nhánh. Công thức readiness khóa bộ đếm khiến kết quả tester ghi nhận không được phản ánh.

Report hiện hành là `test-report@2.5.0`, plugin `2.1.0`. Mỗi TC có tiêu đề/kết quả thực hiện, điều kiện có nhãn, bảng Bước/Thao tác chung, bảng trường hợp năm cột và ảnh bên dưới. Bảng trường hợp gồm Trường hợp; Dữ liệu/thao tác riêng; Kết quả mong đợi; Kết quả thực tế; Đánh giá. Không có danh sách biến thể lặp, Expected chung ngoài bảng hoặc cột Xem ảnh. Mỗi nhánh giữ tên dễ hiểu kèm ID, dữ liệu quyết định và đầy đủ assertions của chính nhánh đó.

Chỉ phần ảnh thu/mở; title nằm trên mỗi ảnh, hàng dự phòng ẩn hoàn toàn. Bold chọn lọc nhãn UI, operator và giá trị quyết định bằng rich text native; literal không đổi và vẫn kiểm privacy trên toàn nội dung nối từ các runs. Không thêm Markdown vào ô hoặc bold toàn đoạn.

Điều chỉnh đã duyệt: nội dung ngoài bảng trường hợp căn giữa theo chiều dọc; nội dung trong bảng căn trên-trái, có khoảng cách trên 4 px. XLSX tạo một hàng matrix_padding 3 pt (4 px) có chủ đích trước mỗi hàng dữ liệu; hàng này không là TC/kết quả, không lặp nội dung và không là hàng dự phòng ảnh. Không tạo padding bằng newline trong giá trị hoặc number format. Giá trị căn phải giữ indent 1. Google Sheets dùng padding thực trên/dưới 4 px, trái/phải 8 px; không áp dụng đồng thời spacer XLSX và padding native. Tiêu đề ở Tổng quan là plain text với hyperlink toàn ô; nội dung vẫn bold chọn lọc. Kiểm riêng spacing/navigation sau save/reopen/import.


Kết quả ghi nhận không bị khóa bởi readiness/Actual. Thứ tự tổng hợp: có FAIL → FAIL; tất cả PASS → PASS; tất cả SKIPPED → SKIPPED; có BLOCKED → BLOCKED; tất cả NOT RUN → NOT RUN; còn lại → Đang thực hiện. Tổng quan đếm status đã ghi nhận. Checker vẫn báo thiếu Actual, fixture, oracle, readiness và evidence; PASS ghi nhận không chứng minh nghiệm thu hoặc release. Readiness nguồn không tự promote.

## Phạm vi và thay thế

Quyết định này thay layout/count của [008](008-readable-report-and-viewport-evidence.vi.md) và phiên bản hiện hành trong [009](009-current-report-only.vi.md); không thay nghĩa nguồn, IDs, dữ liệu biên, quyền, oracle hoặc hợp đồng evidence. Những quyết định trước giữ lại để giải thích lịch sử, không là hướng dẫn count hiện hành.

Chỉ giữ một cặp asset JA/VI cho report2.5; workbook2.4 và cũ hơn bị từ chối không ghi lại. Đọc grammar nguồn1.0–1.3 không cho phép tự sửa nguồn hoặc migrate kết quả. Tái sinh report trắng phải có yêu cầu riêng, giữ bản trước ngoài deliverable; không tự ghi đè Google Sheets có kết quả, đồng bộ hai report, cài cache, commit, push hoặc phát hành.
