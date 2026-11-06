---
name: skill-feedback
description: Vòng lặp phản hồi skill — khi agent ĐANG làm theo một skill và gặp lỗi/biến chứng/workaround mà skill đó CHƯA nói đến, agent phải xác minh rồi đóng góp bài học đó NGƯỢC LẠI VÀO skill (bài học sống thẳng trong skill, cập nhật bản đồ lessons-learned, verify + sync). Dùng khi: gặp lỗi khi chạy theo skill, tìm ra cách làm đúng khác tài liệu, skill thiếu hướng dẫn, lỗi lặp lại nhiều phiên, "đóng góp lỗi vào skill", "ghi bài học vào skill", "skill feedback", "pitfall", "skill chưa nói lỗi này".
---

# Skill Feedback — Đóng góp lỗi thật trở lại vào skill

Mục tiêu: mỗi lỗi agent từng mắc khi chạy theo một skill phải trở thành tri thức **ngay trong skill đó**, để phiên sau không lặp. Skill thiếu bài học = skill chưa hoàn thiện; người phát hiện lỗi có trách nhiệm vá nó.

> [!IMPORTANT]
> Nguyên tắc gốc: **BÀI HỌC SỐNG THẲNG TRONG SKILL** (đồng bộ `docs/lessons-learned.md` — file đó chỉ là bản đồ, không phải kho thứ hai). Chỉ ghi cái ĐÃ XÁC MINH; chưa xác minh mà đáng nhớ thì ghi kèm `[UNVERIFIED]`, cấm ghi như thể đã chứng minh.

---

## 1. Khi nào kích hoạt

Kích hoạt khi **đồng thời đủ 3 điều kiện**:

1. Đang thực thi theo skill X (đã nạp `SKILL.md` của X).
2. Gặp một trong: lỗi, kết quả sai so với skill mô tả, mất thời gian vì một bẫy, hoặc tìm ra cách làm đúng mà skill không ghi.
3. Tra `SKILL.md` + `reference/` + `scripts/` của X (grep từ khóa triệu chứng) — **không thấy nói đến**.

KHÔNG kích hoạt khi:
- Lỗi do thực thi sai skill đã ghi rõ (đó là lỗi của agent, không phải thiếu tài liệu) — vẫn có thể đóng góp nếu skill viết chưa đủ rõ để tránh hiểu nhầm.
- Lỗi môi trường một-off, hết ngay sau restart (chỉ ghi nếu lặp ≥ 2 lần).

**Ghi nháp NGAY khi phát hiện** (triệu chứng + ngữ cảnh + lệnh) — ngữ cảnh lỗi dễ bay hơi, đừng đợi cuối phiên.

---

## 2. Quy trình 6 bước (đúng thứ tự)

1. **Ghi nháp candidate**: skill nào, triệu chứng, lệnh/output lỗi, điều kiện tái lập.
2. **XÁC MINH trước khi ghi** (Evidence-before-Done): tái lập được + cách sửa đã chạy thử PASS. Bằng chứng = lệnh + output ngắn nhất. Chưa xác minh được mà đáng nhớ → ghi kèm `[UNVERIFIED]` + điều kiện cần kiểm.
3. **Chống trùng**: grep `SKILL.md` + `reference/` + `scripts/` của X, và bảng `docs/lessons-learned.md`. Đã có → không ghi; bản cũ thiếu chi tiết thì **CẬP NHẬT tại chỗ** (minimal patch), không thêm bản sao.
4. **Ghi vào ĐÚNG NƠI** (mục 3), đúng mức severity (mục 4), ≤ 12 dòng, kèm bằng chứng.
5. **Cập nhật bản đồ + kiểm định + đồng bộ**: thêm 1 dòng vào bảng `docs/lessons-learned.md` → chạy `tools/verify-skills.ps1` → chạy `tools/sync-skills.ps1`.
6. **Báo người dùng 1 dòng**: đã đóng góp gì vào skill nào (không dán nguyên entry dài ra chat).

Có thể dùng script hỗ trợ ghi nhanh (tự tạo file + chống trùng, nhưng vẫn phải tự làm bước 2, 5):
```bash
python .claude/skills/skill-feedback/scripts/add-pitfall.py --skill <ten-skill> \
  --severity warn --title "<tên ngắn>" --symptom "..." --cause "..." --fix "..." --evidence "..."
```

---

## 3. Ghi vào đâu (thứ tự ưu tiên)

