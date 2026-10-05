<!-- blend-template: implementation-plan@1.0.0 -->
# {{対象名}} — 実装計画

<!-- TEMPLATE INSTRUCTIONS: implementation-plan@1.0.0. Retain all six H2s and localized labels. Explicit none with scoped reason, never empty sections. Repeat supported outcome step blocks; step IDs are local planning references, never source Task IDs. Optional H3 predicates are in references/planning.md: prior findings, meaningful independent parallel work, affected DB/migration only. Remove comments/placeholders in completed output. -->

## 承認済み入力・根拠

- 目的: {{問題と実装する承認済み結果}}
- 状態: Draft — {{計画レビュー用。承認・業務判断が不足する対象は Blocked}}
- 識別情報: {{検証済み Feature ID・情報源・リンク。タスク対象なら正確な Task ID と直接の親。連番から推定しない}}
- 情報源リビジョン: {{実際の承認済み artifact paths + per-file revision/SHA-256 + clauses/AC。現行 CONTEXT・許可された確認の identities/authority は区別}}
- レビュー判定: {{Report path/revision/disposition、読んだ範囲、未解決 findings。未実施なら限界を明記}}
- 承認根拠: {{Explicit source/role/date、正確な approved paths/revisions/hashes と selected scope。実際の bytes との一致または gap}}
- 承認範囲: {{選択した outcomes/AC、承認された範囲と未承認範囲}}
- コード基準: {{Application Git SHA + relevant working-content identities/status。blend:repo-relative evidence と static limits}}
- Research依存: {{Selected actual topic paths/hashes、使用する結論、decisive source/code/confirmation identities。不要なら理由}}

<!-- OPTIONAL H3 “既存指摘の扱い” only with relevant prior review findings: stable ID, disposition, exact evidence, blocking scope/dependents and approval impact. -->

## 対象範囲・維持する動作

- 対象: {{Actors/actions/outcomes と expected affected code/consumer surfaces}}
- 対象外: {{除外した動作、未承認・依存する範囲と情報源の根拠}}
- 維持する動作: {{維持する既存の permissions/state/defaults/exceptions/data/lifecycle/shared consumers}}

## 実装手順

### P1 — {{独立した結果}}

- 手順ID: P1
- 結果: {{Observable outcome と proof seam}}
- ファイル・シンボル: {{正確な blend:repo-relative existing paths/symbol roles。新規提案の files は明記}}
- 開始条件: {{開始に必要な正確な input artifact/interface/decision。なければ明記}}
- 契約: {{Cross-step dependency がある場合は canonical consumes/produces name/signature/types。なければ明記}}
- 担当範囲: {{責任を持つ role と owned paths。個人名を創作しない}}
- 依存: {{Producer step + artifact/decision、start/integration gate。なければ明記}}
- 拘束条件: {{Verbatim approved constraints、正確な defaults/values/forbidden behavior と source/AC IDs}}
- 変更内容: {{一貫した実装 actions、既存 code の再利用。Engineering proposal は明記}}

## 依存・並列化

{{正確な step/artifact dependencies、order/start/integration gates と ownership conflicts。依存・並列作業がなければ理由を明記。}}

<!-- OPTIONAL H3 “並列化計画” only with meaningful independent steps: wave | steps | disjoint owned paths | exact prerequisite | parallel peers. Unknown independence remains serial. -->

## 受入条件・検証

- AC対応: {{すべての active selected AC/obligation → step → 識別可能な required observation/proof、または正確な Blocked gap}}
- 検証コマンド: {{検証済み toolchain の完全な commands/flags、application root に対する相対 cwd。新規提案 checks と作成前提を明記。未解決 command は Blocked}}
- 検証状態: Planned / Not run — {{Planning 中は実行しない。Static/test/DB/browser/release evidence は区別}}

| AC・義務 | 手順 | 観察・維持する動作 | Proof種別・コマンド・準備 | 期待する信号 | 状態・gap |
| --- | --- | --- | --- | --- | --- |
| {{Exact AC ID}} | P1 | {{Discriminating outcome/preserved state}} | {{Toolchain-backed command、相対 cwd、environment/fixture}} | {{Success/failure signal}} | Planned / Not run |

## リスク・最終確認

- リスク: {{Business blockers、engineering proposals/facts、compatibility/proof/permission risks と影響する steps。なければ確認範囲を明記}}
- 最終確認: {{Final selected AC/preservation/interface validation、planned commands、deliverables/handoff と残る evidence/authorization。完了・runtime を主張しない}}
- 実行権限: 本計画からは付与されない — {{Execution、test/SQL、publication/release は別途 authorization が必要。実際の制限を記載}}

<!-- OPTIONAL H3 “DB・移行” only when affected: storage/schema/current rows, compatibility/release order, rerun/partial failure/backfill/locks/replicas/preservation, rollback limits and missing proof. No SQL/migration output or execution. -->
