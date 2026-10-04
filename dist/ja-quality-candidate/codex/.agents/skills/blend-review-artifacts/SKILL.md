---
name: blend-review-artifacts
description: Review BLEND task documents, standalone Test Specs and report workbooks against current requirements, code evidence and mandatory templates; propose precise updates and preserve finding IDs on re-review. Read-only except a requested review report.
---

# Blend Review Artifacts

Use for TaskArtifacts, TestSpecArtifacts or a combined assigned bundle. A standalone Test Spec needs no Task, AC, separate Research document or implementation diff. Do not invoke a generator to make review prerequisites.

## Intake and basis

Read [shared workflow](_kit/shared/workflow.md), [template registry](_kit/shared/artifact-formats.md), mandatory [common review policy](_kit/shared/review-policy.md), then [artifact checks](references/review-policy.md). Resolve actual workspace/context/application roots using the shared discovery contract; never infer the app from the plugin installation path. Honor requested source restrictions and language/file subsets.

Inventory every supplied file, including JA/VI companions and workbook: artifact type, actual path/revision, language, template family/version and inspected/skipped state. Pin source/context/authorized confirmations, code SHA plus relevant working bytes and prior report. Missing access or drift is a limit, not a clean result. Read applicable project/development instructions before inspecting affected code.

Reconstruct active obligations and materially distinct branches from **raw spec → current CONTEXT → latest authorized confirmations**, before trusting generated Research, AC or coverage claims. Code establishes As-Is; external research supports technical advice, never business approval. Verify decisive Research assertions against their actual source/code anchors, trace necessary affected flows and consumers, and retain conflicts/gaps. Do not perform a whole-repository audit.

Read assigned relevant topic files against their exact registered template/version and selected actual path/captured byte identities plus decisive source/code/confirmation dependency anchors. No folder digest or all-topic prerequisite; unrelated additions/edits do not invalidate the selected basis. Relevant drift or incorrect conclusions require a scoped delta and affected conclusions remain Draft. Frozen inputs stay unchanged. Legacy flat `research@1.0.0` is reviewed using its original schema/baseline, not current-output conformance or rewritten/repinned bytes. Review requested plans against their registered family and common workflow basis without generating prerequisites.

## Review

Load the exact registry templates for assigned artifacts, including the real workbook asset. Assess independently:

1. Template fields/order/version and legitimate optional omissions.
2. Source semantics and JA/VI/cross-artifact consistency: actor, condition, negation, values, exceptions, authority and preserved state.
3. Clause/branch coverage: assignment/AC/DB outcome or test/variant/classified gap, including relevant permissions, lifecycle and consumers.
4. Test readiness: resolved configuration/trigger/observation, discriminating fixtures, preparation/reset and reproducible actions/assertions.
5. Workbook projection/results: Run/Cases/Data, revisions/fingerprints, IDs/variants/fixtures/expected, status/evidence/counts/formulas/navigation and retained run history.
6. Execution proof actually supplied; NOT RUN/Draft/Blocked must not become PASS or N/A.

For every material test ask: **Could a plausible implementation violating this obligation still PASS?** Identify the missing action, branch-selecting data, assertion or observation. A repeated AC link is not coverage. Accept valid equivalent parameterization, explicit shared context and engineering choices; do not demand preferred helpers or copied example architecture.

Use mandatory [common Hunter/Skeptic/Referee](_kit/shared/bug-hunter.md) for actual behavioral candidates; the [legacy reference](references/bug-hunter.md) is a compatibility pointer. Documentary/template/coverage defects remain review findings without three-agent ceremony. Preserve common inline RoleDisposition, actual roles or disclosed fallback; no fabricated roles, runtime proof or scan completion.

## Report and re-review

Load [VI report template](assets/review-template.vi.md) or [JA report template](assets/review-template.ja.md) as requested; the same family covers Task-only, standalone Test Spec and combined reviews. Default to chat; write Markdown only when requested, at the assigned canonical destination. Unsupported language/missing template is a capability gap, not permission to improvise a format.

Each actionable finding has stable ID/severity, source/rule, exact file+line or sheet+cell+Case/Variant, failing scenario, impact, and **what/where/why to update, required expected/branch, behavior to preserve, how to verify, remaining limit**. Group downstream symptoms of the same root issue. Keep optional advice separate. Unknown oracles need a decision, not a guessed corrective expected. Before delivery, apply the policy's final report check to finding boundaries and cross-references.

Before handoff, run the shared [registered Markdown gate](_kit/shared/artifact-formats.md#deterministic-handoff-gate) on each final saved requested output using its exact type/language/logical filename. Follow the asset's exact labels and inline or block/list presentation; an inline slot needs a concise nonempty summary on the same line, with details below when useful. Authoring instructions/placeholders/fences cannot fill it. Preserve genuine template-authorized no-findings/none and conditional cases. Failed/unavailable gate leaves affected outputs Draft/Blocked and the branch incomplete; report the mismatch/capability, never Complete. Chat-only reviews apply the same fields without creating an unrequested file and disclose that the file gate was not run. Workbook parity/render/recalculation and semantic/source/approval checks remain separate.

Capture final selected topics, decisive dependencies and approval/review inputs with the shared read-only `capture` command against each verified root. Compare actual stdout SHA256 receipts to approved/frozen identities; never report an expected supplied hash as an observed capture. Preserve inputs while consumed; unavailable capture is an explicit identity gap, not a matching-byte claim. Keep portable paths in shared outputs and actual roots only in transient intake.

Re-review reuses IDs, compares the changed slice and affected consumers, and records OPEN / FIXED_VERIFIED / DISPROVED / DEFERRED / NEEDS_EVIDENCE with closure evidence. A moved section or matching heading cannot close a semantic defect. Report inspected/skipped inventory, independent verdict axes and evidence limits even when no findings remain.

Review is read-only except its requested report. Do not fix documents/code, regenerate workbooks, run application tests/SQL, install tools, activate skills or publish. Workbook reading/formula inspection is permitted; it does not prove rendered usability or recalculation. State missing visual/calculation/runtime proof explicitly.

Distribution resource base: the directory containing this `SKILL.md`. Shared policy and registry are bundled under `_kit/shared/`; registry paths resolve from this skill root. Invocation by skill name uses the separate installed entrypoint; no nested entrypoint is bundled.
