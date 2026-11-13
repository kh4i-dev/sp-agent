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
| Chỉ dùng `lxml`, cấm `xml.etree` ghi XML Word | `safe-docx-modifier` Bài học 10; `docx-report-tnut` rules §1.1 dòng 8 |
| Cấm substring-match trên XML serialize (`"drawing" in XML`) | `docx-report-tnut` rules §1.1 dòng 9 |
| Regex: viết trực tiếp ký tự Unicode, không `\u` trong raw-string | `human-md-audit` §"Bẫy đã biết" |
| Quét field đúng thẻ `w:instrText` (tránh false positive `styles.xml`) | `human-md-audit` §"Bẫy đã biết" |
| Dựng field bằng `OxmlElement`, không nối f-string XML | `docx-report-tnut` rules §1.1 dòng 10 |
| Số chương lấy từ text Heading (`CHƯƠNG N`), không `STYLEREF` (trả 0) | `docx-report-tnut` rules §6 |
| Caption số tay → Danh mục trống; chuyển SEQ một lần, F9 trong Word | `docx-report-tnut` rules §6–§7; `human-md-audit` §"Bẫy đã biết" |
| Chèn/xóa nội dung → TOC stale → nhắc user Word F9 | `docx-report-tnut` rules §7 |
| Bảng: cỡ chữ tách `--table-font-size`, khóa `tblGrid`/`tcW` | code `edit_docx.py` + bảng cờ trong `docx-report-tnut` SKILL.md |
| Render Word COM phải `Fields.Update()`; soffice không tự update | `docx-report-tnut` SKILL.md + rules §8 |
| Audit docs ↔ code (mô tả phải có lệnh chạy chứng minh) | `skill-coordinator` §4 quy tắc 2 |
| Quét tham chiếu chết sau đổi tên/xóa skill | `skill-coordinator` §4 quy tắc 2 (grep toàn `.claude/skills`) |
| Description/frontmatter và rule trong thân phải cùng một lời | `AGENTS.md` "Bẫy khiến skill KHÔNG nạp" |
| Mâu thuẫn liên-skill chốt ở AGENTS.md, sửa skill sai cho khớp | `AGENTS.md` Nguyên tắc bất biến; `skill-coordinator` §4 quy tắc 1 |
| Phạm vi màu: học thuật trắng-đen / branded được màu | `AGENTS.md` #13; nhắc trong skill sơ đồ liên quan |
| Không hardcode thông tin user; thiếu thì báo lỗi bắt hỏi | `docx-report-tnut` §"Phần đầu tài liệu (Bìa)" + `make_cover.py` REQUIRED |
| Tra cứu trước khi thêm quy tắc mới (VD: cấm `title` trong ảnh đã có ở 4 skill) | `skill-coordinator` §4 + `docs/rule-conflicts.md` |
| Việc lớn nạp `skill-coordinator` trước, không gọi lẻ skill | `AGENTS.md` Routing + `skill-coordinator` §2–§3 |
| Kỷ luật nạp skill (name==thư mục, từ khóa, sync, <500 dòng) | `AGENTS.md` "Giao thức nạp skill" |
| Backup `.bak_safe` + patch tối thiểu + verify sau ghi | `safe-docx-modifier` §1 SOP + Bài học 1–5 |
| User Acceptance Gate trước swap ảnh | `safe-docx-modifier` Bài học 6 |
| Source truth > suy đoán (đối chiếu schema/code; hỏi khi quyết định phá) | `safe-docx-modifier` Bài học 4; `AGENTS.md` #1, #10, #12 |
| Ngôn từ caption mềm hóa (vòng đời, không thuật ngữ cứng) | `docx-report-tnut` §Caption + `reference/caption-wording.md` |
| Quy mô báo cáo tối thiểu, chống báo cáo mỏng | `reference/report-scope.md` + `docx-report-tnut` SKILL.md |
| Văn phong nghiêm túc-tự nhiên, kiểm soát jargon | `human-report-writing` §2–§4 + `reference/register-and-jargon.md` |
| Vòng nhanh humanize→Markdown→audit, render chỉ ở gate cuối | `human-md-audit` SKILL.md |
| Bìa 2 định dạng, viền chừa gáy, hỏi trước khi sinh | `docx-report-tnut` §Bìa + `reference/cover-formats.md` |
| Thay ảnh DOCX: cấm ghi lại `document.xml` (lxml đổi prefix `ns0:` → Word báo "file appears to be corrupted"); dùng **byte-level swap** + ảnh cùng tỉ lệ + **mở thử bằng Word COM** | `docx-report-tnut` §"Thay thế ảnh siêu tốc" (CẢNH BÁO) |
| Vệ sinh commit (gitignore vendor/pycache, secret scan, `-F` UTF-8) | Quy trình làm việc (không thuộc skill nào — giữ ở đây làm checklist) |
| Gặp lỗi khi dùng skill chưa nói đến → xác minh + chống trùng + đóng góp ngược lại vào skill | `skill-feedback` (toàn bộ — vòng lặp này là nơi sinh ra các dòng trên) |
| Đường sạch ≠ đẹp: một bước đều toàn hình = lưới máy móc; bố cục theo cụm luồng (đều trong cụm, rộng giữa cụm, stagger, neo la bàn, cong nhẹ chùm toả); G-GAP/N-UNALIGN/A-SKEW/C-FAN/S-LADDER là ứng viên thiết kế LOW, mắt phán BAO-OAN nếu là chủ đích nhóm | `use-case-layout` §3.2b + `visual-audit-protocol.md` §2/§3.1/§3.4/§3.6 |
| Người dùng cần tự sửa line trên web → AI sinh `.drawio` edge-glued (app.diagrams.net hoặc Lucidchart import trực tiếp) + preview SVG **cùng toạ độ, cùng điểm neo, có mũi tên hở** để chạy eye_audit | `use-case-layout` §3.4 + `scripts/make_drawio.py` |
| **CẤM xếp toàn bộ use case trên CUNG TRÒN đồng tâm actor** → mọi association thành bán kính, hội tụ 1 điểm = "con nhện", giữa cung trống hoác. Đúng: **cột theo cụm, cụm sau lùi phải (bậc thang)** — cột dọc làm thứ tự `y` đích đơn điệu nên dây không thể cắt nhau (ca thật: `uc_rap_phim_v2` bị trả lại 2026-10-29) | `use-case-layout` §3.2b (CAUTION) + `visual-audit-protocol.md` §4 bậc 0 + §5c |
| Chùm dây rời actor: neo phải nằm trong **THÂN** (`exitY 0.33–0.87`), **không rời từ đầu/cổ**; dải neo quá hẹp (38px) vẫn đọc ra "quạt" nếu tên actor đặt dưới chân → đặt tên **bên cạnh** hình | `use-case-layout` §3.4 + `make_drawio.py` (`EXIT_BASE`/`FAN_SPAN`) |
| "Script 0 đỏ" ≠ hình đẹp: bản v2 có HIGH=0 mà vẫn sai vì lỗi ở **bố cục**, không ở từng nét → phải có phép kiểm bố cục (`C-FAN`, `S-LADDER`) và mắt soi overlay | `use-case-layout` Bước 4 + `eye_audit.py` |
| `C-DANGLE` báo oan **barb của mũi tên hở** (`«include»/«extend»`) vì đầu barb lơ lửng theo thiết kế → miễn trừ đoạn ≤18px có đầu kia đã neo vào node | `eye_audit.py` (C-DANGLE) |
| Chùm association tụ 1 điểm trên ngực actor khi số hàng UC lớn (≥10 hàng) = "con nhện" xấu — phóng to figure theo dải hàng (`TH=spanUC+3*RY (ca cao bang cot UC, exit 0.30..0.90)`, exit rải fr 0.20..0.86) hoặc đốt gốc chung; mặt soi crop F16 bắt được, eye_audit không ập mức HIGH | `use-case-layout` §3.2%§3.2b + `reference/pitfalls.md` (IRON 2026-11-01) |

