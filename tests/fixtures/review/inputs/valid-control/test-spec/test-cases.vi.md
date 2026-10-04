<!-- blend-template: test-cases@1.0.0 -->
# FX-REVIEW — Test cases

## Quy ước và context

| Field | Value |
| --- | --- |
| Revision | design-v2 |
| Feature | FX-REVIEW score alert settings |
| Conventions | scope-and-approach and test-data; stable variants independently reported; new design NOT RUN |

### Context: CTX-1

| Field | Value |
| --- | --- |
| Cấu hình | Alert Settings S-A/Y-2/C-A; threshold=80 |
| Kích hoạt | Recalculate -> server AlertSettings.recalculate |
| Quan sát | Score Results and saved target/non-target rows |
| Actor và quyền | school-admin admin alias |
| Fixture | TD-01 |

## Các testcase

### Flow: Configure and recalculate

#### TC-01 — threshold boundary

| Field | Value |
| --- | --- |
| Chức năng | Alert configuration/recalculation |
| Căn cứ | SPEC.md C1,C2; confirmation.md |
| Priority | High |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Ready |
| Gap | none |
| Cấu hình | @CTX-1 |
| Kích hoạt | @CTX-1 |
| Quan sát | @CTX-1 |
| Actor và quyền | @CTX-1 |
| Fixture | @CTX-1 |
| Thao tác | Recalculate each threshold parameter from restored state |
| Expected | alert true for below; false for equal/above |
| Bảo toàn | Existing score entry and non-target saved values remain unchanged |
| Bằng chứng | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| below | score=79 | alert=true |
| equal | score=80 | alert=false |
| above | score=81 | alert=false |

#### TC-02 — percentage fraction

| Field | Value |
| --- | --- |
| Chức năng | Alert configuration/recalculation |
| Căn cứ | SPEC.md C3; confirmation.md |
| Priority | High |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Ready |
| Gap | none |
| Cấu hình | @CTX-1 |
| Kích hoạt | @CTX-1 |
| Quan sát | @CTX-1 |
| Actor và quyền | @CTX-1 |
| Fixture | @CTX-1 |
| Thao tác | Set percent method; produce 79.9; execute |
| Expected | 79 |
| Bảo toàn | Existing score entry and non-target saved values remain unchanged |
| Bằng chứng | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| fraction | positive percentage result=79.9 | 79 |

#### TC-03 — server role permission

| Field | Value |
| --- | --- |
| Chức năng | Alert configuration/recalculation |
| Căn cứ | SPEC.md C5; confirmation.md |
| Priority | High |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Ready |
| Gap | none |
| Cấu hình | @CTX-1 |
| Kích hoạt | @CTX-1 |
| Quan sát | @CTX-1 |
| Actor và quyền | @CTX-1 |
| Fixture | @CTX-1 |
| Thao tác | Call recalculation server seam with each actor alias |
| Expected | Admin updates; teacher forbidden and no writes |
| Bảo toàn | Existing score entry and non-target saved values remain unchanged |
| Bằng chứng | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

##### Variants

| Variant | Inputs | Expected |
| --- | --- | --- |
| admin | school-admin | update target |
| teacher | teacher direct server request | forbidden; all rows unchanged |

#### TC-04 — target isolation

| Field | Value |
| --- | --- |
| Chức năng | Alert configuration/recalculation |
| Căn cứ | SPEC.md C4; confirmation.md |
| Priority | High |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Ready |
| Gap | none |
| Cấu hình | @CTX-1 |
| Kích hoạt | @CTX-1 |
| Quan sát | @CTX-1 |
| Actor và quyền | @CTX-1 |
| Fixture | @CTX-1 |
| Thao tác | Execute selected S-A/Y-2/C-A; compare target and three sentinels |
| Expected | Target changes; non-target sentinels unchanged |
| Bảo toàn | Existing score entry and non-target saved values remain unchanged |
| Bằng chứng | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

#### TC-05 — disabled preservation

| Field | Value |
| --- | --- |
| Chức năng | Alert configuration/recalculation |
| Căn cứ | SPEC.md C6; confirmation.md |
| Priority | Medium |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Ready |
| Gap | none |
| Cấu hình | @CTX-1 |
| Kích hoạt | @CTX-1 |
| Quan sát | @CTX-1 |
| Actor và quyền | @CTX-1 |
| Fixture | @CTX-1 |
| Thao tác | Set enabled=false; execute |
| Expected | Skipped; existing rows byte-equivalent |
| Bảo toàn | Existing score entry and non-target saved values remain unchanged |
| Bằng chứng | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |

#### TC-06 — missing source preservation

| Field | Value |
| --- | --- |
| Chức năng | Alert configuration/recalculation |
| Căn cứ | SPEC.md C8; confirmation.md |
| Priority | High |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Blocked |
| Gap | G-PREP |
| Cấu hình | @CTX-1 |
| Kích hoạt | @CTX-1 |
| Quan sát | @CTX-1 |
| Actor và quyền | @CTX-1 |
| Fixture | @CTX-1 |
| Thao tác | Arrange missing source score; execute |
| Expected | source-score-missing; all saved rows unchanged |
| Bảo toàn | Existing score entry and non-target saved values remain unchanged |
| Bằng chứng | Capture before/after saved rows plus response and role, not button visibility alone |
| Reset | Restore fixture-preparation.md snapshot and flags before next variant/case |
