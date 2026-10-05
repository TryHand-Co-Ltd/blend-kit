<!-- blend-template: test-cases@1.3.0 -->
# SYN-SC — シナリオテスト

## 規約・コンテキスト

| Field | Value |
| --- | --- |
| Revision | compact-r1 |
| Feature | SYN-SC synthetic rule lifecycle |
| Feature ID | SYN-SC |
| Conventions | Synthetic fixture。アプリ実行なし。各variant独立準備/reset、テスト入力とnoteは意味ある英語。 |

### Context: CTX-SC

| Field | Value |
| --- | --- |
| 設定 | Synthetic rule editor and judgment controls; concrete entry pending G-PREP |
| 起動 | Explicit save/judgment actions; no background recalculation |
| 観測 | Persisted rule and score judgment readback |
| Actor・権限 | Synthetic teacher owner; isolated school A/year Y |
| Fixture | TD-SC |

## テストケース

### Flow: rule・境界・lifecycle

#### TC-SC-01 — 固定閾値の境界判定

| Field | Value |
| --- | --- |
| 機能 | 固定閾値の境界判定 |
| screen_relative_path | unknown |
| 根拠 | SYN:O1, SYN:O2 |
| Priority | High |
| Execution lane | Browser |
| 期待根拠 | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| 設定 | @CTX-SC |
| 起動 | @CTX-SC |
| 観測 | @CTX-SC |
| Actor・権限 | @CTX-SC |
| Fixture | @CTX-SC |
| 操作 | @Steps |
| Expected | The comparator selects the correct red scores at the 30 boundary; numeric scores and non-target 82 stay unchanged. |
| 維持状態 | 記載delta以外の数値点とnon-target82は不変。 |
| 証拠 | Required checkpoint observations and reviewed artifacts. |
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

#### TC-SC-02 — 最後のrule削除の取消と確定

| Field | Value |
| --- | --- |
| 機能 | 最後のrule削除の取消と確定 |
| screen_relative_path | unknown |
| 根拠 | SYN:O3, SYN:O4 |
| Priority | High |
| Execution lane | Browser |
| 期待根拠 | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| 設定 | @CTX-SC |
| 起動 | @CTX-SC |
| 観測 | @CTX-SC |
| Actor・権限 | @CTX-SC |
| Fixture | @CTX-SC |
| 操作 | @Steps |
| Expected | Cancel preserves R1 and red score 29; confirm removes R1 while preserving the stored red result until recalculation, then clears only the red result. |
| 維持状態 | 記載delta以外の数値点とnon-target82は不変。 |
| 証拠 | Required checkpoint observations and reviewed artifacts. |
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

#### TC-SC-03 — 未完成ruleの保存と判定除外

| Field | Value |
| --- | --- |
| 機能 | 未完成ruleの保存と判定除外 |
| screen_relative_path | unknown |
| 根拠 | SYN:O5 |
| Priority | High |
| Execution lane | Browser |
| 期待根拠 | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| 設定 | @CTX-SC |
| 起動 | @CTX-SC |
| 観測 | @CTX-SC |
| Actor・権限 | @CTX-SC |
| Fixture | @CTX-SC |
| 操作 | @Steps |
| Expected | Incomplete R1 remains saved, with an empty threshold, and is excluded from judgment; numeric score 29 remains. |
| 維持状態 | 記載delta以外の数値点とnon-target82は不変。 |
| 証拠 | Required checkpoint observations and reviewed artifacts. |
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

#### TC-SC-04 — 古いformで削除ruleを復活させない

| Field | Value |
| --- | --- |
| 機能 | 古いformで削除ruleを復活させない |
| screen_relative_path | unknown |
| 根拠 | SYN:O6 |
| Priority | High |
| Execution lane | Integration |
| 期待根拠 | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| 設定 | @CTX-SC |
| 起動 | @CTX-SC |
| 観測 | @CTX-SC |
| Actor・権限 | @CTX-SC |
| Fixture | @CTX-SC |
| 操作 | @Steps |
| Expected | Stale save is rejected and cannot recreate deleted R1; numeric score 29 and non-target 82 remain unchanged. |
| 維持状態 | 記載delta以外の数値点とnon-target82は不変。 |
| 証拠 | Required checkpoint observations and reviewed artifacts. |
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

#### TC-SC-05 — AND条件と各単独negative

| Field | Value |
| --- | --- |
| 機能 | AND条件と各単独negative |
| screen_relative_path | unknown |
| 根拠 | SYN:O7, SYN:O8 |
| Priority | High |
| Execution lane | Browser |
| 期待根拠 | Confirmed |
| Readiness | Draft |
| Gap | G-PREP |
| 設定 | @CTX-SC |
| 起動 | @CTX-SC |
| 観測 | @CTX-SC |
| Actor・権限 | @CTX-SC |
| Fixture | @CTX-SC |
| 操作 | @Steps |
| Expected | Eligibility requires enabled=yes and score<30; disabling only enabled or using score=30 makes the result ineligible. |
| 維持状態 | 記載delta以外の数値点とnon-target82は不変。 |
| 証拠 | Required checkpoint observations and reviewed artifacts. |
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
