<!-- blend-template: test-data@1.0.0 -->
# SYN-JA-001 — 合成の共通データ

## データ規約

| Field | Value |
| --- | --- |
| Revision | ja-syn-r1 |
| Conventions | 合成の別名のみ。アプリケーションとSQLは実行しない |

## Fixtures

### Fixture: TD-JA-01

| Field | Value |
| --- | --- |
| 役割 | 所有者権限を持つ教員 |
| 範囲 | 対象は学校A・年度Y、対象外は学校B・年度Z |
| 状態 | 有効・満点100・点数59・保留中の書込なし |
| 値 | 対象59・対象外82 |
| Target・non-target | A/YとB/Z |
| 作成 | 合成のフィクスチャエディタを使用する |
| 確認 | 両レコードの範囲と初期値を再読込する |
| Reset | 有効設定・満点・点数を復元し、両レコードを確認する |
