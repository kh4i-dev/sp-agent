---
name: diagram-pack
description: "Đóng gói toàn bộ vòng đời sơ đồ của MỘT dự án vào MỘT thư mục đích (pack contract): code nguồn sinh sơ đồ → diagrams/, ảnh render .svg+.png 1:1 → images/diagrams/, dấu vết soi mắt → audit/soi-so-do/, Bước 0 → domain/. Quy tắc gen chống đè/chồng/vòng xa; vòng sửa: sửa nguồn → render lại chỉ hình ảnh hưởng → soi lại; PNG render Chrome headless để giữ dấu tiếng Việt. Dùng khi: gen sơ đồ cho báo cáo/đồ án, tạo pack sơ đồ dự án mới, sửa sơ đồ rồi render lại, 'ảnh ra ảnh code ra code', kiểm tra pack sơ đồ, check_pack, sơ đồ chồng nhau/đè nhãn."
license: MIT
---

> **Quy tắc hiện hành (02/11/2026):** bản cuối dùng `handdrawn-diagrams`: Python toạ độ cố định → `docs/diagrams/vectors/*.svg` + `docs/images/diagrams/*.png`, spec JSON riêng. PlantUML/Graphviz/Mermaid/drawio/tldraw trong các ví dụ bên dưới chỉ dùng nháp. Nguồn `.py` là bắt buộc. Duyệt ngữ nghĩa theo nguồn, chạy `run_diagrams.py` (cổng máy), rồi Vision QA từng hình; không suy PASS bố cục từ exit 0. Use Case chung gốc ở junction thân–tay `(ax, ay−4)` = tâm đầu +18 với mẫu hiện hành, không ở bụng. State đọc `plantuml-diagrams/reference/state-playbook.md`, không note/legend/footer trên canvas. Khi hướng dẫn cũ trái khối này, áp dụng khối này.


# Diagram Pack Skill — Hợp Đồng Thư Mục & Vòng Đời Sơ Đồ

**Mục tiêu:** Đóng gói toàn bộ sơ đồ của một dự án vào **một thư mục duy nhất** với hợp đồng rõ ràng: source code ở `diagrams/`, rendered images 1:1 ở `images/diagrams/`, audit traces ở `audit/soi-so-do/`. Tránh sơ đồ trông lên nhau bằng các quy tắc chống đè/chồng/vòng xa và workflow nghiệm thu 5 cổng.

> [!SCOPE]
> **Phạm vi:** Skill này chủ yếu về **"nơi file nằm"** + **"vòng đời"**. Tính chất ngữ nghĩa của từng loại sơ đồ (Use Case vs Class vs ERD, layout rules) defer về các skill chuyên biệt: `use-case-layout`, `plantuml-diagrams`, `tldraw-diagrams`, `diagram-orchestrator`.

---

## 1. Hợp Đồng Thư Mục (SSOT)

Cho mỗi target root `<TARGET>/` (ví dụ: `E:\...\btl-cnpm\private-docs`), **luật cứng**:

```
<TARGET>/                                   ← 1 thư mục duy nhất (gốc của pack)
├── domain/step0-<du-an>.md                 ← Bước 0: bài toán, tác nhân, phạm vi (TRƯỚC khi vẽ Use Case)
├── diagrams/                               ← TOÀN BỘ CODE NGUỒN: *.py, *.puml, *.dot, *.drawio, *.tldr, model/*.md, layout/*.md
│   ├── gen_usecase_draw.py                 ← generator chính (hoặc tương tự)
│   ├── svg_render.py                       ← module render PNG dùng chung (Chrome headless)
│   └── *.md                                ← use-case-master, use-case-model, use-case-layout, etc.
├── images/diagrams/                        ← CHỈ ẢNH RENDER: <ten>.svg + <ten>.png theo CẶP 1:1
│   ├── _legacy/                            ← ảnh cũ chỉ để đối chiếu, KHÔNG đụng
│   └── *.svg | *.png                       ← luôn theo cặp 1:1 (không có png không svg hoặc ngược lại)
├── audit/soi-so-do/                        ← DẤU VẾT SOI MẮT: <đợt>/<ten>/{overlay.png, crops/, eye-audit.md}
│   ├── truoc-khi-sua/<ten>                 ← đợt 1: overlay + crop của bản CŨ
│   ├── sau-khi-sua/<ten>                   ← đợt 2: overlay + crop của bản ĐÃ SỬA
│   └── README.md                           ← ghi chép việc đã làm, verdict
├── tools/                                  ← script bổ trợ (check_overlap, verify_report_numbers, ...)
│                                               CẤM rải ở root/target
└── _legacy/                                ← tài liệu cũ, KHÔNG chạy, KHÔNG đụng
```

