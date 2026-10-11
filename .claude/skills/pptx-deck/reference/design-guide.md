# 09 · Hướng Dẫn Làm Slide PPTX (chuẩn, có ảnh, không bừa)

> Mục tiêu: làm bộ slide thuyết trình BTL **sạch – nhất quán – đúng chuẩn cỡ chữ**, có ảnh chụp app +
> sơ đồ (Mermaid đã render ra PNG/SVG). File `.pptx` mở/sửa được (không phải ảnh dán).

---

## 1. Chọn công cụ

| Công cụ | Ngôn ngữ | Hợp khi | Ảnh | Sửa được trong PowerPoint | Ghi chú |
|---|---|---|---|---|---|
| **PptxGenJS** | JS/TS (Node) | Sinh deck từ code, web/Node | Có (`addImage`) | ✅ | Nhanh, dễ làm theme, khuyến nghị |
| **python-pptx** | Python | Batch deck, đọc template | Có | ✅ | Mạnh về chart; **không embed được font** |
| **Pandoc** | CLI | Viết Markdown → .pptx | Có | ✅ | Cần `--reference-doc` để đẹp |
| **Marp / Slidev** | Node | Talk nhanh, web-first | Có | ❌ (export ra ảnh) | **Không dùng để nộp** nếu cần sửa |
| **reveal.js** | HTML | Web nhúng | Có | ❌ (không có pptx) | Chỉ HTML/PDF |

**Khuyến nghị cho BTL này:** **PptxGenJS** (Node đã có sẵn) — deck sửa được, chèn ảnh/sơ đồ thoải mái.

---

## 2. Quy tắc trình bày & cỡ chữ chuẩn (điểm)

- **Tiêu đề slide:** **36–40 pt** (tối thiểu 28) · **1 dòng** nếu được · ≈ **2× cỡ chữ body**.
- **Tiêu đề phụ / section:** **24–28 pt**.
- **Nội dung / bullet:** **18–24 pt** (sàn 18; lý tưởng 20–24).
- **Chú thích / nguồn / số trang:** **12–16 pt** (không < 12).
- **Nhãn biểu đồ / trục:** 14–18 pt · **bảng:** 16–20 pt.
- **Giới hạn nội dung:** 1 ý / slide · tối đa **6 bullet** · quy tắc **6×6** (≤6 dòng × ≤6 từ). Không đoạn văn dài.
- **Hierarchy:** ≤ **3 cỡ chữ** mỗi slide; ≤ **2 font** cả deck. Body thường (400), tiêu đề đậm (700).
- **Khoảng trắng:** mục tiêu **40–50%** trống; line spacing **1.2–1.5×**; canh lề theo **lưới chung**.
- **Tương phản:** đạt WCAG AA (body ≥ 4.5:1). Tránh font weight mảnh (100–300) — mờ khi chiếu.
- **Lề an toàn:** giữ chữ cách mép ≥ 5% (tránh mất khi chiếu máy khác).
- **Tỉ lệ:** **16:9** native — đặt `slide_width = 13.333in`, `slide_height = 7.5in`
  (EMU: `12192000 × 6858000`). Không kéo giãn ảnh bằng tay (giữ tỉ lệ theo góc).

**Bảng màu gợi ý (khớp nhận diện TMĐT):** Navy `#0E3A47` · Cyan `#0891B2` · Accent `#06B6D4` ·
Nền `#FFFFFF` · Nền phụ `#F1F6F8` · Chữ `#33474F`.

---

## 3. Cấu trúc deck gợi ý (~16–20 slide)

