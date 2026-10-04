<?php
// Synthetic CodeIgniter snapshot; never production code or a runnable app.
class Notice extends CI_Controller {
    public function edit($id) {
        $draft = $this->db->get_where('notices', ['id' => $id])->row_array();
        if (!$this->owned_current_draft($draft)) { show_error('Forbidden', 403); return; }
        $this->load->view('admin/notice/edit', ['draft' => $draft]);
    }
    public function send($id) {
        $draft = $this->db->get_where('notices', ['id' => $id])->row_array();
        if (!$this->owned_current_draft($draft)) { show_error('Forbidden', 403); return; }
        if (trim($draft['body']) === '') { show_error('Body is required', 422); return; }
        $this->db->where('id', $id)->update('notices', ['state' => 'published']);
        redirect('/admin/notice');
    }
    private function owned_current_draft($draft) {
        return $draft && $this->session->userdata('role') === 'teacher'
            && $draft['owner_id'] === $this->session->userdata('user_id')
            && $draft['school_id'] === $this->session->userdata('school_id')
            && $draft['year'] === $this->session->userdata('year') && $draft['state'] === 'draft';
    }
}
