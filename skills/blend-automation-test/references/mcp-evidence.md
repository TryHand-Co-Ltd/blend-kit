# Focused MCP evidence

Read [the shared contract](../../../shared/automation-testing.md) before this capture protocol. Use the project's currently callable Playwright MCP tools; do not upgrade, patch, configure or replace its server. Discover schemas on each runtime: a documented tool is not proof that it is callable here.

## Capability boundary

The verified MCP exposes `browser_resize(width,height)`, `browser_snapshot()`, `browser_evaluate(expression)` and `browser_take_screenshot(full_page,highlight_refs,highlight_mode)`. Its screenshot API has no filename, output-folder, note, crop or custom-color/stroke arguments. It has no dedicated trace/video/download-path tool. If a capability is absent, record the affected proof gap; do not invoke an imagined API. `browser_pdf` prints the current page and cannot replace a PDF exported by the application.

Start desktop runs with a 1920×1080 viewport, unless the case explicitly requires another viewport. **Default raw and annotated capture to `browser_take_screenshot(full_page=false)` explicitly.** Choose a view retaining the screen/record identity and values needed for the assertion. Use `true` only when the whole layout is necessary and record the reason. Scroll and capture separate pairs when needed rather than stretching one image. Full-page is a screenshot scope, not window maximization or proof that every pane/row is visible.

## Capture one checkpoint

1. Read its concrete Expected/Focus and identify the application state needed to prove it. Wait for the required visible state with available tools, then snapshot before any interaction. Use fresh snapshot refs for actions, one action per call. No app-field, filter, score, response or result mutation through evaluate to manufacture evidence.
2. Ensure no earlier temporary note/highlight remains. Capture **raw first**, with the selected explicit boolean `full_page` scope and no highlight refs. Archive the returned path immediately through [run artifacts](output.md), verify its digest, and retain the raw pixels unchanged. Do not derive a path from timestamp or let the next capture overwrite it before archival.
3. Confirm the same observed state, viewport, scroll position and capture scope are still present. If any changed between captures, start a new pair; do not combine the earlier raw with the later annotated image. Record a short observed-state/scroll description and actual capture references/times/scope in the ledger.
4. Add a temporary, clearly separated English note using `browser_evaluate` only if that tool is allowed. It identifies Case/Variant/Checkpoint and describes the observation, for example `TC-SYN-001 / below / CP-result: score 29 is marked red; displayed red count is 1.` Use `textContent`, never interpolate note text into executable JS/HTML. Place it in visually checked free space; no data, labels or messages may be covered. Keep original UI labels, identifiers and test payload literals. Text created as test data must also be meaningful English; report prose follows the user's language.
5. Place the short English observed-state note at the **top-right** in visually checked free space. If it would cover UI/data, adjust the view before a new raw capture, or use an authorized annotation-only gutter without changing product data; document that method and keep the same scope/state in both captures. Never shrink away relevant context. **After adding the note**, acquire the final snapshot. Select only cells/inputs/messages needed for the assertion. Remove duplicate and nested refs; reject regions whose rendered borders touch, intersect or overlap. When proving a score/result pair, one shared box around the pair is appropriate. A whole table is not adequate for an assertion about one value. Include all required validation messages.
6. Check each chosen ref has exactly one DOM match, is visible with positive width/height, and its text/value/state/bounds match the focus. DOM reads may inspect snapshot-assigned refs; actions still use MCP refs. On the observed duplicate-ref bug, clear only temporary `data-mcp-ref` attributes, take another snapshot, then recheck. Clearing attributes invalidates previous refs; never interact with them afterwards.
7. Capture annotated with the **same explicit `full_page` scope as raw**, `highlight_refs=[current refs]`, `highlight_mode="each"` for separated regions. Use `union` only if a single combined area proves the assertion (such as a score/result pair) without highlighting unrelated content. Do not rely on `auto` merging. Archive immediately before another capture.
8. Open **both archived files as pixels** with the available image viewer, then inspect annotated highlight position, complete assertion coverage, note truth/placement, readable values and checkpoint identity. If the image is long, inspect at original resolution and additional image views as needed; a downscaled preview alone can conceal misplaced highlights. Preserve PNG resolution/proportions; only report display dimensions may change.
9. On bad evidence, record the reason and correct/repeat the pair. Allow at most **three corrections per checkpoint**, tracked separately as `correction_attempt` 1–3; an original view uses 0. Image `sequence` is a positive archive ordinal, not the correction counter: a checkpoint can need more than four accepted full-page views. Preserve rejected attempts. Exhausted correction budget becomes an evidence-quality gap with the last observed state. It does not establish an application failure or complete PASS.
10. In a finally-style cleanup sequence, remove only the note/styles created by this capture and verify their absence. The native tool normally removes its overlay and restores temporary full-page styles; check rather than assume. Log cleanup failure and stop dependent evidence actions until the page state is understood. Cleanup does not perform test reset; execute the case's reset separately and record the action actually performed.

