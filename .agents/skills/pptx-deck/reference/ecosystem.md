# Hệ sinh thái PPTX — repo & skill tham khảo (high-star)

> Nguồn cho việc tạo/sửa slide `.pptx` biên tập được. Số ⭐ là ước lượng tại 2026-10.
> Nguồn template + icon đã có riêng ở `reference/template-sources.md`.

## Ngôi sao dẫn đầu

| Repo | ⭐ | Vai trò |
|---|---|---|
| `hugohe3/ppt-master` | **~56.1k** | **Đáng tham chiếu nhất.** AI biến tài liệu (PDF/DOCX/web) → `.pptx` **native** bằng pipeline **SVG → PPTX**: shape/transition/animation gốc, chart & bảng có dữ liệu, audio narration từ speaker notes, import `.pptx` template của bạn. Là một *skill* chạy trong agent; có CLI (`uvx ppt-master <cmd>`): `project`, `pdf-to-md`, `doc-to-md`, `web-to-md`, `finalize-svg`, `svg-to-pptx`, `image-gen`, `latex-render`, `svg-quality-check`, `visual-review`… MIT. |
| `gitbrent/PptxGenJS` | ~3.5k | Thư viện JS tạo PPTX (Node/React/browser) — sp-agent dùng. Chart native OOXML. |
| `scanny/python-pptx` | ~2.7k | Thư viện Python đọc/tạo/sửa PPTX. |
| `slidevjs/slidev` | ~32k | Slide bằng Markdown cho dev. **Lưu ý:** export ra PDF/PNG → chữ thành ảnh, không biên tập được. |
| `marp-team/marp` | ~9k | Markdown → slide (dùng cho deck đơn giản; cũng ra ảnh khi export). |

## Bổ trợ đáng chú ý

| Repo | Vai trò |
|---|---|
| `betteroffice-pptx` (Rust, PyPI) | Layout slide từ Python: line breaking, text metrics, display list, CRDT merge — lấp khoảng trống python-pptx không layout được. |
| `harshankur/officeParser` | Parse `.pptx/.docx/.xlsx…` → AST, convert HTML/PDF/Markdown; hữu ích để kiểm tra nội dung deck. |
| `atomiechen/THU-PPT-Theme` | Theme học thuật flat (mô phỏng: ô vuông + dải dọc + tiêu đề màu nhấn). |
| `aresplus/tech-slides-generator`, `lionelwust/openwebui-generate-slides`, `SamyGenAI/Smart-creator-design-system` | Skill/engine python-pptx với layout + icon (chi tiết trong `template-sources.md`). |
| `elvisw/ppt-master` (PyPI fork) | Bản fork đóng gói `uvx ppt-master` (kèm skill + template + icon). |

## Ý tưởng nên mượn cho `pptx-deck`

- **Pipeline SVG → PPTX** của `ppt-master`: dựng từng slide bằng SVG (dễ kiểm soát bố cục +
  tự soi render), rồi convert sang shape native. Bổ trợ cho nhánh `pptxgenjs` hiện có.
- **Speaker notes → audio narration** (TTS) khi cần deck tự thuyết minh.
- **Import template `.pptx`** giữ design gốc: dùng khi map nội dung vào template có sẵn.
- **Đừng convert EMF/WMF → PNG**: giữ tham chiếu gốc để PowerPoint render vector (ppt-master).
- **Visual review tự động** bằng Playwright sau render.

## Bản clone / cài trong project

- `ppt-master` — đã cài **skill thật** ở `.claude/skills/ppt-master/` (v6.7.0, MIT), không nằm trong `vendor/`.
- Anti-slop cho bố cục slide: skill `anti-slop` của project; repo đầy đủ ở `vendor/anti-slop/`,
  `vendor/unslop-ui/`, `vendor/no-slop-ui/` (không auto-load).

## Cảnh báo giữ nguyên từ skill gốc

- Slide xuất từ Slidev/Marp là **ảnh** — không dùng khi cần sửa chữ.
- Luôn render (PowerPoint COM / LibreOffice) và soi từng slide trước khi giao.
