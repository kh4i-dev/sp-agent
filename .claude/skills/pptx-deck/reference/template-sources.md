# Nguồn template & minh họa cho deck PPTX

## Template tải trực tiếp (.pptx/.potx)
- Slidesgo — https://slidesgo.com (free, giữ slide credit) — tech pitch, 1000+ icons.
- SlidesCarnival — https://www.slidescarnival.com (free, không cần đăng ký) — có **illustration isometric** ("Tech Illustrated").
- GreatPPT — https://www.greatppt.com (16:9, 500+ icons).
- Slidesdocs — https://slidesdocs.com (minimalist tech).
- AiPPT — https://www.aippt.com (modern tech, mockup).
- Slidestack — https://slidestack.com (1500+ icons, master slides).
- Microsoft Create — https://create.microsoft.com (.potx chính chủ).

## Repo GitHub / skill
- aresplus/tech-slides-generator — skill python-pptx "tech": 6 theme, bento, tự lấy ảnh Unsplash.
- hugohe3/ppt-master — doc → .pptx native; 20 layout, 52 mẫu infographic, 6700+ icon Tabler, import template.
- lionelwust/openwebui-generate-slides — engine python-pptx; ~25 layout, Lucide icons, native charts.
- SamyGenAI/Smart-creator-design-system — design system → .pptx (pptxgenjs); có `assets/icons`, `assets/illustrations`.
- atomiechen/THU-PPT-Theme — theme học thuật flat (mô phỏng: ô vuông + dải dọc + tiêu đề màu nhấn).
- gbif/ppt-template — .potx + toolkit + fonts.
- eLearningHub/quarto-simple-presentation-starter — 4 theme pptx (cosmic-latte/classy/dark-mode/nord).

## Icon / minh họa
- Icon vector: Tabler Icons, Lucide, Iconify API (`https://api.iconify.design/<set>/<name>.svg`), SVG Repo.
- Ảnh: Unsplash, Pexels, Pixabay.

## Mẹo chuyển SVG → PNG (Windows)
```powershell
# ImageMagick (winget install ImageMagick.ImageMagick). QUAN TRỌNG: input phải đứng TRƯỚC -resize
magick -background none -density 384 icon.svg -resize 128x128 icon.png
```
Iconify thường xuất `width="1em"` → cần `-density` để rasterize đúng.
