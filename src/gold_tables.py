"""Table-level parser for Barrick (GOLD/B) SEC HTML exhibits.

Parses cell-by-cell so that footnote markers appended to a row LABEL can never
be mistaken for a data value, and so that '(' / '123' / ')' split across three
<td> elements is reassembled into a single negative number.
"""
import re, html as _html
from lxml import html as LH

DASHES = {'-', '–', '—', '−', ''}
NUMRE = re.compile(r'^\$?\s*\(?\s*\$?\s*(\d[\d,]*(?:\.\d+)?)\s*\)?$')


def _clean(s):
    s = _html.unescape(s or '')
    s = s.replace('\xa0', ' ').replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('−', '-')
    return re.sub(r'\s+', ' ', s).strip()


def _cellvals(cells):
    """Return ordered numeric values from a row's cells.
    Handles '(' , '123' , ')' split across cells and '$' in its own cell."""
    vals, open_paren = [], False
    for raw in cells:
        c = _clean(raw)
        if c in ('$', ''):
            continue
        if c == '(':
            open_paren = True
            continue
        if c == ')':
            if vals and open_paren:
                vals[-1] = -abs(vals[-1])
            open_paren = False
            continue
        if c in DASHES or c.lower() in ('nil', '$nil', '$-', '-'):
            vals.append(0.0)
            open_paren = False
            continue
        m = NUMRE.match(c)
        if m:
            v = float(m.group(1).replace(',', ''))
            neg = c.startswith('(') or (open_paren and not c.endswith(')'))
            if c.startswith('(') and c.endswith(')'):
                neg = True
            elif c.startswith('('):
                neg = True
                open_paren = True
            elif open_paren:
                neg = True
            if c.endswith(')'):
                open_paren = False
            vals.append(-v if neg else v)
            continue
        # non-numeric, non-marker cell: closes any dangling paren state
        open_paren = False
    return vals


def _label(cells):
    for raw in cells:
        c = _clean(raw)
        if len(c) > 2 and re.search(r'[A-Za-z]{3}', c):
            return c
    return ''


def parse(path):
    """-> list of row dicts: {tbl, hdr, label, vals}"""
    with open(path, 'rb') as fh:
        doc = LH.fromstring(fh.read())
    rows = []
    for ti, tbl in enumerate(doc.iter('table')):
        trs = tbl.findall('.//tr')
        if not trs:
            continue
        hdr_parts = []
        for tr in trs[:8]:
            hdr_parts.append(' '.join(_clean(td.text_content()) for td in tr.findall('./td') + tr.findall('./th')))
        hdr = _clean(' | '.join(hdr_parts))
        for tr in trs:
            cells = [td.text_content() for td in tr.findall('./td') + tr.findall('./th')]
            if not cells:
                continue
            lab = _label(cells)
            if not lab:
                continue
            vals = _cellvals(cells[1:] if len(cells) > 1 else cells)
            rows.append({'tbl': ti, 'hdr': hdr, 'label': lab, 'vals': vals})
    return rows


def flat_text(path):
    with open(path, 'rb') as fh:
        doc = LH.fromstring(fh.read())
    return re.sub(r'[\s\xa0]+', ' ', doc.text_content())
