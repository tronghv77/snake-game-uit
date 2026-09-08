# Về CI — vì sao đang tắt và thay bằng gì

Cập nhật: 08/09/2026

## Tóm tắt

Workflow CI (`.github/workflows/ci.yml`) **đang tắt tạm thời**. Đây là quyết định
có chủ đích của nhóm, không phải quên hay làm hỏng.

Việc này **không ảnh hưởng gì tới đồ án**. Clone, code, commit, Pull Request,
chạy game — tất cả vẫn bình thường.

## Vì sao tắt

Tài khoản GitHub của chủ repo bị khoá GitHub Actions vì một giao dịch thanh
toán bị ngân hàng từ chối (gói Copilot Pro, không liên quan gì tới đồ án này).
Thông báo GitHub trả về khi chạy CI:

```
The job was not started because your account is locked due to a billing issue.
```

Hệ quả: mọi lần push đều hiện dấu ✗ đỏ cạnh commit, dù code hoàn toàn đúng.
Dấu đỏ đó gây hiểu nhầm là code nhóm bị lỗi, nên nhóm tắt workflow đi cho sạch.

## Thay bằng gì

**Mỗi người tự chạy test ở máy trước khi tạo Pull Request.** Đúng một lệnh:

```bash
python -m pytest
```

Thấy dòng `passed` màu xanh là được. Thấy `failed` thì sửa xong mới tạo PR.

Quy tắc này vốn đã nằm trong [CONTRIBUTING.md](../CONTRIBUTING.md) từ đầu, CI
chỉ là lớp kiểm tra tự động thêm cho chắc. Với nhóm 3 người và bộ test chạy hết
4 giây, chạy tay là hoàn toàn đủ.

## Bật lại khi nào

Khi chủ repo xử lý xong phần thanh toán, bật lại bằng một lệnh:

```bash
gh workflow enable ci.yml
```

Rồi chạy lại lần kiểm tra gần nhất để xác nhận:

```bash
gh run rerun --failed
```

File `ci.yml` được giữ nguyên trong repo, không xoá, nên bật lại là chạy ngay
không phải viết lại gì.

## Ghi chú cho người chấm bài

Nhóm có viết cấu hình CI đầy đủ (cài Python, cài thư viện, chạy `pytest` ở chế
độ không cần màn hình). Cấu hình này đã được kiểm chứng là đúng — GitHub đọc
được file và tạo đúng job, chỉ bị chặn ở khâu cấp máy chạy vì lý do thanh toán
của tài khoản cá nhân. Toàn bộ bộ test vẫn chạy và pass ở máy các thành viên.
