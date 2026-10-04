<!-- blend-template: scope-and-approach@1.0.0 -->
# SYN-JA-001 — 日本語の合成テスト設計

## 目的・根拠

| Field | Value |
| --- | --- |
| Revision | ja-syn-r1 |
| Source | SPEC:S1 合成仕様のみ・実運用の根拠ではない |
| Research根拠 | 合成入力の構造検証のみ |
| Code baseline | 合成データのみ・アプリケーションを参照しない |
| Mode | design |
| 調査限界 | 実行・業務承認・画面表示は未検証 |

## 対象範囲

| Field | Value |
| --- | --- |
| 対象 | 二条件の組合せと境界・対象外データの維持 |
| 対象外 | アプリケーションとデータベースの実行 |
| 役割 | 所有者権限を持つ教員 |

## 準備・実行方針

| Field | Value |
| --- | --- |
| 環境 | 合成の学校A・年度Yと学校B・年度Z |
| 準備 | TD-JA-01を確認し、各バリエーション前に復元する |
| 実行選択 | 同一ケースの各バリエーションを独立して選択する |
| 開始条件 | 初期値と権限の確認 |
| 終了条件 | 必須の全バリエーションを証拠付きで評価する |
| 証拠 | 要求・応答・再読込の記録。実際の結果は未入力 |

## Coverage・Gaps

### Coverage

| Clause / anchor | Obligation / branch | Case / variant / gap | Rationale / proof limit |
| --- | --- | --- | --- |
| SPEC:S1 | 二条件・等号境界・対象外の維持 | TC-JA-01:a, TC-JA-01:b, TC-JA-01:c | 合成の期待結果に限定する |

### Gaps

| Gap ID | Kind | Known obligation / source | Missing decision / proof | Impact / next check |
| --- | --- | --- | --- | --- |

Gapsなし。
