# Quy tắc đóng góp

## Trước khi code
1. `git pull origin main` để lấy code mới nhất.
2. Tạo nhánh riêng: `git checkout -b feat/ten-tinh-nang`.
3. Kiểm tra trên GitHub xem việc mình định làm đã có ai nhận trong tab **Issues** chưa.

## Trong lúc code
- Chỉ sửa file thuộc phần mình phụ trách (xem [docs/PHAN-CONG.md](docs/PHAN-CONG.md)).
- Đặt tên biến và hàm bằng tiếng Anh, viết comment bằng tiếng Việt.
- Không viết số cứng trong code, đưa hằng số vào `src/snake/config.py`.
- Mỗi commit chỉ giải quyết một việc.

## Trước khi tạo Pull Request
- [ ] Chạy `python main.py` thấy game không lỗi.
- [ ] Chạy `python -m pytest` thấy test pass.
- [ ] Không commit nhầm thư mục `.venv/` hay `__pycache__/`.
- [ ] Commit message viết theo mẫu `feat:` / `fix:` / `docs:` / `refactor:`.

> ⚠️ **Bước chạy `pytest` là bắt buộc, không được bỏ.** CI tự động trên GitHub
> đang tắt tạm thời nên không ai chạy test giùm bạn nữa — xem lý do ở
> [docs/VE-CI.md](docs/VE-CI.md).

## Pull Request
- Tiêu đề mô tả rõ việc đã làm.
- Mô tả kèm ảnh chụp màn hình nếu có thay đổi giao diện.
- Gán một thành viên khác làm reviewer.
- **Cần ít nhất 1 người duyệt mới được merge.** Không tự duyệt PR của mình.
- Merge xong thì xoá nhánh cũ.

## Review code cho bạn cùng nhóm
Đọc kỹ, chạy thử trên máy mình, góp ý cụ thể và tử tế. Nếu không có vấn đề gì
thì bấm **Approve**, đừng để PR treo quá 2 ngày.
