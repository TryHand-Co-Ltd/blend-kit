<!-- blend-template: split-tasks@1.0.0 -->
# {{Chức năng}} — Nội dung thay đổi và chia công việc

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,scope,title,main_screen,affected_screens,business,technical,completion. Keep both H2 headings and task labels. Repeat H3 task block per usable outcome; local numbers are not source IDs. Optional summary table only when comparison helps; dependencies/open decisions H4 only if applicable. Explicit no-screen seam/no-other-screen result; never omit required labels because empty. Remove instructions/placeholders. -->

## Phạm vi

- Nguồn: {{ID/parent nguyên gốc đã kiểm, nguồn/link dùng chung, revision, authority}}
- Phạm vi: {{Vấn đề, actors/permissions, operations, intended outcome, phần chưa được duyệt và phần giữ nguyên}}

## Các task

<!-- OPTIONAL summary when multiple outcomes benefit from comparison: Task | Màn hình chính | Thay đổi | Đầu vào thực sự cần có. Titles/screens must match detail. -->

### 1. {{Kết quả độc lập có thể bàn giao}}

**Màn hình chính:** {{[Tên Việt（日本語）] - `verified route`; hoặc không có màn trực tiếp và API/job/shared seam cụ thể}}

**Màn hình bị ảnh hưởng:**

- {{Screen/path khác đã kiểm; không lặp màn chính; nếu không có, ghi rõ không có trong phạm vi đã kiểm}}

**Phạm vi thay đổi:** {{Direct ownership, role/permission, necessary dependency, regression-only và unresolved impact}}

#### Thay đổi nghiệp vụ

- {{Actor/action/conditions → outcome, failures/exceptions và trạng thái cần giữ; proposal chưa duyệt được đánh dấu}}

#### Hướng kỹ thuật

- {{Verified repo-relative anchor/symbol và vai trò → hướng thay đổi → input/output/save/readback/consumer → constraints; engineering choice không bắt buộc nếu có cách tương đương}}

<!-- OPTIONAL H4 “Phụ thuộc và phần chưa chốt” only with real prerequisite/open decision: producer + needed result; can-start-now/start/integration gates; exact unanswered decision. -->

#### Hoàn tất khi

{{Một kết quả quan sát được, không claim đã implement/test; có thể bổ trợ bằng AC ID}}
