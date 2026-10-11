# QUY TRÌNH TOÀN DIỆN: TỪ HỌC BÁO CÁO ĐẾN SLIDE BẢO VỆ ĐỒ ÁN (END-TO-END PIPELINE)

> Cẩm nang kỹ sư AI/Agent để tự động hóa toàn bộ quy trình: Đọc hiểu báo cáo dự án -> Rút trích sự thật -> Lập dàn ý -> Thiết kế template & background -> Chọn icon & 3D element -> Sinh PPTX -> Tiêm Speaker Notes -> Luyện phản biện vấn đáp -> Visual QA.

---

## 8 GIAI ĐOẠN THỰC THI (THE 8-STAGE PIPELINE)

```text
[Báo cáo / Docs]
       │
       ▼
[Giai đoạn 1: Khai phá & Học Báo Cáo] (Report Mining & Fact Extraction)
       │
       ▼
[Giai đoạn 2: Dàn Ý & Phân Cấp Thị Giác] (Assertion-Evidence, 1 slide = 1 ý)
       │
       ▼
[Giai đoạn 3: Thiết Kế Template & Nền 16:9] (Brand Colors, Negative Space)
       │
       ▼
[Giai đoạn 4: Bộ Icon & 3D Spot Illustration] (Assets chuẩn bị sẵn trên nền trắng)
       │
       ▼
[Giai đoạn 5: Sinh Slide Bằng Code] (PptxGenJS / Python-pptx, Chart native)
       │
       ▼
[Giai đoạn 6: Soạn & Tiêm Speaker Notes] (Lời thoại tự nhiên + tools/add_notes.py)
       │
       ▼
[Giai đoạn 7: Chuẩn Bị Bộ Câu Hỏi Chặn Vặn] (Dự trù câu hỏi hội đồng & đáp án 10đ)
       │
       ▼
[Giai đoạn 8: Render PDF & Visual QA Gate] (Soi từng slide, chống tràn chữ)
```

---

## GIAI ĐOẠN 1: KHAI PHÁ & "HỌC" BÁO CÁO (REPORT MINING)

Trước khi viết bất kỳ dòng slide nào, Agent phải đọc các tài liệu gốc của dự án:
- `BAO_CAO_*.md`, `README.md`, `DATABASE_BLUEPRINT.md`, `schema.prisma`.
- Trích xuất ra **Bộ 6 sự thật cốt lõi (Core Truths)**:
  1. **Bài toán thực tế**: Nỗi đau lớn nhất (Ví dụ: Ship COD bị bom hàng, tráo ruột, lộ thông tin PII).
  2. **Các tác nhân (Actors / Roles)**: Bao nhiêu vai trò (Người mua, Shop, Shipper, Admin...).
  3. **Kiến trúc hệ thống (Architecture)**: 3 tầng (Frontend Nuxt/React, Backend NestJS/FastAPI, CSDL SQLite/PostgreSQL).
  4. **Điểm sáng công nghệ khác biệt (Tech Highlights)**: Ví dụ ký số HMAC-SHA256, tem dùng 1 lần, quỹ ký quỹ Escrow, sổ cái kép.
  5. **Mô hình dữ liệu (ERD / Class Diagram)**: Bao nhiêu bảng, các thực thể chính và quan hệ số lượng.
  6. **Kết quả kiểm thử thực chứng (Test Evidence)**: Số kịch bản đã pass (11/11 luồng tiền, 100% khớp sổ cái, chạy thật có demo).

---

## GIAI ĐOẠN 2: DÀN Ý & BỐ CỤC SLIDE (ASSERTION-EVIDENCE)

### Nguyên tắc vàng:
1. **Một ý một slide**: Tuyệt đối không nhồi 2 chủ đề lớn vào 1 slide.
2. **Tiêu đề là câu khẳng định (Assertion Headline)**: 
   - ❌ *Không tốt:* "Quá trình giao hàng"
   - ✅ *Chuẩn:* "Xác thực & giải ngân ba dòng — Tiền chia tự động khi tem hợp lệ"
3. **Quy tắc 10/20/30**:
   - Font chữ nội dung tối thiểu từ **14pt – 18pt**; Tiêu đề từ **24pt – 32pt**.
   - Mật độ chữ trên slide không vượt quá **40 – 45 từ**. Phần giải thích dài đưa vào **Speaker Notes**.

### Cấu trúc 4 phần chuẩn đồ án tốt nghiệp:
- **Phần 1: Bối cảnh & Tác nhân** (Slide 1: Bìa -> Slide 2: Mục lục -> Slide 3: Nỗi đau -> Slide 4: Các vai trò).
- **Phần 2: Kiến trúc & Thiết kế** (Kiến trúc 3 tầng, Use Case, Phân rã phân hệ).
- **Phần 3: Luồng nghiệp vụ trọng tâm** (Đặt hàng, Đóng gói & Ký tem QR, Giao nhận, Giải ngân).
- **Phần 4: Cơ sở dữ liệu & Kiểm thử** (Máy trạng thái FSM, Class Diagram, ERD lõi, Demo & Kết luận).

---

## GIAI ĐOẠN 3: THIẾT KẾ TEMPLATE & NỀN SLIDE 16:9

### 1. Phối màu (Palette):
- Chọn **1 màu chủ đạo** (Primary) + **1 màu nhấn** (Accent) + **1 màu nền** (Background).
- *Ví dụ Tech/Fintech:*
  - Primary: `#0E3A47` (Xanh Navy đậm) hoặc `#0891B2` (Teal)
  - Accent: `#06B6D4` (Cyan neon) hoặc `#F59E0B` (Amber gold)
  - Background: `#FFFFFF` (Nền sáng) hoặc `#F8FAFC` (Xám nhạt dịu mắt)

