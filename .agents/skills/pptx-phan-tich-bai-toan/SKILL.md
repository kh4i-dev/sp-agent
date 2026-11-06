---
name: pptx-phan-tich-bai-toan
description: Làm slide .pptx cho CHƯƠNG PHÂN TÍCH BÀI TOÁN của báo cáo đồ án/BTL/luận văn — bìa học thuật, đặt vấn đề, mục tiêu, phạm vi, tác nhân & phân quyền, kiến trúc tổng thể, so sánh phương án (ưu điểm/nhược điểm). Ưu tiên ít sơ đồ (chỉ sơ đồ chính), ảnh chụp THẬT của hệ thống, chữ vừa phải, layer biên tập được, văn phong "không giống AI", render QA. Dùng khi người dùng nói: slide phân tích bài toán, slide bảo vệ đồ án phần đặt vấn đề, slide báo cáo học thuật, slide đừng giống AI, slide ít chữ, slide có bảng ưu nhược điểm, kịch bản slide đồ án.
---

# PPTX Phân tích bài toán — slide học thuật, không "mùi AI"

Mục tiêu: bộ slide `.pptx` cho **chương phân tích bài toán** (đặt vấn đề → mục tiêu →
phạm vi → phân tích hệ thống → so sánh phương án) đủ **chuẩn học thuật** để nộp cô giáo,
**chữ vừa phải**, **biên tập được từng layer**, và **không lộ dấu hiệu AI**.

Skill này KHÔNG thay `pptx-deck` (làm mọi deck) hay `plantuml-diagrams` (vẽ sơ đồ).
Nó là lớp chuyên biệt cho **chương "phân tích bài toán"** với bộ layout + luật riêng.

## 0. Khi nào dùng / không dùng

- **Dùng:** slide bảo vệ/nộp phần *đặt vấn đề, khảo sát, phân tích–thiết kế, so sánh phương án*;
  cần deck "trông người làm" chứ không "trông máy làm".
- **Không dùng:** làm lại UI/marketing (`anti-slop`, `diagram-design`), Word
  (`docx-report`), sơ đồ chuẩn UML (`plantuml-diagrams`).

## 1. Nguyên tắc bất biến (IRON RULE)

1. **LAYER BIÊN TẬP ĐƯỢC.** Mọi thứ là **shape/textbox native** của PowerPoint (đặt tên
   shape), ảnh là **picture object**; **cấm** flatten sang ảnh, cấm "ảnh hóa" chữ hay bảng,
   cấm export Slidev/Marp (dạng ảnh). Người dùng phải click vào sửa được từng dòng.
2. **CHỮ VỪA PHẢI.** ≤ **45 từ/slide**; tiêu đề là **câu khẳng định** (không phải nhãn);
   bullet ≤ **5 dòng × ≤ 10 từ**; ≤ **1 ý/slide**. Nhiều chữ hơn thì **tách slide**, không thu nhỏ chữ.
3. **ÍT SƠ ĐỒ — CHỈ SƠ ĐỒ CHÍNH.** Tối đa **2 sơ đồ ảnh**/chương (thường: kiến trúc tổng thể,
   phân rã chức năng). Luồng/bước vẽ bằng **shape native** (chevron, khối) — sửa được và nhẹ.
   Sơ đồ học thuật **trắng–đen**; cấm sơ đồ nhiều màu trong báo cáo.
4. **ẢNH THẬT > ảnh minh hoạ AI.** Ưu tiên **ảnh chụp màn hình hệ thống thật, khung 16:9**
   (`docs/screenshots/`). Không có ảnh thật thì để **khung trống ghi chú rõ**, cấm ảnh AI
   chung chung; cấm ảnh full-page dài.
5. **KHÔNG MÙI AI.** Cấm: gradient tím–xanh, glassmorphism, "accent stripe" dưới tiêu đề,
   icon trang trí cạnh chữ, emoji, số liệu "social proof" bịa, và **bộ từ sáo AI** (§6).
6. **SỐ LIỆU CÓ NGUỒN.** Mọi con số phải kèm nguồn (cơ quan/tài liệu/năm). Không có nguồn →
   bỏ số, hoặc ghi `UNVERIFIED`. **Cấm bịa số cho đẹp.**
7. **KHÔNG HARDCODE THÔNG TIN NGƯỜI DÙNG.** Trường Họ tên/GVHD/Lớp/trường: **bắt buộc hỏi**;
   chưa có thì để `[điền]` trong bản nháp, **không tự chế tên**, không ship placeholder.
