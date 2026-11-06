# Playbook: Sơ đồ dày (nhiều quan hệ đan chéo)

Rút kinh nghiệm thực chiến (đồ án kết nối gia sư, 10/2026): PlantUML auto-layout
gãy khi một hub (VD `User`) nối 7+ quan hệ + quan hệ kép cùng cặp lớp
(`reviewer`/`reviewee`, `files`/`resolves`). Không chữa bằng cách xếp thêm
`hidden` links hàng loạt — càng thêm càng rối.

## 1. Thử rẻ trước (1 biến/lần)

```plantuml
left to right direction
skinparam linetype polyline
skinparam nodesep 30
skinparam ranksep 45
```

Xóa toàn bộ chuỗi `-[hidden]-` cũ rồi render + soi. `polyline` đỡ góc vuông
cứng, `left to right` dàn hàng ngang. `dpi 300` chỉ tăng phân giải, không sửa bố cục.

## 2. Gợi ý hướng cho từng quan hệ khó

Cú pháp `-up-` / `-down-` / `-left-` / `-right-` chen vào giữa quan hệ, VD:

```plantuml
TutorProfile "1" -up-> "0..*" ConnectionRequest : receives >
Review "0..*" -down-> "1" User : reviewee >
```

Dùng khi hai quan hệ song song đè nhãn nhau: cho một đường đi dưới,
một đường đi phải. Render + soi sau MỖI gợi ý (chúng có thể xáo cả bố cục).

## 3. Phân rã khi vẫn đè (quy tắc chính)

Ngưỡng: hub nối ≥ 7 quan hệ, hoặc cặp quan hệ kép (`reviewer`/`reviewee`)
không tách được nhãn → phân rã theo nghiệp vụ, mỗi hình ≤ 6 lớp:

- 3.xa — Định danh & hồ sơ: `User, Profile, TutorProfile, Doc, Post, Favorite`
- 3.xb — Kết nối & hội thoại: `User, TutorProfile, Request, Conversation, Participant, Message`
- 3.xc — Đánh giá & báo cáo: `User, Request, Review, Report`

Lớp lặp lại ở nhiều hình phải GIỮ NGUYÊN thuộc tính/phương thức (góc nhìn,
không phải mô hình riêng). Đánh số caption liên tục (3.3→3.8) để giữ field
`SEQ`/`REF` tự động — không dùng hậu tố tay kiểu "3.4a" (gãy TOF).

## 4. Bẫy Kroki: PNG bị cắt ở 4096px

Kroki cắt PNG ngang ở ~4096px nhưng SVG vẫn đủ. Sau render LUÔN kiểm tra
`width` trong SVG + soi PNG: nếu nội dung phải bị cắt → chuyển sang top-down
(xếp dọc, VD `erd_c_trust.puml`) hoặc sang vẽ tay.

## 5. Vẽ tay SVG/PNG (fallback cuối, đã được người dùng duyệt)

Khi auto-layout bó tay: `tools/draw_diagram.py` (engine boxes + orthogonal
routing + halo chữ) + script layout riêng, VD `tools/layout_class_bc.py`.
Luật: lưới cột cố định, mỗi quan hệ đi làn (lane) riêng, nhãn đặt trên đoạn
ngang trong khoảng trống, mults có halo trắng, canvas portrait vừa trang A4
(ratio 0.5–2.4), font DejaVu Sans (đủ dấu Việt), zero-color, không title.
Xuất đồng thời `.png` (supersample 2x) + `.svg`. Nguồn chỉnh sửa = script
layout trong `tools/`, ảnh ra `docs/diagrams/`.

## 6. Quan hệ kép cùng cặp lớp

Giữ đủ cả hai (ngữ nghĩa nghiệp vụ), tách bằng hướng đi khác nhau (§2) hoặc
làn song song cách nhau ≥ 20px. Nếu script `audit-diagrams.mjs` báo "quan hệ
2 chiều trùng lặp" trong khi mắt thấy hai đường + hai nhãn tách bạch → ghi
nhận false-positive có bằng chứng soi ảnh, không xóa quan hệ để qua cổng.
