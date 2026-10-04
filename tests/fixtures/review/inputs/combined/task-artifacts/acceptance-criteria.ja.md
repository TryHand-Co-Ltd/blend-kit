<!-- blend-template: acceptance-criteria@1.0.0 -->
# FX-REVIEW alert configuration — 受入条件



## 対象範囲

- 参照元: FX-REVIEW SPEC.md revision2; confirmation.md
- 対象範囲: School-admin configuration and recalculation; existing score entry unchanged

## 受入条件

### Configure and recalculate

- [ ] **AC-01 — Alert at threshold:** Actor: school-admin。条件: score=80; threshold=80; selected school/year/course。結果: alert=true。例外: Disabled state also recalculates。保持: Only other school values preserved。根拠: Confirmed from generated Research, including subtraction rounding by analogy。