| Loại file | Thư mục | Luật |
|---|---|---|
| Code nguồn (`*.py`, `*.puml`, `*.dot`, `*.drawio`, `*.tldr`) | `diagrams/` | MỌI sửa bắt đầu ở đây; cấm sửa ảnh trực tiếp thay cho sửa source |
| Model/layout md | `diagrams/` | bảng adjacency, master UC, traceability |
| `.svg` + `.png` | `images/diagrams/` | CHỈ OUTPUT, luôn render từ source, luôn theo cặp 1:1 |
| Eye-audit traces | `audit/soi-so-do/` | mỗi vòng sửa: một folder với overlay.png + crops/ + eye-audit.md |
| Bước 0 | `domain/step0-<du-an>.md` | bắt buộc trước vẽ Use Case; thiếu = FAIL nghiệp vụ |
| Script công cụ | `tools/` hoặc `diagrams/` | CẤM ở root, phải gom vào nơi có tên ý nghĩa |

### 1.1. Naming Convention

| Loại | Pattern | Ví dụ |
|---|---|---|
| Use case (người mua/bán/tài xế/nội bộ) | `33{a,b,c,d}-usecase-{actor}.svg|.png` | `33a-usecase-nguoi-mua.svg` |
| Activity diagram | `act-{NN}-{mo-ta}.svg|.png` | `act-01-dang-nhap.svg` |
| Sequence diagram | `seq-{NN}-{mo-ta}.svg|.png` | `seq-34-dat-hang.svg` |
| State machine | `state-{NN}-{mo-ta}.svg|.png` | `state-01-don-hang.svg` |
| ERD (lô 6 phân hệ) | `erd_{NN}_{chuc-nang}.svg|.png` | `erd_01_loi-giao-dich-escrow.svg` |
| Flowchart | `flow-{NN}-{mo-ta}.svg|.png` | `flow-01-quy-trinh-dat-hang.svg` |
| Modules | `hang-muc-phan-ra-M1-M14.svg|.png` | Tên đặc thù cho cây module |

### 1.2. Luật Cặp 1:1

- Mỗi `.svg` trong `images/diagrams/` **phải** có `.png` cùng tên, **và ngược lại**.
- Cả hai đều xuất phát từ cùng generator/script.
- Không tồn tại orphan (`?.svg` không có `?.png` hoặc `?.png` không có `?.svg`).
- `_legacy/` được phép lệch vì là archive lịch sử.

### 1.3. Audit Layout

Hai mẫu chấp nhận:

- **Trước/Sau (trường hợp đã fix lỗi):** `audit/soi-so-do/truoc-khi-sua/<ten>/` + `sau-khi-sua/<ten>/` (mỗi thư mục có `eye-audit.md`, `overlay.png`, `crops/F*.png`)
- **Tên riêng (single iteration):** `audit/soi-so-do/<ten>-audit/{...}`

Script `scripts/check_pack.py` sẽ quét và cảnh báo nếu thiếu `overlay.png` hoặc `crops/`.

---

## 2. Quy Tắc Chống Chồng/Đè/Vòng Xa (Anti-Slop Generation Rules)

