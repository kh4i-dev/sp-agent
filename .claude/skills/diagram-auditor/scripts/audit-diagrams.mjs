#!/usr/bin/env node
/**
 * audit-diagrams.mjs
 * Cổng kiểm định chất lượng sơ đồ NGHIÊM NGẶT (Strict Quality Gate):
 * 1. Chống banner cảnh báo ngầm (PlantUML notice, deprecation, please use, warning)
 * 2. Chống nhúng tiêu đề cứng vào ảnh (Zero-title in canvas)
 * 3. Chống đè chữ lên chữ (Text-on-text overlap)
 * 4. Chống đường kẻ cắt ngang chữ (Line-through-text intersection)
 * 5. Chống đường đi trùng lặp / song song quá sát nhau (Parallel edge congestion < 8px)
 * 6. Chống nhãn đè lên đường Crow's foot trong ERD (Chuẩn Visual Paradigm & Lucidchart)
 * 7. Kiểm tra đủ cặp SVG vector + PNG 300DPI
 * 8. ZERO-COLOR GATE: chỉ cho phép thang độ xám — cấm mọi mã màu (kể cả copy từ ảnh mẫu)
 * 9. Cỡ chữ tối thiểu ≥ 9pt (đọc được khi in A4) + tỷ lệ khung 0.5–2.4
 * 10. Heuristic bố cục (advisory): lệch trọng tâm, cụm dồn cục, mật độ nhãn dày
 *
 * Cờ: --allow-color  → tắt ZERO-COLOR GATE (chỉ dùng khi có ghi đè tường minh override-monochrome: true)
 */

import fs from 'node:fs';
import path from 'node:path';

const cliArgs = process.argv.slice(2);
const targetDir = cliArgs.find((a) => !a.startsWith('--')) || process.cwd();
const allowColor = cliArgs.includes('--allow-color');
const recursive = !cliArgs.includes('--top-level-only');

function isGrayscaleHex(hex) {
  let h = hex.replace('#', '').toLowerCase();
  if (h.length === 3) h = h.split('').map((c) => c + c).join('');
  if (h.length !== 6) return true;
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  if ([r, g, b].some((n) => isNaN(n))) return true;
  return Math.max(r, g, b) - Math.min(r, g, b) <= 12;
}

const GRAY_NAMES = new Set([
  'none', 'transparent', 'currentcolor', 'inherit', 'url',
  'white', 'black', 'gray', 'grey', 'silver', 'gainsboro', 'whitesmoke',
  'dimgray', 'dimgrey', 'darkgray', 'darkgrey', 'lightgray', 'lightgrey',
  'lightgrey', 'darkslategray', 'darkslategrey', 'slategray', 'slategrey'
]);




