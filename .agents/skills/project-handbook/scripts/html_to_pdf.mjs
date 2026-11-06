#!/usr/bin/env node
/**
 * html_to_pdf.mjs — HTML -> PDF bằng Chrome headless qua CDP (KHONG can npm package nao).
 *
 * Vi sao khong dung `chrome --print-to-pdf`:
 *   - CLI khong dat duoc CHAN TRANG (footer) co so trang dong.
 *   - CLI khong kiem soat duoc le/khung in theo tung file.
 * Qua CDP `Page.printToPDF` ta dat duoc: kho A4, le, footer co `.pageNumber`, in nen mau.
 *
 * Dung:
 *   node html_to_pdf.mjs --in <file.html> --out <file.pdf>
 *        [--title "..."] [--footer-left "..."] [--no-footer] [--no-page-number]
 *        [--header "..."] [--margin-mm 18,16,18,16] [--landscape] [--scale 1]
 *        [--paper-w 8.27 --paper-h 11.69] [--prefer-css-size]
 *        [--wait-ms 700] [--chrome "<path>"] [--keep-open]
 *
 *   --paper-w/--paper-h  kich thuoc trang theo INCH (mac dinh A4). Dung khi can
 *                        trang dung bang mot khung tuy y, vd xuat so do SVG:
 *                        paper = <w_px>/96 x <h_px>/96 roi rasterize o dpi 96*scale.
 *
 * Node >= 20 (can WebSocket global). Chrome/Edge tim tu dong neu khong truyen --chrome.
 */

import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';

// ---------------------------------------------------------------- CLI
function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) out[key] = true;
      else { out[key] = next; i++; }
    } else out._.push(a);
  }
  return out;
}
const args = parseArgs(process.argv.slice(2));

const inPath = args.in;
const outPath = args.out;
if (!inPath || !outPath) {
  console.error('Usage: node html_to_pdf.mjs --in <file.html> --out <file.pdf> [options]');
  process.exit(2);
}
if (!existsSync(inPath)) {
  console.error(`[html_to_pdf] Khong thay file: ${inPath}`);
  process.exit(2);
}

const toMm = (v, d) => (v === undefined ? d : Number(v));
const [mt = 18, mr = 16, mb = 18, ml = 16] = String(args['margin-mm'] ?? '')
  .split(',').map((s) => s.trim()).filter((s) => s !== '').map(Number);
const margin = {
  top: toMm(mt, 18) / 25.4,
  right: toMm(mr, 16) / 25.4,
  bottom: toMm(mb, 18) / 25.4,
  left: toMm(ml, 16) / 25.4,
};
const waitMs = Number(args['wait-ms'] ?? 700);
const scale = Number(args.scale ?? 1);
const landscape = Boolean(args.landscape);

// ---------------------------------------------------------------- tim Chrome
function findChrome() {
  if (args.chrome && existsSync(args.chrome)) return args.chrome;
  const cands = [
    process.env.CHROME_PATH,
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ].filter(Boolean);
  for (const c of cands) if (existsSync(c)) return c;
  return null;
}
const chromePath = findChrome();
if (!chromePath) {
  console.error('[html_to_pdf] Khong tim thay Chrome/Edge. Truyen --chrome "<duong dan>".');
  process.exit(3);
}

// ---------------------------------------------------------------- tien ich
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function fetchJson(url, tries = 40, delay = 150) {
  for (let i = 0; i < tries; i++) {
    try {
      const res = await fetch(url);
      if (res.ok) return await res.json();
    } catch { /* chrome chua len */ }
    await sleep(delay);
  }
  throw new Error(`Khong ket noi duoc CDP endpoint: ${url}`);
}