### 2. Nguyên tắc khoảng trống âm bản (Negative Space):
- **Slide Bìa (Cover)**: Dành **50% diện tích bên trái** là nền trơn (cho tiêu đề và tên sinh viên), dồn toàn bộ đồ họa 3D/vector sang **nửa bên phải**.
- **Slide Nội dung (Content)**: Nền phải là **trắng trơn hoặc cực tối giản (>85% diện tích)**. Hoa văn vi mạch/lưới polygon chỉ được xuất hiện rất mờ ở các góc ngoài mép viền, tuyệt đối không chèn hình ảnh to ở giữa làm chìm text/sơ đồ.

---

## GIAI ĐOẠN 4: THƯ VIỆN ICON & HÌNH MINH HỌA 3D

1. **Icons**:
   - Đồng bộ một phong cách (Line icon hoặc Flat icon). Kích thước chuẩn: `24x24px` hoặc `32x32px`.
   - Các icon cơ bản cần có: `wallet`, `shield-check`, `package`, `qrcode`, `truck-delivery`, `database`, `chart-bar`.
2. **Hình 3D Spot Illustration (Minh họa cô lập)**:
   - Sinh ảnh với câu prompt: `Isolated on pure solid white background (#ffffff), clean studio lighting, zero background shadows`.
   - Giúp dễ dàng chèn vào bất kỳ vị trí trống nào trên slide mà không sợ viền ảnh bị lộ vệt cắt.

---

## GIAI ĐOẠN 5: SINH SLIDES BẰNG CODE (PPTXGENJS)

Khuyến nghị sử dụng **PptxGenJS (Node.js)** vì tạo ra file `.pptx` chuẩn OpenXML, có thể click vào sửa từng shape và chart:

```javascript
// tools/slides/make-slides.mjs
import pptxgen from 'pptxgenjs';

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE'; // 16:9 (13.33 x 7.5 inches)

// Hàm tạo card chuẩn
function card(s, x, y, w, h, { fill = 'FFFFFF', line = 'DCE8EC' } = {}) {
  s.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: line, width: 1 } });
}
```

---

## GIAI ĐOẠN 6: SOẠN & TIÊM SPEAKER NOTES

### 1. Viết file `speaker_notes.md`:
```markdown
<!-- slide 16 | Máy trạng thái đơn hàng -->
Thưa thầy cô, slide này thể hiện Máy trạng thái (State Machine)...

<!-- slide 17 | Class diagram -->
Thưa thầy cô, sơ đồ lớp này gồm 8 thực thể lõi...
```

### 2. Tiêm tự động vào file PPTX:
Sử dụng script có sẵn trong skill:
```bash
python .claude/skills/pptx-deck/scripts/add_notes.py deck.pptx speaker_notes.md
```

---

## GIAI ĐOẠN 7: BỘ CÂU HỎI CHẶN VẶN & PHẢN BIỆN HỘI ĐỒNG

Khi bảo vệ, thầy cô luôn xoay quanh tính nhất quán giữa Phân tích, Cơ sở dữ liệu và Code:

1. **Về Biểu đồ lớp vs CSDL**:
   - *Hỏi:* "Tại sao trong Class Diagram chỉ ghi `+string status` mà không ghi `pending_payment`, `paid`?"
   - *Đáp:* "Dạ Class Diagram mô tả cấu trúc tĩnh nên chỉ thể hiện Tên thuộc tính và Kiểu dữ liệu. Còn các trạng thái cụ thể là Miền giá trị động (Domain values) của cột `status`, em đã thể hiện ở biểu đồ Máy trạng thái (Slide 16) ạ."

2. **Về Tính đóng gói OOP**:
   - *Hỏi:* "Tại sao các thuộc tính đều để dấu cộng `+` (public)?"
   - *Đáp:* "Dạ vì đây là Biểu đồ thực thể dữ liệu (Data Entity Model) ánh xạ với CSDL. Toàn bộ logic nghiệp vụ và tính đóng gói được đặt chặt chẽ ở tầng Dịch vụ (Service layer) ạ."

3. **Về Khóa chính & Quan hệ tách bảng**:
   - *Hỏi:* "Tại sao `Order` phải tách ra `Parcel` và `EscrowHold`?"
   - *Đáp:* "Dạ để phục vụ đơn đa shop (1 đơn nhiều kiện hàng) và quản lý sổ cái ký quỹ độc lập, cho phép giải ngân hoặc đóng băng tranh chấp độc lập từng kiện mà không ảnh hưởng toàn bộ đơn ạ."

---

## GIAI ĐOẠN 8: RENDER PDF & VISUAL QA GATE

Không bao giờ giao slide khi chưa soi trực quan:
```bash
# 1. Xuất PDF và ảnh PNG từng slide (tự động nhận PowerPoint COM trên Windows)
python .claude/skills/pptx-deck/scripts/render_pptx.py deck.pptx --output_dir render

# 2. Quét kiểm tra chất lượng tự động:
python .claude/skills/pptx-deck/scripts/inspect_deck.py deck.pptx --verbose
```

### Bảng kiểm định trước khi nộp (Checklist):
- [ ] 100% slide đã có Speaker Notes.
- [ ] Không có slide nào tràn chữ ra mép hoặc bị che khuất bởi footer.
- [ ] Sơ đồ kiến trúc / ERD rõ nét, chữ không bị nhòe vỡ hạt.
- [ ] Số trang và footer đồng bộ từ slide đầu đến slide cuối.
