#!/usr/bin/env node
/**
 * run-evals.mjs — Test Runner cho Diagram Benchmark Evals
 * Tự động chạy render và kiểm định toàn bộ các ca kiểm thử trong evals/
 */

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillDir = path.resolve(__dirname, '..');
const evalsDir = path.resolve(skillDir, 'evals');

console.log('====================================================');
console.log('🚀 ĐANG CHẠY BỘ KIỂM THỬ SƠ ĐỒ (DIAGRAM BENCHMARK EVALS)');
console.log('====================================================');

const testCases = [
  { id: 'EVAL-01', name: '01_long_labels', file: 'test.dot', type: 'dot' },
  { id: 'EVAL-02', name: '02_nested_packages', file: 'test.puml', type: 'puml' },
  { id: 'EVAL-03', name: '03_crowded_erd', file: 'test.puml', type: 'puml' },
  { id: 'EVAL-04', name: '04_balanced_trie', file: 'test.dot', type: 'dot' },
  { id: 'EVAL-05', name: '05_sequence_a4', file: 'test.puml', type: 'puml' },
];

let totalPass = 0;
let totalFail = 0;

for (const tc of testCases) {
  const tcDir = path.join(evalsDir, tc.name);
  const sourcePath = path.join(tcDir, tc.file);

  if (!fs.existsSync(sourcePath)) {
    console.log(`❌ [${tc.id}] Không tìm thấy file: ${sourcePath}`);
    totalFail++;
    continue;
  }

  console.log(`\n▶ Đang chạy [${tc.id}: ${tc.name}]...`);

  // 1. Render file
  try {
    if (tc.type === 'dot') {
      const renderScript = path.join(__dirname, 'render-graphviz.mjs');
      execSync(`node "${renderScript}" --in "${sourcePath}"`, { stdio: 'pipe' });
    } else {
      const renderScript = path.resolve(skillDir, '../plantuml-diagrams/scripts/render-puml.mjs');
      execSync(`node "${renderScript}" --in "${sourcePath}"`, { stdio: 'pipe' });
    }
  } catch (err) {
    console.error(`  ❌ Lỗi render file ${tc.file}:`, err.message);
    totalFail++;
    continue;
  }

  // 2. Chạy diagram-auditor
  try {
    const auditorScript = path.resolve(skillDir, '../diagram-auditor/scripts/audit-diagrams.mjs');
    execSync(`node "${auditorScript}" "${tcDir}"`, { stdio: 'pipe' });
    console.log(`  ✅ [PASS] ${tc.id}: Vượt qua kiểm định chất lượng 100%!`);
    totalPass++;
  } catch (err) {
    console.error(`  ❌ [FAIL] ${tc.id}: Thất bại ở cổng audit!`);
    totalFail++;
  }
}

console.log('\n====================================================');
console.log(`📊 TỔNG KẾT BENCHMARK: ${totalPass}/${testCases.length} ĐẠT (PASS)`);
if (totalFail === 0) {
  console.log('🎉 100% SƠ ĐỒ ĐẠT CHUẨN THIẾT KẾ & THẨM MỸ!');
  process.exit(0);
} else {
  console.error(`⚠️ Có ${totalFail} bài test thất bại. Cần rà soát lại!`);
  process.exit(1);
}
