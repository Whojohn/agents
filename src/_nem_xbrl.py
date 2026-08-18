import re, sys, json
from collections import defaultdict

NUM = re.compile(r'^[\d,\.]+$')

def load(path):
    return open(path,'rb').read().decode('utf8','ignore')

def contexts(t):
    ctx={}
    for m in re.finditer(r'<xbrli:context id="([^"]+)"\s*>(.*?)</xbrli:context>', t, re.S|re.I):
        cid, body = m.group(1), m.group(2)
        mem = re.findall(r'<xbrldi:explicitMember dimension="([^"]+)"\s*>([^<]+)</xbrldi:explicitMember>', body)
        sd = re.search(r'<xbrli:startDate>([^<]+)<', body)
        ed = re.search(r'<xbrli:endDate>([^<]+)<', body)
        inst = re.search(r'<xbrli:instant>([^<]+)<', body)
        ctx[cid] = {
            'start': sd.group(1) if sd else None,
            'end': ed.group(1) if ed else None,
            'instant': inst.group(1) if inst else None,
            'dims': {d.split(':')[-1]: v.split(':')[-1] for d, v in mem},
        }
    return ctx

def facts(path):
    t = load(path)
    ctx = contexts(t)
    out=[]
    for m in re.finditer(r'<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>', t, re.S|re.I):
        a = m.group(1); raw = re.sub(r'<[^>]+>','',m.group(2))
        raw = raw.replace('&#160;',' ').replace('&nbsp;',' ').strip()
        name = re.search(r'name="([^"]+)"', a); cref = re.search(r'contextRef="([^"]+)"', a)
        if not name or not cref: continue
        scale = re.search(r'scale="(-?\d+)"', a); sign = re.search(r'sign="(-)"', a)
        unit = re.search(r'unitRef="([^"]+)"', a)
        v = raw.replace(',','').replace('$','').strip()
        if v in ('','—','—','&#8212;'): v='0'
        try: val=float(v)
        except: continue
        if scale: val *= 10**int(scale.group(1))
        if sign: val = -val
        c = ctx.get(cref.group(1), {})
        out.append({'concept':name.group(1),'val':val,'start':c.get('start'),'end':c.get('end'),
                    'instant':c.get('instant'),'dims':c.get('dims',{}),'unit':unit.group(1) if unit else None})
    return out

if __name__=='__main__':
    fs=facts(sys.argv[1])
    if len(sys.argv)>2 and sys.argv[2]=='concepts':
        cs=defaultdict(int)
        for f in fs: cs[f['concept']]+=1
        for k,v in sorted(cs.items()): print(v,k)
    else:
        for f in fs:
            if re.search(sys.argv[2], f['concept'], re.I):
                print(f['concept'], f['start'], f['end'], f['instant'], f['dims'], f['val'])
