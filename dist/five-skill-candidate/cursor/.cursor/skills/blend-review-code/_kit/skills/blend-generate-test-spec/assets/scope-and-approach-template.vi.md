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

<!-- AUTHORING: Cột Case / variant / gap chỉ chứa ID hiện có: TC-ID, TC-ID:variant hoặc G-ID. Nhiều tham chiếu phân cách đúng dấu phẩy và một khoảng trắng, ví dụ TC-X:a, TC-X:b, G-X. Không lặp ID, dùng dấu chấm phẩy, chú thích bước hoặc văn xuôi trong cột này; chuyển mô tả vào Rationale / proof limit. Các ID ví dụ không phải ID nghiệp vụ mới. -->

### Gaps

| Gap ID | Kind | Known obligation / source | Missing decision / proof | Impact / next check |
| --- | --- | --- | --- | --- |
| [G-ID] | [business/fact/engineering/preparation/proof] | [known obligation] | [unknown oracle/seam/fixture] | [affected TC; smallest check] |

<!-- AUTHORING: Mỗi dòng gap có đúng MỘT Kind: business, fact, engineering, preparation hoặc proof; ví dụ fact, không phải fact, proof. Ghi giới hạn thứ cấp vào Missing decision / proof. Nguyên nhân độc lập cần bản ghi gap riêng với ID ổn định, không gộp để che mất blocker. -->

<!-- AUTHORING: No gaps permits no rows and a clear none statement. Coverage always retains every active clause/branch. Research basis records standalone or frozen-handoff reuse, decisive checks and any delta. Exclusions need authority. Source and dirty code revision are independent. -->
