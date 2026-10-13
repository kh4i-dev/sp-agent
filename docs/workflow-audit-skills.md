# Quy trình kiểm định skill tự động (quét theo khối)

Mục đích: thay việc soi tay bằng **một lệnh chạy được**, quét toàn bộ skill theo 6 khối
(`coord-report`, `coord-docs`, `coord-diagrams`, `coord-slides`, `coord-data`, `coord-research`),
phát hiện: frontmatter sai, SKILL.md quá dài, mirror `.claude`↔`.agents` lệch, link hỏng,
thành viên khối thiếu, thiếu invariant theo khối (zero-color / em dash / gate), và drift
giữa bảng block trong `AGENTS.md` với bảng "Khối gồm" của từng `coord-*`.

## Chạy nhanh

```powershell
# Toàn bộ (verify frontmatter + audit theo khối); exit != 0 khi có FAIL
powershell -ExecutionPolicy Bypass -File tools/check-all.ps1

# Chỉ 1 khối:
powershell -ExecutionPolicy Bypass -File tools/audit-skills.ps1 -Block coord-diagrams

# Xuất JSON cho agent xử lý tiếp:
powershell -ExecutionPolicy Bypass -File tools/audit-skills.ps1 -Json
```

## Các công cụ

- `tools/verify-skills.ps1`: frontmatter (`name` trùng tên thư mục, kebab-case, ≤64 ký tự;
  `description` ≤1024 ký tự).
- `tools/audit-skills.ps1`: quét theo khối — đọc bảng "Khối gồm" của từng `coord-*` làm SSOT —
  kiểm: SKILL.md ≤500 dòng, UTF-8 (phát hiện mojibake), link nội bộ trong `SKILL.md`
  (bỏ qua placeholder/minh hoạ), parity mirror `.claude`↔`.agents`, invariant theo khối,
  drift `AGENTS.md`↔`coord-*`.
- `tools/check-all.ps1`: chạy cả hai lệnh trên; exit khác 0 khi có FAIL.

## Khi nào chạy

- Sau mọi lần sửa skill, **trước khi commit/push** (thay cho checklist tay).
- Sau khi chạy `sync-skills.ps1` nếu nghi lệch mirror.
- Định kỳ khi thêm skill mới / thêm khối mới / đổi thành viên khối.

## Đọc kết quả

- `FAIL` = bắt buộc sửa (thiếu file, frontmatter sai, mirror lệch, mojibake).
- `WARN` = nên sửa (SKILL.md >500 dòng, link hỏng, thiếu invariant, drift).
- `[ok]` theo từng skill trong khối; mục "Khong thuoc khoi nao" liệt kê skill meta/chưa gán.

## Thêm invariant / khối mới

- Thêm khối: tạo `coord-<ten>/SKILL.md` đúng mẫu (có bảng "Khối gồm" + "Definition of Done"),
  cập nhật bảng Block coordinators trong `AGENTS.md`, chạy lại audit để xác nhận.
- Thêm invariant: mở `tools/audit-skills.ps1`, bổ sung vào mục "invariant theo khoi".
  Giữ script **thuần ASCII** (PowerShell 5.1 đọc `.ps1` không BOM thành ANSI sẽ vỡ chuỗi tiếng Việt).
