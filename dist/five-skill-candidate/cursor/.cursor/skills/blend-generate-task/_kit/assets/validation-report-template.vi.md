<!-- blend-template: validation-report@1.0.0 -->
<!-- Template instructions: fill actual evidence, remove this instruction. Keep all eight headings. Empty sets explicitly say none. Planned/Failing/Blocked proof cannot become completion; no substitute runtime evidence. Format adapted from ai-workflow docs/templates/validation-report.md. -->
# BLEND Kit — Báo cáo kiểm chứng

## Phạm vi

- Thay đổi được kiểm chứng: [scope thực tế]
- Source contract: [link shared contract/design]
- Plan: [link approved plan]
- Ngày kiểm chứng: [YYYY-MM-DD]
- Runtime/model/version/tool scope: [đã quan sát; agent chưa chạy ghi rõ]

## Đối chiếu proof

| Area / requirement | Proof type | Required? | Status | Evidence | Gap / follow-up |
| --- | --- | --- | --- | --- | --- |
| R1–R14 | [mapping từng yêu cầu; không gộp để che thiếu proof] | Yes | Planned / Passing / Failing / Blocked / Not applicable | [actual path/anchor] | [limit] |
| Template / package | [focused controls; full inventory/build/relocation] | Yes | [observed status] | [evidence] | [gap] |
| Codex / Cursor / Claude | [actual scenario output và semantic scoring từng runtime] | Yes | [observed status mỗi runtime] | [versions/outputs/scoring] | [missing executor/proof] |
| Workbook | [parity/reopen; render và recalculation riêng] | Yes | [observed status] | [actual workbook/cells/screenshots] | [gap] |

## Commands đã chạy

| Command | Result | Evidence |
| --- | --- | --- |
| [exact command và cwd nếu cần, không private paths] | [exit/result thực tế] | [log path/anchor] |

## Checks đã chạy

| Check | Result | Evidence |
| --- | --- | --- |
| [scope cụ thể; structural và semantic riêng] | Passing / Failing / Blocked / Not applicable | [actual evidence] |

## Checks chưa chạy

| Check | Reason | Substitute Evidence |
| --- | --- | --- |
| [required proof chưa có hoặc ngoài scope] | [lý do] | [partial evidence và giới hạn; không coi là proof tương đương] |

## Bằng chứng

- Report/output paths: [actual paths portable]
- Screenshots/render/recalculation: [actual proof hoặc chưa có]
- Tool outputs và targeted searches: [actual evidence]
- Input byte preservation và source revision: [actual checks]
- Independent Spec/Standards review: [actual review và dispositions]

## Gaps

[Remaining risk, missing capabilities, failed scenarios và deferred proof. Mỗi mục có impact và smallest next check; none chỉ khi đã xác minh.]

## Kết quả

[Nêu complete/incomplete scope. Required proof Planned/Failing/Blocked không được claim completion nếu chưa có accepted rationale. Tách package readiness, agent semantic parity và workbook proof. Không claim active cutover, marketplace publication hoặc feature execution.]