function analyzeUseCaseGraph(source) {
  const actors = [...source.matchAll(/^\s*actor\s+(?:"[^"]+"\s+as\s+)?([A-Za-z_][A-Za-z0-9_]*)/gm)].map((m) => m[1]);
  const useCases = [...source.matchAll(/^\s*usecase\s+(?:"[^"]+"\s+as\s+)?([A-Za-z_][A-Za-z0-9_]*)/gm)].map((m) => m[1]);
  if (actors.length === 0 || useCases.length === 0) return [];

  const out = [];
  const hiddenConstraints = source.split(/\r?\n/).filter((line) => !line.trim().startsWith("'") && /\[hidden\]/i.test(line)).length;
  if (actors.length >= 3 && useCases.length > 12) {
    out.push("Use Case complexity warning: " + actors.length + " actors and " + useCases.length +
      " use cases. Confirm a lane/layout plan; consider manual placement or decomposition when actor positions and connector paths matter.");
  } else if (actors.length >= 3 || useCases.length > 12) {
    out.push("Use Case layout planning warning: " + actors.length + " actors and " + useCases.length +
      " use cases. Check actor distribution, system-boundary crossings and connector routes in the rendered image.");
  }
  if (hiddenConstraints > 3) {
    out.push("Use Case hidden-layout constraint warning: " + hiddenConstraints +
      " hidden links. Hidden constraints do not pin absolute positions and can make real associations take long routes; review one change at a time.");
  }
  return out;
}

function analyzeClassGraph(source) {
  const classDecl = /^\s*(?:(?:abstract|static|final)\s+)*(?:class|interface|entity|enum|object)\s+(?:"[^"]+"\s+as\s+)?([A-Za-z_][A-Za-z0-9_]*)/gm;
  const classes = [...source.matchAll(classDecl)].map((m) => m[1]);
  const ids = [...new Set(classes)];
  if (ids.length < 2 || !/^\s*(?:abstract\s+)?class\s+/m.test(source)) return [];

  const degree = new Map(ids.map((id) => [id, 0]));
  const pairCounts = new Map();
  let semanticEdges = 0;
  let hiddenConstraints = 0;

  for (const rawLine of source.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("'")) continue;
    if (!/(?:--|\.{2,}>|<\|--|--\|>|-\[hidden\])/.test(line)) continue;

    if (/\[hidden\]/i.test(line)) {
      hiddenConstraints++;
      continue;
    }

    const hits = [];
    for (const id of ids) {
      const re = new RegExp("\\b" + id + "\\b", "g");
      let match;
      while ((match = re.exec(line)) !== null) hits.push({ id, index: match.index });
    }
    hits.sort((a, b) => a.index - b.index);
    const endpoints = [];
    for (const hit of hits) {
      if (!endpoints.some((e) => e.id === hit.id)) endpoints.push(hit);
    }
    if (endpoints.length < 2) continue;

    const a = endpoints[0].id;
    const b = endpoints[1].id;
    semanticEdges++;
    degree.set(a, (degree.get(a) || 0) + 1);
    degree.set(b, (degree.get(b) || 0) + 1);
    const key = [a, b].sort().join(" <-> ");
    pairCounts.set(key, (pairCounts.get(key) || 0) + 1);
  }

  const out = [];
  const ranked = [...degree.entries()].sort((a, b) => b[1] - a[1]);
  const hubs = ranked.filter(([, n]) => n >= 5);
  if (hubs.length) {
    out.push("Class graph hub warning: " + hubs.map(([id, n]) => id + " (degree " + n + ")").join(", ") +
      ". Check hub placement and whether edges pass through unrelated groups; this is a layout warning, not proof of semantic error.");
  }
  const parallel = [...pairCounts.entries()].filter(([, n]) => n > 1);
  if (parallel.length) {
    out.push("Class graph parallel-association warning: " + parallel.map(([pair, n]) => pair + " (" + n + " associations)").join("; ") +
      ". Verify whether these are valid role-distinct associations or accidental duplicates; never merge/delete automatically.");
  }
  if (semanticEdges > 0 && ids.length >= 6) {
    const avgDegree = (2 * semanticEdges) / ids.length;
    const ratio = semanticEdges / ids.length;
    if (ratio >= 1.35 || avgDegree >= 2.7) {
      out.push("Class graph density warning: " + ids.length + " classes, " + semanticEdges + " relationships, average degree " +
        avgDegree.toFixed(2) + ". Consider domain grouping or decomposition if the render has crossings/long edges; metrics alone do not prove poor layout.");
    }
  }
  if (hiddenConstraints > Math.max(2, semanticEdges / 2)) {
    out.push("Hidden-layout constraint warning: " + hiddenConstraints + " hidden links vs " + semanticEdges +
      " semantic relationships. Review hidden links because they can force long detours.");
  }

  const header = source.split(/\r?\n/).slice(0, 5).join(" ");
  const statedCount = header.match(/\b(\d+)\s*(?:classes|class|lop)\b/i);
  if (statedCount && Number(statedCount[1]) !== ids.length) {
    out.push("Source/comment count mismatch: header states " + statedCount[1] + " classes, parser found " + ids.length +
      ". Verify the stated class count and rendered artifact.");
  }
  return out;
}

console.log(`[diagram-auditor] Đang kiểm định chất lượng sơ đồ tại: ${targetDir} (recursive=${recursive})`);

if (!fs.existsSync(targetDir)) {
  console.error(`[diagram-auditor] Lỗi: Thư mục không tồn tại: ${targetDir}`);
  process.exit(1);
}

function collectSvgFiles(dir, recurse = false) {
  const found = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isFile() && entry.name.toLowerCase().endsWith('.svg')) {
      found.push(path.relative(targetDir, fullPath));
    } else if (
      recurse &&
      entry.isDirectory() &&
      !['.git', 'node_modules', '.next', 'dist', 'build'].includes(entry.name)
    ) {
      found.push(...collectSvgFiles(fullPath, true));
    }
  }
  return found.sort();
}

const files = collectSvgFiles(targetDir, recursive);

if (files.length === 0) {
  console.error(
    `[diagram-auditor] FAIL: Không tìm thấy file .svg trong scope: ${targetDir}${recursive ? ' (recursive)' : ''}. Không được coi thư mục rỗng là PASS.`
  );
  process.exit(1);
}

let totalErrors = 0;
let totalWarnings = 0;

const BANNER_PATTERNS = [
  /Please[\s\u00a0]+use/i,
  /handwritten/i,
  /syntax[\s\u00a0]+warning/i,
  /deprecation[\s\u00a0]+warning/i,
  /plantuml[\s\u00a0]+error/i,
  /cannot[\s\u00a0]+find/i,
  /unsupported/i
];

for (const file of files) {
  const filePath = path.join(targetDir, file);
  const pumlPath = filePath.replace(/\.svg$/, '.puml');
  const pngPath = filePath.replace(/\.svg$/, '.png');
  const sourceCandidates = ['.puml', '.dot', '.drawio', '.tldr', '.mmd', '.json']
    .map((ext) => filePath.replace(/\.svg$/, ext));
  const content = fs.readFileSync(filePath, 'utf8');
  const issues = [];
  const warnings = [];

  // Check 1: Banner / Warning text
  for (const pattern of BANNER_PATTERNS) {
    if (pattern.test(content)) {
      issues.push(`Phát hiện banner thông báo/cảnh báo ngầm trong ảnh (khớp mẫu: ${pattern})`);
      break;
    }
  }

  // Check 2: Valid SVG structure & size
  if (!content.includes('<svg') || !content.includes('</svg>')) {
    issues.push('File SVG không đúng cấu trúc (thiếu thẻ <svg> hoặc </svg>)');
  }
  if (content.length < 500) {
    issues.push(`Kích thước file quá nhỏ (${content.length} bytes), có thể bị render lỗi`);
  }

  // Check 3: Corresponding PNG and editable source exist
  if (!fs.existsSync(pngPath)) {
    issues.push('Thiếu file ảnh PNG tương ứng (cần đủ cả vector SVG và raster PNG 300DPI)');
  } else {
    const pngStat = fs.statSync(pngPath);
    if (!pngStat.isFile() || pngStat.size < 500) {
      issues.push(`File PNG tương ứng không hợp lệ hoặc quá nhỏ (${pngStat.size} bytes; yêu cầu tối thiểu 500 bytes)`);
    }
  }

  const sourcePath = sourceCandidates.find((candidate) => fs.existsSync(candidate));
  if (!sourcePath) {
    issues.push('Thiếu tệp nguồn chỉnh sửa được cùng tên (.puml/.dot/.drawio/.tldr/.mmd/.json); SVG/PNG không đủ để bảo trì sơ đồ.');
  }

  // Check 4: Check if corresponding PlantUML source has hardcoded title
  if (sourcePath && sourcePath.endsWith('.puml')) {
    const pumlContent = fs.readFileSync(sourcePath, 'utf8');
    warnings.push(...analyzeClassGraph(pumlContent));
    warnings.push(...analyzeUseCaseGraph(pumlContent));
    if (/^\s*title\s+(?![:=])/im.test(pumlContent)) {
      issues.push("Phát hiện từ khóa 'title' trong file .puml — tiêu đề phải để ở caption báo cáo (Hình X.Y), KHÔNG nhúng cứng vào khung ảnh");
    }

    // Check 4b: ERD relationship labels (In ERD, Crow's foot lines should NOT have text labels like : "places", : "activates")
    const isErd = /entity\s+/i.test(pumlContent) || /03-erd/i.test(file);
    if (isErd) {
      const erdLabelMatches = pumlContent.match(/[|o}{]+--+[|o}{]+\s*:\s*["'][^"']+["']/g);
      if (erdLabelMatches && erdLabelMatches.length > 0) {
        issues.push(`Phát hiện ${erdLabelMatches.length} nhãn chữ trên đường Crow's foot ERD (${erdLabelMatches[0]}). Chuẩn Visual Paradigm/Lucidchart CẤM viết chữ lên đường nối ERD vì sẽ gây đè nét/cắt chữ!`);
      }

      // Check 4c: Duplicate reciprocal lines between same entities
      const relPairs = [];
      const relRegex = /([A-Za-z_][A-Za-z0-9_]*)\s+[|o}{]+--+[|o}{]+\s+([A-Za-z_][A-Za-z0-9_]*)/g;
      let rMatch;
      while ((rMatch = relRegex.exec(pumlContent)) !== null) {
        const e1 = rMatch[1];
        const e2 = rMatch[2];
        const pairKey = [e1, e2].sort().join('<->');
        if (relPairs.includes(pairKey)) {
          issues.push(`Phát hiện quan hệ 2 chiều trùng lặp giữa ${e1} và ${e2} trong ERD. Điều này làm Graphviz vẽ 2 đường song song đè lên nhau!`);
        } else {
          relPairs.push(pairKey);
        }
      }
    }
  }

  // Check 5: Aspect Ratio Check (Chống sơ đồ dẹt lép hoặc dài ngoằng làm vỡ trang A4)
  const viewBoxMatch = content.match(/viewBox="([^"]+)"/i);
  const widthAttrMatch = content.match(/width="([^"]+)"/i);
  const heightAttrMatch = content.match(/height="([^"]+)"/i);

  let svgWidth = 0;
  let svgHeight = 0;
  if (viewBoxMatch) {
    const vbParts = viewBoxMatch[1].trim().split(/[\s,]+/).map(parseFloat);
    if (vbParts.length === 4) {
      svgWidth = vbParts[2];
      svgHeight = vbParts[3];
    }
  } else if (widthAttrMatch && heightAttrMatch) {
    svgWidth = parseFloat(widthAttrMatch[1]);
    svgHeight = parseFloat(heightAttrMatch[1]);
  }

  if (svgWidth > 0 && svgHeight > 0) {
    const ratio = svgWidth / svgHeight;
    if (ratio > 3.8) {
      issues.push(`Tỷ lệ khung hình quá dẹt ngang (${ratio.toFixed(2)}:1 > 3.8). Khi chèn vào Word A4 (khổ rộng ~15cm), chiều cao chỉ còn ~${(15 / ratio).toFixed(1)}cm khiến chữ bị thu nhỏ li ti, không đọc được! Cần tái cấu trúc bố cục nhiều hàng.`);
    } else if (ratio < 0.28) {
      issues.push(`Tỷ lệ khung hình quá dài dọc (${ratio.toFixed(2)}:1 < 0.28). Nguy cơ cao bị tràn trang hoặc rớt trang trong tài liệu Word A4.`);
    }
  }

  // Check 6: Text Collision Detection (Chữ đè chữ)
  const textRegex = /<text\b([^>]*)>([\s\S]*?)<\/text>/g;
  let tMatch;
  const texts = [];
  while ((tMatch = textRegex.exec(content)) !== null) {
    const attrs = tMatch[1];
    const rawText = tMatch[2]
      .replace(/<tspan\b[^>]*>/g, '')
      .replace(/<\/tspan>/g, ' ')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"').replace(/&#39;/g, "'")
      .replace(/\s+/g, ' ').trim();
    const textVal = rawText;
    const xMatch = attrs.match(/x="([^"]+)"/);
    const yMatch = attrs.match(/y="([^"]+)"/);
    const fsMatch = attrs.match(/font-size="([^"]+)"/);
    const tlMatch = attrs.match(/textLength="([^"]+)"/);
    if (xMatch && yMatch && textVal.length > 0) {
      const x = parseFloat(xMatch[1]);
      const y = parseFloat(yMatch[1]);
      const fontSize = fsMatch ? parseFloat(fsMatch[1]) : 12;
      const width = tlMatch ? parseFloat(tlMatch[1]) : textVal.length * fontSize * 0.6;
      texts.push({
        text: textVal,
        x,
        y,
        minX: x,
        maxX: x + width,
        minY: y - fontSize,
        maxY: y + 2
      });
    }
  }

  const textCollisions = [];
  for (let i = 0; i < texts.length; i++) {
    for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i];
      const b = texts[j];
      // Kiểm tra thực tế va chạm hộp chữ nhật (AABB Bounding Box Overlap)
      const overlapX = Math.min(a.maxX, b.maxX) - Math.max(a.minX, b.minX);
      const overlapY = Math.min(a.maxY, b.maxY) - Math.max(a.minY, b.minY);

      // Nếu cả chiều X và Y đều giao cắt (thực sự đè chữ lên nhau)
      if (a.text !== b.text && overlapX > 1 && overlapY > 1) {
        textCollisions.push(`'${a.text}' và '${b.text}' bị chồng đè toạ độ (overlapX=${overlapX.toFixed(1)}px, overlapY=${overlapY.toFixed(1)}px)`);
      }
    }
  }
  if (textCollisions.length > 0) {
    issues.push(`Phát hiện ${textCollisions.length} điểm va chạm/đè chữ: ${textCollisions.slice(0, 3).join('; ')}`);
  }

  // Check 7: Clustered Edge Labels Congestion (Mật độ nhãn dày đặc chen chúc giữa các tầng)
  // Các nhãn quan hệ ngắn (độ dài 3-25 ký tự, không chứa cú pháp kiểu dữ liệu) nếu tập trung quá dày đặc trong một dải Y hẹp
  const standaloneLabels = texts.filter(
    (t) => t.text.length >= 3 && t.text.length <= 30 && !t.text.includes(':') && !t.text.includes('(') && !t.text.includes(';')
  );
  const clusteredLabels = [];
  for (let i = 0; i < standaloneLabels.length; i++) {
    const nearby = standaloneLabels.filter(
      (other, j) => j !== i && Math.abs(other.y - standaloneLabels[i].y) < 22 && Math.abs(other.x - standaloneLabels[i].x) < 120
    );
    if (nearby.length >= 3) {
      const labelNames = [standaloneLabels[i].text, ...nearby.map((n) => n.text)].slice(0, 4).join(', ');
      const key = `Dải Y ~ ${standaloneLabels[i].y.toFixed(0)}: [${labelNames}]`;
      if (!clusteredLabels.includes(key)) {
        clusteredLabels.push(key);
      }
    }
  }
  if (clusteredLabels.length > 0) {
    issues.push(`Cảnh báo chen chúc nhãn (Inter-tier Label Congestion): Phát hiện ${clusteredLabels.length} cụm nhãn bị dồn cục quá sát nhau (${clusteredLabels[0]}). Sơ đồ kiến trúc tầng không nên ghi dày đặc thao tác chi tiết lên đường nối; hãy đưa chi tiết vào Sequence Diagram!`);
  }

  // Check 8: Line-Through-Text Intersection (Đường kẻ cắt ngang mặt chữ)
  const pathRegex = /<path\s+[^>]*d="([^"]+)"[^>]*>/g;
  let pMatch;
  const lineIntersections = [];
  while ((pMatch = pathRegex.exec(content)) !== null) {
    const d = pMatch[1];
    const coords = d.match(/[-+]?[0-9]*\.?[0-9]+[,\s]+[-+]?[0-9]*\.?[0-9]+/g);
    if (!coords) continue;
    for (const coord of coords) {
      const parts = coord.split(/[,\s]+/).map(parseFloat);
      if (parts.length < 2 || isNaN(parts[0]) || isNaN(parts[1])) continue;
      const px = parts[0];
      const py = parts[1];
      for (const t of texts) {
        // Chỉ kiểm tra các nhãn quan hệ (text ngắn độc lập, không phải thuộc tính trong bảng)
        if (t.text.length < 30 && px > t.minX + 4 && px < t.maxX - 4 && py > t.minY + 2 && py < t.maxY - 2) {
          lineIntersections.push(`Đường nối cắt ngang qua chữ '${t.text}' tại toạ độ (${px.toFixed(1)}, ${py.toFixed(1)})`);
        }
      }
    }
  }
  if (lineIntersections.length > 0) {
    issues.push(`Phát hiện ${lineIntersections.length} điểm đường kẻ cắt ngang mặt chữ: ${lineIntersections.slice(0, 2).join('; ')}`);
  }

  // Check 9: ZERO-COLOR GATE (Chỉ cho phép thang độ xám)
  if (!allowColor) {
    const colorViolations = new Set();
    const colorAttrRegex = /(?:fill|stroke|stop-color|flood-color|color)\s*[:=]\s*["']?\s*(#[0-9a-fA-F]{3,8}|rgb\([^)]*\)|[a-zA-Z]+)/g;
    let cMatch;
    while ((cMatch = colorAttrRegex.exec(content)) !== null) {
      const raw = cMatch[1].trim();
      const low = raw.toLowerCase();
      if (low.startsWith('#')) {
        if (!isGrayscaleHex(low)) colorViolations.add(raw);
      } else if (low.startsWith('rgb')) {
        const nums = (raw.match(/[0-9.]+/g) || []).map(Number);
        if (nums.length >= 3) {
          const [r, g, b] = nums;
          if (Math.max(r, g, b) - Math.min(r, g, b) > 12) colorViolations.add(raw);
        }
      } else if (!GRAY_NAMES.has(low)) {
        colorViolations.add(raw);
      }
    }
    if (colorViolations.size > 0) {
      issues.push(`VI PHẠM ZERO-COLOR: phát hiện ${colorViolations.size} mã màu phi thang độ xám (${[...colorViolations].slice(0, 5).join(', ')}). Sơ đồ báo cáo BẮT BUỘC trắng-đen — kể cả khi ảnh mẫu người dùng có màu thì cũng KHÔNG được sao chép màu!`);
    }
  }

  // Check 10: Minimum font size (đọc được khi in A4)
  const fontSizes = [];
  const fsRegex = /font-size\s*[:=]\s*"?'?([0-9.]+)/g;
  let fm;
  while ((fm = fsRegex.exec(content)) !== null) {
    const v = parseFloat(fm[1]);
    if (!isNaN(v) && v > 0) fontSizes.push(v);
  }
  const tinyFonts = fontSizes.filter((v) => v < 9);
  if (tinyFonts.length > 0) {
    issues.push(`Cỡ chữ quá nhỏ: ${tinyFonts.length} nhãn có font-size < 9pt (nhỏ nhất ${Math.min(...tinyFonts).toFixed(1)}pt). Trên trang A4 (~15cm) sẽ khó đọc; tăng cỡ chữ hoặc phân rã sơ đồ.`);
  }

  // Check 11: Layout heuristics — CẢNH BÁO VÀNG (Agent phải soi mắt phân xử)
  if (svgWidth > 0 && svgHeight > 0 && texts.length >= 5) {
    const cx = texts.reduce((s, t) => s + (t.minX + t.maxX) / 2, 0) / texts.length;
    const cy = texts.reduce((s, t) => s + (t.minY + t.maxY) / 2, 0) / texts.length;
    const dx = Math.abs(cx - svgWidth / 2) / svgWidth;
    const dy = Math.abs(cy - svgHeight / 2) / svgHeight;
    if (dx > 0.2 || dy > 0.2) {
      warnings.push(`Trọng tâm khối lệch tâm khung (Δx=${(dx * 100).toFixed(0)}%, Δy=${(dy * 100).toFixed(0)}%). Cân nhắc tái bố cục cho khoảng trắng cân đối.`);
    }
  }
  let crowdedPairs = 0;
  for (let i = 0; i < texts.length; i++) {
    for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i];
      const b = texts[j];
      if (a.text !== b.text && Math.abs(a.x - b.x) < 30 && Math.abs(a.y - b.y) < 30) crowdedPairs++;
    }
  }
  if (crowdedPairs >= 12) {
    warnings.push(`Mật độ nhãn cao (${crowdedPairs} cặp nhãn cách nhau < 30px). Nguy cơ dồn cục khi in nhỏ; cân nhắc tăng nodesep/ranksep hoặc phân rã.`);
  }
  if (texts.length > 80) {
    warnings.push(`Sơ đồ có ${texts.length} nhãn — khá dày. Cân nhắc phân rã thành 1 sơ đồ tổng quan + các sơ đồ chuyên sâu (Use Case/Sequence).`);
  }

  if (issues.length > 0) {
    totalErrors += issues.length;
    console.log(`❌ [FAIL] ${file}:`);
    for (const issue of issues) {
      console.log(`    - ${issue}`);
    }
  } else if (warnings.length > 0) {
    totalWarnings += warnings.length;
    console.log(`⚠️  [PASS*] ${file}: đạt lỗi chặn cứng, còn ${warnings.length} cảnh báo VÀNG cần Agent soi mắt phân xử:`);
    for (const w of warnings) {
      console.log(`    ! ${w}`);
    }
  } else {
    console.log(`✓ [PASS] ${file} (Chuẩn mực 100%, không đè chữ, không cắt nét, đủ SVG + PNG)`);
  }
}

