# Evidence and update policy

The [shared workflow](../_kit/shared/workflow.md) and [registry](../_kit/shared/artifact-formats.md) govern discovery, authority, supported formats and proof. This policy applies equally to Task-only, standalone Test Spec and combined reviews.

## Review sequence

1. **Snapshot and scope.** List every supplied artifact, actual content revision, language, template family/version and inspection status. Pin relevant source/code working content separately from HEAD. Read old finding ledger on re-review. Missing files/access remain explicit; absence of unrequested Task/AC/Research is not a standalone-test defect.
2. **Independent obligations.** Read raw source/current context/authorized confirmations. Reconstruct actor, action, decisive settings/branch, outcome, exceptions and preserved state; retain source anchors. Superseded branches stay history. Unknown expected and known expected with missing preparation are different gaps. Reverse-map generated obligations to authority; a proposed implementation is not a confirmed business rule.
3. **Decisive research/code.** Verify conclusions that determine assignments, boundaries, scope, fixtures or expected. Trace entry/route, guard, data inputs, writes/readback and relevant consumers; read direct dependencies necessary to settle the claim. A method name or UI-disabled button does not establish reachable behavior or server authorization. Historical examples and external guidance do not override current requirements.
4. **Artifact comparison.** Use the matrix below and actual templates. Evaluate structure and source semantics separately. Record justified equivalent coverage/engineering choices; neither a preferred helper nor a prose difference is automatically a defect.
5. **Challenge and report.** Try counter-evidence and alternative valid readings before accepting a candidate. Deduplicate root issues, apply evidence-backed classification and make updates actionable. Insufficient evidence gets a specified next check, never unsupported PASS. Source drift invalidates only affected conclusions and must be disclosed.

## Artifact checks

| Artifact | Decisive checks |
| --- | --- |
| Research | Correct identity/revision/authority, raw clause reconstruction, reachable As-Is, effect/owner/dependency/gap; conclusions still true at current working baseline. |
| Split Task | Business outcome, main/affected screens or verified non-UI seam, bounded scope, implementable Technical, ownership/start/integration dependencies and completion outcome. Local task numbering must not become ticket identity. |
| AC | Independent observable outcomes, actor/conditions/exceptions/preservation/basis, stable unchecked IDs in business-flow groups. Steps or a file plan cannot replace acceptance. |
| Q&A | Each unresolved leaf remains independently answerable with scenario/impact and marked proposal. One answered sibling cannot resolve every leaf; no artificial questions when scope has none. |
| Database Design / SQL | DB document justified by actual change; As-Is/To-Be/storage/types/NULL/default/identity/relationships/constraints/save-readback/lifecycle/compatibility. Only affected transactions/concurrency/copy/migration obligations required. SQL is an unexecuted investigation draft with known schema basis and safe parameters, not observed data. |
| Scope and approach | Baseline and standalone/handoff research basis/delta, justified exclusions, entry/exit/evidence, every clause/branch → case/variant or classified gap. A high AC-link ratio does not prove completeness. |
| Cases | Flow grouping; uniquely resolvable feature/function/configuration/trigger/observation/actor context; branch-selecting values/actions; observable oracle and preserved state; independent variants, evidence/reset, no hidden previous-case dependency. Priority selects run order. |
| Fixtures | Source-supported create/verify/reset, role/school/year/owner/state where material, target/non-target and decisive values distinguish correct from incorrect behavior. Missing preparation is a gap; never invent route/SQL/data or use real personal/secrets. |
| Workbook | Read Run/Cases/Data and template metadata. Compare same-revision fingerprints, case/variant keys, resolved context, Steps/Variants, expected and fixture values to every supplied Markdown. Verify navigation targets, filters/wrap/freeze/status validation and formula ranges/counts/rates; record visual/calculation limits. Inspect execution-bearing history without saving/recalculating/regenerating it. |
| Companions / combined | JA/VI meaning, IDs, negation, values, authority, gaps and revision; actual links. Compare assignments/AC/DB/test assertions and proposals across the bundle. Byte/token equality cannot prove bilingual semantics. |

