<!-- blend-template: business-questions@1.0.0 -->
# {{機能}} — 業務確認

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,scope,scenario,decision,impact,proposal,question,status. Two required H2s. Each independent leaf uses labels below; shared parent context only when each leaf is unambiguous. Stable Q IDs, one decision per leaf. If no business gap, replace question blocks with “[assessed scope]について、[source revision]時点で未回答の業務確認はありません。” Do not invent questions/answers. Remove instructions/placeholders. -->

## 対象範囲

- 参照元: {{Verified ID/parent、共有link/revision、authority状態}}
- 対象範囲: {{機能、actor、operations、関連する確認済み範囲}}

## 確認が必要な質問

### {{Q ID}} — {{一つの業務判断}}

- 状況: {{画面/機能、role、具体条件、確認した現行挙動}}
- 判断事項: {{未確定事項；確認済み内容や調査可能なcode factを再質問しない}}
- 影響: {{選択による結果・保留範囲・進められる部分}}
- 選択肢: {{実際の選択肢と効果；単一確認なら不要な二択を作らない}}
- 提案: {{未承認proposal、理由/trade-off；証拠不足なら最小investigationと選択基準}}
- 確認依頼: {{中立で独立して回答できる一つのdecision}}
- 状態: {{Awaiting decision、または根拠のあるauthorized answer；別leafの回答で閉じない}}
