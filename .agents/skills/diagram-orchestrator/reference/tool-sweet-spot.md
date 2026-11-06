# Tool Sweet-Spot — Loại sơ đồ nào AUTO đẹp, loại nào phải VẼ TAY (SSOT)

> **Vị trí:** `diagram-orchestrator/reference/tool-sweet-spot.md` là **SSOT** cho câu hỏi
> *"sơ đồ này nên để công cụ tự sinh (PlantUML/Graphviz/tldraw) hay phải vẽ tay (draw.io/SVG)?"*
> Mọi skill sơ đồ (`plantuml-diagrams`, `use-case-layout`, `tldraw-diagrams`,
> `simplified-diagrams`, `diagram-auditor`) defer về đây, không diễn giải lại.
> Bằng chứng thực nghiệm nằm ở [`layout-thinking.md`](layout-thinking.md) §9–§14.

## 0.0. QUYẾT ĐỊNH MỚI NHẤT (2026-11-01) — VẼ TAY 100%, BỎ AUTO

> [!IMPORTANT]
> **Toàn bộ mục §0, §0.1 và bảng §1 dưới đây là LỊCH SỬ, không còn hiệu lực để chọn công cụ.**
>
> Từ 2026-11-01, theo yêu cầu người dùng (*"vẽ tay hết các sơ đồ, không dùng PlantUML hay các
> công cụ ngoài, chỉ vẽ xấu và hard"*):
>
> - **MỌI sơ đồ kỹ thuật** (Use Case, Class, ERD, Sequence, Activity, State, DFD, BFD, kiến trúc,
>   cây/trie/BK-tree) đều **VẼ TAY bằng SVG sinh từ Python với toạ độ hằng số** —
>   skill `handdrawn-diagrams`.
> - **PlantUML / Graphviz / Mermaid / drawio = NHÁP** để nghĩ bố cục, **không phải bản nộp**.
> - Lý do: công cụ ngoài **không ghim được vị trí**, nhãn trôi, dây xuyên node, và **không kiểm
>   soát được** để sửa từng pixel. Vẽ tay + toạ độ cứng cho kết quả tất định, sửa được, và
>   kiểm định được bằng `audit_svg.py` (E1..E6).
> - Câu hỏi "AUTO hay VẼ TAY?" **không còn tồn tại** → luôn VẼ TAY.
>   Bảng §1 giữ lại chỉ để tham khảo lịch sử/bằng chứng.
>
> Thay thế: `handdrawn-diagrams/SKILL.md` + `handdrawn-diagrams/reference/coordinate-workflow.md`.

## 0. Nguyên tắc mẹ: cấu trúc quyết định, không phải sở thích

- **Auto (PlantUML / Graphviz / tldraw-renderer) = ĐẸP khi bố cục là HỆ QUẢ TẤT ĐỊNH của cấu trúc.**
  Chuỗi tuần tự, cây, lưới: engine tự xếp ra hình cân đối, đều, ít giao cắt → auto thắng.
  (*State Machine và Activity KHÔNG còn thuộc nhóm auto — xem quyết định dự án ở §0.1.*)
- **Vẽ tay (draw.io / SVG) = CHUẨN khi bố cục do CON NGƯỜI quyết (vị trí tuyệt đối).**
  Khi cần ghim actor hai bên, đặt hub ở giữa, để "hành lang" cho dây đi, hoặc nhóm theo vùng tự do:
  auto không ghim được vị trí → phải vẽ tay.
- **Không có công cụ nào vẽ mọi thứ vừa đẹp vừa đúng.** Chọn theo bản chất, không theo thói quen.

## 0.1. Quyết định dự án (2026-10-26): STATE & ACTIVITY = VẼ TAY BẮT BUỘC

> [!CAUTION]
> Theo yêu cầu của người dùng (chuẩn ảnh mẫu: State kiểu Nulab — state bo tròn + nhãn sự kiện
> đặt đúng trên cạnh; Activity kiểu swimlane 2 lane "Người dùng | Hệ thống"), **State Machine
> và Activity Diagram chuyển từ AUTO sang VẼ TAY (draw.io/SVG) BẮT BUỘC**, ngang hàng Use Case.
> Lý do kỹ thuật: cả hai loại đều cần **ghim vị trí phần tử và điểm neo nhãn trên cạnh**
> (nhãn `enterButton_onclick`, guard `Hợp lệ/Không hợp lệ` phải nằm đúng cạnh đó) —
> auto-layout hay làm nhãn sự kiện trôi giữa hai state/lane, dây chéo xuyên qua node,
> lane tự dồn. PlantUML/Graphviz chỉ dùng làm **bản nháp tham chiếu**, không phải bản nộp.
> Quy tắc bố cục chi tiết: `plantuml-diagrams/reference/state-rules.md` và
> `plantuml-diagrams/reference/activity-rules.md`.

## 1. Bảng điểm ngọt (Sweet-Spot Table)

| Loại sơ đồ | Công cụ nên dùng | Vẽ tay hay Auto? | Vì sao (bằng chứng) |
|---|---|---|---|
| **Use Case** | **draw.io / SVG tay** (PlantUML chỉ để nháp) | **VẼ TAY (bắt buộc)** | PlantUML không ghim vị trí actor, không chia 2 cột UC với actor hai bên → dồn 1 cột, dây quạt dài. `[layout-thinking §11.6]` |
| **Class Diagram** (≥ 6 lớp, có hub bậc ≥ 5, hoặc nhiều association cùng cặp) | **draw.io tay** hoặc **phân rã** | **VẼ TAY / PHÂN RÃ** | Auto cho ra hình học Y HỆT nhau dù đổi hint/lock → hết đường ép auto. `[layout-thinking §10.6]` |
| **Class Diagram** (nhỏ, 4–6 lớp, quan hệ thưa) | PlantUML auto | Auto | Ít ràng buộc, auto xếp gọn được. |
| **ERD** (vừa, ≤ 4 cột, không nhãn động từ trên đường) | PlantUML auto (theo luật) | Auto-first | Áp luật "cạnh kề + bỏ nhãn verb" → nhảy điểm 3.5→5/6, không cần vẽ tay. `[layout-thinking §9]` |
| **ERD** (rất dày, > 4 cột / > 8 bảng) | Auto rồi **trang ngang / tách miền**, hoặc draw.io | Auto + tách, tay khi bí | 5 cột @300DPI ≈ 35cm > A4 → landscape hoặc tách domain. `[layout-thinking §9.5]` |
| **Sequence** | **PlantUML auto** | **AUTO (đẹp)** | Guided (autonumber + alt/opt + activate) đọc được ngay, cùng nội dung khác tư duy. `[layout-thinking §12]` |
| **Activity** | **draw.io / SVG tay** (PlantUML chỉ để nháp) | **VẼ TAY (bắt buộc)** | Swimlane cần ghim lane "Người dùng\|Hệ thống" + nhãn guard đúng trên cạnh rẽ; auto hay làm nhãn trôi, dây chéo xuyên node. `[§0.1 quyết định dự án]` |
| **State Machine** | **draw.io / SVG tay** (PlantUML chỉ để nháp) | **VẼ TAY (bắt buộc)** | Cần ghim vị trí state + nhãn sự kiện `event [guard] / action` đúng trên cạnh; chu kỳ `backButton_onclick` dễ thành dây chéo/vòng xa khi auto. `[§0.1 quyết định dự án]` |
| **Prefix Trie / BK-Tree / AST / đồ thị thuật toán có trọng số** | **Graphviz DOT auto** | **AUTO (đẹp)** | Cây phân cấp là bố cục tất định của DOT. `[decision-matrix §2]` |
| **Kiến trúc tổng quan (High-Level)** | **tldraw / draw.io** | **Đặt tay (vùng tự do)** | Cần phân vùng trực quan (Client/Gateway/Service/DB), bo góc mềm — auto (PlantUML) không kiểm soát vùng. `[decision-matrix §1]` |
| **DFD / Deployment (trực quan mạng)** | **tldraw / draw.io** | **Đặt tay** | Nhiều vùng, mũi tên dữ liệu cần vị trí chính xác. |
| **Deployment (chuẩn UML node/artifact)** | PlantUML auto | Auto | Nếu chỉ là node/artifact UML thuần, auto đủ. `[decision-matrix §1]` |
| **Flowchart xử lý nghiệp vụ** | PlantUML Activity (auto) hoặc tldraw (thẩm mỹ cong) | Auto ok; tay khi cần cong đẹp | Logic tuần tự auto tốt; cần nét mềm/hiện đại → tldraw. `[tldraw-diagrams]` |
| **Mô hình khái niệm tinh gọn** (5–9 thực thể) | PlantUML auto (lưới 3 cột tiết chế) | Auto | Ít thực thể + lưới đơn giản → auto đủ. `[simplified-diagrams]` |

## 2. Luật chọn công cụ (1 câu)

> **Nếu bố cục là hệ quả tất định của cấu trúc (chuỗi/cây/lưới) → để AUTO.**
> **Nếu bố cục cần vị trí tuyệt đối do người quyết (actor hai bên, hub giữa, vùng tự do, lane swimlane, nhãn neo trên cạnh) → VẼ TAY (draw.io/SVG).**
> **Riêng STATE MACHINE và ACTIVITY: VẼ TAY BẮT BUỘC theo quyết định dự án §0.1, không phụ thuộc dấu hiệu.**

Dấu hiệu buộc VẼ TAY: actor ≥ 2 bên · ≥ 3 actor cần phân vùng · hub bậc cao · nhiều association cùng cặp · cần "hành lang" cho dây · cần nhóm theo vùng tự do · cần ghim lane swimlane · cần nhãn neo đúng trên một cạnh cụ thể.

Dấu hiệu nên AUTO: chuỗi thời gian (Sequence) · cây/phân cấp (Trie/BK-Tree/AST) · ERD vừa và thưa. *(State và Activity không còn trong danh sách này — xem §0.1.)*

## 3. Nhưng chọn đúng công cụ vẫn chưa đủ — phải NGHĨ trước và SOI ảnh sau

1. **NGHĨ trước khi vẽ:** lập bảng adjacency-first + chọn zone + dự đoán bố cục
   ([`layout-thinking.md`](layout-thinking.md) §1–§2) **trước khi viết một dòng code**.
   Không "render rồi tính".
2. **SOI ảnh sau khi vẽ:** mở PNG vào ngữ cảnh model, tự trả lời **đè / đều / dễ nhìn**
   ([`diagram-auditor`](../diagram-auditor/SKILL.md) §2). Script chỉ tham khảo, không thay mắt.
3. **Khi auto ≥ 1–2 vòng không tiến triển → dừng vá, chuyển vẽ tay/phân rã**
   ([`manual-fallback.md`](manual-fallback.md)). Cấm vá tham số vô hạn.