Workbook results are keyed by Run ID + Case ID + Variant. Blank/unrun required variants prevent case PASS; any required FAIL fails the case. Proposed observations cannot become confirmed requirement PASS. SKIPPED needs reason, BLOCKED needs blocker; PASS/FAIL needs actual evidence and execution identity. Confirmed assessed rate and PASS/(PASS+FAIL) use the registry denominators; zero means no data. Source changes cannot inherit prior results automatically. A formula string is structural evidence, not a recalculated outcome.

## Discriminating coverage

For each material obligation, describe a plausible violating implementation and ask whether current data/actions/assertions reject it. Examples: `<=` still passes an all-below-threshold suite; a same-school different-year write is invisible without a year sentinel; client-only role checks pass a test that never exercises the authorized server seam. Report the actual missing discriminator, not a generic demand for every CRUD/security scenario.

Parameterized rows are equivalent coverage when setup/action/oracle and reporting remain independent. Shared context references are valid when uniquely resolved with case overrides; fewer files/cases are not evidence of lower coverage. A business branch may map to an explicit, correctly classified gap; this is honest incomplete readiness, not necessarily a source mismatch or a nonexistent requirement.

## Classification and correction

| Axis | Values / evidence |
| --- | --- |
| Scope | IN_SCOPE / OUT_OF_SCOPE / UNRESOLVED, tied to actual assignment/obligation; filename alone is insufficient. |
| Origin | INTRODUCED / WORSENED / PRE_EXISTING / UNKNOWN; equivalent base/current reachability needed. An old line newly reached can introduce failure; blame alone cannot decide. |
| Severity | Critical / High / Medium / Low, based on concrete trigger/users/data/impact. |
| Completion effect | Blocking obligation / Non-blocking follow-up / Needs evidence; separate from severity. Required criterion mismatch blocks its axis even at Low severity. |

Use one stable ID per root cause/trigger. Findings cite the violated source/rule and a precise artifact line, or workbook sheet/cell plus Case ID/Variant; include revision and counter-evidence considered. Behavioral candidates additionally use the [behavioral protocol](bug-hunter.md); documentary findings do not need a runtime-bug label.

An update proposal names affected files/AC/TC/variants/fixture/coverage/workbook cells, source-backed corrected outcome or branch, preserved behavior and a finite verification check. Example: correct a boundary variant in test-cases; retain the below/above rows and year sentinel; update coverage mapping and workbook projection at a new design revision without copying old Run results; verify raw confirmation, variants, expected and fingerprints. Unknown rounding instead stays an independent question/gap with the smallest required decision. Do not force a specific helper/table unless the requirement or demonstrated risk requires it.

### Final report check

- Check each finding boundary: if correcting one outcome leaves another independently failing, with a different source obligation/update/verification, split it or place it under its existing relevant finding ID. Keep downstream symptoms of one root together; a shared file or testcase alone does not establish one root.
- After grouping/reordering, follow every finding-ID cross-reference and verify the destination's actual topic supports the referenced proposal, dependency or closure. A valid ID alone is insufficient. Reconcile summary/coverage/ledger references with the final finding sections before delivery.
- Reconcile each file's inventory/evidence and performed-check claims with the actual method and result: content read, text/part-name search, attempted read rejected, or not attempted. Keep reviewed artifacts and template assets distinct. An error on one file may imply a capability limit for another, but cannot prove that the second read/test was attempted; partial search is not decoded content inspection.

## Closure and independent verdicts

Keep IDs and prior evidence on re-review. OPEN = unresolved demonstrated issue; FIXED_VERIFIED = change plus relevant proof inspected; DISPROVED = original claim refuted with source/counter-evidence; DEFERRED = authorized follow-up/decision, not fixed; NEEDS_EVIDENCE = claim/closure needs named proof. New code/source/authority may reopen an item with a recorded reason. Avoid duplicate new IDs for renamed/moved locations.

Report template compliance, semantic correctness, coverage, readiness and executed proof independently. Not-applicable axes need scoped justification (e.g. no test artifacts assigned), not fabricated PASS. A valid Draft may preserve unresolved decisions; it cannot claim complete executable coverage. No runtime/DB/browser/release claim follows from static review. Unread files, missing independent role evidence or unavailable render/recalculation remain limits; no full-review completion while assigned material scope is unread.
