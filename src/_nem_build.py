import os, sys, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _nem_seg import F, plain, seg_leaves
from _nem_tbl import tables, nums

R="data/raw/NEM/"
Q10 = {
 "2021Q1":"2021-Q1_0001164727-21-000114_nem-20210331.htm",
 "2021Q2":"2021-Q2_0001164727-21-000194_nem-20210630.htm",
 "2021Q3":"2021-Q3_0001164727-21-000235_nem-20210930.htm",
 "2022Q1":"2022-Q1_0001164727-22-000017_nem-20220331.htm",
 "2022Q2":"2022-Q2_0001164727-22-000024_nem-20220630.htm",
 "2022Q3":"2022-Q3_0001164727-22-000035_nem-20220930.htm",
 "2023Q1":"2023-Q1_0001164727-23-000021_nem-20230331.htm",
 "2023Q2":"2023-Q2_0001164727-23-000034_nem-20230630.htm",
 "2023Q3":"2023-Q3_0001164727-23-000039_nem-20230930.htm",
 "2024Q1":"2024-Q1_0001164727-24-000031_nem-20240331.htm",
 "2024Q2":"2024-Q2_0001164727-24-000039_nem-20240630.htm",
 "2024Q3":"2024-Q3_0001164727-24-000061_nem-20240930.htm",
 "2025Q1":"2025-Q1_0001164727-25-000020_nem-20250331.htm",
 "2025Q2":"2025-Q2_0001164727-25-000035_nem-20250630.htm",
 "2025Q3":"2025-Q3_0001164727-25-000046_nem-20250930.htm",
 "2026Q1":"2026-Q1_0001164727-26-000019_nem-20260331.htm",
 "2026Q2":"2026-Q2_0001164727-26-000036_nem-20260630.htm",
}
K10 = {2021:"2021-Q4_0001164727-22-000007_nem-20211231.htm",
       2022:"2022-Q4_0001164727-23-000011_nem-20221231.htm",
       2023:"2023-Q4_0001164727-24-000016_nem-20231231.htm",
       2024:"2024-Q4_0001164727-25-000011_nem-20241231.htm",
       2025:"2025-Q4_0001164727-26-000010_nem-20251231.htm"}
ER4 = {2021:"2021-Q4_0001157523-22-000249_a52584477ex99_1.htm",
       2022:"2022-Q4_0001157523-23-000340_a53340839_ex991.htm",
       2023:"2023-Q4_0001164727-24-000006_newmontq42023earningsand20.htm",
       2024:"2024-Q4_0001164727-25-000008_newmontq42024earningsand20.htm",
       2025:"2025-Q4_0001164727-26-000009_newmontq42025earningsand20.htm"}

QEND={1:"03-31",2:"06-30",3:"09-30",4:"12-31"}
QSTART={1:"01-01",2:"04-01",3:"07-01",4:"10-01"}
REV="us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
CAS="us-gaap:CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization"
DDA="us-gaap:DepreciationDepletionAndAmortization"
NONGOLD={'CopperMember','SilverMember','LeadMember','ZincMember','MolybdenumMember'}

ALLFILES=[R+v for v in Q10.values()]+[R+v for v in K10.values()]
def plain2(path, concept, s, e, allow=()):
    vs=set()
    for x in F(path):
        if x['concept']==concept and x['start']==s and x['end']==e:
            d=x['dims']
            if not d or all(f"{k}={v}" in allow for k,v in d.items()): vs.add(x['val'])
    return sorted(vs)

def find_any(concept, s, e, allow=(), prefer=None):
    """search every 10-Q/10-K for this concept+period; returns (value, [srcfiles]) or (None,[])"""
    hits={}
    order = ([prefer] if prefer else []) + [f for f in ALLFILES if f!=prefer]
    for f in order:
        for v in plain2(f, concept, s, e, allow):
            hits.setdefault(v, []).append(f)
    if not hits: return None, []
    if len(hits)>1: return ('AMBIG:'+str({k:v[0] for k,v in hits.items()})), []
    v=list(hits)[0]
    return v, hits[v][:1]      # provenance = first file in preference order only

def one(path, concept, s, e, label="", allow=()):
    v = plain2(path, concept, s, e, allow)
    if len(v)==1: return v[0]
    if len(v)==0: return None
    raise SystemExit(f"AMBIGUOUS {label} {concept} {s}..{e} in {path}: {v}")

import re as _re
NG_SUB=_re.compile(r'(Silver|Copper|Lead|Zinc|Molybdenum)Subsegment')
_SUBMETAL=_re.compile(r'^(.*?)(Gold|Silver|Copper|Lead|Zinc|Molybdenum)Subsegment(Member)?$')
INVTYPE={'GoldDoreMember':'DORE','SalesFromConcentrateAndOtherProductionMember':'CONC'}

