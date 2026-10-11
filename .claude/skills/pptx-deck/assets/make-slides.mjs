// Sinh slide PPTX cho BTL TMĐT — PptxGenJS, 16:9. Thiết kế sạch + speaker notes.
// Chạy:  cd tools/slides && node make-slides.mjs
import pptxgen from 'pptxgenjs';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..', '..');
const OUT_DIR = resolve(ROOT, 'docs', 'slides');
mkdirSync(OUT_DIR, { recursive: true });

// ---------- Design system ----------
const FONT = 'Segoe UI';
const C = { navy: '0E3A47', navy2: '12505F', cyan: '0891B2', accent: '06B6D4', ink: '36474F', muted: '7B8D95', line: 'DCE8EC', soft: 'F3F8FA', white: 'FFFFFF' };
const S = { W: 13.333, H: 7.5, M: 0.85 }; // margin
const IMG = (p) => resolve(ROOT, 'docs', 'images', p);
const IMGF = (p) => resolve(ROOT, 'frontend', 'public', 'img', p);
const ICON = (n) => resolve(ROOT, 'docs', 'slides', 'icons', n + '.png');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Nhóm BTL CNPM';
pptx.company = 'TMĐT';
pptx.title = 'TMĐT — Sàn TMĐT ký quỹ & giao vận an toàn';
let SLIDE_NO = 0;
function mk() { SLIDE_NO++; return pptx.addSlide(); }
const notes = (s, t) => { if (t) s.addNotes(t); };
function pngSize(p) { try { const b = readFileSync(p); if (b.length > 24 && b.readUInt32BE(0) === 0x89504e47) return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; } catch {} return null; }

// ---------- Primitives ----------
function footer(s) {
  s.addShape(pptx.ShapeType.line, { x: S.M, y: 7.03, w: S.W - 2 * S.M, h: 0, line: { color: C.line, width: 1 } });
  s.addText('TMĐT · Sàn TMĐT ký quỹ & giao vận an toàn', { x: S.M, y: 7.07, w: 9.5, h: 0.3, fontFace: FONT, fontSize: 9.5, color: C.muted });
  s.addText(String(SLIDE_NO).padStart(2, '0'), { x: S.W - S.M - 0.7, y: 7.07, w: 0.7, h: 0.3, fontFace: FONT, fontSize: 9.5, bold: true, color: C.cyan, align: 'right' });
}
function topbar(s) {}
function header(s, title, kicker) {
  s.background = { color: C.white };
  s.addShape(pptx.ShapeType.rect, { x: 0.6, y: 0.5, w: 0.52, h: 0.52, fill: { color: C.cyan }, line: { type: 'none' } });
  s.addShape(pptx.ShapeType.rect, { x: 0.6, y: 1.02, w: 0.16, h: 5.82, fill: { color: C.soft }, line: { type: 'none' } });
  s.addText(title, { x: 1.42, y: 0.46, w: 11.2, h: 0.62, fontFace: FONT, fontSize: 25, bold: true, color: C.cyan, valign: 'middle' });
  if (kicker) s.addText(kicker, { x: 1.44, y: 1.1, w: 11.2, h: 0.3, fontFace: FONT, fontSize: 10.5, bold: true, color: C.muted, charSpacing: 1.4 });
}
function bullets(s, items, x, y, w, { size = 18, gap = 0.86, color = C.ink } = {}) {
  items.forEach((t, i) => {
    const yy = y + i * gap;
    s.addShape(pptx.ShapeType.rect, { x, y: yy + 0.12, w: 0.11, h: 0.24, fill: { color: C.cyan }, line: { type: 'none' } });
    s.addText(t, { x: x + 0.3, y: yy, w: w - 0.3, h: gap, fontFace: FONT, fontSize: size, color, valign: 'top', lineSpacingMultiple: 1.04 });
  });
}
function card(s, x, y, w, h, { fill = C.soft, line = C.line } = {}) {
  s.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: line, width: 1 } });
}
function fitImage(s, img, x, y, w, h, caption) {
  if (existsSync(img)) s.addImage({ path: img, x, y, w, h, sizing: { type: 'contain', w, h } });
  else s.addText(`[Thiếu ảnh]`, { x, y, w, h, fontFace: FONT, fontSize: 12, color: 'C0392B', align: 'center', valign: 'middle' });
  if (caption) s.addText(caption, { x, y: y + h + 0.05, w, h: 0.28, fontFace: FONT, fontSize: 10.5, italic: true, color: C.muted, align: 'center' });
}

