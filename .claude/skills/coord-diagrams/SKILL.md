---
name: coord-diagrams
description: Điều phối khối SƠ ĐỒ KỸ THUẬT: nạp nhanh để vẽ Use Case/UML/ERD/Class/Sequence/Activity/State, cây/trie/bk-tree, kiến trúc, flowchart, luồng dữ liệu. Gom diagram-orchestrator (SSOT + chọn công cụ), plantuml-diagrams, tldraw-diagrams, simplified-diagrams, use-case-layout, diagram-design (branded) và diagram-auditor (GATE). Từ khóa kích hoạt: vẽ sơ đồ, use case, UML, ERD, class diagram, sequence, activity, state machine, kiến trúc, flowchart, trie, bk-tree, plantuml, tldraw, audit sơ đồ.
---

# coord-diagrams — Điều phối khối Sơ đồ Kỹ thuật

Nạp để vào khối **sơ đồ** với đúng công cụ + qua cổng kiểm định.

> **SSOT quy tắc sơ đồ:** `diagram-orchestrator` (khối "Đồng bộ quy tắc liên skill"). Baseline: `docs/rule-conflicts.md`.

## Khi nào nạp

- Vẽ sơ đồ UML / Use Case / ERD / Class / Sequence / Activity / State, cây-trie-bk-tree, kiến trúc, flowchart, luồng dữ liệu.

## Khối gồm

| Skill | Vai trò | Khi nào |
|---|---|---|
| `diagram-orchestrator` | **CHỦ / SSOT**: phân tích ngữ nghĩa, chọn công cụ, giao thức | luôn nạp đầu |
| `plantuml-diagrams` | UML/ERD/Sequence/Activity/Class/Use Case chuẩn, trắng-đen | sơ đồ chuẩn mực |
| `tldraw-diagrams` | Kiến trúc/flowchart nét cong mềm, `.tldr` sửa được | sơ đồ tự do đẹp |
| `simplified-diagrams` | Sơ đồ khái niệm 5–9 thực thể cho slide/bảo vệ | cần tinh gọn |
| `use-case-layout` | Use Case đúng nghiệp vụ + lane gọn, cấm vòng xa | Use Case nhiều actor |
| `diagram-design` | Sơ đồ **branded/presentational (được màu)** HTML/SVG | marketing, KHÔNG báo cáo |
| `diagram-auditor` | **GATE**: Semantic + Visual Review, zero-color, proof-of-view | trước khi chèn |

## Thứ tự nạp & chuỗi

```text
diagram-orchestrator (phân tích → chọn công cụ + Bước 0 nếu Use Case/domain)
 → <tool>: plantuml / tldraw / simplified / use-case-layout / diagram-design
 → diagram-auditor (GATE: PASS mới được chèn vào docx/pptx)
```

## Cổng (gate)

- `diagram-auditor` là **cổng bắt buộc** cho mọi sơ đồ học thuật.
- Bước 0 (Use Case/domain): `docs/domain/step0-<du-an>.md` — thiếu → **BLOCKED**.

## Quy ước chung (SSOT)

- Báo cáo học thuật = **zero-color**; branded mới được dùng màu.
- **Không nhúng tiêu đề** trong ảnh; caption do `docx-report` sinh (`Hình X.Y: ...`).
- Ratio khuyến nghị 0.5–2.4 (hard-fail `>3.8` / `<0.28`); node ≤ 15 (chi tiết) / ≤ 9 (khái niệm); chữ ≥ 9pt; lưu `docs/diagrams/` (nguồn + `.svg` + `.png`).

## Anti-patterns

- ❌ Vẽ Use Case/domain khi chưa có Bước 0.
- ❌ Dùng màu cho sơ đồ đồ án; nhúng title trong ảnh.
- ❌ Chèn sơ đồ chưa qua `diagram-auditor`.

## Definition of Done

```text
[ ] Đúng công cụ theo ngữ nghĩa (orchestrator).
[ ] Có tệp nguồn (.puml/.dot/.tldr/.drawio) + .svg + .png.
[ ] diagram-auditor: PASS (Semantic + Visual + proof-of-view).
```
