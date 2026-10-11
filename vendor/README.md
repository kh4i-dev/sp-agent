# vendor/ — Repo agent-skill tham khảo (KHÔNG auto-load)

Thư mục này chứa các repo **bên thứ ba** clone về để tham chiếu/đọc nội dung.
**Không phải skill của sp-agent** — agent KHÔNG tự nạp các `SKILL.md` ở đây.
Muốn dùng như skill thật thì copy thủ công vào `.claude/skills/<name>/` rồi chạy
`tools/sync-skills.ps1`.

Clone bằng `git clone --depth 1` (lịch sử rút gọn). Các repo vẫn giữ `.git` để có thể
`git -C vendor/<repo> pull` cập nhật.

| Thư mục | Repo | Commit | Ngày | License |
|---|---|---|---|---|
| `python-docx-editor/` | martinderm/python-docx-editor | `e994b2b` | 2026-09-09 | GPL-3.0 |
| `anti-slop/` | miqdadbadjuber/anti-slop | `388cbe3` | 2026-10-05 | MIT |
| `unslop-ui/` | yuwen-lu/unslop-ui | `df1e58a` | 2026-04-06 | MIT |
| `no-slop-ui/` | LeoStehlik/no-slop-ui | `3c8f9e5` | 2026-08-31 | xem `LICENSE` |
| `markdown-viewer-skills/` | markdown-viewer/skills | `2672b69` | 2026-10-06 | xem `LICENSE` |
| `plantuml-skill/` | fa-ina-tic/plantuml-skill | `d78ab89` | 2026-07-20 | xem `LICENSE` |
| `spillwave-plantuml/` | SpillwaveSolutions/plantuml | `8aa811c` | 2026-08-24 | xem `LICENSE` |

## Có gì trong từng repo

- **python-docx-editor** — CLI sửa `.docx` an toàn cho AI agent: trích JSON (`docx-structure.v2`),
  patch có guard, Markdown↔DOCX, fill ô bảng. `SKILL.md` + `scripts/` + `references/`.
  → bổ trợ skill `docx-report`.
- **anti-slop** — hệ thống 6 skill anti-slop: `skills/antislop` (core) + `antislop-ui`,
  `antislop-copywriting`, `antislop-human`, `antislop-layoutmobile`, `antislop-code`.
  → bản tinh gọn đã nằm ở skill `anti-slop` của project; repo này để tra cứu đầy đủ.
- **unslop-ui** — skill nhỏ chống AI-slop UI; có `examples/` ảnh before/after.
- **no-slop-ui** — skill no-slop-ui: `references/banned-patterns.md`, `references/colour-palettes.md`.
- **markdown-viewer-skills** — bộ skill tài liệu/hình. **Lưu ý:** mục 7 của
  `mermaid-diagrams/reference/visual-style.md` ghi có `uml/SKILL.md`, nhưng bản hiện tại
  (`2672b69`) KHÔNG có thư mục `uml/` — chỉ có `documd-visuals/`, `research/`, `scripts/`.
  `SKILL.md` UML đã không còn ở repo này.
- **plantuml-skill** — biến mô tả → `.puml`, render PNG/SVG qua Kroki (không cần Java).
  Skill tại `skills/plantuml-skill/SKILL.md`.
- **spillwave-plantuml** — skill PlantUML + ví dụ theo loại app; `SKILL.md`, `SKILL-PDA.md`,
  `references/`, `examples/`, `scripts/`.

> `ppt-master` (hugohe3/ppt-master) KHÔNG nằm trong `vendor/`: nó đã được cài là skill thật
> tại `.claude/skills/ppt-master/` (v6.7.0, MIT).
