<!-- blend-template: test-cases@1.3.0 -->
# SYN-SC — Kiểm thử theo scenario

## Quy ước và context

| Field | Value |
| --- | --- |
| Revision | compact-r1 |
| Feature | SYN-SC synthetic rule lifecycle |
| Feature ID | SYN-SC |
| Conventions | Fixture tổng hợp; chưa chạy ứng dụng. Mỗi variant chuẩn bị/reset độc lập; tiếng Anh có nghĩa khi test và ghi note. |

### Context: CTX-SC

| Field | Value |
| --- | --- |
| Cấu hình | Synthetic rule editor and judgment controls; concrete entry pending G-PREP |
| Kích hoạt | Explicit save/judgment actions; no background recalculation |
| Quan sát | Persisted rule and score judgment readback |
| Actor và quyền | Synthetic teacher owner; isolated school A/year Y |
| Fixture | TD-SC |

## Các testcase

### Flow: Quy tắc, biên và vòng đời

#### TC-SC-01 — Xét biên ngưỡng cố định

| Field | Value |
| --- | --- |
| Chức năng | Xét biên ngưỡng cố định |
| screen_relative_path | unknown |
| Căn cứ | SYN:O1, SYN:O2 |
| Priority | High |
| Execution lane | Browser |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| Cấu hình | @CTX-SC |
| Kích hoạt | @CTX-SC |
| Quan sát | @CTX-SC |
| Actor và quyền | @CTX-SC |
| Fixture | @CTX-SC |
| Thao tác | @Steps |
| Expected | The comparator selects the correct red scores at the 30 boundary; numeric scores and non-target 82 stay unchanged. |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Required checkpoint observations and reviewed artifacts. |
| Reset | Restore TD-SC initial rule/scores independently and verify its defined baseline. |

##### Steps

| Step | Action |
| --- | --- |
| 1 | Restore TD-SC initial scores and configure this variant comparator |
| 2 | Run judgment and inspect all three score results |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| lt | T=30; S=29,30,31; comparator < | Step 1: select comparator < | 29 is red; 30 and 31 are not red; red count 1 |
| le | T=30; S=29,30,31; comparator ≤ | Step 1: select comparator ≤ | 29 and 30 are red; 31 is not red; red count 2 |

##### Checkpoints

| Variant | Checkpoint | Step | Stage | Expected | Focus | Artifact |
| --- | --- | --- | --- | --- | --- | --- |
| lt | CP-setup | 1 | setup | Threshold 30; comparator <; scores 29, 30, 31 | Threshold/comparator controls and three score cells | screenshot |
| lt | CP-result | 2 | result | 29 is red; 30 and 31 are not red; red count 1 | All three judgment cells and total red count 1 | screenshot |
| le | CP-setup | 1 | setup | Threshold 30; comparator ≤; scores 29, 30, 31 | Threshold/comparator controls and three score cells | screenshot |
| le | CP-result | 2 | result | 29 and 30 are red; 31 is not red; red count 2 | All three judgment cells and total red count 2 | screenshot |

#### TC-SC-02 — Hủy hoặc xác nhận xóa quy tắc cuối

| Field | Value |
| --- | --- |
| Chức năng | Hủy hoặc xác nhận xóa quy tắc cuối |
| screen_relative_path | unknown |
| Căn cứ | SYN:O3, SYN:O4 |
| Priority | High |
| Execution lane | Browser |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| Cấu hình | @CTX-SC |
| Kích hoạt | @CTX-SC |
| Quan sát | @CTX-SC |
| Actor và quyền | @CTX-SC |
| Fixture | @CTX-SC |
| Thao tác | @Steps |
| Expected | Cancel preserves R1 and red score 29; confirm removes R1 while preserving the stored red result until recalculation, then clears only the red result. |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Required checkpoint observations and reviewed artifacts. |
| Reset | Restore TD-SC initial rule/scores independently and verify its defined baseline. |

##### Steps

| Step | Action |
| --- | --- |
| 1 | Restore TD-SC with only complete R1 and stored red score 29 |
| 2 | Open deletion dialog and choose variant decision |
| 3 | Read rules and stored result before recalculation |
| 4 | Run recalculation and inspect score and red result |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| cancel | Only complete R1; score 29; decision cancel | Step 2: cancel deletion | After recalculation R1 remains; score 29 remains red; numeric score 29 unchanged |
| confirm | Only complete R1; score 29; decision confirm | Step 2: confirm deletion | R1 removed; old red result remains before recalculation; afterwards score 29 is not red and numeric score 29 remains |

##### Checkpoints

| Variant | Checkpoint | Step | Stage | Expected | Focus | Artifact |
| --- | --- | --- | --- | --- | --- | --- |
| cancel | CP-before | 1 | before | Only R1 exists; stored score 29 is red | Rule R1 and score 29/red state | screenshot |
| cancel | CP-result | 3 | result | R1 remains; stored score 29 remains red | Rule list R1 and unchanged stored result | screenshot |
| cancel | CP-after | 4 | after | After recalculation R1 remains; score 29 remains red | Rule R1 and recalculated score 29/red state | screenshot |
| confirm | CP-before | 1 | before | Only R1 exists; stored score 29 is red | Rule R1 and score 29/red state | screenshot |
| confirm | CP-result | 3 | result | R1 is removed; stored score 29 remains red before recalculation | Empty rule list and stored score 29/red state | screenshot |
| confirm | CP-after | 4 | after | After recalculation score 29 is not red; numeric score 29 remains | Recalculated judgment and unchanged numeric score 29 | screenshot |

#### TC-SC-03 — Lưu quy tắc nhập dở và loại khỏi xét

