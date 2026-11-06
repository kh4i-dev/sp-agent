"""Acceptance tests for artifact and type-specific gates (stdlib only)."""
import json
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

HERE=Path(__file__).resolve().parent


def png():
    def chunk(tag,data):
        return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    data=b''.join(b'\0'+b'\xff'*1600 for _ in range(300))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',400,300,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(data))+chunk(b'IEND',b'')


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for folder in ('docs/diagrams/vectors','docs/diagrams/spec','docs/images/diagrams'):
            (self.root/folder).mkdir(parents=True,exist_ok=True)
        self.generator=self.root/'docs/diagrams/gen_demo.py';self.generator.write_text('# fixture generator\n',encoding='utf-8')
        self.svg=self.root/'docs/diagrams/vectors/demo.svg'
        self.svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><text x="20" y="60">CLEAN</text><!--'+('padding '*70)+'--></svg>',encoding='utf-8')
        self.image=self.root/'docs/images/diagrams/demo.png';self.image.write_bytes(png())
        self.spec=self.root/'docs/diagrams/spec/demo.json'
        self.meta=dict(diagram_type='sequence',generator='docs/diagrams/gen_demo.py')
        self.save()

    def save(self):self.spec.write_text(json.dumps(self.meta),encoding='utf-8')
    def run_gate(self,*args):
        return subprocess.run([sys.executable,str(HERE/'run_diagrams.py'),'--root',str(self.root),'--audit',*args],capture_output=True,text=True,encoding='utf-8',errors='replace')

    def test_complete_artifacts_pass_automated_only(self):
        r=self.run_gate();self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('Vision QA NOT RUN',r.stdout)

    def test_missing_png_fails(self):
        self.image.unlink();self.assertNotEqual(self.run_gate().returncode,0)

    def test_missing_generator_fails(self):
        self.generator.unlink();self.assertNotEqual(self.run_gate().returncode,0)

    def test_missing_spec_fails(self):
        self.spec.unlink();self.assertNotEqual(self.run_gate().returncode,0)

    def test_bad_png_fails(self):
        self.image.write_bytes(b'not an image'*100);self.assertNotEqual(self.run_gate().returncode,0)

    def test_unrecognized_usecase_is_not_pass(self):
        self.meta['diagram_type']='usecase';self.save()
        r=self.run_gate();self.assertNotEqual(r.returncode,0)
        self.assertIn('Fan gate NOT RUN',r.stdout)

    def test_box_gate_runs(self):
        self.meta.update(diagram_type='box',layout=dict(canvas=dict(width=500,height=250),grid=dict(box_width=100,col_left=[0,150,300],head_height=40,line_height=20),entities=[dict(id=k,col=i,top=50,fields=['id','x','y']) for i,k in enumerate(['a','b','c'])],relationships=[dict(id='edge',a='a',b='c',points=[[100,80],[300,120]])]))
        self.save();r=self.run_gate();self.assertNotEqual(r.returncode,0)
        self.assertIn('[E4]',r.stdout)

    def test_only_no_match_fails(self):self.assertNotEqual(self.run_gate('--only','absent').returncode,0)

    def test_stale_outside_generator_fails(self):
        self.meta['generator']='../outside.py';self.save();self.assertNotEqual(self.run_gate().returncode,0)


if __name__=='__main__':unittest.main()
