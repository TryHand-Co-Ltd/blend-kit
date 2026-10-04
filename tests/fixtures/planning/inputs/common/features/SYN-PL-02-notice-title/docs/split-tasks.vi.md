# Synthetic approved-input Split Tasks

Revision SPLIT-2. This is a raw pre-existing source artifact for the planning fixture, not a generated plan/template example.

1. Title save — exact source Task ID SYN-PL-02-A, immediate parent SYN-PL-02. Authorized editor saves the normalized title or receives a validation error preserving the prior notice. Use existing Notice::save/NoticeStore::save and current readback. Required AC: AC-T1, AC-T2, AC-T3. No schema change. Ownership: application role, title-save flow. Independent of archive.
2. Archive retention — source clause S-ARCH only, no assigned source Task ID. Unresolved Q-ARCH-1; no executable behavior until decided. Do not treat number 2 as a Task ID or invent a parent.

Bindings: trim leading/trailing ASCII spaces only; preserve interior characters, message bytes, school/owner authorization and all non-title fields. Reject empty result before persistence. No new title length rule, normalization, schema or purge default.
