"""Read-only adversarial audit of the handdrawn SVG checker."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
MODULE=ROOT/'.claude/skills/handdrawn-diagrams/scripts/audit_svg.py'
spec=importlib.util.spec_from_file_location('auditor_under_review',MODULE)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
OUT=ROOT/'docs/analysis/handdrawn-skill-audit-2026-11-02'
OUT.mkdir(parents=True,exist_ok=True)
cases={
 'halo_text_overlap':('<text x="20" y="60" font-size="20" paint-order="stroke" stroke="white">SAME LABEL</text><text x="20" y="60" font-size="20" paint-order="stroke" stroke="white">SAME LABEL</text>','E2'),
 'transformed_outside_canvas':('<g transform="translate(500 0)"><text x="20" y="60">OUTSIDE</text></g>','E1'),
 'nonfinite_line':('<text x="20" y="60">OK</text><line x1="NaN" y1="100" x2="200" y2="100" stroke="black"/>','E6'),
 'white_label_background_below_later_line':('<rect x="10" y="30" width="160" height="50" fill="white"/><text x="20" y="60" font-size="20">LABEL</text><line x1="0" y1="55" x2="300" y2="55" stroke="black"/>','E3'),
 'shape_outside_canvas':('<text x="20" y="60">OK</text><rect x="390" y="200" width="100" height="50" stroke="black" fill="none"/>','E1'),
}
rows=[]
for name,(body,expected) in cases.items():
 p=OUT/(name+'.svg')
 p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">'+body+'</svg>',encoding='utf-8')
 result=mod.audit(p)
 codes={x['code'] for x in result['errors']}
 rows.append(dict(case=name,expected=expected,detected=expected in codes,errors=result['errors'],warnings=result['warnings']))
 print(name,'DETECTED' if expected in codes else 'MISSED', 'errors=',len(result['errors']),'warnings=',len(result['warnings']))
(OUT/'probes.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
