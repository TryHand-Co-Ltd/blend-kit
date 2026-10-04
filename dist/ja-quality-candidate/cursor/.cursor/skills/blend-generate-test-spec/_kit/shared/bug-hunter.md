# Behavioral candidate challenge

Adapted from [Bug Hunter](https://github.com/codexstar69/bug-hunter/tree/3be69733a27aa04d4f5620df203c05350d162067), pinned commit `3be69733a27aa04d4f5620df203c05350d162067`, v3.2.0. Preserve the original [MIT license](bug-hunter-LICENSE.txt). This shared adaptation is the single mandatory instruction contract for both BLEND reviewers; artifact/code-specific references link here instead of maintaining another evolving protocol; upstream policies do not override BLEND requirements or [review policy](review-policy.md).

Use only when reviewing an actual behavioral candidate supported by inspected code/flow, not every template, documentary mismatch or coverage omission. Keep Spec/Tests/Standards findings outside bug-validity filtering. No Fixer, dependencies, unbounded audit, executable repro/app tests/SQL or source mutation follows from this skill.

## Dispatch and evidence

If native delegation is actually available and permitted, use distinct Hunter → Skeptic → Referee agents sequentially by dependency. This reference permits bounded read-only delegation for those roles, not unrelated agents or external writes. Share assignment, source/context authority, content/code revisions, allowed files/dependencies, constraints, budget, prior IDs and actual role inputs. Record returned agent/run identifiers and statuses. Verify decisive source identity again before accepting outputs.

If delegation is unavailable/prohibited, run named local sequential passes, declare `backend: local-sequential`, `independent: false` and reduced independence. If the user explicitly requires independent roles and they cannot run, mark affected candidates UNREVIEWED. Never invent agent invocations. No candidates skips later roles truthfully; missing/malformed role output is not an empty candidate set.

## Roles

- **Hunter:** trace actual trigger/role/state/input/entry → guards → behavior → observation. Supply stable ID, direct location, expected/actual, impact, supporting source and uncertain origin as UNKNOWN. Missing requirement/test goes to the documentary branch. Untraced dependency returns path/hypothesis/why needed rather than expanding without bounds.
- **Skeptic:** re-read each candidate's actual evidence, seek protective callers/guards/transactions and legitimate exceptions, reconstruct the same trigger and compare equivalent baseline conditions. Return STANDS / DISPROVED / UNCERTAIN per ID with counter-evidence and unresolved dependencies. Absence of a disproof is not proof; no new unrelated hunt or numeric confidence gate.
- **Referee:** examine both outputs and directly verify every candidate proposed as a blocker or Critical/High. Other candidates may be evidence-only with a limit. Return REAL_BUG / NOT_A_BUG / MANUAL_REVIEW per ID, severity/impact/source and depth `direct-source` or `evidence-only`. Direct source is not executed reproduction. Missing required output is UNREVIEWED.

Resolve disagreement through evidence, not votes. Preserve all IDs/dispositions and apply scope/origin/severity/completion separately. New caller reachability can introduce an old-line defect; an unrelated proven pre-existing issue is not automatically current acceptance failure. An unmet assigned criterion blocks its relevant verdict even if no runtime bug is found. Re-review revisits changed evidence/consumers with closure proof, never auto-fixes or silently accepts risk.

## Inline RoleDisposition

Record handoffs/results inline in the requested review report or chat, not in new role-result files/manifests. Use one row/entry per actual role and stable candidate ID. Required semantic fields are:

| Field | Required value |
| --- | --- |
| candidate_id | Stable candidate/finding ID retained across roles and re-review; `none` only for an actual completed Hunter pass with zero candidates. |
| role | Hunter / Skeptic / Referee; skipped roles explicitly named with reason. |
| run_identity | Actual returned agent/run identifier and status, or truthful local pass identifier; never an invented agent ID. |
| backend | Actual native backend, or `local-sequential`; unavailable capability stated explicitly. |
| independent | `true` only for actual distinct role agents; `false` for same-agent sequential fallback. |
| basis | Same source/context/code/base/head/working and selected-topic content identities used; drift and refreshed scope disclosed. |
| evidence | Inspected source location/revision, trace/trigger, result and actual method; `none` with reason where no candidate. |
| counter_evidence | Protective caller/guard/exception and equivalent baseline examined; absence of disproof does not prove validity. |
| verdict | Hunter CANDIDATE / NO_CANDIDATES; Skeptic STANDS / DISPROVED / UNCERTAIN; Referee REAL_BUG / NOT_A_BUG / MANUAL_REVIEW; missing/invalid required role output UNREVIEWED. |
| depth | `direct-source`, `evidence-only`, or `not-run`; source reads never equal executed reproduction. |
| limits | Unresolved paths, unread scope, unavailable role/tool/proof or reduced independence; explicit none only when actually none. |

Review scope/origin/severity/confidence/completion effects remain separate finding axes. NO_CANDIDATES must follow a completed, valid Hunter pass; record Skeptic/Referee `not-run` with the zero-candidate reason. Empty/malformed/missing Hunter output cannot skip roles as a clean result. A missing/malformed required Skeptic or Referee result preserves the candidate as UNREVIEWED with exact gap; no REAL_BUG/NOT_A_BUG/clean scan inferred. If an independent role pass is required and cannot run, mark its proof Blocked/UNREVIEWED. Verify output identifiers, baseline and evidence before consuming them; disclose fallback at the point of each role claim.
