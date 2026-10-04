<?php
class NoticeStore extends CI_Model
{
    public function findOwned($id, $schoolId, $ownerId)
    {
        return $this->db->get_where('notices', [
            'id' => $id, 'school_id' => $schoolId, 'owner_id' => $ownerId
        ])->row_array();
    }

    public function save($id, $title)
    {
        return $this->db->where('id', $id)->update('notices', ['title' => $title]);
    }
}