### Hiệu chỉnh bố cục Use Case — 2026-11-01

Hai ảnh mẫu người dùng xác nhận quạt tia thẳng chung gốc ở thân actor là bố cục mong muốn. Các dòng lịch sử cấm hội tụ hoặc khuyên kéo figure theo chiều cao cột UC ở trên đã được thay thế bởi `use-case-layout/reference/actor-function-composition.md`. Bản nội bộ v6 có cột chức năng dài và toàn bộ vai trò bên trái; sửa tư duy phân cụm/vị trí node trước, không phóng to actor hoặc bẻ dây để chữa. Không suy diễn quyền nghiệp vụ từ ảnh tham khảo.

| Bài học | Nằm trong |
|---|---|
| State: no-note phải chặn cả footer/chữ rời; declared matrix không đồng nghĩa runtime; Completed không phải FinalState; composite mở rộng phải khớp cạnh nguồn | `plantuml-diagrams/reference/state-playbook.md` + `scripts/render_state_model.py`; ca btl-cnpm 01/11/2026 |
| Bộ kiểm State dùng assert bị tắt bởi Python -O; default-entry composite không được nhân thành mọi child; completion hợp lệ có thể không nhãn | `plantuml-diagrams/reference/state-playbook.md` §4 + `scripts/test_state_model.py`; audit 01/11/2026: 21/21 thường và -O |
| Handdrawn auditor: selftest cũ đạt nhưng còn bỏ lọt halo text overlap, transform, NaN line, z-order và diagonal box; runner chưa đủ cổng | `handdrawn-diagrams/reference/known-audit-gaps.md` (đã sửa các ca tái hiện 02/11; giới hạn parser vẫn được ghi rõ); bằng chứng `docs/analysis/handdrawn-skill-audit-2026-11-02/` |
| Halo không miễn chữ đè; transform/z-order phải được kiểm hoặc từ chối; runner phải chặn thiếu nguồn/PNG/spec và chạy gate riêng theo loại hình | `handdrawn-diagrams`: selftest regression + 9 test pipeline, 02/11/2026 |
| Đặc tả use case cần kỷ luật ID (bước đánh số, luồng A1/E1, BR-xx) + exception đủ 4 thứ (điều kiện, phản hồi, thông báo, điểm quay về) + post-condition luồng lỗi — để Dev/Tester truy vết, không tự diễn giải | `docx-report-tnut` `reference/use-case-spec.md` (nguồn: bài viết user 02/11/2026) |
| Audit skill: tham chiếu backtick + tên-trần chéo skill + hàng bảng mồ côi thoát qua `audit-skills.ps1`; kết quả scanner ad-hoc phải đối chiếu thực địa trước khi kết luận; tools/*.ps1 ASCII thuần (5.1 ANSI) | `skill-feedback/reference/pitfalls.md` (5 entry, 02/11/2026) |

### Cấm dây chéo ERD/Class — 2026-11-07 (đồ án Quản lý dịch vụ thú cưng)

| Bài học | Nằm trong |
|---|---|
| Dây nối hộp **chéo** từ góc ra góc là lỗi bố cục thật (9/21 cạnh ERD+Class) mà E1..E4 không chặn → audit cũ vẫn PASS; thêm **E5 cấm chéo + E6 thẳng hàng thì đi thẳng**, kèm selftest chống False PASS | `handdrawn-diagrams` SKILL.md §3.1 + `verify_box_layout.py` + `test_pipeline.py`; SSOT `diagram-orchestrator/reference/box-connector-routing.md` |
| E6 báo oan kênh ngoài biên cột nếu chỉ xét lòng hộp: đường thẳng trong cột sẽ **đè viền** hộp trung gian → xét hành lang với cả biên (inset âm) | `verify_box_layout.py` E6 (`seg_hits(inset=-2)`) |
| Toạ độ quan hệ viết tay ở 2 nơi (generator + spec) gây drift, audit chạy trên dữ liệu cũ → khai báo 1 bảng REL trong generator, make_specs import | `box-connector-routing.md` §4; project mẫu `gen_diagrams.py`/`make_specs.py` |

### Cổng VISION bị "qua" bằng tool chỉ-trả-đường-dẫn — 2026-11-08

| Bài học | Nằm trong |
|---|---|
| `tools.browser.preview` **chỉ trả `{ path }`** (mở ảnh cho *người dùng*), **KHÔNG đưa pixel vào ngữ cảnh model** → gọi nó rồi tự nhận "đã soi ảnh" là **audit giả**; skill cũ ghi nó là cách hợp lệ nên agent dùng nó để qua ĐK2 rồi **chốt in**. Công cụ vision ĐÚNG ở harness này là **`read` trên file `.png`** (hoặc vision subagent). Phép thử: kết quả công cụ chỉ là path/kích thước/text → audit text, KHÔNG phải vision → CẤM PASS | `diagram-auditor` §1.5–§2 (bỏ `browser.preview`, thêm phép thử) + `docx-report-tnut` §8 Cổng 2 + `AGENTS.md` #10; sự kiện: ảnh chat agent tự nhận dùng `browser.preview` (2026-11-08) |
| Đọc liên tiếp nhiều trang PNG full-page dễ gặp `HTTP 429 Too Many Requests` → đọc theo lô nhỏ (2–3 trang/lần) / hạ DPI / giao vision subagent; **cấm** bỏ trang chưa soi rồi vẫn kết luận "in được" | `docx-report-tnut` §8 Cổng 2 (bẫy tải ảnh) |
| Chỗ chưa điền: **KHÔNG tự điền hộ, KHÔNG bôi vàng** (vi phạm format) → để **dấu chấm `............`** + liệt kê; không chặn goal để chờ hỏi (user có thể đi vắng). Chỗ **chữ ký + dòng ngày ký** để **TRỐNG** (in ra ký tay), không tính là thiếu | `AGENTS.md` #11; `coord-report` GOAL; `docx-report-tnut` §8 Cổng 3 + §12 + §14; `report-scope.md` §4; `tnut-btl-checklist.md` |
| "Làm docx" phải là MỘT goal khép kín (cấu trúc+người viết · rà sơ đồ→auditor GATE · ảnh chụp 16:9 thật · quét chỗ chưa điền · render+soi ảnh), lặp tới PASS; thiếu gate cuối = chưa xong | `coord-report` §GOAL + chuỗi + DoD; `skill-coordinator` §3A |
| Bảng mô tả thực thể CSDL gộp nhiều thực thể (dòng tiêu đề phụ "User"/"Profile") khó nhìn → **tách mỗi thực thể 1 bảng**, caption ở TRÊN, **bỏ dòng tên thực thể trong bảng** (caption đã nêu), căn **cột văn bản TRÁI / cột mã GIỮA**; đánh số lại + dựng lại Danh mục (dùng số y nguyên caption, bỏ caption phụ lục `Bảng A.`) | `docx-report-tnut` §4.2; ca thật `ecosystem_ketnoi_giasu/thesis_defense_docs` 2026-11-08 |
| **Vị trí caption là BẤT BIẾN: BẢNG trên / HÌNH dưới** (kể cả title trắng-đen hay mẫu GV khác thì vẫn vậy); caption in nghiêng chỉ là MẶC ĐỊNH TNUT — mẫu GV yêu cầu khác thì theo GV nhưng nhất quán | `docx-report-tnut` §4 + §4.2 |