// ---------- Slides ----------
function cover(note) {
  const s = mk();
  s.background = { color: C.navy };
  const im = IMGF('hero-1.jpg');
  if (existsSync(im)) s.addImage({ path: im, x: 7.0, y: 0, w: 6.333, h: S.H, sizing: { type: 'cover', w: 6.333, h: S.H } });
  s.addShape(pptx.ShapeType.rect, { x: 6.0, y: 0, w: 2.6, h: S.H, fill: { type: 'gradient', stops: [{ color: C.navy, transparency: 0, position: 0 }, { color: C.navy, transparency: 100, position: 100 }], angle: 0 }, line: { type: 'none' } });
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 6.6, h: S.H, fill: { color: C.navy }, line: { type: 'none' } });
  s.addShape(pptx.ShapeType.rect, { x: S.M, y: 2.4, w: 0.16, h: 1.7, fill: { color: C.accent } });
  s.addText('BTL · CÔNG NGHỆ PHẦN MỀM · 2026', { x: 1.15, y: 1.55, w: 5.6, h: 0.35, fontFace: FONT, fontSize: 12, bold: true, color: C.accent, charSpacing: 2 });
  s.addText('TMĐT', { x: 1.15, y: 2.3, w: 5.6, h: 1.1, fontFace: FONT, fontSize: 54, bold: true, color: C.white, valign: 'middle' });
  s.addText('Sàn thương mại điện tử\nKý quỹ & giao vận an toàn', { x: 1.15, y: 3.5, w: 5.6, h: 1.05, fontFace: FONT, fontSize: 22, bold: true, color: 'DCE9ED', lineSpacingMultiple: 1.08 });
  s.addText('Giao dịch trung lập · Tem kiện ký số HMAC-SHA256 · Che mờ dữ liệu (NĐ 13)', { x: 1.15, y: 4.65, w: 5.5, h: 0.7, fontFace: FONT, fontSize: 12.5, color: '9FB9C1', lineSpacingMultiple: 1.1 });
  s.addText('Nhóm thực hiện: ..................   ·   GVHD: ..................', { x: 1.15, y: 6.45, w: 5.6, h: 0.4, fontFace: FONT, fontSize: 11.5, color: '9FB9C1' });
  notes(s, note);
}

function agenda(items, note) {
  const s = mk();
  header(s, 'Nội dung trình bày', 'AGENDA');
  const y0 = 1.95, rowH = 1.0, x = S.M + 0.3;
  items.forEach((it, i) => {
    const y = y0 + i * rowH;
    s.addText(String(i + 1).padStart(2, '0'), { x, y: y - 0.12, w: 1.2, h: 0.8, fontFace: FONT, fontSize: 30, bold: true, color: C.cyan, transparency: 35, valign: 'middle' });
    s.addText(it.t, { x: x + 1.35, y, w: 8.5, h: 0.5, fontFace: FONT, fontSize: 20, bold: true, color: C.navy, valign: 'middle' });
    s.addText(it.d, { x: x + 1.35, y: y + 0.5, w: 9.5, h: 0.4, fontFace: FONT, fontSize: 13, color: C.muted });
    if (i < items.length - 1) s.addShape(pptx.ShapeType.line, { x, y: y + rowH - 0.16, w: 11.0, h: 0, line: { color: C.line, width: 1 } });
  });
  footer(s); notes(s, note);
}

function statsSlide(title, kicker, stats, note) {
  const s = mk();
  header(s, title, kicker);
  const y = 2.5, gap = 0.5, w = (S.W - 2 * S.M - 2 * gap) / 3, h = 3.0;
  stats.forEach((st, i) => {
    const x = S.M + i * (w + gap);
    card(s, x, y, w, h, { fill: C.white, line: C.line });
    s.addShape(pptx.ShapeType.rect, { x, y, w: 0.14, h, fill: { color: C.cyan }, line: { type: 'none' } });
    s.addText(st.value, { x: x + 0.35, y: y + 0.5, w: w - 0.6, h: 1.0, fontFace: FONT, fontSize: 44, bold: true, color: C.cyan });
    s.addText(st.label, { x: x + 0.35, y: y + 1.55, w: w - 0.6, h: 0.5, fontFace: FONT, fontSize: 15, bold: true, color: C.navy });
    s.addText(st.desc, { x: x + 0.35, y: y + 2.05, w: w - 0.6, h: 0.8, fontFace: FONT, fontSize: 12, color: C.ink, lineSpacingMultiple: 1.05 });
  });
  footer(s); notes(s, note);
}

