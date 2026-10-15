# Vẽ tay Fallback — Khi auto-layout vẫn xấu (SSOT)

> **Vị trí:** `diagram-orchestrator/reference/manual-fallback.md` là **SSOT**.
> Mọi skill sơ đồ (`plantuml-diagrams` §5, `use-case-layout` §3.3–3.4, `tldraw-diagrams` §1,
> `simplified-diagrams`) defer về đây. Không copy quy trình ra chỗ khác, chỉ trỏ link.

## 0. Khi nào kích hoạt (ngưỡng cứng)

Chuyển sang vẽ tay **khi và chỉ khi** đủ cả 2 điều kiện:

1. Đã làm **≥ 2 vòng render → soi → sửa-1-biến → render lại**
   (PlantUML: đã thử `nodesep`/`ranksep`, rút nhãn ≤ 25 ký tự, `xlabel`, đổi thứ tự khai báo,
   tách `package`/lane) mà **Visual Review vẫn FAIL**: dồn actor một phía, connector
   vòng xa / xuyên ellipse, nhãn đè viền `cluster`, dồn cục ≥ 3 node < 30px.
2. Lỗi là **hình học / bố cục**, KHÔNG phải lỗi nghiệp vụ.
   (Mô hình sai → sửa mô hình trước, cấm vẽ tay để che lỗi — xem `diagram-orchestrator` §3.13.)

**Cấm** nhảy sang vẽ tay ngay vòng 1 để "cho nhanh". **Cấm** vá mã auto vô hạn
(quá 3 vòng không tiến triển → dừng, chuyển fallback).

## 1. Ba đường fallback (chọn 1)

| Đường | File nguồn | Khi nào dùng | Mở bằng gì |
|---|---|---|---|
| **A. draw.io thủ công (khuyên dùng cho Use Case)** | `.drawio` (+ xuất `.svg` + `.png`) | Use Case ≥ 3 actor, cần actor 2 bên, `include/extend` nhiều nhánh | diagrams.net / VS Code extension |
| **B. tldraw kéo tay** | `.tldr` (+ xuất `.svg` + `.png` scale 2×) | Kiến trúc / flowchart / DFD cần vùng tự do, cong mềm | tldraw.com / VS Code extension |
| **C. SVG tay thuần** | `.svg` (+ xuất `.png` 300 DPI) | Chỉ khi A/B không cài được; sơ đồ nhỏ ≤ 9 node | Text editor + trình xem SVG |

Nguyên tắc: **freeze ngữ nghĩa đã duyệt** (Bước 0 + model UML) rồi mới dựng tay.
Vẽ tay chỉ đổi **vị trí / routing**, không đổi actor, use case, quan hệ.

## 2. Quy trình 6 bước (bắt buộc)

### Bước F1 — Chốt ngữ nghĩa (freeze)
- Khóa file Bước 0 `docs/domain/step0-<du-an>.md` + model UML (`<name>-model.md`).
- Xuất bản auto cuối cùng làm **baseline** (`<name>-auto-vN.png`) để so sánh.

### Bước F2 — Dựng khung tay
- **A (draw.io):** tạo `system boundary` trước, tên hệ thống mép trên; chia lane
  `L` (actor trái) / `C-L,C-R` (use case trong) / `R` (actor phụ/hệ thống ngoài) /
  `R-REL` (vùng `include/extend`). Dùng grid + snap, ellipse cùng nhóm đồng kích thước.
- **B (tldraw):** tạo frame/group theo vùng chức năng, đặt node trước, căn tâm/mép
  nhất quán, `bend` so le (`-20/0/20`) cho chùm cạnh song song.
- **C (SVG):** viewBox tỷ lệ 0.5–2.4, font `Segoe UI, Arial`, chữ ≥ 9pt ở A4.

### Bước F3 — Đi dây ngắn-trực tiếp (luật NO FAR LOOPS)
1. Nối association actor → use case **cột cạnh nó** trước (đường ngắn nhất).
2. Nối `include/extend` sau cùng; cặp base↔target **đặt gần nhau** (ngang hàng/liền kề).
3. Connector **ngắn, trực tiếp, lần theo được**; orthogonal/elbow chỉ khi làm rõ hơn.
4. **CẤM vòng xa** qua mép canvas; gặp vòng xa → **di chuyển node**, không kéo dây.
   (Chi tiết: `use-case-layout` §3.5.)

### Bước F4 — Giữ chuẩn học thuật (zero-color + UML)
- **Zero-color tuyệt đối:** nền `#FFFFFF`, viền/chữ `#000000` (`#1A1A1A/#333333` cho nét phụ,
  tô nhạt `#F1F1F1/#E3E3E3` nếu cần). `max(R,G,B)-min(R,G,B) ≤ 12`, cấm `title` trong ảnh.
- **Use Case UML:** actor = stick figure, use case = ellipse, boundary = rectangle;
  association = nét liền **không mũi tên**; `include/extend` = nét đứt + mũi tên hở + nhãn;
  kế thừa actor = tam giác rỗng; tên use case = động từ + đối tượng ≤ 25 ký tự.
- Caption `Hình X.Y: ...` do `docx-report` sinh, không nhúng vào ảnh.

### Bước F5 — Xuất đủ artifact
- Lưu nguồn chỉnh được: `.drawio` / `.tldr` / `.svg` tại `docs/diagrams/`.
- Xuất **đồng thời `.svg` + `.png`** (PNG 300 DPI hoặc scale 2×, > 500B).
- Đặt tên: `<name>-manual.drawio|.tldr` + `<name>-manual.svg|.png`;
  giữ bản auto cũ (`<name>-auto-vN.*`) để truy vết, không xóa.

### Bước F6 — Qua cổng auditor như bản auto
- Chạy `node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <thư-mục>` — 0 lỗi ĐỎ.
- Proof-of-View: mở PNG vào ngữ cảnh model, ghi ≥ 3 nhãn nguyên văn + vị trí +
  danh sách lỗi/không lỗi + dấu vết file (tên + dung lượng + thời điểm render).
- Báo cáo 5 kết quả độc lập + hỏi người dùng nghiệm thu trước khi swap vào DOCX
  (`diagram-orchestrator` §7).

## 3. Checklist PASS cho bản vẽ tay

- [ ] Có baseline auto + lý do chuyển fallback (vòng nào, lỗi gì, ảnh nào).
- [ ] Bước 0 + model UML đã freeze, không đổi ngữ nghĩa khi vẽ tay.
- [ ] Actor 2 bên (trái = chính, phải = phụ/ngoài), không actor vô cớ ở đáy.
- [ ] Không connector vòng xa / xuyên ellipse / đè nhãn; nhãn ≤ 25 ký tự.
- [ ] Zero-color, không `title`, chữ ≥ 9pt, ratio 0.5–2.4, ≤ 15 node (chi tiết) / ≤ 9 (khái niệm).
- [ ] Đủ nguồn + `.svg` + `.png` tại `docs/diagrams/`; audit 0 đỏ; Proof-of-View có bằng chứng.

## 4. Anti-patterns (cấm)

- Vẽ tay để **che mô hình sai** (thiếu Bước 0, actor là phương thức/kênh như VietQR/SePay/SMTP).
- Chỉ nộp PNG mà **không có file nguồn** (`.drawio`/`.tldr`/`.svg`).
- Xả mã XML draw.io / JSON tldraw ra chat (lưu đĩa + nhúng ảnh preview + link, như §8 orchestrator).
- Vẽ tay xong **bỏ qua auditor** vì "nhìn đã đẹp".
