---
name: blend-review-code
description: Review actual BLEND implementation against an approved plan, AC and current context, including every assigned change, bounded shared consumers and conditional DB risks. Preserve finding IDs and separate acceptance from behavioral validity and runtime proof; read-only except a requested report.
---

# Blend Review Code

Use after implementation for an assigned diff/range/worktree, with approved plan/AC/current authority as intended scope. Artifact-only review belongs to `blend-review-artifacts`; this skill does not generate prerequisites or execute a plan.

## Basis and scope

Read [shared workflow](_kit/shared/workflow.md), [template registry](_kit/shared/artifact-formats.md), [common review policy](_kit/shared/review-policy.md), [pinned behavioral protocol](_kit/shared/bug-hunter.md) and its [MIT license](_kit/shared/bug-hunter-LICENSE.txt), then [code review procedure](references/code-review.md). Resolve workspace, context, application Git root and package separately; read applicable project/development rules before source inspection.

Keep the shared textual **ReviewBasis** inline. Verify exact feature/task/source/parent, current CONTEXT/confirmations, approved plan/AC/review revisions, selected topic/dependency identities and prior IDs. Source approval, plan approval, review verdict and execution permission are separate facts. Missing authority/baseline/access stays visible; do not infer approval or rewrite requirements to fit code.

Pin actual base/head or verified merge-base, included commits and staged/unstaged/relevant untracked/renamed/deleted byte identities. Separate intended business scope, expected plan surfaces, actual diff inventory and allowed impact inspection. A plan file list is not diff evidence; never assume `HEAD~1` or fetch/stash/reset/checkout for convenience.

## Review and deliver

Read every assigned hunk and decisive surrounding code, then named, bounded risk-driven callers/consumers and dynamic CodeIgniter wiring. Inventory actual inspection method, state and limits per file/path; unread material scope means Partial/Needs evidence. Follow the reference for independent Spec / Tests / Standards checks, shared-flow correctness and conditional DB/migration checks.

For behavioral candidates use the **common** Hunter → Skeptic → Referee protocol: actual distinct native agents sequentially by dependency when available/authorized, otherwise disclosed local sequential passes with `independent: false`. Record actual role identities and all eleven inline RoleDisposition fields. Missing/empty/malformed required role outputs are UNREVIEWED, never a clean zero-candidate scan. Documentary/AC/test/standards defects remain actionable independently of behavioral validity.

Report scope/origin/severity/confidence/completion effect independently under common policy. Missing supplied proof remains UNKNOWN origin without an equivalent inspected historical evidence baseline; scope follows assigned source/AC obligations, independent of proof owner/oracle. An old line can become newly reachable; OUT_OF_SCOPE never excuses an introduced/worsened regression. Low mandatory AC mismatch can block task acceptance. Preserve prior IDs and evidence-backed closure on re-review.

Load the exact [VI template](assets/code-review-template.vi.md) or [JA template](assets/code-review-template.ja.md) from the registry before output. Default to chat in the same family; files only when requested, routed to verified feature docs/task ownership. Unsupported language/missing mapping blocks that output. Keep all seven H2 sections with scoped none statements; omit only template-authorized conditional H3 detail. Findings name actual line/revision, trigger, expected/actual, impact, counter-evidence, precise update/preservation/verification and proof limits. Apply the common final cross-reference/root-atomicity check.

Before handoff, run the shared [registered Markdown gate](_kit/shared/artifact-formats.md#deterministic-handoff-gate) on each final saved requested output using its exact type/language/logical filename. Follow the asset's exact labels and inline or block/list presentation; an inline slot needs a concise nonempty summary on the same line, with details below when useful. Authoring instructions/placeholders/fences cannot fill it. Preserve genuine template-authorized no-findings/none and conditional cases. Failed/unavailable gate leaves affected outputs Draft/Blocked and the branch incomplete; report the mismatch/capability, never Complete. Chat-only reviews apply the same fields without creating an unrequested file and disclose that the file gate was not run. Workbook parity/render/recalculation and semantic/source/approval checks remain separate.

Capture final selected topics, decisive dependencies and approval/review inputs with the shared read-only `capture` command against each verified root. Compare actual stdout SHA256 receipts to approved/frozen identities; never report an expected supplied hash as an observed capture. Preserve inputs while consumed; unavailable capture is an explicit identity gap, not a matching-byte claim. Keep portable paths in shared outputs and actual roots only in transient intake.

Keep assigned acceptance, regression, standards, DB risk and runtime/QA/release proof as separate verdicts. Code/static/fixture proof does not prove DB contents, executed behavior or release readiness. Review is read-only except its requested report: no Fixer, source fixes, application test execution, SQL/live DB reads, production setup, install/configuration, publication or release.

Distribution resource base: the directory containing this `SKILL.md`. Shared policy and registry are bundled under `_kit/shared/`; registry paths resolve from this skill root. Invocation by skill name uses the separate installed entrypoint; no nested entrypoint is bundled.
