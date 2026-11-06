# Coordinate Workflow — hướng dẫn chi tiết

Tài liệu này là bản mở rộng của `SKILL.md`. Đọc khi cần dựng sơ đồ mới hoặc sửa bố cục.

---

## 1. Dựng project mới (5 phút)

```text
<project>/
  docs/
    diagrams/                 # NGUỒN
      gen_usecase.py          # mỗi sơ đồ 1 generator
      gen_class_erd.py
      spec/                   # *.json (toạ độ máy đọc — nguồn sự thật)
      drawio/                 # *.drawio (bản web-editable, tuỳ chọn)
      vectors/                # SVG (DUY NHẤT)
    images/diagrams/          # PNG (DUY NHẤT)
    tools/                    # công cụ (không để script rác ở root)
      build_all.py
      audit_svg.py
      selftest_audit_svg.py
      verify_endpoints.py
```

Sao chép các script `scripts/` của skill này vào `docs/tools/` của project.

**Luật thư mục:**
- `.json` spec → `docs/diagrams/spec/`
- `.svg` → `docs/diagrams/vectors/` **DUY NHẤT**
- `.drawio` (nếu có) → `docs/diagrams/drawio/` **DUY NHẤT**
- `.png` → `docs/images/diagrams/` **DUY NHẤT**

Cấm lẫn SVG/Drawio vào thư mục PNG; cấm để PNG trong `vectors/`.

---

## 2. Generator skeleton (mẫu tối thiểu)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_<ten>.py — <mô tả>. Vẽ tay SVG, toạ độ cứng, không công cụ ngoài."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_PNG = ROOT / "docs" / "images" / "diagrams"
OUT_SVG = ROOT / "docs" / "diagrams" / "vectors"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
SCALE = 2
W, H = 1600, 900          # ← toạ độ canvas, HẰNG SỐ

FONT = "Arial, Helvetica, sans-serif"
HALO = 'paint-order="stroke" stroke="#fff" stroke-width="3.5" stroke-linejoin="round"'


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build() -> str:
    c, n = [], []                      # c = hình, n = chữ
    # ... vẽ bằng toạ độ số cứng ở đây ...
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" font-family="{FONT}">\n'
            f'<rect width="{W}" height="{H}" fill="#fff"/>\n'
            + "\n".join(c) + "\n" + "\n".join(n) + "\n</svg>")


