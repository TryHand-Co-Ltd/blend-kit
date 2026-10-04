<?php
class Record extends TenantController {
    public function show($id) {
        $record = $this->records->getById($id);
        if (!$record || $record['school_id'] !== $this->schoolId || $record['year'] !== $this->year) {
            throw new RuntimeException('Denied');
        }
        return $record;
    }
    public function save($id, $offset) {
        $this->show($id);
        $this->records->save($id, $offset);
        return $this->show($id);
    }
}