8. **RENDER LÀ CỔNG.** Chưa render (PDF/PNG) và soi từng slide = **chưa xong** (AGENTS.md #2).
9. **PHÂN ĐỊNH ẢNH/SƠ ĐỒ.** Ảnh chụp UI → `docs/screenshots/`; mã nguồn + ảnh sơ đồ →
   `docs/diagrams/`. Không trộn. Không xả `.puml` ra chat.

## 2. Kiến trúc deck chuẩn (chương phân tích bài toán)

Khung 15–18 slide, chọn theo dàn ý báo cáo. **Không bắt buộc đủ hết** — cái nào báo cáo có thì mới làm.

| # | Slide | Layout | Ghi chú |
|---|---|---|---|
| 1 | Bìa | `cover` | Tên đề tài + GVHD + SV + năm học, ảnh thật bên phải |
| 2 | Nội dung trình bày | `agenda` | 4 mục, 2 cột |
| 3 | Bối cảnh + số liệu | `kpi` | 2–4 chỉ số, kèm nguồn |
| 4 | Ba vấn đề chính | `cards` | 3 thẻ, mỗi thẻ 1 câu |
| 5 | Định hướng giải pháp | `flow` | 3–5 bước |
| 6 | Mục tiêu | `bullets` | 5–6 ý ngắn |
| 7 | Phạm vi trong/ngoài | `table` | 5–8 dòng |
| 8 | Đối tượng & quy mô | `split` | chữ trái + **ảnh thật** phải |
| 9 | Rủi ro & biện pháp | `table` | 3 cột |
| 10 | Chuyển chương | `section` | nền đậm |
| 11 | Tác nhân & phân quyền | `table` | bảng vai trò |
| 12 | **Kiến trúc tổng thể** | `diagram` | **sơ đồ chính #1** |
| 13 | Phân rã chức năng | `chips` | 14 ô native (hoặc sơ đồ chính #2) |
| 14 | Luồng nghiệp vụ cốt lõi | `flow` | 5–7 bước |
| 15 | **So sánh phương án** | `compare` | Ưu/nhược — trang nhiều chữ, xem §4 |
| 16 | Lựa chọn công nghệ | `table` | tầng · công nghệ · lý do |
| 17 | Kết luận phần phân tích | `bullets` | 3–4 điểm + cầu nối chương sau |
| 18 | Cảm ơn / Q&A | `closing` | |

## 3. Bộ layout & khi nào dùng

Chi tiết toạ độ, cỡ chữ, mã màu: **`reference/layouts.md`**.

`cover` · `agenda` · `kpi` · `cards` · `flow` · `bullets` · `split` · `table` · `compare` ·
`chips` · `diagram` · `section` · `closing`.

Quy ước chung (đã cài sẵn trong script):
- Nền trắng; **1 màu chủ đạo** cyan `#0E7490` + **1 accent** đậm `#0A4E60`; nền phụ `#F5F9FA`.
- Tiêu đề **Arial** (không gạch chân, không stripe), thân bài **Times New Roman** (đúng dấu tiếng Việt).
- Cỡ: tiêu đề 25 · thân 15 · thẻ 13,5 · bảng 12,5 · chú thích nguồn 10,5. **Không < 9**.
- Mỗi slide: `kicker` nhỏ (chữ thường, không IN HOA giãn chữ) + tiêu đề + nội dung + footer + số trang.

## 4. Trang nhiều chữ ⇒ "trang trí" bằng cấu trúc, không bằng clip-art

Bảng so sánh / ưu–nhược là chỗ dễ "tường chữ" nhất. Cách xử lý (layout `compare`):

- Hai **khối phương án** cạnh nhau; mỗi khối có **thanh tiêu đề đậm** + 2 **khối nền nhạt**:
  *Ưu điểm* nền xanh nhạt `#EAF6EE` (chữ xanh `#1B7F4B`), *Nhược điểm* nền đỏ nhạt `#FBECEA`
  (chữ đỏ `#B42318`).
- **Dấu đầu dòng là ô vuông nhỏ native** (không dùng icon/emoji), **chữ thường** (không in hoa).
- Mỗi ý **≤ 10 từ**; tổng mỗi khối **≤ 4 ý**. Vẫn quá dài → tách thành 2 slide.
- Đường kẻ hairline `#D7E4EA` phân tách; **nhiều khoảng trắng** hơn là thêm màu.
- Bảng nhiều dòng: header nền nhạt, dòng chẵn/lẻ so le rất nhẹ, **cột đầu đậm**, caption nguồn dưới bảng.

Nguyên tắc chung: **cấu trúc (khối, cột, số thứ tự mờ lớn) tạo nhịp thị giác** — không dán icon
trang trí, không gradient, không khung nhiều màu.

## 5. Toolchain

| Việc | Lệnh |
|---|---|
| Sinh deck (native, editable) | `python scripts/make_deck.py --spec <spec.json> --out deck.pptx` |
| Khung rỗng để tự điền | `python scripts/make_deck.py --blank --out template.pptx` |
| Kiểm tra nhanh (số từ, placeholder, font, tràn chữ) | `python scripts/inspect_deck.py deck.pptx` |
| Render PDF + PNG từng slide | `python scripts/render_pptx.py deck.pptx --outdir render` |

- Spec mẫu: `assets/spec.example.json` (mọi field + ghi chú). **Nội dung nằm trong JSON**,
  sửa JSON rồi sinh lại — hoặc click sửa trực tiếp từng layer trong PowerPoint.
- Cài: `pip install python-pptx pymupdf Pillow` + LibreOffice (render).
- Font an toàn khi render: **Arial / Times New Roman / Calibri / Cambria**. Cấm Poppins/Inter/… mặc định.

## 6. Ngôn từ & giọng văn (chống "mùi AI")

Danh sách đầy đủ + ví dụ sửa: **`reference/anti-ai-voice.md`**.

Ngắn gọn:
- Viết như **đang nói với lớp**: câu ngắn, chủ ngữ rõ, thuật ngữ Việt + tiếng Anh trong ngoặc.
- Cấm bộ từ sáo: "trong thời đại số ngày nay", "không chỉ… mà còn", "giải pháp toàn diện",
  "đột phá", "tối ưu hoá trải nghiệm", "hành trình", "đóng vai trò then chốt", "vô cùng quan trọng".
- Cấm **3 gạch đầu dòng song song na ná** (dấu hiệu AI): mỗi ý một độ dài/kiểu khác nhau tự nhiên.
- Cấm lạm dụng em-dash (—), dấu ngoặc kép "nhấn mạnh", và số liệu không nguồn.
- Tiêu đề **khẳng định có nội dung**: "COD khiến người mua trả tiền trước khi kiểm hàng"
  (đúng) thay vì "Tổng quan về vấn đề" (rỗng).

## 7. Quy trình 7 bước

```text
1. NẠP & HỎI      : đọc báo cáo (chương 1 & 3); HỎI tên/GVHD/Lớp/trường; hỏi màu nhận diện nếu có.
2. CHỌN DÀN Ý     : map dàn ý báo cáo -> bảng §2; chốt slide list (15–18).
3. CHỌN ẢNH/SƠ ĐỒ : lọc ảnh chụp thật 16:9 + 1–2 sơ đồ chính; tuyệt đối không ảnh AI.
4. VIẾT SPEC      : điền spec.json theo §1 (≤45 từ/slide) — không bịa số, ghi nguồn.
5. SINH DECK      : make_deck.py -> deck.pptx (native shapes, có tên layer).
6. INSPECT        : inspect_deck.py -> sửa placeholder / tràn chữ / font / số từ.
7. RENDER & SOI   : render_pptx.py -> soi TỪNG ảnh slide -> fix -> render lại slide đã sửa.
```

**Gate:** chỉ giao khi Render = PASS và đã soi ảnh. Bước 6–7 lặp tới khi sạch.

## 8. Render & Visual QA — checklist bắt buộc

Soi từng ảnh slide, kiểm:

- [ ] **Tràn/cắt chữ**, chữ đè khối, chữ đè ảnh, ảnh méo tỉ lệ.
- [ ] Lề ≥ 0,5"; khoảng cách phần tử ≥ 0,3"; không sát mép.
- [ ] **Font bị thay thế khi render** (dấu tiếng Việt lỗi ô vuông).
- [ ] Tương phản chữ/nền đạt (không xám mờ trên nền nhạt).
- [ ] **Số từ/slide ≤ 45** (inspect đã cảnh báo).
- [ ] Ảnh là **ảnh thật**; caption ghi nguồn; số liệu có nguồn.
- [ ] Slide **chỉ toàn chữ** → cân nhắc thêm ảnh/cấu trúc.
- [ ] Số trang, footer, tên đề tài nhất quán.

## 9. Footguns

- `python-pptx` **không nhân bản slide trực tiếp** (chỉ `add_slide`); `text_frame.text =` làm mất định dạng.
- **SVG/EMF lỗi** `UnidentifiedImageError` → luôn chuyển PNG trước khi chèn.
- Ảnh `contain` giữ tỉ lệ; `cover` có thể cắt chữ trong ảnh infographic → ưu tiên `contain`.
- LibreOffice QA **không đáng tin về font** hơn PowerPoint; nghi ngờ → chỉ dùng font ở §5.
- Đừng tin "trông xong": mở ảnh render ra soi thật (AGENTS.md #2, #10).

## 10. Definition of Done

```text
[ ] Đã HỎI thông tin người dùng (không hardcode); không còn placeholder trong bản giao.
[ ] Deck native, sửa được từng layer; ≤ 45 từ/slide; tiêu đề là câu khẳng định.
[ ] Ít sơ đồ (≤ 2 sơ đồ ảnh), sơ đồ trắng–đen; ảnh là ảnh thật 16:9.
[ ] Số liệu có nguồn; không số bịa; không còn từ sáo AI.
[ ] inspect_deck.py: 0 LỖI.
[ ] Render PDF/PNG: PASS và đã soi từng slide.
```

## 11. Format phản hồi cuối

```text
Deck   : <file.pptx>   (native, biên tập được)
Slides : N — <N từ> từ/slide (max)
Spec   : <spec.json>
Sơ đồ  : n sơ đồ ảnh (trắng–đen) · Ảnh thật: n ảnh 16:9
QA     : inspect PASS/FAIL · render PASS/FAIL · đã soi ảnh: có/không
Cần bạn điền: [Họ tên, GVHD, Lớp...]
Tinh chỉnh tiếp: [gợi ý 2–3 chỗ có thể muốn đổi]
```
