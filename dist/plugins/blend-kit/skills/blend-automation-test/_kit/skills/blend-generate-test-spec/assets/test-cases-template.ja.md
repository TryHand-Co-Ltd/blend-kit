<!-- blend-template: test-cases@1.3.0 -->
# [Feature] — [test cases]

<!-- AUTHORING: Replace brackets and remove this instruction. Required headings/fields/order stay. Use <br> within a table cell and &#124; for literal pipe. Confirmed/Proposed/Awaiting decision are authority; Ready/Draft/Blocked are readiness; new execution is NOT RUN. Unsupported oracle remains gap. -->

<!-- AUTHORING: Write for a reader who has not seen the conversation. Title identifies one behavior; configuration/inputs contain decisive values; actions describe what to do; overall Expected states the final outcome. Each variant Expected contains only that branch's final result, not all other branches or a copy of the overall paragraph. Keep meaningful timing/negative controls. Common conventions belong once in Context. Customer report is the self-contained 2.4 projection; metadata is not its main reading flow. -->

## 規約・コンテキスト

| Field | Value |
| --- | --- |
| Revision | [same design revision] |
| Feature | [verified identity and purpose] |
| Feature ID | [verified source ID, not title or slug] |
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

#### TC-01 — [one clear scenario objective]

| Field | Value |
| --- | --- |
| 機能 | [verified value] |
| screen_relative_path | [verified relative URL or exact unknown/not-applicable; non-UI basis belongs in observation/gap] |
| 根拠 | [verified value] |
| Priority | [verified value] |
| Execution lane | [Browser/Integration/DB/Security/Performance] |
| 期待根拠 | [verified value] |
| Readiness | [verified value] |
| Gap | [verified value] |
| 設定 | [verified value] |
| 起動 | [verified value] |
| 観測 | [verified value] |
| Actor・権限 | [verified value] |
| Fixture | [verified value] |
| 操作 | @Steps |
| Expected | [concrete overall outcome, including relevant timing and preserved state] |
| 維持状態 | [verified value] |
| 証拠 | [verified value] |
| Reset | [verified value] |

<!-- AUTHORING: All Field identities/order/enums and gap/fixture semantics remain unchanged. Thao tác/操作=@Steps; Expected is the concrete overall TC outcome. Write concise conditions and decisive data; reference shared setup instead of copying actor/create/verify/reset prose. One TC has one objective and one Reset field; do not duplicate reset in Steps. Explicit variants retain independent data/actions/final outcomes. Keep identity/readiness/oracle/fixture/checkpoint metadata internal. Customer core retains all material conditions/actions/Expected/Actual/Status; include technical facts only when needed to execute, understand or verify, beside related content. No default technical appendix or reader-facing preparation label. -->

<!-- AUTHORING: ReadyのGapはliteral none。Draft/BlockedのGapは既存のgap ID一つ以上をコンマと一つの空白で区切る（例: G-X または G-X, G-Y）。独立したblockerをすべて保持し、参照を捨てるために集約gapを作らない。ID重複、セミコロン、noneとの混在、説明文は不可。説明は対応するgap/fixture/proofに置く。例のIDをsource IDとして発明しない。 -->

##### Steps

| Step | Action |
| --- | --- |
| 1 | [establish only the decisive prerequisite] |
| 2 | [exercise operation and observe the result using variant inputs/action delta] |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| a | [branch-selecting values] | [none or Step 2: concrete change to existing step] | [concrete final outcome for a only] |
| b | [boundary values] | [none or Step 2: concrete change to existing step] | [concrete final outcome for b only] |

##### Checkpoints

| Variant | Checkpoint | Step | Stage | Expected | Focus | Artifact |
| --- | --- | --- | --- | --- | --- | --- |
| a | CP-result | 2 | result | [concrete source-backed result for a only] | [exact result values and distinguishing controls] | screenshot |
| b | CP-result | 2 | result | [concrete source-backed result for b only] | [exact result values and distinguishing controls] | screenshot |

<!-- AUTHORING: Steps are exactly Step/Action with consecutive positive integers. Variants are exactly Variant/Inputs/Action delta/Expected, explicit base for a single run. Keep stable Variant IDs; start Inputs with a human description followed by decisive data so the report can show description (ID), e.g. Nhỏ hơn (lt) / 未満 (lt). Never change IDs for presentation. Delta is exactly none or names an existing step with Step N/step N, Bước N/bước N, or ステップ N. Example: Step 2: cancel deletion. Bare 2:/3: labels are invalid. Final Expected is concrete for that variant; no @Checkpoints, unresolved placeholder, other-branch reference or copied multi-branch outcome. Checkpoints retain seven columns/enums and concrete assertions for meaningful capture/inspection/export milestones only. Add before/setup/after/export proof only when needed to discriminate temporal/preservation behavior; no automatic two-image or every-click quota. Each variant needs its meaningful proof milestone(s). Screenshots default to matching raw/annotated viewport captures (full_page=false); full page only when needed for whole-layout proof. Use a short English observed note at top-right in clear space, minimal non-overlapping highlights and actual pixel review; export requires the application file. No Actual/status/image path/review attestation in source. On refresh map old IDs/obligations before removing cases; no inherited PASS/images. -->
