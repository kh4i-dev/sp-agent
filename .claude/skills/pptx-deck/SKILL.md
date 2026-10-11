---
name: pptx-deck
description: Tạo và chỉnh sửa slide PowerPoint (.pptx) cho thuyết trình/báo cáo: chọn template, bố cục slide, bảng, biểu đồ native, ảnh, speaker notes, render & kiểm tra trực quan. Dùng khi người dùng yêu cầu làm slide, thuyết trình, PowerPoint, PPTX, deck, bài trình bày, hoặc nhắc tới pptxgenjs, python-pptx, slide, biểu đồ.
---

# PPTX Deck Skill — Kỹ sư slide thuyết trình

Mục tiêu: deck `.pptx` **biên tập được** (không phải ảnh), nhất quán thương hiệu,
và đã được render kiểm tra từng slide trước khi giao.

## Khi nào dùng

- Làm slide cho báo cáo đồ án / bảo vệ / thuyết trình.
- Chỉnh sửa một deck có sẵn theo template.
- Chuyển dàn ý (outline) thành bộ slide.

## Thứ tự ưu tiên

```text
1. Source truth (nội dung đúng dự án)
2. Template / nhận diện thương hiệu
3. Bố cục & phân cấp thị giác
4. Biểu đồ & hình minh họa
5. Nhất quán thị giác
6. Render verification
7. Giao file cuối
```

## Toolchain

| Việc | Công cụ | Ghi chú |
|---|---|---|
| Tạo mới từ đầu | `pptxgenjs` (Node) | Chart native OOXML, master tùy biến, xuất 16:9 |
| Sửa / thay text / ảnh | `scripts/edit_pptx.py` | Thay text hàng loạt, chèn ảnh/background vào slide |
| Tiêm Speaker Notes | `scripts/add_notes.py` | Đọc `speaker_notes.md` tiêm tự động vào slide |
| Audit & kiểm tra deck | `scripts/inspect_deck.py` | Đếm slide, kiểm tra thiếu notes, cảnh báo >40 từ |
| Render kiểm tra | `scripts/render_pptx.py` | Xuất PDF & PNG (PowerPoint COM Windows / soffice) |

Cài đặt:

```bash
npm install pptxgenjs          # tạo mới
pip install python-pptx        # edit/inject notes/inspect
# Render: tự động dùng PowerPoint (Windows) hoặc LibreOffice (soffice)
```

> Hướng dẫn toàn diện từ nghiên cứu đến bảo vệ: `reference/academic-defense-workflow.md`.
> Script render: `scripts/render_pptx.py`.
> Script tiêm notes: `scripts/add_notes.py`.
> Script kiểm tra deck: `scripts/inspect_deck.py`.
> Script sửa PPTX: `scripts/edit_pptx.py`.

## Quy trình

### Tạo mới (pptxgenjs-first)

```text
1. Chọn template / bảng màu (1 màu chủ đạo + accent)
2. Dựng dàn ý: mỗi slide một ý
3. Sinh bằng pptxgenjs (chart native, không ảnh hóa biểu đồ)
4. Validate (kiểm tra XML/hex/shadow) sau writeFile()
5. Render → soi từng slide → fix → render lại slide thay đổi
```

### Sửa / template

```text
Thumbnail toàn bộ template để chọn layout
→ map nội dung vào placeholder theo idx (ổn định)
→ để bullet/theme font kế thừa từ layout, KHÔNG hardcode
→ nếu template slot ≠ số mục nguồn: xóa cả group của mục dư
→ render → QA
```

## Quy tắc thiết kế deck

- **Một ý một slide.** Không nhồi 2 chủ đề.
- **Headline là câu khẳng định** (assertion), không phải nhãn chủ đề.
- Hạn chế bullet: tối đa ~5 bullet × ~5 từ; ưu tiên hình/ sơ đồ hơn tường chữ.
- **Quy tắc 10/20/30**: ≥ 10 slide ⇒ ≥ 20 phút ⇒ font ≥ 30pt (tối thiểu không dưới ~24pt).
- Nhất quán font/bảng màu/margin; nhiều khoảng trắng; phân cấp & tương phản rõ.
- Tránh: gạch chân tiêu đề, accent stripe, quá nhiều màu, layout lặp nhàm chán.
- Mọi slide nên có yếu tố thị giác (sơ đồ/bảng/biểu đồ/hình).

