import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _nem_xbrl import facts as _facts
from collections import defaultdict
_cache={}
METALS={'GoldMember','CopperMember','SilverMember','LeadMember','ZincMember','MolybdenumMember'}
NONMINE=('OtherNorthAmerica','OtherSouthAmerica','OtherAustralia','OtherAfrica','OtherNevada','CorporateAndOther')

def F(path):
    if path not in _cache: _cache[path]=_facts(path)
    return _cache[path]

def plain(path, concept, start, end):
    """facts with no dimensions for the given duration"""
    vs=set()
    for x in F(path):
        if x['concept']==concept and x['start']==start and x['end']==end and not x['dims']:
            vs.add(x['val'])
    return sorted(vs)

def seg_leaves(path, concept, start, end):
    """returns dict leafkey -> {metal_or_None: value}"""
    rows=defaultdict(dict)
    segs_with_sub=set()
    tmp=[]
    for x in F(path):
        if x['concept']!=concept or x['start']!=start or x['end']!=end: continue
        d=x['dims']
        if d.get('ConsolidationItemsAxis')!='OperatingSegmentsMember': continue
        seg=d.get('StatementBusinessSegmentsAxis'); sub=d.get('SubsegmentsAxis')
        if seg is None: continue
        if sub is not None: segs_with_sub.add(seg)
        tmp.append((seg,sub,d.get('ProductOrServiceAxis'),x['val']))
    for seg,sub,metal,val in tmp:
        if sub is None and seg in segs_with_sub:  # region roll-up row
            continue
        key=(seg,sub)
        m = metal if metal in METALS else None
        rows[key][m]=val
    return rows

def gold_and_total(path, concept, start, end):
    rows=seg_leaves(path, concept, start, end)
    gold=0.0; tot=0.0; nonmine_gold=0.0
    detail={}
    for key,mv in rows.items():
        name = key[1] or key[0]
        is_nonmine = any(name.startswith(p) for p in NONMINE)
        if set(mv.keys())-{None}:
            g = mv.get('GoldMember',0.0)
            t = mv.get(None, sum(v for k,v in mv.items() if k is not None))
        else:
            g = mv.get(None,0.0); t = g
        detail[name]=(g,t,is_nonmine)
        tot+=t
        if is_nonmine: nonmine_gold+=g
        else: gold+=g
    return gold, tot, nonmine_gold, detail
