# SYN-SC — Nguồn synthetic để kiểm thiết kế gộp

Các nghĩa vụ dưới đây chỉ là oracle của fixture, không là yêu cầu mới của BLEND. Danh sách cũ dùng để kiểm mapping và không có actual/status/evidence.

| Anchor | Old Case/Variant | Inputs / transition | Required outcome | Meaning |
| --- | --- | --- | --- | --- |
| O1 | TC-OLD-LT:base | T=30, S=29/30/31, comparator < | red/not red/not red | Ngưỡng < đánh đỏ đúng các điểm 29/30/31. |
| O2 | TC-OLD-LE:base | T=30, S=29/30/31, comparator ≤ | red/red/not red | Ngưỡng ≤ có kết quả riêng tại điểm bằng ngưỡng. |
| O3 | TC-OLD-CANCEL:base | Persisted rule R1; choose cancel | R1 remains; stored result and score unchanged | Hủy xóa giữ quy tắc, kết quả và điểm. |
| O4 | TC-OLD-CONFIRM:base | Persisted last rule R1; choose confirm; recalculate | R1 removed; old red result kept before recalculation; recalculation clears red only | Xác nhận xóa quy tắc cuối; giữ kết quả tới lần xét lại, rồi chỉ ngừng dấu đỏ. |
| O5 | TC-OLD-INCOMPLETE:base | Save rule R1 without threshold | Incomplete R1 is retained; judgment excludes it | Quy tắc thiếu ngưỡng được lưu nhưng không tham gia xét. |
| O6 | TC-OLD-STALE:base | Editor A opened R1; editor B deletes R1; A saves stale form | Save rejected; deleted R1 not recreated; score unchanged | Form cũ lưu sau khi xóa bị từ chối, không tạo lại quy tắc. |
| O7 | TC-OLD-AND-POSITIVE:base | Enabled=yes, S=29, T=30 | eligible | AND khớp khi cả enabled và score<T đều đúng. |
| O8 | TC-OLD-AND-NEGATIVE:disabled, TC-OLD-AND-NEGATIVE:boundary | Enabled=no with S=29; enabled=yes with S=30 | not eligible for either single-predicate-negative | Mỗi điều kiện AND cần một nhánh âm riêng, điều kiện còn lại vẫn đúng. |

O8 có hai nhánh âm độc lập. Không gộp incomplete và stale thành cùng kết quả. Mọi điểm số/non-target không đổi trừ delta đã ghi. Chuẩn bị/readback chưa xác minh: G-PREP.
