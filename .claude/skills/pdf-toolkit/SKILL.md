---
name: pdf-toolkit
description: Đọc, trích xuất, tạo và kiểm tra file PDF: lấy text/bảng, render trang ra ảnh, ghép/tách/rotate, điền form, OCR file scan, tạo PDF từ nội dung. Dùng khi người dùng làm việc với PDF, cần trích nội dung PDF, chuyển tài liệu sang PDF, OCR, hoặc nhắc tới pypdf, pdfplumber, PyMuPDF, reportlab.
---

# PDF Toolkit Skill

Mục tiêu: xử lý PDF **chính xác** và kiểm tra được kết quả (đặc biệt trang scan và bảng).

## Khi nào dùng

- Trích text/bảng từ PDF đồ án, tài liệu tham khảo.
- Render trang PDF ra ảnh để kiểm tra/trích dẫn.
- Ghép/tách/xoay/điền form PDF.
- Tạo PDF từ Markdown/HTML/LaTeX.
- OCR PDF scan.

## Toolchain

| Việc | Thư viện | Ghi chú |
|---|---|---|
| Text nhanh + render ảnh + `find_tables()` | **PyMuPDF (`fitz`)** | nhanh nhất; **giấy phép AGPL** — cần license thương mại nếu dùng trong sản phẩm đóng |
| Trích bảng/layout chính xác | **pdfplumber** | MIT, chậm hơn |
| Ghép/tách/xoay/form | **pypdf** | BSD, pure-Python; text yếu |
| OCR | OCRmyPDF / Tesseract / PaddleOCR | cho file scan |
| Tạo PDF | **ReportLab** (code) hoặc **WeasyPrint** (HTML→PDF) | pandoc `--pdf-engine=pdflatex/xelatex/weasyprint` |

```bash
pip install pymupdf pdfplumber pypdf reportlab
```

## Trích xuất

```python
import fitz  # PyMuPDF
doc = fitz.open("input.pdf")
print(doc.page_count)
for page in doc:
    print(page.get_text())

import pdfplumber
with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        for table in page.extract_tables():
            print(table)
```

## Tạo PDF

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("out.pdf", pagesize=A4)
c.drawString(72, 800, "Xin chao")
c.save()
```

Hoặc: `weasyprint input.html output.pdf` (HTML+CSS → PDF, hỗ trợ page-break tốt),
hoặc pandoc (LƯU Ý: pandoc **không** DOCX→PDF trực tiếp, phải qua LaTeX/HTML).

## OCR (file scan)

```bash
ocrmypdf --language vie+eng --deskew input.pdf output.pdf
```

Nếu không cài được OCRmyPDF: dùng `pytesseract` + `pdf2image`.

## RENDER & QA

```bash
python scripts/pdf_to_images.py input.pdf --output_dir render --dpi 150
```

Soi từng trang để phát hiện: text bị cắt, font thay thế, layout lệch, trang trắng, watermark, mất dấu tiếng Việt.

## Pitfalls

- PDF scan cho text rỗng → phải OCR, không kết luận "không có nội dung".
- PyMuPDF là **AGPL** — cảnh báo người dùng nếu ngữ cảnh là sản phẩm đóng.
- Font thiếu trên máy đọc có thể làm lệch extract/render.
- `pypdf` không tốt cho trích text phức tạp — dùng PyMuPDF/pdfplumber.
- Giữ **đúng số trang gốc** khi chỉ trích dẫn; không tự "sửa" nội dung nguồn.

## Format phản hồi cuối

```text
Input: <file.pdf> (<n> trang)
Action: extract | create | merge | ocr | render
Output: <file>
QA: render PASS/FAIL — trang đã soi: N
Notes: <scan? license?>
```
