---
name: project-handbook
description: "Viết SỔ TAY DỰ ÁN để người khác hiểu trọn dự án rồi XUẤT PDF A4 (bìa, mục lục, số trang). Đọc MÃ NGUỒN làm nguồn sự thật (routes, enum/trạng thái, job, webhook, mã lỗi) — không chép lại slide/báo cáo cũ. Tài liệu gồm: hiểu dự án trong 5 phút, bảng thuật ngữ, máy trạng thái, đường đi của tiền, phần nặng nhất: ĐẶC TẢ TỪNG TRƯỜNG HỢP theo bảng Đầu vào – Xử lý hệ thống – Đầu ra – Nhánh lỗi, kèm 8–15 kịch bản chạy suốt, bảng tra mã lỗi, mục Hạn chế đã biết và bảng kiểm 'đã phủ hết chưa' chống tài liệu mỏng. Dùng khi người dùng nói: viết tài liệu hướng dẫn dự án, sổ tay dự án, tài liệu bàn giao, tài liệu cho người mới, giải thích toàn bộ quy trình nghiệp vụ, liệt kê đầy đủ các trường hợp đầu vào–đầu ra, hoặc xuất tài liệu .md ra PDF để gửi/nộp."
---

# Skill: Sổ tay dự án — viết để NGƯỜI KHÁC hiểu, rồi xuất PDF

> **Sứ mệnh:** sau khi đọc tài liệu này, một người **chưa từng xem dự án** phải trả lời được:
> *dự án giải bài toán gì · có những tác nhân nào · từng trường hợp đầu vào/xử lý/đầu ra ra sao ·
> tiền/dữ liệu đi đâu · cái gì còn thiếu*. Và tài liệu đó phải **mở được bằng PDF trên máy bất kỳ**.

> [!CAUTION]
> **4 LUẬT CỨNG (không thương lượng):**
> 1. **NGUỒN SỰ THẬT LÀ MÃ NGUỒN.** Mọi khẳng định nghiệp vụ phải truy được về một hàm/endpoint/hằng số
>    trong `src/`. Slide, báo cáo, ghi chú cũ **thường lệch** (đã có ca: slide nói "quét tem là giải ngân",
>    code thì không). Nếu code và tài liệu cũ mâu thuẫn → **ghi rõ mâu thuẫn**, không im lặng chọn một.
> 2. **MỖI TRƯỜNG HỢP ĐỦ 4 DÒNG**: `Đầu vào` · `Xử lý hệ thống` (đánh số ①②③ theo đúng thứ tự code chạy) ·
>    `Đầu ra` (trạng thái + **số** thay đổi) · `Nhánh lỗi` (**MÃ LỖI** lấy từ code, không phải câu chữ).
> 3. **KHÔNG DÙNG CHỮ MÀU — CHỈ ĐEN/XÁM + HIGHLIGHT.** Đồng bộ luật của khối tài liệu (`docx-report`):
>    chữ đen, phân cấp bằng **cỡ chữ + độ đậm + đường kẻ + nền xám**, nhấn mạnh bằng **highlight** (`==chữ==`).
>    **Cấm** chữ xanh theme/đỏ/cam và **cấm `codehilite`** (nó tự sinh màu cho token code).
>    Mọi mục đích của màu chữ phải đạt được bằng đậm/nghiêng/highlight. Kiểm bằng máy:
>    `python scripts/check_pdf_monochrome.py <out.pdf>` → phải in `SACH`.
> 4. **PHẢI MỞ PDF SOI TRƯỚC KHI BÁO XONG.** Xuất PDF xong là chưa xong: render **trang bìa + 1 trang có bảng
>    + trang cuối** ra ảnh, nhìn bằng mắt để chắc chắn tiếng Việt **đủ dấu**, bảng **không tràn lề**,
>    mã lỗi **không bị cắt**, và **không có chữ màu**. Không mở PDF = chưa được tuyên bố đã giao.

> [!IMPORTANT]
> **Phân biệt với các skill khác trong bộ:**
> - `docx-report` → báo cáo/đồ án theo mẫu học thuật (bìa TNUT, SEQ/REF, số trang La Mã). **Không** dùng cho sổ tay dự án.
> - `doc-architect` / `living-docs` → README/AGENTS.md/ADR **trong repo**, viết cho lập trình viên & agent.
> - `pdf-toolkit` → đọc/trích/ghép **file PDF có sẵn**. Skill này **tạo** PDF từ Markdown.
> - `human-report-writing` → trau chuốt văn phong. Gọi nó **sau** khi đã có nội dung, nếu muốn câu chữ tự nhiên hơn.

