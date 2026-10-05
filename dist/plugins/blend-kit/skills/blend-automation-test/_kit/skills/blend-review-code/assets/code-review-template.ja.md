<!-- blend-template: code-review@1.0.0 -->
# 実装レビュー — {{scope}}

<!-- 七つのH2を順番どおり保持し、該当なしは対象と理由を明記する。完成時に指示・placeholderを削除する。有効なHunter完了後のみ候補なしと記載し、出力欠落を問題なし扱いしない。 -->

<!-- Semantic schema: identity,source_plan_revisions,base_head,working_identity,intended_scope,actual_diff,inspection_inventory,prior_findings,finding_id,requirement,invariant,evidence,actor_trigger,expected_actual,impact,counter_evidence,proposal,verification,scope,origin,severity,confidence,completion_effect,consumer_impact,db_risk,role_disposition,verdicts,limits; labels below map one-to-one in this order. -->

## 結論・レビュー根拠

| 項目 | 確認した根拠 |
| --- | --- |
| 識別情報 | {{確認済みFeature・Task・参照元・正確な親ID、現在のauthority識別情報}} |
| 参照元・計画Revision | {{承認済みPlan・AC・Reviewのrevisionとcontent identity、承認元・role・日付・scope、選択Topicと依存のidentity}} |
| Base・Head | {{可搬なApplication識別情報、実Base・Headまたは検証済みmerge-base、含まれるcommitsとrangeの意味、不明なbaselineを明記}} |
| 作業内容識別 | {{Staged・Unstaged・関連Untracked・Rename・Deleteのbyte identity、Dirty捕捉の限界}} |

## 予定・実差分・調査範囲

予定業務範囲: {{割り当てられた承認済み結果・除外・維持動作、Planで予定した変更箇所}}

実差分: {{実変更のpaths・hunks・分類・identity、予定外変更と未達結果}}

調査一覧: {{各割当path・hunkまたは具体的リスクのconsumer、実際の確認方法、確認済み・未確認と限界}}

前回Findings: {{初回はなし、再レビューは前回reportのrevision・IDsと下記の証拠Ledger}}

## Findings・更新提案

<!-- 根拠のあるFindingがない場合は、対象・depth・未確認部分を明記した結果でentryを置き換える。H2は空にしない。 -->

### {{安定Finding ID}} — {{タイトル}}

Finding ID: {{参照する正確なroot・triggerの安定ID}}

要求: {{適用中AC・参照元・ruleの正確なanchorとauthority}}

Invariant: {{必須contractまたは維持する動作}}

証拠: {{実際の可搬file・line・revision、根拠となるBase・Currentフローと確認方法}}

Actor・Trigger: {{Actor・権限・state・input・entry、具体的な失敗trigger}}

Expected・Actual: {{参照元に基づくExpectedと確認したActualの比較}}

影響: {{影響を受けるusers・data・flowと具体的な結果}}

Counter-evidence: {{保護caller・guard・例外、同条件のBase・Current到達性を確認、不明な証拠}}

更新提案: {{何を・どこで・なぜ更新するか、対象obligations・consumersと維持動作、oracleを創作しない}}

修正後の確認: {{有限で不具合を識別する確認、提供済み・不足proof、将来のPASSを記載しない}}

対象範囲: {{IN_SCOPE / OUT_OF_SCOPE / UNRESOLVEDと割当根拠}}

Origin: {{INTRODUCED / WORSENED / PRE_EXISTING / UNKNOWNと同条件baseline比較}}

Severity: {{具体的影響に基づくCritical / High / Medium / Low}}

Confidence: {{証拠の強さと未解決path、Severityから独立}}

完了への影響: {{Task blocker / Regression blocker / Release risk / Follow-up / Needs evidenceと理由}}

限界: {{未読scope、不足Role・Source・Runtime・DB・Release proofと有限の残確認、StaticからRuntimeを推定しない}}

## 共有フロー・DBリスク

Consumerへの影響: {{具体的な共有Consumers、risk・flow、確認結果・方法または限界、非該当は対象を明示}}