1. Bìa: tên đề tài + logo + tên nhóm/môn.
2. Đặt vấn đề (nghịch lý ship COD).
3. Giải pháp: Ký quỹ Escrow + Tem QR HMAC.
4. Kiến trúc tổng thể — **ảnh `01-kien-truc.png`**.
5. Phân rã chức năng — **ảnh `02-phan-ra-chuc-nang.png`**.
6. Use case — **ảnh `03-use-case.png`**.
7. Luồng nghiệp vụ: Activity quét QR — **ảnh `04-activity-quet-qr.png`**.
8. Sequence: Mua hàng & Escrow — **ảnh `05-...png`**.
9. Sequence: Verify & giải ngân — **ảnh `06-...png`**.
10. Sequence: Nạp tiền SePay — **ảnh `07-...png`**.
11. Mô hình dữ liệu: Class — **ảnh `08-class-diagram.png`**.
12. Vòng đời đơn hàng: State — **ảnh `09-state-don-hang.png`**.
13. ERD — **ảnh `10-erd.png`**.
14. Demo giao diện — ảnh `docs/images/audit/02-trang-chu.png`, `04-gio-hang.png`, `10-admin-tong-quan.png`…
15. Công nghệ & kiểm thử (Jest, Playwright).
16. Kết luận & hướng phát triển · Cảm ơn.

---

## 4. Repo / bài học tham khảo

**Skill (Agent Skills – cài được):**
- `anthropics/skills` → `skills/pptx` — skill PPTX tham chiếu (PptxGenJS + validate/thumbnail).
- `MiniMax-AI/skills` → `pptx-generator` (MIT) — kèm cả **design system** (palette/font/spacing).
- `proyecto26/slides-ai-plugin` → `pptx-slides` — đo chữ (skia-canvas), 12 theme, chống tràn/đè.
- `PHY041/claude-skill-slide-kit` — python-pptx: 17 kiểu slide, theme `academic_minimal`.

**Lib / repo nền:**
- PptxGenJS — https://github.com/gitbrent/PptxGenJS · docs: https://gitbrent.github.io/PptxGenJS/
- python-pptx — https://github.com/scanny/python-pptx
- `serendipitynz/mermaid2pptx` — Mermaid → shape PPTX chỉnh sửa được (tránh ảnh mờ).

**Bài học thiết kế slide (đọc để làm đúng):**
- Garr Reynolds "Presentation Zen" · Nancy Duarte "slide:ology".
- Quy tắc 10/20/30 (Kawasaki) & 6×6.

**Markdown → PPTX (nếu thích viết nhanh):** Pandoc `--reference-doc`, Quarto `reference-doc`.

---

## 5. Quy trình đề xuất (PptxGenJS)

```bash
cd tools/slides
npm install            # cài pptxgenjs
node make-slides.mjs   # xuất ra docs/slides/TMDT_slides.pptx
```

Script mẫu xem tại `tools/slides/make-slides.mjs` (đã tạo kèm): 16:9, theme TMĐT, chèn sẵn
sơ đồ + ảnh chụp, cỡ chữ chuẩn (title 38pt, body 20pt). Chỉnh nội dung tại mảng `SLIDES`.

---

## 6. Cần tránh (pitfalls)

- **Font tiếng Việt:** PptxGenJS/python-pptx **không nhúng font**. Dùng font có sẵn máy chiếu:
  **Calibri / Arial** (an toàn) hoặc **Be Vietnam Pro** (đẹp, dấu tốt) — nhưng nếu máy khác thiếu font
  sẽ tự đổi. Chốt: dùng **Calibri** cho chắc, hoặc cài Be Vietnam Pro ở mọi máy.
- **Ảnh sơ đồ:** export ở **scale ≥ 2–3** (`mmdc -s 3`) hoặc dùng **SVG** cho nét. PNG mờ khi kéo to.
- **Tràn chữ:** kiểm tra bằng cách xuất PDF (`soffice --headless --convert-to pdf`) và soi từng slide.
- **Tỉ lệ ảnh:** luôn giữ tỉ lệ; đặt ảnh trong khung cố định (fit), đừng kéo méo.
- **Không dán cả đoạn văn** lên slide — cắt còn ý chính; chi tiết để người thuyết trình nói.

---

## 7. Checklist trước khi nộp

- [ ] 16:9, nhất quán nền + dải màu thương hiệu.
- [ ] Title ≥ 28pt, body ≥ 18pt, không chữ < 12pt.
- [ ] Mỗi slide 1 ý; ≤6 bullet; không slide nào dày đặc.
- [ ] Ảnh sơ đồ/ảnh chụp nét, đúng tỉ lệ, không vỡ.
- [ ] Font tiếng Việt hiển thị đúng trên máy chiếu.
- [ ] Đã xuất PDF & xem lại toàn bộ.
