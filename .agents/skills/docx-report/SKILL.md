---
name: docx-report
description: "Tạo, đọc, audit và chỉnh sửa tài liệu Word (.docx) cho báo cáo/đồ án: heading & numbering, bảng, hình, caption, cross-reference, mục lục (TOC), style, render & kiểm tra trực quan. CỔNG PASS HAI ĐIỀU KIỆN — thiếu một là FAIL: (1) MÁY: render ra PDF + PNG từng trang, field TOC/PAGE tự cập nhật, cấu trúc/tiêu đề/bảng/caption đúng; (2) MẮT/VISION: agent có VISION (multimodal) soi từng trang PNG, xác nhận checklist (header bảng, caption, không rớt trang, font/lề, hình+caption khớp) và kết luận bố cục đã hợp lý chưa; model text-only không tính. Dùng khi viết/sửa/kiểm tra file .docx, báo cáo, đồ án, luận văn, hoặc nhắc tới DOCX, Word, python-docx, OOXML, caption, TOC, render, đồ án môn học."
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
| Audit nhanh không ảnh + review Markdown | `.claude/skills/human-md-audit/scripts/fast_audit_docx.py` + `export_review_md.py` | Vòng lặp nhanh trước render; FAST-CHECK PASS **không** thay VISUAL PASS |
| Chuẩn hóa học thuật & Style | `scripts/edit_docx.py` | `--academic-format`: lề giấy 3.5/2/3/3cm, thụt lề 1 tab, Justify, giãn dòng 1.35, **Heading Times New Roman + Heading 1 khóa đầu trang**, style bảng (11pt), **caption bảng tự chuyển xuống dưới bảng** |
| Chèn trường tự động | `scripts/edit_docx.py` | `--add-toc --add-tof --add-tot` (Mục lục/Danh mục hình/Danh mục bảng), `--add-page-numbers` (số trang) |
| **Sinh bìa / phần đầu** | `scripts/make_cover.py` | `--kind doan\|btl`: Bìa chính, Bìa lót, Nhiệm vụ; `--full` thêm Phiếu thông qua/Ghi điểm/Lời cam đoan; viền hoa văn chừa gáy + logo; `--prepend-to` ghép lên đầu báo cáo |
| **Thay ảnh siêu tốc (Non-destructive)** | `scripts/replace_docx_images.py` | **Thay thế ảnh trực tiếp vào ZIP OOXML, bảo toàn 100% định dạng, style, bảng biểu của file Word đã sửa đẹp** |
| Chuyển `.doc` → `.docx` | `scripts/convert_doc.py` | Word 97–2003 không đọc được bằng python-docx — convert bằng Word COM / LibreOffice |
| Tracked changes | `scripts/revisions.py` | `--list` (read-only) · `--accept` / `--reject` (thao tác trên **bản sao**) |
| Tạo mới | `python-docx` | Thư viện chuẩn tạo docx từ Python |
| Render kiểm tra | `scripts/render_docx.py` | Xuất PDF + PNG; **tự cập nhật field (TOC/PAGE) khi dùng Word COM** |

**Bảng cờ `edit_docx.py` (chạy `python edit_docx.py report.docx <cờ>`):**

| Cờ | Tác dụng |
|---|---|
| `--academic-format` | Trọn gói: lề, văn xuôi, heading, bảng, caption |
| `--style-headings` | Chỉ heading: TNR, màu đen; **Heading 1 page-break-before**; H2–5 keep-with-next |
| `--style-tables` | Chỉ bảng: header in đậm/căn trái, nền trắng, cantSplit, tblHeader |
| `--style-captions` | Chỉ caption: **chuyển caption bảng/hình về đúng vị trí (dưới bảng/hình)** + định dạng |
| `--table-font-size 11` | Cỡ chữ trong bảng (mặc định 11pt; chuẩn 10.5–12) |
| `--add-toc` / `--add-tof` / `--add-tot` | Chèn field Mục lục / Danh mục hình / Danh mục bảng |
| `--add-page-numbers` | Chèn field PAGE vào footer (số trang liên tục) |
| `--cover-end "LỜI CAM ĐOAN"` | Mốc bắt đầu front-matter; **trước mốc = bìa không đánh số** (tách Section) |
| `--body-start "MỞ ĐẦU"` | Mốc bắt đầu thân bài; **từ mốc = số Ả Rập bắt đầu lại từ 1** (tách Section) |
| `--number-captions` | Tự đánh số caption bằng field (SEQ, theo chương) + bookmark; tham chiếu "Hình 3.2"/"Bảng 3.2" trong bài thành cross-reference (REF). Thêm `--caption-plain` để đánh số đơn giản (Hình 1, 2, 3…) |
| `--replace "old" "new"` / `--replace-many map.json` | Thay thế văn bản |

> **Đánh số trang theo phần (chuẩn đồ án):**
> ```bash
> python scripts/edit_docx.py report.docx --cover-end "LỜI CAM ĐOAN" --body-start "MỞ ĐẦU" -o out.docx
> ```
> → Bìa (không số) | Front-matter (i, ii, iii) | Thân bài (1, 2, 3…). Mốc khớp theo **đầu đoạn** (không phân biệt hoa thường). Nếu chỉ cần đánh liên tục, dùng `--add-page-numbers`.

