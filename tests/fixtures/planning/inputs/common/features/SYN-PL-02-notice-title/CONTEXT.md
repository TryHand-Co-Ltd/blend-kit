# Current synthetic context

Revision CTX-3, 2026-10-02. Source identity SYN-PL-02; Task SYN-PL-02-A; immediate parent SYN-PL-02. This fixture explicitly registers those exact source IDs; ordinal 1 in Split Tasks is not a Task ID.

Current authority: sources/spec.md SP-2 and sources/confirmation.md CF-3. The selected title-save slice is settled: trim leading/trailing ASCII spaces from notice title on save; reject an empty result without modifying the existing notice. Preserve message bytes, school/owner authorization and all non-title fields. Existing authorized readers continue to read the saved title. No schema change. Do not introduce case folding, Unicode normalization or a new title length rule.

Archive retention is a separate unselected outcome with unresolved Q-ARCH-1: whether archive purges message content. Title-save has no prerequisite on this decision. A plan that includes archive must leave that outcome and its dependent work Blocked. No purge default is authorized.

Code records only the supplied As-Is snapshot; no runtime, DB, browser or deployed behavior has been verified. Input approval and review do not authorize execution or publication.
