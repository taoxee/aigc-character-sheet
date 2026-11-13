"""Regression checks for design contracts; no image generation or networking."""
import argparse
import copy
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import check_design as c
import plan_cast as p


def person(name='A',variant=0):
    return {'id':name,'axes':{k:v[variant%len(v)] for k,v in c.AXES.items()},
            'attributes':{**c.PORTRAIT_LOCKS,'skin_tone':'暖米色','hair':'黑发','mole':'无痣'},
            'bone_plan':dict.fromkeys(c.BONE_KEYS,'已选择的具体结构关系'),
            'makeup':copy.deepcopy(p.MAKEUP['daily'])}


def contract():
    return {'schema_version':1,'request':{'text':'同一套妆设计三位不同成年角色','mode':'text','explicit_image_request':False},
            'roster_goal':'distinct','same_makeup':True,'characters':[person('A',0),person('B',1),person('C',2)]}


def options(**kwargs):
    data=dict(count=1,seed=21,batch_id='test',style='natural',style_prompt='',finish='auto',makeup='daily',same_makeup=False,
              makeup_goal='keep-shape',subject='成年虚构角色',age=30,hair='short',image_type='face',mole_frequency=0.3,
              exclude_manifest=[],max_attempts=5000,request_text='设计一位成年角色，只给提示词')
    data.update(kwargs)
    return argparse.Namespace(**data)


