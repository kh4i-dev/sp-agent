---
name: research-report
description: Quy trình nghiên cứu sâu (deep research) có kiểm chứng nguồn: lập phạm vi, tìm kiếm song song, tổng hợp, xác minh trích dẫn, chống bịa nguồn, viết báo cáo có dẫn nguồn. Dùng khi người dùng yêu cầu nghiên cứu, tìm hiểu chủ đề, tổng hợp tài liệu, viết literature review, fact-check, so sánh công nghệ, hoặc cần dẫn nguồn đáng tin cậy.
---

# Research Report Skill — Nghiên cứu có kiểm chứng

Mục tiêu: báo cáo nghiên cứu **có dẫn nguồn thật**, phân biệt rõ sự thật / suy luận / chưa xác minh.
Nguyên tắc tối thượng: **KHÔNG bịa nguồn** — chỉ trích dẫn URL đã thực sự truy cập.

> **Phạm vi & đồng bộ (Scope):** skill này tạo **báo cáo nghiên cứu học thuật** — dùng ngưỡng **≥ 3 nguồn độc lập** và trích dẫn **IEEE/APA** (khớp `docx-report`). Khi cần lưu thành **bundle OKF nội bộ** (`docs/research/NNNN-slug.md`, frontmatter `type`, chuẩn NBR 6023, ngưỡng ≥2), dùng `research-artifacts` — hai skill bổ trợ theo ngữ cảnh, không mâu thuẫn.

## Khi nào dùng

- Nghiên cứu một chủ đề/công nghệ trước khi làm đồ án.
- Tổng hợp literature review, so sánh giải pháp.
- Fact-check một khẳng định, cần nguồn sơ cấp.
- Thu thập bằng chứng cho báo cáo PTTKHT.

## Pipeline 8 pha

```text
1. SCOPE   → làm rõ câu hỏi, phạm vi, tiêu chí thành công
2. PLAN    → chia thành các sub-question, chọn nguồn cần tìm
3. RETRIEVE→ tìm song song (subagent), thu thập URL + trích đoạn
4. TRIANGULATE → mỗi luận điểm đối chiếu ≥ 3 nguồn độc lập
5. VERIFY  → xác minh trích dẫn ở mức trường (DOI/title/author/year/venue)
6. SYNTHESIZE → dàn ý → báo cáo, mâu thuẫn được nêu rõ
7. CRITIQUE→ tự phản biện: thiên lệch nguồn, bằng chứng yếu, khoảng trống
8. PACKAGE → báo cáo cuối + bảng nguồn + ghi chú hạn chế
```

Nếu câu hỏi mơ hồ: hỏi lại 1–2 câu trước khi tìm (Scope là bắt buộc).

## Tìm kiếm song song bằng subagent

- Tách chủ đề thành 3–5 sub-question độc lập.
- Mỗi subagent: nhận 1 sub-question + danh sách nguồn ưu tiên, trả về **URL thật + trích đoạn + ngày**.
- Lead tổng hợp, phát hiện mâu thuẫn, quyết định vòng tìm tiếp.
- Luôn **tìm rộng trước, hẹp sau**; nhiều tool call song song khi có thể.

## Nguồn & công cụ

| Loại | Nguồn/tool |
|---|---|
| Web search neural | Exa (`exa.ai`, category `publication`) |
| Web search + crawl | Tavily (`/search`, `/extract`, `/crawl`, `/research`) |
| Học thuật | Semantic Scholar API, arXiv API, Crossref (DOI metadata) |
| Tổng hợp có dẫn | Perplexity (domain filter `scholar.google.com`) |
| Trích dẫn | Google Scholar **không có API công khai** — chỉ tìm qua domain filter |

Ưu tiên **nguồn sơ cấp**: repo GitHub chính chủ, docs chính thức (anthropic.com, mermaid.js.org,
python-docx.readthedocs.io...), paper/DOI, hơn là blog tổng hợp.

## Xác minh trích dẫn — chống bịa nguồn

Bằng chứng nghiên cứu: LLM khi "không được ground" có thể bịa 78–90% trích dẫn.
Biện pháp: **xác minh bằng truy hồi**, không dựa vào trí nhớ model.

- Mỗi trích dẫn phải là URL **đã thực sự fetch** trong phiên.
- Kiểm tra ở **mức trường**: DOI, tiêu đề, tác giả, venue, năm — riêng từng cái, không so cả chuỗi.
- Gắn nhãn mức khớp: `EXACT` / `MINOR` / `MAJOR` / `HALLUCINATED`.
- Không chắc → đánh dấu `UNVERIFIED`, KHÔNG đưa vào kết luận như sự thật.

Chấm điểm độ tin cậy nguồn (0–100) dựa trên: chính chủ?, peer-review?, ngày cập nhật?, trích dẫn nguồn gốc?

## Định dạng báo cáo cuối

```markdown
# <Tiêu đề nghiên cứu>
## TL;DR (3–5 dòng)
## Bối cảnh & câu hỏi
## Phát hiện chính (mỗi mục có citation [n])
## Mâu thuẫn / điều chưa chắc chắn
## Khuyến nghị / kết luận
## Hạn chế & khoảng trống
## Nguồn
[1] Tên — URL — ngày truy cập — mức tin cậy
```

## Quy tắc bất biến

- Không bịa URL, không bịa số liệu, không bịa trích dẫn.
- Phân biệt rõ: **sự thật có nguồn** vs **suy luận** vs **chưa xác minh**.
- Nêu mâu thuẫn giữa các nguồn thay vì chọn bừa.
- Nếu không tìm được bằng chứng → nói rõ "không tìm thấy nguồn đủ tin cậy".

Log nguồn khi làm việc: xem `reference/source-log-template.md`.
