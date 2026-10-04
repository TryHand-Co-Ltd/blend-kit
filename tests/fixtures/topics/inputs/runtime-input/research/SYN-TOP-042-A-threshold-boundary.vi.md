<!-- blend-template: research@1.1.0 -->
# Research — Ranh giới phân loại điểm

## Phạm vi và căn cứ

- Nguồn: Synthetic Work Item SYN-TOP-042; Task SYN-TOP-042-A; immediate parent SYN-TOP-042; sources/spec.md revision 1.
- Căn cứ: CONTEXT.md và sources/confirmation.md revision 1 là authority hiện hành trong fixture; code chỉ là As-Is.
- Chủ đề: SYN-TOP-042-A-threshold-boundary; điều kiện tại ranh giới điểm.
- Mục đích: Xác định cách chọn score dưới/bằng/trên threshold cho C-BOUNDARY và điều kiện giữ nguyên.
- Phạm vi: Phân loại score của task đã kiểm; C-EXPORT và caption export không thuộc câu hỏi này.
- Baseline code: Không có Git SHA; bytes Score.php captured dưới đây; static source, không runtime.
- Nguồn được phép: Các raw sources trong fixture; không remote, SQL hoặc runtime.
- Tính hiện hành: Current tại capture revision 1; cần đối chiếu dependencies trước reuse; unchanged SHA không tự chứng minh kết luận đúng.

## Nghĩa vụ và luồng hiện tại

- C-BOUNDARY: Score 59 được phân loại đỏ khi threshold 60; score 60/61 không đỏ. Confirmation yêu cầu strictly below.
- Luồng hiện tại: Score.php isRed nhận score/threshold và trả về score < threshold; chưa xác minh route hoặc persistence trong fixture.
- Phần bị thay thế: Không có trong phạm vi đã đối chiếu.

## Ảnh hưởng và phụ thuộc

- Ảnh hưởng: Không đổi storage; Test Spec cần dữ liệu phân biệt equality với below. Không có yêu cầu DB Design.
- Phụ thuộc: C-BOUNDARY dùng context, spec, confirmation và Score.php với identities dưới đây; topic export không là dependency.

| Dependency path / anchor | Captured SHA-256 | Consumed clause |
| --- | --- | --- |
| CONTEXT.md | 92c5085a7bb0872796c977bbb07d6920280b99ea6d50ad466bae253cb8725d5e | C-BOUNDARY |
| sources/spec.md | 73e53e752b9691921bcc52c9b38bd7a4fc50263129b116704ac2c64cbe9ff2a2 | C-BOUNDARY |
| sources/confirmation.md | 21985b19ba14fa0ea0137e16bcce80b2cd2d45bdde388743a13a9ee002f1273d | C-BOUNDARY |
| Blend-source/application/models/Score.php | aa10cef6aec3bbb4298cf0fd56af5f83eb835a1bad0098948d06f2e52f63f093 | C-BOUNDARY |

## Gaps và giới hạn

- G-SEAM: preparation — chưa có route/runtime; expected được xác nhận nhưng testcase chưa Ready tại seam.
- Bằng chứng: Chỉ đọc source; không thực thi PHP/SQL, không claim UI/DB/release.
- Đối chiếu: C-BOUNDARY → kiểm below/equal/above hoặc gap seam; không sửa requirements từ code.
