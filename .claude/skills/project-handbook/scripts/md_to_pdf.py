#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""md_to_pdf.py — Markdown -> PDF "sach huong dan" (A4, tieng Viet, co muc luc + so trang).

Dung cho skill `project-handbook`: bien file huong dan .md thanh PDF de gui cho nguoi doc.
Chuoi xu ly:  .md  ->  .html (CSS in an A4)  ->  .pdf  (Chrome headless qua CDP)

Vi sao khong dung pandoc/wkhtmltopdf:
  - Font tieng Viet va bang bieu on dinh hon khi render bang Chrome.
  - Dat duoc CHAN TRANG co "Trang n/ N" dong (pandoc HTML khong lam duoc).

CACH DUNG:
  python md_to_pdf.py <file.md> [more.md ...] --out <file.pdf|thu_muc>
  python md_to_pdf.py docs/ --out dist/            # ca thu muc: moi .md 1 PDF

TUY CHON:
  --out PATH        file .pdf dich, hoac thu muc (mac dinh: canh file .md)
  --title T         tieu de bia (mac dinh lay tu front-matter hoac H1 dau tien)
  --subtitle T      phu de tren bia
  --author T        tac gia  --date T   ngay
  --no-cover        khong sinh trang bia
  --no-toc          khong sinh muc luc
  --toc-depth N     do sau muc luc (mac dinh 3)
  --font T          font chu (mac dinh "Segoe UI"; dung "Times New Roman" cho bao cao hoc thuat)
  --size N          co chu than bai pt (mac dinh 11)
  --margin-mm a,b,c,d   le tren,phai,duoi,trai (mm) — mac dinh 18,16,18,16
  --landscape       kho ngang
  --header T        dong chay tren dau trang
  --keep-html       giu lai file .html trung gian de soi
  --chrome PATH     duong dan Chrome/Edge

YEU CAU: `pip install markdown` ; Node >= 20 ; Chrome/Edge co san.
"""

from __future__ import annotations

import argparse
import html as html_mod
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

try:
    import markdown as md_lib
except ImportError:
    print("[md_to_pdf] Thieu thu vien 'markdown'. Cai: pip install markdown", file=sys.stderr)
    sys.exit(2)

HERE = Path(__file__).resolve().parent
NODE_HELPER = HERE / "html_to_pdf.mjs"

# KHONG dung "codehilite": no sinh mau inline cho token code (xanh la #008000,
# do #BA2121...) -> vi pham luat "khong dung chu mau". Chi giu `fenced_code`
# roi to nen xam bang CSS (nen = highlight thi duoc phep).
MD_EXTENSIONS = [
    "tables", "fenced_code", "toc", "attr_list",
    "sane_lists", "def_list", "md_in_html", "footnotes", "admonition", "nl2br",
]
MD_EXT_CONFIG = {
    "toc": {"permalink": False, "toc_depth": "2-3"},
}


# ----------------------------------------------------------------------------- helpers
def parse_front_matter(text: str):
    """Front-matter YAML don gian: --- \n key: value \n --- . Tra (meta, body)."""
    meta: dict[str, str] = {}
    if text.lstrip().startswith("---"):
        lines = text.lstrip().splitlines()
        if lines and lines[0].strip() == "---":
            for i, ln in enumerate(lines[1:], 1):
                if ln.strip() == "---":
                    return meta, "\n".join(lines[i + 1:])
                m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", ln)
                if m:
                    val = m.group(2).strip().strip('"').strip("'")
                    meta[m.group(1).lower()] = val
    return meta, text


def first_h1(body: str) -> str | None:
    for ln in body.splitlines():
        m = re.match(r"^#\s+(.+)$", ln.strip())
        if m:
            return m.group(1).strip()
    return None


def absolutize_assets(html: str, base_dir: Path) -> str:
    """Doi src/href tuong doi -> file:// tuyet doi de Chrome doc duoc anh."""
    def repl(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r"^(https?:|data:|file:|#|mailto:)", val, re.I):
            return m.group(0)
        p = (base_dir / val).resolve()
        return f'{attr}="{p.as_uri()}"'
    return re.sub(r'\b(src|href)="([^"]+)"', repl, html)


