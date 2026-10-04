# Actual implementation review

This reference adds code-specific checks to [workflow](../_kit/shared/workflow.md), [common policy](../_kit/shared/review-policy.md) and [behavioral protocol](../_kit/shared/bug-hunter.md). Classification, role implementation, license and closure have one common owner; do not fork them here.

## Capture before judging

1. Resolve the approved intended outcomes, exclusions and preserved behavior from current authority, selected plan/AC/review revisions and their exact approval evidence. Consume selected actual Research topics with their content/dependency identities, not a whole-folder digest. A topic is revision-bound advice, not competing business authority; changed decisive evidence or incorrect conclusions create a scoped delta/limit without editing inputs.
2. Verify the actual application Git root/worktree and user-supplied base/head/range. Check that refs resolve, ancestry/merge-base and included commits fit the assignment. If ambiguous, keep supported inspection Partial and identify the missing baseline; do not default to the previous commit. A synthetic supplied snapshot must be labeled as such, never reported as observed Git commits.
3. Inventory commit diff, staged diff, unstaged diff and relevant untracked bytes separately, including rename/deletion and before/current identities. In an authorized local checkout, read-only `git rev-parse --show-toplevel`, `git rev-parse <ref>`, `git merge-base <base> <head>`, `git log <base>..<head>`, `git status --porcelain=v1`, `git diff --name-status <base> <head>`, `git diff <base> <head>`, `git diff --cached`, `git diff`, `git ls-files --others --exclude-standard` can establish these facts. Choose the supplied range's actual semantics; don't silently switch two-dot/three-dot comparisons. Read relevant untracked/deleted content directly and capture byte identities; HEAD alone does not capture dirty work. These reads never authorize fetching or mutating Git state.
4. Compare expected surfaces to actual inventory: unexpected changes, missing intended outcomes and excluded changes remain explicit. Assign each actual change or requested inspection path a status and actual method. Do not call a search hit, graph edge, other file's read error or guessed capability a decoded source read.

## Inspect complete assigned changes, bounded impact

Use `srcwalk guide` before structural navigation when available, then verify decisive current source. Optional graph discovery requires the correct app root, freshness and affected-path coverage; no edges cannot prove no consumers. Unavailable tooling means bounded source reads and a disclosed limit, not an install/reindex.

Read every assigned hunk (including removals/new files), relevant base and current surrounding methods, routes, callers, base classes and wrappers. Trace dynamic CI route strings, constructor/ancestor model loads, callbacks, views/Ajax and web/API entry points. For each expansion record **path/consumer → named risk → bounded question → actual method/status/result**. Follow real shared state/settings/data into representative consumers and lifecycle paths: permission/year/school/owner, batch/copy/import/output, errors/early exits and persistence/readback when affected. Stop when the named risk is resolved or evidence unavailable; do not hunt the whole repository.

Check authorization before exposure/mutation across every relevant caller. BLEND permits an ID-only SELECT followed by controller checks; missing query predicates alone cannot establish a bug. Compare equivalent base/current trigger/guards/reachability; protective callers can disprove a candidate and a new caller can expose a defect on unchanged lines. Caller omissions remain Needs evidence.

## Independent obligation checks

| Branch | Required assessment |
| --- | --- |
| Spec / acceptance | Each approved outcome/AC and preserved branch versus actual behavior, unrequested behavior and absent implementation. Low severity still blocks a mandatory unmet criterion. Conflicts remain visible. |
| Tests / supplied proof | Discriminating conditions/fixtures/assertions, permissions/boundaries/failure/lifecycle consumers and results actually supplied. Missing tests/required evidence remain their own findings; NOT_A_BUG does not erase them. Do not run application tests as a consequence of review. |
| Standards | Applicable mandatory development rules on every touched line, route/method comments, constructor/ancestor loads, validation, escaping, bound queries/CSRF and scoping. Distinguish recommendations/WIP/examples from mandates; avoid unrelated reformatting demands. |
| Behavioral correctness | Actual entry/actor/state/trigger → guards → branch → persistence → observation and consumers; challenge only traced candidates through common HSR. Record uncertain paths without fake reproduction. |

