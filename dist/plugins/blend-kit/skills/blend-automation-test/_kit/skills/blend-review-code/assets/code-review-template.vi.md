<!-- blend-template: code-review@1.0.0 -->
# Review triển khai — {{scope}}

<!-- Giữ đủ bảy H2 theo thứ tự; mỗi section ghi rõ không có trong phạm vi khi thích hợp. Xóa instructions/placeholders khi hoàn tất. Không có candidates chỉ sau Hunter hợp lệ; output thiếu không phải kết quả sạch. -->

<!-- Semantic schema: identity,source_plan_revisions,base_head,working_identity,intended_scope,actual_diff,inspection_inventory,prior_findings,finding_id,requirement,invariant,evidence,actor_trigger,expected_actual,impact,counter_evidence,proposal,verification,scope,origin,severity,confidence,completion_effect,consumer_impact,db_risk,role_disposition,verdicts,limits; labels below map one-to-one in this order. -->

## Kết luận và căn cứ review

| Trường | Căn cứ đã kiểm tra |
| --- | --- |
| Danh tính | {{Danh tính feature/task/nguồn/parent chính xác đã xác minh; identities của authority hiện tại}} |
| Nguồn và revision plan | {{Revision và content identities của plan/AC/review đã duyệt; nguồn/role/ngày duyệt và scope; identities của topics/phụ thuộc đã chọn}} |
| Base và head | {{Danh tính application portable; base/head thực tế hoặc merge-base đã kiểm; commits và nghĩa range; nêu baseline chưa rõ}} |
| Danh tính working bytes | {{Content identities staged/unstaged/untracked liên quan/rename/delete; giới hạn capture dirty bytes}} |

## Phạm vi dự kiến, thay đổi thực tế và kiểm tra

Phạm vi nghiệp vụ dự kiến: {{Kết quả, exclusions và hành vi bảo toàn đã duyệt; surfaces dự kiến trong plan}}

Thay đổi thực tế: {{Paths/hunks/categories/identities thay đổi thực tế; thay đổi ngoài dự kiến và kết quả còn thiếu}}

Inventory kiểm tra: {{Mỗi path/hunk được giao hoặc consumer có risk cụ thể; phương pháp đọc thực tế; inspected/skipped và giới hạn}}

Findings trước: {{Lần đầu ghi không có; re-review ghi revision/IDs report trước và ledger bằng chứng}}

## Findings và đề xuất cập nhật

<!-- Khi không có findings được hỗ trợ, thay entry bằng kết quả có phạm vi/depth và nêu phần chưa review; không để trống H2. -->

### {{Finding ID ổn định}} — {{tiêu đề}}

Finding ID: {{ID ổn định của root/trigger chính xác được tham chiếu}}

Yêu cầu: {{Anchor AC/nguồn/rule đang áp dụng và authority chính xác}}

Invariant: {{Contract bắt buộc hoặc hành vi bảo toàn}}

Bằng chứng: {{File/line/revision portable thực tế; luồng base/current hỗ trợ và phương pháp kiểm tra}}

Actor và trigger: {{Actor/permission/state/input/entry và trigger lỗi cụ thể}}

Expected và actual: {{Expected có nguồn đối chiếu actual đã kiểm tra}}

Tác động: {{Users/data/flow bị ảnh hưởng và hậu quả cụ thể}}

Counter-evidence: {{Caller/guard/ngoại lệ bảo vệ và reachability base/current cùng điều kiện đã xét; evidence chưa rõ}}

Đề xuất cập nhật: {{Cập nhật gì/ở đâu/vì sao; obligations/consumers bị ảnh hưởng và hành vi cần bảo toàn; không tự đặt oracle}}

Kiểm chứng sau sửa: {{Check hữu hạn phân biệt lỗi; proof đã cung cấp/còn thiếu, không ghi PASS dự kiến}}

Phạm vi: {{IN_SCOPE / OUT_OF_SCOPE / UNRESOLVED và căn cứ assignment}}

Origin: {{INTRODUCED / WORSENED / PRE_EXISTING / UNKNOWN với so sánh baseline tương đương}}

Severity: {{Critical / High / Medium / Low theo tác động thực tế}}

Confidence: {{Độ mạnh bằng chứng và paths chưa rõ, độc lập severity}}

Ảnh hưởng hoàn thành: {{Task blocker / Regression blocker / Release risk / Follow-up / Needs evidence và lý do}}

Giới hạn: {{Scope chưa đọc, roles/source/runtime/DB/release proof thiếu và check hữu hạn còn lại; static không suy runtime}}

## Luồng dùng chung và rủi ro DB

