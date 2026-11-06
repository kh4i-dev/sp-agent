# Pitfalls — skill-feedback

> Bài học do agent đóng góp khi gặp lỗi/biến chứng mà SKILL.md chưa nói đến.
> Quy trình đóng góp: skill `skill-feedback` (xác minh → chống trùng → ghi → cập nhật
> bản đồ lessons-learned → verify + sync). Bài học mức IRON phải được chuyển lên SKILL.md.

## Bẫy đã đóng góp

| Ngày | Mức | Bẫy |
|---|---|---|
| 2026-11-02 | WARN | `audit-skills.ps1` không soi tham chiếu đường dẫn kiểu backtick → ref gãy ẩn thoát qua cổng |
| 2026-11-02 | WARN | Kết quả script audit phải đối chiếu thực địa trước khi kết luận — resolver nửa vời gây báo oan hàng loạt |
| 2026-11-02 | WARN | Tham chiếu tên-trần chéo skill không tự giải mã được khi đọc |
| 2026-11-02 | WARN | Append dòng mới vào `docs/lessons-learned.md` sau heading/đoạn văn → hàng bảng mồ côi |
| 2026-11-02 | WARN | `tools/*.ps1` phải ASCII thuần: powershell.exe 5.1 đọc file không-BOM theo ANSI, em/en dash trong chuỗi decode thành nháy kép (0x93/0x94) → cắt cụt chuỗi, parse error ảo |

### [WARN] audit-skills.ps1 không soi tham chiếu backtick (2026-11-02)
- **Triệu chứng:** check-all PASS 0 FAIL nhưng vẫn còn đường dẫn gãy trong SKILL.md/reference —
  script chỉ kiểm link markdown `[..](..)`, bỏ qua `` `reference/x.md` `` và `` `scripts/x.py` ``.
- **Nguyên nhân:** thiếu lớp kiểm tra; file hứa-mà-chưa-có (lazy file) và ref chéo skill không bị phát hiện.
- **Sửa/phòng:** đã đưa vào `tools/audit-skills.ps1` (mục 2b/2c + 3c, 02/11/2026): soi backtick-ref
  có `/` trong SKILL.md + reference(s)/*.md, skip tên deliverable project-relative, suffix-match chéo skill
  (bằng chứng: audit tay 02/11/2026 tìm ra `skill-feedback/reference/pitfalls.md` chưa tồn tại dù được trỏ 4 lần).
- **Điều kiện tái lập:** thêm ref backtick sai vào SKILL.md → check-all vẫn PASS.

### [WARN] Kết quả audit script ≠ sự thật — phải đối chiếu thực địa (2026-11-02)
- **Triệu chứng:** script tự viết báo 98 "ref gãy"; đối chiếu `Get-ChildItem -Recurse -Filter`
  chứng minh 14/14 script "mất" đều tồn tại (chỉ 1 ref gãy thật).
- **Nguyên nhân:** resolver nửa vời (không tìm xuống `scripts/`, không ghép chéo skill, bắt cả lệnh shell làm path).
- **Sửa/phòng:** trước khi kết luận lỗi, xác nhận bằng lệnh độc lập khác
  (`Get-ChildItem -Recurse -Filter <file> -Path .claude/skills, tools, docs`); phân loại minh-hoạ-vs-thật theo ngữ cảnh câu.
- **Điều kiện tái lập:** mọi lần viết scanner path ad-hoc không test với ca đã biết tồn tại.

### [WARN] Tham chiếu tên-trần chéo skill gây mơ hồ (2026-11-02)
- **Triệu chứng:** SKILL.md của skill A ghi `` `eye_audit.py` `` nhưng file nằm ở
  `use-case-layout/scripts/eye_audit.py` — người đọc (và agent phiên sau) phải đoán vị trí.
- **Nguyên nhân:** viết tắt theo thói quen, không ghi đủ `<skill>/scripts|reference/<file>`.
- **Sửa/phòng:** ghi đường dẫn đầy đủ từ gốc skills, ví dụ
  `use-case-layout/scripts/eye_audit.py`; scanner tương lai mới truy được.
- **Điều kiện tái lập:** grep `` ` ``-refs tên trần trong SKILL.md khối sơ đồ.

### [WARN] lessons-learned.md: append sau heading → hàng bảng mồ côi (2026-11-02)
- **Triệu chứng:** các dòng dạng `| bài học | nằm trong |` đứng sau `###` heading + đoạn văn,
  cách nhau bằng dòng trống, không có header → GFM render thành chữ thô, tra cứu shaky.
- **Nguyên nhân:** thêm entry bằng cách nối cuối file thay vì nối vào bảng có header.
- **Sửa/phòng:** chỉ append vào bảng chính (kết thúc bằng hàng có `---|---`) hoặc tạo
  header mới `| Bài học | Nằm trong |` + `|---|---|` ngay trước cụm dòng mới, bỏ dòng trống giữa các hàng.
- **Điều kiện tái lập:** thêm 1 dòng bản đồ mới khi cuối file đang là heading/đoạn văn.

### [WARN] tools/*.ps1 phải ASCII thuần — powershell.exe 5.1 đọc không-BOM theo ANSI (2026-11-02)
- **Triệu chứng:** thêm chuỗi có em dash `—` vào audit-skills.ps1 → `powershell -File` báo
  parse error ảo ở dòng KHÁC (`Unexpected token 'WARN'`), PSParser dưới pwsh 7 lại báo sạch.
- **Nguyên nhân:** 5.1 decode file không-BOM theo cp1252; byte 0x93/0x94 (đuôi UTF-8 của
  em/en dash) thành nháy kép → cắt cụt chuỗi, lệch toàn bộ cấu trúc phía sau.
- **Sửa/phòng:** giữ `tools/*.ps1` ASCII thuần (`-replace '[^\x00-\x7F]', '-'`) hoặc lưu UTF-8 BOM;
  kiểm bằng `(Get-Content $p -Raw).IndexOf([char]0x2014)`. Bẫy kèm: `HashSet[string]` không có sẵn
  trong 5.1 → dùng `ArrayList` + `Contains` (cẩn thận truthy của `Add` — trả index, 0 = falsy).
- **Điều kiện tái lập:** chèn `—` vào chuỗi double-quoted trong .ps1 không-BOM, chạy bằng powershell.exe.
