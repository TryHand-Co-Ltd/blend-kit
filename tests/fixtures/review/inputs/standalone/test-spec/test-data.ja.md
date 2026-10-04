<!-- blend-template: test-data@1.0.0 -->
# FX-REVIEW — Data

## データ規約

| Field | Value |
| --- | --- |
| Revision | design-v2 |
| Conventions | Synthetic aliases only; fixture-preparation.md; no real personal/secrets |

## Fixtures

### Fixture: TD-01

| Field | Value |
| --- | --- |
| 役割 | admin/teacher aliases; actor per variant |
| 範囲 | S-A/Y-2/C-A; all three non-target sentinels |
| 状態 | saved rows exist; enabled configurable; missing-score preparation unavailable |
| 値 | T1=17; inputs 79/80/81; percent results79.9/80.1 |
| Target・non-target | T1 and N-school=31 only |
| 作成 | Use preloaded isolated fixture alias as fixture-preparation.md; no SQL |
| 確認 | Verify scope/role/saved values and flags before each case |
| Reset | Next case restores the state |
