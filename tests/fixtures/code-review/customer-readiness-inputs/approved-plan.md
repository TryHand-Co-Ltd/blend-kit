# PLAN-3 — approved synthetic implementation scope

For SYN-RV-03-A (parent SYN-RV-03), add the method storage column, accept and save a valid method selection with the offset, return it in existing readback and the new raw route, and preserve school/year checks. Keep previous NULL selections and offsets intact. Adjust model read handling for an empty identifier while respecting AC-4.

Expected surfaces: Record controller, Record model, routes and one migration. Compare the supplied base and current snapshots cumulatively. They are synthetic byte snapshots, not actual commits. No unrelated feature behavior is assigned. Authorization, method storage/readback, preservation and applicable column/method standards are required acceptance conditions. No execution, rollout or external-system permission is conveyed by this plan.
