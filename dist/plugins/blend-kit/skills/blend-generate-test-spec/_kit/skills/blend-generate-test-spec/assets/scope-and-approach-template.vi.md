<!-- blend-template: scope-and-approach@1.0.0 -->
# [Feature] — [test scope]

<!-- AUTHORING: Replace brackets and remove this instruction. Required headings/fields/order stay. Use <br> within a table cell and &#124; for literal pipe. Confirmed/Proposed/Awaiting decision are authority; Ready/Draft/Blocked are readiness; new execution is NOT RUN. Unsupported oracle remains gap. -->

## Mục tiêu và căn cứ

| Field | Value |
| --- | --- |
| Revision | [verified value] |
| Nguồn | [verified value] |
| Căn cứ research | [verified value] |
| Baseline code | [verified value] |
| Mode | [verified value] |
| Giới hạn | [verified value] |

## Phạm vi

| Field | Value |
| --- | --- |
| Trong scope | [verified value] |
| Ngoài scope | [verified value] |
| Vai trò | [verified value] |

## Chuẩn bị và cách chạy

| Field | Value |
| --- | --- |
| Môi trường | [verified value] |
| Chuẩn bị | [verified value] |
| Chọn lượt chạy | [verified value] |
| Điều kiện bắt đầu | [verified value] |
| Điều kiện kết thúc | [verified value] |
| Bằng chứng | [verified value] |

## Coverage và gaps

### Coverage

| Clause / anchor | Obligation / branch | Case / variant / gap | Rationale / proof limit |
| --- | --- | --- | --- |
| [source clause] | [actor, branch, outcome and preservation] | [TC-ID:variant or G-ID] | [discriminating check/equivalence] |

<!-- AUTHORING: Cột Case / variant / gap chỉ chứa ID hiện có: TC-ID, TC-ID:variant, TC-ID:variant:checkpoint (source 1.2.0) hoặc G-ID. Nhiều tham chiếu phân cách đúng dấu phẩy và một khoảng trắng. Không lặp ID, dùng dấu chấm phẩy hoặc văn xuôi trong cột này; old-ID mapping, lane và giải thích nằm ở Rationale / proof limit. ID ví dụ không phải ID nghiệp vụ mới. -->

### Gaps

| Gap ID | Kind | Known obligation / source | Missing decision / proof | Impact / next check |
| --- | --- | --- | --- | --- |
| [G-ID] | [business/fact/engineering/preparation/proof] | [known obligation] | [unknown oracle/seam/fixture] | [affected TC; smallest check] |

<!-- AUTHORING: Mỗi dòng gap có đúng MỘT Kind: business, fact, engineering, preparation hoặc proof; ví dụ fact, không phải fact, proof. Ghi giới hạn thứ cấp vào Missing decision / proof. Nguyên nhân độc lập cần bản ghi gap riêng với ID ổn định, không gộp để che mất blocker. -->

<!-- AUTHORING: No gaps permits no rows and a clear none statement. Coverage retains every active clause/branch; no case-count quota. Rationale / proof limit records each case's Browser/Integration/DB/Security/Performance lane and non-browser proof seams. On authorized grouping refresh map old Case/Variant → new Case/Variant/Checkpoint or gap, obligation, disposition and reduction reason here; do not add an unregistered table. Target references may include TC-ID:variant:checkpoint for test-cases@1.2.0. Tiny UI/persistence checks may become checkpoints only if their obligations remain mapped. Keep permission/lifecycle/source/writer/output branches independently testable. Plan before/setup/result/after/export proof as needed; reviewed viewport images (full page only when necessary) remain inside the same TC in Testcases, with descriptive titles above images and one collapsed evidence group per TC. Configuration is not output proof; actual Excel/PDF file is required. Research basis records standalone or frozen-handoff reuse, decisive checks and delta. Exclusions need authority. Source/code identity, expected authority, readiness and execution remain independent. -->
