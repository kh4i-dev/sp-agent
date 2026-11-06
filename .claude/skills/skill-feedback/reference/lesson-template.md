# Lesson/Pitfall Templates — bản mẫu khi đóng góp bài học vào skill

Bản mẫu cho 2 nơi ghi: (A) file `reference/pitfalls.md` của một skill, (B) entry rút gọn chèn vào `SKILL.md`.

## A. Header chuẩn cho `reference/pitfalls.md` (tạo mới khi chưa có)

```markdown
# Pitfalls — <tên-skill>

> Bài học do agent đóng góp khi gặp lỗi/biến chứng mà SKILL.md chưa nói đến.
> Quy trình đóng góp: skill `skill-feedback` (xác minh → chống trùng → ghi → cập nhật
> bản đồ lessons-learned → verify + sync). Bài học mức IRON phải được chuyển lên SKILL.md.

## Bẫy đã đóng góp

| Ngày | Mức | Bẫy |
|---|---|---|
| (bảng này cập nhật khi thêm entry — 1 dòng/entry) |
```

## B. Entry đầy đủ (cho `reference/pitfalls.md`)

```markdown
### [WARN] COM render Word không update field (2026-10-27)
- **Triệu chứng:** Xuất PDF bằng Word COM nhưng TOC/số trang hiện giá trị cũ.
- **Nguyên nhân:** COM không tự chạy `Fields.Update()` khi SaveAs.
- **Sửa/phòng:** Gọi `Fields.Update()` trên từng story trước SaveAs
  (bằng chứng: `python render_docx.py a.docx` → PDF trang 1 hiện đúng TOC).
- **Điều kiện tái lập:** .docx có TOC/SEQ field + render bằng COM.
```

Quy ước:
- Tiêu đề: `[MỨC]` + tên bẫy ngắn, dễ grep; ngày mở đầu entry theo `YYYY-MM-DD`.
- Chỉ dùng mục ở trên; không thêm mục trống; **≤ 12 dòng**.
- `[UNVERIFIED]` (nếu chưa xác minh) ghi ở tiêu đề, kèm "Cần kiểm: <điều kiện>".

## C. Entry rút gọn (chèn vào mục bẫy của `SKILL.md`)

```markdown
- **<tên bẫy>** — <triệu chứng 1 câu>; phòng: <cách sửa 1 câu> (`<lệnh>`)
```

## D. Ví dụ tốt vs xấu

Tốt:
```markdown
### [WARN] Regex raw-string chứa \u gây lỗi escape (2026-10-27)
- **Triệu chứng:** `re.compile(r"\u00e0")` khớp sai chuỗi có dấu tiếng Việt.
- **Nguyên nhân:** raw-string khiến `\u` không được Python xử lý như escape Unicode.
- **Sửa/phòng:** Viết trực tiếp ký tự Unicode vào regex (`r"à"`).
- **Điều kiện tái lập:** regex chứa `\uXXXX` trong raw-string.
```

Xấu (cấm ghi kiểu này):
```markdown
### [WARN] Regex khó dùng (2026-10-27)
- Regex với tiếng Việt hay bị sai, nhớ cẩn thận.
```
(Không có lệnh, không có nguyên nhân, không sửa được — người đọc vẫn phải mò lại từ đầu.)