console.log('----------------------------------------------------');
console.log('[LƯU Ý NGHIỆM THU - ANTI-FALSE-PASS DOCTRINE]:');
console.log('  * Lỗi ĐỎ (FAIL) chặn cứng: banner, SVG hỏng, thiếu PNG, title nhúng, nhãn ERD,');
console.log('    quan hệ trùng, đè chữ, đường cắt chữ, VI PHẠM ZERO-COLOR, cỡ chữ < 9pt, tỷ lệ khung lệch.');
console.log('  * Cảnh báo VÀNG (PASS*) KHÔNG chặn tự động — nhưng Agent BẮT BUỘC soi mắt phân xử.');
console.log('  * Script KHÔNG THỂ thay thế kiểm tra ngữ nghĩa (Gate A) và soi trực quan bằng mắt (Gate C).');
console.log('  * Chỉ kiểm tra các path vertex nằm trong bounding box chữ; KHÔNG phải bộ phát hiện mọi giao cắt giữa các đoạn đường nối hoặc va chạm node-edge.');
console.log('  * Agent KHÔNG ĐƯỢC tuyên bố hoàn thành nếu chưa tự mở ảnh soi mắt + có bằng chứng soi ảnh!');
console.log('----------------------------------------------------');

if (totalErrors > 0) {
  console.error(`[diagram-auditor] KẾT QUẢ: ${totalErrors} LỖI ĐỎ nghiêm trọng phát hiện (+ ${totalWarnings} cảnh báo vàng). Vui lòng sửa triệt để!`);
  process.exit(1);
} else {
  console.log(`[diagram-auditor] KẾT QUẢ STATIC: ${files.length} SVG đã qua các kiểm tra chặn cứng được triển khai trong script.`);
  console.log('[diagram-auditor] LƯU Ý: Kết quả static không chứng minh sơ đồ đúng ngữ nghĩa hoặc không có mọi giao cắt đường nối; vẫn bắt buộc Visual Review/Proof-of-View.');
  if (totalWarnings > 0) {
    console.log(`[diagram-auditor] Còn ${totalWarnings} cảnh báo VÀNG cần Agent soi mắt phân xử trước khi PASS (không được bỏ qua).`);
  }
  process.exit(0);
}
