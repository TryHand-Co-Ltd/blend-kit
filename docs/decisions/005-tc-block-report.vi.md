# 005 — Báo cáo dạng TC block

> Historical record. Workbook compatibility/asset retention clauses are superseded by [decision 009](009-current-report-only.vi.md); they do not describe current support.


Ngày: 04/10/2026. Trạng thái: người phụ trách đã duyệt hướng layout, gồm trạng thái ở dòng riêng dưới tiêu đề. Thực thi/kiểm chứng và quyền xuất bản là các phạm vi riêng.

Output mới dùng test-report@2.0.0 với đúng hai sheet: Tổng quan và Testcases. Mỗi block có title đầy đủ, dòng trạng thái riêng, tên màn hình/chức năng cạnh URL tương đối không domain; bốn phần Điều kiện kiểm thử, Thao tác, Kết quả mong đợi và Kết quả thực tế. Nhãn kỹ thuật được nhấn đậm, nội dung dùng steps/bullets. Reset cần thiết nằm ở thao tác cuối, không có footer riêng. Một kết quả độc lập cho mỗi biến thể, không dataset ẩn hoặc sheet ảnh thứ ba. Ảnh/kết quả/metadata thực thi ban đầu trống, trạng thái Chưa thực hiện.

Không hiển thị các dòng readiness/expected-authority lặp trong từng TC, generic proof, link bằng chứng/lỗi, chú thích ảnh, footer PASS/FAIL hay “Về Tổng quan”. Source/checker vẫn giữ authority, readiness, gap, proof và reset. PASS/FAIL được tính khi Confirmed + Ready, status hợp lệ và actual có nội dung; ảnh là bằng chứng hỗ trợ độc lập, không phải điều kiện tối thiểu của con số tổng hợp.

Template source phải tự mô tả: sheet Testcases chứa một block placeholder ghi rõ là minh họa layout. Generator xóa toàn bộ preview trên bản sao in-memory trước khi chiếu TC thật và thay hướng dẫn template bằng hướng dẫn nhập kết quả. Generated report không chứa sample/placeholder. Title/section/field/step number dùng bold có chọn lọc; action sentence dùng font thường. Title căn giữa theo chiều dọc. Nội dung tiếng Việt hiển thị theo sentence case; identifier/URL/literal kỹ thuật giữ nguyên.

Mọi text trong block căn giữa theo chiều dọc. Reset dùng label chữ **Reset**, không dùng icon. Vùng input dùng nền trung tính rất nhạt và viền mảnh, không dùng nền vàng. Màu không là tín hiệu duy nhất; labels và status luôn có text.

Text trong sheet Testcases căn trái. Action dùng label **Step 1**, **Step 2**, … ở bản Việt và **ステップ 1**, **ステップ 2**, … ở bản Nhật. Reset bản Nhật dùng **リセット**.

Mỗi dòng danh sách trong workbook chỉ có đúng một bullet do renderer tạo; dấu `-`, `+`, `*` hoặc `•` ở đầu dòng nguồn phải được bỏ trước khi chiếu. Vì XLSX/Google Sheets không render Markdown, inline code như `` `incomplete-excluded` `` hiển thị thành `[incomplete-excluded]`. Nội dung bên trong code phải giữ nguyên, ví dụ `` `**24` `` thành `[**24]`; chỉ bỏ `**` khi đó là marker bold ở ngoài code. Generated report không được chứa backtick, marker bold ngoài technical token hoặc dạng `• -`. Dropdown trạng thái nằm trong một ô compact không merge ngay cạnh nhãn, không kéo theo toàn bộ chiều rộng nội dung.

Case template 1.1.0 bổ sung screen_relative_path. Không suy URL từ tên màn hình; unknown và lý do Không áp dụng phải được giữ theo bằng chứng. Expected/preparation chưa xác nhận không được đổi thành xác nhận vì đổi layout.

Quyết định thay hướng bảng bảy cột/Details có điều kiện của 004 cho output mới, giữ lifecycle, identity, privacy, no-overwrite và điều kiện tổng hợp. Báo cáo 1.0.1 và runtime/nguồn tương ứng được giữ làm lịch sử. Không copy observations sang expected thay đổi.

Google Sheets là hướng sử dụng: convert bản trống trước QA, xác minh native rồi nhập và review trên cùng file. XLSX checker không chứng nhận native import, ảnh hoặc quyền người nhận. Không tự tạo cloud file, active skills, commit/push hoặc chạy ứng dụng từ quyết định này.
