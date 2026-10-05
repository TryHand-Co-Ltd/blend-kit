# SYN-SC — grouping評価用synthetic source

以下はfixtureのoracleのみでBLEND新要求ではない。旧IDはmapping評価用、actual/status/evidenceは含まない。

| Anchor | Old Case/Variant | Inputs / transition | Required outcome | Meaning |
| --- | --- | --- | --- | --- |
| O1 | TC-OLD-LT:base | T=30, S=29/30/31, comparator < | red/not red/not red | 閾値<で29/30/31を正しく判定する。 |
| O2 | TC-OLD-LE:base | T=30, S=29/30/31, comparator ≤ | red/red/not red | 閾値≤では等値の結果が異なる。 |
| O3 | TC-OLD-CANCEL:base | Persisted rule R1; choose cancel | R1 remains; stored result and score unchanged | 削除取消でrule・結果・点数を維持する。 |
| O4 | TC-OLD-CONFIRM:base | Persisted last rule R1; choose confirm; recalculate | R1 removed; old red result kept before recalculation; recalculation clears red only | 最後のruleを削除し、再判定前は結果を維持、再判定後は赤点だけを解除する。 |
| O5 | TC-OLD-INCOMPLETE:base | Save rule R1 without threshold | Incomplete R1 is retained; judgment excludes it | 閾値未入力ruleは保存されるが判定対象外。 |
| O6 | TC-OLD-STALE:base | Editor A opened R1; editor B deletes R1; A saves stale form | Save rejected; deleted R1 not recreated; score unchanged | 削除後の古いform保存は拒否し、ruleを再作成しない。 |
| O7 | TC-OLD-AND-POSITIVE:base | Enabled=yes, S=29, T=30 | eligible | enabledとscore<Tが両方成立するとAND適合。 |
| O8 | TC-OLD-AND-NEGATIVE:disabled, TC-OLD-AND-NEGATIVE:boundary | Enabled=no with S=29; enabled=yes with S=30 | not eligible for either single-predicate-negative | AND各条件の単独negativeを検査し、他の条件は成立させる。 |

O8は独立した二negative。Incompleteとstaleを同じ結果にしない。指定delta以外の数値点/non-targetは不変。準備/readback未検証:G-PREP。