Ảnh hưởng consumer: {{Consumers dùng chung cụ thể, risk/flow, kết quả/phương pháp đã kiểm hoặc giới hạn; ghi rõ không ảnh hưởng khi phù hợp}}

Rủi ro DB: {{Rủi ro schema/data/migration/replica bị ảnh hưởng, evidence cung cấp/check hữu hạn còn thiếu; không ảnh hưởng phải ghi rõ}}

<!-- Conditional H3 DB/migration detail is required only when affected; omit otherwise, keep H2 and scoped none statement. -->

### Chi tiết DB/migration (khi bị ảnh hưởng)

{{So sánh design/actual type/NULL/default/identity/relationships/collation/index/query; rows/NULL/duplicates/backfill/school-year; bảo toàn/partial failure/rerun/compatibility/order/rollback; applicability engine/version/shape/volume/lock/rebuild và gaps; replica start/end/early exits/read-after-write; không live DB/chạy SQL}}

## Candidates và phân xử vai trò

RoleDisposition: {{Entries đủ mười một fields thực tế bên dưới; output role cần thiết thiếu/không hợp lệ là UNREVIEWED; không giả role}}

<!-- RoleDisposition schema comes from shared/bug-hunter.md; one inline entry per actual role/candidate. Native distinct agents when available/authorized; local-sequential independent=false disclosed at each claim. Zero candidates: completed valid Hunter NO_CANDIDATES; Skeptic/Referee not-run with reason. Missing/empty/malformed output: UNREVIEWED and exact gap, never clean. -->

| Field | Kết quả thực tế |
| --- | --- |
| candidate_id | {{ID ổn định; none chỉ khi Hunter hợp lệ đã xong không có candidate}} |
| role | {{Hunter / Skeptic / Referee; role bỏ qua ghi đúng tên và lý do}} |
| run_identity | {{Agent/run ID và status trả về thực tế, hoặc ID local pass trung thực; không bịa ID}} |
| backend | {{Backend native thực tế hoặc local-sequential; capability thiếu nêu rõ}} |
| independent | {{true chỉ cho agents thực sự khác nhau; local-sequential dùng false}} |
| basis | {{Cùng identities source/context/code/base/head/working/topics; drift hoặc refresh nêu rõ}} |
| evidence | {{Location/revision source đã đọc, trace/trigger/kết quả/phương pháp thực tế; none có lý do khi không candidate}} |
| counter_evidence | {{Caller/guard/ngoại lệ bảo vệ và baseline tương đương đã xét; không tìm được disproof không chứng minh bug}} |
| verdict | {{Hunter CANDIDATE / NO_CANDIDATES; Skeptic STANDS / DISPROVED / UNCERTAIN; Referee REAL_BUG / NOT_A_BUG / MANUAL_REVIEW; output cần thiết thiếu/không hợp lệ UNREVIEWED}} |
| depth | {{direct-source / evidence-only / not-run; đọc source không là reproduction đã chạy}} |
| limits | {{Paths chưa rõ/scope chưa đọc/role hoặc tool/proof thiếu/độc lập giảm; none chỉ khi thực sự không có}} |

## Ngoài phạm vi, có sẵn và chưa rõ

{{ID liên kết finding chính; owner/phạm vi/origin/effect độc lập; regression mới/nặng hơn vẫn blocker dù OUT_OF_SCOPE; lỗi cũ đã chứng minh không liên quan có follow-up; chưa rõ cần evidence, không mặc định bỏ}}

<!-- Prior-finding ledger is required only on re-review; omit H3/table on initial review, keep H2. -->

### Ledger lần review trước

| ID | Prior revision / evidence | OPEN / FIXED_VERIFIED / DISPROVED / DEFERRED / NEEDS_EVIDENCE | Current evidence / reason / proof limit |
| --- | --- | --- | --- |
| {{ID ổn định trước}} | {{revision trước thực tế}} | {{status có bằng chứng}} | {{thay đổi và proof đóng thực sự đã đọc; defer được duyệt không là fixed}} |

## Nghiệm thu và giới hạn bằng chứng

Kết luận độc lập: {{Acceptance được giao; regression; standards; DB risk; proof runtime/QA/release riêng, mỗi trục có căn cứ/status}}

Giới hạn: {{Scope chưa đọc, roles/source/runtime/DB/release proof thiếu và check hữu hạn còn lại; static không suy runtime}}

Checks đã chạy: {{chỉ phương pháp/kết quả/scope thực tế; đọc source không là reproduction đã chạy}}

Checks chưa chạy: {{checks application/DB/browser/API/device/QA/release còn thiếu; check hữu hạn còn lại}}

Bảo toàn: {{bảo toàn inputs/dirty/history/IDs; kiểm tra root-atomicity và cross-references ID/proposal/ledger}}
