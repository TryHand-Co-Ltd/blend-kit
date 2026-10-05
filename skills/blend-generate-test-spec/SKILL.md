---
name: blend-generate-test-spec
description: Generate or refresh BLEND test specifications and one editable test report from a feature specification and verified context/code, standalone or from Generate Task research. Check recorded results in the same workbook without rewriting it. Does not execute tests.
---

# Blend Generate Test Spec

Read [shared workflow](../../shared/workflow.md) and [template registry](../../shared/artifact-formats.md). They govern discovery, identity, source authority, language, ownership and permission boundaries. Use the resolved BLEND checkouts; never assume the author's workstation layout.

Read the [scenario testing contract](../../shared/automation-testing.md) for current source1.3 and the sole report2.4. Supported older sources remain read-only inputs; older workbook formats are rejected without rewrite or migration.

For a report that will be shared with customers, use the registered `test-report@2.4.0` default layout. This is the same authoritative execution workbook, not a second customer result copy. Each TC must be understandable without opening its Markdown source: concrete context/data, actions, overall final outcome, independent variant results and evidence navigation. Use human descriptions before stable variant codes, e.g. Nhỏ hơn (lt), Nhỏ hơn hoặc bằng (le), Hủy xóa (cancel), Đồng ý xóa (delete). Keep enough conditions/data/actions to run and assess the case; no blanket shortening. Show specific blocked/unknown-oracle impacts without a Chuẩn bị/readiness label. Exactly two sheets; no review/sample notes or default technical appendix. Only evidence collapses: one group per TC, initially collapsed; each image has a descriptive title above it and is vertically stacked, with no URL requirement. Empty evidence is one Chưa có ảnh/画像なし line. Do not equate an existing recorded PASS with acceptance when its preparation/oracle is unresolved.

Supported older testcase sources, including RC-0011.1, project directly to current report2.4 without rewriting source grammar or inventing action deltas/checkpoints. Preserve IDs, assertions and literal values; new reports start blank and never transfer old PASS or evidence. Older saved workbook formats are rejected without mutation; no migration command is shipped.

## Intake and research

For an existing report, check the same workbook using [report guidance](references/test-report.md); do not regenerate it or create a second report. For test design choose `design` for source-backed coverage with visible gaps, `finalize` to verify concrete preparation/entry/observation seams against the supplied implementation, or `refresh` for affected clauses/cases and their immediate dependents. None executes tests. Honor requested language/file subsets; defaults are JA–VI Markdown and one VI workbook under the existing meaningful `test-spec` destination/revision.

- **Standalone:** discover allowed context/application roots; read current source, confirmations and affected code flows. No Task/AC/Research files are prerequisites. External technical/test-method research is allowed within source restrictions. Record compact research basis, code/working-content identity and limitations in `scope-and-approach`. Create separate topic reports only when the user explicitly requests extra Research, using the registered `research@1.1.0` templates at verified feature-root `research/<topic>.{ja,vi}.md`; otherwise the compact basis suffices.
- **Invoked:** consume the exact eight-field ResearchHandoff. Check identity, authority, allowed sources, selected actual topic paths/captured byte identities and decisive source/code/confirmation dependency identities for consumed questions/clauses. Reuse valid conclusions without loading every topic or computing a folder digest. Unrelated topic additions/edits do not invalidate the selected basis. For relevant drift, wrong conclusions or missing decisive evidence, research the affected area and record a scoped delta in `scope-and-approach`; keep affected work Draft and never silently edit frozen caller Research or inherit an unsupported oracle. Legacy flat `research@1.0.0` inputs remain readable at their original schema/baseline without rewriting/repinning. Task/AC links are supplemental, not authority.

Read [coverage guidance](references/test-coverage.md) before deriving cases. Decompose active clauses into independently failing obligations/branches; map each to a case/variant or classified gap. Inspect actual handlers/consumers and preservation/lifecycle risks. A plausible wrong implementation must fail a specific written action/assertion. Missing fixtures do not remove obligations; unknown business oracles stay gaps, not invented expectations.

## Generate only requested artifacts

Load each exact registered asset before authoring. Use its marker/version, required headings, field/order and omission predicates. Missing mappings/templates block that output. Keep IDs and historical languages; do not overwrite without an update request.

| Artifact | Template / purpose |
| --- | --- |
| scope-and-approach | `assets/scope-and-approach-template.{ja,vi}.md`: baseline/research, scope, preparation, evidence, clause/branch coverage and gaps |
| test-cases | `assets/test-cases-template.{ja,vi}.md`: one objective per scenario, shared steps, independently reportable variants and concrete checkpoint oracles |
| test-data | `assets/test-data-template.{ja,vi}.md`: shared fixture create/verify/reset and decisive values |
| test-report.{ja,vi}.xlsx | `assets/test-report-block-template.{ja,vi}.xlsx`: exactly two sheets, full TC blocks and blank result/image areas; VI by default |

Use explicit shared-context references with local overrides to avoid boilerplate while preserving feature/function, configuration, trigger, observation, actor/permission and state. Group main path → variants/boundaries → validation/permission → recovery. Priority selects run order with dependencies/readiness; it does not reorder the design into all High cases first. No hidden previous-case state chains. Keep expected basis, readiness and actual execution independent.

