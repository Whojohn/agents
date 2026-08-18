import sys, os, re, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gold_tables as G

RAW = 'data/raw/GOLD/'
# quarter -> (press release exhibit, MD&A+FS exhibit)
FILES = {
 '2021Q1': ('2021-Q1_0001193125-21-151919_d138491dex991.htm','2021-Q1_0001193125-21-151919_d138491dex992.htm'),
 '2021Q2': ('2021-Q2_0001193125-21-240554_d181316dex991.htm','2021-Q2_0001193125-21-240554_d181316dex992.htm'),
 '2021Q3': ('2021-Q3_0001193125-21-320495_d161850dex991.htm','2021-Q3_0001193125-21-320495_d161850dex992.htm'),
 '2021Q4': ('2021-Q4_0001193125-22-044545_d191140dex991.htm','2021-Q4_0001193125-22-044545_d191140dex992.htm'),
 '2022Q1': ('2022-Q1_0001193125-22-140987_d334408dex991.htm','2022-Q1_0001193125-22-140987_d334408dex992.htm'),
 '2022Q2': ('2022-Q2_0001193125-22-214948_d368220dex991.htm','2022-Q2_0001193125-22-214948_d368220dex992.htm'),
 '2022Q3': ('2022-Q3_0001193125-22-277128_d388122dex991.htm','2022-Q3_0001193125-22-277128_d388122dex992.htm'),
 '2022Q4': ('2022-Q4_0001193125-23-040263_d441831dex991.htm','2022-Q4_0001193125-23-040263_d441831dex992.htm'),
 '2023Q1': ('2023-Q1_0001193125-23-133185_d481455dex991.htm','2023-Q1_0001193125-23-133185_d481455dex992.htm'),
 '2023Q2': ('2023-Q2_0001193125-23-206350_d470594dex991.htm','2023-Q2_0001193125-23-206350_d470594dex992.htm'),
 '2023Q3': ('2023-Q3_0001193125-23-269404_d572113dex991.htm','2023-Q3_0001193125-23-269404_d572113dex992.htm'),
 '2023Q4': ('2023-Q4_0001193125-24-036626_d647461dex991.htm','2023-Q4_0001193125-24-036626_d647461dex992.htm'),
 '2024Q1': ('2024-Q1_0001193125-24-128219_d829874dex991.htm','2024-Q1_0001193125-24-128219_d829874dex992.htm'),
 '2024Q2': ('2024-Q2_0001193125-24-198723_d876961dex991.htm','2024-Q2_0001193125-24-198723_d876961dex992.htm'),
 '2024Q3': ('2024-Q3_0001193125-24-253060_d860543dex991.htm','2024-Q3_0001193125-24-253060_d860543dex992.htm'),
 '2024Q4': ('2024-Q4_0001193125-25-025337_d853431dex991.htm','2024-Q4_0001193125-25-025337_d853431dex992.htm'),
 '2025Q1': ('2025-Q1_0001193125-25-114445_d936939dex991.htm','2025-Q1_0001193125-25-114445_d936939dex992.htm'),
 '2025Q2': ('2025-Q2_0001193125-25-178085_d30477dex991.htm','2025-Q2_0001193125-25-178085_d30477dex992.htm'),
 '2025Q3': ('2025-Q3_0001193125-25-274144_d922379dex991.htm','2025-Q3_0001193125-25-274144_d922379dex992.htm'),
 '2025Q4': ('2025-Q4_0001193125-26-039501_d10712dex991.htm','2025-Q4_0001193125-26-039501_d10712dex992.htm'),
 '2026Q1': ('2026-Q1_0001193125-26-216613_d145525dex991.htm','2026-Q1_0001193125-26-216613_d145525dex992.htm'),
 '2026Q2': ('2026-Q2_0001193125-26-343857_d67611dex991.htm','2026-Q2_0001193125-26-343857_d67611dex992.htm'),
}
QEND = {'Q1':('01-01','03-31','3/31'),'Q2':('04-01','06-30','6/30'),
        'Q3':('07-01','09-30','9/30'),'Q4':('10-01','12-31','12/31')}


