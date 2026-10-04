<!-- blend-template: scope-and-approach@1.0.0 -->
# [Feature] — [test scope]

<!-- AUTHORING: Replace brackets and remove this instruction. Required headings/fields/order stay. Use <br> within a table cell and &#124; for literal pipe. Confirmed/Proposed/Awaiting decision are authority; Ready/Draft/Blocked are readiness; new execution is NOT RUN. Unsupported oracle remains gap. -->

## 目的・根拠

| Field | Value |
| --- | --- |
| Revision | [verified value] |
| Source | [verified value] |
| Research根拠 | [verified value] |
| Code baseline | [verified value] |
| Mode | [verified value] |
| 調査限界 | [verified value] |

## 対象範囲

| Field | Value |
| --- | --- |
| 対象 | [verified value] |
| 対象外 | [verified value] |
| 役割 | [verified value] |

## 準備・実行方針

| Field | Value |
| --- | --- |
| 環境 | [verified value] |
| 準備 | [verified value] |
| 実行選択 | [verified value] |
| 開始条件 | [verified value] |
| 終了条件 | [verified value] |
| 証拠 | [verified value] |

## Coverage・Gaps

### Coverage

| Clause / anchor | Obligation / branch | Case / variant / gap | Rationale / proof limit |
| --- | --- | --- | --- |
| [source clause] | [actor, branch, outcome and preservation] | [TC-ID:variant or G-ID] | [discriminating check/equivalence] |

<!-- AUTHORING: Case / variant / gap列は既存のTC-ID、TC-ID:variant、G-IDのみ。複数参照はコンマと一つの空白で区切る（例: TC-X:a, TC-X:b, G-X）。ID重複、セミコロン、ステップ注釈、説明文は不可。説明はRationale / proof limit列に書く。例のIDを新しい業務IDとして採用しない。 -->

### Gaps

| Gap ID | Kind | Known obligation / source | Missing decision / proof | Impact / next check |
| --- | --- | --- | --- | --- |
| [G-ID] | [business/fact/engineering/preparation/proof] | [known obligation] | [unknown oracle/seam/fixture] | [affected TC; smallest check] |

<!-- AUTHORING: 各gap行のKindはbusiness、fact、engineering、preparation、proofのいずれか一つのみ（例: fact。fact, proofは不可）。二次的な限界はMissing decision / proof列へ。独立原因は安定したIDの別gapとして残し、blockerを隠すために集約しない。 -->

<!-- AUTHORING: No gaps permits no rows and a clear none statement. Coverage always retains every active clause/branch. Research basis records standalone or frozen-handoff reuse, decisive checks and any delta. Exclusions need authority. Source and dirty code revision are independent. -->
