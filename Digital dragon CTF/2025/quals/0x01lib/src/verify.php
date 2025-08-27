<?php
require 'function.php';
require '.env.php';
require 'books.php'; // Include the books array

$result = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $hex = $_POST['token'] ?? '';
    $bin = @hex2bin($hex);

    if ($bin) {
        $decrypted = decrypt($bin, KEY, IV);        
        if ($decrypted) {
            $data = json_decode($decrypted);
            $raw_display = htmlspecialchars($decrypted);
            if (is_object($data) && !empty($data->username)) {
                // Hiển thị thông tin user đã đăng ký
                $info = "<ul>";
                foreach ($data as $k => $v) {
                    $info .= "<li><b>" . htmlspecialchars($k) . ":</b> " . htmlspecialchars($v) . "</li>";
                }
                $info .= "</ul>";

                // Nội dung sách mặc định
                $bookInfo = "<p style='color:red;'>Tên sách không hợp lệ</p>";

                // Nếu bookname hợp lệ thì hiển thị
                if (!empty($data->bookname) && isset($books[$data->bookname])) {
                    $book = $books[$data->bookname];
                    $bookInfo = "
                        <p>📖 Cuốn sách bạn mượn:</p>
                        <img src='" . htmlspecialchars($book['cover']) . "' alt='Book cover' />
                        <p><b>Nội dung sách:</b> " . htmlspecialchars($book['description']) . "</p>
                    ";
                }

                // Check quyền admin
                $extra = "";
                if (!empty($data->is_admin)) {
                    $extra = "<br><b>🎉 Chào mừng Admin! Đây là thông điệp mà bạn tìm kiếm</b><br><b>🔐 FLAG: </b><code>" . FLAG . "</code>";
                }

                // Thành công
                $result = "<b>📚 Thông tin bạn đã đăng ký:</b>$info $bookInfo $extra";
            } else {
                $result = "<b style='color:red'>❌ Không thể đọc dữ liệu JSON</b><br>
                   <pre>$raw_display</pre>";
            }
        } else {
            $result = "<b style='color:red'>❌ Token không hợp lệ</b>";
        }
    } else {
        $result = "<b style='color:red'>❌ Token không hợp lệ</b>";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Xác thực thẻ mượn sách</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="box">
    <h2>🔐 Xác thực thẻ mượn sách</h2>
    <form method="POST">
        <label>Token:</label>
        <textarea name="token" required></textarea>
        <input type="submit" value="Xác thực">
    </form>

    <?php if ($result): ?>
        <div class="result"><?= $result ?></div>
    <?php endif; ?>

    <a class="button-link" href="generate.php">← Đăng ký lại</a>
</div>
</body>
</html>
