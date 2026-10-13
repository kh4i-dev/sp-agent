---
name: tldraw-diagrams
description: Vẽ sơ đồ kiến trúc, flowchart, luồng dữ liệu, phân tầng, whiteboard đẹp và thẩm mỹ cao bằng tldraw; xuất ra SVG (vector sắc nét) và PNG 2x cho báo cáo DOCX, slide PPTX, README. Khắc phục nhược điểm đường vẽ cứng nhắc, gãy góc của Mermaid bằng đường cong mềm mại (bezier arc), bo tròn, bố cục hiện đại (giữ phong cách trắng-đen học thuật) và hỗ trợ file .tldr mở chỉnh sửa trực tiếp trên VS Code / tldraw.com. Dùng khi người dùng cần vẽ sơ đồ đẹp, sơ đồ nét mềm mại, tldraw, kiến trúc hệ thống, flowchart, nâng cấp/thay thế Mermaid.
---

# tldraw Diagrams Skill — Sơ đồ Thẩm mỹ cao cho Báo cáo & Slide

Mục tiêu: Tạo sơ đồ **thẩm mỹ cao, đường cong mềm mại (bezier arc), bố cục rõ ràng, giữ phong cách trắng-đen học thuật** cho báo cáo Word (`docx-report`), slide thuyết trình (`pptx-deck`), và tài liệu kỹ thuật. Khắc phục triệt để nhược điểm đường nối gãy khúc, thô ráp của Mermaid mặc định.

## Vì sao dùng tldraw thay cho Mermaid?

| Tiêu chí | Mermaid mặc định | tldraw-diagrams |
| :--- | :--- | :--- |
| **Đường nối (Edges / Arrows)** | Thường gãy góc trực giao (orthogonal), zíc zắc hoặc cắt ngang node | **Đường cong mềm mại (`kind: "arc"`, `bend`), bo góc tự nhiên, có điểm neo chuẩn** |
| **Hình khối (Nodes)** | Viền đen dày, màu cổ điển, phong cách kỹ thuật cũ | **Bo tròn hiện đại, phong cách Notion/Linear/Stripe, màu pastel hài hòa** |
| **Độ linh hoạt & Tương tác** | Tĩnh, chỉ sửa bằng text | **Sinh ra file `.tldr` mở trực tiếp trong VS Code hoặc tldraw.com để kéo thả, tinh chỉnh** |
| **Chất lượng xuất file** | SVG chuẩn | **Cả SVG vector (cho Word/PDF) lẫn PNG 2x/3x (cho PowerPoint)** |

---

## 1. Quy trình thực hiện (Workflow)

```text
Ý tưởng / Yêu cầu sơ đồ
   │
   ▼
1. Tạo file định nghĩa sơ đồ (JSON) hoặc convert từ file .mmd sẵn có
   │
   ▼
2. Chạy renderer tldraw: sinh ra .tldr, .svg và .png (scale 2x)
   │
   ▼
3. Visual QA: Soi ảnh SVG/PNG (bắt chữ đè, khoảng cách, nhãn cạnh)
   │
   ▼
4. Nhúng vào tài liệu DOCX hoặc Slide PPTX
```

---

## 2. Cách tạo sơ đồ qua JSON (Khuyên dùng)

Agent sinh một file `diagram.json` với cấu trúc rõ ràng (không cần tính toán tọa độ thủ công, script sẽ tự động auto-layout):

```json
{
  "title": "Kiến trúc Hệ thống Bán hàng & Dịch vụ Đặt hàng",
  "direction": "LR",
  "groups": [
    { "id": "client", "title": "Khách hàng & Giao diện", "color": "blue" },
    { "id": "gateway", "title": "API Gateway & Auth", "color": "violet" },
    { "id": "services", "title": "Dịch vụ Nghiệp vụ", "color": "green" },
    { "id": "data", "title": "Cơ sở Dữ liệu & Cache", "color": "orange" }
  ],
  "nodes": [
    { "id": "web", "label": "Web App (Next.js)\nClient Web UI", "group": "client", "color": "blue", "fill": "semi" },
    { "id": "mobile", "label": "Mobile App (Flutter)\nAndroid & iOS", "group": "client", "color": "blue", "fill": "semi" },
    { "id": "gw", "label": "Kong Gateway\nRate limit & JWT Auth", "group": "gateway", "color": "violet", "fill": "semi" },
    { "id": "order_svc", "label": "Order Service\nXử lý giỏ hàng & đơn", "group": "services", "color": "green", "fill": "semi" },
    { "id": "payment_svc", "label": "Payment Service\nCổng VNPAY / Momo", "group": "services", "color": "green", "fill": "semi" },
    { "id": "postgres", "label": "PostgreSQL Primary\nĐơn hàng & Giao dịch", "group": "data", "color": "orange", "fill": "semi" },
    { "id": "redis", "label": "Redis Cache\nSession & Rate Limit", "group": "data", "color": "red", "fill": "semi" }
  ],
  "edges": [
    { "from": "web", "to": "gw", "label": "HTTPS", "bend": 0 },
    { "from": "mobile", "to": "gw", "label": "HTTPS", "bend": 0 },
    { "from": "gw", "to": "order_svc", "label": "gRPC", "bend": 15 },
    { "from": "gw", "to": "payment_svc", "label": "gRPC", "bend": -15 },
    { "from": "order_svc", "to": "postgres", "label": "SQL query", "bend": 0 },
    { "from": "payment_svc", "to": "postgres", "label": "SQL write", "bend": 15 },
    { "from": "gw", "to": "redis", "label": "Token verify", "bend": -25 }
  ]
}
```

