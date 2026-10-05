<!-- blend-template: research@1.1.0 -->
# Research — {{調査するtopic・フロー}}

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,basis,topic,purpose,scope,dependencies,currentness,clauses,flow,impact,gaps,proof. Four H2 headings and labels are required. Destination: verified feature-root research/<topic>.ja.md; meaningful question/flow, no default whole-feature/trivial/empty output. Basename follows registry; Task ID prefix only when verified, preserving case/zeros and immediate parent. Replace placeholders and remove instructions. Optional ResearchHandoff H3 only when effective user prompt requests Test Spec; exactly eight shared fields, mode outside fields. Empty impact/gaps explicitly state assessed none and scope. Do not invent observations. Legacy research@1.0.0 remains read-only at its original baseline. -->

## 対象・根拠

- 参照元: {{原文ID、確認済み直属parent、URL/anchor、revision/content identity、authority}}
- 根拠: {{受領Spec、current context、適用を許可された最新確認；proposal/conflictを区別}}
- 主題: {{Topic名と再利用する質問・フロー；basenameだけでIDを証明しない}}
- 目的: {{解決する問題、具体的な質問、再利用する結論}}
- 対象範囲: {{Actor、機能、operation、根拠のある対象/除外、要求output/language/destination}}
- Code baseline: {{Git SHAと関連staged/unstaged/untracked/deleted内容identity；blend:path；access限界}}
- 許可された参照元: {{Context/code/public sourceと除外；外部助言のversion/applicabilityは業務承認ではない}}
- 現行性: {{確認範囲のCurrent/stale/unverified；captured file identitiesとdependenciesの照合時点；関連delta・誤った結論は影響範囲をDraftに保持；SHA/mtimeだけで正しさを推定しない}}

## 要求・現行フロー

| 条項・分岐とanchor | Actor・action・条件 | 結果・保持する状態 | As-Isと証拠 | To-Be・authority | 担当範囲・ACまたはgap |
| --- | --- | --- | --- | --- | --- |
| {{Clause ID・branch}} | {{独立した状況}} | {{Outcome/exception/preservation}} | {{Anchor・revision；未確認を明示}} | {{Confirmed/Proposed/Awaiting decision}} | {{Assignment/ACまたはgap}} |

- 現行フロー: {{Entry/route → 権限/validation → inputs/settings/branches → 保存 → readback → consumers/lifecycle；sourceとruntimeを区別}}
- 置換済み範囲: {{Canceled/superseded scope；なければ確認範囲内でなしと記載}}

## 影響・依存

| Surface・operation | 分類 | 根拠のある変更・理由 | Owner・prerequisite | 検証方法 |
| --- | --- | --- | --- | --- |
| {{確認したscreen/API/job/storage/consumer}} | {{Direct/dependency/regression-only/unresolved}} | {{Requirementとengineering proposal}} | {{一つのowner、具体的な入力成果}} | {{Proof限界}} |

- 影響: {{Storage/identity/relationship/data lifecycle変更の要否；条件付きDB Designの理由}}
- 依存: {{質問・結論・条項ごとのsource/code/confirmation path+anchor、revision/content/working identity；capture不足は限界；開始・統合条件；Task IDを作らない。選択した実際のtopic filesとper-file captured identitiesのみ、folder digestなし；無関係topicでfeature全体を無効化しない}}

## Gaps・調査限界

| Gap ID | 種類 | 未知・既知 | 影響 | 最小の次の確認・判断role | 状態 |
| --- | --- | --- | --- | --- | --- |
| {{Stable ID}} | {{Fact/engineering/business/preparation-proof}} | {{Oracle/fixture不足で要求を削除しない}} | {{対象clause/assignment/AC}} | {{Research/checkまたは独立Q leaf}} | {{Open/根拠のあるsettled}} |

- 証拠: {{実際に確認したsource/code；tool fallback/外部source applicability；未実行check；DB/UI/runtime/releaseを推定しない}}
- 対応確認: {{Source → assignment/ACまたはgapと逆方向；supported/blocked範囲}}

<!-- OPTIONAL: If Test Spec requested, emit the transient ResearchHandoff after saving final topic bytes with source, authorized_sources, source_basis, code_baseline, research_snapshot, languages, output_scope, limitations. Snapshot names selected actual saved topic paths + captured byte identities + consumed questions/clauses + decisive dependency identities, never folder digest or self-hash embedded in captured file. An optional H3 ResearchHandoff may explain selected reuse/dependencies; final captured identities belong in the transient invocation. Freeze during consumption; scoped delta only for relevant drift. Actual roots stay transient; shared paths are repository-relative. Remove instruction. -->
