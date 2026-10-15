---
name: safe-docx-modifier
description: Chỉnh sửa an toàn file Word (.docx) ở giai đoạn hoàn thiện mà KHÔNG sinh lại từ đầu (Zero Regeneration). Thay ảnh nhị phân in-place (ZIP Swap) tự tính tỷ lệ aspect ratio, thay thế văn bản bảo toàn Runs/Formatting XML, chèn đoạn văn/bảng mới tại mốc neo (anchor), tự động backup .bak_safe và kiểm định toàn vẹn XML. Dùng khi file Word đã căn chỉnh đẹp cần thay ảnh, sửa thông tin, đổi MSSV/tên/lớp, thêm nội dung mà không được làm vỡ format.
---

# Safe DOCX Modifier — Chỉnh sửa Word An toàn (Zero Regeneration)

Kỹ năng chuyên dụng dành cho **giai đoạn hoàn thiện tài liệu Word (.docx)**. Khi người dùng đã dành thời gian căn chỉnh thủ công lề trang (margins), font chữ, tiêu đề, mục lục (TOC), giãn dòng, thụt lề tab và viền bảng biểu, **tuyệt đối KHÔNG ĐƯỢC sinh lại file từ đầu** (bằng `python-docx` hay `pandoc`). Bất kỳ hành động tạo lại nào cũng sẽ phá hủy 100% công sức căn chỉnh của người dùng.

Skill này cung cấp cơ chế **phẫu thuật vi mô in-place (Micro In-Place Surgical Patching)** trực tiếp trên cấu trúc OpenXML (ZIP OOXML) của tệp Word.

---

## 1. Triết lý Cốt lõi & Bộ 5 Nguyên tắc Vàng (SOP)

```text
1. INSPECT FIRST     : Đọc cấu trúc DOM/XML, xác định phạm vi trước khi động vào file.
2. MINIMAL PATCH     : Sửa tối thiểu, phẫu thuật vi mô, bảo vệ 100% nội dung ngoài phạm vi.
3. FAIL ON AMBIGUITY : Dừng ngay nếu có nhiều hơn 1 kết quả khớp hoặc không đủ căn cứ suy luận.
4. RENDER & VERIFY   : doc.save() chưa phải là xong; phải mở lại kiểm tra cú pháp và render soi trang.
5. REPORT EVIDENCE   : Báo cáo rõ ràng: Sửa cái gì? Vì sao sửa? Kiểm định bằng chứng ra sao?
```

---

## 2. Kinh nghiệm Xương máu khi Sửa Word bằng Code (Lessons Learned)

### Bài học 1: Đọc được nội dung không có nghĩa là hiểu được tài liệu
File DOCX không đơn thuần là một tệp văn bản thô. Bên trong nó gồm nhiều thành phần độc lập:
- Đoạn văn, từng phần định dạng ký tự (`<w:r>`), kiểu tiêu đề (`Heading`).
- Bảng biểu, khung hình, chú thích và công thức toán học (`OMML`).
- Đầu trang (`Header`), chân trang (`Footer`), số trang và các trường tự động (`Field Code`).
- Phân đoạn trang (`Section Break`), ngắt trang và bảng mục lục (`TOC`).
- Khung văn bản đồ họa (`w:txbxContent` trong TextBox/Shape).

Khi Python đọc được 50 trang văn bản, không đồng nghĩa với việc đã kiểm tra được bố cục. Văn bản có thể đủ nhưng bảng bị tràn lề, công thức hiển thị lỗi hoặc tiêu đề bị đẩy sang trang khác. **Phải hiểu cấu trúc trước khi can thiệp.**

### Bài học 2: Đừng sửa văn bản bằng chỉ số thứ tự cố định (Brittle Index)
Tuyệt đối tránh lối viết:
```python
doc.paragraphs[52].text = "Nội dung mới"  # RẤT NGUY HIỂM!
```
Chỉ số `52` chỉ đúng với một bản snapshot duy nhất. Thêm/bớt một đoạn phía trên sẽ làm chỉ số trỏ sang nội dung khác. Luôn định vị bằng mốc neo (Anchor), tiêu đề hoặc nội dung ngữ cảnh; đồng thời kiểm tra số lượng kết quả khớp (chỉ cho phép khớp duy nhất 1 lần).