def canon(seg, sub, pa):
    """-> (mine, metal) canonical across both XBRL tagging regimes"""
    base = sub or seg or ''
    m=_SUBMETAL.match(base)
    if m: mine, metal = m.group(1), m.group(2)
    else:
        mine = base.replace('SubsegmentMember','').replace('Member','')
        metal = None
    if pa in NONGOLD: metal = pa.replace('Member','')
    elif pa == 'GoldMember': metal = 'Gold'
    return mine, metal

def nongold_sum(path, concept, s, e, detail=False):
    """Sum of non-gold CO-PRODUCT segment revenue/CAS, deduped to one value per (mine, metal).
       Regime A (10-Qs, 2023+ filings): metal on ProductOrServiceAxis.
       Regime B (FY2021/FY2022 10-K)  : metal on SubsegmentsAxis (…SilverSubsegmentMember)."""
    buckets={}
    for x in F(path):
        if x['concept']!=concept or x['start']!=s or x['end']!=e: continue
        d=x['dims']
        if d.get('ConsolidationItemsAxis')!='OperatingSegmentsMember': continue
        seg=d.get('StatementBusinessSegmentsAxis'); sub=d.get('SubsegmentsAxis'); pa=d.get('ProductOrServiceAxis')
        mine, metal = canon(seg, sub, pa)
        if metal is None or metal=='Gold': continue
        if pa in ('SilverStreamingAgreementMember','EnvironmentalRemediationMember'): continue
        slot = 'SEGTOTAL' if pa in NONGOLD else INVTYPE.get(pa, 'TOTAL')
        buckets.setdefault((mine,metal),{})[slot]=x['val']
    tot=0.0; det={}
    for k,pv in buckets.items():
        if 'SEGTOTAL' in pv: v=pv['SEGTOTAL']
        elif 'TOTAL' in pv:  v=pv['TOTAL']
        else:                v=pv.get('DORE',0.0)+pv.get('CONC',0.0)
        det[k]=v/1e6; tot+=v
    return (tot,det) if detail else tot

NONMINE=('OtherNorthAmerica','OtherSouthAmerica','OtherAustralia','OtherAsiaPacific','OtherAfrica','OtherNevada','CorporateAndOther','Other')
def gold_seg(path, concept, s, e, detail=False):
    """Gold-attributable sum over MINE-level segment leaves (both tagging regimes)."""
    segs_with_sub=set(); raw=[]
    for x in F(path):
        if x['concept']!=concept or x['start']!=s or x['end']!=e: continue
        d=x['dims']
        if d.get('ConsolidationItemsAxis')!='OperatingSegmentsMember': continue
        seg=d.get('StatementBusinessSegmentsAxis'); sub=d.get('SubsegmentsAxis'); pa=d.get('ProductOrServiceAxis')
        if seg is None: continue
        if pa in ('SilverStreamingAgreementMember','EnvironmentalRemediationMember'): continue
        if pa in INVTYPE: continue
        if sub is not None: segs_with_sub.add(seg)
        raw.append((seg,sub,pa,x['val']))
    leaves={}
    for seg,sub,pa,val in raw:
        if sub is None and seg in segs_with_sub: continue      # region roll-up
        mine, metal = canon(seg, sub, pa)
        leaves.setdefault(mine,{})[metal]=val
    tot=0.0; det={}
    for mine,mv in leaves.items():
        if any(mine.startswith(pfx) for pfx in NONMINE): continue
        metals=[k for k in mv if k is not None]
        v = mv.get('Gold',0.0) if metals else mv.get(None,0.0)
        det[mine]=v/1e6; tot+=v
    return (tot,det) if detail else tot

def mdna_gold(path, period_label):
    """MD&A 'Consolidated sales:' table -> Gold 'Net' value (USD m)"""
    for t in tables(path):
        labs=[r[0] for r in t]
        if not any(l.startswith('Consolidated sales') for l in labs): continue
        if period_label not in " | ".join(t[0]): continue
        for r in t:
            if r[0].strip()=='Net':
                n=nums(r)
                if len(n)>=5: return n[0]
    return None

def aisc_row(path, period_label):
    for t in tables(path):
        h=" | ".join(t[0])
        if 'All-In Sustaining Costs' not in h or 'Ounces' not in h: continue
        if not t[0][0].startswith(period_label): continue
        for r in t:
            if r[0].strip().startswith('Total Gold') and 'Equivalent' not in r[0]:
                return nums(r)
    return None

def highlights(path):
    for t in tables(path):
        labs=[r[0] for r in t]
        i=[k for k,l in enumerate(labs) if l.startswith('Consolidated gold ounces')]
        if not i: continue
        i=i[0]
        return nums(t[i+1]), nums(t[i+2])
    return None,None
