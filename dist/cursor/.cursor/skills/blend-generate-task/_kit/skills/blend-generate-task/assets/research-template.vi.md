<!-- blend-template: research@1.0.0 -->
# Research — {{Chức năng / công việc}}

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,basis,scope,clauses,flow,impact,gaps,proof. Keep four H2 headings and filled labels below. Replace placeholders, remove this comment. Optional ResearchHandoff H3 only if effective prompt requests Test Spec; use exactly eight shared fields, mode outside fields. No invented observations; empty impact/gaps are explicit assessed none with scope. Preserve exact evidence boundaries. -->

## Phạm vi và căn cứ

- Nguồn: {{ID nguyên gốc, parent đã kiểm, link/anchor nguồn, revision/content identity, trạng thái authority}}
- Căn cứ: {{Spec nhận được, context và xác nhận mới được phép áp dụng; proposal/conflict được phân biệt}}
- Phạm vi: {{Actor, chức năng, operations, phần bao gồm/loại trừ có căn cứ; outputs/languages/destination được yêu cầu}}
- Baseline code: {{Git SHA và identity nội dung liên quan staged/unstaged/untracked/deleted; anchors dạng blend:path; giới hạn access}}
- Nguồn được phép: {{Context/code/public sources và exclusions; public advice, version/applicability không phải business approval}}

## Nghĩa vụ và luồng hiện tại

| Điều khoản / nhánh và anchor | Actor / action / điều kiện | Kết quả và trạng thái phải giữ | As-Is và bằng chứng | Hướng cần có / authority | Chủ sở hữu / AC hoặc gap |
| --- | --- | --- | --- | --- | --- |
| {{Clause ID và nhánh}} | {{Tình huống độc lập}} | {{Outcome/exception/preservation}} | {{Anchor + revision; chưa kiểm được ghi rõ}} | {{Confirmed/Proposed/Awaiting decision}} | {{Assignment/AC hoặc gap}} |

- Luồng hiện tại: {{Entry/route → quyền/validation → inputs/settings/branches → lưu → readback → consumers/lifecycle; phân biệt quan sát source với runtime}}
- Phần bị thay thế: {{Canceled/superseded scope nếu có; nếu không, nêu không có trong phạm vi đã đối chiếu}}

## Ảnh hưởng và phụ thuộc

| Surface / operation | Phân loại | Thay đổi và lý do có căn cứ | Chủ sở hữu / prerequisite | Cách kiểm chứng |
| --- | --- | --- | --- | --- |
| {{Screen/API/job/storage/consumer đã kiểm}} | {{Direct / dependency / regression-only / unresolved}} | {{Required vs engineering proposal}} | {{Một owner; kết quả đầu vào cụ thể}} | {{Giới hạn proof}} |

- Ảnh hưởng: {{Storage/identity/relationship/data lifecycle có cần đổi không; rationale cho DB Design có điều kiện}}
- Phụ thuộc: {{Điều có thể bắt đầu, prerequisite để bắt đầu và để kiểm tích hợp; không bịa Task ID}}

## Gaps và giới hạn

| Gap ID | Loại | Điều chưa biết / điều đã biết | Ảnh hưởng | Bước nhỏ nhất / role quyết định | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| {{Stable ID}} | {{Fact / engineering / business / preparation-proof}} | {{Không xóa nghĩa vụ khi thiếu oracle/fixture}} | {{Clause/assignment/AC bị ảnh hưởng}} | {{Research/check hoặc Q leaf độc lập}} | {{Open/settled có nguồn}} |

- Bằng chứng: {{Nguồn/code đã kiểm thực tế; tool fallback/external applicability; checks chưa chạy; không claim DB/UI/runtime/release}}
- Đối chiếu: {{Source → assignment/AC hoặc gap và chiều ngược lại; supported vs blocked scope}}

<!-- OPTIONAL: When Test Spec requested, append H3 “ResearchHandoff” containing source, authorized_sources, source_basis, code_baseline, research_snapshot, languages, output_scope, limitations. Include actual resolved roots only in transient handoff, never shared document; saved Research paths are repository-relative with content identity. Remove this instruction from output. -->
