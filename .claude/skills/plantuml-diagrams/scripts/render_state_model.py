"""Render an explicitly positioned state model to SVG and editable drawio.

No auto-layout, notes or decorative text. Geometry and semantic checks are
necessary checks, never a replacement for rendered visual review.
"""
import argparse
import math
import re
import json
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(m):
    require(m['view'] in ('declared', 'as-is', 'to-be'), 'Choose evidence scope')
    require(not any(k in m for k in ('note', 'notes', 'legend', 'title', 'footer')), 'No annotations on canvas')
    def finite(v):
        return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
    require(all(finite(m.get(k)) and m[k] > 0 for k in ('width', 'height')), 'Canvas needs positive finite width/height')
    all_ids = [n['id'] for n in m['nodes']] + [e['id'] for e in m['edges']]
    require(all(isinstance(key, str) and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.:-]*', key) for key in all_ids), 'Use safe named IDs, never reserved drawio IDs 0/1')
    nodes = {n['id']: n for n in m['nodes']}
    require(any(n['kind'] == 'state' for n in nodes.values()), 'Model needs at least one concrete state')
    require(len(nodes) == len(m['nodes']), 'Duplicate node id')
    ids = set(nodes)
    edge_ids = [e['id'] for e in m['edges']]
    require(len(set(edge_ids)) == len(edge_ids) and not ids.intersection(edge_ids), 'Duplicate edge id')
    for n in nodes.values():
        require(n['kind'] in ('state', 'composite', 'initial', 'final'), 'Invalid state model')
        require(n.get('parent') is None or nodes[n['parent']]['kind'] == 'composite', 'Invalid state model')
        require(n['w'] > 0 and n['h'] > 0, 'Invalid state model')
        if n['kind'] in ('state', 'composite'):
            require(n.get('label') and n.get('evidence'), 'State needs label and evidence')
    for n in nodes.values():
        chain = {n['id']}
        parent_key = n.get('parent')
        while parent_key is not None:
            require(parent_key in nodes and parent_key not in chain, 'Missing parent or cyclic hierarchy')
            chain.add(parent_key)
            parent_key = nodes[parent_key].get('parent')
        require(all(finite(n.get(k)) for k in ('x', 'y', 'w', 'h')), 'Node coordinates must be finite numbers')
        require(n['x'] >= 0 and n['y'] >= 0 and n['x']+n['w'] <= m['width'] and n['y']+n['h'] <= m['height'], 'Node outside canvas')
        if n.get('parent'):
            parent = nodes[n['parent']]
            require(parent['x'] <= n['x'] and parent['y'] <= n['y'] and n['x']+n['w'] <= parent['x']+parent['w'] and n['y']+n['h'] <= parent['y']+parent['h'], 'Child outside parent composite')
        if n['kind'] in ('initial', 'final'):
            require(n['w'] == n['h'] and n['w'] > 12, 'Initial/final must be circular and large enough')
        if n['kind'] == 'composite':
            require(any(x.get('parent') == n['id'] and x['kind'] in ('state', 'composite') for x in nodes.values()), 'Empty composite unsupported')
    def leaves(key):
        kids = [x['id'] for x in nodes.values() if x.get('parent') == key]
        return sum((leaves(k) for k in kids if nodes[k]['kind'] in ('state', 'composite')), []) if kids else [key]
    expanded = set()
    for e in m['edges']:
        src, dst = nodes[e['source']], nodes[e['target']]
        require(src['kind'] != 'final', 'FinalState cannot have outgoing transitions')
        require(dst['kind'] != 'initial', 'Initial cannot have incoming transitions')
        require(len(e['points']) >= 2 and e.get('evidence'), 'Edge needs path and evidence')
        require(dst['kind'] != 'composite', 'Target a concrete child explicitly; composite default-entry semantics are unsupported')
        require(all(len(pt) == 2 and all(finite(v) for v in pt) and 0 <= pt[0] <= m['width'] and 0 <= pt[1] <= m['height'] for pt in e['points']), 'Edge coordinates must be finite and on canvas')
        require(all((a[0] == b[0]) != (a[1] == b[1]) for a,b in zip(e['points'], e['points'][1:])), 'Use nonzero orthogonal path segments')
        if e.get('label'):
            require(e.get('label_at') is not None and len(e['label_at']) == 2 and all(finite(v) for v in e['label_at']), 'Label needs finite position')
            require(0 <= e['label_at'][0] <= m['width'] and 0 <= e['label_at'][1] <= m['height'], 'Label anchor outside canvas')
        require(not e.get('completion') or not e.get('trigger'), 'Completion transition has no explicit trigger')
        if src['kind'] != 'initial' and e.get('trigger'):
            require(e.get('label') and e.get('label_at'), 'Triggered edge needs attached label, including edges to final')
        if src['kind'] == 'initial':
            require(not e.get('trigger') and not e.get('guard'), 'Initial has no trigger/guard')
            require(not e.get('label') or (e.get('effect') and e['label'].lstrip().startswith('/')), 'Initial label may only describe an initialization effect')
        elif dst['kind'] != 'final':
            require(e.get('trigger') or e.get('completion'), 'Explain state transition trigger')
            require(e.get('completion') or (e.get('label') and e.get('label_at')), 'Triggered edge needs attached label')
            for s in leaves(src['id']):
                for t in leaves(dst['id']):
                    expanded.add((s, t))
        for key, point in [(e['source'], e['points'][0]), (e['target'], e['points'][-1])]:
            n = nodes[key]; x, y = point
            require(n['x'] <= x <= n['x']+n['w'] and n['y'] <= y <= n['y']+n['h'], f"Endpoint outside {key}")
            require(min(abs(x-n['x']), abs(x-n['x']-n['w']), abs(y-n['y']), abs(y-n['y']-n['h'])) < .01, f"Endpoint not on perimeter: {key}")
            if n['kind'] in ('initial', 'final'):
                radius=n['w']/2
                require(abs(math.hypot(x-n['x']-radius, y-n['y']-radius)-radius)<.01, f'Endpoint not on circular perimeter: {key}')
        if src['kind'] == 'composite':
            require(e.get('shared_exit_verified') is True, 'Composite exit must apply to every child')
    for n in nodes.values():
        if n['kind'] == 'initial':
            require(sum(e['source'] == n['id'] for e in m['edges']) == 1, 'Invalid state model')
    expected = {tuple(e) for e in m['expected_pairs']}
    require(expanded == expected, f'Coverage mismatch extra={expanded-expected} missing={expected-expanded}')
    return nodes, expanded


def render(m, stem):
    nodes, expanded = check(m)
    w, h = m['width'], m['height']
    mx = ET.Element('mxfile', host='app.diagrams.net')
    diagram = ET.SubElement(mx, 'diagram', id='state-model', name=stem.name)
    model = ET.SubElement(diagram, 'mxGraphModel', page='1', pageWidth=str(w), pageHeight=str(h))
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', id='0'); ET.SubElement(root, 'mxCell', id='1', parent='0')
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 9 5 L 0 10 Z" fill="black"/></marker></defs>',
           '<rect width="100%" height="100%" fill="white"/>']
    font = 'fontFamily=Arial;fontSize=30;fontColor=#000000;strokeColor=#000000;fillColor=#ffffff;'
    def text(x, y, value, size=30):
        lines = value.split('\n')
        for i, line in enumerate(lines):
            svg.append(f'<text x="{x}" y="{y+i*29}" text-anchor="middle" font-family="Arial" font-size="{size}" fill="black">{escape(line)}</text>')
    # Ancestor composites must precede descendants, regardless of JSON order.
    def depth(n):
        return 1+depth(nodes[n['parent']]) if n.get('parent') else 0
    for n in sorted(m['nodes'], key=depth):
        x,y,nw,nh=n['x'],n['y'],n['w'],n['h']; kind=n['kind']
        parent = nodes.get(n.get('parent'))
        styles = {'state':'rounded=1;arcSize=18;', 'composite':'rounded=1;arcSize=7;verticalAlign=top;spacingTop=12;', 'initial':'ellipse;fillColor=#000000;', 'final':'shape=endState;'}
        style = font + styles[kind] + 'whiteSpace=wrap;html=0;'
        c=ET.SubElement(root,'mxCell',id=n['id'],value=n.get('label',''),style=style,vertex='1',parent=n.get('parent','1'))
        ET.SubElement(c,'mxGeometry',x=str(x-(parent['x'] if parent else 0)),y=str(y-(parent['y'] if parent else 0)),width=str(nw),height=str(nh),attrib={'as':'geometry'})
        if kind=='composite':
            svg.append(f'<rect x="{x}" y="{y}" width="{nw}" height="{nh}" rx="16" fill="white" stroke="black" stroke-width="2"/>')
            text(x+nw/2,y+34,n['label'])
    # Edges sit over composite backgrounds and beneath ordinary states.
    for e in m['edges']:
        pts=e['points']; d='M '+' L '.join(f'{x} {y}' for x,y in pts)
        svg.append(f'<path data-edge="{e["id"]}" d="{d}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>')
        style=font+'edgeStyle=none;rounded=0;endArrow=block;endFill=1;exitPerimeter=0;entryPerimeter=0;fontSize=27;'
        for side,key,point in [('exit',e['source'],pts[0]),('entry',e['target'],pts[-1])]:
            n=nodes[key]
            style+=f'{side}X={(point[0]-n["x"])/n["w"]};{side}Y={(point[1]-n["y"])/n["h"]};'
        c=ET.SubElement(root,'mxCell',id=e['id'],value=e.get('label',''),style=style,edge='1',parent='1',source=e['source'],target=e['target'])
        geo=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        arr=ET.SubElement(geo,'Array',attrib={'as':'points'})
        for x,y in pts[1:-1]: ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
        if e.get('label_at'):
            # drawio offsets are measured from the path-length midpoint.
            lengths=[abs(b[0]-a[0])+abs(b[1]-a[1]) for a,b in zip(pts,pts[1:])]
            half=sum(lengths)/2
            for a,b,length in zip(pts,pts[1:],lengths):
                if half<=length:
                    mid=[a[j]+(b[j]-a[j])*half/length for j in (0,1)];break
                half-=length
            lx,ly=e['label_at']; lines=e['label'].count('\n')+1
            ET.SubElement(geo,'mxPoint',x=str(lx-mid[0]),y=str(ly+((lines-1)*29)/2-8-mid[1]),attrib={'as':'offset'})
    for n in m['nodes']:
        x,y,nw,nh=n['x'],n['y'],n['w'],n['h']; kind=n['kind']
        if kind=='state':
            svg.append(f'<rect x="{x}" y="{y}" width="{nw}" height="{nh}" rx="12" fill="white" stroke="black" stroke-width="2"/>')
            text(x+nw/2,y+nh/2+9-(len(n['label'].split('\n'))-1)*29/2,n['label'])
        elif kind in ('initial','final'):
            cx,cy=x+nw/2,y+nh/2
            if kind=='final': svg.append(f'<circle cx="{cx}" cy="{cy}" r="{nw/2}" fill="white" stroke="black" stroke-width="2"/>')
            svg.append(f'<circle cx="{cx}" cy="{cy}" r="{nw/2 if kind=="initial" else nw/2-6}" fill="black"/>')
    for e in m['edges']:
        if e.get('label'):
            x,y=e['label_at']; lines=e['label'].split('\n')
            # Labels are placed beside ink, never painted over it to hide collisions.
            text(x,y,e['label'],27)
    svg.append('</svg>')
    stem.parent.mkdir(parents=True,exist_ok=True)
    stem.with_suffix('.svg').write_text('\n'.join(svg),encoding='utf-8')
    ET.indent(mx); ET.ElementTree(mx).write(stem.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
    print(f'CHECK: {len(nodes)} nodes; {len(m["edges"])} drawn edges; {len(expanded)} expanded state pairs; no annotations')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model');p.add_argument('--out');p.add_argument('--check-only',action='store_true');args=p.parse_args()
    m=json.loads(Path(args.model).read_text(encoding='utf-8'))
    if args.check_only:
        _,pairs=check(m);print(f'CHECK: {len(pairs)} expanded state pairs')
    else:
        p.error('--out is required') if not args.out else render(m,Path(args.out))