def emphas_label(html: str) -> str:
    """Danh dau lai nhan <<include>> / <<extend>> thanh the dep (giu nguyen chu)."""
    return re.sub(r"«([^»]+)»", r'<span class="guillemet">«\1»</span>', html)


def apply_highlight(html: str) -> str:
    """`==chu==` -> <mark>chu</mark> (HIGHLIGHT — cach nhan manh DUY NHAT duoc phep).

    - Bo qua moi khoi <pre>...</pre> de khong pha code / so do ASCII.
    - Cho phep `==...==` trai qua NHIEU DONG (nhan trong blockquote hay bi wrap),
      nhung KHONG trai qua dong trong (tranh "nuot" ca tai lieu neu thieu dau dong).
    - Sau khi chuyen, neu con sot `==` ngoai khoi <pre> thi CANH BAO (de khong
      am tham in ra dau `==` trong PDF).
    """
    parts = re.split(r"(<pre\b.*?</pre>)", html, flags=re.S | re.I)
    leftover = 0
    for i, seg in enumerate(parts):
        if seg.lower().startswith("<pre"):
            continue
        seg = re.sub(r"==((?:[^=\n]|\n(?!\s*\n))+?)==", r"<mark>\1</mark>", seg)
        # `===` / `==` con lai (vd toan tu JS) -> chi dem, khong chuyen
        leftover += len(re.findall(r"(?<!=)==(?!=)", seg))
        parts[i] = seg
    if leftover:
        print(f"[md_to_pdf] CANH BAO: con {leftover} dau '==' chua chuyen thanh <mark> "
              f"(thuong do ==..== trai qua DONG TRONG, hoac sot 1 dau ==). "
              f"Kiem lai markdown keo PDF in ra dau '=='.",
              file=sys.stderr)
    return "".join(parts)


