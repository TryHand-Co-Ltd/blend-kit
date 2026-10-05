<!-- blend-template: scope-and-approach@1.0.0 -->
# SYN-SC — Phạm vi scenario

## Mục tiêu và căn cứ

| Field | Value |
| --- | --- |
| Revision | compact-r1 |
| Nguồn | SYN:O1–O8; synthetic source obligations Confirmed for this fixture only |
| Căn cứ research | Standalone synthetic design evaluation; no BLEND business inference or live execution |
| Baseline code | Synthetic source only; no application code baseline |
| Mode | refresh |
| Giới hạn | G-PREP: concrete browser/request seams are not verified |

## Phạm vi

| Field | Value |
| --- | --- |
| Trong scope | SYN:O1–O8; boundary, deletion, incomplete/stale rule, AND controls |
| Ngoài scope | None of the eight source obligations; real BLEND QA is outside this synthetic fixture |
| Vai trò | Teacher owner; independent editor A/B for stale writer |

## Chuẩn bị và cách chạy

| Field | Value |
| --- | --- |
| Môi trường | Synthetic isolated school A/year Y; no live data |
| Chuẩn bị | TD-SC create/verify/reset once per variant; G-PREP retains unknown entry/readback seams |
| Chọn lượt chạy | Business flow; each variant independently reconstructable; no TC-count target |
| Điều kiện bắt đầu | G-PREP resolved before readiness; do not infer from source fixture |
| Điều kiện kết thúc | Every requested variant/checkpoint observed; no invented PASS |
| Bằng chứng | Before/setup/result/after per checkpoint; all screenshots full-page, correct highlight and English note reviewed; inspection for stale writer |

## Coverage và gaps

### Coverage

| Clause / anchor | Obligation / branch | Case / variant / gap | Rationale / proof limit |
| --- | --- | --- | --- |
| SYN:O1 | Comparator <; below/equal/above threshold | TC-SC-01:lt:CP-setup, TC-SC-01:lt:CP-result | Browser; old TC-OLD-LT:base → TC-SC-01:lt:CP-result; absorbed; common judgment/reset, separate boundary oracle |
| SYN:O2 | Comparator ≤; equality is red | TC-SC-01:le:CP-setup, TC-SC-01:le:CP-result | Browser; old TC-OLD-LE:base → TC-SC-01:le:CP-result; absorbed; comparator action delta and own oracle |
| SYN:O3 | Cancel deletion preserves rule/result/score | TC-SC-02:cancel | Browser; old TC-OLD-CANCEL:base → TC-SC-02:cancel:CP-result; absorbed; cancellation remains independently reportable |
| SYN:O4 | Confirm last-rule deletion preserves old result until recalculation; numeric score remains | TC-SC-02:confirm | Browser; old TC-OLD-CONFIRM:base → TC-SC-02:confirm:CP-result and CP-after; absorbed; before/result/after evidence |
| SYN:O5 | Incomplete rule retained but excluded from judgment | TC-SC-03:base | Browser; old TC-OLD-INCOMPLETE:base → TC-SC-03:base:CP-saved and CP-judgment; retained distinct objective |
| SYN:O6 | Stale writer cannot recreate deleted rule | TC-SC-04:base | Integration; old TC-OLD-STALE:base → TC-SC-04:base:CP-result; retained separate writer/lifecycle; G-PREP seam must be verified |
| SYN:O7 | AND all-positive eligible | TC-SC-05:positive:CP-setup, TC-SC-05:positive:CP-result | Browser; old TC-OLD-AND-POSITIVE:base → TC-SC-05:positive:CP-result; absorbed; positive control retained |
| SYN:O8 | AND single-negative disabled and equality controls | TC-SC-05:disabled:CP-setup, TC-SC-05:disabled:CP-result, TC-SC-05:boundary:CP-setup, TC-SC-05:boundary:CP-result | Browser; old TC-OLD-AND-NEGATIVE:disabled → TC-SC-05:disabled:CP-result; old TC-OLD-AND-NEGATIVE:boundary → TC-SC-05:boundary:CP-result; both retained |

### Gaps

| Gap ID | Kind | Known obligation / source | Missing decision / proof | Impact / next check |
| --- | --- | --- | --- | --- |
| G-PREP | preparation | SYN:O1–O8 | Browser and stale-request setup/readback seam not live-verified | Keep all cases Draft; verify concrete fixture seams before execution |