> **Lưu ý cập nhật field**: TOC/TOF/TOT/PAGE chỉ hiển thị đúng sau khi **cập nhật field**. `render_docx.py` dùng **Word COM** sẽ tự `Fields.Update()` trước khi xuất PDF. Nếu render bằng **LibreOffice (soffice)**, field **không tự cập nhật** → mở bằng Word bấm `Ctrl+A` → `F9` (hoặc `References → Update Table`) rồi render lại trước khi kết luận.

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
> **Sinh bìa / phần đầu (2 định dạng Đồ án & BTL): `scripts/make_cover.py`** — chi tiết `reference/cover-formats.md`.
> Chuyển `.doc` → `.docx`: `scripts/convert_doc.py`. · Tracked changes: `scripts/revisions.py`.
> Quy mô & độ sâu báo cáo (chống báo cáo mỏng): `reference/report-scope.md`.
> Ngôn từ caption / tên hình (mềm hóa, tránh cụm kỹ thuật cứng): `reference/caption-wording.md`.
> Đặc tả use case (bộ 9 thành phần, ID luồng A/E + BR-xx, exception đủ 4 thứ, template, ví dụ): `reference/use-case-spec.md`.

## Phần đầu tài liệu (Bìa) — HỎI ĐỊNH DẠNG TRƯỚC (bất biến)

Khi người dùng cần **bìa / phần đầu tài liệu**, **BẮT BUỘC hỏi** họ chọn loại nào (không tự đoán):

1. **Đồ án PTTKHT** (`--kind doan`): tiêu đề **"ĐỒ ÁN PHÂN TÍCH THIẾT KẾ HỆ THỐNG"**; có Nhiệm vụ thiết kế; cấu trúc 13 phần.
2. **Báo cáo bài tập lớn** (`--kind btl`): tiêu đề **"BÁO CÁO BÀI TẬP LỚN"** + **MÔN HỌC** + **NĂM HỌC**; phần đầu gọn hơn.

### Phỏng vấn thu thập thông tin (BẮT BUỘC — kiểu `grill-me`)

**KHÔNG hardcode tên sinh viên / giảng viên.** `make_cover.py` sẽ **báo lỗi** nếu thiếu thông tin bắt buộc.
Trước khi sinh bìa, **hỏi người dùng TỪNG CÂU MỘT** (mỗi câu kèm 1 đáp án gợi ý), không tự bịa:

1. Loại tài liệu? → *Đồ án PTTKHT* / *Báo cáo bài tập lớn* (gợi ý: Đồ án PTTKHT)
2. Tên đề tài (đúng như bìa)?
3. Giáo viên hướng dẫn (học vị + họ tên)?
4. Họ tên sinh viên?
5. Lớp? · 6. MSSV? · 7. Niên khóa (VD 2022-2026)?
8. Ngành? · Hệ? (gợi ý: KỸ THUẬT MÁY TÍNH / ĐẠI HỌC CHÍNH QUY)
9. Bộ môn / Khoa? (gợi ý: CÔNG NGHỆ THÔNG TIN / KHOA ĐIỆN TỬ)
10. *(BTL)* Môn học + Năm học? · *(Đồ án)* Ngày giao / ngày hoàn thành nhiệm vụ?
11. Năm trên bìa? (gợi ý: năm hiện tại)
12. Mục tiêu số trang / có dùng `--full` (Phiếu thông qua + Ghi điểm + Cam đoan) không?

Chỉ khi đã có đủ **đề tài + GVHD + SV + lớp + MSSV** (+ môn học nếu BTL) mới chạy script.

```bash
# Đồ án
python scripts/make_cover.py --kind doan --out bia.docx --topic "..." --gvhd "..." \
    --sv "..." --lop "..." --mssv "..." --khoa-dao-tao "2022-2026" --year 2026
# BTL
python scripts/make_cover.py --kind btl --out bia.docx --mon-hoc "CÔNG NGHỆ PHẦN MỀM" \
    --nam-hoc "2025-2026" --topic "..." --gvhd "..." --sv "..." --lop "..." --mssv "..." --year 2026
# Ghép lên ĐẦU báo cáo có sẵn
python scripts/make_cover.py --kind btl --prepend-to report.docx -o report_full.docx --data data.json
```

Bìa gồm **Bìa chính + Bìa lót + Nhiệm vụ**, có **khung viền hoa văn bám theo lề văn bản (`offsetFrom="text"`) để chừa gáy đóng quyển** + logo TNUT. Sau khi ghép bìa, chạy bộ đánh số trang để thân bài bắt đầu từ 1 (xem ở trên).

## Phạm vi công cụ (trung thực — đọc trước khi hứa với người dùng)

**Đã có script làm được (đã kiểm chứng chạy thật):**
- Chuẩn hóa học thuật: lề, văn xuôi, **heading (TNR + Heading 1 khóa đầu trang)**, bảng (11pt), caption.
- **Tự chuyển caption bảng/hình về đúng vị trí** (dưới bảng/hình) khi caption đang nằm trên.
- Chèn field TOC/TOF/TOT + số trang (PAGE); render bằng Word COM **tự cập nhật field**.
- **Tách Section + đánh số trang chuẩn**: bìa (không số) | front-matter (La Mã i,ii) | thân bài (Ả Rập từ 1) — qua `--cover-end` / `--body-start`.
- **Sinh bìa/phần đầu 2 định dạng (Đồ án PTTKHT & Báo cáo BTL)** — có viền hoa văn chừa gáy, logo TNUT; `--full` thêm **Phiếu thông qua đồ án + Phiếu ghi điểm + Lời cam đoan**; ghép được lên đầu báo cáo có sẵn.
- **Caption tự đánh số (SEQ) + cross-reference (REF)** — `edit_docx.py --number-captions` (Hình/Bảng theo chương, tự cập nhật khi chèn/xóa; tham chiếu trong bài tự liên kết).
- **Danh mục từ viết tắt** (bảng ẩn viền, A–Z) — `make_cover.py --abbr "CSDL:Cơ sở dữ liệu;API:..."` hoặc `--full`.
- **Chuyển `.doc` cũ → `.docx`** — `convert_doc.py` (Word COM / LibreOffice).
- **Tracked changes an toàn** — `revisions.py --list` (read-only) / `--accept` / `--reject` (tác trên bản sao).
- Thay ảnh in-place; render PDF→PNG; audit cấu trúc.

