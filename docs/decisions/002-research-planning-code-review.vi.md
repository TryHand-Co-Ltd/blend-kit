# 002 — Research theo chủ đề, shared planning và common code review

## Status

Accepted — 2026-10-02. Người dùng duyệt design 000003, chốt D1/D2 và duyệt plan 000004 với Parallel. Quyết định này bổ sung [decision 001](001-blend-kit-workflow.vi.md); không sửa lịch sử approval/proof của bộ ba skill, không authorize activation/publication hoặc implementation feature.

## Context và căn cứ

Một file Research mặc định không biểu đạt được nhiều câu hỏi/baselines trong feature. Team cần plan portable theo scope đã duyệt và review actual diff/shared consumers/DB risks. Tách policy Bug Hunter thành hai bản sẽ gây drift; dùng protocol shared và giữ kiểm tra đặc thù từng reviewer.

| Artifact | Căn cứ |
| --- | --- |
| Design | [Approved design 000003](../plans/2026-10-02-000003-research-planning-code-review-design.vi.md), D1–D5 và N1–N11. |
| Plan | [Approved plan 000004](../plans/2026-10-02-000004-research-planning-code-review-plan.vi.md), T1–T7 và một Verify Gate. |
| Contract | [Workflow](../../shared/workflow.md), [Registry](../../shared/artifact-formats.md), [Common review policy](../../shared/review-policy.md), [Pinned role protocol](../../shared/bug-hunter.md). |
| Lịch sử | [Decision 001](001-blend-kit-workflow.vi.md) và validation/runtime snapshots của ba skill giữ nguyên phạm vi chứng cứ cũ. |

## Decision và tác động

- Chọn feature-root `research/<topic>.ja.md`/`.vi.md` cho vấn đề/luồng có kết luận dùng lại được; authorized query draft `<topic>.sql` khi có câu hỏi cụ thể. Không mặc định một file toàn feature, không scaffold rỗng, không move historical Research/DB SQL. Metadata ghi verified task/scope/parent khi thuộc task; task docs link tới một bản canonical.
- Shared implementation plans ở feature-root `plans/<scope>-implementation-plan.ja.md`/`.vi.md`, gồm cả approved task slices. Plan portable, nguồn/review/approval revisions tách riêng; private operational plans giữ private. Planning tạo plan Draft từ approved scope, không tạo Design hay tự execute.
- Năm skill dùng chung authority/template contract. ResearchHandoff vẫn đúng tám fields, snapshot pin selected actual files và per-file identities/dependencies; topic không liên quan không tự invalidate tất cả.
- Code review pin actual base/head/worktree và đọc assigned changes cùng bounded consumers. Scope/origin/severity/confidence/effect độc lập; OOS introduced/worsened regression không được bỏ. Acceptance/spec/tests/standards tách khỏi behavioral validity và runtime/release proof.
- Cả reviewers dùng một pinned Bug Hunter v3.2.0 adaptation/commit với MIT license giữ nguyên bytes. Actual Hunter/Skeptic/Referee hoặc disclosed sequential fallback; inline disposition, không fake role runs, Fixer/install hoặc manifests mới.
- Topic Research dùng `research@1.1.0` vì thêm required topic/purpose/dependencies/currentness; legacy `1.0.0` chỉ đọc với schema cũ, SQL contract không đổi vẫn `1.0.0`. Mandatory JA/VI template mappings mới `implementation-plan` và `code-review` là Planned đến khi matching assets tồn tại. Focused controls có thể pass trước asset creation; full inventory không được pass khi thiếu assets/groups.

## Trade-offs và follow-up

Phải cập nhật governance, selective-topic consumers, templates và build closure của năm skill trên ba runtime. Structural/profile equality không chứng minh semantic parity; cần actual source-bound writer/reader/role evidence. T2–T4 tạo assets/fixtures theo T1 interfaces; T5–T7 tích hợp, build candidate và ghi proof/gaps. Active `.agents`, config, legacy distributions/snapshots/results và unrelated dirty files giữ nguyên. Chưa có research Markdown trong context để di chuyển; không tạo feature business artifacts vì thay đổi governance.

## Review trigger

Đối chiếu lại khi source/approval/topic dependency hoặc template family thay đổi, khi raw fixture/role output chứng minh drift, hoặc khi runtime không resolve bundled resources. Thay đổi kit không nâng technical advice thành yêu cầu confirmed và không cấp quyền Git/external/DB/release mới.
