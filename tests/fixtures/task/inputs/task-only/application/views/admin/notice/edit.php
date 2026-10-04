<?php // Synthetic teacher draft editor source; not executed. ?>
<form method="post" action="/admin/notice/send/<?= (int) $draft['id'] ?>">
    <input type="hidden" name="csrf_token" value="<?= html_escape($this->security->get_csrf_hash()) ?>">
    <p><?= html_escape($draft['body']) ?></p>
    <button type="submit" onclick="return confirm('Send to the selected group?')">Publish</button>
</form>
