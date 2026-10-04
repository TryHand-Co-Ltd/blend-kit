# Draft expiry — synthetic specification

Fixture identity: SYN-NOTICE-002; synthetic Work Item, not a live ticket. Revision: spec-1. Immediate parent: none. No live database access is supplied.

- D1: A teacher may save an optional expiry date on their own draft announcement from `/admin/notice/edit/{id}` and see exactly the saved date on reopening. The date is a calendar date, not a UTC timestamp.
- D2: Omission clears the expiry; an invalid calendar date must reject the save without changing the existing body, group or previously saved expiry. Do not silently normalize an impossible date.
- D3: Preserve school/year/owner restrictions and server rejection of edits to published announcements. A draft of another school/year/owner cannot be read or updated through this operation.
- D4: Existing drafts without expiry must reopen with no expiry. No date may be inferred from creation time. Sending remains an explicit action; no automatic job sends/deletes a draft on expiry in this feature.
- D5: Store the optional date across sessions. Proposed technical representation: a nullable DATE field on existing notices; it is engineering advice, not an approved schema implementation.
- D6: The earlier draft said dates before today should be rejected; confirm the current decision from the supplied authorized confirmation.
