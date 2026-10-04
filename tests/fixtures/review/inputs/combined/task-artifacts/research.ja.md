<!-- blend-template: research@1.0.0 -->
# Research — FX-REVIEW alert settings



## 対象・根拠

- 参照元: FX-REVIEW SPEC.md revision 2; confirmation.md Q1-Q4
- 根拠: CONTEXT.md revision2; code As-Is; external advice not approval
- 対象範囲: Alert settings/recalculation for school/year/course; existing score entry preserved
- Code baseline: Synthetic app snapshot, not Git/deployed; application/services/AlertService.php
- 許可された参照元: Only supplied raw source pack, no external/customer sources

## 要求・現行フロー

| 条項・分岐とanchor | Actor・action・条件 | 結果・保持する状態 | As-Isと証拠 | To-Be・authority | 担当範囲・ACまたはgap |
| --- | --- | --- | --- | --- | --- |
| C1-C8 source clauses | School-admin recalculates selected S-A/Y-2/C-A | Alerts at score <= threshold; fractional percentages round to 80; no unresolved decisions | application/services/AlertService.php supports inclusive comparison and rounding | Confirmed from code | Local assignment 1 / AC-01 |

- 現行フロー: Alert Settings -> server role guard -> target writes -> Score Results; source only
- 置換済み範囲: Inclusive comparison draft has not changed

## 影響・依存

| Surface・operation | 分類 | 根拠のある変更・理由 | Owner・prerequisite | 検証方法 |
| --- | --- | --- | --- | --- |
| Recalculate and saved score results | Direct | Add new alert_config unique school/course; all years share values | Local task1; existing storage reused until table design | Inspect design only |

- 影響: Storage must change; authorized mandatory new table inferred from template sample
- 依存: No prerequisites

## Gaps・調査限界

| Gap ID | 種類 | 未知・既知 | 影響 | 最小の次の確認・判断role | 状態 |
| --- | --- | --- | --- | --- | --- |
| G-ROUND | business | Subtraction rounding deemed settled by current code | C7 acceptance becomes Confirmed | No additional business decision required | settled |

- 証拠: Source inspection only; no app/SQL/render executed
- 対応確認: All C1-C8 covered by AC-01 and no gaps