| Field | Value |
| --- | --- |
| Chức năng | Lưu quy tắc nhập dở và loại khỏi xét |
| screen_relative_path | unknown |
| Căn cứ | SYN:O5 |
| Priority | High |
| Execution lane | Browser |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| Cấu hình | @CTX-SC |
| Kích hoạt | @CTX-SC |
| Quan sát | @CTX-SC |
| Actor và quyền | @CTX-SC |
| Fixture | @CTX-SC |
| Thao tác | @Steps |
| Expected | Incomplete R1 remains saved, with an empty threshold, and is excluded from judgment; numeric score 29 remains. |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Required checkpoint observations and reviewed artifacts. |
| Reset | Restore TD-SC initial rule/scores independently and verify its defined baseline. |

##### Steps

| Step | Action |
| --- | --- |
| 1 | Restore TD-SC with no rule and no red result |
| 2 | Create R1 without threshold and save; reopen R1 |
| 3 | Run judgment using incomplete R1 |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| base | R1 threshold empty; score 29 | none | Incomplete R1 remains saved, with an empty threshold, and is excluded from judgment; numeric score 29 remains. |

##### Checkpoints

| Variant | Checkpoint | Step | Stage | Expected | Focus | Artifact |
| --- | --- | --- | --- | --- | --- | --- |
| base | CP-saved | 2 | result | R1 is retained with empty threshold and marked incomplete | Reopened R1 threshold and incomplete state | screenshot |
| base | CP-judgment | 3 | after | Incomplete R1 is excluded; score 29 is not red | Judgment state and numeric score 29 | screenshot |

#### TC-SC-04 — Form cũ không tạo lại quy tắc đã xóa

| Field | Value |
| --- | --- |
| Chức năng | Form cũ không tạo lại quy tắc đã xóa |
| screen_relative_path | unknown |
| Căn cứ | SYN:O6 |
| Priority | High |
| Execution lane | Integration |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| Cấu hình | @CTX-SC |
| Kích hoạt | @CTX-SC |
| Quan sát | @CTX-SC |
| Actor và quyền | @CTX-SC |
| Fixture | @CTX-SC |
| Thao tác | @Steps |
| Expected | Stale save is rejected and cannot recreate deleted R1; numeric score 29 and non-target 82 remain unchanged. |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Required checkpoint observations and reviewed artifacts. |
| Reset | Restore TD-SC initial rule/scores independently and verify its defined baseline. |

##### Steps

| Step | Action |
| --- | --- |
| 1 | Restore TD-SC; open R1 in editor A and retain its version |
| 2 | Delete R1 from independent editor B; verify persisted absence |
| 3 | Submit stale editor A and inspect refusal and authoritative readback |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| base | A holds R1 version 1; B deletes it before A save | none | Stale save is rejected and cannot recreate deleted R1; numeric score 29 and non-target 82 remain unchanged. |

##### Checkpoints

| Variant | Checkpoint | Step | Stage | Expected | Focus | Artifact |
| --- | --- | --- | --- | --- | --- | --- |
| base | CP-before | 2 | before | R1 is absent after editor B deletion | Authoritative rule readback absence and editor A stale version | inspection |
| base | CP-result | 3 | result | Stale save rejected; R1 remains absent; numeric score 29 unchanged | Save refusal, persisted rule absence and score readback | inspection |

#### TC-SC-05 — Điều kiện AND với từng nhánh âm

| Field | Value |
| --- | --- |
| Chức năng | Điều kiện AND với từng nhánh âm |
| screen_relative_path | unknown |
| Căn cứ | SYN:O7, SYN:O8 |
| Priority | High |
| Execution lane | Browser |
| Căn cứ kỳ vọng | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| Cấu hình | @CTX-SC |
| Kích hoạt | @CTX-SC |
| Quan sát | @CTX-SC |
| Actor và quyền | @CTX-SC |
| Fixture | @CTX-SC |
| Thao tác | @Steps |
| Expected | Eligibility requires enabled=yes and score<30; disabling only enabled or using score=30 makes the result ineligible. |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Required checkpoint observations and reviewed artifacts. |
| Reset | Restore TD-SC initial rule/scores independently and verify its defined baseline. |

##### Steps

| Step | Action |
| --- | --- |
| 1 | Restore TD-SC and set enabled/score from variant inputs |
| 2 | Run eligibility preview and inspect result |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| positive | enabled=yes; score=29; threshold=30 | Step 1: enabled=yes and score=29 | Eligible: enabled=yes and 29<30 are both true |
| disabled | enabled=no; score=29; threshold=30 | Step 1: enabled=no and score=29 | Not eligible: enabled is false while 29<30 remains true |
| boundary | enabled=yes; score=30; threshold=30 | Step 1: enabled=yes and score=30 | Not eligible: 30<30 is false while enabled remains true |

##### Checkpoints

| Variant | Checkpoint | Step | Stage | Expected | Focus | Artifact |
| --- | --- | --- | --- | --- | --- | --- |
| positive | CP-setup | 1 | setup | Enabled=yes; score 29; threshold 30 | Enabled control, score 29 and threshold 30 | screenshot |
| positive | CP-result | 2 | result | Eligible: enabled=yes and 29<30 are both true | Eligibility result and both predicate values | screenshot |
| disabled | CP-setup | 1 | setup | Enabled=no; score 29; threshold 30 | Enabled control, score 29 and threshold 30 | screenshot |
| disabled | CP-result | 2 | result | Not eligible: enabled is false while 29<30 remains true | Eligibility result, disabled control and score/threshold | screenshot |
| boundary | CP-setup | 1 | setup | Enabled=yes; score 30; threshold 30 | Enabled control, score 30 and threshold 30 | screenshot |
| boundary | CP-result | 2 | result | Not eligible: 30<30 is false while enabled remains true | Eligibility result, enabled control and score/threshold equality | screenshot |
