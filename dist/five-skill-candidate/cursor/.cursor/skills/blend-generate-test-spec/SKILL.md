---
name: blend-generate-test-spec
description: Generate or refresh BLEND test specifications and a same-revision execution workbook from a feature specification and verified context/code, standalone or from Generate Task research. Designs tests; does not execute them.
---

# Blend Generate Test Spec

Read [shared workflow](_kit/shared/workflow.md) and [template registry](_kit/shared/artifact-formats.md). They govern discovery, identity, source authority, language, ownership and permission boundaries. Use the resolved BLEND checkouts; never assume the author's workstation layout.

## Intake and research

Choose `design` for source-backed coverage with visible gaps, `finalize` to verify concrete preparation/entry/observation seams against the supplied implementation, or `refresh` for affected clauses/cases and their immediate dependents. None executes tests. Honor requested language/file subsets; defaults are JA–VI Markdown and one VI workbook under the existing meaningful `test-spec` destination/revision.

- **Standalone:** discover allowed context/application roots; read current source, confirmations and affected code flows. No Task/AC/Research files are prerequisites. External technical/test-method research is allowed within source restrictions. Record compact research basis, code/working-content identity and limitations in `scope-and-approach`. Create separate topic reports only when the user explicitly requests extra Research, using the registered `research@1.1.0` templates at verified feature-root `research/<topic>.{ja,vi}.md`; otherwise the compact basis suffices.
- **Invoked:** consume the exact eight-field ResearchHandoff. Check identity, authority, allowed sources, selected actual topic paths/captured byte identities and decisive source/code/confirmation dependency identities for consumed questions/clauses. Reuse valid conclusions without loading every topic or computing a folder digest. Unrelated topic additions/edits do not invalidate the selected basis. For relevant drift, wrong conclusions or missing decisive evidence, research the affected area and record a scoped delta in `scope-and-approach`; keep affected work Draft and never silently edit frozen caller Research or inherit an unsupported oracle. Legacy flat `research@1.0.0` inputs remain readable at their original schema/baseline without rewriting/repinning. Task/AC links are supplemental, not authority.

Read [coverage guidance](references/test-coverage.md) before deriving cases. Decompose active clauses into independently failing obligations/branches; map each to a case/variant or classified gap. Inspect actual handlers/consumers and preservation/lifecycle risks. A plausible wrong implementation must fail a specific written action/assertion. Missing fixtures do not remove obligations; unknown business oracles stay gaps, not invented expectations.

## Generate only requested artifacts

Load each exact registered asset before authoring. Use its marker/version, required headings, field/order and omission predicates. Missing mappings/templates block that output. Keep IDs and historical languages; do not overwrite without an update request.

| Artifact | Template / purpose |
| --- | --- |
| scope-and-approach | `assets/scope-and-approach-template.{ja,vi}.md`: baseline/research, scope, preparation, evidence, clause/branch coverage and gaps |
| test-cases | `assets/test-cases-template.{ja,vi}.md`: business-flow groups; compact cases, expanded steps and independently reportable variants |
| test-data | `assets/test-data-template.{ja,vi}.md`: shared fixture create/verify/reset and decisive values |
| test-case-report.xlsx | `assets/test-case-report-template.xlsx`: Run/Cases/Data projection of VI design Markdown; no second editable design source |

Use explicit shared-context references with local overrides to avoid boilerplate while preserving feature/function, configuration, trigger, observation, actor/permission and state. Group main path → variants/boundaries → validation/permission → recovery. Priority selects run order with dependencies/readiness; it does not reorder the design into all High cases first. No hidden previous-case state chains. Keep expected basis, readiness and actual execution independent.

## Workbook

Read the export syntax in [coverage guidance](references/test-coverage.md#export-interface). Resolve a Python interpreter with the already available dependency in `requirements.txt`; never install it automatically. Run:

```text
python scripts/export_report.py --source-dir <test-spec-folder> --output <new-report-path.xlsx>
```

Only the default bundled template is resolved relative to the script. Relative CLI values for `--source-dir`, `--output` and explicit `--template` resolve from the process working directory; prefer resolved absolute input/output paths. Export loads the XLSX asset, validates Markdown schema/revision/references, records fingerprints of the exact captured source/template bytes and refuses **any** existing output path. New run rows are NOT RUN with no invented tester/date/actual/evidence. Executed history stays with its original revision/build; changed expected gets a new requested revision/path. The shipped asset supports VI only: requested JA workbook is a visible unsupported-capability gap, never silently delivered as VI. Requested Markdown-only subsets remain valid.

## Reconcile and deliver

Check each generated file against its template, reverse-map expectations to authority, compare JA/VI IDs/conditions/values/negation/gaps and verify workbook projection across every case/variant/fixture. Render and recalculate workbook in an available spreadsheet engine separately; successful export/formula text is only structural proof. Disclose unavailable runtime/render/recalculation evidence.

Return BranchResult: actual paths, basis used, completed/incomplete scope, gaps/deltas and status. Full Test Spec requires the workbook; unavailable export is an incomplete branch. Separate topic reports require the explicit extra-Research request above; no auxiliary manifests/JSON/CSV, app/SQL tests, activation, commit, push or publication follows.

Distribution resource base: the directory containing this `SKILL.md`. Shared policy and registry are bundled under `_kit/shared/`; registry paths resolve from this skill root. Invocation by skill name uses the separate installed entrypoint; no nested entrypoint is bundled.
