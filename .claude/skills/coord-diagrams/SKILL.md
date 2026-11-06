---
name: coord-diagrams
description: "Điều phối khối SƠ ĐỒ KỸ THUẬT: nạp nhanh để vẽ Use Case/UML/ERD/Class/Sequence/Activity/State, cây/trie/bk-tree, kiến trúc, flowchart, luồng dữ liệu. **Mặc định VẼ TAY 100% bằng SVG toạ độ cứng** (`handdrawn-diagrams`) — PlantUML/Mermaid/drawio chỉ là nháp. Gom handdrawn-diagrams (chủ), diagram-orchestrator (SSOT ngữ nghĩa), plantuml-diagrams (nháp + luật UML), tldraw-diagrams, simplified-diagrams, use-case-layout, diagram-design (branded) và diagram-auditor (GATE). Từ khóa kích hoạt: vẽ sơ đồ, vẽ tay hết, không dùng PlantUML, không dùng công cụ ngoài, sơ đồ vẽ xấu, toạ độ cứng, eye audit, use case, UML, ERD, class diagram, sequence, activity, state machine, kiến trúc, flowchart, trie, bk-tree, audit sơ đồ."
---

> **Quy tắc hiện hành (02/11/2026):** bản cuối dùng `handdrawn-diagrams`: Python toạ độ cố định → `docs/diagrams/vectors/*.svg` + `docs/images/diagrams/*.png`, spec JSON riêng. PlantUML/Graphviz/Mermaid/drawio/tldraw trong các ví dụ bên dưới chỉ dùng nháp. Nguồn `.py` là bắt buộc. Duyệt ngữ nghĩa theo nguồn, chạy `run_diagrams.py` (cổng máy), rồi Vision QA từng hình; không suy PASS bố cục từ exit 0. Use Case chung gốc ở junction thân–tay `(ax, ay−4)` = tâm đầu +18 với mẫu hiện hành, không ở bụng. State đọc `plantuml-diagrams/reference/state-playbook.md`, không note/legend/footer trên canvas. Khi hướng dẫn cũ trái khối này, áp dụng khối này.


# coord-diagrams — Điều phối khối Sơ đồ Kỹ thuật

Nạp để vào khối **sơ đồ** với đúng công cụ + qua cổng kiểm định.

> **SSOT quy tắc sơ đồ:** `diagram-orchestrator` (khối "Đồng bộ quy tắc liên skill"). Baseline: `docs/rule-conflicts.md`.

## Khi nào nạp

- Vẽ sơ đồ UML / Use Case / ERD / Class / Sequence / Activity / State, cây-trie-bk-tree, kiến trúc, flowchart, luồng dữ liệu.

## Khối gồm

| Skill | Vai trò | Khi nào |
|---|---|---|
| `handdrawn-diagrams` | **CHỦ / BẮT BUỘC cho bản nộp**: vẽ tay SVG từ Python, toạ độ hằng số, `vectors/*.svg` tách `images/*.png`, audit E1..E6 + selftest | **mọi sơ đồ cuối** |
| `diagram-orchestrator` | **SSOT ngữ nghĩa**: phân tích bài toán, Bước 0, chọn mức trừu tượng (không chọn công cụ nữa) | luôn nạp đầu |
| `plantuml-diagrams` | **NHÁP**: `.puml` để nghĩ bố cục + bộ luật UML/zero-color/state-playbook đáng giữ | chỉ khi cần nháp |
| `tldraw-diagrams` | Kiến trúc/flowchart nét cong mềm, `.tldr` sửa được | sơ đồ tự do đẹp |
| `simplified-diagrams` | Sơ đồ khái niệm 5–9 thực thể cho slide/bảo vệ | cần tinh gọn |
| `use-case-layout` | Use Case: **SVG sinh từ Python; draw.io chỉ nháp**, lane gọn, cấm vòng xa, **duyệt bằng mắt soi ảnh (không script)** | mọi Use Case |
| `diagram-design` | Sơ đồ **branded/presentational (được màu)** HTML/SVG | marketing, KHÔNG báo cáo |
| `diagram-auditor` | **GATE**: Semantic + Visual Review, zero-color, proof-of-view | trước khi chèn |
| `diagram-pack` | Đóng gói vòng đời sơ đồ vào MỘT thư mục đích (code → `diagrams/`, ảnh → `images/diagrams/`, audit → `audit/soi-so-do/`) + `check_pack.py` | khi cần bàn giao/gói sơ đồ |

