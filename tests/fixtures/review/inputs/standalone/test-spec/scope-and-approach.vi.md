<!-- blend-template: scope-and-approach@1.0.0 -->
# FX-REVIEW — Test scope

## Mục tiêu và căn cứ

| Field | Value |
| --- | --- |
| Revision | design-v2 |
| Nguồn | FX-REVIEW SPEC.md revision 2; confirmation.md Q1-Q4 |
| Căn cứ research | Standalone raw source/context plus decisive guards/code |
| Baseline code | Synthetic source snapshot; no Git/runtime; see SNAPSHOT.md |
| Mode | standalone |
| Giới hạn | No runtime/render/recalculation proof |

## Phạm vi

| Field | Value |
| --- | --- |
| Trong scope | C1-C8 alert setting/recalculation/result preservation |
| Ngoài scope | Existing score entry; not changed |
| Vai trò | school-admin; teacher negative role |

## Chuẩn bị và cách chạy

| Field | Value |
| --- | --- |
| Môi trường | isolated synthetic fixture harness, not production |
| Chuẩn bị | fixture-preparation.md; missing-score fixture unavailable |
| Chọn lượt chạy | Flow order; High first respecting readiness |
| Điều kiện bắt đầu | Confirmed oracle and prepared fixture; blocked case not runnable |
| Điều kiện kết thúc | No complete execution claim with gaps |
| Bằng chứng | Record before/after target and sentinel values, role/error response |

## Coverage và gaps

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
Không có gaps.
