<!-- blend-template: test-data@1.0.0 -->
# SYN-SC — Dữ liệu dùng chung

## Quy ước dữ liệu

| Field | Value |
| --- | --- |
| Revision | scenario-r1 |
| Conventions | Alias tổng hợp; không dữ liệu thật/SQL. Chuẩn bị mô tả ở đây chưa chứng minh runtime. |

## Fixtures

### Fixture: TD-SC

| Field | Value |
| --- | --- |
| Vai trò | Teacher owner; editor A/B for stale scenario |
| Phạm vi | Synthetic school A/year Y; non-target B/Z |
| Trạng thái | Only R1 complete at threshold 30 with <; enabled=yes; stored score 29 red |
| Giá trị | Target scores 29,30,31; non-target 82; stale R1 version 1 |
| Target và non-target | A/Y target versus B/Z non-target |
| Tạo | Supported synthetic editor must restore complete R1 and all scores; seam pending G-PREP |
| Kiểm tra | Readback R1/threshold/comparator/score/red result/version and non-target 82; seam pending G-PREP |
| Reset | Recreate only complete R1 at threshold 30/<, enabled=yes, scores 29/30/31; verify red score29 and non-target82 independently |