## Thứ tự nạp & chuỗi

```text
diagram-orchestrator (phân tích ngữ nghĩa + Bước 0 nếu Use Case/domain)
 → handdrawn-diagrams (VẼ TAY: gen_*.py toạ độ cứng → vectors/*.svg → images/*.png)
 → audit_svg.py + verify_box_layout.py + selftest  (0 lỗi mới được đi tiếp)
 → diagram-auditor (GATE: PASS mới được chèn vào docx/pptx)
```

## Cổng (gate)

- `diagram-auditor` là **cổng bắt buộc** cho mọi sơ đồ học thuật — theo **CỔNG PASS HAI ĐIỀU KIỆN** (§1.5):
  - **ĐK1 MÁY:** audit 0 lỗi + **file nguồn (`gen_*.py` / `.puml` / `.dot` / `.drawio`) TỒN TẠI** + **file ảnh `.png` + `.svg` TỒN TẠI >500B**.
  - **ĐK2 MẮT/VISION:** **model có vision** soi ảnh thật, ghi ≥3 nhãn nguyên văn + vị trí + kết luận "sắp xếp đã hợp lý chưa" + dòng `Vision audit by: <model-id>`. Model text-only **không tính**.
- Bước 0 (Use Case/domain): `docs/domain/step0-<du-an>.md` — thiếu → **BLOCKED**.
- **CẤM PASS** khi: chỉ chạy script mà chưa vision; chỉ nhìn ảnh mà script lỗi/thiếu file; **ảnh có mà thiếu `.py` nguồn generator = FAIL** (không tái lập được).

## Quy ước chung (SSOT)

- **Mọi sơ đồ kỹ thuật = VẼ TAY** (SVG sinh từ Python, toạ độ hằng số) theo `handdrawn-diagrams`. PlantUML/Mermaid/Graphviz/drawio **chỉ là nháp** — quyết định 2026-11-01: công cụ ngoài vẽ xấu và khó kiểm soát.
- **Hợp đồng thư mục:** `docs/diagrams/spec/*.json` · `docs/diagrams/vectors/*.svg` · `docs/diagrams/drawio/*.drawio` · `docs/images/diagrams/*.png`. **Mỗi định dạng một thư mục riêng** — cấm SVG/drawio trong thư mục PNG.
- **Use Case:** **1 điểm xuất phát ở khuỷu tay** (`(ax, ay−4)`) + **đường thẳng** `<line>` tới mép ellipse — **cấm cung Bezier cho dây nối** (luật 2026-11-01: "vòng cung" là ellipse, không phải dây nối). `include`/`extend`: nét đứt + mũi tên hở.
- **Cổng tất định bắt buộc:** `audit_svg.py` (E1..E6) + `verify_box_layout.py` (E1..E4 hình học) + `selftest_audit_svg.py` (chống False PASS) → **0 lỗi**.
- Báo cáo học thuật = **zero-color**; branded mới được dùng màu.
- **Không nhúng tiêu đề** trong ảnh; caption do `docx-report` sinh (`Hình X.Y: ...`).
- **Use Case:** đọc SSOT `use-case-layout/reference/actor-function-composition.md`; actor trái/phải theo cụm có căn cứ. Không hard-code vai trò của ví dụ dự án khác, không tự xóa Đăng nhập hoặc ép đúng 3 cột/10–16 UC. Quạt chung gốc ở junction thân–tay là hợp lệ, vẫn kiểm từng cạnh.
- **State:** đọc SSOT `plantuml-diagrams/reference/state-playbook.md`; không suy final từ tên, phân biệt declared/as-is/to-be và cấm chú thích cả dạng footer/chữ rời.
- Ratio khuyến nghị 0.5–2.4 (hard-fail `>3.8` / `<0.28`); node ≤ 15 (chi tiết) / ≤ 9 (khái niệm); chữ ≥ 9pt; nguồn `docs/diagrams/`, SVG `vectors/`, PNG `docs/images/diagrams/`.

