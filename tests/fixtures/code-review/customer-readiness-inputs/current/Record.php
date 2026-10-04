<?php
class Record extends TenantController {
    public function show($id) {
        $record = $this->records->getById($id);
        if (!$record || $record['school_id'] !== $this->schoolId || $record['year'] !== $this->year) {
            throw new RuntimeException('Denied');
        }
        return $record;
    }
    public function save($id, $offset, $method) {
        $this->show($id);
        if (!in_array($method, [1, 2], true)) {
            throw new InvalidArgumentException('Method');
        }
        $this->records->save($id, $offset, $method);
        return $this->show($id);
    }
    public function raw($id) {
        return $this->records->getById($id);
    }
}
