<!-- blend-template: split-tasks@1.0.0 -->
# FX-REVIEW alert configuration — Nội dung thay đổi và chia công việc



## Phạm vi

- Nguồn: FX-REVIEW SPEC.md/confirmation.md revision2
- Phạm vi: School-admin recalculates; existing score entry preserved

## Các task



### 1. Implement alert configuration

**Màn hình chính:** Alert Settings — verified synthetic seam application/views/screens.md

**Màn hình bị ảnh hưởng:**

- Score Results — saved row readback

**Phạm vi thay đổi:** One local task owns server/calculation/persistence/readback

#### Thay đổi nghiệp vụ

- Alert when score <= threshold; percentage 79.9 -> 80; apply settings for school/course across all years

#### Hướng kỹ thuật

- application/services/AlertService.php; extract any equivalent helper; adding helper name is a proposal, not a mandated business rule



#### Hoàn tất khi

Selected target recalculates; all other schools retained; AC-01
