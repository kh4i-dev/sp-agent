---
name: algo-flowchart
description: Vẽ SƠ ĐỒ KHỐI THUẬT TOÁN chuẩn giáo trình (kỹ thuật lập trình): oval Bắt đầu/Kết thúc, chữ nhật Xử lý, hình thoi Điều kiện Đúng/Không, hình bình hành Nhập/Xuất, mũi tên luồng gộp nhánh — export SVG → PNG trắng-đen bằng Python + ImageMagick, chèn vào .docx giữ 100% định dạng (Zero Regeneration), bắt buộc RENDER + soi mắt từng trang trước khi báo xong. Dùng khi người dùng nói "sơ đồ khối", "sơ đồ thuật toán", "flowchart chuẩn giáo trình", "sơ đồ giống trên lớp", "giống AI generated quá, vẽ lại kiểu sơ đồ khối", nhắc ký hiệu oval/hình thoi/hình bình hành, hoặc thấy sơ đồ thiếu/hỏng/hợp "AI gen" trong báo cáo đồ án. KHÔNG dùng cho Use Case/UML/ERD/kiến trúc (thuộc handdrawn-diagrams).
---

# algo-flowchart — Sơ đồ khối thuật toán chuẩn giáo trình

Mục tiêu: sinh **sơ đồ khối (flowchart) đúng chuẩn môn Kỹ thuật lập trình** — giáo viên/nhà
trường quen nhìn ký hiệu: `oval` Bắt đầu/Kết thúc, `rect` Xử lý, `hình thoi` Điều kiện
(Đúng/Không), `hình bình hành` Nhập/Xuất, mũi tên luồng; **trắng-đen, không màu**, đọc được
khi in A4. Người dùng đánh giá "giống AI gen" = bố cục kiểu wireframe hộp gạch, thiếu
ký hiệu chuẩn; skill này loại trừ đúng điểm đó.

## Không trùng skill khác

- Sơ đồ Use Case / UML / ERD / Class / Sequence / State / kiến trúc / cây-trie:
  **thuộc `handdrawn-diagrams`** (điều phối `coord-diagrams`). Skill này KHÔNG vẽ.
- Diagram branded/có màu (slide, web): **`diagram-design`**. Nghiêm cấm dùng cho báo cáo
  học thuật (luật trắng-đen).
- Chèn ảnh/sửa .docx giữ định dạng: **thuộc `safe-docx-modifier`**; kiểm tra trang:
  **`docx-report`** (Render gate + Vision gate). Skill này chỉ sinh ảnh + công thức chèn.

## 1. Ký hiệu chuẩn (bắt buộc)

| Ký hiệu | Dùng cho | Công thức SVG (cx, cy, w, h) |
|---|---|---|
| **Oval** (ellipse) | Bắt đầu / Kết thúc | `<ellipse rx=w/2 ry=h/2>` |
| **Chữ nhật** | Xử lý / tính toán / gán | `<rect>` |
| **Hình thoi** | Điều kiện, mỗi nhánh ghi `Đúng` / `Không` (chọn một cặp nhãn nhất quán, vd. Có/Không) | `<polygon cx,cy-h/2 cx+w/2,cy cx,cy+h/2 cx-w/2,cy>` |
| **Hình bình hành** | Nhập / Xuất (dữ liệu vào/ra) | `<polygon top-left shifted +sk>` |
| **Mũi tên** | Luồng; mỗi đầu có mũi tên tam giác đặc | `<line>` + `<polygon head 6.8pt>` |

Quy ước luồng:
- Cột chính đi từ trên xuống (cx cố định); nhánh phụ góc 90° sang trái/phải rồi **gộp về
  khối chung** (thường là "Xếp hạng"/"Tiếp tục").
- Nhãn nhánh đặt **sát đầu mũi tên, cách 6–10pt, KHÔNG đè lên ký hiệu**; nếu gap < 20pt thì
  đẩy khối nhánh xuống dưới (elbow 2 đoạn) rồi vẽ nhãn ở đoạn ngang.
