#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selftest_audit_svg.py — chứng minh audit_svg.py THẬT SỰ bắt được lỗi.

Tạo SVG hỏng có chủ đích (đè nhãn, dây xuyên chữ, chữ tràn khung, text rỗng,
id trùng) rồi chạy bộ kiểm. Nếu bộ kiểm không bắt đủ => script kiểm là ĐỒ GIẢ.

Chạy: py -3 docs/tools/selftest_audit_svg.py
Mã thoát: 0 = bộ kiểm đáng tin, 1 = bộ kiểm hỏng (false PASS).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE / "audit_svg.py"

REGRESSIONS = {
    'halo_overlap': ('<text x="20" y="60" paint-order="stroke" stroke="white">SAME LABEL</text><text x="20" y="60" paint-order="stroke" stroke="white">SAME LABEL</text>', 'E2'),
    'translated_outside': ('<g transform="translate(500 0)"><text x="20" y="60">OUTSIDE</text></g>', 'E1'),
    'nan_line': ('<text x="20" y="60">OK</text><line x1="NaN" y1="100" x2="200" y2="100" stroke="black"/>', 'E6'),
    'late_line': ('<rect x="10" y="30" width="160" height="50" fill="white"/><text x="20" y="60" font-size="20">LABEL</text><line x1="0" y1="55" x2="300" y2="55" stroke="black"/>','E3'),
    'outside_shape': ('<text x="20" y="60">OK</text><rect x="390" y="200" width="100" height="50" stroke="black" fill="none"/>','E1'),
    'late_line_halo': ('<text x="20" y="60" font-size="20" paint-order="stroke" stroke="white">LABEL</text><line x1="0" y1="55" x2="300" y2="55" stroke="black"/>','E3'),
    'relative_path': ('<text x="20" y="60">OK</text><path d="m 20 100 l 100 0" stroke="black"/>','E7'),
    'unsupported_rotation': ('<g transform="rotate(45)"><text x="20" y="60">OK</text></g>','E7'),
    'black_halo': ('<line x1="0" y1="55" x2="300" y2="55" stroke="black"/><text x="20" y="60" font-size="20" paint-order="stroke" stroke="black">LABEL</text>','E3'),
    'clean_white_halo': ('<line x1="0" y1="55" x2="300" y2="55" stroke="black"/><text x="20" y="60" font-size="20" paint-order="stroke" stroke="white" stroke-width="3">LABEL</text>',None),
    'clean_background': ('<line x1="0" y1="55" x2="300" y2="55" stroke="black"/><rect x="10" y="30" width="160" height="50" fill="white"/><text x="20" y="60" font-size="20">LABEL</text>',None),
}

BAD = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
<rect width="400" height="300" fill="#fff"/>
<rect x="40" y="40" width="120" height="60" fill="#fff" stroke="#000"/>
<!-- E2: hai nhãn đè nhau -->
<text x="50" y="70" font-size="14">Chong chu A</text>
<text x="52" y="72" font-size="14">Chong chu B</text>
<!-- E3: dây cắt xuyên nhãn (sau khi đã có nhãn ở trên) -->
<line x1="0" y1="71" x2="400" y2="71" stroke="#000"/>
<!-- E4: chữ tràn ngang khỏi hộp 40..160 -->
<text x="45" y="95" font-size="20">Chu rat dai tran ra ngoai hop nay</text>
<!-- E1: chữ ra ngoài khung -->
<text x="380" y="290" font-size="14">Ngoai khung ben phai day</text>
<!-- E6: text rỗng -->
<text x="10" y="200" font-size="12"></text>
<!-- E5: id trùng -->
<rect id="dup" x="10" y="220" width="10" height="10" stroke="#000" fill="none"/>
<rect id="dup" x="30" y="220" width="10" height="10" stroke="#000" fill="none"/>
</svg>
"""

GOOD = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
<rect width="400" height="300" fill="#fff"/>
<rect x="40" y="40" width="200" height="60" fill="#fff" stroke="#000"/>
<text x="50" y="70" font-size="14">Nhan sach se</text>
<line x1="10" y1="200" x2="390" y2="200" stroke="#000"/>
</svg>
"""

BAD_CURVE = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
<rect width="400" height="300" fill="#fff"/>
<text x="150" y="165" font-size="14">Chu nam tren cung</text>
<path d="M 0 60 Q 200 260 400 60" stroke="#000" fill="none"/>
</svg>
"""


def run(path: Path) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(AUDIT), str(path)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main() -> int:
    regressions_ok=True
    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "bad.svg"
        good = Path(td) / "good.svg"
        curve = Path(td) / "bad_curve.svg"
        bad.write_text(BAD, encoding="utf-8")
        good.write_text(GOOD, encoding="utf-8")
        curve.write_text(BAD_CURVE, encoding="utf-8")

        code_bad, out_bad = run(bad)
        code_good, out_good = run(good)
        code_curve, out_curve = run(curve)
        for name,(body,expected) in REGRESSIONS.items():
            p=Path(td)/(name+'.svg')
            p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">'+body+'</svg>',encoding='utf-8')
            code,out=run(p)
            matched=(code!=0 and f' {expected}:' in out) if expected else code==0
            regressions_ok=regressions_ok and matched
            print(f'Regression {name}: {"OK" if matched else "FAIL"}')

    from verify_box_layout import verify
    diagonal=dict(canvas=dict(width=500,height=250),grid=dict(box_width=100,col_left=[0,150,300],head_height=40,line_height=20),entities=[dict(id=k,col=i,top=50,fields=['id','x','y']) for i,k in enumerate(['a','b','c'])],relationships=[dict(id='edge',a='a',b='c',points=[[100,80],[300,120]])])
    diagonal_ok=any('[E4]' in e for e in verify(diagonal))
    print('Regression diagonal_box:', 'OK' if diagonal_ok else 'FAIL')

    expected = {"E1", "E2", "E3", "E4", "E5", "E6"}
    found = {c for c in expected if f" {c}:" in out_bad}
    missing = expected - found

    print("=== SVG HỎNG (phải FAIL) ===")
    print(f"  exit={code_bad}  (mong đợi != 0)")
    print(f"  bắt được: {sorted(found)}")
    if missing:
        print(f"  BỎ SÓT : {sorted(missing)}")
    print("\n=== SVG SẠCH (phải PASS) ===")
    print(f"  exit={code_good}  (mong đợi 0)")
    print("\n=== ĐƯỜNG CONG Q cắt nhãn (phải bắt E3) ===")
    print(f"  exit={code_curve}  (mong đợi != 0)  |  E3 {'CÓ' if ' E3:' in out_curve else 'KHÔNG'}")

    ok = (code_bad != 0) and not missing and (code_good == 0) \
         and (code_curve != 0) and (" E3:" in out_curve) and regressions_ok and diagonal_ok
    print("\n" + ("KẾT LUẬN: các fixture và regression đã đạt; không thay Vision QA hoặc chứng minh mọi SVG được hỗ trợ"
                  if ok else "KẾT LUẬN: BỘ KIỂM HỎNG — không được dùng để PASS"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
