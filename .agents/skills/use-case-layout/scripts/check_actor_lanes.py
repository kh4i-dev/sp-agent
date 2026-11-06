#!/usr/bin/env python3
"""Gate truoc khi ve Use Case: khoa actor TRAI/PHAI tu bang layout.

Doc file Markdown chua bang layout (skill use-case-layout, Buoc 2.2),
tim bang co cot `side`/`lane`, bat moi hang `kind=actor` phai co side L/R.

Quy uoc bang layout (bat buoc):
  | element_id | label | kind (actor/usecase) | group | side/lane | row | ... |
  - kind = actor  -> side chi nhan L (trai) hoac R (phai)
  - kind = usecase -> side thuoc C-L / C-R / C (khong kiem c ung, chi canh bao)

Usage:
  python check_actor_lanes.py <layout-md>...

Exit code:
  0 = PASS (duoc phep ve), 1 = FAIL (dung, sua bang truoc khi ve),
  2 = khong tim thay bang layout hop le trong file.
"""

import re
import sys

ACTOR_SIDES = {
    "l": "L", "left": "L", "trai": "L", "trái": "L", "lane l": "L",
    "r": "R", "right": "R", "phai": "R", "phải": "R", "lane r": "R",
}
UC_SIDES = {"c-l", "c-r", "c", "cl", "cr", "center", "giữa", "giua"}


def norm(cell):
    c = (cell or "").strip().lower()
    c = re.sub(r"\*|`|_", "", c)
    return " ".join(c.split())


def split_row(line):
    parts = line.strip().strip("|").split("|")
    return [p.strip() for p in parts]


def find_tables(text):
    """Tra ve list (header_cells, data_rows) cho moi bang Markdown."""
    tables = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines):
            sep = lines[i + 1].strip()
            if re.match(r"^\|?[\s:\-|]+\|?$", sep) and "-" in sep:
                header = split_row(lines[i])
                rows = []
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|"):
                    rows.append(split_row(lines[j]))
                    j += 1
                tables.append((header, rows))
                i = j
                continue
        i += 1
    return tables


def col_index(header, *keys):
    for idx, h in enumerate(header):
        hn = norm(h)
        if any(k in hn for k in keys):
            return idx
    return -1


def check_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        return 2, ["Khong doc duoc file '{}': {}".format(path, e)]

    layout_tables = []
    for header, rows in find_tables(text):
        if col_index(header, "side", "lane") >= 0:
            layout_tables.append((header, rows))
    if not layout_tables:
        return 2, [
            "Khong tim thay bang layout (bang co cot `side`/`lane`) trong '{}'.".format(path),
            "Hay tao bang layout theo skill use-case-layout Buoc 2.2 truoc khi ve.",
        ]

    errors, warnings = [], []
    total_actors = 0
    for header, rows in layout_tables:
        i_kind = col_index(header, "kind", "type", "loai", "loại")
        i_side = col_index(header, "side", "lane")
        i_id = col_index(header, "element")
        if i_id < 0:
            i_id = col_index(header, "id")
        if i_kind < 0 or i_side < 0:
            errors.append(
                "Bang layout thieu cot bat buoc: can co `kind` (actor/usecase) "
                "va `side`/`lane`. Header hien tai: {}".format(" | ".join(header))
            )
            continue
        seen = set()
        for r in rows:
            eid = r[i_id] if i_id >= 0 and i_id < len(r) else "?"
            if eid in seen:
                errors.append("Trung element_id '{}'.".format(eid))
            seen.add(eid)
            kind = norm(r[i_kind]) if i_kind < len(r) else ""
            side = norm(r[i_side]) if i_side < len(r) else ""
            if "actor" in kind:
                total_actors += 1
                if side in ACTOR_SIDES:
                    continue
                errors.append(
                    "Actor '{}' co side='{}' -> VI PHAM khoa TRAI/PHAI. "
                    "Chi chap nhan L (trai) hoac R (phai). "
                    "Khong xep duoc thi quay lai Buoc 0/1, cam nhet vao giua.".format(
                        eid, r[i_side] if i_side < len(r) else ""
                    )
                )
            elif "usecase" in kind or "use case" in kind or "uc" == kind:
                if side not in UC_SIDES and side not in ("c-l", "c-r", "c"):
                    warnings.append(
                        "Use case '{}' co side='{}' la (mong doi C-L/C-R/C).".format(eid, side)
                    )
    if total_actors == 0:
        warnings.append("Khong thay hang kind=actor nao — so do Use Case thieu actor?")

    if errors:
        return 1, errors + ["[FAIL] {} loi. Dung, sua bang layout truoc khi ve.".format(len(errors))]
    head = ["[PASS] {} actor dung khoa TRAI/PHAI.".format(total_actors)]
    return 0, head + (["Canh bao:"] + warnings if warnings else [])


def main(argv):
    if len(argv) < 2:
        print("Usage: python check_actor_lanes.py <layout-md>...", file=sys.stderr)
        return 2
    worst = 0
    for path in argv[1:]:
        code, msgs = check_file(path)
        worst = max(worst, code)
        print("== {} ==".format(path))
        for m in msgs:
            print(("  " if code == 0 else "  ! ") + m)
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
