# CLAUDE.md

Dự án này là bộ **agent skills** (tài liệu, slide, sơ đồ, nghiên cứu, PDF, Excel).

Xem `AGENTS.md` để biết danh sách skill, quy tắc routing và nguyên tắc bất biến.

Skills được nạp từ:

- `.claude/skills/<name>/SKILL.md`
- `.agents/skills/<name>/SKILL.md` (bản mirror)

Sau khi sửa skill trong `.claude/skills/`, chạy `tools/sync-skills.ps1` để đồng bộ.