class Contracts(unittest.TestCase):
    def test_all_pairs(self):
        result=c.check(contract())
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(len(result['pairs']),3)

    def test_distant_duplicate_is_detected(self):
        rows,plan,_=p.plan(options(count=15))
        plan['characters'][-1]['axes']=copy.deepcopy(plan['characters'][0]['axes'])
        result=c.check(plan)
        self.assertEqual(result['status'],'FAIL')
        self.assertTrue(any(rows[0]['id']+'/'+rows[-1]['id'] in e for e in result['errors']))

    def test_decorations_do_not_create_identity_differences(self):
        x=contract()
        x['characters'][1]['axes']=copy.deepcopy(x['characters'][0]['axes'])
        x['characters'][1]['attributes'].update(hair='染发',mole='眼角痣',skin_tone='金棕')
        self.assertEqual(c.check(x)['status'],'FAIL')

    def test_multiple_eye_changes_count_as_one_group(self):
        a=person()['axes']; b=copy.deepcopy(a)
        for k,v in c.AXES.items():
            if k.startswith('eyes.'):b[k]=v[1]
        changed,core=c.structural_difference(a,b)
        self.assertEqual(changed,['eyes']);self.assertEqual(core,['eyes'])

    def test_four_groups_still_need_two_core_groups(self):
        x=contract(); x['characters']=x['characters'][:2]
        a=x['characters'][0]['axes']; b=copy.deepcopy(a)
        for k,v in c.AXES.items():
            if k.split('.')[0] in ('jaw','eyes','lips','brows'):b[k]=v[1]
        x['characters'][1]['axes']=b
        self.assertEqual(c.check(x)['status'],'FAIL')

    def test_axis_locks(self):
        x=contract(); x['locks']={'jaw.chin':'round'}
        self.assertEqual(c.check(x)['status'],'FAIL')

    def test_conflicting_global_and_local_locks(self):
        x=contract(); x['locks']={'face.ratio':'short'}
        x['characters'][0]['locks']={'face.ratio':'long'}
        self.assertTrue(any('local/global lock conflict' in e for e in c.check(x)['errors']))

    def test_skin_and_marker_locks(self):
        for key in ('skin_tone','hair','mole'):
            with self.subTest(key=key):
                x=contract(); x['attribute_locks']={key:x['characters'][0]['attributes'][key]}
                x['characters'][1]['attributes'][key]='改变了'
                self.assertEqual(c.check(x)['status'],'FAIL')

    def test_partial_identity_does_not_require_inventing_bones(self):
        x=contract(); x.update(roster_goal='identity',reference_axes={'face.ratio':'short'},same_makeup=False)
        char=person();char['axes']={'face.ratio':'short'};char.pop('bone_plan')
        x['characters']=[char]
        self.assertEqual(c.check(x)['status'],'PASS')
        char['axes']['nose.height']='high'
        self.assertEqual(c.check(x)['status'],'FAIL')

    def test_identity_change_is_rejected(self):
        x=contract();x.update(roster_goal='identity',reference_axes=copy.deepcopy(x['characters'][0]['axes']))
        self.assertEqual(c.check(x)['status'],'FAIL')

    def test_same_makeup_locks_each_component(self):
        for key in c.MAKEUP_KEYS:
            with self.subTest(key=key):
                x=contract();x['characters'][1]['makeup'][key]='另一套妆'
                self.assertEqual(c.check(x)['status'],'FAIL')

    def test_no_random_head_tilt_closed_gaze_or_watermark(self):
        changes={'head_roll_degrees':6,'camera_roll_degrees':-4,'gaze':'closed','visible_text':True,'watermark':True}
        for key,value in changes.items():
            with self.subTest(key=key):
                x=contract();x['characters'][0]['attributes'][key]=value
                self.assertEqual(c.check(x)['status'],'FAIL')

    def test_bone_plan_presence_not_a_semantic_score(self):
        x=contract();x['characters'][0]['bone_plan'].pop('cheek_transition')
        self.assertEqual(c.check(x)['status'],'FAIL')

    def test_missing_unknown_array_and_duplicate_axes(self):
        for value in ('undefined',['short','long'],None):
            x=contract();x['characters'][0]['axes']['face.ratio']=value
            self.assertEqual(c.check(x)['status'],'FAIL')
        x=contract();x['characters'][0]['axes'].pop('nose.width')
        self.assertEqual(c.check(x)['status'],'FAIL')
        with self.assertRaises(ValueError):json.loads('{"eyes.lid":"single","eyes.lid":"double"}',object_pairs_hook=c.unique_keys)

    def test_image_mode_is_not_implied_by_tools(self):
        x=contract();x['request']['mode']='image'
        self.assertEqual(c.check(x)['status'],'FAIL')
        x['request']['explicit_image_request']=True
        self.assertEqual(c.check(x)['status'],'PASS')

    def test_natural_default_is_single_not_cute_batch(self):
        rows,plan,_=p.plan(options())
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['style'],'natural')
        self.assertEqual(rows[0]['finish'],'natural')
        self.assertEqual(plan['request']['text'],'设计一位成年角色，只给提示词')
        self.assertIsNone(rows[0]['image_path'])

    def test_social_and_editorial_are_optional_presets(self):
        for style,finish in [('korean','light-social-retouch'),('japanese','light-social-retouch'),('editorial','editorial')]:
            with self.subTest(style=style):
                rows,_,_=p.plan(options(style=style))
                self.assertEqual(rows[0]['finish'],finish)

    def test_finish_is_independent_of_style(self):
        rows,_,_=p.plan(options(style='korean',finish='natural'))
        self.assertEqual(rows[0]['finish'],'natural')

    def test_custom_style_is_kept(self):
        rows,_,_=p.plan(options(style='custom',style_prompt='低饱和电影人像，克制表情。'))
        self.assertEqual(rows[0]['style_text'],'低饱和电影人像，克制表情。')

    def test_makeup_adaptation_keeps_contract(self):
        axes=person()['axes'];axes['eyes.lid']='single'
        makeup=copy.deepcopy(p.MAKEUP['daily']);before=copy.deepcopy(makeup)
        note=p.adapt_makeup(axes,'keep-shape',makeup)
        self.assertIn('睁眼',note)
        self.assertEqual(makeup,before)

    def test_same_makeup_cannot_silently_change_lines_or_edges(self):
        for goal in ('soften','uplift','widen'):
            with self.subTest(goal=goal):
                with self.assertRaises(ValueError):p.plan(options(count=3,same_makeup=True,makeup_goal=goal))

    def test_legacy_manifest_is_not_pretended_to_be_canonical(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'old.jsonl'
            f.write_text(json.dumps({'character_id':'old-1','identity':{'face':'圆脸'}})+'\n')
            with self.assertRaises(ValueError):p.plan(options(exclude_manifest=[str(f)]))

    def test_roster_complete_shared_makeup_and_reproducibility(self):
        a,_,r=p.plan(options(count=10,same_makeup=True))
        b,_,_=p.plan(options(count=10,same_makeup=True))
        self.assertEqual(a,b);self.assertEqual(len(r['pairs']),45)
        self.assertEqual(len({json.dumps(x['makeup'],sort_keys=True) for x in a}),1)
        self.assertTrue(all(len(x['axes'])==16 and x['bone_plan'] and x['prompt'] for x in a))

    def test_cross_batch_checks_structure_not_just_exact_strings(self):
        old,_,_=p.plan(options(count=5))
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'old.jsonl';f.write_text(''.join(json.dumps(x)+'\n' for x in old))
            new,_,_=p.plan(options(count=5,batch_id='second',exclude_manifest=[str(f)]))
            for a in old:
                for b in new:
                    changed,core=c.structural_difference(a['axes'],b['axes'])
                    self.assertGreaterEqual(len(changed),4);self.assertGreaterEqual(len(core),2)

    def test_cli_preserves_files_and_rejects_incompatible_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out'
            cmd=[sys.executable,str(ROOT/'scripts/plan_cast.py'),'--out-dir',str(out)]
            r=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            before=(out/'manifest.jsonl').read_bytes()
            self.assertNotEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            self.assertEqual((out/'manifest.jsonl').read_bytes(),before)
            for extra in (['--count','0'],['--same-makeup','--makeup','mixed'],['--style','custom']):
                self.assertNotEqual(subprocess.run(cmd[:-1]+[str(Path(tmp)/'bad')]+extra,capture_output=True).returncode,0)

    def test_full_roster_not_a_recent_window(self):
        _,_,report=p.plan(options(count=100))
        self.assertEqual(report['status'],'PASS')
        self.assertEqual(len(report['pairs']),4950)


class WorkflowTests(unittest.TestCase):
    def state(self):
        return {'stage':'ready-for-sheet','final_product':'character-reference-sheet',
                'face_image':'face.png','face_approved':True,'face_approval_evidence':'用户明确说这张可以',
                'clothing':{'mode':'none','reference_images':[],'choice_evidence':'用户回复无输入'},'sheet_image':None}

    def test_explicit_no_clothing_can_proceed(self):
        self.assertEqual(c.check_workflow(self.state()),[])

    def test_face_must_be_approved_before_clothing_and_sheet(self):
        for stage in ('awaiting-clothing','ready-for-sheet','sheet-delivered'):
            w=self.state();w.update(stage=stage,face_approved=False)
            self.assertTrue(c.check_workflow(w))

    def test_no_attachment_is_not_none_choice(self):
        w=self.state();w['clothing']['choice_evidence']=''
        self.assertTrue(c.check_workflow(w))

    def test_pending_clothing_cannot_proceed(self):
        w=self.state();w['clothing']={'mode':'pending','reference_images':[]}
        self.assertTrue(c.check_workflow(w))
        w['stage']='awaiting-clothing'
        self.assertEqual(c.check_workflow(w),[])

    def test_provided_clothing_needs_image_paths(self):
        w=self.state();w['clothing']={'mode':'provided','reference_images':[],'choice_evidence':'用户上传服装图'}
        self.assertTrue(c.check_workflow(w))
        w['clothing']['reference_images']=['outfit.png']
        self.assertEqual(c.check_workflow(w),[])

    def test_final_artifact_is_a_real_sheet_record(self):
        w=self.state();w['stage']='sheet-delivered'
        self.assertTrue(c.check_workflow(w))
        w['sheet_image']='sheet.png'
        self.assertEqual(c.check_workflow(w),[])
        w['final_product']='video'
        self.assertTrue(c.check_workflow(w))

    def test_missing_approval_evidence_fails_integrated_check(self):
        plan=contract();plan['workflow']=self.state()
        self.assertEqual(c.check(plan)['status'],'PASS')
        plan['workflow']['face_approval_evidence']=''
        self.assertEqual(c.check(plan)['status'],'FAIL')

if __name__=='__main__':unittest.main()
