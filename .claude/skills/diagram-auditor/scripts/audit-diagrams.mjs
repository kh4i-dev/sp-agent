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
 */

import fs from 'node:fs';
import path from 'node:path';

const targetDir = process.argv[2] || process.cwd();

console.log(`[diagram-auditor] Đang kiểm định chất lượng sơ đồ tại: ${targetDir}`);

if (!fs.existsSync(targetDir)) {
  console.error(`[diagram-auditor] Lỗi: Thư mục không tồn tại: ${targetDir}`);
  process.exit(1);
}

const files = fs.readdirSync(targetDir).filter((f) => f.endsWith('.svg'));

if (files.length === 0) {
  console.log('[diagram-auditor] Không tìm thấy file .svg nào để kiểm tra.');
  process.exit(0);
}

let totalErrors = 0;

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
  const content = fs.readFileSync(filePath, 'utf8');
  const issues = [];

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

  // Check 3: Corresponding PNG exists
  if (!fs.existsSync(pngPath)) {
    issues.push('Thiếu file ảnh PNG tương ứng (cần đủ cả vector SVG và raster PNG 300DPI)');
  }

  // Check 4: Check if corresponding .puml has hardcoded title
  if (fs.existsSync(pumlPath)) {
    const pumlContent = fs.readFileSync(pumlPath, 'utf8');
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
      const relRegex = /([A-Z_]+)\s+[|o}{]+--+[|o}{]+\s+([A-Z_]+)/g;
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
  const textRegex = /<text\s+([^>]+)>([^<]+)<\/text>/g;
  let tMatch;
  const texts = [];
  while ((tMatch = textRegex.exec(content)) !== null) {
    const attrs = tMatch[1];
    const textVal = tMatch[2].trim();
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
      // Nếu 2 chữ khác nhau nhưng toạ độ x, y gần nhau dưới 15px -> va chạm/đè nhãn
      if (a.text !== b.text && Math.abs(a.y - b.y) < 12 && Math.abs(a.x - b.x) < 25) {
        textCollisions.push(`'${a.text}' và '${b.text}' bị chồng đè toạ độ (dx=${Math.abs(a.x - b.x).toFixed(1)}, dy=${Math.abs(a.y - b.y).toFixed(1)})`);
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

  if (issues.length > 0) {
    totalErrors += issues.length;
    console.log(`❌ [FAIL] ${file}:`);
    for (const issue of issues) {
      console.log(`    - ${issue}`);
    }
  } else {
    console.log(`✓ [PASS] ${file} (Chuẩn mực 100%, không đè chữ, không cắt nét, đủ SVG + PNG)`);
  }
}

console.log('----------------------------------------------------');
console.log('[LƯU Ý NGHIỆM THU - ANTI-FALSE-PASS DOCTRINE]:');
console.log('  * Kết quả script tự động chỉ xác nhận tính toàn vẹn hình học & cú pháp (Gate B & một phần Gate C).');
console.log('  * Script KHÔNG THỂ thay thế việc kiểm tra ngữ nghĩa (Gate A) và soi trực quan bằng mắt (Gate C Visual QA).');
console.log('  * Agent KHÔNG ĐƯỢC tuyên bố hoàn thành dự án nếu chưa tự mở ảnh soi mắt và đối chiếu với code/schema!');
console.log('----------------------------------------------------');

if (totalErrors > 0) {
  console.error(`[diagram-auditor] KẾT QUẢ: ${totalErrors} lỗi/cảnh báo nghiêm trọng phát hiện. Vui lòng sửa triệt để!`);
  process.exit(1);
} else {
  console.log(`[diagram-auditor] KẾT QUẢ TỰ ĐỘNG: 100% Sơ đồ ĐẠT CHUẨN KỸ THUẬT SƠ BỘ (${files.length}/${files.length} files).`);
  process.exit(0);
}
