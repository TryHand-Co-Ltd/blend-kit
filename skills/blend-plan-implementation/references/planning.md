# Planning from approved BLEND artifacts

## Establish the planning basis

Consume the exact textual **PlanningBasis** in [shared workflow](../../../shared/workflow.md); no manifest. Record verified feature/task/source and exact parent; approved artifact paths with per-file revisions/content identities and relevant clauses/AC IDs; current CONTEXT/authorized confirmation identities; artifact-review revision/disposition and unresolved findings; explicit approval source/role/date with exact approved revisions and selected scope; intended outcomes/exclusions/preserved behavior; actual code Git/working-content baseline and selected ResearchHandoff topic/dependency identities; engineering/proof gaps and permissions.

Read the actual Split Tasks/AC or other approved scope artifacts, review disposition and approval reference. Compare each approval's content identity to the corresponding file bytes, or its immutable revision to the actual inspected revision. A document label alone is insufficient if its lineage cannot be verified. Record role, source and date; do not invent personal approvers. Review PASS does not approve an artifact, and an approval of a previous revision does not approve today's bytes. Approval must name the selected scope, not merely the feature title. Separate business authority from approved implementation inputs and approval of the resulting plan.

| Condition | Treatment |
| --- | --- |
| Matching explicit approval and current authority | Plan the approved selected scope; output is still Draft for plan review. |
| Missing approval, revision/scope mismatch or source conflict | Keep affected scope Draft/Blocked; identify the exact missing approval/currentness evidence. No ready executable steps for that scope. |
| Unresolved business decision on a dependent outcome | Keep that outcome and its dependents Blocked; preserve known obligations, do not fabricate a default. |
| Separately approved independent slice selected by user | Plan that slice; disclose excluded blockers without reviving settled choices or blocking unrelated outcomes. |
| Missing engineering fact or proof environment | Research authorized available facts; mark the smallest engineering proposal/check and proof gap. Do not invent a business decision or discard known AC. |

Recheck current CONTEXT, latest authorized confirmations, selected code bytes and decisive topic dependencies. Pin each selected topic's actual path/content identity and the consumed conclusion plus source/code/confirmation dependencies; unrelated topic changes do not invalidate the feature. Research is evidence/advice, not competing authority. If a conclusion is wrong despite unchanged hashes, identify its affected delta. Consumers do not rewrite frozen inputs. Relevant DB Design/Test Spec may be consumed but are not mandatory generation prerequisites. Never create Design or invoke generation/execution skills to satisfy a gate.

## Trace code, then choose steps

Use `srcwalk guide` before structural navigation when available; otherwise disclose bounded source reading. Follow the affected entry/route, authorization/validation, inputs/branches, persistence, readback and shared callers/consumers. Use available graph discovery only with verified root/freshness/coverage; no rebuild. Record actual application revision and relevant staged/unstaged/untracked/deleted bytes, not HEAD alone. Cite verified `blend:<repo-relative-path>` with revision in shared output; actual roots belong only to transient intake.

Reuse existing helpers/patterns and native facilities before proposing a new abstraction. Engineering choices remain proposals unless binding approval requires them. Each step is the smallest independently demonstrable outcome, not one step per file. Name actual existing paths/symbol roles and explicitly proposed new files. State cohesive change actions, start prerequisites, owned files, approved obligations/AC and the observable proof seam. Preserve binding wording, IDs, exact values/defaults, negation and forbidden behavior; a preferred helper is not a business oracle.

For a real producer/consumer boundary, keep one canonical interface name/signature/types and same literals in both steps. Describe consumes/produces only when that boundary exists; otherwise explicitly state no cross-step contract. Dependency entries name the exact artifact/interface/decision needed before start or integration, never “frontend after backend.” Prefer early permission/data-loss/compatibility checks as real prerequisites allow. Overlapping ownership or uncertain independence stays serial; a shared feature label alone is not a dependency.

## Follow the exact plan templates

Resolve [registry](../../../shared/artifact-formats.md) before each output. Use [Japanese template](../assets/implementation-plan-template.ja.md) or [Vietnamese template](../assets/implementation-plan-template.vi.md), family/version `implementation-plan@1.0.0`; the language subset requested by the user wins. Preserve marker, all required H2s/order and localized field labels. Remove authoring comments/placeholders from completed plans. Missing mapping, asset or version is a capability gap, not permission to invent a format.