function cardsSlide(title, kicker, cards, note) {
  const s = mk();
  header(s, title, kicker);
  const y = 2.0, gap = 0.5, w = (S.W - 2 * S.M - 2 * gap) / 3, h = 4.0;
  cards.forEach((c, i) => {
    const x = S.M + i * (w + gap);
    card(s, x, y, w, h, { fill: C.white, line: C.line });
    const iw = w - 0.36, ih = 1.5, ix = x + 0.18, iy = y + 0.18;
    if (c.img && existsSync(c.img)) s.addImage({ path: c.img, x: ix, y: iy, w: iw, h: ih, sizing: { type: 'cover', w: iw, h: ih } });
    s.addShape(pptx.ShapeType.ellipse, { x: ix + 0.1, y: iy + 0.1, w: 0.5, h: 0.5, fill: { color: C.white }, line: { color: C.line, width: 1 } });
    if (c.icon && existsSync(ICON(c.icon))) s.addImage({ path: ICON(c.icon), x: ix + 0.19, y: iy + 0.19, w: 0.32, h: 0.32 });
    s.addText(c.t, { x: x + 0.28, y: iy + ih + 0.16, w: w - 0.56, h: 0.7, fontFace: FONT, fontSize: 16, bold: true, color: C.navy, lineSpacingMultiple: 1.02 });
    s.addText(c.b, { x: x + 0.28, y: iy + ih + 0.86, w: w - 0.56, h: 1.4, fontFace: FONT, fontSize: 12, color: C.ink, lineSpacingMultiple: 1.12 });
  });
  footer(s); notes(s, note);
}

function bulletsSlide(title, kicker, items, note) {
  const s = mk();
  header(s, title, kicker);
  bullets(s, items, S.M + 0.3, 2.0, 11.4, { size: 18, gap: 0.95 });
  footer(s); notes(s, note);
}

function section(no, title, note, icon) {
  const s = mk();
  s.background = { color: C.navy };
  s.addText(no, { x: 0.7, y: 1.7, w: 6, h: 3.2, fontFace: FONT, fontSize: 150, bold: true, color: 'FFFFFF', transparency: 88 });
  s.addShape(pptx.ShapeType.rect, { x: S.M, y: 3.55, w: 0.16, h: 0.85, fill: { color: C.accent } });
  s.addText(title, { x: S.M + 0.35, y: 3.5, w: 10, h: 0.95, fontFace: FONT, fontSize: 34, bold: true, color: C.white, valign: 'middle' });
  if (icon && existsSync(ICON(icon))) s.addImage({ path: ICON(icon), x: 10.7, y: 2.9, w: 1.5, h: 1.5 });
  s.addText('TMĐT · BTL CNPM', { x: S.M, y: 6.5, w: 6, h: 0.4, fontFace: FONT, fontSize: 11, color: '9FB9C1' });
  notes(s, note);
}

function diagram(title, img, caption, note, bl) {
  const s = mk();
  header(s, title, 'SƠ ĐỒ THIẾT KẾ');
  const dim = pngSize(img); const ratio = dim ? dim.w / dim.h : 2;
  if (ratio < 0.7) {
    card(s, S.M, 1.55, 4.9, 5.0);
    fitImage(s, img, S.M + 0.18, 1.7, 4.54, 4.7);
    if (bl) bullets(s, bl, 6.05, 1.75, 6.4, { size: 15.5, gap: 0.9 });
  } else if (bl) {
    card(s, S.M, 1.55, 11.63, 3.35);
    fitImage(s, img, S.M + 0.22, 1.68, 11.19, 3.09, caption);
    bullets(s, bl, S.M + 0.25, 5.15, 11.2, { size: 15, gap: 0.5 });
  } else {
    card(s, S.M, 1.55, 11.63, 5.0);
    fitImage(s, img, S.M + 0.22, 1.7, 11.19, 4.7, caption);
  }
  footer(s); notes(s, note);
}

function seqGroup(title, imgs, bl, note) {
  const s = mk();
  header(s, title, 'SƠ ĐỒ THIẾT KẾ');
  bullets(s, bl, 0.75, 1.8, 4.3, { size: 14, gap: 1.15 });
  const x = 5.35, w = 7.3, h = 1.66;
  imgs.slice(0, 3).forEach((p, i) => {
    const y = 1.58 + i * (h + 0.18);
    card(s, x, y, w, h);
    if (existsSync(p)) s.addImage({ path: p, x: x + 0.14, y: y + 0.1, w: w - 0.28, h: h - 0.2, sizing: { type: 'contain', w: w - 0.28, h: h - 0.2 } });
  });
  footer(s); notes(s, note);
}

