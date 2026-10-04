<!-- blend-template: test-data@1.0.0 -->
# SYN-001 — Shared data

## データ規約

| Field | Value |
| --- | --- |
| Revision | syn-r2 |
| Conventions | Synthetic aliases only; never execute app/SQL; values are fixture design |

## Fixtures

### Fixture: TD-01

| Field | Value |
| --- | --- |
| 役割 | Teacher owner and visitor |
| 範囲 | School A/year Y target; B/Z non-target |
| 状態 | Enabled; max=100; score=59; no pending write |
| 値 | Distinct target=59, non-target=82 |
| Target・non-target | A/Y versus B/Z |
| 作成 | Use synthetic supported fixture editor |
| 確認 | Readback both scope and initial values |
| Reset | Restore enabled/max/score and verify both records |