Tổng hợp từ `use-case-layout` §3.2/§3.2b, `diagram-orchestrator` §5B, `diagram-auditor` gate:

| Rule | Mô tả | Luật cứng |
|---|---|---|
| **0 line through text** | Không đường nối xuyên ellipse, chữ trong ellipse, tên actor, nhãn quan hệ | CỰC KỲ NGHIÊM: thấy = FAIL |
| **0 far loops** | Không connector đi vòng qua mép canvas để tới đích | Nếu gặp quan hệ dài → DI CHUYỂN NODE, không kéo dây |
| **0 overlap** | Không node/nhãn chồng lên nhau | Nếu chạm → enlarge padding hoặc stagger columns |
| **No ladder grid** | Không xếp mọi node thành 1 cột với bước đều tuyệt đối | Phá vỡ: nhịp đều TRONG cụm, rộng GIỮA cụm (§3.2b) |
| **Node budget** | Chi tiết ≤ 15 nodes/hình; khái niệm ≤ 9 | Quá → phân rã thành overview+detail |
| **Ratio frame** | Tỷ lệ khung 0.5–2.4 (hard-fail >3.8 hoặc <0.28) | Chỉnh W/H canvas trước khi render |
| **Font size** | Cỡ chữ ≥ 9pt khi in A4 (aim ≥ 12pt thực tế) | Zoom 4x trên overlay để đo |
| **Actor name safety** | Tên actor đặt dưới chân/trái, chừa ≥ 20px; neo association từ vai/tay chứ không xuyên vùng tên | Dùng `AX >= 170` và `text-anchor="end"` như học hỏi thật |
| **Wrap tight** | Nhãn dài → wrap sớm (MAXW ≈ int(RX*1.5)), RY đủ cho 2 dòng → radial_max ≤ 0.9 | 109% tràn → chỉnh thành 0.893 |
| **Vietnamese font** | **KHÔNG dùng CairoSVG**; render PNG bằng Chrome headless (module `svg_render.py`) | CairoSVG lấy glyph từ font khác → dấu bị đổi nét |

> [!CAUTION]
> **Script `eye_audit.py` chỉ sinh ứng viên.** Nó báo `L-ACTORNAME`, `T-OVERFLOW`, `G-GAP`... nhưng **không phán PASS/FAIL**. Phải **mở `overlay.png` + MỌI `crops/`** và tự điền verdict `THẬT`/`BÁO OÁN`.

### 2.1. Đo đạt chuẩn

Trước khi tin kết quả `eye_audit.py`:

1. **Đối chiếu số đếm:** `node=` trong output phải khớp số ellipse bạn vẽ; `actor=` phải khớp số tác nhân. Lệch → lỗi parser.
2. **Kiểm tổng ứng viên:** `HIGH=0` yêu cầu nghiêm ngặt (đường cắt tên actor); `MEDIUM` có thể chấp nhận (nhãn sát vỉa).
3. **3 câu trả lời:** ĐÈ? ĐỀU? DỄ NHÌN? Trả lời kèm ≥ 3 nhãn đọc nguyên văn + vị trí.

---

## 3. Quy Trình 7 Bước (End-to-End Workflow)

### B0 — Bước 0: Step0
Tạo `domain/step0-<du-an>.md` (theo template [`diagram-orchestrator/reference/step0-bai-toan-va-tac-nhan.md`](../diagram-orchestrator/reference/step0-bai-toan-va-tac-nhan.md)).

- Bài toán, quy mô, 7 tác nhân (nếu cần).
- Trách nhiệm từng tác nhân + nguồn chứng minh (`[REQ-xx]`, `[BRD §x.y]`, `[code:file:line]`). Chưa rõ ghi `UNKNOWN`.
- Ranh giới hệ thống, hàm ngoài tích hợp.
- Thiếu file Bước 0 → **CẤM VẼ USE CASE**, báo: `⚠️ VI PHẠM KỶ LUẬT: thiếu Bước 0`.

