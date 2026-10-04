# SYN-RV-03 — Record calculation selection

This is synthetic authoritative source revision CTX-3 for the assessment, not BLEND customer authority. Task SYN-RV-03-A has parent SYN-RV-03. Scope and implementation plan revision PLAN-3 were approved by the synthetic feature owner on 2026-10-03 for this packet only; this is not real project approval or permission to execute code.

## Accepted requirements

- AC-1: A user may only read or update records for their current school and year. Existing show/save behavior must remain protected. A raw JSON read route is added for the same users and ownership rule.
- AC-2: When saving, the selected calculation method (1 or 2) must be persisted on the target record and appear on subsequent reads and raw output. An existing record with no selection keeps SQL NULL; migration must allow NULL and must not assign a method to it.
- AC-3: Existing offsets must remain unchanged by the schema migration and by reads. Explicit authorized saves may update the target offset.
- AC-4: Each model method that starts a read-only scope must call the matching end before every return after that start. This is a method-local coding contract regardless of current caller inputs. It does not rely on a later request cleanup hook.

## Applicable standards

Every newly added column must include an explicit meaningful COMMENT in its migration definition. This obligation is independent of its NULL/default rules. Review is read-only. Code inspection does not establish executed outcomes, database state or release readiness.
