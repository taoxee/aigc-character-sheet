#!/usr/bin/env python3
"""Optional portrait planner. No network or rendering; Chinese prompts by default."""
import argparse
import json
import random
import re
from pathlib import Path
from collections import Counter
from check_design import AXES, PORTRAIT_LOCKS, check, structural_difference, unique_keys

WORDS = {
 'face.ratio': dict(short='脸部整体偏短宽', balanced='脸部整体长宽均衡', long='脸部整体偏长窄'),
 'face.midface': dict(short='中庭略短', balanced='中庭比例均衡', long='中庭略长'),
 'jaw.width': dict(narrow='下颌窄于颧部', medium='下颌与颧部宽度接近', wide='下颌略宽于颧部'),
 'jaw.chin': dict(round='圆钝下巴', tapered='自然收束的下巴', square='方圆下巴'),
 'eyes.length': dict(short='眼裂较短', medium='眼裂长度适中', long='眼裂较长'),
 'eyes.opening': dict(small='开合较小', medium='开合适中', large='开合较大'),
 'eyes.spacing': dict(close='眼距略近', medium='眼距适中', wide='眼距略宽'),
 'eyes.lid': dict(single='单眼皮', hooded='内双，褶皱部分被遮盖', double='清楚的自然双眼皮'),
 'eyes.tilt': dict(down='天然眼尾微下垂', level='天然眼尾平直', up='天然眼尾微上扬'),
 'nose.height': dict(low='鼻梁较低', medium='鼻梁高度适中', high='鼻梁较高'),
 'nose.width': dict(narrow='鼻背较窄', medium='鼻背宽度适中', wide='鼻背较宽'),
 'nose.tip': dict(round='鼻尖圆润', defined='鼻尖自然收束', broad='鼻尖稍有体量'),
 'lips.width': dict(narrow='嘴部较窄', medium='嘴部宽度适中', wide='嘴部较宽'),
 'lips.ratio': dict(lower_fuller='上唇稍薄、下唇略丰', balanced='上下唇比例接近', upper_fuller='上唇略丰满'),
 'brows.arc': dict(straight='自然眉形平直', soft='自然眉形柔弧', angled='自然眉峰较明确'),
 'brows.distance': dict(close='眉眼距略近', medium='眉眼距适中', wide='眉眼距略宽'),
}
STYLES = {
 'natural': '自然人像摄影，清洁连贯的肤色、克制细节，保留人物特有的轮廓与比例，不刻意添加粗糙纹理。',
 'korean': '韩系社交平台人像，清透缎光肤质、柔和粉调与精致眉睫；可爱亲近但保留成年比例和个人骨相。',
 'japanese': '日系社交平台人像，轻盈通透肤色、柔和暖调和自然空气感；可爱亲近但保留个人比例。',
 'editorial': '编辑人像摄影，干净克制的色彩和明确但柔和的面部层次，强调个人结构与妆容重点。',
 'retro': '复古人像的创作方向，柔和低饱和色调与有秩序的妆发，不宣称严格年代复原。',
}
FINISHES = {
 'natural': '肤质自然干净，局部纹理低对比，不主动加颗粒、泛红或斑点。',
 'light-social-retouch': '像经过轻度社交修图的真实照片：中间调柔和、肤色连贯、局部细节适当减弱，仍有摄影层次；不磨成塑料，不统一缩鼻瘦脸。',
 'editorial': '干净的编辑修图，保留轮廓与局部高光层次，控制毛孔和反光，不增加油腻或颗粒覆盖。',
}
MAKEUP = {
 'none': dict(base='裸肌感，必要时极轻局部遮瑕', eyes='不添加明显眼影', liner='不添加眼线', lashes='保留自然睫毛', blush='不额外加腮红', lips='保留自然唇色与天然唇缘'),
 'light': dict(base='薄透缎光底妆，保留基础肤色', eyes='上眼睑薄铺低饱和米桃色，边缘柔和', liner='浅棕色贴根极细眼线，短而平直', lashes='轻微卷翘，根根分明', blush='双颊中央薄透暖粉腮红，边缘柔和', lips='沿天然唇缘薄涂玫瑰粉唇釉，唇中央少量柔光'),
 'daily': dict(base='轻遮瑕缎光底妆，肤色连贯', eyes='上眼睑柔和晕染玫瑰棕，外侧轻加深', liner='棕色贴根细眼线，眼尾短而平直', lashes='自然纤长，分明而不浓密', blush='双颊中央桃玫瑰色柔边晕染', lips='沿天然唇缘涂透明玫瑰粉唇釉，保持自然唇形'),
 'glam': dict(base='中等覆盖缎光底妆，局部高光克制', eyes='灰紫棕上眼影有层次晕染，外眼尾加深', liner='清楚而细的深棕眼线，尾部轻上提', lashes='较明显卷翘和束感，仍能分辨睫毛', blush='颧部外侧玫瑰色腮红柔和轻延', lips='莓玫瑰润泽唇，边界明确但不过度外扩'),
}
HAIR = {
 'short': ['下巴长度波波头和空气刘海', '耳下层次短发与侧刘海', '无刘海的短波波头，一侧别耳后'],
 'medium': ['锁骨层次发与轻薄刘海', '齐肩微卷与侧分', '肩上直发与细碎刘海'],
 'long': ['自然长直发与轻薄刘海', '长层次微卷与侧分', '披肩长发，额前保留细发'],
}
SMILES = ['自然闭口微笑，两侧嘴角轻抬', '闭口浅笑，一侧嘴角略高', '轻微张唇微笑，只露一窄条上排前牙', '温和微笑，少量上牙可见，双颊轻抬']
SKINS = ['浅中性肤色', '暖米色肤色', '中等中性肤色', '中深金棕肤色', '中等橄榄底调肤色']
NATURAL = ['自然黑发', '自然深棕发', '自然黑棕发']
DYED = ['奶茶棕染发，发根略深', '柔和铜棕染发', '灰棕挑染', '玫瑰棕染发']
MOLES = ['画面右侧外眼角下方一颗极小的痣', '画面左侧外眼角旁一颗极小的痣', '画面左侧上颊一颗极小的痣']


