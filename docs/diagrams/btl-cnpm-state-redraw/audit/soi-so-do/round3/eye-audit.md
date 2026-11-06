# Soi bang mat — state-01-don-hang

> Sinh boi `eye_audit.py`. **Script KHONG phan quyet PASS/FAIL** — no chi liet ke UNG VIEN
> va cat anh phong to. Cong nghiem thu van la: **mo anh, tu nhin, tu tra loi**.

- Nguon: `docs/diagrams/btl-cnpm-state-redraw/images/diagrams/state-01-don-hang.svg`
- Khung: 1480 x 1030 (ty le 1.44:1)
- Do luong: 9 node ellipse · 20 nhan · 14 duong noi · 0 actor · 0 khung boundary
- Ung vien: **HIGH=0** · MEDIUM=7 · LOW=2 · INFO=0

## 0. BAT BUOC DIEN SAU KHI NHIN ANH

Mo `overlay.png` (co luoi) va tung file trong `crops/`, roi dien bang duoi.

| # | Ma | Zoom can xem | Mat thay gi (nguyen van) | That / Bao oan | Da sua? |
|---|---|---|---|---|---|
| 1 | C-DANGLE | `crops/F01-C_DANGLE.png` | Góc bo composite Trước vận chuyển liền nét, không phải cạnh | BAO-OAN | không cần |
| 2 | C-DANGLE | `crops/F02-C_DANGLE.png` | Cùng viền composite bị parser tính hai đầu | BAO-OAN | không cần |
| 3 | C-DANGLE | `crops/F03-C_DANGLE.png` | Góc bo composite Sau giao hàng liền nét | BAO-OAN | không cần |
| 4 | C-DANGLE | `crops/F04-C_DANGLE.png` | Cùng path viền kín bị parser nhầm | BAO-OAN | không cần |
| 5 | C-DANGLE | `crops/F05-C_DANGLE.png` | Cạnh chạm chấm đen initial, parser bỏ node | BAO-OAN | không cần |
| 6 | C-DANGLE | `crops/F06-C_DANGLE.png` | Cạnh chạm bullseye sau Đã hủy | BAO-OAN | không cần |
| 7 | C-DANGLE | `crops/F07-C_DANGLE.png` | Cạnh chạm bullseye sau Trả hàng | BAO-OAN | không cần |
| 8 | S-FONT | `crops/F08-S_FONT.png` | Đã đối chiếu PNG và 3 crop Chromium: dấu và arrowhead rõ; MuPDF fallback | BAO-OAN | không cần |
| 9 | D-DUP | `crops/F09-D_DUP.png` | Hai cạnh khác nguồn cùng nhãn trả hàng theo hợp đồng | CHAP-NHAN-DUOC | không cần |

Bang chung toi thieu de duoc coi la **DA SOI**: doc nguyen van >= 3 nhan + vi tri
(vd "ellipse 'Rút tiền' o cot giua, hang 8"), va tra loi du 3 cau **de? deu? de nhin?**

## 1. Ung vien MUC DO CAO — uu tien soi truoc

_(khong co)_


## 2. Ung vien MUC DO TRUNG BINH

- **C-DANGLE** — Duong #0 co dau LO LUNG tai (1064,70) — khong cham node/actor/nhan nao
  - Goi y sua: Keo neo dung vao bien node/actor; kiem lai toa do.
- **C-DANGLE** — Duong #0 co cuoi LO LUNG tai (1064,70) — khong cham node/actor/nhan nao
  - Goi y sua: Keo neo dung vao bien node/actor; kiem lai toa do.
- **C-DANGLE** — Duong #1 co dau LO LUNG tai (1424,390) — khong cham node/actor/nhan nao
  - Goi y sua: Keo neo dung vao bien node/actor; kiem lai toa do.
- **C-DANGLE** — Duong #1 co cuoi LO LUNG tai (1424,390) — khong cham node/actor/nhan nao
  - Goi y sua: Keo neo dung vao bien node/actor; kiem lai toa do.
- **C-DANGLE** — Duong #2 co dau LO LUNG tai (38,198) — khong cham node/actor/nhan nao
  - Goi y sua: Keo neo dung vao bien node/actor; kiem lai toa do.
- **C-DANGLE** — Duong #12 co cuoi LO LUNG tai (500,666) — khong cham node/actor/nhan nao
  - Goi y sua: Keo neo dung vao bien node/actor; kiem lai toa do.
- **C-DANGLE** — Duong #13 co cuoi LO LUNG tai (500,966) — khong cham node/actor/nhan nao
  - Goi y sua: Keo neo dung vao bien node/actor; kiem lai toa do.

## 3. Ung vien MUC DO THAP

- **S-FONT** — 12/20 nhan co >1 ho font tron lan trong 1 nhan (vd 'Trước vận chuyển': ['Helvetica', 'Noto Serif Regular']). Thuong do dau tieng Viet roi sang font du phong cua trinh render.
  - Goi y sua: Nhung font phu day du dau tieng Viet (Arial Unicode / DejaVu Sans) de 1 font duy nhat; kiem lai bang Chrome/LibreOffice chu khong chi viewer nay.
- **D-DUP** — Nhan 'chấp thuận trả hàng' xuat hien 2 lan Y NGUYEN VAN — kiem copy-paste
  - Goi y sua: Xac nhan co phai 2 use case that su khac nhau; neu khong thi gop lai.

## 4. Ghi chu thiet ke (KHONG phai loi)

_(khong co)_


## 5. Ket luan

```text
Da mo overlay.png?            YES
Da mo TAT CA crops/?          YES   (neu NO thi moi ket luan deu KHONG hop le)
De?        Chờ thanh toán trái trên; Đã xác thực giữa phải; Hoàn tất dưới phải; Trả hàng dưới trái. Không đè ở Chromium cuối.
Deu?       State 220x76, spine hàng trên đều, nhánh tách trái.
De nhin?   Theo được mỗi cạnh; không route vòng toàn canvas.
Ket luan:  PASS (chỉ Visual, PNG Chromium, rộng trình bày 25cm)   (CAM ghi PASS khi chua dien muc 0)
```

Overlay luoi: `overlay.png`
