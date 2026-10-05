# Report dễ đọc và bằng chứng theo vùng cần quan sát

> Historical record. Workbook compatibility/asset retention clauses are superseded by [decision 009](009-current-report-only.vi.md); they do not describe current support.


Status: Approved — 2026-10-05. Người phụ trách đã duyệt mẫu và phạm vi hai skill Generate Test Spec/Automation Test cùng bộ RC-001. Nguồn ràng buộc: phê duyệt trực tiếp ngày 05/10/2026; các ràng buộc đã chốt được ghi đầy đủ bên dưới.

Report khách hàng mới dùng `test-report@2.4.0`, đúng hai sheet. Mỗi tình huống có đủ điều kiện, dữ liệu, thao tác và kết quả cụ thể để người đọc thực hiện và đối chiếu Expected–Actual. Mô tả đứng trước mã biến thể; mã và coverage giữ nguyên. Cùng thao tác khác dữ liệu dùng bảng; khác quy trình hoặc trạng thái đầu phải hiểu được độc lập.

Chỉ phần ảnh thu/mở, một nhóm mỗi TC, mặc định thu gọn. Mỗi ảnh nhúng trực tiếp có tiêu đề mô tả tình huống/mốc/quan sát ở phía trên, xếp dọc và giữ nguyên bytes, tỷ lệ. Không yêu cầu URL. Chưa có ảnh chỉ có một dòng, không dự phòng vùng trống lớn. Kiểm collapse/ảnh native Google Sheets riêng; XLSX không chứng minh hành vi native.

Bỏ ghi chú review/mẫu, nhãn Chuẩn bị và technical appendix mặc định khỏi report. Chỉ giữ thông tin kỹ thuật cần thực hiện, hiểu hoặc xác minh ở cạnh nội dung liên quan. Identity, readiness, oracle, quyền, provenance và điều kiện eligibility vẫn được kiểm nội bộ. Ảnh không thay thế phép kiểm DB/API hoặc file xuất thật.

Thay yêu cầu full-page bắt buộc trong hợp đồng capture đang hoạt động: mặc định `full_page=false`, giữ đủ bối cảnh và dữ liệu quyết định; full page chỉ khi cần toàn bố cục. Raw trước annotated, cùng state/scope, metadata ghi đúng giá trị thực. Note tiếng Anh mô tả quan sát ngắn ở top-right, không che UI/dữ liệu. Highlight tối thiểu, bỏ vùng trùng/lồng và không để khung giao/chạm nhau; chỉ gộp cặp giá trị/kết quả khi cần chứng minh cùng cặp. Mở pixels thật để kiểm trước khi chấp nhận.

Các quyết định/snapshot lịch sử vẫn giữ nguyên. Customer2.3 dùng tài nguyên frozen `legacy-2.3`; layout mới không tự cấp quyền migration. RC-001 cần backup và mapping semantic, bảo toàn 216 Case IDs, 569 variant identities, Actual/Status, metadata lượt chạy và 69 ảnh nguyên bytes. Không chuyển PASS sang oracle đã đổi, không viết Expected theo Actual, không dựng bằng chứng thật.

Phê duyệt này chỉ cho chỉnh source/template/runtime/package local và RC-001 theo kế hoạch. Không install vào cache, publish, commit/push, chạy BLEND hoặc ghi DB.

Điều chỉnh ngày 06/10/2026: ô dữ liệu trong bảng kết quả customer2.4 căn trái và căn trên, dùng thụt lề native nhẹ cùng khoảng dư chiều cao hàng; không thêm khoảng trắng hoặc xuống dòng vào giá trị literal để tạo khoảng cách. Bố cục legacy frozen giữ nguyên.