Absorb tiny UI/persistence checks into the checkpoint that proves the same objective. Group only compatible actor, fixture, trigger, reset and oracle families; retain independently failing permission, lifecycle, source, writer and output-format branches as explicit variants or separate scenarios. Write shared preparation once and require independent create/verify/reset for every variant. There is no target case count. On an authorized grouping refresh, map every old Case/Variant and obligation to the new Case/Variant/Checkpoint or classified gap in scope Coverage before removing an independent case; record disposition and reduction rationale. Old PASS/images do not transfer automatically.

New cases require Steps, Variants (including `base`) and Checkpoints. Case Expected is one concrete overall outcome. Steps have only Step/Action; final variant Expected is concrete for that branch. Write one Reset and reference shared fixture details; never copy another branch outcome or repeat Expected/preservation per step. Define checkpoint stage, exact observable focus and screenshot/export/inspection artifact, only at meaningful before/setup/result/after/export proof milestones; no setup/result or every-click quota. Core criteria/Actual/Status and material conditions stay visible. Identity, readiness, authority, fixture setup/reset and checkpoint provenance remain internal; include only technical detail needed to execute, understand or verify beside its related content. Removing reader prose never removes eligibility or DB/API/export proof. Group same-procedure data variants in a table; display different procedures/initial states as separately understandable situations. Scope records execution lane and proof limits; DB, security, performance and fault-injection obligations are not forced into screenshot-only Browser cases. Generator authors a staged evidence plan, never observations, image paths or review attestations. `blend-automation-test` executes that frozen plan; a test-execution request does not authorize redesign, DB seeding, application fixes, installation or publication.

## Workbook

Read the export syntax in [coverage guidance](references/test-coverage.md#export-interface). Resolve a Python interpreter with the already available dependency in `requirements.txt`; never install it automatically. Run:

```text
python scripts/export_report.py --source-dir <test-spec-folder> --output <new-report-path.xlsx>
```

Use `--language ja` for an explicitly requested JA workbook; the default is VI. Outputs use the registered `test-report.{ja,vi}.xlsx` family. The template resolves from the script location; relative CLI paths resolve from the process working directory. Export validates the matching Markdown schema/revision/references and refuses any existing output path. Projection strips a source list marker before adding one bullet, displays inline technical code as `[identifier]` while preserving literal characters inside it, removes Markdown bold markers outside code, and keeps status dropdowns compact and unmerged. New rows are NOT RUN with blank actual/evidence and no invented tester/date. QA enters results in this same workbook; its formulas update the summary. A new run or changed expected uses a separately requested new path. Missing requested-language assets or matching source is a Blocked gap, never a silent language substitution. Requested Markdown-only subsets remain valid.

## Check the same report

Use [report guidance](references/test-report.md) for entry fields, read-only checking and genuine completion/image/access attestations. `check_report.py --report REPORT.xlsx --source-dir DESIGN --language vi --phase in-progress` reports current gaps without saving the workbook. Use `--phase complete` with actual typed attestations through stdin to assess completion. Missing actual results, reasons, route/image review or access prevents a complete conclusion; update the same workbook with authorized inputs. Presentation readiness never means execution is complete. Older source grammars remain read-only inputs; older workbook formats are unsupported.

## Reconcile and deliver

Check each generated file against its template, reverse-map expectations to authority, compare JA/VI IDs/conditions/values/negation/gaps and verify workbook projection across every case/variant/fixture. Render and recalculate workbook in an available spreadsheet engine separately; successful export/formula text is only structural proof. Disclose unavailable runtime/render/recalculation evidence.

Before handoff, run the shared [registered Markdown gate](../../shared/artifact-formats.md#deterministic-handoff-gate) on each final saved requested output using its exact type/language/logical filename. Follow the asset's exact labels and inline or block/list presentation; an inline slot needs a concise nonempty summary on the same line, with details below when useful. Authoring instructions/placeholders/fences cannot fill it. Preserve genuine template-authorized no-findings/none and conditional cases. Failed/unavailable gate leaves affected outputs Draft/Blocked and the branch incomplete; report the mismatch/capability, never Complete. Chat-only reviews apply the same fields without creating an unrequested file and disclose that the file gate was not run. Workbook parity/render/recalculation and semantic/source/approval checks remain separate.

Capture final selected topics, decisive dependencies and approval/review inputs with the shared read-only `capture` command against each verified root. Compare actual stdout SHA256 receipts to approved/frozen identities; never report an expected supplied hash as an observed capture. Preserve inputs while consumed; unavailable capture is an explicit identity gap, not a matching-byte claim. Keep portable paths in shared outputs and actual roots only in transient intake.

Return BranchResult: actual paths, basis used, completed/incomplete scope, gaps/deltas and status. Full design Test Spec requires the unified workbook; unavailable generation is an incomplete branch. Checking returns findings and evidence limits for the same file without regenerating design or report. Separate topic reports require the explicit extra-Research request above; no auxiliary manifests/JSON/CSV, app/SQL tests, activation, commit, push or publication follows.