**Hạn chế đã biết (không báo quá lời):**
- Tách Section tự động (bìa/front-matter/thân) chỉ chạy khi tài liệu đang ở **1 section**; tài liệu nhiều section phức tạp → tách tay.
- Caption đánh số **theo chương** cần Heading 1 dạng "CHƯƠNG N"; nếu không có thì dùng `--caption-plain`.
- Sửa nội dung mà file có tracked changes phải dùng `revisions.py` trước (python-docx nuốt `w:ins`/`w:del` khi lưu — xem `rules.md` §12).


## Ngữ nghĩa & Quy mô báo cáo — CHỐNG BÁO CÁO MỎNG (bất biến)

Trước khi viết, **xác nhận mục tiêu số trang** với người dùng. Phải đạt quy mô tối thiểu:

| Loại | Trang nội dung tối thiểu | Ghi chú |
|---|---|---|
| **Đồ án PTTKHT** | **40 – 60 trang** | Không kể bìa/phụ lục/danh mục |
| **Báo cáo bài tập lớn (BTL)** | **15 – 30 trang** | |
| Báo cáo môn ngắn | **10 – 15 trang** | |

**Quy tắc cứng (không vi phạm):**
- **Cấm tóm tắt suông**: mỗi mục (Heading 3) phải có **đoạn văn hoàn chỉnh (≥ 5–8 câu)** + dẫn chứng (bảng/sơ đồ/số liệu/ví dụ).
- **Mỗi chương đạt số trang tối thiểu**; nếu mỏng → mở rộng bằng phân tích, ca kiểm thử, sơ đồ — **KHÔNG chèn chữ rỗng/lặp**.
- Đồ án phải có **đủ sơ đồ** (tổ chức, use case, lớp, hoạt động, trạng thái, ERD) + **bảng đặc tả** + **ảnh chụp màn hình thật**.
- Thiếu dữ liệu để đủ độ sâu → **HỎI người dùng**, tuyệt đối **không bịa** (đánh dấu `TODO` nếu chưa có).
- Sau render **đếm số trang từng chương**; mỏng hơn chuẩn → viết bổ sung rồi render lại.

> Bảng độ sâu theo từng chương + checklist "báo cáo mỏng" + bộ skill phối hợp: `reference/report-scope.md`.

## Văn phong thân bài — BẮT BUỘC (đồng bộ với `human-report-writing`)

Khi viết/sửa **văn xuôi thân bài** trong `.docx`, bắt buộc áp nguyên văn bộ luật định dạng của skill `human-report-writing`:

- **CẤM dấu gạch dài em dash (`—`) trong câu văn.** Dùng dấu phẩy, dấu chấm hoặc tách câu. Gạch nối `-` trong từ ghép và gạch đầu dòng vẫn dùng bình thường.
- **CẤM in đậm/bôi đậm chữ trong thân bài** (ngoại lệ: tiêu đề Heading, và ô tiêu đề bảng theo quy tắc bảng ở trên).
- **CẤM tô nền / highlight màu** (đặc biệt nền vàng).
- **CẤM bullet tràn lan**: ưu tiên đoạn văn xuôi; chỉ dùng bullet cho danh mục/bước tuần tự thật sự.
- Loại bỏ từ sáo rỗng AI theo **Fluff Blacklist** của `human-report-writing`.

> **Chống hiểu nhầm (root cause):** các ký tự `—` xuất hiện trong CHÍNH file hướng dẫn này chỉ để trình bày, **KHÔNG** phải kiểu chữ để chép vào báo cáo. Nội dung `.docx` giao cho người dùng **tuyệt đối không chứa em dash**. Khi nhận yêu cầu "viết/sửa báo cáo", hãy **nạp thêm skill `human-report-writing`** để lấy đầy đủ luật văn phong.

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
   - *Giải pháp:* Luôn bật `<w:cantSplit/>` cho mọi hàng bảng; bật `keep_with_next = True` cho ảnh. Nếu bảng dài nằm sát đáy trang, ưu tiên đặt thuộc tính **đoạn `keep_with_next`** cho dòng trước bảng, và **CHỈ** dùng `doc.add_page_break()` như phương án cuối — vì chèn ngắt trang thủ công ở sai vị trí sẽ sinh **trang trắng** (xem quy tắc Heading 1 dùng `page_break_before`).
6. **Bẫy "Ảo tưởng hoàn thành" qua text log (Blind Console Deception)**:
   - *Sai lầm:* Thấy script Python chạy ra `exit code 0` là vội vàng tin rằng file đã hoàn hảo và báo cáo người dùng.
   - *Thực tế:* 90% lỗi vỡ bảng, lệch lề, mất font chỉ hiện ra trên trang render thực tế.
   - *Giải pháp:* **BẮT BUỘC RENDER PDF $\rightarrow$ PNG VÀ DÙNG TOOL XEM ẢNH SOI TỪNG TRANG**.