def balanced(values, count, rng):
    result = [values[i % len(values)] for i in range(count)]
    rng.shuffle(result)
    return result


def bone_for(axes, rng):
    jaw = WORDS['jaw.width'][axes['jaw.width']]
    chin = WORDS['jaw.chin'][axes['jaw.chin']]
    return {
        'brow_socket': rng.choice(['眉骨起伏平缓、眼窝较浅', '眉骨轻微突出、眼窝深度中等', '眉骨有柔和起伏、眼窝略深但不以阴影伪造凹陷']),
        'cheek_transition': rng.choice(['颧位略高、横向体量适中，太阳穴到颧部平顺过渡', '颧位中等，颧部轻微前突，与太阳穴自然衔接', '颧位中等偏低、骨点柔和，与面颊形成连贯过渡']),
        'jaw_chin': jaw+'，下颌转角自然，'+chin+'，前后位置保持中性',
        'soft_tissue': rng.choice(['面颊适度饱满，骨点之间过渡柔和', '面颊体量较轻，仍保留柔和表面过渡', '颊部软组织偏饱满，轮廓线仍清楚']),
    }


def adapt_makeup(axes, goal, contract):
    notes = []
    if axes['eyes.lid'] in ('single', 'hooded'):
        notes.append('眼影与眼线按睁眼后的可见上眼睑安排，不虚构双眼皮褶皱，不为露妆改变眼皮')
    if goal == 'widen':
        notes.append('在已定腮红落点内横向调整覆盖面积，不改变脸部原生长宽')
    elif goal == 'soften':
        notes.append('适度柔化当前眉头、眼尾和唇缘的边界，不改原生眼角或唇形')
    elif goal == 'uplift':
        notes.append('用局部睫毛强调形成向上视觉，不改骨架和天然眼角方向')
    else:
        notes.append('保留原生脸型与唇形，妆的范围按各人比例适配，不自动瘦脸、厚唇或提白')
    return '；'.join(notes)+'。'