# ----------------------------------------------------------------------------- CSS
def css(font: str, size: float, landscape: bool) -> str:
    """CSS in an A4 — LUAT CUNG: **KHONG CHU MAU**, chi DEN/XAM + HIGHLIGHT (nen xam).

    Vi sao: dong bo voi luat cua khoi tai lieu (`docx-report`): tai lieu hoc thuat /
    tai lieu ky thuat dung chu den; nhan manh bang **highlight** chu khong bang mau chu.
    Moi token mau o day deu la XAM (R=G=B). Kiem bang:
        python scripts/check_pdf_monochrome.py <out.pdf>   # phai bao SACH
    """
    page_size = "A4 landscape" if landscape else "A4"
    return f"""
@page {{ size: {page_size}; }}
:root {{
  /* TAT CA deu la xam trung tinh (R=G=B). Khong co mau "accent". */
  --ink: #000000; --muted: #555555; --rule: #cccccc;
  /* THANG DO XAM: trang > blockquote(#f7) > hang chan(#f2) > HIGHLIGHT(#d9).
     Phai cach nhau du xa de HIGHLIGHT nam trong blockquote VAN NHIN THAY. */
  --hl: #d9d9d9;      /* nen HIGHLIGHT — cach nhan manh duy nhat duoc phep */
  --quote-bg: #f7f7f7;
  --hl2: #f2f2f2;     /* nen hang tieu de bang / hang chan */
  --code-bg: #f0f0f0;
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{
  font-family: "{font}", "Segoe UI", "Noto Sans", "DejaVu Sans", Arial, sans-serif;
  font-size: {size}pt; line-height: 1.55; color: var(--ink);
  margin: 0; padding: 0; text-align: left;
}}
/* Tieu de: PHAN BIET bang CO CHU + DO DAM + duong ke, KHONG bang mau chu. */
h1, h2, h3, h4, h5, h6 {{ font-family: "{font}", "Segoe UI", Arial, sans-serif; color: var(--ink);
  line-height: 1.25; margin: 0 0 0.5em; page-break-after: avoid; }}
h1 {{ font-size: {size * 1.75:.1f}pt; font-weight: 700; border-bottom: 2px solid var(--ink);
  padding-bottom: .25em; margin-top: .6em; }}
h2 {{ font-size: {size * 1.38:.1f}pt; font-weight: 700; margin-top: 1.4em;
  border-bottom: 1px solid var(--rule); padding-bottom: .12em; }}
h3 {{ font-size: {size * 1.18:.1f}pt; font-weight: 700; margin-top: 1.15em; }}
h4 {{ font-size: {size * 1.04:.1f}pt; font-weight: 700; margin-top: 1em; }}
h2, h3 {{ page-break-after: avoid; }}
p {{ margin: 0 0 .62em; }}
/* Lien ket: nhan ra bang GACH CHAN, khong bang mau. */
a {{ color: inherit; text-decoration: underline; text-decoration-thickness: .5pt;
  text-underline-offset: .12em; }}
strong {{ font-weight: 700; color: inherit; }}
hr {{ border: 0; border-top: 1px solid var(--rule); margin: 1.2em 0; }}

ul, ol {{ margin: 0 0 .7em; padding-left: 1.35em; }}
li {{ margin: .18em 0; }}
li > ul, li > ol {{ margin: .2em 0 .3em; }}

/* HIGHLIGHT = co che nhan manh DUY NHAT duoc phep (ngoai dam/nghieng). */
mark {{ background: var(--hl); color: inherit; padding: 0 .14em; }}
/* Trong blockquote nen da xam, vien them 1 net mong cho highlight khoi "chin vao nen". */
blockquote mark {{ box-shadow: 0 0 0 1px #bdbdbd; }}

blockquote {{
  margin: .7em 0; padding: .5em .8em; border-left: 3px solid var(--ink);
  background: var(--quote-bg); color: inherit; page-break-inside: avoid;
}}
blockquote p:last-child {{ margin-bottom: 0; }}

code {{ font-family: "Cascadia Mono", Consolas, "DejaVu Sans Mono", monospace;
  font-size: {size * 0.88:.1f}pt; background: var(--code-bg); padding: .08em .32em; border-radius: 3px; }}
pre {{ background: var(--code-bg); border: 1px solid var(--rule); border-radius: 5px;
  padding: .6em .75em; overflow-wrap: anywhere; white-space: pre-wrap;
  font-size: {size * 0.85:.1f}pt; line-height: 1.42; page-break-inside: avoid; }}
pre code {{ background: none; padding: 0; font-size: inherit; }}
/* Khoi ```text thuong la so do ASCII -> giam co chu de it bi wrap lam lech hinh */
pre:has(> code.language-text) {{ font-size: {size * 0.74:.1f}pt; line-height: 1.3; }}

table {{ border-collapse: collapse; width: 100%; margin: .6em 0 1em;
  font-size: {size * 0.9:.1f}pt; page-break-inside: auto; }}
thead {{ background: var(--hl2); display: table-header-group; }}
th, td {{ border: 1px solid var(--rule); padding: .34em .5em; text-align: left; vertical-align: top; }}
th {{ font-weight: 700; color: inherit; }}
tr {{ page-break-inside: avoid; }}
tbody tr:nth-child(even) {{ background: #fafafa; }}

img {{ max-width: 100%; height: auto; }}
img + em, p > em:only-child {{ color: var(--muted); }}

.guillemet {{ font-weight: 600; color: inherit; white-space: nowrap; }}

/* ---------- bia ---------- */
.cover {{ page-break-after: always; height: 92vh; display: flex; flex-direction: column;
  justify-content: center; text-align: center; padding: 0 8mm; }}
.cover .kicker {{ letter-spacing: .18em; text-transform: uppercase; font-size: {size * 0.82:.1f}pt;
  color: var(--muted); margin-bottom: 1.2em; }}
.cover h1 {{ border: 0; font-size: {size * 2.5:.1f}pt; margin: 0 0 .35em; line-height: 1.15; }}
.cover .subtitle {{ font-size: {size * 1.2:.1f}pt; color: var(--muted); margin-bottom: 2em; }}
.cover .meta {{ font-size: {size * 0.95:.1f}pt; color: var(--muted); line-height: 1.9; }}
.cover .rule {{ width: 42mm; height: 3px; background: var(--ink); margin: 1.6em auto; }}

/* ---------- muc luc ---------- */
.toc {{ page-break-after: always; }}
.toc h1 {{ border-bottom: 2px solid var(--ink); }}
.toc ul {{ list-style: none; padding-left: 0; font-size: {size * 0.98:.1f}pt; }}
.toc > ul > li {{ margin: .3em 0; font-weight: 600; }}
.toc ul ul {{ list-style: none; padding-left: 1.2em; font-weight: 400; color: var(--muted);
  font-size: {size * 0.92:.1f}pt; }}
.toc a {{ color: inherit; text-decoration: none; }}

/* ---------- trang cuoi ---------- */
.endnote {{ margin-top: 2em; padding-top: .8em; border-top: 1px solid var(--rule);
  font-size: {size * 0.85:.1f}pt; color: var(--muted); }}
"""


