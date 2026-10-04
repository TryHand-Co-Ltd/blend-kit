<!-- blend-template: research@1.1.0 -->
# Research — 得点分類の境界

## 対象・根拠

- 参照元: Synthetic Work Item SYN-TOP-042; Task SYN-TOP-042-A; immediate parent SYN-TOP-042; sources/spec.md revision 1.
- 根拠: CONTEXT.mdとsources/confirmation.md revision 1がfixtureの現行authority；codeはAs-Isのみ。
- 主題: SYN-TOP-042-A-threshold-boundary；得点の境界条件。
- 目的: C-BOUNDARYのthreshold未満・同値・超過と保持条件を確認する。
- 対象範囲: 確認したTaskの得点分類；C-EXPORTのcaptionはこの質問の対象外。
- Code baseline: Git SHAなし；Score.phpのbytesは以下でcapture；static sourceのみ。
- 許可された参照元: Fixtureのraw sourcesのみ；remote、SQL、runtimeなし。
- 現行性: Capture revision 1ではCurrent；reuse前にdependenciesを照合；SHA不変だけでは結論の正しさを証明しない。

## 要求・現行フロー

- C-BOUNDARY: Threshold 60でscore 59は赤点、60/61は赤点でない。Confirmationはstrictly belowを要求。
- 現行フロー: Score.php isRedはscore/thresholdを受け取りscore < thresholdを返す；fixtureにroute/persistence証拠なし。
- 置換済み範囲: 確認範囲ではなし。

## 影響・依存

- 影響: Storage変更なし；Test Specは同値と未満を区別する値が必要；DB Design要求なし。
- 依存: C-BOUNDARYは以下のcontext/spec/confirmation/Score.php identitiesに依存；export topicはdependencyでない。

| Dependency path / anchor | Captured SHA-256 | Consumed clause |
| --- | --- | --- |
| CONTEXT.md | 92c5085a7bb0872796c977bbb07d6920280b99ea6d50ad466bae253cb8725d5e | C-BOUNDARY |
| sources/spec.md | 73e53e752b9691921bcc52c9b38bd7a4fc50263129b116704ac2c64cbe9ff2a2 | C-BOUNDARY |
| sources/confirmation.md | 21985b19ba14fa0ea0137e16bcce80b2cd2d45bdde388743a13a9ee002f1273d | C-BOUNDARY |
| Blend-source/application/models/Score.php | aa10cef6aec3bbb4298cf0fd56af5f83eb835a1bad0098948d06f2e52f63f093 | C-BOUNDARY |

## Gaps・調査限界

- G-SEAM: preparation — route/runtimeなし；expectedは確認済みだがseamのtestcaseはReadyでない。
- 証拠: Source readsのみ；PHP/SQL未実行；UI/DB/release証明なし。
- 対応確認: C-BOUNDARY → 未満/同値/超過の検証またはseam gap；codeから要求を変更しない。