### B1 — Mô hình UML
Tạo `diagrams/use-case-model.md` (hoặc `class-model.md`, `erd-model.md`):

- Danh sách actor + mục tiêu actor.
- Danh sách use case (hoặc class/table) + quan hệ association/include/extend.
- Giải thích quyết định UML (include ↔ extend, inheritance is-a).
- **Test 1 câu:** mỗi quan hệ phải giải thích được trong 1 câu nghiệp vụ.

### B2 — Bảng Layout
Tạo `diagrams/<ten>-layout.md`:

- Bảng `element_id, label, kind(actor/usecase), group, side/lane, row, connected_actors, relationship_edges`.
- Với Use Case: `side/lane` bắt buộc `L` hoặc `R` (KHÔNG "giữa/đáy/trên").
- Đặt cặp `include/extend` gần nhau (cùng `row`/dòng liền kề) để tránh vòng xa.

**Gate B2:** Chạy `check_actor_lanes.py` (từ `use-case-layout/scripts/`) → `kind=actor` phải chỉ `L` hoặc `R`; id không trùng; cặp `include/extend` gần nhau. Đạt mới vẽ.

### B3 — Viết Nguồn
Viết/sửa generator (`gen_*.py`, `.puml`, `.drawio`, `.tldr`) trong `diagrams/`:

- Tuân thủ luật chống đè (layout bảng B2).
- Sử dụng module chung `svg_render.py` cho PNG (Chrome headless).
- Đặt `W`/`H` canvas phù hợp ratio 0.5–2.4.

### B4 — Render Ảnh
Chạy generator → xuất `.svg` vào `diagrams/` (source intermediate), rồi render `.png` vào `images/diagrams/`:

```bash
py -3 diagrams/gen_usecase_draw.py      # or gen_activity_svg.py, gen_sequence_svg.py, etc.
py -3 diagrams/svg_render.py            # or run from generator directly
```

Luôn xuất cả SVG (vector) + PNG (raster, scale 2.2x cho Word/PPTX).

### B5 — Audit (Eye QA)
Chạy `eye_audit.py` để tìm ứng viên lỗi:

```bash
py -3 "<sp-agent>/.claude/skills/use-case-layout/scripts/eye_audit.py" \
    images/diagrams/<ten>.svg --overlay --dump --out audit/soi-so-do/<đượt>/<ten>
```

Sinh ra `overlay.png` (lưới 10×10 + trục giữa đỏ) + `crops/F*.png` (zoom 4×). Sau đó:

1. Mở `overlay.png` → căn trục, nhịp khoảng cách.
2. Mở **từng** `crops/F*.png` → *đè thật hay báo oan?*
3. Điền `eye-audit.md` với bảng verdict `THẬT` / `BÁO OÁN`.

### B6 — Nghiệm Thu 5 Cổng
Chỉ báo `PASS` khi:

1. **Render validation:** PNG & SVG tồn tại > 500B, không banner error.
2. **Automated audit:** `audit-diagrams.mjs` báo 0 đỏ (zero-color, tỷ lệ frame, cỡ chữ).
3. **Visual review:** Đã mở `overlay.png` + MỌI `crops/` → trả lời ĐÈ? ĐỀU? DỄ NHÌN? với ≥ 3 nhãn nguyên văn.
4. **Semantic correctness:** Bước 0 tồn tại; mô hình khớp schema DB/mã nguồn; không include/extend bịa đặt.
5. **DOCX check:** Nếu chèn report, kiểm wp:extent không đổi (W/H canvas giữ nguyên).

### B7 — Swap vào DOCX (Tuỳ chọn)
Nếu chèn vào `Bao_cao_CNPM.docx` qua `docx-report` skill:

- Đọc SVG, chèn vào docx với caption `Hình X.Y: <tên>` + `keep_with_next`.
- Kích thước ảnh: giữ nguyên W/H pixel → wp:extent trong XML không cần sửa.
- Trước khi thay thế ảnh cũ, hỏi người dùng xác nhận nghiệm thu.

