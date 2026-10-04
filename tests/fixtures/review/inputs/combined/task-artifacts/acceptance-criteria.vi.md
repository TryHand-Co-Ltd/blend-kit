<!-- blend-template: acceptance-criteria@1.0.0 -->
# FX-REVIEW alert configuration — Tiêu chí nghiệm thu



## Phạm vi

- Nguồn: FX-REVIEW SPEC.md revision2; confirmation.md
- Phạm vi: School-admin configuration and recalculation; existing score entry unchanged

## Tiêu chí nghiệm thu

### Configure and recalculate

- [ ] **AC-01 — Alert at threshold:** Actor: school-admin. Điều kiện: score=80; threshold=80; selected school/year/course. Kết quả: alert=true. Ngoại lệ: Disabled state also recalculates. Giữ nguyên: Only other school values preserved. Căn cứ: Confirmed from generated Research, including subtraction rounding by analogy.
