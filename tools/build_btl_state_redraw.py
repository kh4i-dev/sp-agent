"""Prepare the declared order lifecycle and evidence without changing btl-cnpm."""
from pathlib import Path
import json, re, shutil, subprocess, sys, hashlib

REPO=Path(__file__).resolve().parents[1]
PROJECT=Path('E:/HOC TAP/my-project/btl-cnpm')
PACK=REPO/'docs/diagrams/btl-cnpm-state-redraw'
for folder in ['diagrams','images/diagrams','domain','audit/soi-so-do','tools']:
    (PACK/folder).mkdir(parents=True,exist_ok=True)
source=PROJECT/'backend/src/common/enums.ts'
block=source.read_text(encoding='utf-8').split('export const ORDER_TRANSITIONS:')[1].split('\n};')[0]
pairs=[]
for src,targets in re.findall(r'\[OrderStatus\.(\w+)\]:\s*\[([^\]]*)\]',block):
    pairs.extend([src,t] for t in re.findall(r'OrderStatus\.(\w+)',targets))
nodes=[]
def n(key,label,x,y,w=220,h=76,kind='state',parent=None):
    node=dict(id=key,label=label,x=x,y=y,w=w,h=h,kind=kind,evidence='backend/src/common/enums.ts:17-38')
    if parent: node['parent']=parent
    nodes.append(node)
n('pre','Trước vận chuyển',70,70,1010,220,'composite')
n('post','Sau giao hàng',790,390,650,240,'composite')
n('PendingPayment','Chờ thanh toán',160,160,parent='pre')
n('Paid','Đã thanh toán',500,160,parent='pre')
n('Packed','Đã đóng gói',830,160,parent='pre')
n('Shipping','Đang giao',1210,160)
n('Delivered','Đã giao',1210,490,parent='post')
n('DeliveredVerified','Đã xác thực',820,490,parent='post')
n('Cancelled','Đã hủy',390,490)
n('Completed','Hoàn tất',1100,820)
n('Returned','Trả hàng',390,820)
n('initial','',10,184,28,28,'initial')
n('final_cancel','',484,666,32,32,'final')
n('final_return','',484,966,32,32,'final')
edges=[]
def e(key,src,dst,points,label='',at=None,shared=False):
    edge=dict(id=key,source=src,target=dst,points=points,evidence='backend/src/common/enums.ts:28-38')
    if label: edge.update(trigger=label,label=label,label_at=at)
    if shared: edge['shared_exit_verified']=True
    edges.append(edge)
e('init','initial','PendingPayment',[(38,198),(160,198)])
e('payment','PendingPayment','Paid',[(380,198),(500,198)],'thanh toán', [440,143])
e('pack','Paid','Packed',[(720,198),(830,198)],'đóng gói',[775,143])
e('pickup','Packed','Shipping',[(1050,198),(1210,198)],'nhận kiện',[1155,143])
e('deliver','Shipping','Delivered',[(1320,236),(1320,490)],'giao thành công',[1170,355])
e('verify','Delivered','DeliveredVerified',[(1210,528),(1040,528)],'xác thực tem',[1125,479])
e('cancel','pre','Cancelled',[(500,290),(500,490)],'hủy đơn',[370,398],True)
e('release','post','Completed',[(1210,630),(1210,820)],'giải ngân\nthành công',[1340,705],True)
e('return_verified','DeliveredVerified','Returned',[(930,566),(930,745),(500,745),(500,820)],'chấp thuận trả hàng',[715,719])
e('return_completed','Completed','Returned',[(1100,858),(610,858)],'chấp thuận trả hàng',[855,834])
e('finish_cancel','Cancelled','final_cancel',[(500,566),(500,666)])
e('finish_return','Returned','final_return',[(500,896),(500,966)])
m=dict(view='declared',width=1480,height=1030,nodes=nodes,edges=edges,expected_pairs=pairs)
(PACK/'diagrams/state-01-don-hang.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
renderer=REPO/'.claude/skills/plantuml-diagrams/scripts/render_state_model.py'
shutil.copy2(renderer,PACK/'tools/render_state_model.py')
subprocess.run([sys.executable,str(renderer),str(PACK/'diagrams/state-01-don-hang.json'),'--out',str(PACK/'images/diagrams/state-01-don-hang')],check=True)
shutil.move(str(PACK/'images/diagrams/state-01-don-hang.drawio'),PACK/'diagrams/state-01-don-hang.drawio')
files=['private-docs/diagrams/gen_state_svg.py','private-docs/diagrams/svg/state-01-don-hang.svg','private-docs/diagrams/drawio/state-01-don-hang.drawio','private-docs/images/diagrams/state-01-don-hang.png']
(PACK/'audit/baseline-hashes.json').write_text(json.dumps({f:hashlib.sha256((PROJECT/f).read_bytes()).hexdigest() for f in files},indent=2),encoding='utf-8')
print(PACK)
