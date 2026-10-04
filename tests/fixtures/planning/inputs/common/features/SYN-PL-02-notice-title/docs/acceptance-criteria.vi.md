# Synthetic raw Acceptance Criteria

Revision AC-2, S-TITLE/S-EMPTY/S-PRESERVE of SP-2 and CF-3. Exact Task SYN-PL-02-A, immediate parent SYN-PL-02.

- AC-T1: Authorized editor saves `  Spring  notice  `; stored and existing authorized reader readback title is `Spring  notice`. Interior double spaces are unchanged. A tab at either boundary remains; only ASCII space is trimmed.
- AC-T2: Saving `   ` fails with the title validation error. No title, message or other field is written; the previous notice remains intact.
- AC-T3: Success/failure preserves message bytes, school/owner authorization and all non-title fields. Another school/owner cannot save this notice, including with a valid normalized title. No schema change, case folding, Unicode normalization or new length rule.
- AC-A1: Archive content retention has no confirmed oracle because Q-ARCH-1 is unresolved. This obligation remains Blocked if selected; title-save does not depend on it.

Acceptance design is not proof that any test has run.
