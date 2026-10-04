<?php
class Score {
	// View an authorized record.
	public function show($id) {
		$record = $this->record_m->getById($id);
		if ($record['school_id'] !== $this->login_data['school_id'] || $record['year'] !== $this->login_data['year']) {
			return 'denied';
		}
		return $record;
	}
	// Name the calculation action.
	public function label() {
		return 'Run';
	}
	// Export a record for the new endpoint.
	public function rawExport($id) {
		return $this->record_m->getById($id);
	}
}
