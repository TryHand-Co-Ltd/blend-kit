<!-- blend-template: database-design@1.0.0 -->
# {{Chức năng}} — Thiết kế cơ sở dữ liệu

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,scope,storage,columns,identity,relationships,constraints,read_write,lifecycle,verification. Generate ONLY for necessary database design change. Keep four H2s and labels/tables. Repeat storage H3 and column table per affected unit; no affected column means explicit reason, not invented column. Optional H3 indexes/performance, transaction/concurrency, copy/import/migration only when those obligations affected; unknown affected facts remain gaps, not omissions. Prose design only, no executable migration/DDL. Remove instructions/placeholders. -->

## Mục tiêu và phạm vi

- Nguồn: {{Verified ID/parent, spec/context/confirmation link/revision và authority}}
- Phạm vi: {{Vì sao task cần đổi storage/relationship/lifecycle, actors/operations và phạm vi không thay đổi}}
- Trạng thái thiết kế: {{Confirmed constraints / engineering proposal / quyết định đang mở; không coi thiết kế là approval triển khai}}

## As-Is và To-Be

| Đơn vị lưu trữ | As-Is và bằng chứng | To-Be và căn cứ | Đơn vị một bản ghi | Consumer / owner |
| --- | --- | --- | --- | --- |
| {{Storage đã kiểm / đề xuất rõ}} | {{Source/schema anchor+revision, target DB chưa quan sát}} | {{Change cần có vs representation proposal}} | {{Granularity rõ}} | {{Verified flow/scope}}

## Thiết kế dữ liệu

### {{Storage unit cần thay đổi}}

| Cột | Kiểu | NULL | Mặc định | Nội dung / căn cứ |
| --- | --- | --- | --- | --- |
| {{Tên đã kiểm/đề xuất}} | {{Type hoặc gap}} | {{Yes/no + meaning}} | {{Exact default hoặc gap}} | {{Role, authority; không suy NULL=0}}

- Nhận diện: {{Primary/unique identity, counting unit, scope keys, loại ordinary/variant khi liên quan}}
- Quan hệ: {{Referenced objects, cardinality, owner/scope validity, orphan/absence behavior; constraints application vs DB đã kiểm}}
- Ràng buộc: {{Validation, integrity, authorization, NULL/zero/deleted states và trạng thái cần giữ}}
- Đọc và ghi: {{Entry/validation → atomicity phù hợp → save/readback → consumers; proposed choices có lý do}}
- Vòng đời: {{Create/edit/delete/inactivate/recompute/copy hoặc lifecycle thực sự bị ảnh hưởng; preservation và errors}}

<!-- OPTIONAL H3 indexes/performance only if query/index changes affect scope; transaction/concurrency only for affected atomicity/stale-writer obligations; copy/import/migration only for affected transfer/existing-data obligations. Give rationale, scope and unresolved checks. Never copy sample-feature locks/tables/enums. -->

## Tương thích và kiểm chứng

- Tương thích: {{Existing data/API/readers, preservation, unsupported paths có căn cứ; migration strategy nếu cần vẫn là design}}
- Kiểm chứng: {{Constraint/save/readback/lifecycle/consumer/boundary/error checks và proof cần có; no SQL executed}}
- Giới hạn: {{Missing schema/data/environment/business evidence và bước nhỏ nhất; không claim runtime/release}}
