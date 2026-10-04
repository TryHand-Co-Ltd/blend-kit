<?php
// Synthetic source snapshot; never execute as an application.
function recalculate($actor, $school, $year, $course, $enabled, $inputs, $saved) {
    if ($actor->role !== 'school-admin') return ['error' => 'forbidden', 'rows' => $saved];
    if (!$enabled) return ['status' => 'skipped', 'rows' => $saved];
    if (in_array(null, $inputs, true)) return ['error' => 'source-score-missing', 'rows' => $saved];
    return apply_target_only($school, $year, $course, $inputs, $saved);
}
