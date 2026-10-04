<!-- blend-template: scope-and-approach@1.0.0 -->
# SYN-001 — Eligibility

## Mục tiêu và căn cứ

| Field | Value |
| --- | --- |
| Revision | syn-r2 |
| Nguồn | SPEC:S1–S4 sha256:fixture; confirmation:Q1 Confirmed |
| Căn cứ research | Standalone; verified handler; no live runtime |
| Baseline code | blend:controllers/Eligibility.php synthetic SHA; no execution |
| Mode | design |
| Giới hạn | Static only; import seam missing |

## Phạm vi

| Field | Value |
| --- | --- |
| Trong scope | Eligibility, authorization, boundary, non-target preservation |
| Ngoài scope | None; unanswered custom overflow remains G-01 |
| Vai trò | Teacher owner; visitor denied |

## Chuẩn bị và cách chạy

| Field | Value |
| --- | --- |
| Môi trường | Synthetic isolated school A/year Y, no live data |
| Chuẩn bị | TD-01 and independent reset |
| Chọn lượt chạy | Business flow then ready High cases; no previous-case chain |
| Điều kiện bắt đầu | Known oracle, verified fixture and seam |
| Điều kiện kết thúc | All mandatory assessed with evidence; blockers remain visible |
| Bằng chứng | Request/readback for synthetic fixture; no actual results yet |

## Coverage và gaps

### Coverage

| Clause / anchor | Obligation / branch | Case / variant / gap | Rationale / proof limit |
| --- | --- | --- | --- |
| SPEC:S1 | both predicates eligible; boundary | TC-SYN-01:a, TC-SYN-01:b, TC-SYN-01:c | Single-predicate negative and equality distinguish defects |
| SPEC:S2 | visitor denied and no mutation | TC-SYN-02 | Exercise deny; readback |
| SPEC:S3 | custom overflow oracle pending | G-01 | No assumed rounding |
| SPEC:S4 | import scope preservation | TC-SYN-03 | Known expected; preparation blocked |

### Gaps

| Gap ID | Kind | Known obligation / source | Missing decision / proof | Impact / next check |
| --- | --- | --- | --- | --- |
| G-01 | business | SPEC:S3 custom overflow | Overflow rounding unresolved | No runnable oracle; ask separately |
| G-02 | preparation | SPEC:S4 import scope | Import fixture/seam unavailable | TC-SYN-03 blocked; smallest fixture check |
