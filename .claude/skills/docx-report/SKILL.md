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
| Chuẩn hóa học thuật & Style | `scripts/edit_docx.py` | Áp dụng `--academic-format`: thụt lề 1 tab (1.27cm), căn đều 2 bên, lề giấy 3.5cm, style bảng & caption, chèn TOC/TOF/TOT |
| **Thay ảnh siêu tốc (Non-destructive)** | `scripts/replace_docx_images.py` | **Thay thế ảnh trực tiếp vào ZIP OOXML, bảo toàn 100% định dạng, style, bảng biểu của file Word đã sửa đẹp** |
| Tạo mới | `python-docx` | Thư viện chuẩn tạo docx từ Python |
| Render kiểm tra | `scripts/render_docx.py` | Xuất PDF & PNG (tự động nhận Word COM Windows / soffice) |


Cài đặt nhanh:

```bash
pip install python-docx docx-revisions Pillow
# Render: tự động nhận Microsoft Word (Windows) hoặc LibreOffice (soffice)
```

> Chi tiết đầy đủ về từng nhóm quy tắc: xem `reference/rules.md`.
> Hệ sinh thái repo/skill DOCX high-star (python-docx-editor, paper-docx, DocxSpec…): `reference/ecosystem.md`.
> Script thay ảnh nhanh: `scripts/replace_docx_images.py`.
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

## 7 Cạm bẫy & Bài học xương máu khi sửa DOCX (AI Anti-Patterns)

Mọi agent khi làm việc với file Word PHẢI KHẮC CỐT GHI TÂM 7 thất bại kinh điển sau:

1. **Bẫy Ảo tưởng Thư viện (`cell.width` Abstraction Trap)**:
   - *Sai lầm:* Gán `cell.width = ...` trong Python rồi tưởng Word sẽ hiển thị đúng.
   - *Thực tế:* Word hoàn toàn phớt lờ nếu thiếu `<w:tblGrid>` và sẽ ưu tiên thẻ `<w:tcW>` cũ.
   - *Giải pháp:* Bắt buộc xóa `tblGrid` cũ, tạo mới `<w:gridCol>`, và dọn sạch mọi thẻ `<w:tcW>` cũ trước khi gán mới.
2. **Bẫy Tô màu mè (AI Slop Shading)**:
   - *Sai lầm:* Tự ý tô màu xám nhẹ `#EAEAEA` hay màu xanh pastel ở hàng tiêu đề để "trông cho đẹp".
   - *Thực tế:* Chuẩn học thuật/đồ án Việt Nam yêu cầu **100% NỀN TRẮNG TINH**. Càng tô màu càng lộ rõ văn bản do AI sinh ra.
   - *Giải pháp:* Xóa toàn bộ thẻ `<w:shd>` trong toàn bộ bảng.
3. **Bẫy Đảo lộn Header và Caption (Semantic Inversion)**:
   - *Sai lầm:* Nhầm lẫn giữa Header trong ruột bảng và Caption tên bảng ở ngoài.
   - *Thực tế:*
     - **Header cột (trong bảng, hàng 0)**: **IN ĐẬM, KHÔNG CĂN GIỮA (CĂN TRÁI), KHÔNG NGHIÊNG**.
     - **Caption tên bảng (dưới đáy bảng)**: **CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA** (style `bảng`).
4. **Bẫy Co quắp cột làm bẻ gãy từ ngữ (Ugly Word Breaking)**:
   - *Sai lầm:* Chia cột theo cảm tính, để cột chứa mã định danh hoặc công thức quá hẹp (< 1.2 inch).
   - *Thực tế:* Word bẻ gãy từ ngữ thành nhiều dòng dị dạng (`K23.54` xuống dòng `801.024` hay `VARCHAR(` xuống dòng `8)`).
   - *Giải pháp:* Tính toán tổng độ rộng (khuôn in A4 là 6.10 inches), ưu tiên cột chuỗi ký tự dài tối thiểu 1.4 – 1.5 inches, nén các cột số liệu ngắn (0.7 – 0.8 inches).
5. **Bẫy Chú thích mồ côi & Gãy đôi hàng (Orphan Captions & Split Rows)**:
   - *Sai lầm:* Đặt bảng hoặc hình sát đáy trang mà không lường trước ngắt trang.
   - *Thực tế:* Thân bảng ở trang trước, nhưng dòng Caption văng sang đầu trang sau; hoặc 1 hàng bảng bị cắt ngang lưng làm đôi.
   - *Giải pháp:* Luôn bật `<w:cantSplit/>` cho mọi hàng bảng; bật `keep_with_next = True` cho ảnh; chủ động thêm `doc.add_page_break()` trước các bảng dài gần cuối trang.
6. **Bẫy "Ảo tưởng hoàn thành" qua text log (Blind Console Deception)**:
   - *Sai lầm:* Thấy script Python chạy ra `exit code 0` là vội vàng tin rằng file đã hoàn hảo và báo cáo người dùng.
   - *Thực tế:* 90% lỗi vỡ bảng, lệch lề, mất font chỉ hiện ra trên trang render thực tế.
   - *Giải pháp:* **BẮT BUỘC RENDER PDF $\rightarrow$ PNG VÀ DÙNG TOOL XEM ẢNH SOI TỪNG TRANG**.
7. **Bẫy Giả lập Heading bằng định dạng thủ công (Fake Headings)**:
   - *Sai lầm:* Dùng paragraph thường rồi bôi đậm và tăng cỡ chữ để làm tiêu đề.
   - *Thực tế:* Navigation Pane bị trống, Mục lục tự động (TOC) nhảy sai trang hoặc không cập nhật được.
   - *Giải pháp:* Bắt buộc dùng `doc.add_heading(text, level=N)` và áp dụng đúng Heading Styles chuẩn của Word.

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

## Bảng biểu (Tables) — Chuẩn học thuật bất biến

> **QUY TẮC BẢNG CHUẨN:**
> 1. **Nền bảng**: **100% TRẮNG TINH (KHÔNG ĐÁNH MÀU)**. Tuyệt đối không tô xám `#EAEAEA`, không tô xanh, không viền rườm rà. Nền mọi ô (kể cả hàng tiêu đề) luôn là màu trắng / trong suốt.
> 2. **Tiêu đề cột (Header row 0)**: **IN ĐẬM (`bold=True`)**, **KHÔNG CĂN GIỮA** (căn lề trái `LEFT` hoặc căn theo kiểu dữ liệu), **KHÔNG IN NGHIÊNG**. Cỡ chữ 10.5–12pt. Bắt buộc có thuộc tính `<w:tblHeader/>` để tự động lặp lại khi sang trang.
> 3. **Tên gọi của bảng / Chú thích (Caption)**: **ĐẶT Ở CUỐI BẢNG (ngay dưới bảng)**. **CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA** (`italic=True`, `bold=False`, `alignment=CENTER`). Cỡ chữ 12–13pt. Sử dụng paragraph style riêng tên là `bảng` (hoặc `Table Caption`).
> 4. **Khóa chống gãy hàng**: Mọi hàng (`trPr`) bắt buộc có `<w:cantSplit/>`.
> 5. **Khóa cứng độ rộng cột (OOXML Table Grid)**: Tránh lỗi Word tự co dãn gây vỡ chữ, bắt buộc tái tạo `<w:tblGrid>` chứa `<w:gridCol w:w="..."/>` và dọn sạch `<w:tcW>` cũ trước khi gán mới.

Mẫu Python-docx chuẩn hóa bảng học thuật:
```python
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

def format_academic_table(table, col_widths, font_size_pt=11):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.allow_autofit = False

    # 1. Khóa cứng độ rộng bằng tblGrid
    tblGrid = table._tbl.find(qn('w:tblGrid'))
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    tblGrid = OxmlElement('w:tblGrid')
    for w in col_widths:
        col = OxmlElement('w:gridCol')
        col.set(qn('w:w'), str(int(w.inches * 1440)))
        tblGrid.append(col)
    tblPr = table._tbl.tblPr
    table._tbl.insert(table._tbl.index(tblPr) + 1, tblGrid)

    # 2. Lặp lại header hàng 0 khi sang trang
    if len(table.rows) > 0:
        hdr_trPr = table.rows[0]._tr.get_or_add_trPr()
        hdr_trPr.append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

    # 3. Chống gãy hàng & định dạng ô (NỀN TRẮNG 100%)
    for row_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(r'<w:cantSplit xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
        for col_idx, cell in enumerate(row.cells):
            if col_idx < len(col_widths):
                w = col_widths[col_idx]
                w_dxa = int(w.inches * 1440)
                tcPr = cell._tc.get_or_add_tcPr()
                for old_w in tcPr.findall(qn('w:tcW')):
                    tcPr.remove(old_w)
                tcPr.append(parse_xml(f'<w:tcW xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:w="{w_dxa}" w:type="dxa"/>'))
                # XÓA BỎ MỌI SHADING: Nền trắng tinh
                for old_shd in tcPr.findall(qn('w:shd')):
                    tcPr.remove(old_shd)

            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                if row_idx == 0:
                    # Tiêu đề cột: IN ĐẬM, KHÔNG CĂN GIỮA (căn trái), KHÔNG NGHIÊNG
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for r in p.runs:
                        r.font.bold = True
                        r.font.italic = False
                        r.font.size = Pt(font_size_pt)
                        r.font.color.rgb = RGBColor(0, 0, 0)
                else:
                    for r in p.runs:
                        r.font.size = Pt(font_size_pt)
                        r.font.color.rgb = RGBColor(0, 0, 0)

def add_table_caption(doc, text):
    """Caption ở CUỐI BẢNG: chữ thường in nghiêng, căn giữa, style 'bảng'"""
    try:
        bang_style = doc.styles.add_style('bảng', docx.enum.style.WD_STYLE_TYPE.PARAGRAPH)
    except Exception:
        bang_style = doc.styles['bảng']
    bang_style.font.name = 'Times New Roman'
    bang_style.font.size = Pt(12)
    bang_style.font.bold = False
    bang_style.font.italic = True
    bang_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bang_style.paragraph_format.space_before = Pt(4)
    bang_style.paragraph_format.space_after = Pt(12)

    p = doc.add_paragraph(text, style='bảng')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p
```

## Hình ảnh & Sơ đồ (Figures)

> **QUY TẮC HÌNH ẢNH CHUẨN:**
> 1. **Căn lề**: Hình ảnh **CĂN GIỮA (Center)**.
> 2. **Khóa hình với chú thích (`keep_with_next`)**: Paragraph chứa hình BẮT BUỘC phải bật `p.paragraph_format.keep_with_next = True` để Word không bao giờ tách hình ở trang trước còn chú thích rơi xuống trang sau.
> 3. **Tên gọi / Chú thích hình (Figure Caption)**: Đặt ở **DƯỚI HÌNH**, **CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA** (`italic=True`, `bold=False`, `alignment=CENTER`), cỡ chữ 11–12pt. Dùng paragraph style riêng tên là `hình` (hoặc `Figure Caption`).
> 4. **Giữ nguyên tỷ lệ (Aspect Ratio)**: Không bóp méo hình ngang/dọc; screenshot phải chụp từ sản phẩm thật, sơ đồ xuất từ Mermaid/PlantUML (xem skill `mermaid-diagrams`).

Mẫu Python-docx chuẩn hóa hình ảnh & caption:
```python
def add_figure_with_caption(doc, img_path, caption_text, width_inches=6.0):
    # 1. Paragraph chứa ảnh (căn giữa + khóa chặt với caption)
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True  # KHÓA HÌNH VÀ CHÚ THÍCH TRÊN CÙNG TRANG
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inches))

    # 2. Paragraph caption (style 'hình', in nghiêng, căn giữa, chữ thường)
    try:
        hinh_style = doc.styles.add_style('hình', docx.enum.style.WD_STYLE_TYPE.PARAGRAPH)
    except Exception:
        hinh_style = doc.styles['hình']
    hinh_style.font.name = 'Times New Roman'
    hinh_style.font.size = Pt(11)
    hinh_style.font.bold = False
    hinh_style.font.italic = True
    hinh_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_cap = doc.add_paragraph(caption_text, style='hình')
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    return p_img, p_cap
```

### Thay thế ảnh siêu tốc cho file Word có sẵn (In-place Image Replacement)
Khi tài liệu Word đã được người dùng chỉnh sửa, căn lề và định dạng đẹp, **TUYỆT ĐỐI KHÔNG dùng code tạo lại từ đầu (bộ gen cũ) gây phá hủy style của người dùng**. Thay vào đó, dùng `scripts/replace_docx_images.py` để thay trực tiếp nhị phân vào gói ZIP OOXML:

```bash
# 1. Liệt kê toàn bộ ảnh kèm Caption trong file Word:
python scripts/replace_docx_images.py report.docx --list

# 2. Thay thế 1 ảnh theo tên Caption (hoặc số hiệu hình):
python scripts/replace_docx_images.py report.docx --figure "Hình 3.2" --new "new_image.png"

# 3. Thay thế 1 ảnh theo tên media gốc trong Word:
python scripts/replace_docx_images.py report.docx --target "image4.png" --new "new_image.png"

# 4. Thay hàng loạt theo file JSON mapping:
python scripts/replace_docx_images.py report.docx --mapping map.json
# (Nội dung map.json: {"Hình 3.2": "new_mssv.png", "image10.png": "new_search.png"})
```
*Tác dụng:* Bảo toàn 100% định dạng trang, kiểu bảng biểu, heading, mục lục và tự động hiệu chỉnh `wp:extent` để không bị méo ảnh mới.

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

Checklist chuẩn hóa Luận văn / Đồ án học thuật:

```text
[ ] Khổ giấy A4, Lề trang: Trái 3.5 cm (đóng gáy), Phải 2.0 cm, Trên 3.0 cm, Dưới 3.0 cm.
[ ] Văn xuôi: Times New Roman 13 pt, Căn đều hai bên (Justify).
[ ] Thụt đầu dòng đoạn văn: 1.0 cm – 1.27 cm (1 tab / 0.5 inch), cấm dùng phím cách.
[ ] Giãn dòng: 1.3 – 1.5 lines (khuyến nghị 1.35x); Giãn đoạn Before 2pt / After 4pt.
[ ] Chống dòng mồ côi (Widow/Orphan control) đã được bật.
[ ] Heading 1 ngắt trang mới; Heading 2/3/4 không bị mồ côi (keep_with_next).
[ ] BẢNG: Nền trắng 100% (không tô màu), Tiêu đề cột IN ĐẬM, KHÔNG căn giữa; lặp header (tblHeader); chống gãy hàng (cantSplit).
[ ] CAPTION BẢNG: Đặt ở CUỐI BẢNG (ngay dưới bảng), cỡ 12–13pt, chữ thường in nghiêng, CĂN GIỮA (style 'bảng').
[ ] HÌNH ẢNH: Căn giữa, keep_with_next = True; Caption đặt NGAY DƯỚI, chữ thường in nghiêng, CĂN GIỮA (style 'hình').
[ ] Công thức toán: Căn giữa, số thứ tự (Chương.Số) căn sát lề phải.
[ ] Đánh số trang: Phần đầu số La Mã (i, ii, iii...); Thân bài từ Chương 1 số Ả Rập (1, 2, 3...).
[ ] Không lẫn Calibri/Arial ngoài ý muốn.
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

## RENDER & VISUAL QA — BẮT BUỘC KIỂM TRA TRỰC QUAN BẰNG ẢNH (IRON RULE)

> **CẤM TUYỆT ĐỐI**:
> - CẤM kết luận DOCX hoàn thiện hoặc báo cáo hoàn thành chỉ dựa trên code Python hay text log extraction!
> - CẤM audit suông không có bằng chứng ảnh chụp thật từ trang tài liệu!

### Pipeline Render Bắt buộc:
```bash
# 1. Convert DOCX -> PDF -> PNG từng trang độ phân giải cao
python scripts/render_docx.py report.docx --output_dir render --emit_pdf --dpi 150
```

### Visual Verification Loop (Soi từng trang PNG qua tool xem ảnh):
Agent **BẮT BUỘC** phải gọi công cụ xem ảnh (`view_file` trên các file `render/page-N.png`) để kiểm tra bằng mắt từng trang theo Checklist:
1. **Kiểm tra Header bảng**: Bắt buộc **IN ĐẬM**, **KHÔNG CĂN GIỮA** (căn trái), **NỀN TRẮNG 100%** (không có bất kỳ ô nào bị tô màu xám `#EAEAEA` hay màu xanh).
2. **Kiểm tra Caption bảng**: Bắt buộc nằm ở **CUỐI BẢNG (ngay dưới bảng)**, **CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA** (style `bảng`).
3. **Kiểm tra chống gãy bảng & mồ côi caption**:
   - Bảng không bị cắt ngang hàng xấu xí.
   - Tuyệt đối không để xảy ra lỗi: Bảng nằm cuối trang trước mà dòng Caption bị rớt sang đầu trang sau (nếu gặp phải ngắt trang chủ động `doc.add_page_break()` trước bảng).
4. **Kiểm tra Hình ảnh & Caption hình**:
   - Hình ảnh căn giữa trang.
   - Đoạn ảnh có `keep_with_next = True` chống tách rời chú thích.
   - Caption hình nằm **NGAY DƯỚI HÌNH**, **CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA** (style `hình`).
5. **Kiểm tra co dãn cột**: Chữ trong bảng không bị ngắt từ dị hợm do cột quá hẹp (ví dụ: `VARCHAR(` / `8)` hay số hiệu bị tách đôi).
6. **Kiểm tra Font & Lề**: Toàn bộ Times New Roman đồng nhất, thụt đầu dòng 1 tab (1.27 cm), căn đều 2 bên (Justify), lề gáy 3.5 cm không bị lẹm.

```text
[Code/Edit DOCX] ──> [Render PDF] ──> [Render PNG pages] ──> [View từng trang PNG]
                                                                     │
                         ┌───────────────────────────────────────────┴──────────────────────┐
                         ▼                                                                  ▼
                   [Có lỗi trực quan]                                              [100% Hoàn hảo]
                         │                                                                  │
              [Sửa code & layout] ──> (Render lại)                                    [Báo cáo giao file]
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