---

## 4. Vòng Sửa (Edit Loop — Minimal Patch Re-Render)

User muốn sửa sơ đồ:

1. **User nói chỗ sửa HOẶC tự sửa file nguồn:**
   - Vẽ tay: mở `.drawio`/`.tldr` trên app.diagrams.net / tldraw.com → kéo node, đi dây ngắn hơn.
   - Text-based: sửa file `.puml`/`gen_*.py` → adjust spacing, wrapping, positions.
2. **Agent KHÔNG sinh lại từ đầu:** sửa đúng chỗ (minimal patch) để giảm diff noise.
3. **Render lại CHỈ hình ảnh hưởng:** chạy generator lần nữa, ghi đè `.svg` + `.png`.
4. **Re-audit:** chạy lại `eye_audit.py` cho đúng hình đó, lưu vào `audit/soi-so-do/<thời-gian>-after-fix/<ten>/`.
5. **Mắt phán lại:** mở overlay + crops mới, điền verdict.
6. **Nếu chèn docx:** wp:extent không đổi nếu W/H canvas giữ nguyên (như kinh nghiệm thật `33a..33d`).

> [!CAUTION]
> **Không bao giờ sửa trực tiếp `.png`/.svg bằng tay mà không sửa source!** Đây là anti-pattern mất nguồn, làm mất khả năng tái sản xuất.

---

## 5. Lệnh Chuẩn (Copy-Paste Ready)

### Render
```bash
# Toàn bộ sơ đồ hiện tại (nếu chưa chạy lần đầu)
py -3 private-docs/diagrams/gen_usecase_draw.py
py -3 private-docs/diagrams/gen_activity_svg.py
py -3 private-docs/diagrams/gen_flow_svg.py
py -3 private-docs/diagrams/gen_sequence_svg.py
py -3 private-docs/diagrams/gen_state_svg.py
py -3 private-docs/diagrams/gen_modules_svg.py
py -3 private-docs/diagrams/gen_erd_svg.py
```

### Audit
```bash
# Kiểm chéo lồng nhau trong SVG (chống đè trực quan)
py -3 private-docs/diagrams/check_overlap.py

# Soi bằng mắt (use-case-layout scripts)
py -3 "<sp-agent>/.claude/skills/use-case-layout/scripts/eye_audit.py" \
      private-docs/images/diagrams/33a-usecase-nguoi-mua.svg \
      --overlay --dump --out private-docs/audit/soi-so-do/truoc-khi-sua/33a

# Auditors tổng quát (cho tất cả sơ đồ)
node "<sp-agent>/.claude/skills/diagram-auditor/scripts/audit-diagrams.mjs" \
     private-docs/images/diagrams
```

### Verify Pack (new)
```bash
# Kiểm hợp đồng thư mục (1:1 pairs, audit completeness)
py -3 "<sp-agent>/.claude/skills/diagram-pack/scripts/check_pack.py" \
      private-docs
```

---

## 6. Anti-Patterns

- ❌ **Sửa trực tiếp ảnh `.png`/.svg** mà không sửa source → mất truy vết.
- ❌ **Gen lại toàn bộ** khi chỉ 1 hình sai → tốn thời gian, diff noise lớn.
- ❌ **Bỏ soi ảnh sau khi sửa** (tin script 100%) → bỏ sót lỗi phát sinh trong lúc sửa (như `C-MASKED`).
- ❌ **Để code nguồn rải rác ở root/target** → gây nhầm lẫn, khó find sources.
- ❌ **Dùng CairoSVG cho tiếng Việt** → dấu bị đổi font, nhìn không đồng nhất.
- ❌ **Tuyên bố PASS khi chưa mở overlay+crops** → vi phạm proof-of-view.
- ❌ **Vòng xa** → nối dây qua mép canvas thay vì di chuyển node.

---

## 7. Definition of Done

Một diagram pack đạt khi:

