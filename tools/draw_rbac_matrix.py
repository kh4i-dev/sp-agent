#!/usr/bin/env python3
"""Ve lai ma tran RBAC khop code (RolesGuard + ownership checks).
Gia tri da doi chieu: connections.service.ts (accept/reject: chi gia su),
reports/tutor-verification controllers (@Roles ADMIN, MODERATOR)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLS = ["Khách", "Người dùng", "Gia sư", "Kiểm duyệt", "Quản trị"]
ROWS = [
    "Xem hồ sơ công khai",
    "Gửi kết nối",
    "Nhận/chấp nhận kết nối",
    "Chat & đánh giá",
    "Duyệt xác minh",
    "Kiểm duyệt báo cáo",
    "Cấu hình hệ thống",
]
VALS = [
    ["x", "x", "x", "x", "x"],
    ["o", "x", "-", "-", "x"],
    ["-", "-", "x", "-", "-"],
    ["o", "x", "x", "x", "x"],
    ["-", "-", "-", "x", "x"],
    ["-", "-", "-", "x", "x"],
    ["-", "-", "-", "-", "x"],
]

fig, ax = plt.subplots(figsize=(11, 5.2))
ax.axis("off")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
nrows, ncols = len(ROWS) + 1, len(COLS) + 1
c0 = 0.30
cw = (0.94 - c0) / (ncols - 1)
rh = 0.92 / nrows
x0, y1 = 0.03, 0.96
widths = [c0] + [cw] * (ncols - 1)
xs = [x0]
for wd in widths:
    xs.append(xs[-1] + wd)
for j, c in enumerate(["Chức năng \\ Vai trò"] + COLS):
    x = xs[j]
    w = widths[j]
    y = y1 - rh
    bold = (j == 0)
    ax.text(x + w / 2, y + rh / 2, c, ha="center", va="center",
            fontsize=12, fontweight="bold" if (bold or j > 0) else "normal")
    ax.add_patch(plt.Rectangle((x, y), w, rh, fill=False, edgecolor="black", lw=1.2))
for i, r in enumerate(ROWS):
    y = y1 - (i + 2) * rh
    ax.text(xs[0] + widths[0] / 2 - 0.0, y + rh / 2, r, ha="center", va="center", fontsize=12)
    ax.add_patch(plt.Rectangle((xs[0], y), widths[0], rh, fill=False, edgecolor="black", lw=1.2))
    for j, v in enumerate(VALS[i]):
        x = xs[j + 1]
        w = widths[j + 1]
        ax.text(x + w / 2, y + rh / 2, "X" if v == "x" else ("O" if v == "o" else "–"),
                ha="center", va="center", fontsize=14,
                fontweight="bold" if v == "x" else "normal")
        ax.add_patch(plt.Rectangle((x, y), w, rh, fill=False, edgecolor="black", lw=1.2))
ax.text(0.5, 0.015, "x: được phép   o: có điều kiện (đăng nhập)   –: không",
        ha="center", va="center", fontsize=11, style="italic")
out = "E:/HOC TAP/my-project/ecosystem_ketnoi_giasu/docs/diagrams/rbac_matrix.png"
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
fig.savefig(out.replace(".png", ".svg"), bbox_inches="tight", facecolor="white")
print("saved", out)
