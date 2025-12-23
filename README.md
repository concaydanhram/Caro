# ⭕❌ Intelligent Tic-Tac-Toe AI

Dự án mã nguồn mở tái hiện trò chơi Cờ Caro (Tic-Tac-Toe) kinh điển với giao diện đồ họa hiện đại và tích hợp thuật toán trí tuệ nhân tạo (AI). Dự án tập trung vào việc tối ưu hóa thuật toán tìm kiếm nước đi (Minimax & Alpha-Beta Pruning) để đem lại trải nghiệm đối kháng thử thách.

---

## 👥 Đội ngũ phát triển

Dự án được thực hiện bởi nhóm sinh viên với sự phân công cụ thể:

| Vai trò | Thành viên |
| --- | --- |
| **Trưởng nhóm** | **Bùi Lê Hoàng** |
| Thành viên | Nguyễn Đình Kiên |
| Thành viên | Nguyễn Tùng Dương |
| Thành viên | Ngô Minh Hiển |

---

## ✨ Tính năng nổi bật

### 🧠 Hệ thống AI thông minh (Bot)

Bot được xây dựng dựa trên các thuật toán tìm kiếm đối kháng mạnh mẽ:

* **Minimax Algorithm:** Bot tính toán các nước đi khả thi để tối đa hóa lợi thế của mình và giảm thiểu cơ hội của đối thủ.
* **Alpha-Beta Pruning:** Kỹ thuật cắt tỉa nhánh giúp tối ưu hóa tốc độ xử lý, cho phép Bot duyệt sâu hơn trên bàn cờ lớn mà không tốn quá nhiều tài nguyên.
* **Adaptive Difficulty:** 3 cấp độ khó dựa trên độ sâu tìm kiếm (Depth):
* *Easy:* Tính toán nông hoặc ngẫu nhiên.
* *Medium:* Độ sâu trung bình.
* *Hard:* Sử dụng tối đa sức mạnh thuật toán.



### 🎮 Chế độ chơi đa dạng

Người chơi có thể lựa chọn giữa hai chế độ:

1. **Classic Mode (3x3):** Luật chơi truyền thống, thắng khi đạt 3 quân liên tiếp.
2. **Extended Mode (8x8):** Mở rộng bàn cờ, thắng khi đạt 5 quân liên tiếp (tương tự luật Caro).

### 🏆 Hệ thống dữ liệu & Thống kê

* **Leaderboard:** Lưu lại lịch sử đấu, thời gian hoàn thành và điểm số của người chơi vào file `scores.json`.
* **Real-time Stats:** Hiển thị thời gian suy nghĩ và số lượng node (nút) mà AI đã duyệt trong thời gian thực.

---

## ⚙️ Cài đặt & Hướng dẫn sử dụng

### 1. Yêu cầu hệ thống

* **Python 3.x** đã được cài đặt.
* Thư viện **Pygame**.

### 2. Cài đặt thư viện

Mở terminal (hoặc Command Prompt) và chạy lệnh sau:

```bash
pip install pygame

```

### 3. Khởi chạy trò chơi

Để bắt đầu, hãy chạy file `main.py` từ thư mục gốc của dự án:

```bash
python main.py

```

---

## 📂 Cấu trúc dự án

Mô tả ngắn gọn về các module chính trong mã nguồn:

* `main.py`: Điểm khởi chạy chương trình.
* `gameUI.py`: Quản lý giao diện đồ họa, vẽ bàn cờ, xử lý sự kiện chuột và hiển thị các màn hình (Menu, Leaderboard).
* `bot.py`: Chứa lớp `Bot`, cài đặt thuật toán Minimax và logic cắt tỉa Alpha-Beta.
* `game_logic.py`: Xử lý logic cốt lõi (kiểm tra thắng/thua, lượt đi, trạng thái bàn cờ).
* `player.py`: Định nghĩa đối tượng người chơi.
* `scores.json`: Cơ sở dữ liệu JSON lưu trữ bảng xếp hạng.

---

## 📸 Giao diện người dùng

Giao diện được thiết kế theo phong cách phẳng (Flat Design) với tông màu sáng và font chữ Montserrat/Arial:

* **Menu chính:** Cho phép chọn độ khó, chế độ chơi và xem bảng xếp hạng.
* **Trong game:** Hiển thị bàn cờ rõ ràng, có hiệu ứng highlight nước đi vừa đánh và đường kẻ chiến thắng.
* **Dashboard:** Hiển thị thông số kỹ thuật của Bot.

---

## 🤝 Đóng góp

Mọi ý kiến đóng góp hoặc báo lỗi vui lòng liên hệ trực tiếp với nhóm phát triển thông qua GitHub Issues hoặc email của trưởng nhóm.