def build_prompt(record):
    axes = record['axes']
    structure = '；'.join(WORDS[k][axes[k]] for k in AXES)
    bone = '；'.join(record['bone_plan'].values())
    makeup = '；'.join(record['makeup'].values())
    if record['image_type'] == 'selfie':
        scene = '9:16竖幅，手臂距离的直接前置自拍，镜头略高于视线，头部与上半身入画，近肩暗示持机动作，手机和手不入画。浅色家居背景。'
    else:
        scene = '4:5竖幅头肩人像，浅灰纯色背景，视线高度镜头，完整保留头顶、发型、下巴与肩颈。'
    return (
        f'设计一位{record["age"]}岁的{record["subject"]}。{structure}。'
        f'骨架与软组织：{bone}。基础肤色为{record["attributes"]["skin_tone"]}。'
        f'{record["style_text"]}{FINISHES[record["finish"]]}'
        f'妆容：{makeup}。{record["makeup_adaptation"]}'
        f'发型发色：{record["hair"]}。个人标记：{record["mole"]}。'
        f'头部端正、正面朝向镜头、双眼水平、下巴中性，不侧歪、不斜相机；目光直接看镜头，{record["expression"]}。'
        f'{scene}穿素色日常上衣，宽而柔和的自然光，脸与颈肩明暗相容。'
        '单人单图，无任何文字、署名、水印、标志或账号；不添加颗粒、灰褐斑驳或重复细纹覆盖，不改变个体结构来套统一模板脸。'
    )


