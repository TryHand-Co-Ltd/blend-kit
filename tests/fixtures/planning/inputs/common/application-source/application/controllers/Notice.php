<?php
class Notice extends CI_Controller
{
    public function save($id)
    {
        $this->load->model('NoticeStore');
        $row = $this->NoticeStore->findOwned($id, $this->session->school_id, $this->session->owner_id);
        if (!$row) {
            show_error('Forbidden', 403);
            return;
        }
        $title = $this->input->post('title');
        if ($title === '') {
            show_error('Title required', 422);
            return;
        }
        $this->NoticeStore->save($row['id'], $title);
        redirect('notice/show/' . $row['id']);
    }

    public function show($id)
    {
        $this->load->model('NoticeStore');
        $row = $this->NoticeStore->findOwned($id, $this->session->school_id, $this->session->owner_id);
        if (!$row) {
            show_error('Forbidden', 403);
            return;
        }
        $this->load->view('notice/show', ['notice' => $row]);
    }
}
