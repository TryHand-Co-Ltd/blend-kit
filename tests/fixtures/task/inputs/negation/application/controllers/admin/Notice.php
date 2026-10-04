<?php
// Synthetic CodeIgniter snapshot; not production or a runnable app.
class Notice extends CI_Controller {
    public function edit($id) {
        $draft = $this->draft($id);
        if (!$draft) { show_error('Forbidden', 403); return; }
        $this->load->view('admin/notice/edit', ['draft' => $draft]);
    }
    public function send($id) {
        $draft = $this->draft($id);
        if (!$draft) { show_error('Forbidden', 403); return; }
        if (trim($draft['body']) === '') { show_error('Body is required', 422); return; }
        $this->db->where('id', $id)->update('notices', ['state' => 'published']);
        redirect('/admin/notice');
    }
    private function draft($id) {
        if ($this->session->userdata('role') !== 'teacher') { return null; }
        return $this->db->get_where('notices', ['id' => $id,
            'school_id' => $this->session->userdata('school_id'),
            'year' => $this->session->userdata('year'),
            'owner_id' => $this->session->userdata('user_id'), 'state' => 'draft'])->row_array();
    }
}
