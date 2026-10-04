<!-- blend-template: scope-and-approach@1.0.0 -->
# SYN-001 — Eligibility

## 目的・根拠

| Field | Value |
| --- | --- |
| Revision | syn-r2 |
| Source | SPEC:S1–S4 sha256:fixture; confirmation:Q1 Confirmed |
| Research根拠 | Standalone; verified handler; no live runtime |
| Code baseline | blend:controllers/Eligibility.php synthetic SHA; no execution |
| Mode | design |
| 調査限界 | Static only; import seam missing |

## 対象範囲

| Field | Value |
| --- | --- |
| 対象 | Eligibility, authorization, boundary, non-target preservation |
| 対象外 | None; unanswered custom overflow remains G-01 |
| 役割 | Teacher owner; visitor denied |

## 準備・実行方針

| Field | Value |
| --- | --- |
| 環境 | Synthetic isolated school A/year Y, no live data |
| 準備 | TD-01 and independent reset |
| 実行選択 | Business flow then ready High cases; no previous-case chain |
| 開始条件 | Known oracle, verified fixture and seam |
| 終了条件 | All mandatory assessed with evidence; blockers remain visible |
| 証拠 | Request/readback for synthetic fixture; no actual results yet |

## Coverage・Gaps

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