7. **Bẫy Giả lập Heading bằng định dạng thủ công (Fake Headings)**:
   - *Sai lầm:* Dùng paragraph thường rồi bôi đậm và tăng cỡ chữ để làm tiêu đề.
   - *Thực tế:* Navigation Pane bị trống, Mục lục tự động (TOC) nhảy sai trang hoặc không cập nhật được.
   - *Giải pháp:* Bắt buộc dùng `doc.add_heading(text, level=N)` và áp dụng đúng Heading Styles chuẩn của Word.
8. **Bẫy Rải rác Script công cụ ở thư mục gốc (Scattered Scripts Trap)**:
   - *Sai lầm:* Tạo các script Python tạm thời (`replace_docx_images.py`, `inspect_docx_xml.py`, `apply_*.py`) rải rác ngay tại thư mục gốc (`root`) của dự án.
   - *Thực tế:* Gây rác dự án, lẫn lộn mã nguồn phần mềm với công cụ tài liệu.
   - *Giải pháp:* **Bắt buộc gom toàn bộ công cụ sửa docx/render vào thư mục `tools/` (hoặc `docs/tools/`) của dự án.**
9. **Bẫy Lẫn lộn Không gian Tài liệu (Monolithic Docs Pollution)**:
   - *Sai lầm:* Để chung file Báo cáo học thuật/BTL (.docx nộp bài) vào cùng thư mục với tài liệu dự án Open-Source.
   - *Thực tế:* Gây khó khăn khi phát hành mã nguồn mở, lẫn lộn thông tin sinh viên/đồ án với docs dự án.
