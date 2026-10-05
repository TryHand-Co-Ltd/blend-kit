<!-- blend-template: review@1.0.0 -->
# {{Phạm vi được review}} — Review artifacts

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,revision,scope,inventory,verdicts,finding_id,severity,evidence,scenario,impact,proposal,verification,limits. Required H2s and field labels/order stay. Same template for Task-only/standalone Test Spec/combined and chat/file. Replace placeholders and remove instructions. Inventory every assigned file/language/workbook, including skipped/unread. Finding blocks may be absent only when no supported findings remain; state this explicitly. Prior-finding ledger is required only on re-review. Optional advice appears separately only when present. Do not fill unknown facts to conform. -->

## Kết luận và phạm vi

- Nguồn: {{Spec/current context/latest confirmation anchors và authority; Research là bằng chứng được kiểm}}
- Revision: {{Artifact/source snapshot và code SHA + relevant working-content identity; không lộ private paths}}
- Phạm vi: {{TaskArtifacts / TestSpecArtifacts / combined; files/languages và exclusions được giao}}
- Kết luận: {{Kết quả từng trục và những nghĩa vụ/gaps quyết định; không coi static review là runtime PASS}}

| Trục | Kết quả | Căn cứ và giới hạn |
| --- | --- | --- |
| Template | {{Conform / mismatch / needs evidence}} | {{Version, required/conditional fields}} |
| Nội dung | {{Supported / mismatch / needs evidence}} | {{Source semantics và bilingual fidelity}} |
| Coverage | {{Complete design / gaps / mismatch / không áp dụng có lý do}} | {{Clause/branch → case/variant/gap hoặc task/AC}} |
| Readiness | {{Ready / Draft / Blocked / không áp dụng có lý do}} | {{Oracle, preparation, seams}} |
| Execution proof | {{NOT RUN / supplied evidence assessed / needs evidence / không áp dụng có lý do}} | {{Actual proof type; không nâng cấp từ source}} |

### Inventory

| Artifact | Path / revision | Ngôn ngữ | Template / version | Inspected / skipped | Bằng chứng / lý do |
| --- | --- | --- | --- | --- | --- |
| {{Type}} | {{Repository-relative actual path + identity}} | {{ja/vi/workbook}} | {{Family@version hoặc legacy limitation}} | {{Inspected / skipped / unread}} | {{Line/sheet scope hoặc missing access}} |

## Findings và đề xuất cập nhật

### {{Stable finding ID}} — {{Severity}} — {{Vấn đề cụ thể}}

- Phân loại: {{Scope; origin; completion effect; behavioral disposition/backend nếu thực sự có}}
- Bằng chứng: {{Violated source/rule anchor + artifact file:line@revision hoặc Sheet!Cell + Case ID/Variant; counter-evidence được xét}}
- Tình huống: {{Actor/state/input/action dẫn đến thiếu/sai; implementation vi phạm vẫn có thể PASS nếu là test gap}}
- Tác động: {{Outcome/user/data/coverage bị ảnh hưởng và vì sao quan trọng}}
- Đề xuất cập nhật: {{Đổi file/AC/TC/variant/fixture/coverage/workbook nào; corrected expected/branch và nguồn; phần phải giữ; unknown oracle cần quyết định riêng}}
- Kiểm chứng sau sửa: {{Finite source/diff/parity/observation check; proposal không cho phép tự execute}}
- Giới hạn: {{Phần chưa chứng minh, bước chứng minh nhỏ nhất hoặc không có trong phạm vi đã kiểm}}

<!-- OPTIONAL only on re-review: preserve prior IDs, even moved/disproved/deferred; no new ID for the same root cause. -->

### Theo dõi findings cũ

| ID | Trạng thái | Change / closure evidence | Giới hạn / bước tiếp theo |
| --- | --- | --- | --- |
| {{Existing ID}} | {{OPEN / FIXED_VERIFIED / DISPROVED / DEFERRED / NEEDS_EVIDENCE}} | {{New revision/location + relevant proof or counter-evidence}} | {{Remaining proof/decision}} |

<!-- OPTIONAL only if non-binding advice exists: use H3 “Đề xuất tùy chọn”; state rationale and applicability, separate from required findings. With no findings, replace finding blocks by an explicit no-supported-findings statement; do not invent an empty finding. -->

## Coverage và giới hạn

- Coverage: {{Material clauses/branches inspected → assignment/AC/case/variant/gap; justified equivalent coverage; incomplete scope}}
- Checks đã chạy: {{Read/source/template/parity/formula checks actually performed; role backend/independence when used}}
- Checks chưa chạy: {{Application tests/SQL/browser/runtime/render/recalculation not performed or not authorized}}
- Giới hạn: {{Unread sources/artifacts, unknown decisions, missing fixture/proof and minimum next check}}
- Bảo toàn: {{Reviewed input bytes unchanged if verified; otherwise no unsupported preservation claim}}