### Bài học 3: Đừng phá định dạng chỉ để thay một cụm từ (Run Preservation)
Một đoạn văn (`<w:p>`) được cấu thành từ nhiều `Run` (`<w:r>`) mang các định dạng khác nhau (in đậm, in nghiêng, màu sắc, font chữ).
- Nếu gán lại toàn bộ `paragraph.text = "..."`, toàn bộ định dạng chi tiết của từng từ trong đoạn sẽ biến mất.
- **Hiện tượng Run-splitting:** Do bộ gõ tiếng Việt (Unikey) hoặc tính năng Spellcheck của Word, một cụm từ như `"Đặng Văn A"` có thể bị Word xé thành nhiều thẻ `<w:r>` riêng biệt. Không được thay thế mù quáng; phải sử dụng thuật toán phẫu thuật vi mô ở tầng XML.

### Bài học 4: Không lấy suy đoán thay cho dữ liệu thật (Bằng chứng > Giả định)
Tuyệt đối không tự ý sửa số liệu kỹ thuật, mã sinh viên, ngày tháng hay công thức chỉ vì "nghe có vẻ bất hợp lý":
| Loại thông tin | Cách xử lý |
|---|---|
| Lỗi chính tả chắc chắn 100% | Sửa trực tiếp bảo toàn Run |
| Cách diễn đạt chưa chuẩn văn phong | Biên tập nhưng giữ nguyên vẹn nghĩa gốc |
| Số liệu, công thức, mã hiệu kỹ thuật | Đối chiếu nguồn; nếu chưa xác minh thì ghi nhận/hỏi người dùng, CẤM tự bịa |

### Bài học 5: Lưu file thành công (`doc.save()`) không có nghĩa là hoàn thành
Lưu được file vật lý chỉ chứng minh code không bị crash. Nó không chứng minh file hiển thị đúng. Bắt buộc phải:
1. Mở lại file kiểm tra số lần còn sót của từ khóa cũ.
2. Kiểm định tính toàn vẹn cú pháp XML (`verify_docx.py`).
3. Kết xuất (Render PDF/PNG) để soi trực quan từng trang khi có thay đổi lớn.

### Bài học 6: Chờ người dùng nghiệm thu ảnh trước khi thay (User Acceptance Gate)
Khi thay thế ảnh sơ đồ trong file Word, Agent **BẮT BUỘC** phải hiển thị ảnh render mới và hỏi ý kiến xác nhận từ người dùng trước:
*"Ảnh đã OK để thay luôn vào tài liệu chưa, hay cần sửa/tinh chỉnh ảnh nào?"*
Tuyệt đối không được tự ý thực hiện ZIP swap ghi đè `imageX.png` nếu người dùng chưa trực tiếp duyệt hình thức trực quan của sơ đồ!

### Bài học 7: Kỷ luật thư mục công cụ — TUYỆT ĐỐI KHÔNG rải rác script ở root
Mọi công cụ/script bổ trợ sửa DOCX, inspect XML, hoán đổi ảnh hay render BẮT BUỘC phải nằm trong thư mục công cụ của dự án (`docs/tools/` hoặc `tools/`).
- Tuyệt đối CẤM tạo các script Python tạm thời (`replace_docx_images.py`, `inspect_docx_xml.py`, `apply_*.py`) rải rác ngay tại thư mục gốc (`root`) của dự án làm ô nhiễm git repository.

### Bài học 8: Phân định rạch ròi 2 không gian tài liệu (Báo cáo học thuật vs. Open-Source Docs)
- **Báo cáo học thuật / Đồ án môn học**: Đặt ở không gian riêng (ví dụ `reports/` hoặc `docs/report/` / tên tệp báo cáo riêng), phục vụ in ấn nộp trường, bảo vệ đề tài.
- **Tài liệu dự án Open-Source (`docs/`)**: Phục vụ phát hành mã nguồn mở lâu dài (Architecture, Developer Guide, API Reference, User Manual). Tránh để file báo cáo học thuật làm ô nhiễm tài liệu mở.

### Bài học 9: Phân định triệt để Ảnh chụp (Screenshots) và Sơ đồ (Diagrams)
- `docs/screenshots/`: 100% CHỈ chứa ảnh chụp màn hình UI thực tế của phần mềm (`01_*.png` -> `09_*.png`). Tuyệt đối CẤM để sơ đồ hoặc file `.puml`/`.dot` vào đây.
- `docs/diagrams/`: Chứa mã nguồn sơ đồ (`.puml`, `.dot`, `.tldr`) và file xuất vector/raster (`.svg`, `.png`). CẤM xả code sơ đồ ra chat, chỉ đưa ảnh render preview và link file.