---

## 1. Đầu ra bắt buộc

| # | Sản phẩm | Ghi chú |
|---|---|---|
| 1 | `docs/huong-dan/<ten>.md` (hoặc file người dùng chỉ định) | Nguồn — sửa được bằng tay về sau |
| 2 | `docs/huong-dan/<ten>.pdf` | Bản giao cho người đọc |
| 3 | `docs/huong-dan/<ten>-nguon.md` | **Bảng truy vết**: mỗi mục → `file:dòng` đã đọc để viết mục đó |
| 4 | (khuyến nghị) ảnh render bìa + 1 trang bảng | Bằng chứng đã soi PDF; có thể xoá sau khi xác nhận |

Nếu người dùng chỉ muốn PDF và không quan tâm file `.md`: vẫn tạo `.md` (đó là nguồn, để còn sửa),
nhưng chỉ giao đường dẫn PDF.

---

## 2. Quy trình 8 bước (bắt buộc theo thứ tự)

### Bước 1 — Khoanh vùng dự án (không viết gì vội)

- Xác định **ngôn ngữ/framework** và **cây nguồn** (module nào là lõi nghiệp vụ).
- Liệt kê: **routes/endpoints**, **enum & trạng thái**, **bảng dữ liệu chính**, **job/scheduler**,
  **webhook**, **hằng số cấu hình** (hạn mức, ngưỡng, TTL).
- Kết thúc bước này phải có một **danh mục có thể đếm được** ("42 endpoint · 9 trạng thái đơn · 4 job · 2 webhook").
  Lệnh gợi ý: quét `*.controller.ts`/`urls.py`/`routes/*`, file `enum*`, `*.service.*`.

### Bước 2 — Đọc bảng trạng thái & máy trạng thái

Trạng thái là **xương sống** của tài liệu: sai trạng thái thì mọi trường hợp sau đó sai theo.
Với mỗi enum: ghi **giá trị + nghĩa + ai/ở đâu đặt nó**, và **bảng chuyển đổi hợp lệ** nếu code có khai báo.
Đặc biệt săn các trạng thái **dễ nhầm** (ba trạng thái "đã giao / đã xác thực / hoàn tất" là ca kinh điển).

### Bước 3 — Đọc các service lõi và **vét sạch mã lỗi**

Đi từng luồng tiền/dữ liệu quan trọng, ghi lại **mọi mã lỗi** bị ném ra (`new Error('MÃ')`,
`throw new XxxException('MÃ')`, `raise ValueError('MÃ')`) và **điều kiện ném**.
Mã lỗi là thứ người bảo vệ sẽ hỏi, và cũng là thứ chứng minh tài liệu không bịa.

### Bước 4 — Lập BẢNG PHỦ TRƯỜNG HỢP trước khi viết

Dùng checklist trong [reference/handbook-outline.md](reference/handbook-outline.md) §2.6.
Mỗi nhóm tình huống đánh dấu: `có code?` / `cần viết?`. **Chốt danh sách trường hợp** rồi mới viết —
nếu viết trước rồi mới nghĩ, tài liệu sẽ thiếu đúng những nhóm khó (job định kỳ, webhook trùng, race condition).

### Bước 5 — Viết theo khung 4 phần

Khung 4 phần + quy ước bảng nằm ở [reference/handbook-outline.md](reference/handbook-outline.md).
Tóm tắt khung:

```
PHẦN I   Hiểu dự án trong 5 phút  (bài toán · thuật ngữ · sơ đồ khối · cách chạy thử)
PHẦN II  Luồng nghiệp vụ         (máy trạng thái · đường đi của tiền · ví dụ số thật)
PHẦN III Đặc tả từng trường hợp  (theo TÁC NHÂN, bảng Đầu vào/Xử lý/Đầu ra + lỗi + KB-nn)
PHẦN IV  Tra cứu & tin cậy       (mã lỗi · hạn chế đã biết · bảng kiểm phủ · phụ lục endpoint)
```

Nhóm trường hợp **theo tác nhân**, không theo menu giao diện:
`A·` tác nhân chính · `B·`,`C·` tác nhân khác · `D·` nội bộ (tách theo **vai trò thật trong code**) ·
`E·` **tác nhân thời gian/hệ thống** (job, webhook, scheduler) — **đừng bỏ `E·`**, đây là chỗ hay quên
và cũng là chỗ ăn điểm · `KB-nn` kịch bản chạy suốt.

### Bước 6 — Đối chiếu ngược (bước không được bỏ)

