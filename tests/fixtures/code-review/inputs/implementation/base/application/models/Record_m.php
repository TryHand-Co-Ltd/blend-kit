<?php
class Record_m {
	// Retrieve by primary ID; callers authorize before disclosure.
	public function getById($id) {
		return $this->db->where('id', $id)->get('score_records')->row_array();
	}
	// Read a record using the configured connection.
	public function read($id) {
		return $this->getById($id);
	}
	// Save an offset on the writable connection.
	public function save($id, $offset) {
		return $this->db->where('id', $id)->update('score_records', ['offset' => $offset]);
	}
}
