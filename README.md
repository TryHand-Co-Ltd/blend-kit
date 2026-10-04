# BLEND Kit

BLEND Kit packages five reusable workflows for BLEND delivery: task generation, test specification, artifact review, implementation planning, and code review.

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

The repository includes `.cursor-plugin/marketplace.json` and a portable Agent Plugin manifest, so Cursor loads the same five skills from the generated package.

## Included skills

| Skill | Purpose |
| --- | --- |
| `blend-generate-task` | Generate BLEND task breakdowns and acceptance artifacts. |
| `blend-generate-test-spec` | Generate or refresh Test Specs and editable JA/VI reports. |
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

Current package:

- Plugin: `blend-kit@tryhand-blend-kit`
- Version: `1.0.0`
- Skills: `5`
- Files: `207`
- Tree digest: `84f6d975077b7654ac4e77d0490644bc068be97a1270d470f66c0cd100c9eeae`

See [workflow rules](shared/workflow.md), [artifact formats](shared/artifact-formats.md), and [package maintenance](docs/package-reference.vi.md) for implementation details.
