<?php // Synthetic existing draft form. Expiry field is absent in As-Is. ?>
<form method="post" action="/admin/notice/save/<?= (int) $draft['id'] ?>">
    <input type="hidden" name="csrf_token" value="<?= html_escape($this->security->get_csrf_hash()) ?>">
    <textarea name="body"><?= html_escape($draft['body']) ?></textarea>
    <button type="submit">Save draft</button>
</form>
