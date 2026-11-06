import { createRequire } from 'node:module';
import fs from 'node:fs/promises';
import path from 'node:path';
const require=createRequire(import.meta.url);
const {chromium}=require('C:/Users/My PC/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve('docs/diagrams/btl-cnpm-state-redraw');
const file=path.join(root,'images/diagrams/state-01-don-hang.svg');
const svg=await fs.readFile(file,'utf8');
const spec=JSON.parse(await fs.readFile(path.join(root,'diagrams/state-01-don-hang.json'),'utf8'));
const browser=await chromium.launch({channel:'chrome',headless:true});
try {
 const page=await browser.newPage({viewport:{width:1480,height:1030},deviceScaleFactor:2});
 await page.setContent(`<html><head><meta charset="utf-8"><style>html,body{margin:0;background:white;}svg{display:block}</style></head><body>${svg}</body></html>`);
 await page.evaluate(()=>document.fonts.ready);
 await page.screenshot({path:file.replace('.svg','.png')});
 const text=await page.locator('text').evaluateAll(es=>es.map(e=>({text:e.textContent,...(()=>{const b=e.getBBox();return {x:b.x,y:b.y,w:b.width,h:b.height}})()})));
 await fs.writeFile(path.join(root,'audit/text-boxes.json'),JSON.stringify(text,null,2));
 const wanted=[...spec.nodes.flatMap(n=>n.label?n.label.split('\n'):[]),...spec.edges.flatMap(e=>e.label?e.label.split('\n'):[])].sort();
 if(JSON.stringify(wanted)!==JSON.stringify(text.map(t=>t.text).sort()))throw Error('Canvas contains missing/extra text');
 const collisions=[];
 for(const t of text)for(const e of spec.edges)for(let i=1;i<e.points.length;i++){
   const [a,b]=[e.points[i-1],e.points[i]];
   const hit=a[0]===b[0]?a[0]>t.x+1&&a[0]<t.x+t.w-1&&Math.max(a[1],b[1])>t.y+1&&Math.min(a[1],b[1])<t.y+t.h-1:
     a[1]>t.y+1&&a[1]<t.y+t.h-1&&Math.max(a[0],b[0])>t.x+1&&Math.min(a[0],b[0])<t.x+t.w-1;
   if(hit)collisions.push({text:t.text,edge:e.id});
 }
 if(collisions.length)throw Error(JSON.stringify(collisions));
 const fontMin=await page.locator('text').evaluateAll(es=>Math.min(...es.map(e=>parseFloat(getComputedStyle(e).fontSize))));
 const qa={textCount:text.length,noExtraAnnotations:true,textEdgeCollisions:collisions,minFontPx:fontMin,insertWidthCm:25,minPrintPt:fontMin*25/1480*72/2.54};
 if(qa.minPrintPt<9)throw Error('Font below print target');
 await fs.writeFile(path.join(root,'audit/chromium-check.json'),JSON.stringify(qa,null,2));
 const crops=path.join(root,'audit/soi-so-do/round3/chromium-crops');await fs.mkdir(crops,{recursive:true});
 for(const [name,x,y,width,height]of [['top',0,55,1480,240],['middle',350,310,1110,365],['bottom',360,650,1100,365]])await page.screenshot({path:path.join(crops,name+'.png'),clip:{x,y,width,height}});
 console.log(`Rendered ${file.replace('.svg','.png')}; ${text.length} structural text labels`);
} finally {await browser.close();}
