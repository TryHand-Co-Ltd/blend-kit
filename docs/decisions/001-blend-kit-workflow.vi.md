# 001 — Một workflow và bộ template cho BLEND Kit

## Status

Accepted — 2026-10-02. Người dùng duyệt thiết kế, yêu cầu template bắt buộc cho mọi output, duyệt phạm vi Review Artifacts và chọn Parallel. Chưa cho phép activate hay publish.

## Context

Bộ active còn phụ thuộc bố cục workstation, ngôn ngữ Nhật–Anh và output `unit-tests`. Task generation có thể gọi test writer khi người dùng chỉ cần task. Format đã chốt trong `blend-context` cần được dùng nhất quán cho ba agent; một tài liệu hợp lệ headings vẫn có thể sai expected hoặc thiếu branch. Vì vậy phát triển nguồn mới riêng tại `blend-kit`, giữ nguyên bộ active và các tài liệu lịch sử.

## Linked Artifacts

| Artifact | Path | Notes |
| --- | --- | --- |
| Contract | [Shared workflow](../../shared/workflow.md), [Artifact formats](../../shared/artifact-formats.md) | Discovery, authority, ownership, handoff và template registry dùng chung. |
| Story | Không có | Một thay đổi coherent của package, không tạo story hierarchy. |
| Plan | Approved plan | R1–R14 và sáu implementation slices; user đã chọn Parallel. |
| Design | Approved design | Format sources, trade-offs và semantic proof. |
| Validation | [Validation template](../../assets/validation-report-template.vi.md) | Report actual sẽ ở `docs/test_results/blend-kit-validation.vi.md` khi T6 tạo; chưa có runtime proof. |

## Options

| Option | Description | Pros | Cons |
| --- | --- | --- | --- |
| A | Sửa bộ active và export ZIP tiếp | Ít bước đóng gói ban đầu | Có thể làm hỏng workflow hiện dùng; portability/template/runtime proof chưa rõ. |
| B | Ba bộ workflow cho Codex/Cursor/Claude | Tùy chỉnh từng runtime | Tăng policy/template drift và ba nguồn maintain. |
| C | Một nguồn BLEND Kit với shared contract/templates và runtime targets được build | Cùng nghĩa/output contract, dễ review và rollback | Cần focused checks và actual semantic evaluation trên từng runtime. |

## Decision

Chọn C. Chỉ ba skill: `blend-generate-task`, `blend-generate-test-spec`, `blend-review-artifacts`. Áp dụng các binding requirements R1–R14 của plan; không mở thêm PR/QA scope hay business approval.

- Resolve actual workspace/app/context và verified identity; package cache không xác định nơi checkout. Current spec/context/authorized confirmations quyết định nghiệp vụ; source code là As-Is, external research là technical advice.
- Task chỉ invoke Test Spec khi prompt yêu cầu theo nghĩa; phủ định/subset có hiệu lực. Database Design chỉ cho task có DB design change, SQL không thực thi.
- Standalone Test Spec tự research; handoff mode kiểm decisive frozen basis. Ba Markdown families + workbook cùng revision, business-flow grouping, source-to-case/variant-or-gap và ba trục expected/readiness/execution.
- Nhật–Việt mặc định; requested subsets ưu tiên, historical files giữ nguyên. Mọi generated output bắt buộc dùng canonical template/version; thiếu template thì capability gap, không tự dựng format hay giả content.
- Review cả Task/Test Spec/combined bundles theo assigned scope, kiểm nguồn/code/template/coverage/fixture/workbook và đề xuất cập nhật có bằng chứng. Read-only và stable finding IDs/closure evidence.
- Package checks không chứng minh chất lượng giữa agent; cần actual Codex/Cursor/Claude outputs, semantic scoring và workbook render/recalculation. Runtime/evidence thiếu giữ Blocked.

## Consequences

Positive:

- Member có cùng workflow/template dù workspace khác tên/vị trí hoặc dùng agent khác.
- Output inventory, oracle/gaps và update proposals review được mà không cần lịch sử chat.
- Một nguồn template và same-revision workbook giảm expected drift; skill generation không mở rộng quyền thực thi.

Trade-offs:

- Phiên bản mới không tự migration historical `unit-tests` hoặc sửa active registrations; cutover cần yêu cầu riêng.
- Unsupported output/language cần mapping/template trước; không thể coi generation tùy ý là hoàn tất.
- Structural checks, actual semantic evaluation và workbook rendering là proof riêng, nên một package build tốt vẫn có thể thiếu proof để bàn giao.

## Follow-Up

- Required docs updates: T2/T3/T4 implement registry assets/workflows; T5 onboarding và portable target distributions. Không đổi active skills/config.
- Required proof: focused valid/invalid controls, full inventory/relocation gate và T6 actual runtime/semantic/workbook evidence; final Spec/Standards reviews theo plan.
- Owner: controller điều phối một writer cho mỗi path; từng task producer giữ owned scope.

## Review Trigger

Revisit khi nguồn requirements/format thay đổi, có output family/language mới, runtime không discover được resources hoặc semantic evaluation tìm ra lỗi. Không dùng thay đổi package làm lý do nâng proposal nghiệp vụ thành confirmed hay publish ngoài authorization.