Đọc lại tài liệu của chính mình; với **mỗi câu khẳng định** tự hỏi *"tôi biết điều này vì dòng nào?"*.
Không trả lời được → sửa thành `UNKNOWN — cần xác minh` hoặc quay lại đọc code.
Ghi kết quả vào `<ten>-nguon.md` (bảng truy vết).

### Bước 7 — Xuất PDF

```bash
python .claude/skills/project-handbook/scripts/md_to_pdf.py \
    docs/huong-dan/<ten>.md --out docs/huong-dan/ \
    --kicker "Hướng dẫn dự án" --keep-html
```

Pipeline: `.md → .html (CSS in A4) → .pdf` qua **Chrome headless + CDP** (`Page.printToPDF`),
nên có **chân trang "Trang n/ N"** — thứ mà `pandoc`/`wkhtmltopdf` không làm được.
Cần: `pip install markdown`, **Node ≥ 20**, Chrome/Edge.

Bảng màu mặc định là **đen/xám + highlight** (xem 4 luật cứng, luật #3). Muốn đổi font/cỡ/lề thì dùng cờ;
**đừng** sửa CSS để thêm màu chữ — nếu bắt buộc phải thêm (ví dụ người dùng yêu cầu rõ ràng cho slide),
thì đó là **ngoại lệ có ý thức** và phải ghi lại lý do.

Tuỳ chọn hay dùng:

| Cờ | Việc |
|---|---|
| `--font "Times New Roman"` | Nếu tài liệu phải theo chuẩn học thuật (mặc định `Segoe UI`) |
| `--size 11` | Cỡ chữ thân bài (pt) |
| `--margin-mm 18,16,18,16` | Lề trên,phải,dưới,trái (mm) |
| `--no-cover` / `--no-toc` | Bỏ bìa / bỏ mục lục |
| `--toc-depth 2` | Mục lục nông hơn (mặc định 3) |
| `--landscape` | Khổ ngang (bảng rất nhiều cột) |
| `--header "Tên dự án"` | Dòng chạy trên đầu trang |
| `--author`, `--date`, `--subtitle`, `--title` | Ghi đè thông tin bìa |
| `--keep-html` | Giữ `.html` trung gian để soi CSS khi bố cục lạ |

**Nhấn mạnh trong Markdown — chỉ có 3 cách được phép:** `**đậm**`, `*nghiêng*`, `==highlight==`
(→ `<mark>` nền xám). **Không** dùng chữ màu, không dùng icon màu, không dùng emoji để "đánh dấu".
Markdown **không** tự hiểu `==…==`, `md_to_pdf.py` tự chuyển sang `<mark>` (bỏ qua trong khối code).

Hai điều phải nhớ về `==highlight==`:

1. **Dùng TIẾT CHẾ.** Cả tài liệu chỉ nên có vài chỗ (3–6). Highlight tràn lan thì không còn là nhấn mạnh,
   và người đọc sẽ bỏ qua hết. Chỉ đánh dấu **kết luận quan trọng nhất** hoặc **con số phải nhớ**.
2. **Highlight phải ĐỦ TƯƠNG PHẢN với nền đang chứa nó.** Bẫy thật đã gặp: highlight nằm trong `>` (blockquote,
   nền `#F7F7F7`) mà tông highlight đặt `#E8E8E8` thì **mắt gần như không thấy** ở tỉ lệ đọc thường.
   Thang xám trong `md_to_pdf.py` cố ý giãn ra: trang trắng `#FFF` → blockquote `#F7F7F7` →
   hàng chồng bảng `#F2F2F2` → **highlight `#D9D9D9`** (cách nền ~29 mức).
   Nghi ngờ thì **crop vùng đó ở zoom 3×** rồi nhìn, hoặc **đo pixel** — đừng đoán.

### Kiểm "không chữ màu" — bằng máy, không bằng mắt

`md_to_pdf.py` **tự chạy** kiểm tra này sau khi xuất và **cảnh báo** nếu PDF còn chữ màu.
Chạy tay (dùng được cho **mọi** PDF, kể cả PDF của skill khác):

```bash
python scripts/check_pdf_monochrome.py <out.pdf>
# SACH  = mọi span chữ đều đen/xám        -> exit 0
# CO CHU MAU                            -> exit 1 + bảng màu vi phạm + ví dụ
```

Nếu tài liệu gốc là **DOCX**, kiểm cả gốc bằng script của skill `docx-report`:

```bash
python ../docx-report/scripts/check_docx_monochrome.py <file.docx>
```

Bẫy hay gặp ở DOCX: **MỤC LỤC / DANH MỤC BẢNG in ra màu xanh** vì trường TOC mang char style
`Hyperlink` (màu mặc định của Word là `0000FF`) — thân bài vẫn đen nên rất dễ tưởng là sạch.
Sửa: đổi `<w:color>` của style `Hyperlink` thành `000000` và bỏ `w:themeColor`.

> **Cảnh báo kỹ thuật #1 (đã từng mắc):** PyMuPDF trả `span['color']` dạng **số nguyên đóng gói `0xRRGGBB`**,
> **không phải** xám 0..1. Nếu đọc sai kiểu thì màu xanh `0x1F4E79` bị đọc thành **trắng** ⇒ script
> báo `SACH` **oan**. Script này có `_self_test()` tự khẳng định chốt chặn đó ngay khi chạy.
> Khi sửa script kiểm màu, **luôn thử đối chứng**: dựng một PDF có chữ màu và xác nhận script **bắt được**.
>
> **Cảnh báo kỹ thuật #2:** `codehilite` của python-markdown **tự sinh màu inline** cho token code
> (`#008000` xanh lá, `#BA2121` đỏ…) ⇒ **cấm dùng**. Chỉ dùng `fenced_code` rồi tô **nền xám** bằng CSS.

**Bẫy "sửa rồi mà vẫn còn màu" — kiểm đến cùng, đừng đoán:** nếu bạn *nghĩ* đã bỏ hết màu nhưng PDF vẫn còn,
hãy để script **liệt kê mã màu + số span** (nó làm sẵn) thay vì mở mắt dò. Chính cách này đã lôi ra
8 mã màu khác nhau trong CSS cũ: `#1F4E79` (tiêu đề), `#2A2F38` (chữ trong blockquote), `#37414F` (mục lục con),
`#008000` + `#BA2121` (codehilite), `#22303F` (ô tiêu đề bảng), `#33475B` (nhãn «include»/«extend»), `#5A6270` (chữ mờ).

Cũng nhận **cả thư mục**: `md_to_pdf.py docs/huong-dan/ --out dist/` → mỗi `.md` một PDF.
Ảnh trong Markdown được đổi sang đường dẫn tuyệt đối tự động nên **ảnh nhúng được**.

**Dùng lại helper cho việc khác:** `scripts/html_to_pdf.mjs` là công cụ độc lập, không phụ thuộc
`md_to_pdf.py`. Nó có `--paper-w` / `--paper-h` (theo **inch**) để in ra trang **đúng kích thước tuỳ ý** —
hữu ích khi cần render một hình/khung cố định (ví dụ: SVG → PDF → PNG ở đúng kích thước pixel
`W/96 × H/96` inch, rồi rasterize ở `dpi = 96 × scale`). Đây chính là cách các script sinh sơ đồ
dùng để xử lý font tiếng Việt cho đúng.

### Bước 8 — **Mở PDF soi bằng mắt** rồi mới báo xong

Render ít nhất 3 trang ra ảnh và **nhìn**:

```bash
python -c "import pymupdf,sys; d=pymupdf.open(sys.argv[1]);
[print(i, d[i].get_text()[:80].replace(chr(10),' ')) for i in (0,1,d.page_count-1)]" <ten>.pdf
```

Hoặc dùng `pdf-toolkit/scripts/pdf_to_images.py` để chuyển trang thành ảnh rồi mở.
Kiểm đúng 6 thứ:

1. **KHÔNG có chữ màu** — chạy `check_pdf_monochrome.py` (md_to_pdf tự chạy) **và** nhìn bằng mắt;
   phân cấp phải đến từ **đậm + đường kẻ + nền xám**, không từ màu.
2. **Tiếng Việt đủ dấu** (không bị mất dấu / ô vuông).
3. **Bảng không tràn lề**, không cắt cột, không vỡ chữ trong ô.
4. **Mã lỗi và đường dẫn file không bị cắt** (chuỗi dài trong ô bảng).
5. **Chân trang có số trang**, bìa **không** bị chèn số trang lộn xộn.
6. **Mục lục khớp** với các mục thật trong bài (đếm vài mục).

Phát hiện lỗi → sửa `.md` hoặc CSS rồi xuất lại. **Cấm** tuyên bố "đã xuất PDF" khi chưa mở.

---

## 3. Kỹ thuật viết để không bị coi là "tài liệu mỏng"

| Kỹ thuật | Vì sao |
|---|---|
| **Đánh số ①②③ theo thứ tự code chạy** | Chứng minh đã đọc code, không phải kể lại tính năng |
| **Nêu MỘT TRANSACTION ở đâu** | Chi tiết kỹ thuật đắt giá; giải thích được vì sao không sợ trùng |
| **Nêu SỐ cụ thể ở Đầu ra** | "ví shop +24.291.000" kiểm được; "cập nhật thành công" không kiểm được |
| **Có nhóm `E·` (job/webhook/scheduler)** | Đây là nhóm bị bỏ quên nhiều nhất |
| **8–15 kịch bản `KB-nn`, ≥ 4 ca "xấu"** | Ca xấu mới lộ hiểu biết: im lặng, sai tem, sự cố, khiếu nại một phần, vượt ngưỡng, hai người cùng lúc, webhook trùng |
| **Mục "Hạn chế đã biết" kèm hướng sửa** | Giấu khuyết điểm = tài liệu sai; nói thẳng = tài liệu đáng tin |
| **Ghi rõ chỗ tài liệu cũ sai** | Nếu code khác slide, ghi một dòng: *"slide cũ nói X, code thực tế là Y (file:dòng)"* |

---

## 4. Luật chống tự lừa

> [!CAUTION]
> - **Cấm** dán nguyên một file nguồn vào tài liệu rồi gọi đó là "đặc tả". Đặc tả = mô tả **ngữ nghĩa** + mã lỗi + hiệu ứng dữ liệu.
> - **Cấm** ghi mã lỗi mình **chưa từng thấy** trong code. Mã lỗi bịa ra là lỗi nghiêm trọng nhất của tài liệu kỹ thuật.
> - **Cấm** viết "hệ thống kiểm tra và xử lý" — phải nói **kiểm cái gì, đối chiếu với cái gì, sai thì ra mã gì**.
> - **Cấm** bỏ trống dòng nào trong bảng kiểm phủ. ✅ hoặc ❌, không để "—".
> - **Cấm** tuyên bố số trang / số trường hợp mà chưa đếm thật.

---

## 5. Mẫu báo cáo cuối (dùng đúng mẫu này)

```text
Status: DONE | PARTIAL | BLOCKED
Nguồn sự thật: <đã đọc src/... (n file)>   |   KHONG dung slide/bao cao cu: YES/NO
Phạm vi dự án: <số endpoint> · <số trạng thái> · <số job> · <số webhook>
Tài liệu: <path .md>  (<n> dòng / <n> mục)
Truy vết: <path -nguon.md>  (so khang dinh co trich dan / tong)
Trường hợp đã đặc tả: A·<n> B·<n> C·<n> D·<n> E·<n>  = <tổng>
Kịch bản chạy suốt: KB-01..KB-<n>  (so ca "xau": <n>)
Mã lỗi đã liệt kê: <n>   |   Hạn chế đã biết: <n> mục
Bảng kiểm phủ trường hợp: <n> ✅ / <n> ❌ (❌ phải có trong "Hạn chế đã biết")
PDF: <path .pdf>  (<n> trang, <n> KB)
Đã MỞ PDF soi? YES/NO  — trang đã soi: <bìa | trang bảng | trang cuối>
  - check_pdf_monochrome.py: SACH | CO CHU MAU (<màu nào, bao nhiêu span>)
  - Chu mau (mắt thấy)?  KHONG/CO (chỗ nào)
  - Tiếng Việt đủ dấu?   YES/NO
  - Bảng tràn lề?        NO/YES (chỗ nào)
  - Mã lỗi bị cắt?       NO/YES
  - Số trang ở chân?     YES/NO
Findings chưa xử lý: <danh sách hoặc KHONG>
Limitations: <ví dụ: chưa đọc được module X do ..., số liệu UNKNOWN ở mục ...>
```

---

## 6. Chỉ thị ngắn cho Agent

> Đừng viết ngay. **Quét cây nguồn → đọc enum/trạng thái → đọc service lõi và vét mã lỗi →
> lập BẢNG PHỦ trường hợp → mới viết**. Nhóm theo **tác nhân thật** (có nhóm thời gian/hệ thống!).
> Mỗi trường hợp: **Đầu vào · Xử lý hệ thống (①②③) · Đầu ra (có SỐ) · Nhánh lỗi (MÃ từ code)**.
> Thêm 8–15 kịch bản chạy suốt với ≥ 4 ca "xấu". Ghi rõ **hạn chế đã biết**.
> Đối chiếu ngược từng khẳng định về `file:dòng`. Xuất PDF bằng `md_to_pdf.py`.
> **Và MỞ PDF RA XEM** (bìa + trang bảng + trang cuối) trước khi báo xong.
> Nguồn sự thật là **mã nguồn** — không phải slide.