def dtok(q):
    y, qq = q[:4], q[4:]
    return '%s/%s' % (QEND[qq][2], y[2:])


def tables(rows):
    d = {}
    for r in rows:
        d.setdefault(r['tbl'], []).append(r)
    return d


def find_tbl(tbls, need_labels, hdr_any=(), hdr_all=(), reject_hdr=()):
    """Return ids of tables whose rows carry every label prefix in need_labels."""
    out = []
    for t, rs in tbls.items():
        labs = [x['label'] for x in rs]
        hdr = rs[0]['hdr']
        if any(rej in hdr for rej in reject_hdr):
            continue
        if hdr_all and not all(h in hdr for h in hdr_all):
            continue
        if hdr_any and not any(h in hdr for h in hdr_any):
            continue
        ok = all(any(l.startswith(nl) for l in labs) for nl in need_labels)
        if ok:
            out.append(t)
    return sorted(out)


def row(tbls, t, prefix, occ=0, exact=None):
    hits = []
    for r in tbls[t]:
        if exact is not None:
            if r['label'] == exact:
                hits.append(r)
        elif r['label'].startswith(prefix):
            hits.append(r)
    if len(hits) <= occ:
        return None
    return hits[occ]


def v0(r):
    if r is None or not r['vals']:
        return None
    return r['vals'][0]


def vi(r, i):
    if r is None or len(r['vals']) <= i:
        return None
    return r['vals'][i]