| Tình huống | Nơi ghi |
|---|---|
| Skill X đã có mục "Bẫy đã biết" / "Lỗi thường gặp" / bảng bài học | Append vào đúng mục đó (ưu tiên cao nhất) |
| Bài học mức IRON (mục 4) và SKILL.md của X còn dưới ~480 dòng | Sửa/thêm quy tắc ngắn ngay mục liên quan của `SKILL.md` |
| Còn lại (SKILL.md đầy, bài học mang chi tiết) | `X/reference/pitfalls.md` (tạo mới theo header chuẩn — xem `reference/lesson-template.md`); SKILL.md của X cần 1 dòng dẫn tới file đó |
| Bài học KHÔNG thuộc skill nào (môi trường, quy trình chung) | `docs/lessons-learned.md` mục checklist cuối (như dòng "Vệ sinh commit") |

CẤM tạo kho bài học lẻ ngoài các nơi trên (`lessons-X.md` ở root, `docs/notes/...`) — vi phạm chuẩn "bài học sống thẳng trong skill" và Nguyên tắc bất biến #8.

---

## 4. Mức độ (severity)

| Mức | Nghĩa là | Ghi ở đâu |
|---|---|---|
| IRON | Vi phạm → kết quả sai/hỏng, không có ngoại lệ | Mục quy tắc/luật của `SKILL.md` (skill X) |
| WARN | Hay gặp, tốn thời gian, có cách né chuẩn | Mục bẫy/bài học của skill X |
| INFO | Tình huống hiếm, ghi để nhận diện nhanh | `X/reference/pitfalls.md` |

---

## 5. Luật cấm (IRON RULE của chính skill này)

1. **CẤM ghi chưa xác minh như thể đã chứng minh** — thiếu bằng chứng thì phải kèm `[UNVERIFIED]`.
2. **CẤM ghi trùng** cái skill đã có; trùng thì cập nhật bản cũ, không thêm bản mới.
3. **CẤM ghi chi tiết máy cá nhân** (đường dẫn user, version cục bộ, key) thành luật chung; **CẤM ghi secrets** (Nguyên tắc bất biến #4).
4. **CẤM sửa logic/cấu trúc của skill X** khi chỉ đóng góp bài học — minimal patch, có thể rollback.
5. **CẤM xoá/sửa bản ghi có sẵn** của skill khác nếu không đè lên sai sót rõ ràng; mâu thuẫn giữa các skill → hỏi user hoặc chốt ở `AGENTS.md` (không tự sửa skill cho khớp ý mình).
6. **CẤM entry > 12 dòng** — dài thì tóm quy tắc ở skill, chi tiết xuống `reference/`.
7. **CẤM quên đồng bộ**: sửa `.claude/skills/` mà không chạy `tools/sync-skills.ps1` = mirror `.agents/skills/` lệch.
8. **CẤM dùng đóng góp để "đè" quy tắc đã có** ở `AGENTS.md` (Nguyên tắc bất biến đứng trên mọi skill).

---

## 6. Định dạng một entry

Đầy đủ ở `reference/lesson-template.md`. Entry chuẩn (≤ 12 dòng):

```markdown
### [WARN] <tên ngắn của bẫy> (YYYY-MM-DD)
- **Triệu chứng:** ...
- **Nguyên nhân:** ...
- **Sửa/phòng:** ... (bằng chứng: `<lệnh>` → output xác nhận)
- **Điều kiện tái lập:** ...
```

Entry tốt = người đọc phiên sau **làm theo được ngay** mà không cần hỏi lại ai. Entry xấu = chỉ mô tả cảm giác ("chậm", "khó dùng") không có lệnh, không có cách sửa.

---

## 7. Definition of Done

```text
[ ] Đã xác minh (tái lập + fix PASS) hoặc ghi rõ [UNVERIFIED].
[ ] Đã grep chống trùng (SKILL.md + reference/ + scripts/ + lessons-learned.md).
[ ] Entry đúng nơi, đúng mức, ≤ 12 dòng, có bằng chứng.
[ ] Bản đồ docs/lessons-learned.md đã thêm 1 dòng.
[ ] tools/verify-skills.ps1 PASS + tools/sync-skills.ps1 đã chạy.
[ ] Đã báo user 1 dòng.
```

---

## 8. Áp dụng cho chính skill này

Skill này cũng chịu chính vòng lặp nó định nghĩa: khi đóng góp bài học mà gặp bẫy (entry trùng sót, patch làm vỡ frontmatter, mirror lệch hash…) → đóng góp lại vào `skill-feedback/reference/pitfalls.md`.
