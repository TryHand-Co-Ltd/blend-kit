<!-- blend-template: test-cases@1.0.0 -->
# SYN-001 — Cases

## Quy ước và context

| Field | Value |
| --- | --- |
| Revision | syn-r2 |
| Feature | SYN-001 synthetic eligibility |
| Conventions | Synthetic source only; scope-and-approach and test-data; independent cases |

### Context: CTX-1

| Field | Value |
| --- | --- |
| Cấu hình | Settings at synthetic editor |
| Kích hoạt | POST /eligibility/preview verified fixture route |
| Quan sát | Readback preview and non-target record |
| Actor và quyền | Teacher owner; school A/year Y |
| Fixture | TD-01 |

## Các testcase

### Flow: Eligibility and scope

#### TC-SYN-01 — Both predicates and boundary

| Field | Value |
| --- | --- |
| Chức năng | Eligibility preview |
| Căn cứ | SPEC:S1 |
| Priority | High |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Ready |
| Gap | none |
| Cấu hình | @CTX-1 |
| Kích hoạt | @CTX-1 |
| Quan sát | @CTX-1 |
| Actor và quyền | @CTX-1 |
| Fixture | @CTX-1 |
| Thao tác | @Steps |
| Expected | @Steps |
| Bảo toàn | Non-target B unchanged |
| Bằng chứng | Request/response/readback each variant |
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
| Chức năng | Eligibility permission |
| Căn cứ | SPEC:S2 |
| Priority | High |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Ready |
| Gap | none |
| Cấu hình | @CTX-1 |
| Kích hoạt | @CTX-1 |
| Quan sát | @CTX-1 |
| Actor và quyền | Visitor without owner permission |
| Fixture | TD-01 |
| Thao tác | Send preview request as visitor; readback as owner |
| Expected | Request denied; before and after target identical |
| Bảo toàn | All score/settings unchanged |
| Bằng chứng | Request refusal and authorized readback |
| Reset | Restore TD-01; logout visitor |

#### TC-SYN-03 — Imported scope preserves other school

| Field | Value |
| --- | --- |
| Chức năng | Import scope |
| Căn cứ | SPEC:S4 |
| Priority | Medium |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Blocked |
| Gap | G-02 |
| Cấu hình | Verified import settings |
| Kích hoạt | Import seam unavailable — G-02 |
| Quan sát | Owner target and non-target readback |
| Actor và quyền | Teacher owner |
| Fixture | local: import preparation unavailable — G-02 |
| Thao tác | Import fixture after G-02 resolved |
| Expected | Only selected school/year updated |
| Bảo toàn | School B/year Z unchanged |
| Bằng chứng | Import receipt plus readback |
| Reset | Restore isolated snapshots once seam is verified |
