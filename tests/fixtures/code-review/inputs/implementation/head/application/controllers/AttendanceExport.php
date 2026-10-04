<?php
class AttendanceExport {
	// Preserve the existing boundary for attendance export.
	public function classify($record) {
		return isBelow($record['score'], $record['threshold']) ? 'flagged' : 'normal';
	}
}
