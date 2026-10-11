---
name: docx-report
description: Tạo, đọc, audit và chỉnh sửa tài liệu Word (.docx) cho báo cáo/đồ án: heading & numbering, bảng, hình, caption, cross-reference, mục lục (TOC), style, render & kiểm tra trực quan. Dùng khi người dùng yêu cầu viết/sửa/kiểm tra file .docx, báo cáo, đồ án, luận văn, hoặc nhắc tới DOCX, Word, python-docx, OOXML, caption, TOC, render, đồ án môn học.
---

# DOCX Report Skill — Kỹ sư tài liệu Word

Bạn KHÔNG chỉ viết văn xuôi. Bạn phải tạo ra một file `.docx` đúng cấu trúc,
đúng style và ĐÃ ĐƯỢC KIỂM TRA trực quan (render) trước khi giao.

## Khi nào dùng

- Viết / bổ sung / rút gọn nội dung một chương báo cáo.
- Sửa lỗi hình thức: heading sai cấp, caption lệch, bảng vỡ, TOC lệch.
- Audit một file `.docx` có sẵn trước khi nộp.
- Chuẩn hóa font/style cho toàn tài liệu dài.

## Thứ tự ưu tiên (bất biến)

```text
1. Source truth (dữ liệu/sự thật của dự án)
2. Cấu trúc báo cáo được yêu cầu
3. Heading hierarchy
4. Bảng & hình
5. Nhất quán thị giác
6. Render verification
7. Giao file cuối
```

## Source truth — KHÔNG được vi phạm

- Bằng chứng dự án là nguồn chân lý cho tính năng đã triển khai.
- Không biến `PARTIAL` / `NOT_FOUND` thành `IMPLEMENTED`.
- Không bịa kết quả test, không bịa số liệu khảo sát.
- Giữ nguyên thuật ngữ kỹ thuật của dự án.
- Tài liệu tham khảo ngoài chỉ để giải thích chuẩn/công nghệ, không phải sự thật của dự án.

## Toolchain

| Việc | Công cụ | Ghi chú |
|---|---|---|
| Đọc & Audit cấu trúc | `scripts/inspect_docx.py` | Đếm từ, thống kê bảng, hình, liệt kê cây Heading |
| Sửa text & Chuẩn hóa font | `scripts/edit_docx.py` | Tìm/thay thế từ khóa, đặt font/size chuẩn đồ án |
| Tạo mới | `python-docx` | Thư viện chuẩn tạo docx từ Python |
| Render kiểm tra | `scripts/render_docx.py` | Xuất PDF & PNG (tự động nhận Word COM Windows / soffice) |

Cài đặt nhanh:

```bash
pip install python-docx docx-revisions
# Render: tự động nhận Microsoft Word (Windows) hoặc LibreOffice (soffice)
```

> Chi tiết đầy đủ về từng nhóm quy tắc: xem `reference/rules.md`.
> Hệ sinh thái repo/skill DOCX high-star (python-docx-editor, paper-docx, DocxSpec…): `reference/ecosystem.md`.
> Script render: `scripts/render_docx.py`.
> Script sửa DOCX: `scripts/edit_docx.py`.
> Script kiểm tra DOCX: `scripts/inspect_docx.py`.

## Quy trình 3 nhánh

### A. Đọc & Audit (read-only)

```text
Xác định file đầu vào
→ Đọc paragraph/style/heading/table/image
→ Liệt kê cấu trúc heading thực tế
→ Kiểm tra caption hình/bảng
→ Render toàn bộ ra PNG
→ Mở & soi từng trang
→ Ghi nhận lỗi theo nhóm: content / structure / style / layout
```

`python-docx` đọc nhanh cấu trúc:

```python
from docx import Document

doc = Document("report.docx")
for p in doc.paragraphs:
    print(p.style.name, "|", repr(p.text))
for t in doc.tables:
    for row in t.rows:
        print([c.text for c in row.cells])
```

### B. Tạo mới

```text
Đọc rubric / template / style requirement
→ Dựng outline chương
→ Viết bằng python-docx (đặt style chuẩn ngay từ đầu)
→ Thêm bảng → thêm hình → thêm caption → gắn cross-ref
→ Sửa heading level → cập nhật TOC field
→ Style audit → render toàn bộ → visual QA
```

### C. Sửa (patch tối thiểu) — golden workflow

