<!-- blend-template: split-tasks@1.0.0 -->
# {{機能}} — 変更内容・作業分割

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,scope,title,main_screen,affected_screens,business,technical,completion. Keep two H2 headings and task labels. Repeat H3 per usable outcome; local numbers are not source IDs. Optional summary table only if comparison helps; dependencies/open decisions H4 only if applicable. Explicit no-screen seam/no-other-screen result. Remove instructions/placeholders. -->

## 対象範囲

- 参照元: {{確認した原文ID/直属parent、共有source URL、revision、authority}}
- 対象範囲: {{問題、actors/permissions、operations、目的、未承認範囲、保持する挙動}}

## タスク一覧

<!-- OPTIONAL summary when comparison helps: Task | メイン画面 | 変更内容 | 実際に必要な入力. Titles/screens match detail. -->

### 1. {{独立して提供可能な成果}}

**メイン画面:** {{[原文の画面名] - `verified route`；直接画面がなければ具体的API/job/shared seam}}

**影響画面:**

- {{確認した他画面/path；mainを重複しない；なければ確認範囲内でなしと明記}}

**変更範囲:** {{Direct owner、role/permission、necessary dependency、regression-only、unresolved impact}}

#### 業務変更

- {{Actor/action/conditions → outcome、failure/exception、保持状態；未承認proposalを区別}}

#### 技術対応

- {{Verified repo-relative anchor/symbol・役割 → 変更案 → input/output/save/readback/consumer → constraints；同等実装を認める}}

<!-- OPTIONAL H4 “依存・未決事項” only for real prerequisites/open decisions: producer + needed result, can-start-now/start/integration gates, exact unanswered decision. -->

#### 完了条件

{{観察可能な成果を一文で示す；実装/test済みとしない；AC IDを補助に使用可}}
