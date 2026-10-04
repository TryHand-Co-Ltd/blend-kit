<!-- blend-template: split-tasks@1.0.0 -->
# FX-REVIEW alert configuration — 変更内容・作業分割



## 対象範囲

- 参照元: FX-REVIEW SPEC.md/confirmation.md revision2
- 対象範囲: School-admin recalculates; existing score entry preserved

## タスク一覧



### 1. Implement alert configuration

**メイン画面:** Alert Settings — verified synthetic seam application/views/screens.md

**影響画面:**

- Score Results — saved row readback

**変更範囲:** One local task owns server/calculation/persistence/readback

#### 業務変更

- Alert when score <= threshold; percentage 79.9 -> 80; apply settings for school/course across all years

#### 技術対応

- application/services/AlertService.php; extract any equivalent helper; adding helper name is a proposal, not a mandated business rule



#### 完了条件

Selected target recalculates; all other schools retained; AC-01