function demo(title, pairs, note) {
  const s = mk();
  header(s, title, 'DEMO GIAO DIỆN');
  if (pairs.length === 1) {
    const [a, ca] = pairs[0];
    card(s, S.M, 1.55, 11.63, 5.0);
    if (existsSync(a)) s.addImage({ path: a, x: S.M + 0.22, y: 1.7, w: 11.19, h: 4.7, sizing: { type: 'contain', w: 11.19, h: 4.7 } });
    s.addText(ca, { x: S.M, y: 6.63, w: 11.63, h: 0.3, fontFace: FONT, fontSize: 10.5, italic: true, color: C.muted, align: 'center' });
  } else {
    const w = 5.37, h = 4.35;
    [[S.M, ...pairs[0]], [S.W / 2 + 0.28, ...pairs[1]]].forEach(([x, p, c]) => {
      card(s, x, 1.55, w, h + 0.72);
      if (existsSync(p)) s.addImage({ path: p, x: x + 0.14, y: 1.7, w: w - 0.28, h, sizing: { type: 'contain', w: w - 0.28, h } });
      s.addText(c, { x, y: 1.62 + h + 0.12, w, h: 0.34, fontFace: FONT, fontSize: 12, bold: true, color: C.navy, align: 'center' });
    });
  }
  footer(s); notes(s, note);
}

function closing(note) {
  const s = mk();
  s.background = { color: C.navy };
  s.addShape(pptx.ShapeType.rect, { x: S.W / 2 - 0.66, y: 3.15, w: 1.33, h: 0.1, fill: { color: C.accent } });
  s.addText('Cảm ơn!', { x: 0.9, y: 2.0, w: 11.53, h: 1.1, fontFace: FONT, fontSize: 46, bold: true, color: C.white, align: 'center' });
  s.addText('Hỏi & Đáp', { x: 0.9, y: 3.5, w: 11.53, h: 0.6, fontFace: FONT, fontSize: 22, color: 'CFE9EF', align: 'center' });
  s.addText('TMĐT · Sàn TMĐT ký quỹ & giao vận an toàn', { x: 0.9, y: 6.45, w: 11.53, h: 0.4, fontFace: FONT, fontSize: 12, color: '9FB9C1', align: 'center' });
  notes(s, note);
}

// ---------- Deck ----------
cover('Chào hội đồng, em xin trình bày đề tài TMĐT — sàn TMĐT áp dụng ký quỹ (escrow) và tem kiện ký số để chống tráo hàng COD.');

agenda([
  { t: 'Bối cảnh & giải pháp', d: 'Vấn đề ship COD và 3 trụ cột giải pháp của TMĐT' },
  { t: 'Thiết kế & kiến trúc', d: 'Kiến trúc, phân rã chức năng, use case, luồng, mô hình dữ liệu' },
  { t: 'Demo hệ thống', d: 'Ảnh chụp các màn hình chính đang chạy thực tế' },
  { t: 'Công nghệ & kiểm thử', d: 'Tech stack, bảo mật và kết quả kiểm thử' },
], 'Em xin trình bày theo 4 phần: bối cảnh & giải pháp, thiết kế & kiến trúc, demo, và công nghệ & kiểm thử.');

statsSlide('Đặt vấn đề — nghịch lý COD', 'BỐI CẢNH', [
  { value: '15–25%', label: 'Tỷ lệ "boom hàng"', desc: 'Đơn COD bị bùng/hoàn, gây thiệt hại nặng cho người bán.' },
  { value: '0%', label: 'Bảo đảm cho người mua', desc: 'Khách trả tiền trước khi biết trong hộp có gì — rủi ro tráo hàng.' },
  { value: '1 lỗ hổng', label: 'Khâu giao nhận', desc: 'Tráo ruột, shipper giả mạo, rò rỉ dữ liệu cá nhân (PII).' },
], 'Nêu 3 con số thể hiện nghịch lý COD: tỷ lệ boom hàng cao, người mua không có bảo đảm, và rủi ro tập trung ở khâu giao nhận.');