HTML_SHELL = """<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8">
<title>{title}</title>
<style>{css}</style>
</head><body>
{cover}
{toc}
<main>{body}</main>
{endnote}
</body></html>
"""


def build_html(md_text: str, base_dir: Path, opts) -> tuple[str, str]:
    meta, body = parse_front_matter(md_text)
    title = opts.title or meta.get("title") or first_h1(body) or Path(opts.src_name).stem
    subtitle = opts.subtitle or meta.get("subtitle", "")
    author = opts.author or meta.get("author", "")
    date = opts.date or meta.get("date", "")

    md = md_lib.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_EXT_CONFIG)
    html_body = md.convert(body)
    html_body = absolutize_assets(html_body, base_dir)
    html_body = emphas_label(html_body)
    html_body = apply_highlight(html_body)

    # --- Muc luc ---
    toc_html = ""
    if not opts.no_toc:
        md_toc = md_lib.Markdown(extensions=["toc"], extension_configs={
            "toc": {"permalink": False, "toc_depth": f"2-{opts.toc_depth}"}})
        md_toc.convert(body)
        toc = md_toc.toc
        if toc.strip():
            toc_html = f'<nav class="toc"><h1>Mục lục</h1>{toc}</nav>'

    # --- Bia ---
    cover_html = ""
    if not opts.no_cover:
        meta_lines = "".join(f"<div>{html_mod.escape(x)}</div>" for x in (author, date) if x)
        cover_html = (
            '<section class="cover">'
            f'<div class="kicker">{html_mod.escape(opts.kicker)}</div>'
            f"<h1>{html_mod.escape(title)}</h1>"
            + (f'<div class="subtitle">{html_mod.escape(subtitle)}</div>' if subtitle else "")
            + '<div class="rule"></div>'
            + (f'<div class="meta">{meta_lines}</div>' if meta_lines else "")
            + "</section>"
        )

    from datetime import date as _d
    endnote = (
        '<div class="endnote">Tài liệu được sinh tự động từ mã nguồn và tài liệu gốc của dự án. '
        f'Bản in: {_d.today().strftime("%d/%m/%Y")}.</div>'
    )
    html_doc = HTML_SHELL.format(
        title=html_mod.escape(title), css=css(opts.font, opts.size, opts.landscape),
        cover=cover_html, toc=toc_html, body=html_body, endnote=endnote,
    )
    return title, html_doc


