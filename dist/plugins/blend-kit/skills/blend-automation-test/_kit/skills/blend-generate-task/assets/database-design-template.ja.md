<!-- blend-template: database-design@1.0.0 -->
# {{機能}} — データベース設計

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,scope,storage,columns,identity,relationships,constraints,read_write,lifecycle,verification. Generate ONLY for necessary DB design change. Four required H2s and labels/tables. Repeat storage H3 and column table per affected unit; if no column affected give reason. Optional indexes/performance, transaction/concurrency, copy/import/migration H3 only when affected; unknown affected facts stay gaps, not omitted. Prose only, no executable DDL/migration. Remove instructions/placeholders. -->

## 目的・範囲

- 参照元: {{Verified ID/parent、spec/context/confirmation link/revision、authority}}
- 対象範囲: {{Storage/relationship/lifecycle変更が必要な理由、actors/operations、変更しない範囲}}
- 設計状態: {{Confirmed constraints / engineering proposal / 未決事項；実装承認としない}}

## As-Is・To-Be

| 保存対象 | As-Is・証拠 | To-Be・根拠 | 一レコードの単位 | Consumer・owner |
| --- | --- | --- | --- | --- |
| {{確認したstorage/明示proposal}} | {{Source/schema anchor+revision；target DB未観測}} | {{必要変更とrepresentation proposal}} | {{明確なgranularity}} | {{確認flow/scope}} |

## データ設計

### {{変更対象storage unit}}

| カラム | 型 | NULL | デフォルト | 内容・根拠 |
| --- | --- | --- | --- | --- |
| {{確認/提案名}} | {{Typeまたはgap}} | {{可否と意味}} | {{Exact defaultまたはgap}} | {{Role/authority；NULL=0と推定しない}} |

- 識別: {{Primary/unique identity、counting unit、scope keys、関連ordinary/variant}}
- 関係: {{参照先、cardinality、owner/scope validity、orphan/absence；application/DB制約を区別}}
- 制約: {{Validation/integrity/authorization、NULL/zero/deleted状態、保持事項}}
- 読み書き: {{Entry/validation → 必要atomicity → save/readback → consumers；選択案の理由}}
- ライフサイクル: {{実際に影響するcreate/edit/delete/inactivate/recompute/copy；preservation/errors}}

<!-- OPTIONAL H3 indexes/performance for affected query/index obligations; transaction/concurrency for affected atomicity/stale-writer obligations; copy/import/migration for affected transfer/existing-data obligations. Include rationale/scope/gaps; no sample-feature locks/tables/enums. -->

## 互換性・検証

- 互換性: {{Existing data/API/readers、preservation、根拠あるunsupported paths；必要migrationもdesignのみ}}
- 検証: {{Constraint/save/readback/lifecycle/consumer/boundary/error checksと必要proof；SQL未実行}}
- 限界: {{不足schema/data/environment/business evidenceと最小次check；runtime/releaseを主張しない}}
