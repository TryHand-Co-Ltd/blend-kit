<!-- blend-template: test-cases@1.0.0 -->
# SYN-001 — Cases

## 規約・コンテキスト

| Field | Value |
| --- | --- |
| Revision | syn-r2 |
| Feature | SYN-001 synthetic eligibility |
| Conventions | Synthetic source only; scope-and-approach and test-data; independent cases |

### Context: CTX-1

| Field | Value |
| --- | --- |
| 設定 | Settings at synthetic editor |
| 起動 | POST /eligibility/preview verified fixture route |
| 観測 | Readback preview and non-target record |
| Actor・権限 | Teacher owner; school A/year Y |
| Fixture | TD-01 |

## テストケース

### Flow: Eligibility and scope

#### TC-SYN-01 — Both predicates and boundary

| Field | Value |
| --- | --- |
| 機能 | Eligibility preview |
| 根拠 | SPEC:S1 |
| Priority | High |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-1 |
| 起動 | @CTX-1 |
| 観測 | @CTX-1 |
| Actor・権限 | @CTX-1 |
| Fixture | @CTX-1 |
| 操作 | @Steps |
| Expected | @Steps |
| 維持状態 | Non-target B unchanged |
| 証拠 | Request/response/readback each variant |
| Reset | Restore TD-01 initial state |

##### Steps

| Step | Action | Expected | Preservation |
| --- | --- | --- | --- |
| 1 | Verify TD-01 initial settings | 100 maximum and enabled | Non-target unchanged |
| 2 | Preview each variant independently | Compare variant expected | Stored score unchanged |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| a | enabled=yes, score=59, max=100 | Eligible |
| b | enabled=no, score=59, max=100 | Not eligible |
| c | enabled=yes, score=60, max=100 | Not eligible |

#### TC-SYN-02 — Denied visitor does not mutate

| Field | Value |
| --- | --- |
| 機能 | Eligibility permission |
| 根拠 | SPEC:S2 |
| Priority | High |
| 期待根拠 | Confirmed |
| Readiness | Ready |
| Gap | none |
| 設定 | @CTX-1 |
| 起動 | @CTX-1 |
| 観測 | @CTX-1 |
| Actor・権限 | Visitor without owner permission |
| Fixture | TD-01 |
| 操作 | Send preview request as visitor; readback as owner |
| Expected | Request denied; before and after target identical |
| 維持状態 | All score/settings unchanged |
| 証拠 | Request refusal and authorized readback |
| Reset | Restore TD-01; logout visitor |

#### TC-SYN-03 — Imported scope preserves other school

| Field | Value |
| --- | --- |
| 機能 | Import scope |
| 根拠 | SPEC:S4 |
| Priority | Medium |
| 期待根拠 | Confirmed |
| Readiness | Blocked |
| Gap | G-02 |
| 設定 | Verified import settings |
| 起動 | Import seam unavailable — G-02 |
| 観測 | Owner target and non-target readback |
| Actor・権限 | Teacher owner |
| Fixture | local: import preparation unavailable — G-02 |
| 操作 | Import fixture after G-02 resolved |
| Expected | Only selected school/year updated |
| 維持状態 | School B/year Z unchanged |
| 証拠 | Import receipt plus readback |
| Reset | Restore isolated snapshots once seam is verified |
