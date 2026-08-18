import re, warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
_c={}
def tables(path):
    if path in _c: return _c[path]
    soup=BeautifulSoup(open(path,'rb').read(),'lxml')
    out=[]
    for tb in soup.find_all('table'):
        if tb.find_parent('table') is not None: continue
        rows=[]
        for tr in tb.find_all('tr'):
            cells=[re.sub(r'\s+',' ',td.get_text(" ",strip=True).replace('\xa0',' ')).strip() for td in tr.find_all(['td','th'])]
            cells=[c for c in cells if c!='']
            if cells: rows.append(cells)
        if rows: out.append(rows)
    _c[path]=out
    return out

NUMRE=re.compile(r'^\(?-?[\d,]+(\.\d+)?\)?%?$')
def nums(cells):
    v=[]
    for c in cells:
        c=c.replace('$','').replace('%','').strip()
        if c in ('—','–','-','—'): v.append(0.0); continue
        if NUMRE.match(c):
            neg = c.startswith('(')
            x=c.strip('()').replace(',','')
            try: f=float(x)
            except: continue
            v.append(-f if neg else f)
    return v

def find_tables(path, pred):
    return [t for t in tables(path) if pred(t)]

def row_after(rows, label_re, offset=0):
    rx=re.compile(label_re)
    for i,r in enumerate(rows):
        if rx.search(r[0]):
            return rows[i+offset]
    return None

def rows_matching(rows, label_re):
    rx=re.compile(label_re)
    return [r for r in rows if r and rx.search(r[0])]
