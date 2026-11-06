"""Regenerate the declared Order model. See state-01-don-hang-audit.md.
No notes or explanatory text are emitted on the canvas.
"""
from pathlib import Path
import json
import re
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
spec=HERE/'state-01-don-hang.json'
model=json.loads(spec.read_text(encoding='utf-8'))
block=(PROJECT/'backend/src/common/enums.ts').read_text(encoding='utf-8').split('export const ORDER_TRANSITIONS:')[1].split('\n};')[0]
pairs=set()
for src,targets in re.findall(r'\[OrderStatus\.(\w+)\]:\s*\[([^\]]*)\]',block):
    pairs.update((src,t) for t in re.findall(r'OrderStatus\.(\w+)',targets))
if pairs!={tuple(p) for p in model['expected_pairs']}:
    raise SystemExit('ORDER_TRANSITIONS changed: review the model and audit before rendering')
renderer=HERE.parent/'tools/render_state_model.py'
stem=HERE/'svg/state-01-don-hang'
subprocess.run([sys.executable,str(renderer),str(spec),'--out',str(stem)],check=True)
shutil.move(str(stem.with_suffix('.drawio')),HERE/'drawio/state-01-don-hang.drawio')
subprocess.run(['node',str(HERE/'render_state.mjs')],check=True)
shutil.copy2(stem.with_suffix('.svg'),HERE.parent/'images/diagrams/state-01-don-hang.svg')
shutil.copy2(HERE.parent/'images/diagrams/state-01-don-hang.png',HERE.parent/'images/diagrams/state-preview.png')
print('Regenerated declared view only; rerun visual review after any model change.')