### Bài học 10: Chỉ dùng `lxml`, CẤM `xml.etree` để ghi XML của Word
`xml.etree.ElementTree` serialize lại toàn bộ (đổi prefix namespace, đảo thứ tự attribute)
khiến Word báo "file appears to be corrupted" — **đã chứng minh**: round-trip ET trắng
(không đổi một chữ) vẫn gãy, cùng thao tác bằng `lxml` thì mở bình thường.
Mọi script đọc/ghi XML `.docx` trong skill này BẮT BUỘC `from lxml import etree`
(`lxml` đi kèm `python-docx`, không cần cài thêm). Chỉ đọc-parse thì ET vẫn dùng được.

### Bài học 11: Hỏng file thì cô lập từng bước, test bằng khả năng thật
Khi file lỗi sau nhiều bước sửa: test từng bước riêng trên bản sao
(`safe_replace` đơn lẻ → gãy / `number_captions` đơn lẻ → OK) thay vì đoán mò.
Và kiểm tra môi trường bằng **khả năng thật**, không qua trung gian:
tìm Word bằng đường dẫn chuẩn + tạo COM object thật, đừng tìm trong PATH
(Office không tự thêm vào PATH nên check PATH luôn báo sai).

---

## 3. Mẫu Code Python Chuẩn tắc (Safe In-Place Script Pattern)

Khi cần viết một script Python can thiệp nhanh, hãy tuân thủ mẫu chuẩn sau (có cơ chế **Fail on ambiguity** và **Post-save Verification**):

```python
#!/usr/bin/env python3
from pathlib import Path
from typing import Generator
from docx import Document
from docx.text.paragraph import Paragraph


def iter_paragraphs(doc: Document) -> Generator[Paragraph, None, None]:
    """Duyệt toàn bộ paragraph trong tài liệu, bao gồm cả các ô trong Table."""
    for p in doc.paragraphs:
        yield p
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    yield p


def replace_exact_phrase(doc: Document, old_text: str, new_text: str) -> None:
    """Thay thế một cụm từ duy nhất với độ an toàn cao:
    - Bắt buộc cụm từ chỉ xuất hiện đúng 1 lần trong toàn tài liệu.
    - Cụm từ phải nằm trọn vẹn trong 1 Run duy nhất để bảo toàn 100% định dạng.
    - Tự động raise Exception nếu phát hiện mơ hồ hoặc phân mảnh Run.
    """
    matching_paragraphs = [p for p in iter_paragraphs(doc) if old_text in p.text]

    if len(matching_paragraphs) == 0:
        raise ValueError(f"Không tìm thấy cụm từ '{old_text}' trong tài liệu.")
    if len(matching_paragraphs) > 1:
        raise ValueError(
            f"Tìm thấy {len(matching_paragraphs)} vị trí chứa '{old_text}'. "
            "Dừng lại để tránh sửa nhầm ngữ cảnh không mong muốn."
        )

    target_paragraph = matching_paragraphs[0]
    matching_runs = [r for r in target_paragraph.runs if old_text in r.text]

    if len(matching_runs) == 0:
        raise ValueError(
            f"Cụm từ '{old_text}' bị ngắt qua nhiều thẻ Run (<w:r>). "
            "Dừng lại: Cần dùng scripts/safe_replace_text.py để xử lý tầng XML."
        )
    if len(matching_runs) > 1:
        raise ValueError(f"Cụm từ '{old_text}' xuất hiện nhiều lần trong cùng đoạn.")

    target_run = matching_runs[0]
    target_run.text = target_run.text.replace(old_text, new_text, 1)


def main():
    source = Path("input.docx")
    output = Path("output.docx")
    if not source.is_file():
        raise FileNotFoundError(f"Không tìm thấy file: {source}")
    if source.resolve() == output.resolve():
        raise ValueError("Không được ghi đè trực tiếp lên file gốc.")

    doc = Document(source)
    replace_exact_phrase(doc, old_text="Cụm từ cũ", new_text="Cụm từ mới")
    doc.save(output)

    # Thẩm định lại: Mở file vừa lưu để đếm số vị trí cũ còn sót
    check_doc = Document(output)
    remaining = sum(p.text.count("Cụm từ cũ") for p in iter_paragraphs(check_doc))
    if remaining > 0:
        raise RuntimeError(f"Vẫn còn {remaining} vị trí chứa nội dung cũ.")
    print(f"✅ Đã lưu và kiểm định an toàn: {output.resolve()}")
```

---

## 4. Bộ Công cụ Tích hợp (`scripts/`)