function esc(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function footerTemplate() {
  if (args['no-footer']) return '<div></div>';
  const left = args['footer-left'] ?? '';
  const num = args['no-page-number']
    ? ''
    : '<span style="font-size:8pt">Trang <span class="pageNumber"></span>/<span class="totalPages"></span></span>';
  return `
  <div style="width:100%;padding:0 12mm;font-family:'Segoe UI',Arial,sans-serif;color:#555;
              display:flex;justify-content:space-between;align-items:center;">
    <span style="font-size:8pt">${esc(left)}</span>
    ${num}
  </div>`;
}

function headerTemplate() {
  if (!args.header) return '<div></div>';
  return `
  <div style="width:100%;padding:0 12mm;font-family:'Segoe UI',Arial,sans-serif;color:#777;font-size:8pt;
              border-bottom:0.4pt solid #ccc;padding-bottom:2mm;">${esc(args.header)}</div>`;
}

// ---------------------------------------------------------------- CDP
class Cdp {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.events = []; }
  static async connect(url) {
    const ws = new WebSocket(url);
    await new Promise((res, rej) => {
      ws.addEventListener('open', res, { once: true });
      ws.addEventListener('error', (e) => rej(new Error('WS error: ' + (e?.message ?? 'unknown'))), { once: true });
    });
    const c = new Cdp(ws);
    ws.addEventListener('message', (ev) => {
      let msg;
      try { msg = JSON.parse(ev.data); } catch { return; }
      if (msg.id && c.pending.has(msg.id)) {
        const { res, rej } = c.pending.get(msg.id);
        c.pending.delete(msg.id);
        msg.error ? rej(new Error(msg.error.message)) : res(msg.result);
      } else if (msg.method) c.events.push(msg.method);
    });
    return c;
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => {
      this.pending.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => {
        if (this.pending.has(id)) {
          this.pending.delete(id);
          rej(new Error(`CDP timeout: ${method}`));
        }
      }, 60000);
    });
  }
  close() { try { this.ws.close(); } catch { /* ignore */ } }
}

// ---------------------------------------------------------------- main
async function main() {
  const htmlAbs = resolve(inPath);
  const pdfAbs = resolve(outPath);
  mkdirSync(dirname(pdfAbs), { recursive: true });

  const port = 9400 + Math.floor(Math.random() * 500);
  const profile = resolve(tmpdir(), `hb-chrome-${process.pid}-${Date.now()}`);
  const url = pathToFileURL(htmlAbs).href;

  const child = spawn(chromePath, [
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-extensions',
    '--disable-background-networking',
    '--hide-scrollbars',
    `--user-data-dir=${profile}`,
    `--remote-debugging-port=${port}`,
    '--remote-allow-origins=*',
    url,
  ], { stdio: 'ignore', detached: false });

  let cdp = null;
  try {
    // Cho trang dich xuat hien trong danh sach target
    let pageTarget = null;
    for (let i = 0; i < 60 && !pageTarget; i++) {
      const list = await fetchJson(`http://127.0.0.1:${port}/json/list`).catch(() => null);
      if (Array.isArray(list)) {
        pageTarget = list.find((t) => t.type === 'page' && t.webSocketDebuggerUrl);
      }
      if (!pageTarget) await sleep(200);
    }
    if (!pageTarget) throw new Error('Chrome khong mo duoc trang (khong co target page).');

    cdp = await Cdp.connect(pageTarget.webSocketDebuggerUrl);
    await cdp.send('Page.enable');

    // Doi DOM + font san sang (tranh PDF bi cat chu / thieu font Viet)
    await cdp.send('Runtime.enable').catch(() => undefined);
    await sleep(waitMs);
    await cdp.send('Runtime.evaluate', {
      expression: `(async () => { try { await document.fonts.ready; } catch(e){} ; return true; })()`,
      awaitPromise: true,
    }).catch(() => undefined);
    await sleep(150);

    // --paper-w/--paper-h (inch): dung khi can trang DUNG kich thuoc tuy y
    // (vd xuat so do SVG ra PDF/PNG voi kich thuoc pixel chinh xac ~ W/96 inch).
    const paperW = Number(args['paper-w'] ?? 8.27);
    const paperH = Number(args['paper-h'] ?? 11.69);
    const preferCss = Boolean(args['prefer-css-size']);

    const res = await cdp.send('Page.printToPDF', {
      landscape,
      printBackground: true,
      preferCSSPageSize: preferCss,
      scale,
      paperWidth: paperW,   // A4 ngang (inch) hoac --paper-w
      paperHeight: paperH,  // A4 doc (inch)  hoac --paper-h
      marginTop: margin.top,
      marginBottom: margin.bottom,
      marginLeft: margin.left,
      marginRight: margin.right,
      displayHeaderFooter: !(args['no-footer'] && !args.header),
      headerTemplate: headerTemplate(),
      footerTemplate: footerTemplate(),
      transferMode: 'ReturnAsBase64',
    });

    const buf = Buffer.from(res.data, 'base64');
    writeFileSync(pdfAbs, buf);
    const kb = (buf.length / 1024).toFixed(1);
    console.log(`[html_to_pdf] OK -> ${pdfAbs}  (${kb} KB)`);
  } finally {
    if (cdp) cdp.close();
    if (!args['keep-open']) {
      try { child.kill(); } catch { /* ignore */ }
      await sleep(250);
      try { rmSync(profile, { recursive: true, force: true }); } catch { /* ignore */ }
    }
  }
}

main().catch((e) => {
  console.error('[html_to_pdf] LOI:', e?.message ?? e);
  process.exit(1);
});
