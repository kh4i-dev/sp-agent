#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_diagrams.py — vẽ lại TẤT CẢ sơ đồ của một project + kiểm định tất định.

Tự dò `docs/diagrams/gen_*.py`, chạy lần lượt, rồi chạy audit_svg.py trên mọi SVG.

Chạy:
  py -3 run_diagrams.py --root <project>
  py -3 run_diagrams.py --root <project> --audit      # chỉ audit
  py -3 run_diagrams.py --root <project> --only erd   # chỉ sơ đồ khớp tên

Mã thoát: 0 = tất cả PASS, 1 = có generator lỗi hoặc audit có lỗi.
"""
from __future__ import annotations

import argparse
import json
import struct
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def find_gen(root: Path) -> list[Path]:
    d = root / "docs" / "diagrams"
    return sorted(p for p in d.glob("gen_*.py") if p.is_file())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="thư mục project (chứa docs/)")
    ap.add_argument("--audit", action="store_true", help="chỉ audit, không vẽ lại")
    ap.add_argument("--only", default=None, help="chỉ chạy generator khớp tên")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    gens = find_gen(root)
    if args.only:
        gens=[g for g in gens if args.only in g.stem]
    if not gens:
        print(f"FAIL: không thấy docs/diagrams/gen_*.py trong {root}", file=sys.stderr)
        return 1

    t0 = time.time()
    failed: list[str] = []
    if not args.audit:
        for g in gens:
            if args.only and args.only not in g.stem:
                continue
            print(f"\n--- {g.name} ---")
            r = subprocess.run([sys.executable, str(g)], cwd=str(root))
            if r.returncode != 0:
                failed.append(g.name)

    vectors=root/'docs/diagrams/vectors'
    files=sorted(vectors.glob('*.svg'))
    if args.only:files=[f for f in files if args.only in f.stem]
    if not files:
        print('FAIL: no matching SVG outputs');return 1
    selected=[]
    for svg in files:
        try:
            png=root/'docs/images/diagrams'/(svg.stem+'.png')
            spec_path=root/'docs/diagrams/spec'/(svg.stem+'.json')
            meta=json.loads(spec_path.read_text(encoding='utf-8'))
            generator=(root/meta['generator']).resolve()
            if not generator.is_relative_to(root) or generator.suffix!='.py' or not generator.is_file():
                raise ValueError('missing/outside-root Python generator')
            if args.only and generator not in gens:
                raise ValueError('selected output does not belong to selected generator')
            if svg.stat().st_size<=500 or png.stat().st_size<=500:
                raise ValueError('SVG/PNG missing or <=500 bytes')
            header=png.read_bytes()[:24]
            if len(header)<24 or header[:8]!=b'\x89PNG\r\n\x1a\n' or header[12:16]!=b'IHDR' or min(struct.unpack('>II',header[16:24]))<=0:
                raise ValueError('invalid PNG header/dimensions')
            if meta['diagram_type'] not in ('usecase','class','erd','box','architecture','bfd','state','activity','sequence','dfd','tree'):
                raise ValueError('unsupported diagram_type')
            selected.append((svg,meta))
        except (KeyError,ValueError,OSError,TypeError) as exc:
            failed.append(f'{svg.name}: {exc}')
    if failed:
        print('FAIL artifact gate:',*failed,sep='\n');return 1
    print("\n=== AUTOMATED GATES (Vision remains separate) ===")
    r = subprocess.run([sys.executable,str(HERE/'selftest_audit_svg.py')],cwd=str(root))
    if r.returncode: return 1
    r = subprocess.run([sys.executable, str(HERE / "audit_svg.py"), *map(str,files)],cwd=str(root))
    if r.returncode: return 1
    from check_fan_arc import check as fan_check
    from verify_box_layout import verify as box_check
    for svg,meta in selected:
        if meta['diagram_type']=='usecase':
            errors,stats=fan_check(svg)
            if not stats['actors'] or not stats['assoc']:
                errors.append('Fan gate NOT RUN: actor/association not recognized; normalize SVG or extend parser')
            failed.extend(f'{svg.name}: {e}' for e in errors)
        if meta['diagram_type'] in ('class','erd','box','architecture','bfd'):
            try:failed.extend(f'{svg.name}: {e}' for e in box_check(meta.get('layout',meta)))
            except (KeyError,ValueError,TypeError,StopIteration):failed.append(f'{svg.name}: missing/invalid box layout spec')

    print(f"\nXong trong {time.time() - t0:.1f}s")
    if failed:
        print(f"GATE FAIL: {failed}")
        return 1
    print('AUTOMATED gates passed. Vision QA NOT RUN by this script; no overall diagram PASS.')
    return 0


if __name__ == "__main__":
    sys.exit(main())
