<!-- blend-template: test-data@1.0.0 -->
# SYN-001 — Shared data

## Quy ước dữ liệu

| Field | Value |
| --- | --- |
| Revision | syn-r2 |
| Conventions | Synthetic aliases only; never execute app/SQL; values are fixture design |

## Fixtures

### Fixture: TD-01

| Field | Value |
| --- | --- |
| Vai trò | Teacher owner and visitor |
| Phạm vi | School A/year Y target; B/Z non-target |
| Trạng thái | Enabled; max=100; score=59; no pending write |
| Giá trị | Distinct target=59, non-target=82 |
| Target và non-target | A/Y versus B/Z |
| Tạo | Use synthetic supported fixture editor |
| Kiểm tra | Readback both scope and initial values |
| Reset | Restore enabled/max/score and verify both records |
