<?php
// Determine whether a score is below the configured threshold.
function isBelow($score, $threshold) {
	return $score < $threshold;
}
// Format a legacy alias.
function legacyAlias($record) {
	return $record['alias'];
}