cardsSlide('Giải pháp TMĐT', 'ĐỀ XUẤT', [
  { img: IMGF('step-1.jpg'), icon: 'wallet', t: 'Ký quỹ Escrow', b: 'Tiền bị khóa ở quỹ trung lập cho tới khi nhận hàng thành công. Người bán không thể rút sớm.' },
  { img: IMGF('step-2.jpg'), icon: 'qrcode', t: 'Tem QR HMAC-SHA256', b: 'Mỗi kiện hàng gắn một chữ ký số độc bản, chống tráo và chống tái sử dụng tem.' },
  { img: IMGF('step-3.jpg'), icon: 'shield-lock', t: 'Che mờ dữ liệu PII', b: 'Theo NĐ 13/2023/NĐ-CP: ẩn SĐT & địa chỉ trên vận đơn, chặn shipper giả.' },
], 'Giải pháp gồm 3 trụ cột: ký quỹ giữ tiền ở giữa, tem QR ký số định danh kiện hàng, và che mờ dữ liệu cá nhân.');

section('01', 'Thiết kế & Kiến trúc', 'Sang phần thiết kế hệ thống và các sơ đồ UML.', 'shield-check');

diagram('Kiến trúc tổng thể', IMG('diagrams/01-kien-truc.png'), 'Nuxt 3 (client) → NestJS /api/v1 → Prisma (SQLite/PG); SePay webhook.', 'Kiến trúc 3 tầng client → API → DB, kèm webhook SePay xác thực HMAC.', [
  'Client Nuxt 3 (SSR) → API NestJS: Guards (JWT + RBAC + Throttler) → Controllers → Services → Prisma DB.',
  'Webhook SePay (VietQR) xác thực HMAC-SHA256, chống trùng bằng sepayId.',
]);
diagram('Phân rã chức năng (10 phân hệ)', IMG('diagrams/02-phan-ra-chuc-nang.png'), 'P1..P10.', 'Hệ thống chia 10 nhóm chức năng P1–P10.', [
  'P1–P10: định danh & bảo mật · gian hàng & sản phẩm · vận hành shipper · nhận hàng an toàn · đơn hàng.',
  'Tiếp: thanh toán & ký quỹ · tra cứu & bảo mật TT · khiếu nại & chống lừa đảo · đánh giá · dashboard.',
]);
diagram('Biểu đồ ca sử dụng', IMG('diagrams/03-use-case.png'), 'Use case theo 4 tác nhân: Buyer · Shop · Shipper · Admin.', 'Use case chia theo 4 tác nhân; ca trọng tâm UC-06 quét QR xác thực.', [
  '4 nhóm tác nhân: Người mua · Người bán · Tài xế · Quản trị.',
  'Ca trọng tâm UC-06: Người mua quét QR xác thực kiện hàng để giải ngân.',
]);
diagram('Luồng hoạt động — Quét QR xác thực', IMG('diagrams/04-activity-quet-qr.png'), '', 'Luồng quét QR với các nhánh kiểm tra và nhánh lỗi.', [
  'Kiểm tra chữ ký HMAC → token còn hạn → đúng đơn → ghi scan_events.',
  'Nhánh lỗi: QR_INVALID / QR_EXPIRED / NOT_FOUND / wrong_parcel (gắn cờ gian lận).',
  'Hợp lệ → bắn event ParcelVerified → giải ngân escrow, đơn chuyển completed.',
]);
seqGroup('Ba luồng tuần tự chính', [
  IMG('diagrams/05-sequence-mua-hang-escrow.png'),
  IMG('diagrams/06-sequence-verify-giai-ngan.png'),
  IMG('diagrams/07-sequence-nap-tien-sepay.png'),
], [
  'Mua hàng & ký quỹ: tách đơn theo shop → Escrow hold → ghi sổ cái kép.',
  'Quét QR & giải ngân: verify HMAC → parcel.verified → release cho shop (trừ hoa hồng).',
  'Nạp tiền VietQR: webhook SePay idempotent (sepayId unique) → cộng ví.',
], 'Trình bày 3 luồng tuần tự chính.');
diagram('Biểu đồ lớp (rút gọn)', IMG('diagrams/08-class-diagram.png'), 'Thực thể lõi.', 'Các thực thể lõi và quan hệ.', [
  'Thực thể lõi: User, ShopProfile, Product, Order, Parcel, Wallet, EscrowHold, Dispute, Review.',
  'Quan hệ: Order 1—* OrderItem; Order 1—1 EscrowHold; Parcel 1—* ParcelToken / ScanEvent.',
]);
diagram('Vòng đời đơn hàng', IMG('diagrams/09-state-don-hang.png'), '', 'Vòng đời trạng thái đơn hàng và tiền ký quỹ.', [
  'pending_payment → paid (escrow held)',
  'paid → packed → shipping → delivered',
  'delivered → delivered_verified (quét QR) → completed',
  'Nhánh: cancelled · returned (khiếu nại/hoàn tiền)',
]);
diagram('ERD rút gọn', IMG('diagrams/10-erd.png'), 'Bản đầy đủ: docs/CHO_AGENT_DEV/03_ERD_SCHEMA.dbml.', 'ERD rút gọn các thực thể lõi.', [
  'Tiền là số nguyên VND; sổ cái wallet_ledger_entries append-only.',
  'parcel_tokens.token_hash unique; sepay_webhooks.sepayId unique.',
  'Hệ thống ~35 bảng — sơ đồ là các thực thể lõi.',
]);

