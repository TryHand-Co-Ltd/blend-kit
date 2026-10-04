<?php
class ScoreJob {
	// Return the newly saved record to subsequent processing.
	public function saveAndRead($id, $offset) {
		$this->record_m->save($id, $offset);
		return $this->record_m->read($id);
	}
}
