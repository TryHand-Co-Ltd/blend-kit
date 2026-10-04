<!-- blend-template: test-cases@1.1.0 -->
# [Feature] — [test cases]

<!-- AUTHORING: Replace brackets and remove this instruction. Required headings/fields/order stay. Use <br> within a table cell and &#124; for literal pipe. Confirmed/Proposed/Awaiting decision are authority; Ready/Draft/Blocked are readiness; new execution is NOT RUN. Unsupported oracle remains gap. -->

## 規約・コンテキスト

| Field | Value |
| --- | --- |
| Revision | [same design revision] |
| Feature | [verified identity and purpose] |
| Conventions | [links to scope/data; priority rationale, evidence/reset conventions] |

<!-- AUTHORING: Optional shared context block only when reused. Same-field @CTX-ID references are allowed; no recursive/mixed reference. Do not repeat identical setup in every case. -->

### Context: CTX-1

| Field | Value |
| --- | --- |
| 設定 | [verified value] |
| 起動 | [verified value] |
| 観測 | [verified value] |
| Actor・権限 | [verified value] |
| Fixture | [verified value] |

## テストケース

### Flow: [business operation]

#### TC-01 — [one independently failing behavior]

| Field | Value |
| --- | --- |
| 機能 | [verified value] |
| screen_relative_path | [verified relative URL, unknown, or not-applicable with a verified non-UI basis] |
| 根拠 | [verified value] |
| Priority | [verified value] |
| 期待根拠 | [verified value] |
| Readiness | [verified value] |
| Gap | [verified value] |
| 設定 | [verified value] |
| 起動 | [verified value] |
| 観測 | [verified value] |
| Actor・権限 | [verified value] |
| Fixture | [verified value] |
| 操作 | [verified value] |
| Expected | [verified value] |
| 維持状態 | [verified value] |
| 証拠 | [verified value] |
| Reset | [verified value] |

<!-- AUTHORING: Priority = High/Medium/Low; expected basis = Confirmed/Proposed/Awaiting decision. Ready requires known oracle plus verified preparation/seams; Draft/Blocked require Gap ID defined in scope (Ready uses none). Fixture = exact TD IDs separated by comma-space, or local: reproducible setup. All field rows required; genuine preservation/proof/reset inapplicability needs reason. Compact case puts action/expected inline. Expanded case replaces both values with @Steps and uses Steps below. Source may use one Markdown list marker and inline code; workbook projection emits exactly one bullet, displays inline code as [identifier], and never exposes Markdown markers. -->

<!-- AUTHORING: ReadyのGapはliteral none。Draft/BlockedのGapは既存のgap ID一つ以上をコンマと一つの空白で区切る（例: G-X または G-X, G-Y）。独立したblockerをすべて保持し、参照を捨てるために集約gapを作らない。ID重複、セミコロン、noneとの混在、説明文は不可。説明は対応するgap/fixture/proofに置く。例のIDをsource IDとして発明しない。 -->

##### Steps

| Step | Action | Expected | Preservation |
| --- | --- | --- | --- |
| 1 | [establish prerequisite] | [observable condition] | [required preserved state or reason] |
| 2 | [exercise operation] | [source-backed observation; parameter placeholders only if variant table] | [required preserved state] |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| a | [branch-selecting values] | [source-backed expected] |
| b | [boundary values] | [source-backed expected] |

<!-- AUTHORING: Steps absent only for inline compact action/expected. Variants absent only for one base run; present table lists all mandatory rows separately, never compound a/b/c. Same schema/context/fields for compact/expanded/parameterized cases. Group main path, boundaries, validation/permission, recovery; priority only selects run order. No actual/evidence-result fields in Markdown. Unknown oracle goes in scope gaps, not fabricated expected. -->
