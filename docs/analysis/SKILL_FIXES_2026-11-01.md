# Tóm tắt sửa skill `use-case-layout` — 2026-11-01

## Vấn đề đã xác minh từ audit

### Từ `use-case-include-extend-inheritance.md`

**Lỗi mô hình:**
1. Skill nói "quan hệ nếu có căn cứ" nhưng không có **test 1 câu bắt buộc** để quyết định include/extend/generalization.
2. Không phân biệt "included use case có actor riêng khởi tạo độc lập" ≠ include (phải là association).
3. Không có **bảng traceability** để xác minh từng quan hệ trước khi vẽ.
4. Anti-pattern kế thừa (`Auditor --|> Viewer`) không được liệt kê cụ thể.

**Sửa:**
- ✅ Nâng `include-extend-inheritance.md` thành **SSOT đầy đủ** (§0–6, bảng test 1 câu, anti-pattern, traceability mẫu).
- ✅ Ghi vào SKILL.md Bước 1: **bảng traceability bắt buộc** + test 1 câu cho mỗi quan hệ.
- ✅ Thêm chỉ thị §6 (Agent): "Quan hệ UML phải có lý do" + trỏ tới `include-extend-inheritance.md` §1.

### Từ `state-skill-audit-2026-11-01.md`

**Lỗi kiểm chứng (không ảnh hưởng trực tiếp use-case-layout):**
- State Machine: P1 lỗi model, P2 lỗi hình học.
- Đã sửa: bộ kiểm model từ assert → ValueError (luôn hoạt động với `-O`), kiểm composite/cycle đầy đủ, xuất SVG/drawio nhất quán.

**Bài học cho use-case-layout:**
- Visual Review phải **chạy script + mở ảnh** (2 nhịp), không được chỉ 1 trong 2.
- Mô hình SAI nhưng hình vẽ đẹp → vẫn FAIL (lỗi Semantic, không phải Visual).

### Từ `btl-cnpm-usecase-audit/audit.md`

**6 lỗi P1/P2 đã xác minh:**

| Lỗi | Mức | Nguyên nhân | Sửa trong skill |
|---|---|---|---|
| Generator bỏ qua `side` actor, ép mọi vai trò về trái | P1 | Code viết `(name, indices, _)` bỏ qua trường `side` | Thêm **Hợp đồng Generator** (§3.4 SKILL.md) — giữ `side` L/R |
| Mọi UC chính một cột + nửa phải trống | P1 | Layout `y += hằng số` cho mọi hàng | Bộ cục **cụm luồng** với nhịp giữa cụm ≥ 2× (§3.2b) |
| Gốc association không gắn vào thân actor trên SVG | P1 | SVG neo `(x+22, y)` cạnh thân; draw.io không khóa `entryPerimeter=0` | Neo thân/bụng `exitY 0.667`; SVG ↔ draw.io đồng bộ điểm chạm |
| SVG + drawio không cùng điểm chạm ellipse | P1 | SVG dùng mép trái cố định; draw.io dùng `entryX=0.5` | Tính giao điểm tia–ellipse theo hướng cạnh; khóa tọa độ 2 định dạng |
| Tài liệu audit trỏ bản v6 không còn tồn tại | P2 | Link cũ hư; gây nhầm khi cập nhật | Chọn bộ hiện hành, sửa liên kết |
| Nhiều Bước 0 mâu thuẫn quyền IT/Admin | P2 | 2+ file step0 khác nhau trong cùng dự án; agent chọn nhầm | **Một** Bước 0 bản hiện hành; báo trong CONTEXT.md |

**Sửa trong skill:**
- ✅ Thêm **Hợp đồng Generator** (§3.4): giữ `side`, neo thân, entry ellipse tính giao điểm, cấm 1 cột duyc.
- ✅ Nhấn mạnh **bố cục cụm** (§3.2b): nhịp giữa cụm ≥ 2× nhịp trong cụm.
- ✅ Thêm **bẫy 3 bài học** vào `pitfalls.md` (§HIGH × 2, §MEDIUM).

## Các file đã sửa

1. **`.claude/skills/use-case-layout/reference/include-extend-inheritance.md`** — SSOT đầy đủ
   - Thêm §0 (tại sao cần), §2 (bảng so sánh include ↔ extend), §3.2 (anti-pattern), §4 (hệ thống ngoài), §5 (traceability mẫu), §6 (checklist).
   - Bảng test 1 câu rõ ràng; bảng traceability mẫu + quy tắc included-use-case-không-có-actor-riêng.

2. **`.claude/skills/use-case-layout/SKILL.md`** — Bước 1 + §6
   - Bước 1: thêm "**bảng traceability bắt buộc**" + test 1 câu.
   - Quy tắc quan hệ: nhấn mạnh include/extend/generalization với trỏ tới reference.
   - §3.4: thêm **Hợp đồng Generator** — 5 quy tắc bắt buộc cho script tự viết (giữ `side`, neo thân, entry ellipse đồng bộ, cấm 1 cột, render+soi bắt buộc).
   - §6: thêm chỉ thị "Quan hệ UML phải có lý do" + trỏ reference.

3. **`.claude/skills/use-case-layout/reference/pitfalls.md`** — 3 bài học mới
   - [IRON] Con nhện: đã có từ lần audit trước; ghi lại context.
   - [HIGH] Generator bỏ qua `side` + neo lộn xộn (btl-cnpm 2026-11-01).
   - [HIGH] `<<include>>` ≠ proof of implementation (phân biệt intent vs code hiện thực).
   - [MEDIUM] Nhiều Bước 0 mâu thuẫn cùng dự án.

4. **`.agents/skills/use-case-layout/`** — Sync tất cả file từ `.claude`

## Checklist sửa hoàn tất

- [x] Nâng `include-extend-inheritance.md` thành SSOT đầy đủ (§0–6)
- [x] Bước 1 (SKILL.md): bảng traceability + test 1 câu bắt buộc
- [x] Quy tắc quan hệ: include/extend/generalization có lý do + trỏ reference
- [x] §3.4: Hợp đồng Generator (5 quy tắc)
- [x] §6: Chỉ thị ngắn về UML + reference
- [x] `pitfalls.md`: 3 bài học mới từ audit btl-cnpm
- [x] Sync `.agents/skills/use-case-layout/` từ `.claude`

## Không trong phạm vi sửa (để sau)

- Sửa generator `gen_usecase.py` của btl-cnpm (scope: skill, không dự án cụ thể)
- Render lại 4 slide Use Case btl-cnpm (người dùng quyết định khi áp skill)
- Update AGENTS.md (tham chiếu skill, không phải file skill)
- Audit State Machine chi tiết (scope riêng, đã có state-skill-audit-2026-11-01.md)

---

**Ngày:** 2026-11-01  
**Agent:** Sửa skill theo audit lỗi từ `docs/analysis`  
**Status:** ✅ Hoàn tất skill; sẵn sàng cho `skill-feedback` hoặc audit lỗi tiếp theo
