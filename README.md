# 🐍 Snake Game — Đồ án nhóm UIT

Game rắn săn mồi kinh điển, viết bằng **Python + Pygame**.
Đây là đồ án môn học của nhóm 3 thành viên, Trường Đại học Công nghệ Thông tin — ĐHQG TP.HCM.

---

## 👥 Thành viên nhóm

| # | Họ và tên | MSSV | Vai trò | Phụ trách |
|---|-----------|------|---------|-----------|
| 1 | Hồ Văn Trọng | 26730077 | Nhóm trưởng | Vòng lặp game, va chạm, tính điểm, quản lý repo |
| 2 | Lê Kiều Diễm | 26730010 | Thành viên | Đối tượng rắn, mồi, xử lý di chuyển |
| 3 | Đặng Đức Tín | 26730073 | Thành viên | Giao diện, menu, âm thanh, cấu hình |

Bảng phân công tóm tắt: [docs/PHAN-CONG.md](docs/PHAN-CONG.md)
**Mô tả công việc chi tiết từng người: [docs/MO-TA-CONG-VIEC.md](docs/MO-TA-CONG-VIEC.md)**
Sơ đồ trạng thái và sơ đồ lớp: [docs/SO-DO.md](docs/SO-DO.md)

---

## 🎮 Tính năng dự kiến

- [ ] Rắn di chuyển bằng phím mũi tên / WASD
- [ ] Sinh mồi ngẫu nhiên, ăn mồi thì rắn dài ra
- [ ] Va chạm tường và va chạm thân rắn → thua
- [ ] Hiển thị điểm hiện tại và điểm cao nhất
- [ ] Màn hình menu, tạm dừng (phím `P`), game over
- [ ] Nhiều mức độ khó (tốc độ rắn khác nhau)
- [ ] Âm thanh khi ăn mồi và khi thua

---

## 🚀 Cách chạy game

Yêu cầu: **Python 3.10 trở lên**.

```bash
# 1. Tải code về
git clone https://github.com/tronghv77/snake-game-uit.git
cd snake-game-uit

# 2. Tạo môi trường ảo
python -m venv .venv

# 3. Kích hoạt môi trường ảo
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 4. Cài thư viện
pip install -r requirements.txt

# 5. Chạy game
python main.py
```

Nếu chạy được, bạn sẽ thấy một cửa sổ hiện lưới ô vuông và dòng chữ báo dự án đã sẵn sàng.

---

## 📁 Cấu trúc thư mục

```
snake-game-uit/
├── main.py              # File chạy game
├── requirements.txt     # Danh sách thư viện cần cài
├── src/snake/
│   ├── config.py        # Hằng số: kích thước, màu sắc, tốc độ  (Tín)
│   ├── game.py          # Vòng lặp game, trạng thái, va chạm    (Trọng)
│   ├── snake.py         # Lớp Snake — thân rắn, di chuyển       (Diễm)
│   ├── food.py          # Lớp Food — sinh mồi ngẫu nhiên        (Diễm)
│   └── ui.py            # Vẽ menu, điểm số, màn hình game over  (Tín)
├── assets/              # Hình ảnh, âm thanh, font chữ
├── tests/               # Kiểm thử
└── docs/                # Tài liệu nhóm
```

---

## 🤝 Quy trình làm việc nhóm

**Không ai được push thẳng lên nhánh `main`.** Mọi thay đổi đều đi qua Pull Request.

```bash
git checkout main
git pull origin main
git checkout -b feat/ten-tinh-nang
# ... code ...
git add .
git commit -m "feat: mô tả ngắn việc đã làm"
git push -u origin feat/ten-tinh-nang
```

Sau đó vào GitHub tạo Pull Request, chờ 1 thành viên khác duyệt rồi mới merge.

Hướng dẫn Git đầy đủ cho người mới: [docs/HUONG-DAN-GIT.md](docs/HUONG-DAN-GIT.md)
Quy tắc đóng góp: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 Giấy phép

[MIT License](LICENSE)
