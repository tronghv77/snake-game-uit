# Phân công công việc

## Thông tin nhóm

| Họ và tên | MSSV | GitHub | Vai trò |
|-----------|------|--------|---------|
| Hồ Văn Trọng | 26730077 | @tronghv77 | Nhóm trưởng |
| Lê Kiều Diễm | 26730010 | @Lekieudiem26730010 | Thành viên |
| Đặng Đức Tín | 26730073 | @26730073 | Thành viên |

---

> 📄 Tài liệu này chỉ là bảng tóm tắt. Mô tả chi tiết từng đầu việc — gồm mục tiêu,
> gợi ý thực hiện, cạm bẫy thường gặp và tiêu chí nghiệm thu — nằm ở
> [MO-TA-CONG-VIEC.md](MO-TA-CONG-VIEC.md).

## Chia việc theo file

Mỗi người làm trên file riêng để hạn chế đụng độ khi merge code.

### Hồ Văn Trọng — `src/snake/game.py`
- Vòng lặp game (`run`, `update`, `draw`)
- Nhận phím điều khiển: mũi tên, WASD, `P` tạm dừng, `Space` bắt đầu / chơi lại
- Quản lý trạng thái: MENU → PLAYING → PAUSED → GAME_OVER
- Kiểm tra va chạm tường và va chạm thân rắn
- Tính điểm, lưu và đọc điểm cao nhất
- Quản lý repository, duyệt Pull Request, gộp code

### Lê Kiều Diễm — `src/snake/snake.py`, `src/snake/food.py`
- Lớp `Snake`: khởi tạo thân rắn, di chuyển, dài ra khi ăn mồi
- Chặn thao tác quay đầu 180 độ
- Hàm `hits_self()` phát hiện rắn cắn phải thân mình
- Lớp `Food`: sinh mồi ở ô ngẫu nhiên, không trùng lên thân rắn
- Viết test cho hai lớp này trong `tests/`

### Đặng Đức Tín — `src/snake/ui.py`, `src/snake/config.py`
- Vẽ rắn, vẽ mồi
- Hiển thị điểm hiện tại và điểm cao nhất
- Màn hình menu và màn hình game over
- Chọn bảng màu, font chữ, tinh chỉnh các hằng số trong `config.py`
- Thêm âm thanh khi ăn mồi và khi thua

---

## Mốc thời gian

| Giai đoạn | Nội dung | Ai làm | Hạn |
|-----------|----------|--------|-----|
| 1 | Ai cũng clone được repo và chạy được `python main.py` | Cả nhóm | |
| 2 | Rắn di chuyển được trên màn hình | Diễm + Trọng | |
| 3 | Ăn mồi, dài ra, cộng điểm | Diễm + Trọng | |
| 4 | Va chạm và màn hình game over | Trọng + Tín | |
| 5 | Menu, âm thanh, mức độ khó | Tín | |
| 6 | Viết báo cáo, quay video demo | Cả nhóm | |

> Nhóm trưởng điền deadline cụ thể sau khi biết ngày nộp bài.

---

## Quy ước làm việc

- Họp online mỗi tuần 1 lần, báo tiến độ trong nhóm Zalo.
- Ai kẹt quá 1 ngày ở một chỗ thì nhắn nhóm ngay, đừng ngồi im.
- Commit ít nhất 2–3 lần mỗi tuần để giảng viên thấy được đóng góp của từng người.
- Không sửa file của người khác. Nếu cần sửa, nhắn cho người đó trước.