- Mọi nhánh điều kiện **phải có cả 2 nhãn** (Đúng/Không); không còn nhánh "suy đoán".

## 2. Phong cách & thông số (bất biến)

- Nền trắng, nét `stroke="#000" stroke-width="1.1"`, chữ `#000`, font
  `font-family="Arial, Helvetica, sans-serif"`, size **8–9pt** (nhãn 8, tiêu đề khối 8.5–9
  đậm khi cần).
- Kích thước canvas theo **pt**; chiều ngang chuẩn khớp báo cáo: **431pt** như các hình
  chương 3 đang dùng (chèn inline với `wp:extent cx="5472000"` EMU). Mọi hình cùng chương
  phải cùng chiều rộng để không nhảy cỡ khi lật trang.
- Không icon, không màu, không emoji, không nền xám. Có thể dùng `·` `→` `×` `≈` `≤` `d`.
- Ghi chú số liệu (nếu có — telemetry) để trong **khung nét đứt** ở cuối, mỗi dòng
  ≤ ~50 ký tự; số liệu phải **đo thật từ code, cấm bịa**.

## 3. Quy trình 6 bước (không lược bỏ)

1. **Đặc tả luồng**: liệt kê từng khối + điều kiện + nhãn nhánh thành bảng (khối, loại
   ký hiệu, nhãn, nối tới). Vượt ~12 khối phải tách thành 2 hình hoặc rút gọn.
2. **Gen SVG**: dùng `scripts/flowchart_svg.py` (hàm `oval/rect/para/diamond`,
   `seg_arrow`, `note_box`) — không đặt tọa độ tay thiếu kiểm soát. Render PNG:
   `magick -density 300 -background white fig.svg -flatten fig.png`
   (ImageMagick nằm tại `C:\Program Files\ImageMagick-7*\magick.exe`).
3. **Soi PNG bằng mắt** (tool `read`): (a) chữ không tràn khung; (b) nhãn nhánh không đè;
   (c) đủ mũi tên; (d) ngôn ngữ nhất quán với báo cáo (vd. `khóa` không `khoá`).
4. Chèn vào .docx **Zero Regeneration** (mẫu thực dịch đã chạy thành công: script
   `tools/fix6_mo_phong.py` + `fix7_mo_phong_noteoff.py` trong thư mục dự án báo cáo):
   - clone paragraph ảnh có sẵn (đổi `rId`, `wp:docPr id` +1, `pic:cNvPr name`),
   - clone caption đúng style `anh`/`bang` (đổi bookmark `cap_h_x_y`, field
     `SEQ` → `\r n`, cached number),
   - clone dòng DANH MỤC tương ứng (đổi text + `PAGEREF cap_h_x_y \h`),
   - chèn câu dẫn trong thân bài để hình có lời dẫn ("Hình 3.7 thể hiện...").
   - thêm relationship `rIdN` vào `word/_rels/document.xml.rels` (MAX rId +1) + file vào
     `word/media/`. Cú pháp zip: ghi lại toàn bộ entry giữ nguyên bytes trừ 2 phần đã sửa.
5. **Render gate**: Word COM render PDF + PNG từng trang (script `docx-report`), field
   TOC/DANH MỤC tự cập nhật (cần `pywin32`: cả `Fields.Update()` lẫn
   `TablesOfContents.Update()`).
6. **Vision gate**: soi từng trang đã đổi + trang Danh mục; xác nhận (a) mới hiện đúng chỗ
   đúng caption; (b) số trang mục lục khớp; (c) trang CHƯƠNG kế tiếp vẫn sang trang mới;
   (d) tổng số trang thay đổi hợp lệ. Có bằng mắt mới kết luận PASS.

## 4. Bẫy phổ biến (thực tế đã dính)

- **Bẫy A — chữ tràn khung**: ước lượng độ rộng theo pt (Arial 9pt ≈ 5pt/ký tự HOA,
  3.9pt/ký tự thường); soi từng dòng PNG trước khi chèn.