def plan(args):
    if args.same_makeup and (args.makeup == 'mixed' or args.makeup_goal != 'keep-shape'):
        raise ValueError('Same-makeup mode fixes one contract; use one makeup level and keep-shape adaptation only. Redesign the shared contract first for another goal.')
    rng = random.Random(args.seed)
    styles = balanced(['korean', 'japanese'] if args.style == 'mixed' else [args.style], args.count, rng)
    levels = balanced(['light', 'daily', 'glam'] if args.makeup == 'mixed' else [args.makeup], args.count, rng)
    dyes = balanced([True, False], args.count, rng)
    marks = [True] * int(args.count * args.mole_frequency + 0.5)
    marks += [False] * (args.count-len(marks))
    rng.shuffle(marks)
    previous, ids = [], set()
    for filename in args.exclude_manifest:
        for line in Path(filename).read_text().splitlines():
            if line.strip():
                old = json.loads(line, object_pairs_hook=unique_keys)
                if set(old.get('axes', {})) != set(AXES) or any(old['axes'][k] not in AXES[k] for k in AXES):
                    raise ValueError('Exclusion needs v5 canonical axes; legacy text-only records need manual comparison/migration.')
                previous.append(old)
                ids.add(old['character_id'])
    records = []
    for i in range(args.count):
        cid = f'{args.batch_id}-{i+1:04d}'
        if cid in ids:
            raise ValueError('Existing character ID; use a new --batch-id.')
        for attempt in range(args.max_attempts):
            axes = {k: rng.choice(v) for k, v in AXES.items()}
            if all(len(structural_difference(axes, old['axes'])[0]) >= 4 and len(structural_difference(axes, old['axes'])[1]) >= 2 for old in previous+records):
                break
        else:
            raise ValueError(f'No candidate fits all-pairs constraints for {cid}; reduce requested roster or expand the design space. No threshold was lowered.')
        style = styles[i]
        finish = args.finish if args.finish != 'auto' else ('light-social-retouch' if style in ('korean', 'japanese') else 'editorial' if style == 'editorial' else 'natural')
        length = rng.choice(list(HAIR)) if args.hair == 'mixed' else args.hair
        hair = rng.choice(DYED if dyes[i] else NATURAL)+'，'+rng.choice(HAIR[length])
        mole = rng.choice(MOLES) if marks[i] else '不额外添加痣或雀斑'
        age = args.age if args.age is not None else rng.randint(23, 40)
        contract = dict(MAKEUP[levels[i]])
        record = {
            'schema_version': 2, 'character_id': cid, 'id': cid, 'synthetic': True,
            'status': 'planned', 'image_path': None, 'identity_anchor': None,
            'subject': args.subject, 'age': age, 'axes': axes, 'bone_plan': bone_for(axes, rng),
            'attributes': {**PORTRAIT_LOCKS, 'skin_tone': rng.choice(SKINS), 'age': age, 'hair': hair, 'mole': mole},
            'style': style, 'style_text': args.style_prompt if style == 'custom' else STYLES[style],
            'finish': finish, 'makeup_level': levels[i], 'makeup': contract,
            'makeup_adaptation': adapt_makeup(axes, args.makeup_goal, contract),
            'hair': hair, 'mole': mole, 'expression': rng.choice(SMILES),
            'image_type': args.image_type, 'planning_seed': args.seed, 'visual_distinctness': 'not-yet-reviewed',
        }
        record['prompt'] = build_prompt(record)
        records.append(record)
    contract_plan = {'schema_version': 1, 'request': {'text': args.request_text or '按脚本参数规划；未提供原始自然语言请求', 'mode': 'text', 'explicit_image_request': False},
                     'roster_goal': 'single' if len(records)==1 else 'distinct', 'same_makeup': args.same_makeup, 'characters': records}
    report = check(contract_plan)
    if report['status'] != 'PASS':
        raise ValueError('; '.join(report['errors']))
    return records, contract_plan, report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--count', type=int, default=1)
    p.add_argument('--seed', type=int, default=20261111)
    p.add_argument('--batch-id', default='portrait')
    p.add_argument('--request-text', default='', help='Retain the current original request for human review.')
    p.add_argument('--style', choices=list(STYLES)+['custom', 'mixed'], default='natural')
    p.add_argument('--style-prompt', default='')
    p.add_argument('--finish', choices=['auto']+list(FINISHES), default='auto')
    p.add_argument('--makeup', choices=list(MAKEUP)+['mixed'], default='daily')
    p.add_argument('--same-makeup', action='store_true')
    p.add_argument('--makeup-goal', choices=['keep-shape','soften','uplift','widen'], default='keep-shape')
    p.add_argument('--subject', default='成年虚构角色')
    p.add_argument('--age', type=int)
    p.add_argument('--hair', choices=['mixed']+list(HAIR), default='mixed')
    p.add_argument('--image-type', choices=['face','selfie'], default='face')
    p.add_argument('--mole-frequency', type=float, default=0.3)
    p.add_argument('--exclude-manifest', action='append', default=[])
    p.add_argument('--max-attempts', type=int, default=5000)
    p.add_argument('--out-dir', type=Path, required=True)
    a = p.parse_args()
    if not 1 <= a.count <= 1000 or not 1 <= a.max_attempts <= 20000:
        p.error('Count must be 1..1000 and max attempts 1..20000; feasible roster size is not guaranteed.')
    if a.age is not None and not 18 <= a.age <= 100:
        p.error('This planner supports adult ages 18..100.')
    if not 0 <= a.mole_frequency <= 1 or not re.fullmatch(r'[a-zA-Z0-9_-]+',a.batch_id):
        p.error('Invalid mole frequency or batch ID.')
    if a.same_makeup and a.makeup == 'mixed':
        p.error('--same-makeup needs one fixed makeup level.')
    if a.same_makeup and a.makeup_goal != 'keep-shape':
        p.error('--same-makeup allows proportional adaptation only; redesign the shared contract instead of changing edge/direction per face.')
    if a.style == 'custom' and not a.style_prompt.strip():
        p.error('--style custom requires --style-prompt.')
    if a.style != 'custom' and a.style_prompt.strip():
        p.error('--style-prompt applies only with --style custom.')
    if a.out_dir.exists() and any(a.out_dir.iterdir()):
        p.error('Output directory must be empty; existing files are never overwritten.')
    try:
        records, contract, report = plan(a)
    except (ValueError, KeyError, OSError) as exc:
        p.error(str(exc))
    a.out_dir.mkdir(parents=True,exist_ok=True)
    (a.out_dir/'prompts').mkdir()
    (a.out_dir/'manifest.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    for r in records:
        (a.out_dir/'prompts'/(r['character_id']+'.txt')).write_text(r['prompt']+'\n')
    for filename,data in [('design-plan.json',contract),('check-report.json',report)]:
        (a.out_dir/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    summary={'planned_characters':len(records),'rendered_images':0,'all_pairs_checked':len(report['pairs']),
             'style':dict(Counter(r['style'] for r in records)),'makeup':dict(Counter(r['makeup_level'] for r in records)),
             'scope':'Text constraints and field presence only; visual review still required.'}
    (a.out_dir/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))

if __name__ == '__main__':
    main()
