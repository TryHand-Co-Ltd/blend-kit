<!-- blend-template: business-questions@1.1.0 -->
# {{機能}} — 業務Q&A

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,scope,scenario,decision,impact,proposal,question,status. Use customer-facing paragraphs and option/impact tables, not seven repeated field bullets. Keep both numbered H2 sections. Introduction carries source/scope, and sections distinguish actual/provisional answers from unanswered proposals. Answers never imply approval of the entire specification. If no answers exist, replace answered entries with a scoped “回答済みQ&A：なし。” statement; do not turn requirements/default proposals into answers. If no open questions remain, use a scoped “未回答の業務確認：なし。” statement. Remove instructions/placeholders. -->

更新日：**{{更新日}}**。

対象・参照元：{{確認する機能・操作と共有要求元または依頼受領日。読者に必要な情報だけを記載し、ローカルpath、コード、調査logや技術metadataは含めない。}}

## 1. 回答を得ているQ&A

{{回答済み項目の確認程度と根拠。再回答を求めるものではないことを示す。}}

### {{Q ID}} — {{回答を得ている質問}}

**現状と課題。** {{具体的な状況と確認した内容。}}

**回答を得ている内容。** {{実際の回答、対象範囲、根拠/日付。暫定回答・確認済み・既存要求を区別し、回答を捏造しない。}}

## 2. 未回答のQ&A

以下の案は提案段階であり、合意済みの決定事項ではありません。

### {{Q ID}} — {{確認が必要な業務判断}}

**現状と確認したい点**

{{具体状況、結果の違いを示す例、一つの未確定判断。状況/判断事項/影響/状態を反復する欄には分けない。}}

| 案 | 処理 | 影響 |
| --- | --- | --- |
| A — {{案の名称}} | {{Aの操作と結果}} | {{利点と制約}} |
| B — {{案の名称}} | {{Bの操作と結果}} | {{利点と制約}} |

**提案：** {{推奨案、理由とtrade-off。未承認提案であることを維持する。}}

**確認：** {{独立して回答できる中立な一つの質問。}}

<!-- TEMPLATE INSTRUCTIONS: Related decisions may share the parent context. Use bold child headings “**Q ID.1 — Decision**”, “**Q ID.2 — Decision**”, etc. Each child has specific context where needed, its own option/impact table, 提案 and 確認; an answer to one child never resolves siblings. Keep existing IDs. Use the three-column table for real alternatives; omit it for a genuine single confirmation rather than inventing A/B options. A short question may use inline “**現状と課題。**” instead of the block context. Per-question state is needed only for a different answer state; unanswered status is inherited from section2. Do not re-ask settled questions or ask the customer to select discoverable code/schema details. -->
