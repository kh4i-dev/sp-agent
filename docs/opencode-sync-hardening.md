# Giảm tác nhân làm gián đoạn OpenCode khi đồng bộ skill — 2026-10-27

## Phạm vi và mức tin cậy

- **observed:** nhật ký OpenCode 2.1.4 có nhiều lần khởi chạy service mới ngay sau lệnh `tools/sync-skills.ps1`; không có mã thoát cũ để chứng minh nguyên nhân backend chết.
- **observed:** script cũ `Copy-Item -Recurse -Force` ghi lại file giữ nguyên nội dung. Ca thử nhỏ đo trực tiếp bằng FileSystemWatcher: 8 sự kiện thay đổi file trên lần sync không đổi (10 sự kiện nếu tính cả thư mục).
- **observed:** cây thật có 43 skill, 13.770 file giống nhau ở hai phía tại lúc đối chiếu.
- **Đọc mã tham chiếu:** compatibility skill watcher của OpenCode nạp lại skill sau sự kiện thay đổi trong cây skill. Đây là mã fork tham chiếu, không phải bằng chứng binary 2.1.4 có cùng mọi chi tiết.
- **inferred:** ghi lại toàn bộ cây làm tăng tải watcher và khả năng gián đoạn; chưa chứng minh đây là nguyên nhân duy nhất của các lần thoát.
- **observed:** OpenCode chuyển lên 2.2.0 trong lúc điều tra; trước khi vá script, lệnh sync qua Shell của bản này đã chạy exit 0 và backend giữ PID 7292. Không quy kết việc hết lỗi cho riêng bản vá này.

## Bản vá tại nguồn phát sinh thao tác ghi

Chủ đồng bộ vẫn là `tools/sync-skills.ps1`; không thêm một đường đồng bộ khác.

- So sánh SHA-256, không chỉ dựa vào timestamp/kích thước. File giống nhau không ghi lại.
- File đổi được sao chép vào file tạm cùng thư mục, kiểm lại hash rồi publish bằng File.Replace/File.Move. Lỗi không để lại file tạm; không xoá file riêng ở đích.
- Từ chối symlink/junction để không ghi ra ngoài hai cây skill.
- In số file đã chép và số file giữ nguyên để lần sau nhận biết sync bất thường.

Không thay binary OpenCode, không tắt watcher, không đổi model/provider, không reset dữ liệu hay cài plugin. Bản vá này giảm tác nhân ghi thừa, không phải bảo đảm OpenCode không bao giờ crash.

## Kiểm thử hồi quy

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/test-sync-skills.ps1 -FixtureRoot E:/Tools/Lealia-HUB-lab/scratch/opencode-sync-hardening
```

Fixture ở lab, không sinh file thử trong repo. Kiểm trực tiếp: sao chép lần đầu; tên có khoảng trắng/ký tự `[]`; file/thư mục rỗng; chạy lại có 0 sự kiện thay đổi **file**; nội dung đổi nhưng cùng kích thước và mtime vẫn được cập nhật; file mới được thêm; file riêng ở đích giữ nguyên; không sót file tạm. Sự kiện thư mục được in riêng, không gán thành lượt ghi file.

Cùng bài kiểm thử thất bại trên bản cũ và đạt trên bản vá bằng Windows PowerShell 5.1. Không gọi model để thử hạ tầng.

## Hoàn tác

Bản gốc được giữ ở `E:/Tools/Lealia-HUB-lab/scratch/opencode-sync-hardening/sync-skills.before.ps1`. Kiểm tra diff trước khi chép lại nếu phiên khác đã sửa script:

```powershell
Copy-Item -LiteralPath E:/Tools/Lealia-HUB-lab/scratch/opencode-sync-hardening/sync-skills.before.ps1 -Destination tools/sync-skills.ps1
```

## Nếu service còn thoát

Giữ log và ghi PID/mã thoát trước khi thử lại; không kill theo tên `node`/`bun`/`opencode`. Nhật ký desktop ở `%APPDATA%/ai.opencode.desktop/logs/`, log backend ở `%USERPROFILE%/.local/share/opencode/log/`. Không đưa `service.json`, credential hoặc log thô có dữ liệu người dùng vào báo cáo công khai. Không tự chạy lại lệnh ghi của agent khi chưa biết kết quả lần trước.
## Nghiệm thu thật sau khi áp dụng

**observed:** gọi `/api/shell` của OpenCode 2.2.0 chạy liên tiếp hai lần `tools/sync-skills.ps1`, rồi `tools/verify-skills.ps1` trong dự án thật. Cả hai lần sync báo `copied=0 unchanged=13770`; kiểm định 43/43 skill đạt; Shell kết thúc mã 0. PID backend trước/sau đều 7292. Parser PowerShell của script có 0 lỗi.

Bằng chứng máy cục bộ (không chứa credential): `E:/Tools/Lealia-HUB-lab/scratch/opencode-sync-hardening/live-result.json`. Không gọi model; không reset hay xoá dữ liệu OpenCode. Nghiệm thu này chứng minh hành vi đồng bộ và daemon sống qua phép thử, không chứng minh độ ổn định vô thời hạn.