## Bảng & biểu đồ

- Bảng: header đậm, ít đường kẻ, căn số liệu, không quá 5–6 cột.
- Biểu đồ: dùng chart **native** (có thể sửa số liệu trong PowerPoint), không dán ảnh chart.
- pptxgenjs hỗ trợ combo/3D: area, bar, line, pie, radar, scatter, bubble, doughnut.

## Speaker notes

- Dùng `addNotes` (pptxgenjs) hoặc notes master (python-pptx).
- Nội dung: ý chính + số liệu cần nhớ, KHÔNG dán nguyên văn slide.

## RENDER & VISUAL QA — shipping gate

```bash
python scripts/render_pptx.py deck.pptx --output_dir render
```

Soi **mọi** slide để phát hiện:

- chữ tràn/ cắt (lỗi phổ biến nhất), overlap;
- margin < 0.5" hoặc khoảng cách < 0.3" quá sát;
- tương phản thấp;
- font bị thay thế khi render (Aptos/Georgia/Trebuchet không đáng tin);
- layout lặp lại, body text bị căn giữa.

Content QA: `markitdown deck.pptx` và grep `xxx`, `lorem`, `TODO` còn sót.

## Footguns (bắt buộc tránh)

- pptxgenjs: layout mặc định 10×5.625"; KHÔNG dùng `#` trước hex hay hex 8 ký tự; shadow offset ≥ 0;
  chart combo phải đủ trục; sau `writeFile()` luôn validate.
- python-pptx: không nhân bản slide trực tiếp (chỉ `add_slide(layout)`); `text_frame.text=` làm mất định dạng;
  SVG/EMF trong template lỗi (`UnidentifiedImageError`); không auto-reflow như PowerPoint.
- Slide xuất từ Slidev/Marp là **ảnh** (không sửa được chữ) — không dùng khi cần biên tập.

## Template & tài sản kèm theo

- `reference/design-guide.md` — quy tắc bố cục + cỡ chữ chuẩn + cấu trúc deck (đầy đủ).
- `reference/template-sources.md` — nguồn template (Slidesgo, SlidesCarnival, repo GitHub…) + mẹo SVG→PNG.
- `reference/ecosystem.md` — hệ sinh thái repo/skill PPTX high-star (ppt-master ~56k, PptxGenJS, python-pptx…) + ý tưởng nên mượn.
- `assets/make-slides.mjs` — **mẫu generator pptxgenjs**: 16:9, cover có ảnh + blend, section divider, slide số liệu/cards, diagram + text, gộp nhiều sơ đồ, footer + số trang, icon badge, speaker notes. Sửa mảng nội dung rồi chạy.
- `assets/icons/*.png` — icon Tabler (màu nhấn) sẵn dùng, 128px.

### pptxgenjs — mảnh cần nhớ
- 16:9: `pptx.layout='LAYOUT_WIDE'` (13.333×7.5in = 12192000×6858000 EMU).
- Ảnh vừa khung giữ tỉ lệ: `sizing:{type:'contain',w,h}`; phủ kín: `'cover'`. Luôn `existsSync()` trước khi chèn.
- Cover đẹp: panel màu + ảnh bên phải + dải gradient blend ở mép (fill `{type:'gradient',stops,angle}`).
- Mỗi slide: header (ô vuông nhấn + tiêu đề màu nhấn), footer + số trang, `addNotes()` cho speaker notes.
- Gộp nhiều sơ đồ phụ vào 1 slide (trái chú thích, phải 3 sơ đồ dọc) cho deck gọn.

## Format phản hồi cuối

```text
Deck: <file.pptx>
Slides: N
Template: yes/no
Charts: (native/image)
QA:
- Render: PASS/FAIL
- Visual inspection: PASS/FAIL
Known limitations:
- ...
```
