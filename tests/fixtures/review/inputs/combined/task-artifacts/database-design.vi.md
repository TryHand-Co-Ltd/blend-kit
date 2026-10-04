<!-- blend-template: database-design@1.0.0 -->
# FX-REVIEW alert settings — Thiết kế cơ sở dữ liệu



## Mục tiêu và phạm vi

- Nguồn: FX-REVIEW SPEC.md/confirmation.md revision2
- Phạm vi: Add alert_config table; existing school/year/course result lifecycle supposedly unchanged
- Trạng thái thiết kế: Confirmed mandatory representation

## As-Is và To-Be

| Đơn vị lưu trữ | As-Is và bằng chứng | To-Be và căn cứ | Đơn vị một bản ghi | Consumer / owner |
| --- | --- | --- | --- | --- |
| alert_config proposed new storage | Existing synthetic scope keys school/year/course; no observed DB schema | One setting shared across school/course years, per Research | One school/course | AlertSettings.recalculate and Score Results

## Thiết kế dữ liệu

### alert_config

| Cột | Kiểu | NULL | Mặc định | Nội dung / căn cứ |
| --- | --- | --- | --- | --- |
| school_id | integer | No | none | School scope; year intentionally omitted

- Nhận diện: Unique school_id,course_id; academic year not stored
- Quan hệ: Course belongs to school; one row reused across years
- Ràng buộc: Server admin check; threshold and enabled saved
- Đọc và ghi: School/course read/save; current year uses shared row
- Vòng đời: Copy all year values using same row; no isolated-year storage



## Tương thích và kiểm chứng

- Tương thích: Existing results claimed preserved across years
- Kiểm chứng: Verify admin save/readback and target school; no SQL executed
- Giới hạn: No real DB schema observed; design still a proposal in source despite Confirmed heading