def extract(q):
    prf, mdf = FILES[q]
    rows = G.parse(RAW + mdf)
    T = tables(rows)
    tok = dtok(q)
    o = {'quarter': q, 'source_file': RAW + mdf}
    chk = {}
    notes = []

    # ---- 1. MD&A revenue-by-metal table (discrete 3M, col0) --------------
    cands = find_tbl(T, ['Other sales', 'Total revenue'])
    cands = [t for t in cands if tok in T[t][0]['hdr'] or 'Revenue' in T[t][0]['hdr']]
    assert cands, 'no MDNA revenue table ' + q
    tr = cands[0]
    assert tok in T[tr][0]['hdr'], 'REVTBL header lacks %s: %s' % (tok, T[tr][0]['hdr'][:160])
    o['total_revenue'] = v0(row(T, tr, 'Total revenue'))
    o['segment_revenue_gold_consolidated'] = v0(row(T, tr, 'Revenue', occ=0))
    o['byproduct_credits'] = v0(row(T, tr, 'Other sales'))
    oz_sold = row(T, tr, '000s oz sold') or row(T, tr, 'Gold sold')
    oz_prod = row(T, tr, '000s oz produced') or row(T, tr, 'Gold produced')
    o['gold_oz_sold'] = int(round(v0(oz_sold) * 1000)) if v0(oz_sold) is not None else None
    o['gold_oz_produced'] = int(round(v0(oz_prod) * 1000)) if v0(oz_prod) is not None else None

    # ---- 2. MD&A gold cost-of-sales breakdown (discrete 3M, col0) --------
    cands = find_tbl(T, ['Site operating costs', 'Cost of sales'], hdr_all=[tok])
    cands = [t for t in cands if any(r['label'] == 'Gold' for r in T[t])]
    assert cands, 'no MDNA COS table ' + q
    tc = cands[0]
    o['opcost_ex_dda'] = v0(row(T, tc, 'Site operating costs', 0))
    o['segment_dda'] = v0(row(T, tc, 'Depreciation', 0))
    roy = v0(row(T, tc, 'Royalty expense', 0))
    mpt = v0(row(T, tc, 'Mining and production taxes', 0))
    o['royalties'] = (roy or 0) + (mpt or 0) if roy is not None else None
    chk['gold_cos_total'] = v0(row(T, tc, 'Cost of sales', 0))
    chk['community_relations'] = v0(row(T, tc, 'Community relations', 0))
    chk['mining_prod_taxes'] = mpt

    # ---- 3. AISC reconciliation ------------------------------------------
    cands = find_tbl(T, ['Total cash costs', 'All-in sustaining costs'], hdr_all=[tok])
    cands = [t for t in cands if any(r['label'].startswith(('Cost of sales applicable to gold production',
                                                           'COS applicable to gold production')) for r in T[t])]
    assert cands, 'no AISC recon ' + q
    ta = cands[0]
    A = lambda p, occ=0: v0(row(T, ta, p, occ))
    anchor = A('Cost of sales applicable to gold production')
    if anchor is None:
        anchor = A('COS applicable to gold production')
    chk['aisc_anchor'] = anchor
    chk['aisc_depn'] = A('Depreciation')
    chk['aisc_eqm'] = A('Cash cost of sales applicable to equity method investments')
    if chk['aisc_eqm'] is None:
        chk['aisc_eqm'] = A('Total cash cost applicable to equity method investments')
    if chk['aisc_eqm'] is None:
        chk['aisc_eqm'] = A('Total cash costs applicable to equity method investments')
    chk['aisc_byp'] = A('By-product credits')
    if chk['aisc_byp'] is None:
        chk['aisc_byp'] = A('Costs allocated to by-products')
    chk['aisc_hedge'] = A('Realized (gains) losses on hedge')
    chk['aisc_nonrec'] = A('Non-recurring items')
    chk['aisc_other'] = v0(row(T, ta, None, 0, exact='Other'))
    chk['aisc_nci'] = A('Non-controlling interests')
    chk['aisc_tcc'] = v0(row(T, ta, None, 0, exact='Total cash costs'))
    chk['aisc_ga'] = A('General & administrative costs')
    chk['aisc_expl'] = A('Minesite exploration and evaluation costs')
    chk['aisc_scapex'] = A('Minesite sustaining capital expenditures')
    chk['aisc_leases'] = A('Sustaining leases')
    chk['aisc_rehab'] = A('Rehabilitation - accretion and amortization (operating')
    chk['aisc_nciadj'] = A('Non-controlling interest, copper operations and other')
    chk['aisc_total'] = v0(row(T, ta, None, 0, exact='All-in sustaining costs'))
    ozr = row(T, ta, 'Ounces sold')
    chk['aisc_oz'] = v0(ozr)
    chk['aisc_oz_caption'] = ozr['label'] if ozr else None
    o['published_aisc'] = A('AISC/oz') or A('All-in sustaining costs per ounce')
    o['published_aic'] = A('AIC/oz') or A('All-in costs per ounce')
    chk['published_tcc'] = A('TCC/oz') or A('Total cash costs per ounce')
    chk['aisc_byp_caption'] = ('Costs allocated to by-products'
                               if row(T, ta, 'Costs allocated to by-products') else 'By-product credits')

    # ---- 4. Realized-price reconciliation (attributable gold revenue) ----
    cands = find_tbl(T, ['Sales applicable to non-controlling interests', 'Revenues - as adjusted'])
    assert cands, 'no realized price recon ' + q
    tp = cands[0]
    o['segment_revenue_gold'] = v0(row(T, tp, 'Revenues - as adjusted'))
    chk['rpr_sales'] = v0(row(T, tp, None, 0, exact='Sales'))
    chk['rpr_nci'] = v0(row(T, tp, 'Sales applicable to non-controlling interests'))
    chk['rpr_eqm'] = v0(row(T, tp, 'Sales applicable to equity method investments'))
    chk['realized_price'] = v0(row(T, tp, 'Realized gold'))

    # ---- 5. Finance costs, net -------------------------------------------
    cands = find_tbl(T, ['Interest expense', 'Finance income', 'Finance costs, net'], hdr_all=[tok])
    assert cands, 'no finance costs table ' + q
    tf = cands[0]
    ie = v0(row(T, tf, 'Interest expense'))
    fi = v0(row(T, tf, 'Finance income'))
    o['reclamation_accretion'] = v0(row(T, tf, 'Accretion'))
    chk['interest_expense'] = ie
    chk['finance_income'] = fi
    chk['interest_capitalized'] = v0(row(T, tf, 'Interest capitalized'))
    chk['finance_costs_net'] = v0(row(T, tf, 'Finance costs, net'))
    o['net_interest'] = round(ie + fi, 3) if (ie is not None and fi is not None) else None

    # ---- 6. MD&A financial summary (capex, net earnings) -----------------
    cands = find_tbl(T, ['Total consolidated capital expenditures'], hdr_all=[tok])
    assert cands, 'no MDNA summary ' + q
    ts = cands[0]
    o['capex_total'] = v0(row(T, ts, 'Total consolidated capital expenditures'))
    chk['sustaining_capex'] = v0(row(T, ts, 'Minesite sustaining capital expenditures'))
    chk['project_capex'] = v0(row(T, ts, 'Project capital expenditures'))
    ne = row(T, ts, 'Net earnings') or row(T, ts, 'Net (loss) earnings') or row(T, ts, 'Net earnings (loss)')
    chk['net_earnings_mdna'] = v0(ne)

    # ---- 6b. MD&A exploration/evaluation table (discrete 3M, col0) -------
    cands = find_tbl(T, ['Total exploration, evaluation and project expenses'], hdr_all=[tok])
    assert cands, 'no MDNA exploration table ' + q
    te = cands[0]
    o['exploration_expensed'] = v0(row(T, te, 'Total exploration, evaluation and project expenses'))
    chk['expl_minesite'] = v0(row(T, te, 'Minesite exploration and evaluation'))

    # ---- 7. Statements (IS / CF) -----------------------------------------
    isq = find_tbl(T, ['General and administrative expenses', 'Exploration, evaluation and project expenses'],
                   hdr_any=['except per share data'])
    cfq = find_tbl(T, ['Lease repayments', 'Capital expenditures'], hdr_any=['OPERATING ACTIVITIES', 'Net income'])
    o['_is_tbl'], o['_cf_tbl'] = isq, cfq
    is_annual_only = False
    if isq:
        h = T[isq[0]][0]['hdr']
        is_annual_only = ('Three months' not in h and 'three months' not in h)
    o['_is_annual_only'] = is_annual_only
    if isq:
        ti = isq[0]
        o['corporate_g_and_a'] = v0(row(T, ti, 'General and administrative expenses'))
        chk['is_exploration'] = v0(row(T, ti, 'Exploration, evaluation and project expenses'))
        o['net_income_attributable'] = v0(row(T, ti, 'Equity holders of Barrick'))
        chk['is_revenue'] = v0(row(T, ti, 'Revenue'))
        chk['is_cos'] = v0(row(T, ti, 'Cost of sales'))
        chk['is_hdr'] = T[ti][0]['hdr'][:110]
        chk['is_expl_all'] = row(T, ti, 'Exploration, evaluation and project expenses')['vals']
        chk['is_rev_all'] = row(T, ti, 'Revenue')['vals']
    if cfq:
        tcf = cfq[0]
        o['cash_tax_paid'] = v0(row(T, tcf, 'Income taxes paid')) or v0(row(T, tcf, 'Income taxes'))
        o['lease_payments'] = v0(row(T, tcf, 'Lease repayments'))
        chk['cf_capex'] = v0(row(T, tcf, 'Capital expenditures'))
        chk['cf_hdr'] = T[tcf][0]['hdr'][:110]
        _it = row(T, tcf, 'Income taxes paid') or row(T, tcf, 'Income taxes')
        chk['cf_tax_all'] = _it['vals'] if _it else None
        chk['cf_lease_all'] = row(T, tcf, 'Lease repayments')['vals']
    # sign normalisation: all cost/outflow items POSITIVE
    for k in ('cash_tax_paid','lease_payments','capex_total','reclamation_accretion',
              'opcost_ex_dda','segment_dda','royalties','corporate_g_and_a','exploration_expensed'):
        if o.get(k) is not None:
            o[k] = abs(o[k])
    o['_chk'] = chk
    o['_notes'] = notes
    return o


if __name__ == '__main__':
    import pprint
    for q in sys.argv[1:]:
        r = extract(q)
        pprint.pprint(r, width=130)
