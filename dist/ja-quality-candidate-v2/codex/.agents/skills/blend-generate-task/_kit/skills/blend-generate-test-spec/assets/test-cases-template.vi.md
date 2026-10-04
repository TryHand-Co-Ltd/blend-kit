<!-- blend-template: test-cases@1.0.0 -->
# [Feature] — [test cases]

<!-- AUTHORING: Replace brackets and remove this instruction. Required headings/fields/order stay. Use <br> within a table cell and &#124; for literal pipe. Confirmed/Proposed/Awaiting decision are authority; Ready/Draft/Blocked are readiness; new execution is NOT RUN. Unsupported oracle remains gap. -->

## Quy ước và context

| Field | Value |
| --- | --- |
| Revision | [same design revision] |
| Feature | [verified identity and purpose] |
| Conventions | [links to scope/data; priority rationale, evidence/reset conventions] |

<!-- AUTHORING: Optional shared context block only when reused. Same-field @CTX-ID references are allowed; no recursive/mixed reference. Do not repeat identical setup in every case. -->

### Context: CTX-1

| Field | Value |
| --- | --- |
| Cấu hình | [verified value] |
| Kích hoạt | [verified value] |
| Quan sát | [verified value] |
| Actor và quyền | [verified value] |
| Fixture | [verified value] |

## Các testcase

### Flow: [business operation]

#### TC-01 — [one independently failing behavior]

| Field | Value |
| --- | --- |
| Chức năng | [verified value] |
| Căn cứ | [verified value] |
| Priority | [verified value] |
| Căn cứ kỳ vọng | [verified value] |
| Readiness | [verified value] |
| Gap | [verified value] |
| Cấu hình | [verified value] |
| Kích hoạt | [verified value] |
| Quan sát | [verified value] |
| Actor và quyền | [verified value] |
| Fixture | [verified value] |
| Thao tác | [verified value] |
| Expected | [verified value] |
| Bảo toàn | [verified value] |
| Bằng chứng | [verified value] |
| Reset | [verified value] |

<!-- AUTHORING: Priority = High/Medium/Low; expected basis = Confirmed/Proposed/Awaiting decision. Ready requires known oracle plus verified preparation/seams; Draft/Blocked require Gap ID defined in scope (Ready uses none). Fixture = exact TD IDs separated by comma-space, or local: reproducible setup. All field rows required; genuine preservation/proof/reset inapplicability needs reason. Compact case puts action/expected inline. Expanded case replaces both values with @Steps and uses Steps below. -->

<!-- AUTHORING: Gap của Ready là đúng literal none. Gap của Draft/Blocked là một hoặc nhiều ID gap hiện có, phân cách dấu phẩy và một khoảng trắng: G-X hoặc G-X, G-Y. Giữ mọi blocker độc lập; không tạo gap tổng hợp để bỏ tham chiếu. Không lặp ID, dùng dấu chấm phẩy, trộn none với ID hoặc thêm giải thích trong field Gap; mô tả nằm ở bản ghi gap/fixture/proof tương ứng. ID ví dụ không được tự phát minh cho source. -->

##### Steps

| Step | Action | Expected | Preservation |
| --- | --- | --- | --- |
| 1 | [establish prerequisite] | [observable condition] | [required preserved state or reason] |
| 2 | [exercise operation] | [source-backed observation; parameter placeholders only if variant table] | [required preserved state] |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| a | [branch-selecting values] | [source-backed expected] |
| b | [boundary values] | [source-backed expected] |

<!-- AUTHORING: Steps absent only for inline compact action/expected. Variants absent only for one base run; present table lists all mandatory rows separately, never compound a/b/c. Same schema/context/fields for compact/expanded/parameterized cases. Group main path, boundaries, validation/permission, recovery; priority only selects run order. No actual/evidence-result fields in Markdown. Unknown oracle goes in scope gaps, not fabricated expected. -->
