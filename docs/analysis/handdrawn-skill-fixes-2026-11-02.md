# Sửa skill sơ đồ — 02/11/2026

Đã sửa audit_svg: chữ đè dù có halo, transform translate/scale, phần tử vượt khung, NaN, thứ tự vẽ nền/line và từ chối cấu trúc chưa hỗ trợ bằng E7. Box checker bắt dây chéo xuyên hộp. Fan checker dùng tay của đúng actor và báo actor không có association.

Runner kiểm nguồn Python + spec + SVG/PNG tương ứng, kích thước file và header PNG; chạy selftest, SVG gate, fan/box theo diagram_type. Không nhận diện Use Case là NOT RUN, không PASS. Thành công chỉ là cổng máy; Vision QA riêng.

Hướng dẫn bỏ lưới 5 cột bắt buộc, bỏ halo bắt buộc, phân biệt mũi tên chéo với ký hiệu cạnh hộp, thống nhất junction thân–tay và hợp đồng thư mục. Các coordinator có khối ưu tiên hiện hành để không chọn công cụ nháp làm bản nộp.

Kiểm chứng: test_pipeline.py 9/9; selftest E1..E6, đường cong và 12 regression (11 SVG + diagonal box); tools/check_handdrawn_skill.py bắt lại 5/5 ca audit.

Giới hạn: bbox chữ ước lượng, fan parser theo mẫu r=10, chưa chứng minh spec/SVG đồng nhất, PNG chỉ kiểm header; nghiệp vụ/thẩm mỹ vẫn cần nguồn và ảnh thật. Đợt này sửa skill và bộ kiểm, chưa vẽ lại hoặc duyệt lại ảnh btl-cnpm.

Cấu trúc: 45 frontmatter hợp lệ; các skill sơ đồ không quá 500 dòng; hash hai mirror của các skill đã sửa trùng nhau. Cảnh báo ngoài phạm vi: docx-report/SKILL.md hiện 714 dòng.
