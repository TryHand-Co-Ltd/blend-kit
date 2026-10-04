<!-- blend-template: scope-and-approach@1.0.0 -->
# FX-REVIEW — Test scope

## 目的・根拠

| Field | Value |
| --- | --- |
| Revision | design-v2 |
| Source | FX-REVIEW SPEC.md revision 2; confirmation.md Q1-Q4 |
| Research根拠 | Standalone raw source/context plus decisive guards/code |
| Code baseline | Synthetic source snapshot; no Git/runtime; see SNAPSHOT.md |
| Mode | standalone |
| 調査限界 | No runtime/render/recalculation proof |

## 対象範囲

| Field | Value |
| --- | --- |
| 対象 | C1-C8 alert setting/recalculation/result preservation |
| 対象外 | Existing score entry; not changed |
| 役割 | school-admin; teacher negative role |

## 準備・実行方針

| Field | Value |
| --- | --- |
| 環境 | isolated synthetic fixture harness, not production |
| 準備 | fixture-preparation.md; missing-score fixture unavailable |
| 実行選択 | Flow order; High first respecting readiness |
| 開始条件 | Confirmed oracle and prepared fixture; blocked case not runnable |
| 終了条件 | No complete execution claim with gaps |
| 証拠 | Record before/after target and sentinel values, role/error response |

## Coverage・Gaps

### Coverage

| Clause / anchor | Obligation / branch | Case / variant / gap | Rationale / proof limit |
| --- | --- | --- | --- |
| SPEC.md C1 | configuration and trigger/observation | TC-01:below | Design mapping only; no executed proof |
| SPEC.md C2 | below/equal/above threshold | TC-01:below | Design mapping only; no executed proof |
| SPEC.md C3 | percentage truncation | TC-02:fraction | Design mapping only; no executed proof |
| SPEC.md C4 | school/year/course isolation | TC-04:base | Design mapping only; no executed proof |
| SPEC.md C5 | server role rejection | TC-03:admin | Design mapping only; no executed proof |
| SPEC.md C6 | disabled preserves rows | TC-05:base | Design mapping only; no executed proof |
| SPEC.md C7 | subtraction rounding undecided | TC-07:base | Design mapping only; no executed proof |
| SPEC.md C8 | missing source error preserves all rows | TC-06:base | Design mapping only; no executed proof |

### Gaps

| Gap ID | Kind | Known obligation / source | Missing decision / proof | Impact / next check |
| --- | --- | --- | --- | --- |
Gapsなし。
