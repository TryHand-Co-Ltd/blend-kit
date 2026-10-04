<!-- blend-template: test-cases@1.0.0 -->
# SYN-JA-001 — 日本語のテストケース

## 規約・コンテキスト

| Field | Value |
| --- | --- |
| Revision | ja-syn-r1 |
| Feature | SYN-JA-001 合成の判定プレビュー |
| Conventions | 合成の仕様のみ。各バリエーションは独立し、履歴を引き継がない |

### Context: CTX-JA-1

| Field | Value |
| --- | --- |
| 設定 | 合成エディタで学校A・年度Yを選択する |
| 起動 | 合成プレビューの要求を送信する |
| 観測 | 応答と対象・対象外レコードを再読込する |
| Actor・権限 | 所有者権限を持つ教員 |
| Fixture | TD-JA-01 |

## テストケース

### Flow: 判定と対象外状態の維持

#### TC-JA-01 — 二条件の組合せと等号境界

| Field | Value |
| --- | --- |
| 機能 | 合成の判定プレビュー |
| 根拠 | SPEC:S1 |
| Priority | High |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-JA-1 |
| 起動 | @CTX-JA-1 |
| 観測 | @CTX-JA-1 |
| Actor・権限 | @CTX-JA-1 |
| Fixture | @CTX-JA-1 |
| 操作 | @Steps |
| Expected | @Steps |
| 維持状態 | 学校B・年度Zの設定と保存済み点数を維持する |
| 証拠 | 各バリエーションの要求・応答・再読込 |
| Reset | TD-JA-01の初期状態に復元し、両レコードを確認する |

##### Steps

| Step | Action | Expected | Preservation |
| --- | --- | --- | --- |
| 1 | TD-JA-01の初期状態を確認する | 満点100・有効・保存済み点数59を確認できる | 学校B・年度Zは変更されない |
| 2 | 各バリエーションを独立してプレビューする | バリエーションごとの期待結果と一致する | 保存済み点数と対象外設定を維持する |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| a | enabled=yes, score=59, max=100 | 対象になる。学校B・年度Zの設定と保存済み点数は変更されない |
| b | enabled=no, score=59, max=100 | 対象にならない。対象と対象外の保存済み状態は変更されない |
| c | enabled=yes, score=60, max=100 | 等号境界では対象にならない。対象と対象外の保存済み状態は変更されない |
