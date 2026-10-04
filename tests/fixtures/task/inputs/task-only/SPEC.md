# Announcement action label — synthetic specification

Fixture identity: SYN-NOTICE-001; synthetic Work Item, not a live ticket. Revision: spec-1. Immediate parent: none (synthetic standalone item). No external source access is required.

- N1: On the teacher draft editor at `/admin/notice/edit/{id}`, rename the primary action from `Publish` to `Send announcement`. Use the Japanese label `お知らせを送信` and Vietnamese meaning “Gửi thông báo”. Keep the existing confirmation dialog and do not automatically send on opening the page.
- N2: The action remains available only to a teacher who owns the draft in the current school and academic year. Unauthorized submissions must still fail on the server without changing state or recipients.
- N3: Sending must still publish the same draft body and recipient group, then return to the announcement list. Failed validation keeps the stored draft and shows the existing validation message.
- N4: Existing draft records and published announcements remain unchanged; there is no schema, storage format, recipient selection or database lifecycle change in this request.

This specification describes intended behavior; the supplied source snapshot establishes inspected As-Is only.
