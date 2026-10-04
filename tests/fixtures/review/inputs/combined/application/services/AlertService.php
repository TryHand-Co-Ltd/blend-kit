<?php
// Synthetic snapshot proving As-Is, not business authority.
function percent_result($score, $percent) { return floor($score * $percent / 100); }
function alert($score, $threshold) { return $score < $threshold; }
function subtraction_result($score, $offset) { return round($score - $offset); } // unresolved business oracle
function apply_target_only($school, $year, $course, $inputs, $saved) {
    foreach ($saved as &$row) {
        if ($row['school'] !== $school || $row['year'] !== $year || $row['course'] !== $course) continue;
        $row['alert'] = alert($inputs[$row['id']], 80);
    }
    return ['status' => 'done', 'rows' => $saved];
}