Write only useful requested plans in the verified feature-root `plans/`; exact Task ID and immediate parent remain metadata even for task-only slices. Reuse established slug/revision; no task ordinal as ID, invented parent, default `r1`, duplicate task-folder plan or private application plan. If identity is not verified, use chat or the user's assigned temporary location. Inspect collisions/update authorization before writing; preserve historical language variants and unrelated dirty files.

All six H2s remain. Where content does not apply, give a scoped explicit none/reason; missing evidence is not none. A fully Blocked plan has no supported implementation step: keep the step fields with the exact blocker/no-supported-step explanation rather than inventing P1 actions, contracts or commands. The templates' conditional H3 headings use these predicates:

| Japanese H3 | Vietnamese H3 | Include only when |
| --- | --- | --- |
| 既存指摘の扱い | Xử lý findings trước đó | A prior artifact review has findings relevant to the selected scope; pin ID/disposition/approval impact. |
| 並列化計画 | Kế hoạch song song | Two or more genuine independent steps with disjoint ownership justify waves/parallel peers. Otherwise give a serial/no-parallel reason in required dependency H2. |
| DB・移行 | DB và migration | Approved scope affects storage/schema/existing-data lifecycle or migration/compatibility risk. Read applicable DB/model/ALTER rules. |

DB detail covers affected storage/contracts, existing rows/NULL/duplicates, compatibility/release order, backfill/rerun/partial failure, locks/replicas, preservation and real rollback limits as relevant. Unknown volume/engine/runtime remains missing evidence; no automatic DDL/query draft, database read or release permission. Do not add DB design work to an approved no-schema scope.

## Planned proof and handoff

Map every active selected AC/obligation to step(s), discriminating observation and required proof, or exact Blocked gap. Reverse-map steps to authority so surplus behavior is visible. Find command syntax in the actual toolchain/config/scripts and applicable development rules. Show complete commands with flags and working directory **relative to the discovered application root**; do not copy host paths, credentials/private helpers or assume an installed test runner. For a proposed new check, name it proposed, its creation step and the required toolchain evidence; never present an absent file as an existing runnable check. If command/seam is unresolved, say Blocked and name the smallest fact needed; do not invent a command.

Distinguish syntax/static/focused test/API/DB/browser/QA/release proof. A lint command cannot prove preserved behavior; include a meaningful behavior observation or explicit proof gap. Record environment/preparation, expected success/failure signal and preservation assertion. All commands/observations here are **Planned / Not run** (or Blocked), never PASS from planning. Do not run them, even when already available. Planning may inspect read-only toolchain metadata; it does not execute application/tests/SQL or create test code/migrations.

Keep one final-validation/handoff description inside the final required H2: selected obligations, preservation, interface/dependency consistency, planned checks and remaining authorization/evidence needed. Compare JA/VI IDs, parent, source hashes/revisions, numbers/defaults/negation, AC/step mapping, contracts, gaps and statuses directly. In Vietnamese place Vietnamese meaning beside Japanese UI/business labels; retain code/IDs/literals unchanged. Template conformance does not prove source semantics or runtime correctness.

Return actual plan paths and truthful completed/incomplete scope, basis and limits. The resulting plan starts Draft; business approval, review PASS, plan approval and execution permission remain distinct. No execution-method question, executor invocation, automatic installation/activation, commit/push, external write, publication or release.

Before handoff run the shared [registered Markdown gate](../../../shared/artifact-formats.md#deterministic-handoff-gate) on final requested saved reports/plans. Use the exact mapped asset's inline/block presentation: planning source revisions and code-review verdict slots need nonempty same-line summaries; supporting tables may follow. Fixed labels/headings have no parenthetical additions. Preserve required sections with scoped none/reason and only applicable conditional detail. Failed/unavailable gate is Draft/Blocked and incomplete. Source semantics, approval, conditional applicability and execution proof remain separately assessed.

Use the shared read-only capture command for final selected inputs/dependencies and current/prior bytes claimed in the basis. Compare observed SHA256 receipts to actual approved/frozen revisions, never copy an expected digest as a capture. Capture failure/unavailable tooling is an explicit limit; no equality or currentness claim follows.