- [ ] Bước 0 (`domain/step0-*.md`) tồn tại, có bằng chứng nguồn cho từng tác nhân.
- [ ] Source code sinh sơ đồ tồn tại trong `diagrams/` (`.py`, `.puml`, `.drawio`, `.tldr`).
- [ ] Image outputs 1:1 trong `images/diagrams/` (`.svg` + `.png` theo cặp).
- [ ] Eye-audit traces tồn tại trong `audit/soi-so-do/` với `overlay.png` + `crops/` + `eye-audit.md`.
- [ ] Visual QA: 3 câu ĐÈ? ĐỀU? DỄ NHÌN? đã được trả lời với ≥ 3 nhãn nguyên văn.
- [ ] Không còn lỗi `HIGH` trong eye-audit findings (trừ trường hợp cố ý ghi chú).
- [ ] Script `check_pack.py` chạy sạch (no errors), exit code 0.
- [ ] Nếu chèn docx: kích thước ảnh giữ nguyên W/H, caption khớp Hình X.Y.

---

## ⚡ PROMPT BẮT BUỘC KHI GỌI SKILL NÀY

> Khi bạn được yêu cầu gen sơ đồ hoặc tổ chức thư mục sơ đồ cho một dự án:
>
> 1. **HỎI THƯ MỤC ĐÍCH:** `<TARGET>/` là gì? (vd. `E:\...\btl-cnpm\private-docs`)
> 2. **CHỐP HỢP ĐỒNG:** trình bày tree + naming convention (§1.1–1.2), user xác nhận.
> 3. **CHECK BƯỚC 0:** thiếu Bước 0 → dừng, yêu cầu tạo `domain/step0-<du-an>.md`.
> 4. **GEN NGUỒN VÀO `diagrams/`:** không xả code block ra chat; chỉ giữ link source.
> 5. **RENDER -> IMAGES:** xuất cả SVG + PNG vào `images/diagrams/` theo cặp 1:1.
> 6. **AUDIT -> SOI ẢNH:** chạy `eye_audit.py` → mở overlay + MỌI crops → điền bảng verdict.
> 7. **RUN CHECK_PACK:** xác nhận 1:1 mapping + audit completeness → PASS/FAIL.
> 8. **STOP CHO USER ACCEPTANCE:** hiển thị ảnh preview + báo cáo 5 cổng, hỏi "Bạn kiểm tra giúp tôi: ảnh đã đạt để thay thế vào Word chưa?".
>
> **ANTI-PATTERNS TUYỆT ĐỐI KHÔNG:** sửa ảnh trực tiếp; gen hàng loạt + tuyên bố "N hình đều đạt" không dấu vết; bypass step0.
>
> **REPORT FORMAT CUỐI CÙNG:**
> ```
> Status: PASS | FAIL | BLOCKED
> Step 0: VERIFIED | MISSING
> Pack Integrity: PASS | FAIL (check_pack.py exit)
> Source files: diagrams/<các file>
> Rendered images: images/diagrams/<các cặp svg/png>
> Audit folders: audit/soi-so-do/<đợt>/<ten>/
> Verdict: ĐÈ? [YES/NO]; ĐỀU? [YES/NO]; DỄ NHÌN? [YES/NO] (+ ≥3 nhãn)
> Changed: <files changed>
> Next: wait for user acceptance → optional swap into docx
> ```

---

> **SSOT References:**
> - Directory contract detail: [`reference/dir-contract.md`](reference/dir-contract.md)
> - Checking pack integrity: [`scripts/check_pack.py`](scripts/check_pack.py)
> - Visual audit protocol: [`use-case-layout/reference/visual-audit-protocol.md`](../use-case-layout/reference/visual-audit-protocol.md)
> - Layout thinking: [`diagram-orchestrator/reference/layout-thinking.md`](../diagram-orchestrator/reference/layout-thinking.md)
> - Tool sweet spot: [`diagram-orchestrator/reference/tool-sweet-spot.md`](../diagram-orchestrator/reference/tool-sweet-spot.md)