section('02', 'Demo giao diện', 'Chuyển sang demo trên hệ thống đang chạy (ảnh chụp thật 16:9).', 'layout-grid');

demo('Trang chủ', [[IMG('audit/02-trang-chu.png'), 'Trang chủ — danh mục & sản phẩm bảo chứng']], 'Giới thiệu trang chủ: tìm kiếm, danh mục, sản phẩm gắn badge bảo chứng.');
demo('Đăng nhập & Chi tiết sản phẩm', [[IMG('audit/01-dang-nhap.png'), 'Đăng nhập (tài khoản demo)'], [IMG('audit/03-san-pham.png'), 'Chi tiết sản phẩm']], 'Đăng nhập tài khoản mẫu và xem chi tiết sản phẩm.');
demo('Giỏ hàng & Đơn mua', [[IMG('audit/04-gio-hang.png'), 'Giỏ hàng (escrow)'], [IMG('audit/05-don-mua.png'), 'Đơn mua — tab trạng thái']], 'Giỏ hàng và danh sách đơn; chú ý tiền đang ở trạng thái ký quỹ.');
demo('Chi tiết đơn & Ví người bán', [[IMG('audit/06-chi-tiet-don.png'), 'Chi tiết đơn & hành trình ký quỹ'], [IMG('audit/07-so-du-nguoi-ban.png'), 'Số dư ví người bán']], 'Chi tiết đơn có timeline escrow; ví thể hiện số dư khả dụng / chờ / đóng băng.');
demo('Kênh người bán & Cổng tài xế', [[IMG('audit/08-kenh-nguoi-ban.png'), 'Kênh người bán (Shop)'], [IMG('audit/09-cong-tai-xe.png'), 'Cổng tài xế (Shipper)']], 'Shop: đơn chờ đóng gói, in tem QR. Shipper: nhận đơn, quét nhận kho & quét đối soát.');
demo('Admin: Tổng quan & Duyệt rút', [[IMG('audit/10-admin-tong-quan.png'), 'Admin — GMV & trọng tài'], [IMG('audit/11-admin-duyet-rut.png'), 'Admin — duyệt lệnh rút']], 'Khu quản trị: GMV, quỹ escrow, KPI; duyệt nạp/rút và xử lý khiếu nại.');

bulletsSlide('Công nghệ & Kiểm thử', 'TỔNG KẾT', [
  'Frontend: Nuxt 3 + Tailwind v4 (SSR).',
  'Backend: NestJS 10 + Prisma + SQLite; JWT/RBAC + Throttler.',
  'Bảo mật: HMAC-SHA256 (tem kiện), Idempotency (webhook), Ledger kép append-only.',
  'Kiểm thử: Jest (đơn vị) + Playwright (E2E quét chốt đơn).',
], 'Tóm tắt công nghệ và kiểm thử.');

closing('Em xin cảm ơn hội đồng đã lắng nghe. Nhóm sẵn sàng nhận câu hỏi.');

// ---------- Save ----------
const outPath = resolve(OUT_DIR, 'TMDT_slides.pptx');
let saved = outPath;
try { await pptx.writeFile({ fileName: outPath }); }
catch (e) {
  const stamp = new Date().toISOString().slice(11, 19).replace(/:/g, '');
  saved = resolve(OUT_DIR, `TMDT_slides_${stamp}.pptx`);
  await pptx.writeFile({ fileName: saved });
  console.log('(!) File gốc đang mở → ghi bản mới:', saved.split('\\').pop());
}
console.log('✔ Đã tạo slide:', saved.replace(ROOT + '\\', ''), '(tổng ' + SLIDE_NO + ' slide)');
