<?php
// Synthetic existing flow: no expiry support yet; not a runnable application.
class Notice extends CI_Controller {
    public function edit($id) {
        $draft = $this->owned_current_draft($id);
        if (!$draft) { show_error('Forbidden', 403); return; }
        $this->load->view('admin/notice/edit', ['draft' => $draft]);
    }
    public function save($id) {
        $draft = $this->owned_current_draft($id);
        if (!$draft) { show_error('Forbidden', 403); return; }
        $body = $this->input->post('body');
        if (!is_string($body) || trim($body) === '') { show_error('Body is required', 422); return; }
        $this->db->where('id', $id)->update('notices', ['body' => $body]);
        redirect('/admin/notice/edit/' . (int) $id);
    }
    private function owned_current_draft($id) {
        if ($this->session->userdata('role') !== 'teacher') { return null; }
        return $this->db->get_where('notices', ['id' => $id,
            'school_id' => $this->session->userdata('school_id'),
            'year' => $this->session->userdata('year'),
            'owner_id' => $this->session->userdata('user_id'), 'state' => 'draft'])->row_array();
    }
}
