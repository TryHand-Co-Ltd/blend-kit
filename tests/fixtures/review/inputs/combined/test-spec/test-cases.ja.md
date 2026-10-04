<!-- blend-template: test-cases@1.0.0 -->
# FX-REVIEW — Test cases

## 規約・コンテキスト

| Field | Value |
| --- | --- |
| Revision | design-v2 |
| Feature | FX-REVIEW score alert settings |
| Conventions | scope-and-approach and test-data; stable variants independently reported; new design NOT RUN |

### Context: CTX-1

| Field | Value |
| --- | --- |
| 設定 | Alert Settings S-A/Y-2/C-A; threshold=80 |
| 起動 | Recalculate -> server AlertSettings.recalculate |
| 観測 | Score Results and saved target/non-target rows |
| Actor・権限 | school-admin admin alias |
| Fixture | TD-01 |

## テストケース

### Flow: Configure and recalculate

#### TC-01 — threshold boundary

| Field | Value |
| --- | --- |
| 機能 | Alert configuration/recalculation |
| 根拠 | SPEC.md C1,C2; confirmation.md |
| Priority | High |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-1 |
| 起動 | @CTX-1 |
| 観測 | @CTX-1 |
| Actor・権限 | @CTX-1 |
| Fixture | @CTX-1 |
| 操作 | Recalculate each threshold parameter from restored state |
| Expected | alert true for below; false for equal/above |
| 維持状態 | Existing score entry and non-target saved values remain unchanged |
| 証拠 | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| below | score=79 | alert=true |

#### TC-02 — percentage fraction

| Field | Value |
| --- | --- |
| 機能 | Alert configuration/recalculation |
| 根拠 | SPEC.md C3; confirmation.md |
| Priority | High |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-1 |
| 起動 | @CTX-1 |
| 観測 | @CTX-1 |
| Actor・権限 | @CTX-1 |
| Fixture | @CTX-1 |
| 操作 | Set percent method; produce 79.9; execute |
| Expected | 80 |
| 維持状態 | Existing score entry and non-target saved values remain unchanged |
| 証拠 | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| fraction | positive percentage result=79.9 | 80 |

#### TC-03 — server role permission

| Field | Value |
| --- | --- |
| 機能 | Alert configuration/recalculation |
| 根拠 | SPEC.md C5; confirmation.md |
| Priority | High |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-1 |
| 起動 | @CTX-1 |
| 観測 | @CTX-1 |
| Actor・権限 | @CTX-1 |
| Fixture | @CTX-1 |
| 操作 | Call recalculation server seam with each actor alias |
| Expected | Admin updates; teacher forbidden and no writes |
| 維持状態 | Existing score entry and non-target saved values remain unchanged |
| 証拠 | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| admin | school-admin | update target |

#### TC-04 — target isolation

| Field | Value |
| --- | --- |
| 機能 | Alert configuration/recalculation |
| 根拠 | SPEC.md C4; confirmation.md |
| Priority | High |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-1 |
| 起動 | @CTX-1 |
| 観測 | @CTX-1 |
| Actor・権限 | @CTX-1 |
| Fixture | @CTX-1 |
| 操作 | Execute selected S-A/Y-2/C-A; inspect target only |
| Expected | Target changes; non-target sentinels may also change |
| 維持状態 | Existing score entry and non-target saved values remain unchanged |
| 証拠 | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

#### TC-05 — disabled preservation

| Field | Value |
| --- | --- |
| 機能 | Alert configuration/recalculation |
| 根拠 | SPEC.md C6; confirmation.md |
| Priority | Medium |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-1 |
| 起動 | @CTX-1 |
| 観測 | @CTX-1 |
| Actor・権限 | @CTX-1 |
| Fixture | @CTX-1 |
| 操作 | Set enabled=false; execute |
| Expected | Recomputed target alert |
| 維持状態 | Existing score entry and non-target saved values remain unchanged |
| 証拠 | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

#### TC-06 — missing source preservation

| Field | Value |
| --- | --- |
| 機能 | Alert configuration/recalculation |
| 根拠 | SPEC.md C8; confirmation.md |
| Priority | High |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-1 |
| 起動 | @CTX-1 |
| 観測 | @CTX-1 |
| Actor・権限 | @CTX-1 |
| Fixture | @CTX-1 |
| 操作 | Arrange missing source score; execute |
| Expected | source-score-missing; all saved rows unchanged |
| 維持状態 | Existing score entry and non-target saved values remain unchanged |
| 証拠 | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

#### TC-07 — subtraction rounding

| Field | Value |
| --- | --- |
| 機能 | Alert configuration/recalculation |
| 根拠 | SPEC.md C7; confirmation.md |
| Priority | Low |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-1 |
| 起動 | @CTX-1 |
| 観測 | @CTX-1 |
| Actor・権限 | @CTX-1 |
| Fixture | @CTX-1 |
| 操作 | Subtract offset producing 79.9; execute |
| Expected | 79 by truncation |
| 維持状態 | Existing score entry and non-target saved values remain unchanged |
| 証拠 | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |
