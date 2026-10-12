# DOCX — Quy tắc chi tiết (reference)

Tài liệu tham chiếu đầy đủ cho skill `docx-report`. Đọc khi cần chi tiết từng hạng mục.

## 1. Read & Review (đọc và đánh giá)

Mục tiêu: đọc `.docx` theo cách kiểm chứng được — hiểu cấu trúc, phát hiện heading sai cấp,
phát hiện bảng/hình/caption, kiểm tra layout sau render.

Quy trình bắt buộc:

1. Xác định file đầu vào.
2. Đọc paragraph, style, heading, table, image relationship.
3. Liệt kê cấu trúc heading theo thực tế.
4. Kiểm tra caption hình/bảng.
5. Render DOCX → PNG.
6. Mở và kiểm tra toàn bộ trang.
7. Ghi nhận lỗi theo nhóm: content, structure, style, layout.
8. Chỉ kết luận sau khi render đã được kiểm tra.

Visual QA phải kiểm tra: không cắt chữ, không chồng lấn, không vỡ bảng, caption không bị tách,
font không nhảy, header/footer đúng, page break hợp lý, ký tự tiếng Việt hiển thị đúng.

Không được: suy đoán nội dung bị thiếu; tự đổi nội dung chuyên môn khi chỉ được yêu cầu format;
coi text/XML extraction là bằng chứng layout; giao file trước khi render lại.

Output mong muốn:

```text
READ SUMMARY
STRUCTURE
STYLE ISSUES
FIGURE/TABLE ISSUES
LAYOUT ISSUES
RECOMMENDED PATCHES
FINAL QA RESULT
```

## 1.1. Thất bại kinh điển & Anti-Patterns của AI Agent khi sửa DOCX

Kinh nghiệm thực chiến chứng minh rằng AI agent dù có được nạp prompt hay tài liệu hướng dẫn vẫn liên tục mắc phải các sai lầm có tính hệ thống sau:

| Anti-Pattern (Sai lầm phổ biến) | Cơ chế gây lỗi của AI | Hậu quả thực tế trên bản in Word | Giải pháp kỹ thuật bắt buộc |
|---|---|---|---|
| **1. Ảo tưởng thuộc tính `cell.width`** | Gọi `cell.width = Inches(...)` mà không can thiệp OOXML. | Word hoàn toàn bỏ qua, bảng bị co cụm hoặc tràn lề vì thiếu `<w:tblGrid>`. | Tạo mới `<w:tblGrid><w:gridCol>`, xóa sạch mọi thẻ `<w:tcW>` cũ trước khi ghi thẻ mới. |
| **2. Bệnh tô màu mè (AI Slop Shading)** | Tự tiện tô nền `#EAEAEA` hoặc màu xanh ở header để "làm đẹp". | Vi phạm chuẩn đồ án học thuật Việt Nam (yêu cầu đen trắng tối giản, nền trắng 100%). | Xóa sạch toàn bộ thẻ `<w:shd>` trong bảng, đảm bảo 100% nền trắng trong suốt. |
| **3. Đảo lộn Header và Caption** | Nhầm lẫn ngữ nghĩa giữa tiêu đề cột trong ruột bảng và tên gọi bảng ở dưới đáy. | Header bị biến thành in nghiêng căn giữa, còn caption bị biến thành in đậm căn trái. | Khóa cứng: Header cột = **IN ĐẬM, CĂN TRÁI, KHÔNG NGHIÊNG**; Caption bảng = **IN NGHIÊNG, CĂN GIỮA, KHÔNG ĐẬM** (style `bảng`). |
| **4. Co quắp cột bẻ gãy từ ngữ** | Chia độ rộng cột theo cảm tính, để cột chứa mã/thuật ngữ quá hẹp (< 1.2 in). | Chữ bị ngắt dòng phản cảm: `K23.54` / `801.024`, `VARCHAR(` / `8)`, `O(1` / `)`. | Tính toán tổng độ rộng khuôn in (A4 trừ lề = 6.10 in), cấp tối thiểu 1.4–1.5 in cho cột chuỗi dài. |
| **5. Caption mồ côi & Hàng bị xẻ đôi** | Đặt bảng/hình sát đáy trang mà không lường trước ngắt trang. | Thân bảng ở trang trước, dòng caption rơi trơ trọi sang đầu trang sau; hàng bảng bị cắt đôi ngang lưng. | Luôn bật `<w:cantSplit/>` cho mọi hàng; bật `keep_with_next = True` cho ảnh; chủ động ngắt trang (`add_page_break`) trước bảng nếu ở đáy trang. |
| **6. Ảo tưởng qua text console log** | Thấy Python chạy `exit code 0` là vội vã báo cáo người dùng xong việc. | 90% lỗi vỡ layout, tràn lề, sai font bị bỏ lọt vì terminal không bao giờ báo lỗi dàn trang. | **Bắt buộc Render PDF $\rightarrow$ PNG** và dùng tool xem ảnh soi bằng mắt từng trang trước khi báo cáo. |
| **7. Giả lập Heading thủ công** | Dùng paragraph thường rồi bôi đậm và tăng cỡ chữ Pt(14) để làm tiêu đề. | Word Navigation Pane không nhận diện được mục, Mục lục tự động (TOC) bị trống hoặc nhảy sai trang. | Dùng `doc.add_heading(text, level=N)` và quản lý chuẩn qua Word Styles Gallery. |

## 2. Create & Edit

Nguyên tắc: patch tối thiểu; giữ nội dung & cấu trúc đã có; style nhất quán; có thể rollback;
render sau mỗi batch thay đổi lớn.

Ưu tiên `python-docx` cho paragraph/run/heading/table/image/header-footer/margin/style.
Dùng OOXML trực tiếp (gỡ gói, sửa `word/document.xml`, đóng gói lại) chỉ khi cần:
field, cross-reference, tracked changes, comments, cấu trúc XML đặc biệt.

Định dạng style chuẩn:

```python
from docx.shared import Pt

style = doc.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(13)
```

Mỗi phiên chỉnh sửa phải báo: Changed (file/section/style), Not Changed (protected content),
QA (render passed, pages inspected).

## 2.1. Quy chuẩn Luận văn & Đồ án Học thuật (Academic Thesis Standards)

Tham chiếu theo quy chế Bộ GD&ĐT (Thông tư 23/2021/TT-BGDĐT, 53/2026/TT-BGDĐT) và quy định của các trường ĐH lớn (Bách khoa ĐHQG, ĐHKHTN, UET, CTU, NEU):

### A. Khổ giấy & Căn lề trang (Page Margins)
- **Khổ giấy:** A4 chuẩn (210 x 297 mm), hướng dọc (Portrait).
- **Lề trái (Left):** `3.5 cm` (bắt buộc để chừa khoảng trống đóng gáy sách/dập ghim).
- **Lề phải (Right):** `2.0 cm`.
- **Lề trên (Top):** `3.0 cm` (hoặc 2.5 cm nếu có header).
- **Lề dưới (Bottom):** `3.0 cm` (hoặc 2.5 cm nếu có footer).

### B. Định dạng Văn xuôi & Đoạn văn (Paragraph Typography)
- **Font chữ:** Unicode Times New Roman đồng nhất toàn bài.
- **Cỡ chữ thân bài:** `13 pt` (một số trường cho phép 13–14 pt).
- **Thụt đầu dòng (First line indent):** Bắt buộc thụt vào `1.0 cm – 1.27 cm` (tương đương **1 Tab / 0.5 inch**). Tuyệt đối không dùng phím Spacebar để thụt đầu dòng.
- **Căn lề văn bản:** **Căn đều hai bên (Justify)**. Cấm để căn trái (Left align) gây lởm chởm viền phải.
- **Giãn dòng (Line spacing):** Đặt từ `1.3 lines đến 1.5 lines` (chuẩn khuyến nghị: `1.35 lines`).
- **Giãn đoạn (Paragraph spacing):** Spacing Before `2–3 pt`, Spacing After `4–6 pt`. Cấm nhấn phím Enter 2 lần để tạo khoảng cách giữa các đoạn.
- **Chống dòng mồ côi (Widow/Orphan control):** Bắt buộc bật `widow_control = True` để không có dòng chữ đơn độc ở đầu/cuối trang.

### C. Phân vùng Section & Đánh số trang (Page Numbering)
Sử dụng **Section Break (Next Page)** để chia báo cáo thành 3 phần rõ rệt:
1. **Section 1 — Bìa & Trang bìa phụ:** Không đánh số trang, không header/footer. Khung viền đôi trang trí theo mẫu trường.
2. **Section 2 — Phần đầu (Front Matter):** Lời cam đoan, Lời cảm ơn, Tóm tắt/Abstract, Mục lục, Danh mục hình, Danh mục bảng, Danh mục từ viết tắt.
   - **Đánh số trang La Mã thường (`i, ii, iii, iv...`)**, căn giữa ở chân trang (Footer).
3. **Section 3 — Nội dung chính (Body Matter):** Từ Mở đầu / Chương 1 đến hết Kết luận, Tài liệu tham khảo, Phụ lục.
   - **Đánh số Ả Rập (`1, 2, 3...`)**, bắt đầu lại từ số 1 (`start_type = 1`), căn giữa hoặc góc phải chân trang/đầu trang.

### D. Công thức Toán học & Kỹ thuật (Equations)
- **Trình bày:** Mỗi công thức nằm riêng trên một dòng, **căn giữa (Center)**.
- **Đánh số công thức:** Đánh số theo chương trong dấu ngoặc đơn, đặt **sát lề phải (Right-align)**: `(Chương.Số)`, ví dụ: `(2.1)`, `(3.4)`.
- **Kỹ thuật Word:** Dùng bảng ẩn 1 hàng 2 cột (cột 1 căn giữa chứa công thức, cột 2 căn phải chứa số) hoặc đặt Tab stop giữa + phải.
- **Diễn giải ký hiệu:** Ngay dưới công thức phải giải thích các đại lượng nếu xuất hiện lần đầu: "Trong đó: *x* là...; *y* là...".

### E. Danh mục Từ viết tắt (List of Abbreviations)
- Đặt ngay sau Mục lục / Danh mục bảng biểu.
- Trình bày dạng bảng ẩn viền: Cột 1 (STT), Cột 2 (Từ viết tắt), Cột 3 (Thuật ngữ đầy đủ tiếng Việt / tiếng Anh). Sắp xếp theo thứ tự bảng chữ cái A–Z.
- **Quy tắc trong thân bài:** Lần đầu tiên thuật ngữ xuất hiện phải viết dạng: `Tên đầy đủ (Từ viết tắt)`. Ví dụ: `Cơ sở dữ liệu (CSDL)`. Sau đó mới được dùng từ viết tắt `CSDL`.

### F. Trích dẫn & Danh mục Tài liệu tham khảo (Citations)
- **Chuẩn IEEE (Khối Kỹ thuật & CNTT):** Trích dẫn trong bài bằng số thứ tự trong ngoặc vuông: `[1]`, `[2, 3]`. Danh mục TLTK ở cuối xếp theo đúng thứ tự xuất hiện trong bài.
- **Chuẩn APA / Harvard (Khối Kinh tế & Xã hội):** Trích dẫn bằng `(Tác giả, Năm)`. Danh mục TLTK xếp theo thứ tự bảng chữ cái họ tên tác giả.
- **Nguyên tắc bất biến:** Mọi tài liệu có trích dẫn trong bài phải có tên trong Danh mục TLTK và ngược lại.


## 3. Headings & Numbering

```text
Heading 1 = Chương / tiêu đề cấp cao
Heading 2 = 1. / 2. / 3.
Heading 3 = 1.1. / 1.2.
Heading 4 = 1.1.1.
Heading 5 = chỉ khi thực sự cần
```

Phải xuất được cây:

```text
H1  CHƯƠNG 1...
  H2  1.1...
    H3  1.1.1...
  H2  1.2...
H1  CHƯƠNG 2...
```

Nguyên tắc: không giả heading bằng chữ đậm; không gõ tay `1.1.1` nếu numbering đã quản lý;
không đổi numbering hiện có nếu chưa audit TOC; sau khi sửa phải kiểm tra Navigation Pane.

QA: cấp heading không nhảy; không có Heading 4 nằm trực tiếp dưới Heading 1 khi tài liệu không có cấu trúc đó;
TOC phản ánh đúng hierarchy; số mục không trùng/mất; không có heading rỗng.

## 4. Tables & Style (Bảng biểu học thuật)

> **QUY CHUẨN BẢNG BIỂU HỌC THUẬT BẮT BUỘC:**
> 1. **Màu nền**: **100% TRẮNG TINH (TUYỆT ĐỐI KHÔNG ĐÁNH MÀU)**. Cấm tô màu xám `#EAEAEA`, cấm tô màu xanh hay bất kỳ màu nền nào ở hàng tiêu đề hoặc thân bảng. Tất cả các ô đều giữ màu nền trắng tự nhiên.
> 2. **Dòng tiêu đề cột (Row 0 Header)**:
>    - **IN ĐẬM (`bold=True`)**, **KHÔNG IN NGHIÊNG (`italic=False`)**.
>    - **KHÔNG CĂN GIỮA** (Căn lề trái `LEFT` hoặc căn theo kiểu dữ liệu của cột).
>    - Cỡ chữ: 10.5 – 12pt (tùy số lượng cột để tránh tràn).
>    - Thuộc tính `<w:tblHeader/>` trên `trPr` để tự động lặp lại tiêu đề khi bảng dài sang trang tiếp theo.
> 3. **Tên gọi của bảng / Chú thích (Caption bảng)**:
>    - **ĐẶT Ở CUỐI BẢNG (ngay dưới bảng)**.
>    - **CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA** (`italic=True`, `bold=False`, `alignment=CENTER`).
>    - Cỡ chữ: 12 – 13pt.
>    - Áp dụng Paragraph Style trong Word tên là `bảng` (hoặc `Table Caption`).
>    - Định dạng: `Bảng 3.1: <Tên gọi mô tả nội dung bảng>`.
> 4. **Chống gãy hàng & Khóa layout**:
>    - Mọi hàng (`trPr`) bắt buộc có `<w:cantSplit/>` chống gãy đôi một hàng qua 2 trang.
>    - **Khóa cứng độ rộng từng cột (Table Grid)**: Bắt buộc tái tạo `<w:tblGrid>` chứa `<w:gridCol w:w="{w_dxa}"/>` và dọn sạch `<w:tcW>` cũ trước khi gán thẻ mới để Word không phá layout.
>    - **Khóa bảng với Caption**: Nếu bảng nằm gần cuối trang, người viết phải chủ động ngắt trang (`doc.add_page_break()`) đưa cả bảng sang trang mới, tuyệt đối không để xảy ra tình trạng thân bảng ở cuối trang trước mà dòng Caption rơi mồ côi sang đầu trang sau.

QA Checklist cho Bảng:
```text
[ ] Nền bảng 100% TRẮNG TINH (không có màu xám/xanh ở bất kỳ ô nào)
[ ] Header hàng 0: IN ĐẬM, KHÔNG CĂN GIỮA, không nghiêng
[ ] Caption đặt ở CUỐI BẢNG (ngay dưới bảng)
[ ] Caption: CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA (style 'bảng')
[ ] Độ rộng cột khóa cứng bằng tblGrid (không vỡ chữ, không ngắt từ dị dạng)
[ ] Lặp header khi sang trang (tblHeader)
[ ] Không gãy hàng ngang trang (cantSplit)
[ ] Caption không bị trôi đơn độc sang trang tiếp theo
```

## 5. Figures & Images (Hình ảnh & Sơ đồ)

> **QUY CHUẨN HÌNH ẢNH HỌC THUẬT BẮT BUỘC:**
> 1. **Căn lề**: Hình ảnh **CĂN GIỮA (Center)**, giữ đúng tỷ lệ khung hình (Aspect Ratio), không bóp méo hình ảnh.
> 2. **Khóa hình với chú thích (`keep_with_next`)**: Paragraph chứa hình BẮT BUỘC phải bật thuộc tính `keep_with_next = True` để Word khóa cứng ảnh và dòng chú thích trên cùng một trang, ngăn chặn tuyệt đối lỗi hình ở trang trước còn chú thích rớt sang trang sau.
> 3. **Tên gọi / Chú thích hình (Figure Caption)**:
>    - **ĐẶT NGAY DƯỚI HÌNH**.
>    - **CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA** (`italic=True`, `bold=False`, `alignment=CENTER`).
>    - Cỡ chữ: 11 – 12pt.
>    - Áp dụng Paragraph Style trong Word tên là `hình` (hoặc `Figure Caption`).
>    - Định dạng: `Hình 3.1: <Tên gọi mô tả nội dung hình>`.
> 4. **Nguồn gốc hình ảnh**: Screenshot phải chụp trực tiếp từ sản phẩm/phần mềm thực tế; Sơ đồ kiến trúc/UML phải sinh từ Mermaid/PlantUML (xem skill `mermaid-diagrams`), tuyệt đối không dùng ảnh AI ảo không đúng sự thật.

QA Checklist cho Hình ảnh:
```text
[ ] Ảnh căn giữa, không méo hình
[ ] Paragraph ảnh có keep_with_next = True
[ ] Caption nằm NGAY DƯỚI HÌNH
[ ] Caption: CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA (style 'hình')
[ ] Ảnh và caption luôn nằm trọn trên cùng một trang
[ ] Text trong ảnh rõ nét, đọc được rõ ràng
```

### 5.1. Thay thế hình ảnh In-place (Non-destructive Image Swapping)

Khi một tài liệu Word đã được con người chỉnh sửa, định dạng hoàn hảo, **tuyệt đối không dùng code tạo lại từ đầu (re-generate) khiến tài liệu bị ghi đè mất hết các định dạng thủ công**.
Bắt buộc dùng cơ chế **In-place ZIP Binary Swap** (`scripts/replace_docx_images.py`):
1. **Liệt kê hình ảnh hiện hữu:**
   `python scripts/replace_docx_images.py document.docx --list`
2. **Thay thế ảnh đơn lẻ:**
   `python scripts/replace_docx_images.py document.docx --figure "Hình 3.2" --new "new_diagram.png"`
3. **Thay thế hàng loạt bằng mapping:**
   `python scripts/replace_docx_images.py document.docx --mapping mapping.json`
4. **Cơ chế:** Ghi đè nhị phân trực tiếp vào `word/media/imageX.png` bên trong ZIP OOXML, tính toán lại tỷ lệ `wp:extent` để ảnh mới không bị méo, giữ nguyên 100% tất cả các đoạn văn, bảng biểu, headers/footers và mục lục của tài liệu.

## 6. Captions & Cross References

Quản lý số thực tế và tham chiếu cho hình, bảng, mục nội bộ. Không dùng text thủ công cho số thực tế
nếu Word field xử lý được.

Luồng: Insert caption → tạo field/sequence → bookmark nếu cần → insert REF tại vị trí tham chiếu
→ materialize field → render → kiểm tra.

Khi thêm/xóa hình: cập nhật field, kiểm tra numbering, kiểm tra các câu "theo Hình 3.1", "xem Bảng 3.2", render lại.

Không được: để `Hình 3.4` xuất hiện trước `Hình 3.2`; tham chiếu tới số không tồn tại; caption và hình cách xa nhau.

## 7. TOC & Navigation

TOC và Danh mục hình/bảng được tạo tự động bằng OOXML Field Codes, không gõ tay:
- **Mục lục (TOC 1-3):** `<w:fldSimple w:instr="TOC \o &quot;1-3&quot; \h \z \u"/>`
- **Danh mục hình (TOF):** `<w:fldSimple w:instr="TOC \c &quot;Hình&quot; \h \z"/>`
- **Danh mục bảng (TOT):** `<w:fldSimple w:instr="TOC \c &quot;Bảng&quot; \h \z"/>`

Dùng lệnh tự động:
```bash
python scripts/edit_docx.py report.docx --add-toc --add-tof --add-tot
```

Luồng cập nhật và hiển thị:
```text
Audit headings → fix styles → chèn field codes → render (Word COM / soffice tự tính số trang)
→ soi trang TOC → soi Navigation Pane
```

Kiểm tra: tên chương đúng; cấp mục đúng; số trang đúng sau render; không xuất hiện đoạn văn body trong TOC;
không mất mục con; không có tiêu đề nằm ngoài TOC do dùng sai style.


## 8. Render & Visual Verification (Bắt buộc kiểm tra trực quan bằng ảnh)

> **THIẾT LUẬT BẤT BIẾN (IRON RULE):**
> 1. Tuyệt đối không kết luận DOCX hoàn thiện hoặc báo cáo người dùng chỉ dựa trên code hoặc text extraction.
> 2. Bắt buộc convert DOCX sang PDF rồi render từng trang sang ảnh PNG độ nét cao (PyMuPDF / fitz, DPI 150–200).
> 3. Agent BẮT BUỘC phải mở và soi từng file ảnh (`page-N.png`) qua tool xem ảnh để đối soát trực quan:
>    - Bảng: Nền trắng 100%, header in đậm không căn giữa, không có màu xám/xanh.
>    - Caption bảng: Nằm ở cuối bảng, chữ thường in nghiêng, căn giữa (style `bảng`).
>    - Hình ảnh: Căn giữa, có `keep_with_next=True`, caption nằm dưới hình, in nghiêng căn giữa (style `hình`).
>    - Ngắt trang: Bảng và hình không bị rớt caption mồ côi sang trang sau; hàng bảng không bị gãy đôi.
>    - Độ rộng cột: Khóa cứng bằng `tblGrid`, chữ không bị ngắt từ dị dạng (`VARCHAR(` / `8)`).
> 4. Chỉ khi 100% trang ảnh đạt yêu cầu thị giác mới được phát hành hoặc bàn giao cho người dùng.

```bash
python scripts/render_docx.py input.docx --output_dir render --emit_pdf --dpi 150
```

Vòng lặp chuẩn: `Edit → Render PDF → Render PNG → Soi từng ảnh PNG → Có lỗi? Sửa → Render lại | Hết lỗi? Hoàn tất`.

## 9. Style Audit & Normalization

Audit: font, font size, paragraph spacing, line spacing, heading styles, direct formatting, table style, caption style.

Nguyên tắc normalize: không phá emphasis cần thiết; không xóa style đặc biệt của code/hình; không thay nội dung.

Checklist:

```text
[ ] Normal = Times New Roman 13
[ ] Heading 1 nhất quán
[ ] Heading 2 nhất quán
[ ] Heading 3 nhất quán
[ ] Caption nhất quán
[ ] Table style nhất quán
[ ] Paragraph spacing nhất quán
[ ] Không lẫn Calibri/Arial ngoài ý muốn
```

Sau normalize bắt buộc render lại.

## 10. Accessibility & Privacy

Accessibility: kiểm tra heading hierarchy, alt text cho hình quan trọng, table header, link có nghĩa,
không dùng màu làm tín hiệu duy nhất.

Privacy (trước khi phát hành): kiểm tra metadata author, comments, tracked changes, hidden content,
đường dẫn nội bộ trong document, và secrets/password/API key không xuất hiện.

Nếu cần scrub: Audit → xác định metadata nhạy cảm → scrub → render → kiểm tra lại.

Không được: xóa evidence nghiệp vụ chỉ vì nó chứa tên file; tự công khai credential demo; đưa secret vào báo cáo.

## 11. Compare & Regression

Dùng khi: chỉnh style hàng loạt, sửa heading, đổi template, merge chương, sửa nhiều bảng/hình.

```text
BASE.docx + NEW.docx → Render both → Per-page diff → Inspect changed pages
```

Kiểm tra: nội dung không mất; số trang thay đổi có lý do; hình không biến mất; caption không đổi sai;
bảng không vỡ; TOC không lệch.

Output: `Structural changes / Visual changes / Unexpected regressions / Approved or Rejected`.

## 12. Pitfalls công cụ (từ nghiên cứu)

- `python-docx` KHÔNG hỗ trợ tracked changes và có thể nuốt `w:ins`/`w:del` khi lưu; khi lưu chỉ ghi lại một phần các OOXML part (có thể mất printSettings/customXml). Sửa revision nên dùng OOXML trực tiếp hoặc `docx-revisions`.
- Nhiều tiến trình `soffice` chạy song song dùng chung profile sẽ im lặng không tạo output (exit 1). Luôn truyền `-env:UserInstallation=file:///<profile riêng>` (script render đã xử lý).
- `docx2pdf` chỉ chạy trên máy có Microsoft Word (COM/JXA).
- `pandoc` KHÔNG chuyển DOCX → PDF trực tiếp; phải qua LaTeX/HTML.
- Font thiếu trên máy render sẽ bị thay thế âm thầm và làm lệch layout.