def render_pdf(html_path: Path, pdf_path: Path, opts, title: str):
    node = "node"
    cmd = [node, str(NODE_HELPER), "--in", str(html_path), "--out", str(pdf_path),
           "--title", title, "--margin-mm", opts.margin_mm,
           "--footer-left", opts.footer_left or title]
    if opts.landscape:
        cmd.append("--landscape")
    if opts.header:
        cmd += ["--header", opts.header]
    if opts.chrome:
        cmd += ["--chrome", opts.chrome]
    if opts.wait_ms:
        cmd += ["--wait-ms", str(opts.wait_ms)]
    env = dict(os.environ)
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if res.returncode != 0:
        print(res.stdout.strip(), file=sys.stderr)
        print(res.stderr.strip(), file=sys.stderr)
        return False
    print(res.stdout.strip())

    # TU KIEM LUAT "KHONG CHU MAU" ngay sau khi xuat: khong the quen buoc nay.
    checker = HERE / "check_pdf_monochrome.py"
    if checker.exists():
        chk = subprocess.run([sys.executable, str(checker), str(pdf_path)],
                             capture_output=True, text=True)
        out = (chk.stdout or "").strip()
        if out:
            print(out)
        if chk.returncode != 0:
            print("[md_to_pdf] CANH BAO: PDF CON CHU MAU — luat la chi den/xam + highlight. "
                  "Xem bang mau o tren roi sua CSS/markdown.", file=sys.stderr)
    return True


def collect_md(paths) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            out.extend(sorted(q for q in p.rglob("*.md") if "_build" not in q.parts))
        elif p.suffix.lower() in (".md", ".markdown"):
            out.append(p)
        else:
            print(f"[md_to_pdf] Bo qua (khong phai .md): {p}", file=sys.stderr)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Markdown -> PDF (A4, tieng Viet, muc luc, so trang).")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", default=None)
    ap.add_argument("--title"); ap.add_argument("--subtitle")
    ap.add_argument("--author"); ap.add_argument("--date")
    ap.add_argument("--kicker", default="Hướng dẫn dự án")
    ap.add_argument("--no-cover", action="store_true")
    ap.add_argument("--no-toc", action="store_true")
    ap.add_argument("--toc-depth", type=int, default=3)
    ap.add_argument("--font", default="Segoe UI")
    ap.add_argument("--size", type=float, default=11.0)
    ap.add_argument("--margin-mm", default="18,16,18,16")
    ap.add_argument("--footer-left", default=None)
    ap.add_argument("--header", default=None)
    ap.add_argument("--landscape", action="store_true")
    ap.add_argument("--keep-html", action="store_true")
    ap.add_argument("--wait-ms", type=int, default=700)
    ap.add_argument("--chrome", default=None)
    opts = ap.parse_args(argv)

    files = collect_md(opts.paths)
    if not files:
        print("[md_to_pdf] Khong co file .md nao.", file=sys.stderr)
        return 2
    if not NODE_HELPER.exists():
        print(f"[md_to_pdf] Khong thay helper: {NODE_HELPER}", file=sys.stderr)
        return 2

    out_arg = Path(opts.out) if opts.out else None
    multi = len(files) > 1
    if out_arg and out_arg.is_dir() is False and multi:
        print("[md_to_pdf] Nhieu file .md nhung --out la 1 file; se ghi vao thu muc cha.", file=sys.stderr)
    if out_arg and not multi and (out_arg.suffix.lower() == ".pdf"):
        out_dir = out_arg.parent or Path(".")
        out_name = out_arg.name
    else:
        out_dir = out_arg or None

    ok = 0
    for f in files:
        base_dir = f.parent
        opts.src_name = f.name
        title, html_doc = build_html(f.read_text(encoding="utf-8"), base_dir, opts)
        target_dir = out_dir or base_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        build_dir = target_dir / "_build"
        build_dir.mkdir(exist_ok=True)
        html_path = build_dir / (f.stem + ".html")
        html_path.write_text(html_doc, encoding="utf-8")
        pdf_path = (target_dir / out_name) if (out_arg and not multi and out_arg.suffix.lower() == ".pdf") \
            else (target_dir / (f.stem + ".pdf"))
        print(f"== {f.name} -> {pdf_path}")
        if render_pdf(html_path, pdf_path, opts, title):
            ok += 1
        if not opts.keep_html:
            try:
                html_path.unlink()
            except OSError:
                pass
    print(f"[md_to_pdf] Xong {ok}/{len(files)} file.")
    return 0 if ok == len(files) else 1


if __name__ == "__main__":
    sys.exit(main())
