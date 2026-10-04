# Customer report from a closed run

The customer receives a standalone XLSX. The working Run/Cases/Data workbook and frozen Markdown retain internal provenance and execution history. This operation creates a separate requested-language `customer-test-report@1.0.0` copy; it does not execute tests, translate observations, edit an existing run or publish anything.

## Inputs and export

Resolve an interpreter with the skill's declared dependencies; do not install automatically. The [customer exporter](../scripts/customer_report.py) loads the [renderer](../scripts/render_customer_report.py) and the exact asset from its own location. Call:

```text
python scripts/customer_report.py --run-file MASTER.xlsx --design-dir DESIGN --output customer-test-report.ja.xlsx --language ja --delivery-stdin
```

`MASTER.xlsx` and `DESIGN` stand for caller-resolved paths. Relative paths resolve from the process cwd; use resolved paths after bounded discovery. Requested language is explicit `ja` or `vi`; the matching design files must already be fingerprint-bound to that run. Use a new output path; an existing path is preserved and rejected. The original `export_report.py` CLI and internal v1 templates remain unchanged.

Pass exactly one JSON object through structured stdin with keys `closure_confirmation`, `evidence_access`, `screenshots`. This is transient input, not a saved manifest; use the runtime's argument array/stdin facility, never concatenate untrusted text into shell code.

| Key | Required record fields |
| --- | --- |
| `closure_confirmation` | `closed_by`, timezone-bearing ISO `closed_at`, `source`, exact recipient `audience` |
| `evidence_access` | List of `url`, exact `audience`, `verified_by`, timezone-bearing ISO `verified_at`, `method`, `source`; method is `human-attestation` or `recipient-session` |
| `screenshots` | List of `case_id`, `variant`, transient `path`, `caption`, `reviewed_by`, timezone-bearing ISO `reviewed_at`, `source` |

Supply actual confirmations, not generated attestations. Evidence access must match the intended customer audience and every published evidence/bug URL. An agent being authenticated is insufficient. Missing access verification blocks delivery; no upload, permission change or link fetching follows. Empty screenshot lists are permitted when no important defect needs an image; important defect images require an actual reviewed source and caption bound to the correct Case/Variant. Pillow is used only for image handling; no automatic dependency installation.

The master must carry recorded Run ID, build/environment/scope and valid per-variant observations. Preserve NOT RUN, FAIL, BLOCKED and SKIPPED, visible reasons, open defects and untested scope; closed does not mean all passed. Empty unexecuted designs and incomplete critical metadata cannot become completed reports. The exporter verifies frozen design fingerprints and projection before resolving context, steps and variants. Never reverse-parse the internal pipe-joined display strings or copy old results onto changed expected.

## Reader path and template contract

- Summary: run/build/environment/period, scope/exclusions, a bounded conclusion, case and variant totals/rates, limitations and outstanding work. A zero denominator is no data, not 100%.
- Results: exactly seven columns — TC/Variant; screen/function; conditions/actions; expected; actual; status; evidence/bug. Keep actor, decisive input, expected and preserved state understandable without another file.
- Details: generated only when material structured steps/content or reviewed images need space. The owning result links to it; do not truncate, shrink text or remove conditions to keep two sheets. The source asset stores this conditional layout, but simple output has no blank or hidden Details tab.

Use the exact JA/VI assets registered as `customer-test-report@1.0.0`. Status literals and stable identities remain unchanged. Do not add an internal Data/setup/research tab or readiness/hash/traceability columns. Customer text is an allowlisted projection; closure/access receipts, private locators and source fingerprints never become customer content. Intentional dummy test input is not a workstation locator to delete blindly.

## Validation and handoff

Reconcile every Case/Variant, exact expected/actual/status, case aggregation and denominator against the recorded master/frozen design. Inspect the entire saved XLSX package, including properties, comments, hidden content, relationships and media. Review important screenshots for visible private details before providing them; metadata stripping cannot sanitize image pixels. Render all used sheets at readable zoom and verify navigation, overflow, contrast and formulas in an available engine. Native Excel/accessibility and actual recipient-access checks are distinct evidence; disclose what was unavailable.

Report the actual new output, requested language, matching basis, preserved master, checks and unresolved delivery gaps. Synthetic fixtures, export success and source/package checks are not application test execution, customer-access verification or feature-wide coverage. No app tests/SQL, source edits, active skill cutover, external publication or release is authorized by this operation.
