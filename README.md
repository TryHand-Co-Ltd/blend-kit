# BLEND Kit

BLEND Kit packages six reusable workflows for BLEND delivery: task generation, test specification, automation testing, artifact review, implementation planning, and code review.

The private repository is a marketplace named `tryhand-blend-kit`. The install ID is `blend-kit@tryhand-blend-kit`.

## Install

Repository access is required because the marketplace is private.

### Codex

```powershell
codex plugin marketplace add git@github.com:TryHand-Co-Ltd/blend-kit.git
codex plugin add blend-kit@tryhand-blend-kit
codex plugin list --json
```

Restart Codex or open a new session after installation.

### Claude Code

```powershell
claude plugin marketplace add git@github.com:TryHand-Co-Ltd/blend-kit.git
claude plugin install blend-kit@tryhand-blend-kit
claude plugin list
```

Restart the Claude Code session after installation. Skills are invoked with the plugin prefix, for example `/blend-kit:blend-review-code`.

### Cursor

Open **Customize → Plugins → From GitHub Repository**, select `TryHand-Co-Ltd/blend-kit`, then install **BLEND Kit**. Teams and Enterprise organizations can add the same private repository as a Team Marketplace.

The repository includes `.cursor-plugin/marketplace.json` and a portable Agent Plugin manifest, so Cursor loads the same six skills from the generated package.

## Included skills

| Skill | Purpose |
| --- | --- |
| `blend-generate-task` | Generate BLEND task breakdowns and acceptance artifacts. |
| `blend-generate-test-spec` | Generate or refresh Test Specs and editable JA/VI reports. |
| `blend-automation-test` | Execute provided Test Cases with the available Playwright MCP, review appropriately scoped annotated image evidence, and update one XLSX or Google Sheets report. |
| `blend-review-artifacts` | Review task and Test Spec artifacts against source requirements. |
| `blend-plan-implementation` | Create an implementation plan from approved scope. |
| `blend-review-code` | Review scoped code changes against requirements and project rules. |

## Update

### Codex

```powershell
codex plugin marketplace upgrade tryhand-blend-kit
codex plugin remove blend-kit@tryhand-blend-kit
codex plugin add blend-kit@tryhand-blend-kit
```

For Claude Code or Cursor, refresh the marketplace and reinstall/update the plugin from that client, then start a new session.

## Build and validate

```powershell
pwsh -File scripts/build-plugin-package.ps1 -Python python
pwsh -File scripts/check-plugin-package.ps1
python tests/test_kit.py --area all
```

The generated package is stored at `dist/plugins/blend-kit`.

For a customer-facing report, use Generate Test Spec's default report (`test-report@2.4.0`). The same workbook supports testing and customer review: self-contained conditions/actions/branch-specific outcomes and independent result rows. Human descriptions precede variant codes. Only images expand, in one initially collapsed group per TC; descriptive titles sit above vertically stacked images, without evidence URL inputs. No default technical appendix, preparation label or review notes; internal readiness/oracle/provenance safeguards remain. Older workbook formats are rejected without rewriting; no migration helper is shipped. XLSX-to-Google-Sheets conversion after testing needs native readback and viewing checks before sharing.

Current authored source uses `test-cases@1.3.0` and the only report layout is `test-report@2.4.0`, from the root JA/VI asset pair. Supported source1.0..1.2 remains readable with original IDs, literals, oracles and gaps; this does not retain old workbook templates or dispatch. Actual/Status stay with their TC, and unused image reserve rows are fully hidden. Browser evidence defaults to 1920×1080 and screenshots default to `full_page=false`, with full page only when needed. Short English observed notes sit top-right without covering UI; minimal highlights do not overlap/touch, and actual pixels are reviewed.

The automation skill selects one authoritative report per run and archives files by verified feature and Run ID under `blend-context/local/test-output/`. It does not upgrade Playwright MCP, redesign TC during execution, seed databases, modify the application, migrate existing reports, install skills or publish as part of a test run. Native Sheets needs actual connector/UI capabilities and separate readback/image verification, including grouping and image layout; XLSX/package checks do not certify those behaviors. The RC-001 report is a blank handoff for a separately authorized automation run; cleanup does not execute tests.

The previously verified package snapshot (before this source change):

- Plugin: `blend-kit@tryhand-blend-kit`
- Version: `1.0.0`
- Skills: `5`
- Files: `207`
- Tree digest: `84f6d975077b7654ac4e77d0490644bc068be97a1270d470f66c0cd100c9eeae`

See [workflow rules](shared/workflow.md), [artifact formats](shared/artifact-formats.md), and [package maintenance](docs/package-reference.vi.md) for implementation details.
