# Use Case — Chuẩn bắt buộc khi vẽ tay (fallback)

> Dùng khi PlantUML/Mermaid **không vẽ đúng** Use Case (nhiều actor → tự dồn actor xuống đáy, đường nối chằng chịt).
> Vẽ tay (SVG) hoặc `.drawio` là ĐƯỢC PHÉP — nhưng **bắt buộc tuân thủ các quy tắc dưới đây**. Không tự do vẽ sai.

---

## 1. Phân loại phần tử (đúng/sai)

| Phần tử | Vẽ đúng | Vẽ SAI (cấm) |
|---|---|---|
| **Actor** | Hình người (stick figure), tên chức danh | Hình chữ nhật; hoặc biến **phương thức thanh toán/kênh** (SePay, VietQR, SMTP) thành actor |
| **Use case** | Ellipse, tên = *động từ + đối tượng* | Hình tròn/flowchart node; tên danh từ rời |
| **Ranh giới** | Hình chữ nhật bao quanh các use case | Không có ranh giới |
| **Association (actor–usecase)** | Đường **thẳng, KHÔNG mũi tên** | Mũi tên (sai — trông như luồng dữ liệu) |
| **`<<include>>`/`<<extend>>`** | Nét **đứt + mũi tên hở + nhãn**; nối **usecase↔usecase** | Nối actor↔usecase |
| **Kế thừa actor** | Tam giác rỗng `--|>` | Đường thường |

> **SePay/VietQR/SMTP KHÔNG phải actor.** Thanh toán = use case "Mua gói & thanh toán VietQR"; email OTP = bước trong use case, không vẽ SMTP thành actor (nếu buộc phải thể hiện hệ thống ngoài thì để **secondary xa bên phải**, KHÔNG để là actor nghiệp vụ chính).

---

## 2. Bố cục hai bên (bắt buộc khi nhiều actor)

```
[TRÁI]  Người dùng:  Khách · Phụ huynh/Học sinh · Gia sư
                 │  (đường thẳng ngắn, không xuyên ellipse)
                 ▼
        ┌─────────── cột use case ──────────┐   ┌── cột use case ──┐
        │  nhóm theo chức năng (package)    │──►│  include/extend   │
        └───────────────────────────────────┘   └───────────────────┘
                 ▲
[PHẢI]  Vận hành:  Kiểm duyệt viên · Quản trị viên  (+ hệ thống ngoài xa hơn)
```

Nguyên tắc:
- Mỗi actor nối **một cột use case cạnh nó** (đường thẳng ngắn, fan ra — không xuyên ellipse khác).
- Nhánh `include/extend` đi **ngang/gập vuông sang phải**, đặt use case nguồn ở **độ cao khác nhau** để nhánh không chồng.
- Actor vận hành **bên phải** — không dồn xuống đáy.

---

## 3. Quy trình 4 bước (trước khi vẽ)
1. **Chốt nghiệp vụ:** actor, mục tiêu từng actor, ranh giới hệ thống, include/extend/kế thừa (chỉ khi cần).
2. **Phân vùng bố cục:** nhóm use case theo chức năng; actor **hai bên**.
3. **Tối ưu đường nối:** hạn chế giao cắt; **không xuyên ellipse**; nhãn sát đường.
4. **Kiểm tra đầu ra:** A4, chữ không cắt, actor không chồng biên, đường nối không quá dài.

---

## 4. Kỹ thuật vẽ tay
- **SVG trắng–đen**: stick figure (đầu tròn + thân + tay + chân), ellipse `rx/ry` cố định, `font-family:"Segoe UI"`, không gradient/shadow.
- **`.drawio`**: mỗi actor `shape=umlActor;`, use case `ellipse;`, association `endArrow=none;`, include/extend `endArrow=open;dashed=1;`. Người dùng mở diagrams.net → export PNG/SVG.
- Render SVG → PNG bằng Playwright (viewport theo tỉ lệ khung, `deviceScaleFactor:2`).

---

## 5. Checklist trước khi nộp (PASS mới được giao)
- [ ] Không actor nào là **phương thức/kênh** (SePay/VietQR/SMTP).
- [ ] Actor đủ & **hai bên**; không actor ở đáy vô cớ.
- [ ] Association **không mũi tên**; include/extend **nét đứt có mũi tên + nhãn**.
- [ ] **Không đường nối xuyên ellipse**; giao cắt tối thiểu.
- [ ] Chữ không cắt; đọc được ở A4.
