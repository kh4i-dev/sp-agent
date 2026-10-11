---
name: mermaid-diagrams
description: Vẽ sơ đồ kỹ thuật dạng code (diagram-as-code): Mermaid và PlantUML cho Use Case, Class, Activity, Sequence, State, ERD, kiến trúc (C4), flowchart, Gantt; render ra SVG/PNG/PDF và nhúng vào DOCX/PPTX/Markdown. Dùng khi người dùng cần sơ đồ, biểu đồ, UML, ERD, mermaid, plantuml, use case, class diagram, sequence, kiến trúc hệ thống.
---

# Mermaid Diagrams Skill — Sơ đồ as-code

Mục tiêu: sơ đồ **rõ ràng, đọc được, đúng loại**, render thành công và tái sử dụng được (lưu `.mmd` trong git).

## Khi nào dùng

- Vẽ sơ đồ nghiệp vụ/kỹ thuật cho báo cáo, slide, README.
- Chuyển mô tả bằng lời thành Use Case / ERD / Sequence / kiến trúc.
- Sinh sơ đồ minh họa tài liệu PTTKHT (phân tích & thiết kế hệ thống).

## Chọn công cụ theo loại sơ đồ

| Sơ đồ | Khuyến nghị | Ghi chú |
|---|---|---|
| Flowchart, Sequence, Class, State, ER, Gantt, C4 (beta) | **Mermaid** | render native trên GitHub |
| Use Case UML chuẩn, Component, Deployment, Timing, Wireframe | **PlantUML** | Mermaid chỉ có use-case **beta** |
| Kiến trúc có container/edge phức tạp | **D2** hoặc **Graphviz** | D2 render server-side, không cần browser |
| Graph phân cấp lập trình | **Graphviz (dot)** | mạnh, style cũ |

> Với đồ án nhúng Word: Mermaid cho sơ đồ phổ biến; **Use Case** nên cân nhắc PlantUML
> hoặc dùng cú pháp `usecase-beta` của Mermaid rồi render và soi lại.

## Mermaid CLI (`mmdc`)

```bash
# Không cần cài global:
npx -p @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.svg

# Render PNG nền trong, theme neutral, scale 2x:
npx -p @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.png -t neutral -b transparent -s 2

# Kiểm tra cú pháp bằng cách render vào file tạm rồi xoá
npx -p @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o check.svg
```

- `-t` theme: `default | neutral | dark | forest | base`.
- `-b` nền: `transparent` hoặc mã màu.
- `-s` scale (PNG), `--cssFile` để tùy biến, `--configFile` cho `mermaid.json`.
- Cần Chrome/Chromium (Puppeteer đi kèm). Trên môi trường thiếu sandbox:
  truyền `-p puppeteer-config.json` với `{"args":["--no-sandbox"]}`.

## Quy tắc sơ đồ cho agent

- **Một sơ đồ một ý.** Hệ lớn → chia thành **bộ sơ đồ nhỏ**, không dồn một chart khổng lồ.
- Chọn loại theo ý định (hành vi → sequence/activity; cấu trúc → class/ER; luồng → flowchart).
- Nút/edge tối thiểu; tên nút khớp tên trong code/DB.
- Đặt hướng: `TD` cho phân cấp, `LR` cho luồng.
- Nhóm bằng `subgraph` khi có module.
- Tránh cạnh cắt nhau; nhãn ngắn, dễ đọc.
- Validate cú pháp trước khi export; sau đó **tự soi ảnh render** (kể cả dùng khả năng "nhìn" ảnh),
  sửa tối đa ~2 vòng.

## Lỗi cú pháp thường gặp (phải nhớ)

- `end` viết thường phá flowchart/sequence — phải quote: `"end"` hoặc `(end)` / `[end]`.
- Node ID bắt đầu bằng `o` hoặc `x` tạo cạnh tròn/chéo ngoài ý muốn — thêm space hoặc viết hoa.
- Quote nhãn chứa `: { } [ ] < > '`; escape bằng mã HTML entity (`#35;`).
- Directive `%%{init: ...}%%` **deprecated từ v10.5** — dùng **YAML frontmatter** (`---` … `---`) với key `config`.
- `classDef` / `class` chỉ có tác dụng trong flowchart/graph; sequence/class/ER bỏ qua (chỉ theme toàn cục).
- Subgraph styling cần ID không quote: `subgraph MyLayer["Label"]`.
- ID dành riêng: `end`, `class`, `style`, `click`, `graph`, `subgraph`.
- Accessibility: `accTitle` / `accDescr` được hỗ trợ cho **mọi** loại sơ đồ.

## Nhúng vào tài liệu

- **Markdown/GitHub**: giữ nguyên fence ` ```mermaid ` để render native.
- **DOCX/PPTX/PDF**: convert `.mmd` → PNG/SVG bằng `mmdc` rồi chèn ảnh.
  - pandoc + `mermaid-filter` cũng được (`format=svg|png`, `#fig:id` cho cross-ref).
  - Quarto render `{mermaid}`/`{dot}` native cho pdf/docx.
- Lưu cặp `Hình X.Y. <mô tả>` theo skill `docx-report` (caption dưới hình).

## RENDER & QA

```text
Viết .mmd → validate (render ra file tạm) → render PNG/SVG (theme neutral)
→ mở ảnh, soi nhãn bị cắt / layout chật / cạnh chồng → sửa (≤2 vòng)
→ nhúng vào tài liệu → cập nhật caption/cross-ref
```

## Format phản hồi cuối

```text
Diagrams:
- <tên>.mmd (type) → <tên>.svg/png
Placement:
- Hình X.Y (file chèn)
QA:
- Syntax: PASS/FAIL
- Visual: PASS/FAIL
```

Chi tiết cú pháp từng loại sơ đồ: xem `reference/diagram-types.md`.
Công cụ & repo high-star (mermaid ~90k, mmdc, bản Go không cần Node, D2/PlantUML/DBML/Kroki): `reference/ecosystem.md`.

## Style mặc định (flat, nền trắng)

Config kèm theo: `assets/mermaid.config.json` (theme `base`, `look: classic`, viền mảnh nhạt, nền trắng) — tránh "hộp neo" nổi màu và đổ bóng.

```bash
npx -p @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.png -c assets/mermaid.config.json -b white -s 2
```

- **Tỉ lệ ảnh rất quan trọng**: sơ đồ quá dẹt (ratio ≳ 5) hoặc quá cao (ratio ≲ 0.5) sẽ bị nhỏ xíu khi nhét vào slide.
  Cân đối bằng: đổi hướng (`TD` ↔ `LR`), gom `subgraph`, hoặc dùng liên kết ẩn `~~~` để xếp cột.
- Sau khi render, **tự soi ảnh** (dùng khả năng nhìn ảnh) để bắt chữ tràn/nhỏ, sửa ≤2 vòng.
- Chi tiết: `reference/visual-style.md`.
