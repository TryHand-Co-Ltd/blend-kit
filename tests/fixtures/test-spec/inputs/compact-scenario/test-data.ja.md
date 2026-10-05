<!-- blend-template: test-data@1.0.0 -->
# SYN-SC — 共通データ

## データ規約

| Field | Value |
| --- | --- |
| Revision | compact-r1 |
| Conventions | Synthetic alias。実データ/SQLなし。記述準備はruntime証明ではない。 |

## Fixtures

### Fixture: TD-SC

| Field | Value |
| --- | --- |
| 役割 | Teacher owner; editor A/B for stale scenario |
| 範囲 | Synthetic school A/year Y; non-target B/Z |
| 状態 | Only R1 complete at threshold 30 with <; enabled=yes; stored score 29 red |
| 値 | Target scores 29,30,31; non-target 82; stale R1 version 1 |
| Target・non-target | A/Y target versus B/Z non-target |
| 作成 | Supported synthetic editor must restore complete R1 and all scores; seam pending G-PREP |
| 確認 | Readback R1/threshold/comparator/score/red result/version and non-target 82; seam pending G-PREP |
| Reset | Recreate only complete R1 at threshold 30/<, enabled=yes, scores 29/30/31; verify red score29 and non-target82 independently |