DBリスク: {{影響のあるSchema・Data・Migration・Replicaリスク、提供証拠と有限の不足確認、非該当は明示}}

<!-- Conditional H3 DB/migration detail is required only when affected; omit otherwise, keep H2 and scoped none statement. -->

### DB・Migration詳細（影響がある場合）

{{Designと実Type・NULL・Default・Identity・Relationships・Collation・Index・Query、既存Rows・NULL・Duplicates・Backfill・School-Year、保全・Partial failure・Rerun・Compatibility・Order・Rollback、Engine・Version・Shape・Volume・Lock・Rebuild適用性とGaps、Replica start/end・Early exits・Read-after-write、Live DB・SQL実行なし}}

## 候補・ロール判定

RoleDisposition: {{下記の実際の十一Fields、必須Role出力が欠落・不正ならUNREVIEWED、Roleを創作しない}}

<!-- RoleDisposition schema comes from shared/bug-hunter.md; one inline entry per actual role/candidate. Native distinct agents when available/authorized; local-sequential independent=false disclosed at each claim. Zero candidates: completed valid Hunter NO_CANDIDATES; Skeptic/Referee not-run with reason. Missing/empty/malformed output: UNREVIEWED and exact gap, never clean. -->

| Field | 実際の結果 |
| --- | --- |
| candidate_id | {{安定ID、noneは有効なHunterが完了し候補なしの場合のみ}} |
| role | {{Hunter / Skeptic / Referee、省略Roleの名前と理由を明記}} |
| run_identity | {{実際に返されたAgent・Run IDとStatus、または正直なLocal pass ID、IDを創作しない}} |
| backend | {{実際のNative backendまたはlocal-sequential、利用不可Capabilityを明記}} |
| independent | {{実際に別Agentの場合のみtrue、Local sequentialはfalse}} |
| basis | {{同じSource・Context・Code・Base・Head・Working・Topic identities、Drift・Refreshを明記}} |
| evidence | {{確認したSource location・Revision、Trace・Trigger・結果・実方法、候補なしのnoneは理由付き}} |
| counter_evidence | {{保護Caller・Guard・例外、同条件Baselineの確認、反証なしはBug立証ではない}} |
| verdict | {{Hunter CANDIDATE / NO_CANDIDATES、Skeptic STANDS / DISPROVED / UNCERTAIN、Referee REAL_BUG / NOT_A_BUG / MANUAL_REVIEW、必須出力欠落・不正はUNREVIEWED}} |
| depth | {{direct-source / evidence-only / not-run、Source確認は実行Reproductionではない}} |
| limits | {{未解決Path・未読Scope・不足Role・Tool・Proof・独立性低下、noneは実際にない場合のみ}} |

## 範囲外・既存・未解決

{{本体Finding IDを参照し、owner・scope・origin・effectを独立に記載。OUT_OF_SCOPEでも新規・悪化した回帰はblocker。無関係と立証した既存不具合はfollow-up。不明は追加証拠が必要で黙って除外しない}}

<!-- Prior-finding ledger is required only on re-review; omit H3/table on initial review, keep H2. -->

### 前回Finding Ledger

| ID | Prior revision / evidence | OPEN / FIXED_VERIFIED / DISPROVED / DEFERRED / NEEDS_EVIDENCE | Current evidence / reason / proof limit |
| --- | --- | --- | --- |
| {{前回の安定ID}} | {{実際の前回Revision}} | {{証拠に基づくStatus}} | {{変更と実際に確認したclosure proof、承認済み延期はFixedではない}} |

## 受入判定・証拠限界

独立判定: {{割当Acceptance・Regression・Standards・DB risk・Runtime/QA/Release proofを独立に根拠・status付きで記載}}

限界: {{未読scope、不足Role・Source・Runtime・DB・Release proofと有限の残確認、StaticからRuntimeを推定しない}}

実施したChecks: {{実際の方法・結果・Scopeのみ、Source確認は実行Reproductionではない}}

未実施Checks: {{不足Application・DB・Browser・API・Device・QA・Release確認、有限の残確認}}

保全: {{Inputs・Dirty・履歴・IDsを保全、root-atomicityとID・提案・Ledger参照を確認}}
