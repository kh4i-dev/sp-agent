"""Regression cases for the state model acceptance rules (stdlib only)."""
import unittest
import tempfile
from pathlib import Path
from render_state_model import check, render


def valid():
    return dict(view='declared',width=400,height=250,nodes=[
        dict(id='a',kind='state',label='A',x=0,y=0,w=100,h=60,evidence='REQ-1'),
        dict(id='b',kind='state',label='B',x=200,y=0,w=100,h=60,evidence='REQ-1'),
    ],edges=[dict(id='e',source='a',target='b',points=[[100,30],[200,30]],trigger='done',label='done',label_at=[150,15],evidence='REQ-1')],expected_pairs=[['a','b']])


class StateAcceptance(unittest.TestCase):
    def test_simple_transition(self): self.assertEqual(check(valid())[1],{('a','b')})

    def test_reject_note(self):
        m=valid();m['footer']='explanation'
        with self.assertRaises(ValueError):check(m)

    def test_reject_outgoing_final(self):
        m=valid();m['nodes'][0].update(kind='final',w=100,h=100)
        with self.assertRaisesRegex(ValueError,'FinalState cannot have outgoing'):check(m)

    def test_reject_initial_guard(self):
        m=valid();m['nodes'][0].update(kind='initial',w=60,h=60)
        m['edges'][0].update(guard='yes',points=[[60,30],[200,30]])
        with self.assertRaisesRegex(ValueError,'Initial has no trigger/guard'):check(m)

    def test_reject_missing_contract_pair(self):
        m=valid();m['expected_pairs'].append(['b','a'])
        with self.assertRaises(ValueError):check(m)

    def test_completed_is_not_a_final(self):
        m=valid();m['nodes'][0]['label']='Completed';m['nodes'][1]['label']='Returned'
        self.assertEqual(check(m)[1],{('a','b')})

    def test_composite_expansion(self):
        m=valid();m['nodes'].insert(0,dict(id='group',kind='composite',label='Group',x=0,y=0,w=100,h=180,evidence='REQ-1'))
        m['nodes'][1]['parent']='group'
        m['nodes'].append(dict(id='c',kind='state',label='C',x=0,y=100,w=100,h=60,evidence='REQ-1',parent='group'))
        m['edges'][0].update(source='group',shared_exit_verified=True)
        m['expected_pairs'].append(['c','b'])
        self.assertEqual(check(m)[1],{('a','b'),('c','b')})
        m['edges'][0]['shared_exit_verified']=False
        with self.assertRaises(ValueError):check(m)

    def test_completion_may_be_unlabelled(self):
        m=valid();m['edges'][0].update(completion=True,trigger='',label='')
        self.assertEqual(check(m)[1],{('a','b')})

    def test_reserved_drawio_id_is_rejected(self):
        m=valid();m['nodes'][0]['id']='0';m['edges'][0]['source']='0';m['expected_pairs']=[['0','b']]
        with self.assertRaises(ValueError):check(m)

    def test_unmodelled_composite_entry_is_rejected(self):
        m=valid();m['nodes'][1]['kind']='composite'
        m['nodes'].append(dict(id='c',kind='state',label='C',x=200,y=0,w=100,h=60,parent='b',evidence='REQ-1'))
        m['expected_pairs']=[['a','c']]
        with self.assertRaises(ValueError):check(m)

    def test_parent_cycle_is_rejected(self):
        m=valid()
        for n in m['nodes']:n['kind']='composite'
        m['nodes'][0]['parent']='b';m['nodes'][1]['parent']='a'
        m['nodes'].append(dict(id='c',kind='state',label='C',x=0,y=0,w=100,h=60,parent='a',evidence='REQ-1'))
        with self.assertRaisesRegex(ValueError,'cyclic hierarchy'):check(m)

    def test_child_outside_parent_is_rejected(self):
        m=valid();m['nodes'].append(dict(id='group',kind='composite',label='G',x=0,y=0,w=100,h=100,evidence='REQ-1'))
        m['nodes'][1]['parent']='group'
        with self.assertRaises(ValueError):check(m)

    def test_outside_canvas_is_rejected(self):
        m=valid();m['width']=250
        with self.assertRaises(ValueError):check(m)

    def test_diagonal_route_is_rejected(self):
        m=valid();m['edges'][0]['points']=[[100,30],[150,45],[200,30]]
        with self.assertRaises(ValueError):check(m)

    def test_initial_trigger_cannot_hide_in_label(self):
        m=valid();m['nodes'][0]['kind']='initial';m['nodes'][0]['w']=60
        m['edges'][0].update(trigger='',points=[[60,30],[200,30]])
        with self.assertRaises(ValueError):check(m)

    def test_nonfinite_waypoint_is_rejected(self):
        m=valid();m['edges'][0]['points'].insert(1,[float('nan'),30])
        with self.assertRaises(ValueError):check(m)

    def test_circle_corner_is_not_a_valid_port(self):
        m=valid();m['nodes'][0].update(kind='initial',w=100,h=100)
        m['edges'][0].update(trigger='',label='',points=[[100,0],[200,0],[200,30]])
        m['expected_pairs']=[]
        with self.assertRaises(ValueError):check(m)

    def test_unlabelled_completion_renders(self):
        m=valid();m['edges'][0].update(completion=True,trigger='',label='')
        with tempfile.TemporaryDirectory() as folder:
            stem=Path(folder)/'completion';render(m,stem)
            self.assertTrue(stem.with_suffix('.svg').exists())
            self.assertTrue(stem.with_suffix('.drawio').exists())

    def test_blank_model_is_rejected(self):
        m=valid();m.update(nodes=[],edges=[],expected_pairs=[])
        with self.assertRaises(ValueError):check(m)

    def test_completion_cannot_also_have_an_explicit_trigger(self):
        m=valid();m['edges'][0]['completion']=True
        with self.assertRaises(ValueError):check(m)

    def test_label_anchor_must_be_on_canvas(self):
        m=valid();m['edges'][0]['label_at']=[-100,15]
        with self.assertRaises(ValueError):check(m)


if __name__=='__main__':unittest.main()
