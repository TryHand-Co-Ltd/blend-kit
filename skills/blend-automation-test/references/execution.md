# Execution of a frozen Test Spec

Read [the shared automation contract](../../../shared/automation-testing.md). This reference executes the supplied design; changing case grouping, steps, fixtures or Expected belongs to a separately requested generator refresh. Keep source bytes/revision, authority and report history intact.

## Inventory and prerequisites

Resolve feature identity from the user's verified source and applicable feature README/CONTEXT, not folder-title resemblance. Record target/build/environment, source revision/content identity, report identity, allowed roles/actions and requested scope. The local [run ledger](output.md) contains every requested Case/Variant and its checkpoints before execution. It is a progress ledger, not a second report.

Use the actual parser/report bindings for the supplied versions. Use report2.5 with current1.3 or supported read-only older source grammar. Preserve source IDs/oracles and meaningful checkpoints. Sources without checkpoint IDs use run-local capture labels tied to exact existing assertions/anchors; these labels do not alter design or counts. Older saved workbook formats are rejected without mutation. If a legacy field lacks verified identity/route, ground that fact from supplied context or retain the exact gap. Older unknown paths do not prove that the page is unavailable.

Separate prerequisite availability from readiness metadata. An attempted auth/role/fixture/source/tool check supplies an actual blocker reason; the word Draft or a previous run's blocker alone does not. Follow fixture create/verify/reset instructions through the permitted UI. If preparation needs DB writes or unsupported fault injection, record the affected execution/proof gap and continue independent cases; test permission alone does not grant those actions. Check non-Browser lanes with the specifically authorized proof source, rather than forcing screenshots to certify DB/security/performance behavior.

Full requested scope includes every variant, including known gaps. Record each as attempted, completed, pending or untouched in the ledger, while keeping report status tokens unchanged. Select run order by prerequisite independence and requested priorities. Browser/session and report have one writer; do not run shared mutable fixtures concurrently by default.

## Per-variant flow

1. Read the overall Expected and variant's Inputs, action delta, concrete final Expected, required checkpoints, preservation and one Reset. Verify the starting state now, including actor, identifiers, settings and fixture values. Create/reset independently; a passing earlier case is not a preparation step unless the design explicitly defines that dependency. Checkpoints select meaningful capture/inspection/export milestones; there is no automatic two-image or every-click quota.
2. Snapshot, then perform one ref-based action. Condition-wait for the expected observation using available MCP tools; inspect returned snapshots before further interactions. Keep user-created text meaningful English, with exact UI labels and required negative/security payloads preserved.
3. Record the actual value/state and matching checkpoint identity, including evidence needed to exclude another explanation. For cross-page consistency, keep the same stable record ID and capture both pages when required. A setting saved successfully does not prove its downstream output changed.
4. Capture reviewed pairs through [MCP evidence](mcp-evidence.md). Default to the necessary viewport (`full_page=false`); use full-page only when the assertion needs the whole layout and record that reason. An assertion may require several views; collect them under its existing checkpoint and meaningful stage/scroll-state note. Keep scope/state unchanged within each raw/annotated pair. Use separate defined checkpoints for distinct proof types.
5. Evaluate every mandatory assertion, preservation condition and artifact. Record a concrete reason/next check when any cannot be established. Write the variant to its authoritative report through [writeback](report-writeback.md) after evidence acceptance.
6. Execute the actual reset/final action and verify the restored state. Log completed cleanup or its specific failure. Annotation cleanup is separate from fixture reset. If reset fails, reassess which later cases depend on that state; continue demonstrably independent cases instead of blanket blocking the suite.

## Result semantics

Use canonical tokens only as writer inputs; the writer/report's existing locale maps them to saved dropdown strings. Never add a new execution state to the workbook. Expected basis and readiness stay as frozen metadata.

| Canonical token | Observed justification |
| --- | --- |
| PASS | Every required assertion is observed against a known oracle, with required reviewed screenshot/export/inspection proof. Recorded counts reflect the saved status; source/readiness/Actual/evidence checks separately determine proof quality and never silently change that status. |
| FAIL | An exercised application behavior contradicts a known oracle, with the failing action/state and evidence identified. A capture/ref/annotation/layout failure alone is not product FAIL. |
| BLOCKED | An attempted prerequisite or operation demonstrates a dependency preventing completion. Actual identifies the attempt, observed reason and next check; do not apply this to untouched variants. |
| SKIPPED | A deliberate omission permitted by requested scope/design or an actual unavailable safe preparation/proof seam is explained. Missing mandatory proof never becomes optional coverage. |
| NOT RUN | The variant was not exercised, or interruption left it without a valid conclusion. Preserve partial observations in the ledger/Actual as appropriate; never overwrite an existing concluded result automatically. |

For user-authorized observations on Draft/Proposed inputs, identify observed agreement/disagreement and proof limits without changing metadata or claiming eligible formal PASS/FAIL. Unknown Expected stays an oracle gap; do not infer PASS from attractive UI or modify Expected to match Actual. Numeric counts do not certify evidence completeness, authority or release.

## Async and exported results

Before waiting, identify the job/record key, required terminal state and wait budget from the frozen TC or observed application contract. Capture queued/processing when relevant and the terminal result. Queued/HTTP 200 is not terminal success. Use condition-based bounded waits and record last state/elapsed time/source of budget; an unsupported source or unavailable dependency is a proof gap. Do not invent a short timeout or increase a global timeout to hide uncertainty.

For exports, capture the actual trigger and visible result, then retrieve and inspect the real app-generated artifact only through available, authorized tools. Verify exact identity, format and the TC's content assertions; archive bytes under exports. Network metadata proves only that metadata. If the MCP cannot expose the download, record the successful browser action plus missing artifact proof; no complete PASS for an export checkpoint. Browser-printed PDFs are not app exports.

## Failure, interruption and resume

A failure does not cancel the next independent case. Attempt its own preconditions and reset rather than inheriting the prior outcome. Retry product actions only when requested rerun scope permits; retain the original failure and note any differing later observation. Evidence correction alone is bounded by the capture protocol and does not rerun the product suite.

On unexpected tool/app errors, retain last observed state, checkpoint, time, any pending writeback and cleanup status. Stop dependent actions if state/ownership is uncertain, then continue supported independent work. Do not auto-fix code, seed fixtures, install tools or restart/change the MCP to force completion.

When the user stops, cease browser actions and external report updates promptly. Locally record the resume point and incomplete cleanup; do not mark remaining rows BLOCKED/SKIPPED or synthesize results. Resume only after a user resume request. Reread design/report/ledger, verify revision/feature/report/run identities and compare actual current fixture/session state. Reconcile a pending or unknown report write by readback before retrying, rebuild required preparation independently and retain already concluded results. Explicit reruns append truthful history rather than silently replacing previous failure evidence.