def main() -> int:
    OUT_PNG.mkdir(parents=True, exist_ok=True)
    OUT_SVG.mkdir(parents=True, exist_ok=True)
    p_svg = OUT_SVG / "<ten>.svg"
    p_png = OUT_PNG / "<ten>.png"
    p_svg.write_text(build(), encoding="utf-8")
    subprocess.run([str(CHROME), "--headless=new", "--disable-gpu",
                    f"--force-device-scale-factor={SCALE}",
                    f"--window-size={W},{H}", f"--screenshot={p_png}",
                    "--hide-scrollbars", "--default-background-color=FFFFFFFF",
                    p_svg.as_uri()], check=True)
    print(f"OK  {p_svg.name} + {p_png.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Bẫy:** thiếu `--window-size` → Chrome chụp khung mặc định 800×600 → ảnh trắng/cụt.
**Bẫy:** `encoding="utf-8"` bắt buộc, nếu không tiếng Việt thành `?`.

---

## 3. Layout spec JSON (sơ đồ hộp)

```json
{
  "generator": "docs/diagrams/gen_example.py",
  "diagram_type": "erd",
  "canvas": {"width": 2300, "height": 1100},
  "grid": {
    "box_width": 300,
    "col_left": [20, 500, 980, 1460, 1940],
    "head_height": 40,
    "line_height": 21
  },
  "entities": [
    {"id": "user", "name": "User", "col": 0, "top": 70,
     "fields": ["id: int", "email: string"]}
  ],
  "relationships": [
    {"id": "user_user", "a": "user", "b": "user",
     "mult_a": "1", "mult_b": "*",
     "points": [[320,80],[362,80],[362,100],[320,100]]}
  ]
}
```

Hộp cao = `head_height + line_height × len(fields)` — nên **không cần khai báo height**.

Kiểm: `py -3 verify_box_layout.py layout_spec.json` → phải `PASS`.

---

## 4. Quy tắc tuyến dây (bắt buộc)

| Tình huống | Cách đi |
|---|---|
| Hai hộp **cùng cột**, liền kề | đoạn thẳng khi hành lang trống; kênh bên cạnh nếu cần tránh hình |
| Hai hộp **cùng cột**, không liền kề | **vẫn** kênh bên cạnh, kéo dài theo trục dọc |
| Hai hộp **khác cột** | kênh dọc giữa 2 cột, elbow 1 lần vào vỉa |
| Hai hộp **kề nhau, cùng hàng** | đường thẳng ngang |
| Nhiều dây cùng đi qua 1 kênh | so le ≥ 16 px |

**Cấm:** tuyến xuyên hộp trung gian. Đường thẳng giữa hai hộp liền kề có hành lang trống là hợp lệ.

### 4.1. Đầu mút phải chạm biên

Đầu mút là điểm có `x == x1|x2` (trong dải y) hoặc `y == y1|y2` (trong dải x).
Sai 1 px cũng bị `verify_box_layout.py` bắt (dung sai `EPS = 1.0`).

### 4.2. Ký hiệu Crow's foot trùng axis

```python
def edge_normal(x, y, box):
    x1, y1, x2, y2 = box
    d = [("left", abs(x - x1)), ("right", abs(x - x2)),
         ("top", abs(y - y1)), ("bottom", abs(y - y2))]
    side = min(d, key=lambda p: p[1])[0]
    return {"left": (-1.0, 0.0), "right": (1.0, 0.0),
            "top": (0.0, -1.0), "bottom": (0.0, 1.0)}[side]
```

**Đừng** tính `unit(x - cx, y - cy)` từ tâm hộp → ký hiệu bị nghiêng.

---

## 5. Nhãn không bị dây cắt

```python
n.append(f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="middle" {HALO}>{esc(t)}</text>')
```

Halo trắng `stroke-width=3.5` phủ lên dây nối nằm sau → mắt đọc sạch. `audit_svg.py`
chỉ công nhận che khuất trắng đúng thứ tự vẽ; halo không miễn E2 và không thay sửa bố cục.

---

## 6. Use Case (khó nhất)

Không tự viết lại từ đầu — dùng bộ vẽ đã kiểm chứng trong skill `use-case-layout`
(`make_drawio.py`), nếu cần tái sử dụng, chép helper vào dự án rồi kiểm tương thích; không giả định file docs/diagrams/usecase_render.py đã tồn tại. Bản cuối vẫn phải do generator Python sinh SVG.

```bash
py -3 docs/diagrams/gen_usecase.py             # svg + png
py -3 docs/diagrams/gen_usecase.py --drawio    # thêm .drawio vào docs/diagrams/drawio/
```

**Luật vẽ tay bắt buộc cho Use Case (chốt 2026-11-01):**

| Luật | Thực thi |
|---|---|
| Một điểm xuất phát duy nhất (khuỷu tay) | `ox,oy = ax, ay - 4` (`ORIGIN_DY = 18` tính từ tâm đầu); không lệch ±12 px |
| **ĐƯỜNG THẲNG, không cung** | `<line>` từ khuỷu tay tới mép ellipse; `CURVE = 0.0`. "Vòng cung" = hình ellipse, không phải dây nối |
| Nhãn «include»/«extend» | nền trắng 68×16 + text, đặt tại trung điểm dây |
| Mũi tên hở | hướng theo dây cung `p0 → p1` |
| Kiểm hình học | `check_fan_arc.py` F1..F5 (1 điểm, phải THẲNG, không cắt đầu/tay/chân) |

Spec use case (toạ độ cứng, lưu tại `docs/diagrams/spec/<ten>.json`):

```json
{
  "title": "Hệ thống Quản lý Rạp chiếu phim",
  "fan": "belly",
  "actors":   [{"id":"USER","label":"Khách hàng (USER)","side":"L","x":190,"y":550}],
  "usecases": [{"id":"UC01","label":"Đăng ký, đăng nhập","x":350,"y":263,"cluster":"Tài khoản"}],
  "associations": [["USER","UC01"]],
  "includes":     [["UC05","UC07"]],
  "extends":      [["UC06","UC05"]]
}
```

- `"fan": "belly"` → quạt chung gốc ở khuỷu tay actor (mặc định, đúng UML).
  (`"fan": "spread"` rải neo dọc thân — chỉ dùng khi được yêu cầu rõ).
- `secondary: true` → UC phụ (chỉ là đích của include/extend).
- **Luật "từ 1 điểm xuất phát + đường thẳng"** được áp dụng cho mọi file spec này;
  `CURVE = 0.0` trong code là mặc định, không ghi đè qua spec.

**Lỗi lịch sử cần tránh:**
- Lỗi cũ: `ox = ax ± 12` — lệch nguồn khỏi khuỷu tay actor → "dây mọc từ cánh" ≠ "quạt từ gốc".
- Lỗi cũ: dùng `<path d="...Q...">` cho association → vi phạm luật "đường thẳng"; **cung Bezier chỉ dùng khi được yêu cầu rõ**.
- Lỗi cũ: xuất phát từ **bụng** actor khiến tia đi LÊN cắt ngang cánh tay (đo được 1 cạnh vi phạm F4) → đổi sang **khuỷu tay** `(ax, ay − 4)`.
- Tự `vendor_usecase_render.py` là CẤM — logic vẽ phải nội tuyến, không phụ thuộc đường dẫn ngoài.

---

## 7. Chạy & kiểm

```bash
py -3 docs/tools/build_all.py             # vẽ lại tất cả + audit
py -3 docs/tools/build_all.py --only erd  # một sơ đồ
py -3 docs/tools/audit_svg.py             # chi tiết lỗi
py -3 docs/tools/check_fan_arc.py         # Use Case: 1 điểm xuất phát + ĐƯỜNG THẲNG (F1..F5)
py -3 docs/tools/selftest_audit_svg.py    # chứng minh bộ kiểm đáng tin
```

---

## 8. Sổ tay lỗi thường gặp

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Ảnh PNG trắng trơn | thiếu `--window-size` | ép `--window-size={W},{H}` |
| Tiếng Việt thành `?` | ghi file không `utf-8` | `write_text(..., encoding="utf-8")` |
| Dây xuyên hộp giữa | đi tâm cột | chuyển sang kênh bên cạnh |
| Nhãn nằm trong lòng hộp khác | đặt nhãn ở trung điểm dây dài | đặt **cạnh kênh**, sát đầu mút |
| Crow's foot bị nghiêng | pháp tuyến tính từ tâm | chọn cạnh gần nhất (mục 4.2) |
| `E3` báo dây cắt nhãn | dây/nhãn dùng chung vùng | dời nhãn hoặc đổi tuyến; không che lỗi bằng halo |
| `E3` **không** báo dù dây cong cắt nhãn | `audit_svg.py` chỉ đọc `M/L/H/V`, bỏ qua `Q`/`C` | mẫu hoá `Q`/`C` thành đoạn thẳng (đã sửa; selftest có ca `BAD_CURVE`) |
| Dây "mọc từ cánh" chứ không từ gốc | nguồn lệch `ox = ax ± 12` | dùng đúng `(ax, ay − 4)` (khuỷu tay) |
| Dây bị vẽ cong dù không ai yêu cầu | render `<path Q>` | dùng `<line>`, `CURVE = 0.0` |
| Tia đi LÊN cắt ngang cánh tay actor | xuất phát từ **bụng** `(ax, ay+10)` | xuất phát ở **khuỷu tay** `(ax, ay−4)`; kiểm `check_fan_arc.py` F4 |
| Mũi tên include/extend lệch khỏi trục dây | hướng lấy theo tiếp tuyến cung | lấy dây cung `p0 → p1` |
| Audit PASS nhưng vẫn xấu | bộ kiểm chỉ đo hình học | nhờ người soi nhịp cuối |

---

## 9. Bài học đã trả giá (đừng lặp lại)

1. **Không được bịa "Proof-of-View".** Nếu model không có vision, ảnh sẽ bị omit khỏi context.
   Mọi câu "tôi thấy nhãn X ở toạ độ Y" khi không thật sự thấy ảnh = **bịa bằng chứng**.
   Đúng phải nói: `Visual QA unavailable — chỉ có kết quả đo tất định; cần người kiểm nhịp cuối`.
2. **Script 0 đỏ ≠ sơ đồ đúng.** Phải có `selftest_audit_svg.py` chứng minh bộ kiểm bắt được lỗi
   (đã từng bỏ sót E3 vì coi nền trắng toàn khung là "nền che nhãn").
3. **Đầu mút sai 1 hộp là lỗi thật.** Đã từng có `seat → bseat` trỏ nhầm sang bảng `Promotion`
   và `combo → bcombo` trỏ nhầm sang `BookingCombo` — mắt 100% không thấy, chỉ lộ khi kiểm toạ độ.
4. **SVG lẫn PNG là nguồn gốc của "sửa nhầm file".** Tách `vectors/` và `images/diagrams/`.
   Tương tự với `.drawio`: để riêng `drawio/`, không thả vào thư mục PNG.
5. **"Từ 1 điểm xuất phát" là luật cứng, không phải mỹ thuật.** Bản cũ lệch `ox = ax ± 12` để né chân actor
   → dây mọc từ cánh tay, sai UML. Đúng: **mọi association hội tụ tại đúng `(ax, ay − 4)`** (khuỷu tay).
6. **"Vòng cung" là hình ellipse, không phải dây nối.** Dây nối actor → use case phải **thẳng** (`<line>`).
   Nếu ai đó bật `CURVE > 0` thì **bộ kiểm phải mẫu hoá cung** — nếu không, E3 mù hoàn toàn với path `Q`.
7. **Đừng vendor rồi để lệch.** Logic use case phải sống ở MỘT nơi (skill `make_drawio.py`) và
   project sao chép y nguyên — có test so sánh byte (`skill==project: True`) trước khi tin.