```text
Inspect → Plan → Minimal Edit → Save version mới → Render
        → Inspect PNG → Fix → Render lại → Deliver
```

## Quy tắc patch (bất biến)

- Không rewrite toàn bộ tài liệu nếu chỉ cần sửa một phần.
- Không thay numbering thủ công nếu Word style/field làm được.
- Không resize hình phá aspect ratio.
- Không sửa nội dung bị đánh dấu "evidence" nếu không được yêu cầu.

## Heading & Numbering

```text
Heading 1 = CHƯƠNG / tiêu đề cấp cao
Heading 2 = 1. / 2. / 3.
Heading 3 = 1.1. / 1.2.
Heading 4 = 1.1.1.
```

- Không giả heading bằng chữ đậm + cỡ lớn.
- Không tự gõ số `1.1.1.` nếu hệ thống numbering đã quản lý.
- Không đổi numbering hiện có nếu chưa audit TOC.
- Sau khi sửa, kiểm tra lại Navigation Pane.

## Bảng

- Caption bảng đặt PHÍA TRÊN: `Bảng 3.1. <mô tả>`.
- Header đậm, nền nhẹ, viền rõ nhưng không nặng; body Times New Roman đồng nhất.
- Bảng dài: lặp header row, cho phép ngắt trang, kiểm tra render trang nối tiếp.

## Hình & sơ đồ

- Hình căn giữa, giữ aspect ratio, không làm méo.
- Caption hình đặt NGAY DƯỚI: `Hình 3.1. <mô tả>`.
- Sơ đồ nghiệp vụ (Use Case, Class, Activity, Sequence, State, ERD, kiến trúc):
  dùng **Mermaid/PlantUML** — xem skill `mermaid-diagrams`, KHÔNG chèn ảnh AI.
- Screenshot minh chứng: chụp từ sản phẩm thật, không tạo ảnh giả UI.

## Caption & Cross-reference

```text
Insert caption → tạo field/sequence → bookmark (nếu cần)
→ insert REF tại vị trí tham chiếu → materialize field → render → kiểm tra
```

Không để `Hình 3.4` xuất hiện trước `Hình 3.2`; không tham chiếu tới số không tồn tại.

## TOC & Navigation

Điều kiện: TOC chỉ đúng khi heading hierarchy đúng.

```text
Audit headings → fix styles → update TOC fields → render
→ soi trang TOC → soi Navigation Pane
```

## Style audit & normalize

Checklist:

```text
[ ] Normal = Times New Roman 13
[ ] Heading 1/2/3 nhất quán
[ ] Caption nhất quán
[ ] Table style nhất quán
[ ] Paragraph/line spacing nhất quán
[ ] Không lẫn Calibri/Arial ngoài ý muốn
```

Nguyên tắc: giữ emphasis cần thiết, không xóa style đặc thù của code/hình, không đổi nội dung.
Sau normalize **bắt buộc render lại**.

## Accessibility & Privacy

- Heading hierarchy, alt text, table header, link có nghĩa, không dùng màu làm tín hiệu duy nhất.
- Trước khi phát hành: kiểm tra metadata author, comments, tracked changes, hidden content,
  đường dẫn nội bộ, và **không để lộ secret/API key/mật khẩu**.

## Compare & Regression

Khi sửa lớn (style hàng loạt, đổi template, merge chương):

```text
BASE.docx + NEW.docx → render cả hai → per-page diff → soi trang thay đổi
```

Kiểm tra: không mất nội dung, số trang thay đổi có lý do, hình/caption/bảng/TOC không lệch.

## RENDER & VISUAL QA — shipping gate

> KHÔNG kết luận DOCX hoàn thiện chỉ dựa trên code hoặc text extraction.

```bash
python scripts/render_docx.py report.docx --output_dir render --emit_pdf
```

Mỗi `page-N.png` phải được xem hết để phát hiện: clipping, overlap, bảng vỡ,
thiếu glyph/dấu tiếng Việt, page break sai, caption mồ côi, header/footer sai, hình giãn.

```text
Edit → Render → Inspect → Defect? → (Yes) Fix → Render lại
                                  → (No)  Ship
```

## Format phản hồi cuối

```text
Changed:
- ...

Figures:
- ...
Tables:
- ...

QA:
- Render: PASS/FAIL
- Visual inspection: PASS/FAIL
- Regression: PASS/FAIL

Known limitations:
- ...

Deliverable:
- final.docx
```