269:    - *Giải pháp:* **Phân tách 2 không gian tài liệu độc lập:** 1 thư mục/tài liệu cho Báo cáo học thuật (`reports/` hoặc `docs/report/`) và 1 thư mục `docs/` cho dự án Open-Source (chứa Architecture, Guides, API, Diagrams, Screenshots).
270: 10. **Bẫy Trộn lẫn Ảnh chụp và Sơ đồ (Screenshots vs. Diagrams Mixing)**:
271:     - *Sai lầm:* Để file vẽ sơ đồ (`.puml`, `.dot`, `hinh_*.png`) vào thư mục `screenshots/`, hoặc xả code sơ đồ ra màn hình chat.
272:     - *Giải pháp:*
273:       - `docs/screenshots/`: 100% CHỈ chứa ảnh chụp màn hình UI thật của ứng dụng (`01_*.png` ...).
274:       - `docs/diagrams/`: Chứa mã nguồn sơ đồ (`.puml`, `.dot`) và file ảnh xuất vector/raster (`.svg`, `.png`).
275:       - CẤM xả khối mã nguồn sơ đồ ra chat, chỉ đưa ảnh render preview và link file.
276: 11. **Bẫy Rò rỉ Thụt Lề Đầu Dòng từ Style Normal vào Ô Bảng (Table Indent Leakage Trap)**:
277:     - *Sai lầm:* Nghĩ rằng chỉ cần gán độ rộng cột `cell.width` hay `gridCol` là chữ trong bảng sẽ hiển thị chuẩn.
278:     - *Thực tế:* Trong tài liệu tiếng Việt, style `Normal` thường có thuộc tính thụt lề dòng đầu 1.25 cm (`<w:ind w:firstLine="720"/>`). Do các đoạn văn `<w:p>` trong ô bảng không có khai báo `w:ind` độc lập, Word/LibreOffice để thuộc tính này rò rỉ vào mọi ô bảng, đẩy ký tự đầu tiên sang phải 1.25 cm. Ở các cột hẹp (Mã STT, Mã UC < 1500 twips), thụt lề này nuốt trọn hơn một nửa ô, bóp nghẹt diện tích khiến các mã định danh bị bẻ gãy rớt dòng dị dạng (`F-1` / `2`, `M` / `ã UC`).
279:     - *Giải pháp:* Duyệt toàn bộ `<w:pPr>` trong mọi ô bảng, ép cứng `<w:ind w:firstLine="0" w:left="0" w:right="0"/>` và xóa sạch `w:firstLineChars`.
280: 12. **Bẫy Bẻ Gãy Từ Ghép Tiếng Anh & Tên CSDL trong Bảng (CamelCase Word Fracture)**:
281:     - *Sai lầm:* Giữ nguyên các định danh CSDL hoặc class camelCase dài (`ConnectionRequest`, `TutorVerificationDocument`) trong cột nội dung hẹp.
282:     - *Thực tế:* Từ dài không có dấu cách nên khi ô bị co lại, Word tự động bẻ ngang từ mà không có gạch nối (`Connect` xuống dòng `ionRequest`), gây mất thẩm mỹ trầm trọng.
283:     - *Giải pháp:* Việt hóa sang thuật ngữ nghiệp vụ thân thiện (`Yêu cầu PENDING`, `Tài liệu xác minh`) hoặc thiết kế độ rộng cột tối thiểu 1800–2200 twips.
284: 
285: ## Quy tắc patch (bất biến)
286: 
287: - Không rewrite toàn bộ tài liệu nếu chỉ cần sửa một phần.
288: - Không thay numbering thủ công nếu Word style/field làm được.
289: - Không resize hình phá aspect ratio.
290: - Không sửa nội dung bị đánh dấu "evidence" nếu không được yêu cầu.
291: 
292: ## Heading & Numbering
293: 
294: ```text
295: Heading 1 = CHƯƠNG / tiêu đề cấp cao
296: Heading 2 = 1. / 2. / 3.
297: Heading 3 = 1.1. / 1.2.
298: Heading 4 = 1.1.1.
299: ```
300: 
301: > **QUY TẮC HEADING CHUẨN (bất biến):**
302: > 1. **Khóa Heading 1 ở đầu trang (Page Break Before)**: Mọi `Heading 1` (CHƯƠNG / MỞ ĐẦU / KẾT LUẬN…) **BẮT BUỘC** đặt `paragraph_format.page_break_before = True` để luôn bắt đầu ở đầu một trang mới. Dùng thuộc tính `page_break_before` (thuộc tính đoạn) **KHÔNG** chèn ký tự ngắt trang thủ công `doc.add_page_break()` (tránh sinh trang trắng khi Heading 1 đã nằm sẵn đầu trang sau `Section Break`). Heading 2/3/4 **KHÔNG** ép ngắt trang (chỉ `keep_with_next = True` để chống mồ côi).
303: > 2. **Heading cũng là Times New Roman**: Toàn bộ Heading 1–4 dùng **Times New Roman**, **màu đen `RGBColor(0,0,0)`**, **KHÔNG in nghiêng**. Phải sửa cả **cấp Style** (`doc.styles["Heading 1"]`) *và* mọi **run** thực tế trong đoạn heading (Style Word mặc định là `Calibri Light` + màu xanh theme — nếu bỏ qua sẽ lộ font lạ). Ép thêm `w:rFonts` (ascii/hAnsi/eastAsia/cs) để Word không fallback font.
304: > 3. **Chống mồ côi heading**: Mọi Heading đặt `keep_with_next = True` để tiêu đề không bị bỏ trơ ở đáy trang.
305: 
306: Mẫu Python-docx khóa Heading 1 + ép Times New Roman:
307: ```python
308: from docx.oxml import OxmlElement
309: from docx.oxml.ns import qn
310: from docx.shared import Pt, RGBColor
311: 
312: def format_heading_styles(doc, font_name="Times New Roman", sizes_pt=(16, 14, 13, 12)):
313:     for level in range(1, 5):
314:         st = doc.styles[f"Heading {level}"]
315:         st.font.name = font_name          # Times New Roman, KHÔNG Calibri Light
316:         st.font.bold = True
317:         st.font.italic = False
318:         st.font.color.rgb = RGBColor(0, 0, 0)   # màu ĐEN, không màu xanh theme
319:         st.font.size = Pt(sizes_pt[level - 1])
320:         # Ép w:rFonts đủ 4 khe để không fallback font khi render
321:         rpr = st.element.get_or_add_rPr()
322:         rfonts = rpr.find(qn("w:rFonts")) or OxmlElement("w:rFonts")
323:         rpr.insert(0, rfonts)
324:         for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
325:             rfonts.set(qn(attr), font_name)
326:         st.paragraph_format.keep_with_next = True
327:         if level == 1:
328:             st.paragraph_format.page_break_before = True  # KHÓA HEADING 1 LUÔN ĐẦU TRANG MỚI
329: 
330:     # Áp cả cho run thực tế trong tài liệu (style có thể bị direct formatting phủ)
331:     for p in doc.paragraphs:
332:         name = (p.style.name or "").lower()
333:         if "heading" not in name and "tiêu đề" not in name:
334:             continue
335:         lvl = next((int(c) for c in name if c.isdigit()), 1)
336:         p.paragraph_format.keep_with_next = True
337:         p.paragraph_format.page_break_before = (lvl == 1)
338:         for r in p.runs:
339:             r.font.name = font_name
340:             r.font.italic = False
341:             r.font.color.rgb = RGBColor(0, 0, 0)
342: ```
343: 
344: - Không giả heading bằng chữ đậm + cỡ lớn.
345: - Không tự gõ số `1.1.1.` nếu hệ thống numbering đã quản lý.
346: - Không đổi numbering hiện có nếu chưa audit TOC.
347: - Sau khi sửa, kiểm tra lại Navigation Pane.
348: 
349: ## Bảng biểu (Tables) — Chuẩn học thuật bất biến
350: 
351: > **QUY TẮC BẢNG CHUẨN:**
352: > 1. **Nền bảng**: **100% TRẮNG TINH (KHÔNG ĐÁNH MÀU)**. Tuyệt đối không tô xám `#EAEAEA`, không tô xanh, không viền rườm rà. Nền mọi ô (kể cả hàng tiêu đề) luôn là màu trắng / trong suốt.
353: > 2. **Tiêu đề cột (Header row 0)**: **IN ĐẬM (`bold=True`)**, **KHÔNG CĂN GIỮA** (căn lề trái `LEFT` hoặc căn theo kiểu dữ liệu), **KHÔNG IN NGHIÊNG**. Cỡ chữ 10.5–12pt. Bắt buộc có thuộc tính `<w:tblHeader/>` để tự động lặp lại khi sang trang.
354: > 3. **Tên gọi của bảng / Chú thích (Caption)**: **ĐẶT Ở CUỐI BẢNG (ngay dưới bảng)**. **CHỮ THƯỜNG IN NGHIÊNG, CĂN GIỮA** (`italic=True`, `bold=False`, `alignment=CENTER`). Cỡ chữ 12–13pt. Sử dụng paragraph style riêng tên là `bảng` (hoặc `Table Caption`).
355: > 4. **Khóa chống gãy hàng**: Mọi hàng (`trPr`) bắt buộc có `<w:cantSplit/>`.
356: > 5. **Khóa cứng độ rộng cột & bảng (OOXML Table Grid & Fixed Layout)**: Bắt buộc tái tạo `<w:tblGrid>` chứa `<w:gridCol w:w="..."/>`, dọn sạch `<w:tcW>` cũ trước khi gán mới, và khóa cứng `<w:tblLayout w:type="fixed"/>`, `<w:tblW w:type="dxa" w:w="..."/>`.
357: > 6. **Triệt tiêu 100% rò rỉ thụt lề (Zero Indent Leakage)**: Mọi đoạn văn `<w:p>` trong ô bảng phải có thẻ `<w:ind w:firstLine="0" w:left="0" w:right="0"/>` để chặn thuộc tính `w:firstLine="720"` (1.25 cm) của style `Normal` rò rỉ vào ô bảng gây thụt đầu dòng và bẻ gãy từ.
358: > 7. **Khóa chống ngắt dòng mã định danh (`w:noWrap`)**: Cột STT, Mã UC, Mã chức năng (`F-01`, `F-12`) bắt buộc có `<w:noWrap/>` trong `<w:tcPr>`, căn giữa (`CENTER`) để ngăn Word ngắt dòng tại dấu gạch nối (`-`).
359: > 8. **Căn lề chuẩn & CẤM căn đều (`both`) trong ô bảng**: Cột mã/STT căn giữa, cột nội dung căn trái (`LEFT`). **TUYỆT ĐỐI CẤM căn đều hai bên (`both`/justified)** trong ô bảng vì Word sẽ kéo dãn khoảng cách giữa các từ một cách dị dạng khi gặp từ dài.

