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
  { id: 'EVAL-06', name: '06_class_rutgon_hub', file: 'test.puml', type: 'puml', expectWarnings: ['Class graph hub warning', 'parallel-association warning', 'Source/comment count mismatch'] },
  { id: 'EVAL-07', name: '07_use_case_multi_actor', file: 'test.puml', type: 'puml', expectWarnings: ['Use Case complexity warning', 'Use Case hidden-layout constraint warning'] },
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
    const auditOutput = execSync(`node "${auditorScript}" "${tcDir}"`, { encoding: 'utf8', stdio: 'pipe' });
    const missingExpectedWarnings = (tc.expectWarnings || []).filter((warning) => !auditOutput.includes(warning));
    if (missingExpectedWarnings.length > 0) {
      console.error(`  ❌ [FAIL] ${tc.id}: Không phát hiện warning regression mong đợi: ${missingExpectedWarnings.join(', ')}`);
      totalFail++;
      continue;
    }
    if (auditOutput.includes('[PASS*]')) {
      console.log(`  ⚠️ [STATIC-GATE PASS*] ${tc.id}: Qua hard checks nhưng còn warning; cần Visual Review riêng.`);
    } else {
      console.log(`  ✅ [STATIC-GATE PASS] ${tc.id}: Qua các kiểm tra tĩnh trong auditor; chưa phải chứng nhận thị giác/ngữ nghĩa.`);
    }
    totalPass++;
  } catch (err) {
    const details = err.stdout ? String(err.stdout).slice(-1200) : err.message;
    console.error(`  ❌ [FAIL] ${tc.id}: Static audit thất bại. ${details}`);
    totalFail++;
  }
}

console.log('\n====================================================');
console.log(`📊 TỔNG KẾT STATIC GATE: ${totalPass}/${testCases.length} bài qua kiểm tra tĩnh`);
console.log('⚠️ Đây KHÔNG phải kết luận “100% thẩm mỹ” hoặc Visual PASS.');
console.log('   Reviewer vẫn phải mở từng PNG ở kích thước đọc được, đối chiếu mô hình/ngữ nghĩa và ghi Proof-of-View.');
if (totalFail === 0) {
  console.log('✅ Các ca kiểm tra tĩnh trong runner đã qua.');
  process.exit(0);
} else {
  console.error(`❌ Có ${totalFail} bài test thất bại; chưa được nghiệm thu.`);
  process.exit(1);
}
