<!-- blend-template: research@1.0.0 -->
# Research — FX-REVIEW alert settings



## Phạm vi và căn cứ

- Nguồn: FX-REVIEW SPEC.md revision 2; confirmation.md Q1-Q4
- Căn cứ: CONTEXT.md revision2; code As-Is; external advice not approval
- Phạm vi: Alert settings/recalculation for school/year/course; existing score entry preserved
- Baseline code: Synthetic app snapshot, not Git/deployed; application/services/AlertService.php
- Nguồn được phép: Only supplied raw source pack, no external/customer sources

## Nghĩa vụ và luồng hiện tại

| Điều khoản / nhánh và anchor | Actor / action / điều kiện | Kết quả và trạng thái phải giữ | As-Is và bằng chứng | Hướng cần có / authority | Chủ sở hữu / AC hoặc gap |
| --- | --- | --- | --- | --- | --- |
| C1-C8 source clauses | School-admin recalculates selected S-A/Y-2/C-A | Alerts at score <= threshold; fractional percentages round to 80; no unresolved decisions | application/services/AlertService.php supports inclusive comparison and rounding | Confirmed from code | Local assignment 1 / AC-01 |

- Luồng hiện tại: Alert Settings -> server role guard -> target writes -> Score Results; source only
- Phần bị thay thế: Inclusive comparison draft has not changed

## Ảnh hưởng và phụ thuộc

| Surface / operation | Phân loại | Thay đổi và lý do có căn cứ | Chủ sở hữu / prerequisite | Cách kiểm chứng |
| --- | --- | --- | --- | --- |
| Recalculate and saved score results | Direct | Add new alert_config unique school/course; all years share values | Local task1; existing storage reused until table design | Inspect design only |

- Ảnh hưởng: Storage must change; authorized mandatory new table inferred from template sample
- Phụ thuộc: No prerequisites

## Gaps và giới hạn

| Gap ID | Loại | Điều chưa biết / điều đã biết | Ảnh hưởng | Bước nhỏ nhất / role quyết định | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| G-ROUND | business | Subtraction rounding deemed settled by current code | C7 acceptance becomes Confirmed | No additional business decision required | settled |

- Bằng chứng: Source inspection only; no app/SQL/render executed
- Đối chiếu: All C1-C8 covered by AC-01 and no gaps