> **Lưu ý quy ước caption:** Vị trí caption **dưới bảng** là quy ước của skill này (khớp mẫu tham khảo TNUT). Nhiều trường yêu cầu **tên bảng ghi TRÊN bảng** — hãy kiểm tra quy định của trường trước; nếu vậy thì **bỏ qua** bước chuyển caption, chỉ giữ định dạng chữ nghiêng/căn giữa. `edit_docx.py --style-captions` **tự chuyển** caption đang nằm trên bảng/hình xuống dưới; nếu trường yêu cầu caption trên bảng thì **không** dùng cờ này cho caption bảng.

Mẫu Python-docx chuẩn hóa bảng học thuật:
```python
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

def format_academic_table(table, col_widths, font_size_pt=10.5):
    """
    Chuẩn hóa bảng học thuật chuyên nghiệp (Zero-Indent, Fixed Width, No-Wrap Code Columns):
    - Triệt tiêu 100% hiện tượng thụt lề đầu dòng kế thừa từ style Normal (firstLine="720").
    - Cố định độ rộng từng cột và tổng chiều rộng bảng (tblLayout=fixed, tblW dxa).
    - Căn giữa cột Mã/STT, căn trái các cột nội dung (CẤM căn đều 'both'/justified gây giãn từ).
    - Khóa không ngắt dòng trên cột Mã (w:noWrap).
    - Nền trắng tinh khiết, viền đen sắc nét.
    """
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.allow_autofit = False

    total_width_dxa = sum(int(w.inches * 1440) for w in col_widths)
    tblPr = table._tbl.tblPr
    
    # 0. Khóa cứng tblW và tblLayout fixed
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is None:
        tblW = OxmlElement('w:tblW')
        tblPr.append(tblW)
    tblW.set(qn('w:w'), str(total_width_dxa))
    tblW.set(qn('w:type'), 'dxa')

    tblLayout = tblPr.find(qn('w:tblLayout'))
    if tblLayout is None:
        tblLayout = OxmlElement('w:tblLayout')
        tblPr.append(tblLayout)
    tblLayout.set(qn('w:type'), 'fixed')

    # 1. Khóa cứng độ rộng bằng tblGrid
    tblGrid = table._tbl.find(qn('w:tblGrid'))
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    tblGrid = OxmlElement('w:tblGrid')
    for w in col_widths:
        col = OxmlElement('w:gridCol')
        col.set(qn('w:w'), str(int(w.inches * 1440)))
        tblGrid.append(col)
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
            tcPr = cell._tc.get_or_add_tcPr()
            if col_idx < len(col_widths):
                w = col_widths[col_idx]
                w_dxa = int(w.inches * 1440)
                for old_w in tcPr.findall(qn('w:tcW')):
                    tcPr.remove(old_w)
                tcPr.append(parse_xml(f'<w:tcW xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:w="{w_dxa}" w:type="dxa"/>'))
                # XÓA BỎ MỌI SHADING: Nền trắng tinh
                for old_shd in tcPr.findall(qn('w:shd')):
                    tcPr.remove(old_shd)

            # Khóa không ngắt dòng trên cột đầu tiên nếu là mã ngắn (Mã UC, F-01, STT)
            if col_idx == 0:
                if tcPr.find(qn('w:noWrap')) is None:
                    tcPr.append(OxmlElement('w:noWrap'))

            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                
                # BẮT BUỘC TRIỆT TIÊU THỤT ĐẦU DÒNG TRONG Ô BẢNG (Zero Indentation)
                # Chống rò rỉ thụt lề 1.25cm (firstLine="720") từ style Normal
                pPr = p._p.get_or_add_pPr()
                ind = pPr.find(qn('w:ind'))
                if ind is None:
                    ind = OxmlElement('w:ind')
                    pPr.append(ind)
                ind.set(qn('w:firstLine'), '0')
                ind.set(qn('w:left'), '0')
                ind.set(qn('w:right'), '0')
                if qn('w:firstLineChars') in ind.attrib:
                    del ind.attrib[qn('w:firstLineChars')]

                # Căn chỉnh văn bản: Cột 0 căn giữa, các cột nội dung căn trái (CẤM căn đều 'both')
                if row_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.bold = True
                        r.font.italic = False
                        r.font.size = Pt(font_size_pt)
                        r.font.color.rgb = RGBColor(0, 0, 0)
                else:
                    if col_idx == 0:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for r in p.runs:
                        r.font.size = Pt(font_size_pt)
                        r.font.color.rgb = RGBColor(0, 0, 0)

def add_table_caption(doc, text):
    """Caption ở CUỐI BẢNG: chữ thường in nghiêng, căn giữa, style 'bảng'"""
    from docx.enum.style import WD_STYLE_TYPE   # BẮT BUỘC import (không dùng docx.enum.style.*)
    try:
        bang_style = doc.styles.add_style('bảng', WD_STYLE_TYPE.PARAGRAPH)
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
> 4. **Giữ nguyên tỷ lệ (Aspect Ratio)**: Không bóp méo hình ngang/dọc; screenshot phải chụp từ sản phẩm thật. Sơ đồ: **ưu tiên sinh bằng công cụ** (`plantuml-diagrams` / `tldraw-diagrams` / `diagram-orchestrator`); **được phép vẽ tay / draw.io / tldraw / SVG** khi công cụ không cho bố cục sạch (VD Use Case nhiều actor — xem `use-case-layout`) miễn đúng chuẩn UML và **có file nguồn** (`.puml`/`.dot`/`.tldr`/`.drawio`/`.svg`). **Cấm ảnh AI ảo/bịa không đúng sự thật**.

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

> **CẢNH BÁO (bài học thực chiến 2026-10-27):** `replace_docx_images.py` ghi lại
> `document.xml` bằng lxml nên **đổi hết prefix namespace sang `ns0:`, `ns1:`…** và
> bỏ `standalone="yes"`. Word mở file và báo **"The file appears to be corrupted."**
> (python-docx vẫn đọc được nên rất dễ lọt). Khi cần thay ảnh an toàn, ưu tiên
> **byte-level swap**: copy nguyên xi mọi entry của gói ZIP, chỉ thay bytes của
> `word/media/<tên>.png` (xem `../safe-docx-modifier/scripts/replace_images.py` — ZIP swap in-place); ảnh mới **phải cùng
> tỉ lệ khung** với ảnh cũ để không phải sửa `wp:extent`. Sau khi thay, **bắt buộc mở
> thử bằng Word COM** (`Documents.Open(..., ReadOnly=True)`) trước khi báo xong.

## Caption & Cross-reference

```text
Insert caption → tạo field/sequence → bookmark (nếu cần)
→ insert REF tại vị trí tham chiếu → materialize field → render → kiểm tra
```

Không để `Hình 3.4` xuất hiện trước `Hình 3.2`; không tham chiếu tới số không tồn tại.

### Ngôn từ caption / tên hình — MỀM HÓA (tránh cụm kỹ thuật cứng)

Ưu tiên góc nhìn **vòng đời – hành trình – sự chuyển dịch** thay cho tên loại sơ đồ thuần kỹ thuật:

- ✗ *"Biểu đồ máy trạng thái tài khoản" / "State Machine Diagram"* → ✓ **"Vòng đời tài khoản người dùng"**
- Biến thể: *Hành trình trạng thái…*, *Các giai đoạn của…*, *Sơ đồ luân chuyển trạng thái…*, *Tiến trình quản lý…*, *Quy trình chuyển đổi trạng thái…*, *Sơ đồ vòng đời…*
- Phiên bản ngắn cho slide: *"Trạng thái … & Sự chuyển dịch"*.

Quy tắc mềm hóa:
- **Subtitle nhẹ** dưới tiêu đề (đặt ở caption, không nhồi trong ảnh): *"Mô tả cách tài khoản chuyển đổi qua các giai đoạn: Hoạt động, Tạm khóa và Đã đóng."*
- **Mềm hóa trạng thái**: *"Bị khóa"* → **"Tạm khóa / Gián đoạn"**; *"Đã xóa"* → **"Đã đóng / Ngừng kích hoạt"**; *"Hủy"* → *"Đã hủy"*.
- Áp dụng cho **caption Hình/Bảng, tiêu đề mục, nhãn trong sơ đồ, tiêu đề slide**; giữ **nhất quán** toàn bài; tên chuẩn kỹ thuật chỉ nêu khi thật cần (phụ lục).
- Mềm nhưng **không rỗng**: vẫn đúng bản chất nghiệp vụ (source truth).

> Danh sách đầy đủ + bảng thay thế từ ngữ: `reference/caption-wording.md`.

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
[ ] HEADING: Times New Roman, màu đen, không nghiêng; Heading 1 BẮT BUỘC page_break_before=True (khóa đầu trang mới); Heading 2/3/4 keep_with_next (không mồ côi).
[ ] BẢNG: Nền trắng 100% (không tô màu), Tiêu đề cột IN ĐẬM, KHÔNG căn giữa; lặp header (tblHeader); chống gãy hàng (cantSplit).
[ ] CAPTION BẢNG: Đặt ở CUỐI BẢNG (ngay dưới bảng), cỡ 12–13pt, chữ thường in nghiêng, CĂN GIỮA (style 'bảng').
[ ] HÌNH ẢNH: Căn giữa, keep_with_next = True; Caption đặt NGAY DƯỚI, chữ thường in nghiêng, CĂN GIỮA (style 'hình').
[ ] Công thức toán: Căn giữa, số thứ tự (Chương.Số) căn sát lề phải.
[ ] Đánh số trang: Phần đầu số La Mã (i, ii, iii...); Thân bài từ Chương 1 số Ả Rập (1, 2, 3...).
[ ] Không lẫn Calibri/Arial ngoài ý muốn.
[ ] KHÔNG CHỮ MÀU: chạy `python scripts/check_docx_monochrome.py <file.docx>` → phải SACH.
[ ] Đặc biệt style `Hyperlink` = 000000 (mặc định Word là 0000FF → MỤC LỤC in ra xanh).
[ ] (Nếu xuất PDF) chạy `project-handbook/scripts/check_pdf_monochrome.py <file.pdf>` → phải SACH.
```

