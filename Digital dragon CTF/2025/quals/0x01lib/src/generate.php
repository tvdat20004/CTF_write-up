<?php
require 'function.php';
require '.env.php';
require 'books.php'; // Include the books array


$token = null;
$form_data = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $class = $_POST['class'] ?? '';
    $bookname = $_POST['bookname'] ?? '';

    $form_data = compact('username', 'class', 'bookname');
    $form_data['is_admin'] = 0; // mặc định user thường
    $json = json_encode($form_data);
    $encrypted = encrypt($json, KEY, IV);
    $token = bin2hex($encrypted);
}
?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Thư viện - Đăng ký</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="box">
    <h2>📚 Đăng ký thẻ mượn sách</h2>
    <form method="POST">
        <div>
            <label for="username">Tên sinh viên</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="class">Lớp</label>
            <input type="text" id="class" name="class">
        </div>
        <div>
            <label for="bookname">Chọn sách</label>
            <select id="bookname" name="bookname" required>
                <?php foreach ($books as $title => $info): ?>
                    <option value="<?= htmlspecialchars($title) ?>"><?= htmlspecialchars($title) ?></option>
                <?php endforeach; ?>
            </select>
        </div>
        <input type="submit" value="Đăng ký">
    </form>

    <?php if ($token): ?>
        <div class="token-box">
            <strong>Your Token:</strong><br>
            <code><?= htmlspecialchars($token) ?></code>            
        </div>
        <a class="button-link" href="verify.php">→ Mượn sách</a>
    <?php endif; ?>
</div>
</body>
</html>
