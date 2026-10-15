# Bài học kinh nghiệm sp-agent (bản đồ tra cứu)

> Quy ước bất biến: bài học sống **thẳng trong skill** (agent nạp là thấy).
> File này chỉ là **bản đồ** — không phải nguồn thứ hai. Sửa luật thì sửa trong skill,
> rồi cập nhật bảng dưới đây. Cấm sao chép nguyên văn dài dòng ra đây (gây drift).

> Nguyên tắc đọc: **bằng chứng > lời nói** — mọi bài học đều từng được chứng minh
> bằng lệnh chạy thật + output.

## Quy trình khi phát hiện bài học mới

1. Viết thẳng vào skill liên quan (đúng mục, ngắn gọn, kèm bằng chứng/câu lệnh).
2. Cập nhật bảng dưới đây (1 dòng).
3. `verify-skills.ps1` + `sync-skills.ps1` (mirror khớp hash).

## Bản đồ bài học → skill

| Bài học | Nằm trong |
|---|---|
| "Trông xong" ≠ xong: kết luận cần bằng chứng thực thi (render/soi/mở Word thật) | `skill-coordinator` §6 Definition of Done; `safe-docx-modifier` §1 SOP |
| Debug bằng cô lập từng bước (test riêng từng bước sửa) | `safe-docx-modifier` Bài học 11 |
| Test khả năng thật, không test qua trung gian (COM thay vì PATH) | `safe-docx-modifier` Bài học 11 |
| Chỉ dùng `lxml`, cấm `xml.etree` ghi XML Word | `safe-docx-modifier` Bài học 10; `docx-report` rules §1.1 dòng 8 |
| Cấm substring-match trên XML serialize (`"drawing" in XML`) | `docx-report` rules §1.1 dòng 9 |
| Regex: viết trực tiếp ký tự Unicode, không `\u` trong raw-string | `human-md-audit` §"Bẫy đã biết" |
| Quét field đúng thẻ `w:instrText` (tránh false positive `styles.xml`) | `human-md-audit` §"Bẫy đã biết" |
| Dựng field bằng `OxmlElement`, không nối f-string XML | `docx-report` rules §1.1 dòng 10 |
| Số chương lấy từ text Heading (`CHƯƠNG N`), không `STYLEREF` (trả 0) | `docx-report` rules §6 |
| Caption số tay → Danh mục trống; chuyển SEQ một lần, F9 trong Word | `docx-report` rules §6–§7; `human-md-audit` §"Bẫy đã biết" |
| Chèn/xóa nội dung → TOC stale → nhắc user Word F9 | `docx-report` rules §7 |
| Bảng: cỡ chữ tách `--table-font-size`, khóa `tblGrid`/`tcW` | code `edit_docx.py` + bảng cờ trong `docx-report` SKILL.md |
| Render Word COM phải `Fields.Update()`; soffice không tự update | `docx-report` SKILL.md + rules §8 |
| Audit docs ↔ code (mô tả phải có lệnh chạy chứng minh) | `skill-coordinator` §4 quy tắc 2 |
| Quét tham chiếu chết sau đổi tên/xóa skill | `skill-coordinator` §4 quy tắc 2 (grep toàn `.claude/skills`) |
| Description/frontmatter và rule trong thân phải cùng một lời | `AGENTS.md` "Bẫy khiến skill KHÔNG nạp" |
| Mâu thuẫn liên-skill chốt ở AGENTS.md, sửa skill sai cho khớp | `AGENTS.md` Nguyên tắc bất biến; `skill-coordinator` §4 quy tắc 1 |
| Phạm vi màu: học thuật trắng-đen / branded được màu | `AGENTS.md` #13; nhắc trong skill sơ đồ liên quan |
| Không hardcode thông tin user; thiếu thì báo lỗi bắt hỏi | `docx-report` §"Phần đầu tài liệu (Bìa)" + `make_cover.py` REQUIRED |
| Tra cứu trước khi thêm quy tắc mới (VD: cấm `title` trong ảnh đã có ở 4 skill) | `skill-coordinator` §4 + `docs/rule-conflicts.md` |
| Việc lớn nạp `skill-coordinator` trước, không gọi lẻ skill | `AGENTS.md` Routing + `skill-coordinator` §2–§3 |
| Kỷ luật nạp skill (name==thư mục, từ khóa, sync, <500 dòng) | `AGENTS.md` "Giao thức nạp skill" |
| Backup `.bak_safe` + patch tối thiểu + verify sau ghi | `safe-docx-modifier` §1 SOP + Bài học 1–5 |
| User Acceptance Gate trước swap ảnh | `safe-docx-modifier` Bài học 6 |
| Source truth > suy đoán (đối chiếu schema/code; hỏi khi quyết định phá) | `safe-docx-modifier` Bài học 4; `AGENTS.md` #1, #10, #12 |
| Ngôn từ caption mềm hóa (vòng đời, không thuật ngữ cứng) | `docx-report` §Caption + `reference/caption-wording.md` |
| Quy mô báo cáo tối thiểu, chống báo cáo mỏng | `reference/report-scope.md` + `docx-report` SKILL.md |
| Văn phong nghiêm túc-tự nhiên, kiểm soát jargon | `human-report-writing` §2–§4 + `reference/register-and-jargon.md` |
| Vòng nhanh humanize→Markdown→audit, render chỉ ở gate cuối | `human-md-audit` SKILL.md |
| Bìa 2 định dạng, viền chừa gáy, hỏi trước khi sinh | `docx-report` §Bìa + `reference/cover-formats.md` |
| Vệ sinh commit (gitignore vendor/pycache, secret scan, `-F` UTF-8) | Quy trình làm việc (không thuộc skill nào — giữ ở đây làm checklist) |
