import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_gold as E

QS = sorted(E.FILES)
YQ = {'Q1': ('01-01', '03-31'), 'Q2': ('04-01', '06-30'),
      'Q3': ('07-01', '09-30'), 'Q4': ('10-01', '12-31')}

COLS = ['ticker','quarter','period_start','period_end','basis',
        'segment_revenue_gold','segment_revenue_gold_consolidated','total_revenue',
        'opcost_ex_dda','segment_dda','royalties','corporate_g_and_a','exploration_expensed',
        'capex_total','reclamation_accretion','lease_payments','net_interest','cash_tax_paid',
        'gold_oz_sold','gold_oz_produced',
        'published_aisc','aisc_basis','published_aic','byproduct_credits',
        'net_income_attributable','recon_aisc','recon_residual_pct','flags','source_file']

R = {q: E.extract(q) for q in QS}
gates, problems = [], []


# ---------- gate 1: 6M-current == Q1 + Q2 (income statement revenue) -------
for y in ('2021','2022','2023','2024','2025','2026'):
    q1, q2 = y+'Q1', y+'Q2'
    if q1 in R and q2 in R:
        six = R[q2]['_chk']['is_rev_all'][2]
        s = R[q1]['_chk']['is_rev_all'][0] + R[q2]['_chk']['is_rev_all'][0]
        gates.append(('6M=Q1+Q2 revenue %s' % y, six, s, abs(six - s) < 1e-6))

# ---------- gate 2: 9M-current == Q1+Q2+Q3 --------------------------------
for y in ('2021','2022','2023','2024','2025'):
    qs = [y+'Q1', y+'Q2', y+'Q3']
    if all(q in R for q in qs):
        nine = R[y+'Q3']['_chk']['is_rev_all'][2]
        s = sum(R[q]['_chk']['is_rev_all'][0] for q in qs)
        gates.append(('9M=Q1+Q2+Q3 revenue %s' % y, nine, s, abs(nine - s) < 1e-6))

# ---------- gate 3: FY == 4 quarters (MD&A discrete revenue) --------------
for y in ('2021','2022','2023','2024','2025'):
    qs = [y+'Q1', y+'Q2', y+'Q3', y+'Q4']
    if all(q in R for q in qs):
        fy = R[y+'Q4']['_chk']['is_rev_all'][0]
        s = sum(R[q]['total_revenue'] for q in qs)
        gates.append(('FY=sum(4Q) revenue %s' % y, fy, s, abs(fy - s) < 1e-6))

# ---------- Q4 derivation: statement items = FY - 9M ----------------------
for y in ('2021','2022','2023','2024','2025'):
    q4, q3 = y+'Q4', y+'Q3'
    if q4 not in R or q3 not in R:
        continue
    a, b = R[q4], R[q3]
    fy_tax = abs(a['_chk']['cf_tax_all'][0]); nm_tax = abs(b['_chk']['cf_tax_all'][2])
    fy_lse = abs(a['_chk']['cf_lease_all'][0]); nm_lse = abs(b['_chk']['cf_lease_all'][2])
    a['_restated'] = []
    for key, fy, nm in (('cash_tax_paid', fy_tax, nm_tax), ('lease_payments', fy_lse, nm_lse)):
        if fy < nm:            # audited FY below the interim 9M -> company restated
            a[key] = None
            a['_restated'].append('%s FY=%s < 9M=%s' % (key, fy, nm))
            problems.append((q4, 'RESTATED: annual %s below interim 9M, Q4 not derivable' % key, fy, nm))
        else:
            a[key] = round(fy - nm, 3)
    # exploration comes from the MD&A table (printed discrete) - cross-check the derivation
    der = round(a['_chk']['is_expl_all'][0] - b['_chk']['is_expl_all'][2], 3)
    if abs(der - a['exploration_expensed']) > 1e-6:
        problems.append((q4, 'exploration: MD&A discrete != FY-9M', a['exploration_expensed'], der))
    a['net_income_attributable'] = a['_chk']['net_earnings_mdna']
    a['_derived'] = True