### Lệnh Render:
```bash
node .claude/skills/tldraw-diagrams/scripts/render.mjs --in diagram.json --png
```

- Tạo ra 3 file:
  1. `diagram.tldr`: File canvas tldraw native (mở bằng extension VS Code `tldraw` hoặc import lên `tldraw.com`).
  2. `diagram.svg`: File vector không vỡ nét khi in ấn/thu phóng trong Word/PDF.
  3. `diagram.png`: File ảnh raster độ phân giải cao (scale 2x) để dán vào Slide PowerPoint.

---

## 3. Chuyển đổi nhanh từ Mermaid `.mmd` sang tldraw

Nếu đã có sẵn file Mermaid (`.mmd`) nhưng muốn đường nét và hình khối đẹp hơn:

```bash
node .claude/skills/tldraw-diagrams/scripts/mermaid-to-tldr.mjs diagram.mmd --png
```

Script sẽ tự động:
1. Parse các khối `subgraph`, node, và edge `-->` từ Mermaid sang JSON chuẩn.
2. Render ra `.tldr`, `.svg` và `.png` với giao diện tldraw hiện đại.

---

## 4. QUY TẮC BẤT BIẾN: LUÔN LUÔN TRẮNG ĐEN (Monochrome / B&W)

Mọi sơ đồ dùng cho báo cáo, đồ án, luận văn và slide kỹ thuật **bắt buộc tuân thủ phong cách Trắng - Đen**:
- **Nền:** Luôn là nền trắng thuần (`#FFFFFF`), không đổ nền màu mè.
- **Viền & Đường nét (Stroke):** Luôn là màu đen (`color: "black"`), độ tương phản cao, nét in sắc nét.
- **Màu khối (Nodes):** Viền đen, nền trắng (`fill: "none"` hoặc `"semi"` để phân cấp nhẹ). Tuyệt đối **không** dùng khối xanh, đỏ, vàng, cam sặc sỡ.
- **Mũi tên (Arrows):** Màu đen (`color: "black"`), đầu mũi tên `arrow`, nhãn đen rõ nét.
- **Khung phân tầng (Groups/Frames):** Viền đen mảnh, nền trong suốt (`fill: "none"`), tiêu đề đen in đậm.

### Các thuộc tính điều khiển hình thức:
- **Kiểu nét vẽ (`dash`):**
  - `"draw"`: Nét vẽ tay mềm mại đặc trưng tldraw (tự nhiên, không khô cứng).
  - `"solid"`: Nét thẳng tắp hiện đại, chuẩn kỹ thuật.
  - `"dashed"`: Nét đứt (dùng cho luồng phụ, response, hoặc tương tác ngầm).
- **Độ cong mũi tên (`bend`):**
  - `0`: Đường nối thẳng trực tiếp.
  - `15` đến `30`: Đường cong uốn cong về phía trên/phải.
  - `-15` đến `-30`: Đường cong uốn cong về phía dưới/trái.
- **Hướng sơ đồ (`direction`):**
  - `"LR"`: Luồng từ trái sang phải (khuyên dùng cho kiến trúc hệ thống, phân tầng).
  - `"TD"`: Luồng từ trên xuống dưới (khuyên dùng cho flowchart xử lý nghiệp vụ).

---

## 5. Quy tắc QA cho Agent (Render & Visual Gate)

1. **Kiểm tra chữ trong khối (Labels):**
   - Không dồn quá nhiều chữ vào 1 dòng. Dùng ký tự xuống dòng `\n` để tách thành:
     `Tên thành phần\n(Công nghệ / Mô tả phụ)`
2. **Kiểm tra độ cong mũi tên (Bending):**
   - Nếu có nhiều đường nối song song từ cùng 1 nguồn (ví dụ Gateway -> 3 Services), gán giá trị `bend` so le (`-20`, `0`, `20`) để các đường mũi tên tách nhau ra, không đè lên nhau.
3. **Kiểm tra tỷ lệ hình (Aspect Ratio):**
   - Sơ đồ chèn Word/Slide nên có tỷ lệ ngang từ `16:9` đến `4:3`. Tránh sơ đồ quá dài một chiều (dọc quá mức hoặc ngang quá mức).
4. **Nhúng vào tài liệu:**
   - Trong `docx-report`: Dùng file `.svg` hoặc `.png`, luôn có caption bên dưới: `Hình X.Y. Sơ đồ kiến trúc hệ thống`.
   - Trong `pptx-deck`: Dùng file `.png` (scale 2x) căn giữa slide.
