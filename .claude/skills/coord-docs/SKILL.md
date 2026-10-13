---
name: coord-docs
description: Điều phối khối TÀI LIỆU DỰ ÁN & VIẾT/SỬA DOCS: nạp nhanh để lập, viết, sửa, audit tài liệu kỹ thuật và dự án (README, AGENTS.md, docs/, ADR, PRD, knowledge bundle OKF). Gom doc-architect (chủ README), living-docs (chủ ADR), okf-knowledge-format, documentation, documentation-and-adrs, doc-coauthoring, writing-guidelines. Từ khóa: viết docs, sửa docs, README, AGENTS.md, ADR, PRD, tài liệu dự án, tài liệu kỹ thuật, knowledge bundle, OKF, runbook, developer guide.
---

# coord-docs — Điều phối khối Tài liệu Dự án & Viết/Sửa Docs

Nạp để vào khối **tài liệu dự án / docs kỹ thuật / ghi vết quyết định**.

> Bản đồ toàn cục: `skill-coordinator`. Baseline chống mâu thuẫn: `docs/rule-conflicts.md`.

## Khi nào nạp

- Lập / audit / đồng bộ bộ tài liệu dự án (README, AGENTS.md, CONTEXT, docs/, DESIGN).
- Viết / sửa docs kỹ thuật: API docs, runbook, onboarding guide.
- Ghi ADR/PRD/quyết định; đóng gói tri thức OKF.

## Khối gồm

| Skill | Vai trò | Khi nào |
|---|---|---|
| `doc-architect` | **CHỦ template README** + bộ docs dự án, Fresh Session Test | lập/audit bộ docs |
| `living-docs` | **CHỦ ADR/PRD/issue** (supersede, never delete) + sơ đồ Mermaid sống | ghi vết quyết định |
| `okf-knowledge-format` | Bundle markdown + frontmatter `type` | đóng gói tri thức |
| `documentation` | Tài liệu kỹ thuật: API docs, runbook, onboarding | viết docs kỹ thuật |
| `documentation-and-adrs` | ADR dùng chung (defer `living-docs` nếu dùng) | ghi ADR lẻ |
| `doc-coauthoring` | Đồng soạn proposal/spec có kiểm chứng | soạn tài liệu có quy trình |
| `writing-guidelines` | Soát văn phong **docs sản phẩm EN** (Vercel) | audit prose EN |

## Thứ tự nạp & chuỗi

```text
Lập/audit docs → doc-architect (sở hữu cấu trúc README/docs)
 → [quyết định] living-docs (ADR/PRD) ; [tri thức] okf-knowledge-format
 → [lẻ] documentation / documentation-and-adrs / doc-coauthoring
 → [soát EN] writing-guidelines
 → kiểm: living-docs check (nếu dùng) → không còn placeholder khi ship
```

## Quy ước chung

- Owner: README = `doc-architect`; ADR = `living-docs` (khi dùng nó); `writing-guidelines` = docs EN, KHÔNG cho báo cáo học thuật tiếng Việt.
- Không ship placeholder; `living-docs check` chặn cú pháp `{{PLACEHOLDER}}`.

## Anti-patterns

- ❌ Tạo cấu trúc README thứ 3 ngoài template `doc-architect`.
- ❌ Hai quy ước ADR song song (`docs/decisions/` + `docs/adr/`).
- ❌ Áp luật văn phong Vercel (EN) lên báo cáo học thuật.

## Definition of Done

```text
[ ] Đúng owner cho từng artifact (README / ADR / OKF).
[ ] Không drift: index không lệch; không placeholder khi ship.
[ ] docs/ chạy living-docs check (nếu dùng): PASS.
```