Nguyên tắc: giữ emphasis cần thiết, không xóa style đặc thù của code/hình, không đổi nội dung.
Sau normalize **bắt buộc render lại**.

> **Bẫy màu chữ hay bị bỏ qua nhất — style `Hyperlink`:** Word định nghĩa sẵn char style `Hyperlink`
> màu `0000FF`; MỤC LỤC / DANH MỤC BẢNG là trường TOC (hyperlink) nên **in ra xanh dù thân bài đen**.
> Sửa tối thiểu: đổi `<w:color>` của style `Hyperlink` thành `000000`, **bỏ** `w:themeColor`, **giữ** `<w:u>`.
> Chi tiết + các bẫy màu khác: [`reference/rules.md`](reference/rules.md) mục **2b**.


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

> [!CAUTION]
> **PASS TÀI LIỆU = HAI ĐIỀU KIỆN — THIẾU MỘT = KHÔNG ĐƯỢC BÁO HOÀN THIỆN.**
>
> | # | Điều kiện | Bằng chứng bắt buộc |
> | :-- | :--- | :--- |
> | **ĐK1 — MÁY** | Render thật ra **PDF + PNG từng trang**; field TOC/TOF/TOT/PAGE tự cập nhật; `inspect_docx`/audit script **0 lỗi**; ảnh nhúng là **ảnh thật** (file `.png` tồn tại, không placeholder), rộng 14–15.5 cm, khớp caption `Hình X.Y` |
> | **ĐK2 — MẮT/VISION** | Agent **có VISION (multimodal) soi từng trang PNG** bằng công cụ xem ảnh, xác nhận Checklist §1–7 (header bảng, caption, không rớt trang, font/lề, hình+caption khớp, heading đúng đầu trang; với hình: bố cục cân đối, chú thích liền hình). Ghi **`Vision audit by: <model-id>` + ≥3 chi tiết nguyên văn + kết luận "sắp xếp đã hợp lý chưa"**. Model text-only đọc text extraction **không tính** |
>
> - Chỉ chạy script (ĐK1) → **FAIL — visual QA missing** (script 0 lỗi không thay được mắt soi).
> - Chỉ nhìn ảnh (ĐK2) nhưng chưa render / chưa cập nhật field / thiếu ảnh thật → **FAIL — automated gate not met**.
> - **Audit bằng model text-only (không vision) → FAIL** (không có chứng kiến thực tế; phải giao vision subagent/model nếu model hiện tại không đọc được ảnh).
> - **Sơ đồ nhúng trong DOCX còn phải qua `diagram-auditor`**: ĐK1 (script + file nguồn `.py`/`.puml`/`.dot` tồn tại + ảnh `.png`/`.svg` tồn tại) + ĐK2 (soi ảnh + kết luận "sắp xếp hợp lý"). Thiếu file nguồn sinh sơ đồ = **FAIL**.

