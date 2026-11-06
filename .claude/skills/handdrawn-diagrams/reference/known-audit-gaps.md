# Phạm vi bộ kiểm — cập nhật 02/11/2026

Đã sửa và có regression: halo bỏ lọt chữ đè; translate/scale và phần tử vượt khung; NaN trên line; che trắng sai thứ tự vẽ; đoạn chéo xuyên hộp; runner thiếu PNG/spec/nguồn hoặc bỏ cổng fan/box. Chạy `selftest_audit_svg.py` và `test_pipeline.py` để tái kiểm.

Giới hạn còn lại:
- Bbox chữ là ước lượng, không phải đo glyph của trình duyệt; phải soi PNG thật.
- Parser hỗ trợ translate/scale, path tuyệt đối M/L/H/V/Q/C/Z; từ chối rotation, path tương đối, style sheet/use/image/foreignObject và tspan định vị bằng E7. Đây là dialect giới hạn, không phải validator mọi SVG.
- Fan checker nhận mẫu actor circle r=10 và association gần gốc mẫu; nhận diện một phần không chứng minh phủ mọi cạnh. Đối chiếu bảng node/cạnh trong spec và nguồn khi nghiệm thu. Không nhận actor/association được coi NOT RUN và chặn runner.
- Box gate kiểm metadata, SVG gate kiểm hình render; chưa chứng minh hai biểu diễn đồng nhất. Generator phải dùng cùng dữ liệu toạ độ, không viết hai bản layout riêng.
- PNG mới kiểm header và kích thước; cần mở ảnh để phát hiện file hỏng hoặc nội dung sai. `--audit` không chứng minh freshness.
- Chưa đo thẩm mỹ, độ phủ nghiệp vụ, zero-color hoặc cỡ chữ in đầy đủ bằng runner. Các mục đó vẫn thuộc diagram-auditor và Vision QA.

Không nâng kết quả cổng máy thành PASS toàn bộ sơ đồ. Dấu vết audit gốc: `docs/analysis/handdrawn-skill-audit-2026-11-02/`; probes có thể được cập nhật khi chạy lại.