# ---------- cross-tie checks ---------------------------------------------
for q in QS:
    r, c = R[q], R[q]['_chk']
    if not r.get('_is_annual_only'):
        if abs(c['is_revenue'] - r['total_revenue']) > 1e-6:
            problems.append((q, 'IS revenue != MD&A total revenue', c['is_revenue'], r['total_revenue']))
        if abs(r['corporate_g_and_a'] - c['aisc_ga']) > 1e-6:
            problems.append((q, 'IS G&A != AISC-recon G&A', r['corporate_g_and_a'], c['aisc_ga']))
        if abs(abs(c['cf_capex']) - r['capex_total']) > 1e-6:
            problems.append((q, 'CF capex != MD&A total consolidated capex', c['cf_capex'], r['capex_total']))
        if abs(c['is_exploration'] - r['exploration_expensed']) > 1e-6:
            problems.append((q, 'IS exploration != MD&A exploration table', c['is_exploration'], r['exploration_expensed']))
    else:
        r['corporate_g_and_a'] = c['aisc_ga']
    if abs(c['gold_cos_total'] - c['aisc_anchor']) > 1e-6:
        problems.append((q, 'MD&A gold COS != AISC anchor', c['gold_cos_total'], c['aisc_anchor']))
    if abs(abs(c['aisc_byp']) - r['byproduct_credits']) > 1e-6:
        problems.append((q, 'Note6 Other sales != AISC by-product line', r['byproduct_credits'], c['aisc_byp']))
    if abs(c['aisc_oz'] * 1000 - r['gold_oz_sold']) > 1:
        problems.append((q, 'ounces mismatch', c['aisc_oz'], r['gold_oz_sold']))
    built = (c['gold_cos_total'] + c['aisc_depn'] + c['aisc_eqm'] + c['aisc_byp']
             + (c['aisc_hedge'] or 0) + (c['aisc_nonrec'] or 0) + c['aisc_other'] + c['aisc_nci'])
    if abs(built - c['aisc_tcc']) > 1.0:
        problems.append((q, 'TCC does not re-add', built, c['aisc_tcc']))

# ---------- reconstruction ------------------------------------------------
rows = []
for q in QS:
    r, c = R[q], R[q]['_chk']
    recon_m = (c['gold_cos_total']              # independent: MD&A gold cost-of-sales table
               - r['segment_dda']               # independent: same table
               + c['aisc_eqm']
               - r['byproduct_credits']         # independent: Note 6 / MD&A revenue table
               + (c['aisc_hedge'] or 0) + (c['aisc_nonrec'] or 0)
               + c['aisc_other'] + c['aisc_nci']
               + r['corporate_g_and_a']         # independent: income statement
               + c['aisc_expl']
               + c['sustaining_capex']          # independent: MD&A financial summary
               + c['aisc_leases'] + c['aisc_rehab'] + c['aisc_nciadj'])
    recon = recon_m * 1e6 / r['gold_oz_sold']
    resid = (recon - r['published_aisc']) / r['published_aisc'] * 100.0

    f = ['ONLY_CONSOLIDATED', 'KOZ_ROUNDED']
    if r.get('_derived'):
        f.append('DERIVED_Q4_STATEMENT')
    if r.get('_restated'):
        f.append('RESTATED')
    if r['published_aic'] is None:
        f.append('NO_AIC_PUBLISHED')
    if c.get('mining_prod_taxes') is None:
        f.append('ROYALTY_NO_PRODTAX_SPLIT')
    if abs(resid) > 2.0:
        f.append('AISC_RESIDUAL_GT_2PCT')

    y, qq = q[:4], q[4:]
    rows.append({
        'ticker': 'GOLD/B', 'quarter': q,
        'period_start': '%s-%s' % (y, YQ[qq][0]), 'period_end': '%s-%s' % (y, YQ[qq][1]),
        'basis': 'attributable',
        'segment_revenue_gold': r['segment_revenue_gold'],
        'segment_revenue_gold_consolidated': r['segment_revenue_gold_consolidated'],
        'total_revenue': r['total_revenue'],
        'opcost_ex_dda': r['opcost_ex_dda'], 'segment_dda': r['segment_dda'],
        'royalties': r['royalties'], 'corporate_g_and_a': r['corporate_g_and_a'],
        'exploration_expensed': r['exploration_expensed'], 'capex_total': r['capex_total'],
        'reclamation_accretion': r['reclamation_accretion'], 'lease_payments': r['lease_payments'] if r['lease_payments'] is not None else '',
        'net_interest': r['net_interest'], 'cash_tax_paid': r['cash_tax_paid'],
        'gold_oz_sold': r['gold_oz_sold'], 'gold_oz_produced': r['gold_oz_produced'],
        'published_aisc': r['published_aisc'], 'aisc_basis': 'by-product',
        'published_aic': r['published_aic'] if r['published_aic'] is not None else '',
        'byproduct_credits': r['byproduct_credits'],
        'net_income_attributable': r['net_income_attributable'],
        'recon_aisc': round(recon, 1), 'recon_residual_pct': round(resid, 3),
        'flags': ';'.join(f), 'source_file': r['source_file'],
    })

os.makedirs('data/interim', exist_ok=True)
with open('data/interim/GOLD_quarterly.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    for x in rows:
        w.writerow(x)

print('=== GATES ===')
for n, a, b, ok in gates:
    print('%-32s %12s %12s %s' % (n, a, b, 'PASS' if ok else '*** FAIL ***'))
print('\n=== CROSS-TIE PROBLEMS === (%d)' % len(problems))
for p in problems:
    print('  ', p)
print('\n=== RESIDUALS ===')
for x in rows:
    print('%-7s pub %7.1f  recon %7.1f  resid %+7.3f%%  %s' %
          (x['quarter'], x['published_aisc'], x['recon_aisc'], x['recon_residual_pct'],
           'OK' if abs(x['recon_residual_pct']) <= 2 else '<<< GT 2%'))
