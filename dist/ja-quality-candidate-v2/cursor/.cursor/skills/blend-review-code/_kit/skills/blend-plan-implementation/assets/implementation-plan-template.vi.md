<!-- blend-template: implementation-plan@1.0.0 -->
# {{Tên phạm vi}} — Kế hoạch triển khai

<!-- TEMPLATE INSTRUCTIONS: implementation-plan@1.0.0. Retain all six H2s and localized labels. Explicit none with scoped reason, never empty sections. Repeat supported outcome step blocks; step IDs are local planning references, never source Task IDs. Optional H3 predicates are in references/planning.md: prior findings, meaningful independent parallel work, affected DB/migration only. Remove comments/placeholders in completed output. -->

## Đầu vào đã duyệt và căn cứ

- Mục đích: {{Vấn đề và kết quả đã duyệt cần triển khai}}
- Trạng thái: Draft — {{Plan để review; affected scope Blocked nếu thiếu approval/business decision}}
- Danh tính: {{Feature ID/nguồn/link đã kiểm; Task ID và parent trực tiếp nếu task-scoped; không suy từ ordinal}}
- Revisions nguồn: {{Actual approved artifact paths + per-file revision/SHA-256 + clauses/AC; current CONTEXT/authorized confirmations + identities/authority riêng}}
- Kết quả review: {{Report path/revision/disposition, phạm vi đã đọc và unresolved findings; hoặc chưa có với giới hạn}}
- Căn cứ phê duyệt: {{Explicit source/role/date, exact approved paths/revisions/hashes và selected scope; match actual bytes hay gap}}
- Phạm vi đã duyệt: {{Selected outcomes/AC, approval scope và phần chưa duyệt}}
- Baseline code: {{Application Git SHA + relevant working-content identities/status; blend:repo-relative evidence, static limits}}
- Phụ thuộc Research: {{Selected actual topic paths/hashes, consumed conclusions và decisive source/code/confirmation identities; hoặc không cần với lý do}}

<!-- OPTIONAL H3 “Xử lý findings trước đó” only with relevant prior review findings: stable ID, disposition, exact evidence, blocking scope/dependents and approval impact. -->

## Phạm vi và hành vi bảo toàn

- Trong phạm vi: {{Actors/actions/outcomes và expected affected code/consumer surfaces}}
- Ngoài phạm vi: {{Excluded behavior, unapproved/dependent scope và source authority}}
- Bảo toàn: {{Existing permissions/state/defaults/exceptions/data/lifecycle/shared consumers phải giữ}}

## Các bước triển khai

### P1 — {{Kết quả độc lập}}

- Mã bước: P1
- Kết quả: {{Observable outcome và proof seam}}
- Files và symbols: {{Exact blend:repo-relative existing paths/symbol roles; proposed new files đánh dấu}}
- Điều kiện bắt đầu: {{Exact input artifact/interface/decision needed; hoặc không có}}
- Contracts: {{Canonical consumes/produces name/signature/types nếu cross-step dependency; hoặc không có}}
- Ownership: {{Role chịu trách nhiệm và owned paths; không bịa tên người}}
- Phụ thuộc: {{Producer step + artifact/decision, start/integration gate; hoặc không có}}
- Nghĩa vụ binding: {{Verbatim approved constraints, exact defaults/values/forbidden behavior và source/AC IDs}}
- Hành động: {{Cohesive implementation actions, reuse existing code; engineering proposal được ghi rõ}}

## Phụ thuộc và song song

{{Exact step/artifact dependencies, order/start/integration gates và ownership conflicts; không có dependency/parallel work thì ghi rõ lý do.}}

<!-- OPTIONAL H3 “Kế hoạch song song” only with meaningful independent steps: wave | steps | disjoint owned paths | exact prerequisite | parallel peers. Unknown independence remains serial. -->

## Tiêu chí nghiệm thu và kiểm chứng

- Ánh xạ AC: {{Mọi active selected AC/obligation → step → discriminating required observation/proof hoặc exact Blocked gap}}
- Commands kiểm chứng: {{Full verified toolchain commands/flags, cwd relative to application root; proposed checks + creation prerequisites rõ; unresolved command Blocked}}
- Trạng thái kiểm chứng: Planned / Not run — {{Không chạy trong planning; static/test/DB/browser/release evidence riêng}}

| AC/nghĩa vụ | Bước | Quan sát và bảo toàn | Loại proof, command và chuẩn bị | Tín hiệu mong đợi | Trạng thái/gap |
| --- | --- | --- | --- | --- | --- |
| {{Exact AC ID}} | P1 | {{Discriminating outcome/preserved state}} | {{Toolchain-backed command; cwd relative; environment/fixture}} | {{Success/failure signal}} | Planned / Not run |

## Rủi ro và kiểm tra cuối

- Rủi ro: {{Business blockers, engineering proposals/facts, compatibility/proof/permission risks và affected steps; hoặc không có đã kiểm}}
- Kiểm tra cuối: {{Final selected AC/preservation/interface validation, planned commands, deliverables/handoff và remaining evidence/authorization; không claim hoàn tất/runtime}}
- Quyền thực thi: Chưa được cấp bởi plan này — {{Execution, test/SQL, publication/release cần authorization riêng; ghi actual restrictions}}

<!-- OPTIONAL H3 “DB và migration” only when affected: storage/schema/current rows, compatibility/release order, rerun/partial failure/backfill/locks/replicas/preservation, rollback limits and missing proof. No SQL/migration output or execution. -->
