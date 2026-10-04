<!-- blend-template: research@1.0.0 -->
# Synthetic selected topic

Topic revision TOPIC-2; legacy research@1.0.0 input, read-only. Purpose: identify title-save code and proof seam for SYN-PL-02-A, parent SYN-PL-02.

Conclusion C-TITLE: Notice::save uses NoticeStore::findOwned, persists raw title, and Notice::show reads the stored row through the same authorization lookup. NoticeStore::save currently updates only title. Source dependencies: SP-2 S-TITLE/S-EMPTY/S-PRESERVE; CF-3 confirms ASCII-space-only semantics; CTX-3 confirms no schema change. Code dependencies: application/controllers/Notice.php and application/models/NoticeStore.php in the supplied synthetic application snapshot. Capture actual byte identities at intake; do not use this text's revision alone as a code hash.

Currentness is bounded to those captured dependencies, not all feature topics. No functional runner, database execution or live behavior was observed. Engineering proposal: retain the existing lookup/save/readback boundary rather than introduce a new service. Equivalent approaches remain valid.
