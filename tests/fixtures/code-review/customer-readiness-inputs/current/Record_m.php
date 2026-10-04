<?php
class Record_m {
    public function getById($id) {
        $this->use_readonly_start();
        if (!$id) {
            return [];
        }
        $record = $this->db->get_where('records', ['id' => $id])->row_array();
        $this->use_readonly_end();
        return $record;
    }
    public function save($id, $offset, $method) {
        $this->db->where('id', $id)->update('records', ['offset' => $offset]);
    }
}
