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

## 4. Tables & Style

Caption bảng đặt trên: `Bảng 3.1. Danh sách các bảng dữ liệu chính`.

Header: đậm, căn giữa khi phù hợp, nền nhẹ, viền rõ nhưng không nặng.
Body: Times New Roman, cỡ chữ đồng nhất, padding vừa phải, căn số liệu phù hợp.

Bảng dài: lặp header row, tránh cắt hàng, cho phép tiếp tục sang trang, kiểm tra render trang nối tiếp.

Không được: quá nhiều màu; chữ quá nhỏ; cột quá hẹp; nhồi nội dung dài vào một ô; để header biến mất ở trang sau.

QA:

```text
[ ] Caption đúng format
[ ] Header rõ
[ ] Không overflow
[ ] Không cắt chữ
[ ] Header lặp khi cần
[ ] Số liệu căn đúng
[ ] Font nhất quán
```

## 5. Figures & Images

- Ảnh căn giữa, giữ aspect ratio, không làm méo, không cắt ngoài ý muốn.
- Caption đặt ngay dưới hình, có mục đích rõ ràng: `Hình 3.1. Kiến trúc tổng thể của hệ thống`.

Kích thước: hình kỹ thuật đủ lớn để đọc text; screenshot website giữ 16:9 hoặc tỷ lệ gốc;
không phóng quá lớn gây tăng chiều cao không cần thiết.

Screenshot thật: ưu tiên screenshot từ website/sản phẩm thật; không dùng ảnh AI giả UI;
caption phải mô tả đúng nội dung hình.

Diagram: dùng Mermaid/PlantUML cho Use Case, Class, Activity, Sequence, State, Architecture.

QA: hình không mờ; text trong diagram đọc được; không có khoảng trống bất thường; caption không rời rạc;
hình không che văn bản; không có ảnh trắng/dư thừa.

## 6. Captions & Cross References

Quản lý số thực tế và tham chiếu cho hình, bảng, mục nội bộ. Không dùng text thủ công cho số thực tế
nếu Word field xử lý được.

Luồng: Insert caption → tạo field/sequence → bookmark nếu cần → insert REF tại vị trí tham chiếu
→ materialize field → render → kiểm tra.

Khi thêm/xóa hình: cập nhật field, kiểm tra numbering, kiểm tra các câu "theo Hình 3.1", "xem Bảng 3.2", render lại.

Không được: để `Hình 3.4` xuất hiện trước `Hình 3.2`; tham chiếu tới số không tồn tại; caption và hình cách xa nhau.

## 7. TOC & Navigation

TOC chỉ hoạt động chính xác khi heading hierarchy đúng.

```text
Audit headings → fix styles → update TOC fields → render
→ soi trang TOC → soi Navigation Pane
```

Kiểm tra: tên chương đúng; cấp mục đúng; số trang đúng sau render; không xuất hiện đoạn văn body trong TOC;
không mất mục con; không có tiêu đề nằm ngoài TOC do dùng sai style.

Khi chỉnh báo cáo lớn: không sửa TOC bằng tay trước khi sửa Heading.

## 8. Render & Visual Verification (shipping gate)

Không kết luận DOCX hoàn thiện chỉ dựa trên code hoặc text. Render rồi mới kết luận.

```bash
python scripts/render_docx.py input.docx --output_dir render --emit_pdf
```

Mỗi trang `page-N.png` phải được xem đủ mực để phát hiện: clipping, overlap, broken table,
missing glyph (đặc biệt dấu tiếng Việt), wrong page break, orphan caption, wrong header/footer, image stretching.

Vòng lặp: `Edit → Render → Inspect → Defect? Yes: Fix → Render | No: Ship`.

Không được: chỉ xem 1–2 trang; chỉ kiểm tra trang đầu; tin rằng LibreOffice warning luôn nghĩa là render thất bại;
giao bản chưa kiểm tra visual.

Báo cáo QA: `Pages / Inspected / Defects / Fixed / Final status`.

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