Do not mark an image accepted just because the tool returns `Screenshot saved`. Write reviewer/time/source only **after** opening the pixels. Name the actual agent or user; never invent human approval. Missing note/highlight support or failure to review an image remains an evidence gap, not an exception that accepts unannotated report evidence.

## Ref collision and remaining full-page risk

The inspected runtime assigns refs anew during snapshot but can leave old `data-mcp-ref` attributes on hidden nodes. Native highlight resolves its selector's first match; a hidden duplicate can produce no box even though capture succeeds. The following narrowly scoped repair removes MCP metadata only:

```javascript
(() => {
  const nodes = [...document.querySelectorAll('[data-mcp-ref]')];
  nodes.forEach(node => node.removeAttribute('data-mcp-ref'));
  return { removedTemporaryRefs: nodes.length };
})()
```

Take a new snapshot afterwards. To inspect selected refs, pass the actual refs from that snapshot into this read-only expression (encode the array as JSON rather than interpolating arbitrary text):

```javascript
(() => {
  const refs = ['e21', 'e29']; // Replace with the latest observed refs.
  return refs.map(ref => {
    const nodes = [...document.querySelectorAll('[data-mcp-ref]')]
      .filter(node => node.getAttribute('data-mcp-ref') === ref);
    return { ref, matches: nodes.length, regions: nodes.map(node => {
      const box = node.getBoundingClientRect(), style = getComputedStyle(node);
      return { text: node.textContent, value: node.value,
        visible: style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0',
        x: box.x, y: box.y, width: box.width, height: box.height };
    }) };
  });
})()
```

**Remaining risk:** the screenshot tool itself can prepare a best-effort expanded layout and take another snapshot before resolving highlight refs. Internal panes becoming visible can change numbering; pre-capture uniqueness does not guarantee the same target inside capture. Pixel review and bounded correction remain mandatory. A successfully repaired synthetic probe does not prove arbitrary dynamic BLEND screens are safe. If this runtime cannot highlight the required target correctly within the budget, record that proof gap; do not patch the server or declare coverage.

For horizontal tables, virtualized rows and multiple panes, scroll using available MCP tools to each relevant state and take additional focused viewport pairs. Give each pair a clear checkpoint/sequence and scroll-state note. When necessary, a stitched/expanded full-page view can temporarily change layout; record the method and never claim it is an untouched browser layout. Missing rows, clipped right-hand columns or inaccessible panes must remain explicit. Additional screenshots attach directly to their checkpoint with a descriptive title above each image.

## Note ownership and cleanup

An example safe temporary note uses a unique marker and `textContent`; its position must be selected from actual free space, not copied blindly:

```javascript
(() => {
  const id = '__blend_evidence_note__';
  if (document.getElementById(id)) throw new Error('Note ID already exists');
  const note = document.createElement('aside');
  note.id = id;
  note.setAttribute('data-blend-evidence-note', 'true');
  note.textContent = 'TC-SYN-001 / below / CP-result: score 29 is marked red.';
  Object.assign(note.style, { position: 'fixed', top: '12px', right: '12px',
    maxWidth: '360px', padding: '10px', background: '#fffbe6', color: '#111',
    border: '2px solid #8a6500', font: '16px/1.4 sans-serif', zIndex: '2147483646',
    pointerEvents: 'none' });
  document.body.appendChild(note);
  return { noteAdded: true };
})()
```

After capture or error, remove only this owned note and verify cleanup:

```javascript
(() => {
  const note = document.querySelector('#__blend_evidence_note__[data-blend-evidence-note="true"]');
  if (note) note.remove();
  return { ownedNoteRemaining: !!document.querySelector('[data-blend-evidence-note="true"]'),
    nativeOverlayRemaining: !!document.getElementById('__mcp_screenshot_overlay__') };
})()
```

If the evaluate policy disallows these operations, retain the actual observation and name the annotation capability gap. Do not change evaluate policy, restart the server or silently accept a note-free image. Synthetic capability probes belong in a separate, clearly identified run; their content is never evidence of a product testcase.
