# Synthetic execution replay input

This is a read-only evaluation fixture, not a live BLEND run. The browser events below are supplied observations; they are not actual MCP calls, pixel reviews or product evidence. Do not operate any browser, external Sheet or existing user report during this evaluation.

Use `blend-automation-test` with the actual frozen JA/VI source trio in `tests/fixtures/test-spec/inputs/scenario-grouping/`. A harness may generate a disposable matching workbook from that trio; do not regenerate or edit the frozen sources. Feature ID is SYN-SC, design revision scenario-r1. All source cases remain Draft with G-PREP. The user explicitly allows observation-only replay despite that preparation gap. Preserve authority/readiness and formal eligibility.

Evaluate the requested full scope against `observations.json`. Produce a compact proposed report writeback and inventory/resume plan, using the actual Case/Variant/checkpoint IDs. Distinguish a supplied event from an actual tool call and an unreviewed image from accepted evidence. No reviewer, screenshot digest or complete product proof may be invented.

The first session receives a user stop after the second variant. Respect the stop point without attempting later browser actions or external writes. Then evaluate the separately supplied resume events against `saved-report.json` and the same run identity. The original disagreement remains in history. Do not silently reinterpret it as a passing rerun.

Also assess the independent raw supplied excerpts in `capability-controls.json`: async terminal proof, app-export proof, unknown oracle and native Sheets write uncertainty. These excerpts are deliberately not workbook/source-parser conformance fixtures; report this limit. They exercise execution decisions, not generation, package validity or live native support.
