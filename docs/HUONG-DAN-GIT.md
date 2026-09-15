# Hướng dẫn Git cho người mới bắt đầu

Tài liệu này dành cho thành viên chưa quen dùng Git. Làm theo đúng thứ tự.

---

## Bước 1 — Cài đặt (chỉ làm 1 lần)

1. Tạo tài khoản GitHub tại https://github.com/signup
   **Dùng đúng email đã đăng ký trong nhóm** để commit được ghi nhận tên bạn.
2. Cài Git: https://git-scm.com/downloads
3. Cài Python 3.10+: https://www.python.org/downloads
   Khi cài nhớ tick vào ô **"Add Python to PATH"**.
4. Cài Visual Studio Code: https://code.visualstudio.com

Sau đó mở Terminal (hoặc PowerShell) và khai báo danh tính:

```bash
git config --global user.name "Nguyen Van A"
git config --global user.email "email-cua-ban@gmail.com"
```

> Thay bằng tên và email của chính bạn.

---

## Bước 2 — Nhận lời mời vào repo

Nhóm trưởng sẽ gửi lời mời cộng tác. Bạn sẽ nhận được email từ GitHub,
hoặc vào thẳng https://github.com/notifications để bấm **Accept invitation**.

Chưa bấm Accept thì bạn không push code lên được.

---

## Bước 3 — Tải code về máy

```bash
git clone https://github.com/tronghv77/snake-game-uit.git
cd snake-game-uit
```

---

## Bước 4 — Chạy thử game

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1     # Windows PowerShell
# source .venv/bin/activate    # macOS / Linux

pip install -r requirements.txt
python main.py
```

Hiện ra cửa sổ đen có lưới và dòng chữ "SNAKE GAME" là thành công.
Nhắn vào nhóm Zalo báo đã chạy được.

---

## Bước 5 — Quy trình làm việc hằng ngày

**Nguyên tắc vàng: không bao giờ code trực tiếp trên nhánh `main`.**

```bash
# 1. Lấy code mới nhất về (làm mỗi khi bắt đầu ngồi vào code)
git checkout main
git pull origin main

# 2. Tạo nhánh riêng cho việc mình sắp làm
git checkout -b feat/snake-di-chuyen

# 3. Code...

# 4. Xem mình đã sửa những file nào
git status

# 5. Lưu lại thay đổi
git add .
git commit -m "feat: rắn di chuyển được bằng phím mũi tên"

# 6. Đẩy lên GitHub
git push -u origin feat/snake-di-chuyen
```

Sau khi push, mở https://github.com/tronghv77/snake-game-uit sẽ thấy nút
**Compare & pull request** màu vàng. Bấm vào, viết mô tả ngắn, bấm
**Create pull request**, rồi nhắn nhóm nhờ người khác vào duyệt.

---

## Quy ước đặt tên nhánh

| Loại việc | Mẫu tên | Ví dụ |
|-----------|---------|-------|
| Thêm tính năng | `feat/...` | `feat/am-thanh-an-moi` |
| Sửa lỗi | `fix/...` | `fix/ran-di-xuyen-tuong` |
| Viết tài liệu | `docs/...` | `docs/cap-nhat-readme` |
| Dọn dẹp code | `refactor/...` | `refactor/tach-ham-ve` |

## Quy ước viết commit message

```
<loại>: <mô tả ngắn, tiếng Việt có dấu, không viết hoa đầu câu>
```

Ví dụ tốt:
- `feat: thêm màn hình game over`
- `fix: sửa lỗi mồi sinh trùng lên thân rắn`
- `docs: bổ sung hướng dẫn cài đặt`

Ví dụ nên tránh: `update`, `sửa tí`, `abc`, `final_v2_thatsu`.

---

## Xử lý các tình huống hay gặp

**Lỡ code thẳng trên `main` rồi, giờ sao?**
```bash
git checkout -b feat/ten-nhanh-moi   # chuyển hết thay đổi sang nhánh mới
git add .
git commit -m "feat: mô tả việc đã làm"
git push -u origin feat/ten-nhanh-moi
```

**Push bị báo `rejected` / `non-fast-forward`?**
Nghĩa là trên GitHub có code mới hơn máy bạn:
```bash
git pull origin main --rebase
git push
```

**Bị "conflict" khi merge?**
VS Code sẽ tô màu đoạn code bị đụng, có nút *Accept Current* / *Accept Incoming*.
Chọn phần đúng, xoá các dòng `<<<<<<<`, `=======`, `>>>>>>>`, rồi:
```bash
git add .
git commit -m "fix: giải quyết conflict"
```
Không tự tin thì chụp màn hình gửi nhóm trưởng, đừng đoán bừa.

**Muốn bỏ hết thay đổi chưa commit, quay lại như cũ?**
```bash
git restore .
```
> Cẩn thận: lệnh này xoá vĩnh viễn các sửa đổi chưa commit.
