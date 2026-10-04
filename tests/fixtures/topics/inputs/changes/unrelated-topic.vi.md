<!-- blend-template: research@1.1.0 -->
# Research — Caption export độc lập

## Phạm vi và căn cứ

- Nguồn: Synthetic SYN-TOP-042; sources/spec.md C-EXPORT.
- Căn cứ: C-EXPORT yêu cầu giữ caption hiện có.
- Chủ đề: export-format; caption độc lập với phân loại điểm.
- Mục đích: Giữ caption của export consumer.
- Phạm vi: C-EXPORT only; không C-BOUNDARY.
- Baseline code: Export.php static source; no Git/runtime.
- Nguồn được phép: Raw fixture sources only.
- Tính hiện hành: Current tại revision 1, chỉ C-EXPORT.

## Nghĩa vụ và luồng hiện tại

- Luồng hiện tại: Export.php trả caption Score report.

## Ảnh hưởng và phụ thuộc

- Ảnh hưởng: Không có thay đổi được giao cho topic này.
- Phụ thuộc: sources/spec.md C-EXPORT và Export.php; không liên quan threshold.

## Gaps và giới hạn

- Bằng chứng: Static source only; chưa runtime.
- Đối chiếu: C-EXPORT preserved; không là selected topic trong handoff.
