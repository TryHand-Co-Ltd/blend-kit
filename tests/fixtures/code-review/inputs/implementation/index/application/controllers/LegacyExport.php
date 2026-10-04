<?php
class LegacyExport {
	// Existing alias export is outside the assigned feature.
	public function row($record) {
		return legacyAlias($record);
	}
}
