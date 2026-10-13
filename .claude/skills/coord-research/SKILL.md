---
name: coord-research
description: Điều phối khối NGHIÊN CỨU: nạp nhanh để nghiên cứu chủ đề, tổng hợp, viết literature review, fact-check, so sánh công nghệ, tổng hợp nguồn có dẫn chứng. Gom research-report (báo cáo học thuật), research (gom nguồn, lưu file), research-artifacts (bundle OKF, truy vết). Từ khóa kích hoạt: nghiên cứu, tìm hiểu, tổng hợp tài liệu, literature review, fact-check, so sánh công nghệ, dẫn nguồn, deep research.
---

# coord-research — Điều phối khối Nghiên cứu

> Bản đồ toàn cục: `skill-coordinator`. Baseline chống mâu thuẫn: `docs/rule-conflicts.md`.

## Khi nào nạp

- Nghiên cứu một chủ đề/công nghệ; tổng hợp nguồn; literature review; fact-check.

## Khối gồm

| Skill | Vai trò | Khi nào |
|---|---|---|
| `research-report` | **CHỦ**: quy trình nghiên cứu sâu, báo cáo có dẫn nguồn (≥3 nguồn, IEEE/APA) | báo cáo học thuật |
| `research` | Điều tra nguồn sơ cấp, lưu ghi chú Markdown theo repo | thu thập & lưu |
| `research-artifacts` | Bundle OKF (`docs/research/NNNN-slug.md`), truy vết, mức tin cậy (≥2, NBR 6023) | lưu trữ nội bộ |
| `deep-research` (nếu có) | Pipeline nghiên cứu nhiều agent | nghiên cứu nặng |

## Thứ tự nạp & chuỗi

```text
research-report / deep-research (scope → tìm → tam giác → verify → tổng hợp)
 → [lưu] research (ghi chú) / research-artifacts (bundle OKF)
 → [đưa vào báo cáo] coord-report (docx-report)
```

## Quy ước chung

- **Không bịa nguồn**: chỉ trích URL đã truy cập; nghi ngờ → `UNVERIFIED`.
- Ngưỡng & chuẩn trích dẫn theo ngữ cảnh: báo cáo học thuật ≥3 + IEEE/APA; OKF bundle ≥2 + NBR 6023.

## Anti-patterns

- ❌ Bịa nguồn/số liệu; nâng `PARTIAL`/`NOT_FOUND` thành `DONE`.
- ❌ Trích dẫn không kiểm chứng ở mức trường (DOI/title/author/year).

## Definition of Done

```text
[ ] Mỗi luận điểm có nguồn đã kiểm; mâu thuẫn nêu rõ.
[ ] Chỉ dùng URL đã truy cập; ghi hạn chế.
[ ] Nếu lưu bundle OKF: đúng cấu trúc + truy vết.
```
