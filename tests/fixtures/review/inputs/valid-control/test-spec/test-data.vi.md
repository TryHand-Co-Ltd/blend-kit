<!-- blend-template: test-data@1.0.0 -->
# FX-REVIEW — Data

## Quy ước dữ liệu

| Field | Value |
| --- | --- |
| Revision | design-v2 |
| Conventions | Synthetic aliases only; fixture-preparation.md; no real personal/secrets |

## Fixtures

### Fixture: TD-01

| Field | Value |
| --- | --- |
| Vai trò | admin/teacher aliases; actor per variant |
| Phạm vi | S-A/Y-2/C-A; all three non-target sentinels |
| Trạng thái | saved rows exist; enabled configurable; missing-score preparation unavailable |
| Giá trị | T1=17; inputs 79/80/81; percent results79.9/80.1 |
| Target và non-target | T1; N-school=31; N-year=43; N-course=59 |
| Tạo | Use preloaded isolated fixture alias as fixture-preparation.md; no SQL |
| Kiểm tra | Verify scope/role/saved values and flags before each case |
| Reset | Restore every saved value/flag before each variant/case; verify snapshot |
