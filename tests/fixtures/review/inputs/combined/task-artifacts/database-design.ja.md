<!-- blend-template: database-design@1.0.0 -->
# FX-REVIEW alert settings — データベース設計



## 目的・範囲

- 参照元: FX-REVIEW SPEC.md/confirmation.md revision2
- 対象範囲: Add alert_config table; existing school/year/course result lifecycle supposedly unchanged
- 設計状態: Confirmed mandatory representation

## As-Is・To-Be

| 保存対象 | As-Is・証拠 | To-Be・根拠 | 一レコードの単位 | Consumer・owner |
| --- | --- | --- | --- | --- |
| alert_config proposed new storage | Existing synthetic scope keys school/year/course; no observed DB schema | One setting shared across school/course years, per Research | One school/course | AlertSettings.recalculate and Score Results |

## データ設計

### alert_config

| カラム | 型 | NULL | デフォルト | 内容・根拠 |
| --- | --- | --- | --- | --- |
| school_id | integer | No | none | School scope; year intentionally omitted |

- 識別: Unique school_id,course_id; academic year not stored
- 関係: Course belongs to school; one row reused across years
- 制約: Server admin check; threshold and enabled saved
- 読み書き: School/course read/save; current year uses shared row
- ライフサイクル: Copy all year values using same row; no isolated-year storage



## 互換性・検証

- 互換性: Existing results claimed preserved across years
- 検証: Verify admin save/readback and target school; no SQL executed
- 限界: No real DB schema observed; design still a proposal in source despite Confirmed heading
