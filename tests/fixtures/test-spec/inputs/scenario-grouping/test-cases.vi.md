<!-- blend-template: test-cases@1.2.0 -->
# SYN-SC — Kiểm thử theo scenario

## Quy ước và context

| Field | Value |
| --- | --- |
| Revision | scenario-r1 |
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
| Expected | @Checkpoints |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Checkpoint xác định assertion/stage/focus/artifact; nhiều ảnh full-page có highlight/note được kiểm khi chạy. |
| Reset | Khôi phục TD-SC và đọc lại độc lập ở bước cuối; không phụ thuộc case trước. |

##### Steps

| Step | Action | Expected | Preservation |
| --- | --- | --- | --- |
| 1 | Restore TD-SC initial scores and configure this variant comparator | @Checkpoints | Non-target score 82 unchanged |
| 2 | Run judgment and inspect all three score results | @Checkpoints | Scores 29, 30 and 31 unchanged |
| 3 | Restore TD-SC and verify initial values | Initial values 29, 30, 31; non-target 82 | Other rule settings unchanged |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| lt | T=30; S=29,30,31; comparator < | Step 1: select comparator < | @Checkpoints |
| le | T=30; S=29,30,31; comparator ≤ | Step 1: select comparator ≤ | @Checkpoints |

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
| Expected | @Checkpoints |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Checkpoint xác định assertion/stage/focus/artifact; nhiều ảnh full-page có highlight/note được kiểm khi chạy. |
| Reset | Khôi phục TD-SC và đọc lại độc lập ở bước cuối; không phụ thuộc case trước. |

##### Steps

| Step | Action | Expected | Preservation |
| --- | --- | --- | --- |
| 1 | Restore TD-SC with only complete R1 and stored red score 29 | Only R1 exists; score 29 is red | Non-target score 82 unchanged |
| 2 | Open deletion dialog and choose variant decision | @Checkpoints | Score 29 unchanged |
| 3 | Read rules and stored result before recalculation | @Checkpoints | Non-target score 82 unchanged |
| 4 | Run recalculation and inspect score and red result | @Checkpoints | All numeric scores unchanged |
| 5 | Restore TD-SC and verify initial rule/result | R1 exists; score 29 is red | Non-target score 82 unchanged |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| cancel | Only complete R1; score 29; decision cancel | Step 2: cancel deletion | @Checkpoints |
| confirm | Only complete R1; score 29; decision confirm | Step 2: confirm deletion | @Checkpoints |

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
| Expected | @Checkpoints |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Checkpoint xác định assertion/stage/focus/artifact; nhiều ảnh full-page có highlight/note được kiểm khi chạy. |
| Reset | Khôi phục TD-SC và đọc lại độc lập ở bước cuối; không phụ thuộc case trước. |

##### Steps

| Step | Action | Expected | Preservation |
| --- | --- | --- | --- |
| 1 | Restore TD-SC with no rule and no red result | No rule exists; score 29 is not red | Numeric scores unchanged |
| 2 | Create R1 without threshold and save; reopen R1 | @Checkpoints | Non-target score 82 unchanged |
| 3 | Run judgment using incomplete R1 | @Checkpoints | Numeric score 29 unchanged |
| 4 | Restore TD-SC and verify initial state | Only complete R1 exists; score 29 is red | Non-target score 82 unchanged |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| base | R1 threshold empty; score 29 | none | @Checkpoints |

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
| Expected | @Checkpoints |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Checkpoint xác định assertion/stage/focus/artifact; nhiều ảnh full-page có highlight/note được kiểm khi chạy. |
| Reset | Khôi phục TD-SC và đọc lại độc lập ở bước cuối; không phụ thuộc case trước. |

##### Steps

| Step | Action | Expected | Preservation |
| --- | --- | --- | --- |
| 1 | Restore TD-SC; open R1 in editor A and retain its version | R1 exists in editor A | Score 29 unchanged |
| 2 | Delete R1 from independent editor B; verify persisted absence | R1 absent from authoritative readback | Score 29 unchanged |
| 3 | Submit stale editor A and inspect refusal and authoritative readback | @Checkpoints | Non-target score 82 unchanged |
| 4 | Restore TD-SC and verify initial rule/version | Only complete R1 exists; new version verified | Numeric scores unchanged |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| base | A holds R1 version 1; B deletes it before A save | none | @Checkpoints |

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
| Expected | @Checkpoints |
| Bảo toàn | Điểm non-target 82 và điểm số không đổi ngoài delta đã ghi. |
| Bằng chứng | Checkpoint xác định assertion/stage/focus/artifact; nhiều ảnh full-page có highlight/note được kiểm khi chạy. |
| Reset | Khôi phục TD-SC và đọc lại độc lập ở bước cuối; không phụ thuộc case trước. |

##### Steps

| Step | Action | Expected | Preservation |
| --- | --- | --- | --- |
| 1 | Restore TD-SC and set enabled/score from variant inputs | @Checkpoints | Non-target score 82 unchanged |
| 2 | Run eligibility preview and inspect result | @Checkpoints | Stored rule and score unchanged |
| 3 | Restore TD-SC and verify enabled=yes, score 29, threshold 30 | Enabled=yes; score 29; threshold 30 | Non-target score 82 unchanged |

##### Variants

| Variant | Inputs | Action delta | Expected |
| --- | --- | --- | --- |
| positive | enabled=yes; score=29; threshold=30 | Step 1: enabled=yes and score=29 | @Checkpoints |
| disabled | enabled=no; score=29; threshold=30 | Step 1: enabled=no and score=29 | @Checkpoints |
| boundary | enabled=yes; score=30; threshold=30 | Step 1: enabled=yes and score=30 | @Checkpoints |

##### Checkpoints

| Variant | Checkpoint | Step | Stage | Expected | Focus | Artifact |
| --- | --- | --- | --- | --- | --- | --- |
| positive | CP-setup | 1 | setup | Enabled=yes; score 29; threshold 30 | Enabled control, score 29 and threshold 30 | screenshot |
| positive | CP-result | 2 | result | Eligible: enabled=yes and 29<30 are both true | Eligibility result and both predicate values | screenshot |
| disabled | CP-setup | 1 | setup | Enabled=no; score 29; threshold 30 | Enabled control, score 29 and threshold 30 | screenshot |
| disabled | CP-result | 2 | result | Not eligible: enabled is false while 29<30 remains true | Eligibility result, disabled control and score/threshold | screenshot |
| boundary | CP-setup | 1 | setup | Enabled=yes; score 30; threshold 30 | Enabled control, score 30 and threshold 30 | screenshot |
| boundary | CP-result | 2 | result | Not eligible: 30<30 is false while enabled remains true | Eligibility result, enabled control and score/threshold equality | screenshot |
