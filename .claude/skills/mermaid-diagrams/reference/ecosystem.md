# Hệ sinh thái sơ đồ — repo & công cụ tham khảo (high-star)

> Nguồn cho diagram-as-code. Số ⭐ ước lượng tại 2026-10. Danh sách skill/PlantUML chi tiết
> đã có ở mục 7 của `reference/visual-style.md` — file này bổ sung phần công cụ lõi + render.

## Mermaid (mặc định của skill này)

| Repo / công cụ | ⭐ | Vai trò |
|---|---|---|
| `mermaid-js/mermaid` | ~90k | Engine vẽ sơ đồ từ text (flowchart, sequence, class, state, ER, gantt, mindmap…). Render native trên GitHub/` ```mermaid `. |
| `mermaid-js/mermaid-cli` (`mmdc`) | ~5k | CLI: `.mmd` → SVG/PNG/PDF (Puppeteer). sp-agent dùng qua `npx -p @mermaid-js/mermaid-cli mmdc …`. |
| `coolamit/mermaid-cli` | — | Bản Go, một binary tĩnh, **không cần Node** (vẫn cần Chrome/Chromium). Thay thế khi môi trường thiếu Node. |
| `mermaid-live-editor` | ~6.8k | Editor online: preview + export PNG/SVG. |

## Công cụ khác (khi Mermaid không đủ)

| Công cụ | Vai trò |
|---|---|
| PlantUML (`plantuml.com`) | UML chuẩn: Use Case, Component, Deployment, Timing, Wireframe. Có skill riêng (xem `visual-style.md`). |
| D2 (`terrastruct/d2`) | Kiến trúc container/edge phức tạp; render server-side, không cần browser. |
| Graphviz (`dot`) | Graph phân cấp, style cổ nhưng mạnh. |
| DBML / dbdiagram.io | ERD nhiều bảng (>12) — gọn, đẹp hơn `erDiagram`. |
| Kroki (`kroki.io`) | Render server-side nhiều định dạng qua HTTP POST — không cần cài gì, cần mạng. |

## Render nhanh (nhắc lại)

```bash
# Mermaid CLI (offline, cần Node + Chrome)
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg
# PNG nền trắng, neutral, scale 2x, theo config của skill
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.png -c assets/mermaid.config.json -b white -s 2
```

- Thiếu sandbox (CI/container): thêm `-p puppeteer-config.json` với `{"args":["--no-sandbox"]}`.
- Không có Node: dùng `coolamit/mermaid-cli` (Go) hoặc Kroki.

## Bản clone trong project (`vendor/`, không auto-load)

- `vendor/plantuml-skill/` — `fa-ina-tic/plantuml-skill` (commit `d78ab89`); skill ở
  `skills/plantuml-skill/SKILL.md`, render qua Kroki.
- `vendor/spillwave-plantuml/` — `SpillwaveSolutions/plantuml` (commit `8aa811c`); `SKILL.md` +
  `references/` + `examples/` theo loại app.
- `vendor/markdown-viewer-skills/` — `markdown-viewer/skills` (commit `2672b69`).
  **Sửa lại thông tin cũ:** mục 7 của `visual-style.md` ghi repo này có `uml/SKILL.md`, nhưng bản
  hiện tại KHÔNG còn thư mục `uml/` (chỉ có `documd-visuals/`, `research/`, `scripts/`).

## Ý tưởng nên mượn

- **Validate bằng render thật** (→ file tạm rồi xoá) trước khi xuất chính thức.
- **Tỉ lệ ảnh**: tránh sơ đồ quá dẹt/cao khi nhúng slide — xem `reference/visual-style.md`.
- **Một sơ đồ một ý**; hệ lớn → bộ sơ đồ nhỏ, lưu `.mmd` trong git để tái sinh.