- **Bẫy B — nhãn "Đúng" đè khối** khi gap ngang quá nhỏ. Cách đúng: elbow 2 đoạn
  (vẽ khối nhánh thấp xuống) rồi nhãn nằm trên đoạn ngang.
- **Bẫy C — ký tự đặc biệt**: `&` trong nội dung SVG/XML phải là `&amp;`; nội dung có
  văn bản lạ phải render thử + soi.
- **Bẫy D — số liệu bịa**: mọi con số (nút đã thăm, ms, số khóa...) phải chạy code thật
  trước khi vẽ. Không chạy được = bỏ hẳn cột số liệu.
- **Bẫy E — ngôn ngữ lẫn lộn**: khớp chính tả báo cáo (vd. "khóa" vs "khoá") phải đồng bộ.

## 5. Xong khi nào (definition of done)

- PNG có ký hiệu chuẩn đúng & sạch (mắt đã soi).
- Trang .docx render ra có hình + caption đúng dòng, DANH MỤC có dòng mới, không làm rớt
  bố cục chương sau.
- Số liệu telemetry truy nguyên được (đo thật, có log lệnh chạy).

## 6. PHONG CÁCH GIỐNG NGƯỜI LÀM (chống nhìn "AI gen") — luật bất biến

Dấu hiệu làm hình bị coi là "AI/tự sinh": khối cao thấp lêch vì khối to hơn nội dung,
text dồn trái góc, mũi tên đâm vào **viền khung tầng** thay vì chạm biên khối đích,
nhãn đè dây, khoảng trống chết trong khối. Tránh bằng bộ luật sau (đã kiểm chứng bằng
Hình 3.1 "kiến trúc 3 tầng" trong dự án BTL):

0. **Nhìn như hình sách giáo trình**: 3 dải tầng xếp trên dưới, ĐỀU chiều ngang và có
   lề ≥12pt so với mép canvas; tiêu đề tầng CĂN GIỮA đồng nhất ở mọi dải.
1. **Hệ lưới đo đếm**: cao khối = `HEAD (16pt) + LH (11pt) × số_dòng`. Tất cả các khối cùng
   hàng đều dùng công thức này — không khối nào cao hơn nội dung.
2. **Không khoảng trống chết**: bullet căn **trái thẳng hàng** (x0+5), tiêu đề **căn giữa
   đậm**; cấm thêm bullet "cho đủ" (cấm bịa nội dung).
3. **Mũi tên chạm biên khối đích** (head nằm TRÊN cạnh khối; không đâm vào
   viền khung tầng). Luồng liên tầng **gom về đúng khối trung tâm** của tầng.
4. **Liên tầng chỉ 1 mũi tên DỌC thẳng mỗi lần xuống tầng**, đặt tại cột khối đích,
   nhãn nằm bên phải. CẤM kiểu 3 mũi tên hội tụ bằng elbow treo lơ lửng giữa 2 dải
   tầng (nhìn như nét vẽ dở). Elbow chỉ dùng khi bắt buộc, tối đa 2 khúc và phải
   tránh hẳn chữ lẫn khối, không cắt xuyên khối nào.
5. **Nhãn luồng đặt ở khoảng an toàn** — vùng không có bất kỳ dây dọc/ngang nào đi qua;
   kiểm tra bằng mắt trước khi chốt (không dùng halo để che lỗi giao cắt).
   Đặc biệt: viền khung/chữ trong khung (vd. khung nét đứt "Chỉ mục trong RAM") KHÔNG
   được cắt qua tiêu đề tầng — đặt khung thấp hơn tiêu đề ≥6pt.
6. **Nhãn tầng** (TẦNG ...) được căn **giữa** để nhường hành lang dọc chạy hai bên — chọn
   vị trí SAU KHI vẽ xong toàn bộ dây chính.
7. Soi ảnh PNG **sau mỗi lần chỉnh tọa độ**: (a) mọi chữ trọn trong khung, (b) không có
   giao cắt dây×chữ, (c) mọi head chạm biên, (d) khoảng hở giữa các khối đồng đều.
