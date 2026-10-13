---
name: coord-slides
description: Điều phối khối SLIDE / THUYẾT TRÌNH (PowerPoint .pptx): nạp nhanh để làm, sửa, làm đẹp, tái tạo slide, chuyển tài liệu PDF/Word sang PPT, thêm narration/animation. Gom pptx-deck (slide cơ bản), pptx (thao tác OOXML), ppt-master (native cao cấp), theme-factory (màu/font), anti-slop (chống AI slop). Từ khóa kích hoạt: làm slide, thuyết trình, PowerPoint, pptx, deck, bảo vệ đồ án, beautify slide, PDF sang PPT, tái tạo slide.
---

# coord-slides — Điều phối khối Slide / Thuyết trình

> Bản đồ toàn cục: `skill-coordinator`. Baseline chống mâu thuẫn: `docs/rule-conflicts.md`.

## Khi nào nạp

- Tạo / sửa / làm đẹp slide; chuyển PDF/Word → PPT; dựng deck bảo vệ đồ án.

## Khối gồm

| Skill | Vai trò | Khi nào |
|---|---|---|
| `pptx-deck` | **CHỦ (deck cơ bản)**: template, bố cục, chart native, speaker notes | slide thường |
| `ppt-master` | **CHỦ (native cao cấp)**: chuyển tài liệu→slide, tái tạo, beautify, animation, TTS | deck đẳng cấp |
| `pptx` | Thao tác OOXML/pptxgenjs chuyên sâu (template, chart, QA) | case nâng cao |
| `theme-factory` | Áp theme màu/font (**branded/marketing**) | khi cần theme |
| `anti-slop` | Chặn AI slop (accent line, glass, gradient tím-xanh...) | kiểm thẩm mỹ |

## Thứ tự nạp & chuỗi

```text
pptx-deck / ppt-master (chủ)
 → [sơ đồ trong slide] coord-diagrams → diagram-auditor
 → theme-factory (màu/font — chỉ branded) → anti-slop (bố cục) → render QA
```

## Cổng (gate)

- Render + soi ảnh / QA bắt buộc (AGENTS #2). Với `ppt-master` trong repo này: **bật `visual-review`**.

## Quy ước chung

- Accent line / stripe: **chỉ** trong brand/style template tường minh; KHÔNG cho deck học thuật.
- Font: "PPT-safe" (ppt-master) ≠ "LibreOffice-QA-safe" (pptx); nghi ngờ → Arial / Calibri / Cambria / Times New Roman.
- Số liệu minh hoạ phải gắn nhãn `Scenario data`.

## Anti-patterns

- ❌ Gradient tím-xanh / glass mặc định; accent line dưới tiêu đề.
- ❌ Tin font QA khi render bằng LibreOffice.
- ❌ Chỉ tạo file mà không render/soi.

## Definition of Done

```text
[ ] Đúng chủ (pptx-deck vs ppt-master) theo yêu cầu.
[ ] Sơ đồ (nếu có) qua diagram-auditor.
[ ] Render + soi ảnh / QA: PASS.
```