| Công cụ | Lệnh thực thi | Mục đích |
|---|---|---|
| **Thay ảnh in-place** | `scripts/replace_images.py` | Hoán đổi nhị phân ảnh trực tiếp trong ZIP, tự đồng bộ `wp:extent` và `a:xfrm/a:ext` chống méo hình. |
| **Thay thế văn bản an toàn** | `scripts/safe_replace_text.py` | Thay thế chuỗi bảo toàn thẻ Run, xử lý triệt để bài toán ngắt chuỗi qua nhiều thẻ `<w:r>`. |
| **Chèn nội dung tại mốc** | `scripts/safe_insert_section.py` | Chèn đoạn văn bản/bảng mới ngay sau đoạn mốc (anchor paragraph) trên cây XML. |
| **Kiểm định toàn vẹn** | `scripts/verify_docx.py` | Quét cú pháp XML, kiểm tra liên kết media, thẩm định sự hiện diện/loại bỏ của từ khóa. |

---

## 5. Hướng dẫn Sử dụng Chi tiết

### A. Thay thế hình ảnh (In-Place Image Swap — Tự tính Aspect Ratio)
Word lưu kích thước ảnh theo đơn vị EMU (`cx`, `cy`). Nếu ảnh mới khác tỷ lệ ảnh cũ mà không tính lại `cy`, ảnh sẽ bị bẹp hoặc dẹt:
```bash
# 1. Liệt kê danh sách ảnh và Caption:
python scripts/replace_images.py path/to/document.docx --list

# 2. Thay thế một ảnh theo tên Caption / Hình:
python scripts/replace_images.py path/to/document.docx --figure "Hình 3.2" --new "assets/new_erd.png"

# 3. Thay thế hàng loạt theo file JSON mapping:
python scripts/replace_images.py path/to/document.docx --mapping image_mapping.json
```

### B. Thay thế văn bản bảo toàn Runs (Giải quyết triệt để Run-Splitting)
Khi chuỗi cần thay trải qua nhiều thẻ `<w:r>` do bộ gõ tiếng Việt hoặc Word spellcheck:
```bash
# Kiểm tra số vị trí khớp trước khi sửa (Dry-run):
python scripts/safe_replace_text.py path/to/document.docx --old "K59 KTPM 01" --new "K59KTP.K01" --dry-run

# Thực hiện thay thế:
python scripts/safe_replace_text.py path/to/document.docx --old "K59 KTPM 01" --new "K59KTP.K01"

# Thay thế hàng loạt theo mảng JSON:
python scripts/safe_replace_text.py path/to/document.docx --batch replacements.json
```

### C. Chèn thêm nội dung mới tại Mốc neo (Anchor In-Place Insertion)
Chèn đoạn văn bản/bảng mới ngay sau đoạn mốc mà không xáo trộn bố cục:
```bash
python scripts/safe_insert_section.py path/to/document.docx \
  --anchor "3.2.2. Quy chuẩn định dạng hiển thị phân tách" \
  --content "Lưu ý bổ sung: Mã định danh ngành Kỹ thuật máy tính sử dụng mã 5480106." \
  --style "Normal" --italic
```

### D. Kiểm định Toàn vẹn & Từ khóa (Verification Gate)
```bash
python scripts/verify_docx.py path/to/document.docx \
  --must-have "Trần Văn Khải" "K235480106035" "K59KTP.K01" \
  --must-not-have "K59 KTPM 01" "Academic Lab UI"
```

---

## 6. Những điều Tuyệt đối CẤM (Anti-Patterns)

- ❌ **CẤM** gọi `Document()` mới hay script `export_docx.py` để ghi đè lên file Word đã hoàn thiện của người dùng.
- ❌ **CẤM** sửa văn bản bằng số thứ tự cố định (`paragraphs[i]`).
- ❌ **CẤM** xóa toàn bộ `<w:r>` hoặc gán trực tiếp `paragraph.text` khi đoạn văn chứa nhiều định dạng ký tự khác nhau.
- ❌ **CẤM** thay file ảnh mà không cập nhật lại kích thước `cy` trong OpenXML (gây méo tỷ lệ khung hình).
- ❌ **CẤM** tự ý suy đoán số liệu kỹ thuật, mã sinh viên hoặc kết quả test khi chưa đối chiếu nguồn.
- ❌ **CẤM** kết luận hoàn tất khi chưa kiểm định cú pháp XML (`verify_docx.py`) và tạo bản sao lưu an toàn (`.bak_safe`).
- ❌ **CẤM** tạo các script sửa docx/kiểm tra rải rác ở thư mục gốc (`root`) của dự án; bắt buộc phải đặt trong `tools/` hoặc `docs/tools/`.
- ❌ **CẤM** lẫn lộn sơ đồ (`.puml`, `.dot`, `hinh_*`) vào thư mục `docs/screenshots/` (vốn chỉ dành cho ảnh UI thật).
- ❌ **CẤM** xả khối mã nguồn sơ đồ ra chat gây tràn màn hình; chỉ lưu file đĩa và gửi ảnh preview kèm link.
