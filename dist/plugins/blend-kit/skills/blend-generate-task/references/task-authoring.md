# Task artifact authoring

Read for selected TaskArtifacts after the shared contract. Templates are binding; this reference explains how to fill them without padding or turning implementation suggestions into requirements.

## Research to recipient documents

Use `research@1.1.0` at feature-root `research/<topic>.{ja,vi}.md` for new reports. Select a meaningful reusable question/flow; record topic, purpose/questions, exact verified feature/task/immediate parent, scope, source/code/confirmation dependency anchors and captured identities, currentness and gaps. Reuse a relevant topic only after checking its decisive dependencies and conclusions. No default whole-feature file, per-field quota, empty report or automatic folder/index scaffold. Follow the registry basename grammar; a Task ID prefix is allowed only when source-verified, preserving case/zeros. Task-specific reports stay here and are linked from task documents.

Selected snapshots pin actual per-file bytes and the dependencies supporting consumed clauses/questions, never a folder hash. Unrelated topic changes do not invalidate selected conclusions; changed relevant authority/code/confirmation or incorrect conclusions require a scoped delta, not a whole-feature rewrite. Frozen inputs remain immutable during consumption. Legacy flat `research@1.0.0` is readable with its original baseline/schema; preserve all old snapshots, raw fixtures, results and SQL/DDL without migration or repinning.

Research retains the clause/branch crosswalk, exact source anchors/authority/revision, relevant code content baseline, As-Is evidence and gaps. Trace entry → authorization/validation → inputs/settings/branches → save → readback → consumers/lifecycle; state unread seams rather than claiming completeness from filenames. Every material branch must become an owned outcome/AC or a classified gap. Canceled/superseded clauses remain history and cannot return as active work.

Split Tasks, AC and Q&A must make sense without Research/chat. Restate the affected function, actor, conditions, intended result and preserved state. Shared source links are useful; opaque clause IDs and research logs do not replace explanation. Only Split Technical needs verified `blend:<repo-relative-path>` or symbols with their role explained. Full traces stay in Research. No workstation paths, personal assignments, estimates, fabricated status or named approvers.

## Split Tasks

Split by usable outcomes, not controller/model/view files or a fixed backend/frontend count. Use the same concise outcome titles in summary and detail. Main Screen gives the verified name/path; Affected Screens excludes Main Screen and lists each other affected surface. In Vietnamese write `[Tên Việt（日本語）] - ` followed by the verified route in backticks; Japanese uses the exact source name. A genuine API/job/shared operation says “no direct screen” and identifies the actual seam/consumers. Unverified route stays explicitly unresolved.

Change scope identifies direct changes, necessary technical dependencies, regression-only checks and unresolved impact. A listed screen does not automatically assign a change. Business explains actions/results/decisive failures/preservation. Technical explains where → proposed change → relevant input/output → constraint/persistence/readback; equivalent implementations remain valid. Each actual change has one primary owner. Dependencies distinguish what can start now, a prerequisite to start and an integration prerequisite. Completion is one observable result, not a copied test suite.

Keep simple tasks short; expand only affected flows/constraints. No arbitrary field lengths, transaction model, table count, lock, enum or rule copied from an example feature. Open decisions name the affected operation and exact unblocker without blocking unrelated supported work.

## AC

Use business-flow/outcome groups and `- [ ] **AC-ID — Title:**` entries. The checklist stays unchecked: writing is not executed acceptance. Each item retains actor/conditions, observable outcome, decisive exception, preserved state and authority basis; common context may appear once beside the group with an explicit per-item reference. Inline conditional labels are sufficient; do not add a form/table per simple AC.

Combine repeated conditions and sibling outcomes of one review purpose only when failure remains visible. Split independently failing obligations. Stable IDs stay with unchanged meaning; never recycle deleted IDs. Keep a regrouping map in Research when needed. Detailed setup/action/evidence belongs in Test Spec, while essential acceptance stays in AC. Unknown oracle is named as awaiting decision beside known obligations, never guessed or hidden in an appendix.

## Business Q&A

Each independently answerable leaf has scenario/current facts, unresolved decision/problem, impact, viable options, a marked recommendation with reason/trade-off, confirmation requested and authority status. Related questions may share context but each leaf remains answerable and tracks its own answer/source. A sibling answer does not close the parent or other leaves. Existing settled answers are retained with authority; do not ask them again.

Use the customer-facing 1.1.0 presentation: answered and unanswered sections; concrete situation paragraphs; a three-column option/treatment/impact table when alternatives exist; bold Proposal and Confirmation paragraphs. Do not render the semantic fields as seven repeated bullet labels. Group related decisions under one question heading with bold numbered child headings; each child retains its own proposal and confirmation. Keep answered status faithful (provisional, confirmed or existing requirement), state a scoped none when there are no answers, and do not move proposed defaults into the answered section. Unanswered status comes from its section; repeat status only for a leaf with a different state.

If no product outcome can be recommended from evidence, propose the smallest investigation and selection criterion, not a fabricated default. Engineering choices and discoverable facts are researched/proposed, not sent to the customer as business-policy questions. If there are no open questions, use the template's no-open-questions alternative with the assessed scope; do not manufacture questions to fill the file.

## Conditional Database Design

Generate only when the task needs a changed storage/relationship/data-lifecycle design, not because code queries a database. Show evidenced As-Is vs proposed/confirmed To-Be, storage unit, identity, columns/type/NULL/default, relationships/cardinality/ownership/constraints, validation/write/readback/consumers and lifecycle. Include existing-data compatibility and verification. Mark unresolved schema facts and engineering choices where used; existing schema SQL is not observed target DB.

Indexes/performance, transaction/concurrency, copy/import/migration subsections are required only for affected obligations; omit them when genuinely unaffected, not when unknown. Preserve scope/year/owner/permission guards and meaningful NULL/zero states. Explain a necessary integrity constraint before prescribing its representation. No arbitrary sample-feature columns, status enums, locks or formulas. Generation writes design prose only; executable DDL has no mapped template here.

## Conditional SQL

For a concrete authorized question, draft `research/<topic>.sql` at the verified feature root using `sql-investigation@1.0.0`; follow the same meaningful topic/basename and verified-ID rules. Do not move old SQL/DDL. Identify exact population, counting unit, verified schema/joins, missing target checks, safe parameters and expected aggregate interpretation. Check cardinality, unmatched rows and aligned denominators; `DISTINCT` does not fix a wrong scope or JOIN. Do not replace unknown school/year with zero, wildcard or no filter.

Only read-only SELECT and necessary read-only schema inspection/plain EXPLAIN SELECT are permitted drafts. No DML/DDL, EXPLAIN ANALYZE, locking reads, session changes, temporary tables, output files or side-effect functions. Prefer aggregate counts to personal record dumps. Retain **DRAFT — NOT EXECUTED** and **NOT READY TO RUN** for missing inputs. A draft proves no counts, target schema, performance, migration safety or approval. Preparing it grants no execution permission.

## Completion checks

Load each exact template/version before authoring; preserve required localized H2 order and fields. Optional omissions follow the asset predicate. Remove instructional comments/placeholder values, retain only provenance marker and legitimate uncertainty. Compare JA/VI actor, negation, values/order, exceptions, preserved state, IDs and certainty, not just headings. Template compliance is separate from source correctness and execution proof. Keep output scope/revisions/history and unrelated changes intact.