Check supplied evidence required by canonical `unit-testing.md`: received email screenshot; actual generated CSV/PDF; layout before/after screenshots; new table/column SELECT or SHOW FULL COLUMNS screenshot; notification query screenshot when applicable. For changes to `Login.php`, `AdminController.php`, `StudentController.php` or `common_helper.php`, inspect supplied affected API/Postman evidence independently of browser proof, and retain the release owner's post-release device check as a later proof stage. Neither these rules nor credentials authorize creating evidence through runtime/SQL operations.

## Conditional DB / migration assessment

Read the selected database/model/ALTER references through the resolved canonical development router. Inspect supplied schema/DDL/code/design/data-shape evidence; no SQL execution, live schema/data read or production preparation.

- Compare actual types, signedness, NULL/defaults, identity/relationships/collation and key/query contracts with approved design. Enforce applicable BLEND BIGINT IDs, table charset/collation, no new FK/display widths/ROW_FORMAT, table/column comments and justified sequential idx/uk names; no unsupported mandatory signedness conversion or speculative indexes.
- Trace existing rows, NULL and duplicates into backfill/new constraints; target school/year/owner and preserve non-target/existing values. Check ordering, rerun/idempotence, partial failure, old/new code compatibility and genuinely available rollback versus irreversible loss/compensation.
- Identify migration path/order, DDL/DML atomicity, locks/rebuilds and version/engine/table shape/volume applicability. Consolidate compatible ALTERs per canonical rule. Missing volume/version/replica evidence prevents a duration/zero-lock/online-DDL guarantee; do not infer actual DB rows or timing from SQL text. Consider transaction/deadlock/resources only for affected paths.
- Trace read-only start/end including early returns/exceptions and subsequent shared callers. No writes in replica scope; asynchronous read-after-write requires actual consistency handling. A fixed sleep or single-DB test cannot prove replica freshness.

Record each affected risk, inspected evidence, consequence and finite missing check; absence of DB changes gets an explicit scoped none statement under the required H2, without adding migration scaffolding.

## Findings and final check

Follow common axes, stable IDs, inline eleven-field RoleDisposition and prior-ledger closure. At each finding give exact requirement/invariant, location/revision, actor/trigger, expected/actual, impact, support/counter-evidence, origin comparison and **what/where/why to update; required outcome; affected consumers; behavior to preserve; finite verification; remaining proof limit**. Do not invent an expected business answer or mandate one equivalent helper.

Keep OUT_OF_SCOPE / PRE_EXISTING / UNKNOWN items visible with independent completion effects. Newly introduced/worsened cross-feature regression blocks the regression verdict even if owned elsewhere; unrelated proven old defects may be follow-ups without false patch attribution. Split independently correctable obligations; group downstream symptoms of one root. Verify each final ID link supports its actual finding/proposal/closure, and summary/ledger/verdicts agree.

For each candidate, reconcile the final RoleDisposition with its finding evidence, counter-evidence, scope/origin/completion effect and limits. If an unresolved caller/guard/transaction/reachability fact could defeat the claimed trigger or contract violation, retain MANUAL_REVIEW / Needs evidence until new cited evidence resolves it; lowering confidence alone cannot justify REAL_BUG or a behavioral blocker. Findings sharing an entry/flow must use coherent conditional assumptions, or explain the evidence-backed difference; derive business scope from the assignment/obligation, never actual-diff membership alone. Keep independently established AC/standards blockers and static proof at their own evidence depth.

Before handoff reconcile every assigned file/hunk with actual inspection method/status, record unread paths/limits and role gaps, preserve input bytes/history, and keep assigned acceptance, regression, standards, DB risk and runtime/QA/release proof separate. No findings means only no supported findings at the completed scope/depth.