### Pipeline Render Bắt buộc:
```bash
# 1. Convert DOCX -> PDF + PNG từng trang độ phân giải cao (LUÔN xuất cả hai)
python scripts/render_docx.py report.docx --output_dir render --dpi 150
#    (chỉ cần PDF: thêm --pdf_only)
```
> Render bằng **Microsoft Word (COM)** sẽ tự `Fields.Update()` → TOC/TOF/TOT/PAGE đúng.
> Nếu chỉ có **LibreOffice (soffice)**: field KHÔNG tự cập nhật → trong Word bấm `Ctrl+A` rồi `F9` (Update Field) **trước khi render**, hoặc chấp nhận TOC có thể trống/sai số trang.

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
6. **Kiểm tra Font & Lề**: Toàn bộ **kể cả Heading** là Times New Roman đồng nhất (không lộ Calibri Light ở tiêu đề), màu đen; thụt đầu dòng 1 tab (1.27 cm), căn đều 2 bên (Justify), lề gáy 3.5 cm không bị lẹm.
7. **Kiểm tra ngắt trang Heading**: Mỗi **Heading 1** (CHƯƠNG / MỞ ĐẦU / KẾT LUẬN…) bắt đầu ở **đầu một trang mới** (page-break-before) và **không sinh trang trắng**; không có CHƯƠNG nằm lửng giữa trang.

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
