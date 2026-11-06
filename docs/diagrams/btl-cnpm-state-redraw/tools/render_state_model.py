"""Render an explicitly positioned state model to SVG and editable drawio.

No auto-layout, notes or decorative text. Geometry and semantic checks are
necessary checks, never a replacement for rendered visual review.
"""
import argparse
import json
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET


def check(m):
    assert m['view'] in ('declared', 'as-is', 'to-be'), 'Choose evidence scope'
    assert not any(k in m for k in ('note', 'notes', 'legend', 'title', 'footer')), 'No annotations on canvas'
    nodes = {n['id']: n for n in m['nodes']}
    assert len(nodes) == len(m['nodes']), 'Duplicate node id'
    ids = set(nodes)
    edge_ids = [e['id'] for e in m['edges']]
    assert len(set(edge_ids)) == len(edge_ids) and not ids.intersection(edge_ids), 'Duplicate edge id'
    for n in nodes.values():
        assert n['kind'] in ('state', 'composite', 'initial', 'final')
        assert n.get('parent') is None or nodes[n['parent']]['kind'] == 'composite'
        assert n['w'] > 0 and n['h'] > 0
        if n['kind'] in ('state', 'composite'):
            assert n.get('label') and n.get('evidence'), 'State needs label and evidence'
    def leaves(key):
        kids = [x['id'] for x in nodes.values() if x.get('parent') == key]
        return sum((leaves(k) for k in kids if nodes[k]['kind'] in ('state', 'composite')), []) if kids else [key]
    expanded = set()
    for e in m['edges']:
        src, dst = nodes[e['source']], nodes[e['target']]
        assert src['kind'] != 'final', 'FinalState cannot have outgoing transitions'
        assert dst['kind'] != 'initial', 'Initial cannot have incoming transitions'
        assert len(e['points']) >= 2 and e.get('evidence'), 'Edge needs path and evidence'
        if src['kind'] == 'initial':
            assert not e.get('trigger') and not e.get('guard'), 'Initial has no trigger/guard'
        elif dst['kind'] != 'final':
            assert e.get('trigger') or e.get('completion'), 'Explain state transition trigger'
            assert e.get('label') and e.get('label_at'), 'Visible edge needs attached label'
            for s in leaves(src['id']):
                for t in leaves(dst['id']):
                    expanded.add((s, t))
        for key, point in [(e['source'], e['points'][0]), (e['target'], e['points'][-1])]:
            n = nodes[key]; x, y = point
            assert n['x'] <= x <= n['x']+n['w'] and n['y'] <= y <= n['y']+n['h'], f"Endpoint outside {key}"
            assert min(abs(x-n['x']), abs(x-n['x']-n['w']), abs(y-n['y']), abs(y-n['y']-n['h'])) < .01, f"Endpoint not on perimeter: {key}"
        if src['kind'] == 'composite':
            assert e.get('shared_exit_verified') is True, 'Composite exit must apply to every child'
    for n in nodes.values():
        if n['kind'] == 'initial':
            assert sum(e['source'] == n['id'] for e in m['edges']) == 1
    expected = {tuple(e) for e in m['expected_pairs']}
    assert expanded == expected, f'Coverage mismatch extra={expanded-expected} missing={expected-expanded}'
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
    # Composite backgrounds first; SVG and drawio share absolute canvas geometry.
    for n in m['nodes']:
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
            text(x+nw/2,y+nh/2+9,n['label'])
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
