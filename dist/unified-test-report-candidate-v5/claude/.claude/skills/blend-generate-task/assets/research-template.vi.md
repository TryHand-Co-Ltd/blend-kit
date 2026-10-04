<!-- blend-template: research@1.1.0 -->
# Research — {{Chủ đề / luồng cần nghiên cứu}}

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,basis,topic,purpose,scope,dependencies,currentness,clauses,flow,impact,gaps,proof. Keep four H2 headings and filled labels below. Destination: verified feature-root research/<topic>.vi.md; meaningful question/flow, no default whole-feature/trivial/empty output. Basename follows registry; Task ID prefix only when verified, preserving case/zeros and immediate parent. Replace placeholders, remove this comment. Optional ResearchHandoff H3 only if effective prompt requests Test Spec; use exactly eight shared fields, mode outside fields. No invented observations; empty impact/gaps explicitly state assessed none with scope. Legacy research@1.0.0 remains read-only at its original baseline. -->

## Phạm vi và căn cứ

- Nguồn: {{ID nguyên gốc, parent đã kiểm, link/anchor nguồn, revision/content identity, trạng thái authority}}
- Căn cứ: {{Spec nhận được, context và xác nhận mới được phép áp dụng; proposal/conflict được phân biệt}}
- Chủ đề: {{Tên topic và câu hỏi/luồng tái sử dụng được; basename đã chọn không tự chứng minh ID}}
- Mục đích: {{Vấn đề cần giải đáp, câu hỏi cụ thể và kết luận mà người dùng cần dùng lại}}
- Phạm vi: {{Actor, chức năng, operations, phần bao gồm/loại trừ có căn cứ; outputs/languages/destination được yêu cầu}}
- Baseline code: {{Git SHA và identity nội dung liên quan staged/unstaged/untracked/deleted; anchors dạng blend:path; giới hạn access}}
- Nguồn được phép: {{Context/code/public sources và exclusions; public advice, version/applicability không phải business approval}}
- Tính hiện hành: {{Current/stale/unverified theo phạm vi đã kiểm; captured file identities và dependencies được đối chiếu khi nào; relevant delta/incorrect conclusion giữ phần bị ảnh hưởng Draft, không suy hiện hành chỉ từ SHA/mtime}}

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
- Phụ thuộc: {{Mỗi source/code/confirmation path+anchor, revision/content/working identity gắn với câu hỏi/kết luận/clause được dùng; captures thiếu là giới hạn; prerequisite bắt đầu/tích hợp; không bịa Task ID. Chỉ selected actual topic files với per-file captured identities, không folder digest; unrelated topics không tự invalidate toàn feature}}

## Gaps và giới hạn

| Gap ID | Loại | Điều chưa biết / điều đã biết | Ảnh hưởng | Bước nhỏ nhất / role quyết định | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| {{Stable ID}} | {{Fact / engineering / business / preparation-proof}} | {{Không xóa nghĩa vụ khi thiếu oracle/fixture}} | {{Clause/assignment/AC bị ảnh hưởng}} | {{Research/check hoặc Q leaf độc lập}} | {{Open/settled có nguồn}} |

- Bằng chứng: {{Nguồn/code đã kiểm thực tế; tool fallback/external applicability; checks chưa chạy; không claim DB/UI/runtime/release}}
- Đối chiếu: {{Source → assignment/AC hoặc gap và chiều ngược lại; supported vs blocked scope}}

<!-- OPTIONAL: When Test Spec requested, emit the transient ResearchHandoff after saving final topic bytes with source, authorized_sources, source_basis, code_baseline, research_snapshot, languages, output_scope, limitations. Snapshot names selected actual saved topic paths + captured byte identities + consumed questions/clauses + decisive dependency identities, never folder digest or self-hash embedded in captured file. An optional H3 ResearchHandoff may explain selected reuse/dependencies; final captured identities belong in the transient invocation. Freeze during consumption; scoped delta only for relevant drift. Actual roots stay transient; shared paths are repository-relative. Remove instruction. -->