## Anti-patterns

- ❌ Vẽ Use Case/domain khi chưa có Bước 0.
- ❌ Dùng màu cho sơ đồ đồ án; nhúng title trong ảnh.
- ❌ Chèn sơ đồ chưa qua `diagram-auditor`.

## Definition of Done

```text
[ ] Vẽ tay SVG toạ độ cứng (handdrawn-diagrams), không PlantUML/drawio cho bản nộp.
[ ] Có gen_*.py (nguồn) + spec/*.json + vectors/*.svg + images/diagrams/*.png (+ drawio/*.drawio nếu có).
[ ] Use Case: mọi association từ ĐÚNG 1 điểm khuỷu tay actor + ĐƯỜNG THẲNG (không cung Bezier cho dây nối).
[ ] audit_svg.py 0 lỗi (E1..E6) + verify_box_layout.py PASS (sơ đồ hộp) + selftest PASS.
[ ] diagram-auditor: ĐK1 MÁY (script 0 lỗi + file nguồn + PNG/SVG tồn tại) VÀ ĐK2 VISION (model có vision soi ảnh + `Vision audit by:`) — thiếu một = chưa xong.
```

---

## ⚡ PROMPT BẮT BUỘC KHI NẠP KHỐI NÀY (COPY VÀO PROMPT AGENT)

> **KHI BẠN BẮT ĐẦU VIỆC LIÊN QUAN SƠ ĐỒ (vẽ/audit/điều phối), BẮT BUỘC:**
>
> 1. **NẠP `diagram-orchestrator` TRƯỚC TIÊN** — nó là SSOT ngữ nghĩa + bắt buộc Bước 0.
> 2. **KIỂM TRA BƯỚC 0** (`docs/domain/step0-<du-an>.md`) TRƯỚC KHI VẼ USE CASE/DOMAIN — thiếu = BLOCKED.
> 3. **VẼ TAY 100% (SSOT `handdrawn-diagrams`):** mọi sơ đồ dùng `gen_*.py` với **toạ độ hằng số** → `docs/diagrams/vectors/*.svg` → `docs/images/diagrams/*.png`. PlantUML/Mermaid/Graphviz/drawio **chỉ là nháp**, KHÔNG là file cuối. diagram-design CHỈ cho branded/marketing (được màu), KHÔNG cho báo cáo.
> 4. **CỔNG ĐO ĐƯỢC + CỔNG VISION:** `audit_svg.py` + `verify_box_layout.py` + `selftest_audit_svg.py` → 0 lỗi; **file nguồn `.py` + ảnh `.png`/`.svg` phải tồn tại**. Nhịp cuối **bắt buộc model có vision** soi ảnh thật, ghi `Vision audit by: <model-id>` + 3 nhãn + verdict; model text-only **không tính**; không xem được ảnh thì ghi `Visual QA unavailable`, **cấm bịa Proof-of-View**.
> 5. **CUỐI CÙNG: CHẠY `diagram-auditor` (GATE BẮT BUỘC)** — 5 cổng nghiệm thu độc lập + **PASS hai điều kiện (MÁY + VISION)**.
>
> **ANTI-PATTERNS CỦA COORDINATOR (TUYỆT ĐỐI KHÔNG LÀM):**
> - ❌ Nạp `plantuml-diagrams` hoặc `tldraw-diagrams` mà **không qua `diagram-orchestrator`** chọn công cụ
> - ❌ Vẽ Use Case/ERD **chưa kiểm tra Bước 0**
> - ❌ Dùng `diagram-design` (có màu) cho báo cáo học thuật
> - ❌ Chèn sơ đồ vào docx/pptx **chưa qua diagram-auditor**
> - ❌ Gộp 5 cổng nghiệm thu thành 1 PASS duy nhất
> - ❌ Bỏ qua Visual QA / Proof-of-View
