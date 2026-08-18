"""Newmont (NEM) quarterly extractor — 2021Q1..2026Q2 -> data/interim/NEM_quarterly.csv

Run from the repo root:   python3 src/extract_nem.py

Sources are LOCAL files in data/raw/NEM only. Statement/segment/note figures come from
the filings inline-XBRL facts (period-dated contexts, so no column-guessing); MD&A and
non-GAAP tables (gold sales by metal, ounces, AISC) are parsed from the HTML tables.
Q4 = FY(10-K) - 9M(Q3 10-Q); Q4 AISC/ounces come straight from the Q4 8-K release.
"""

import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _nem_build import *

EXPL="us-gaap:ResultsOfOperationsExplorationExpense"; RD="us-gaap:ResearchAndDevelopmentExpense"
GNA="us-gaap:GeneralAndAdministrativeExpense"; IE="us-gaap:InterestIncomeExpenseNonoperatingNet"
II="us-gaap:InvestmentIncomeInterest"; ACC="us-gaap:AssetRetirementObligationAccretionExpense"
REM="us-gaap:AccretionExpense"; NI="us-gaap:NetIncomeLoss"
CAPX="us-gaap:PaymentsToAcquireProductiveAssets"; LEASE="us-gaap:FinanceLeasePrincipalPayments"
TAX="us-gaap:IncomeTaxesPaidNet"
ENV=("ProductOrServiceAxis=EnvironmentalRemediationMember",)
M={1:"March 31",2:"June 30",3:"September 30",4:"December 31"}
QS={1:"01-01",2:"04-01",3:"07-01",4:"10-01"}; QE={1:"03-31",2:"06-30",3:"09-30",4:"12-31"}

def fa(c,s,e,prefer=None,allow=()):
    v,src=find_any(c,s,e,allow=allow,prefer=prefer)
    if isinstance(v,str): raise SystemExit(f"{v} for {c} {s}..{e}")
    return v,src

def m(v): return None if v is None else round(v/1e6,3)

out=[]; used=set()
for y in range(2021,2027):
    for q in range(1,5):
        key=f"{y}Q{q}"
        if key not in Q10 and not (q==4 and y in K10): continue
        srcs=[]
        if q<4:
            f=R+Q10[key]; srcs.append(R+Q10[key])
            s,e=f"{y}-{QS[q]}",f"{y}-{QE[q]}"
            def D(c,allow=()):
                v,sc=fa(c,s,e,prefer=f,allow=allow); srcs.extend(sc); return v
            tot=D(REV); gr=tot-nongold_sum(f,REV,s,e)
            gc=D(CAS)-nongold_sum(f,CAS,s,e); gd=gold_seg(f,DDA,s,e)
            expl=D(EXPL); rd=D(RD); gna=D(GNA); ie=D(IE); ii=D(II)
            acc=D(ACC,ENV); ni=D(NI)
            ii_local = bool(plain2(f,II,s,e))
            ys,ye=f"{y}-01-01",f"{y}-{QE[q]}"
            pys,pye=(f"{y}-01-01",f"{y}-{QE[q-1]}") if q>1 else (None,None)
            capd,_=fa(CAPX,s,e,prefer=f)
            if capd is not None: cap=capd; capsrc='segnote_footnote_cash_basis'
            else:
                a,sa=fa(CAPX,ys,ye,prefer=f); b,sb=(fa(CAPX,pys,pye) if q>1 else (0.0,[]))
                cap=None if (a is None or b is None) else a-b; capsrc='ytd_minus_prior_ytd'; srcs+=sa+sb
            la,sa=fa(LEASE,ys,ye,prefer=f); lb,sb=(fa(LEASE,pys,pye) if q>1 else (0.0,[]))
            lease=None if (la is None or lb is None) else la-lb; srcs+=sa+sb
            ta,sa=fa(TAX,ys,ye,prefer=f); tb,sb=(fa(TAX,pys,pye) if q>1 else (0.0,[]))
            tax=None if (ta is None or tb is None) else ta-tb; srcs+=sa+sb
            aisc=aisc_row(f,f"Three Months Ended {M[q]}, {y}")
            cp,cs=highlights(f); ozp,ozs=cp[0]*1000,cs[0]*1000
            derived=(q>1)
        else:
            k=R+K10[y]; q3=R+Q10[f"{y}Q3"]; er=R+ER4[y]
            srcs+= [R+K10[y],R+Q10[f'{y}Q3'],R+ER4[y]]
            fs,fe=f"{y}-01-01",f"{y}-12-31"; ns,ne=f"{y}-01-01",f"{y}-09-30"
            def SUB(c,allow=()):
                a,_=fa(c,fs,fe,prefer=k,allow=allow); b,_=fa(c,ns,ne,prefer=q3,allow=allow)
                return None if (a is None or b is None) else a-b
            tot=SUB(REV)
            gr=(fa(REV,fs,fe,prefer=k)[0]-nongold_sum(k,REV,fs,fe))-(fa(REV,ns,ne,prefer=q3)[0]-nongold_sum(q3,REV,ns,ne))
            gc=(fa(CAS,fs,fe,prefer=k)[0]-nongold_sum(k,CAS,fs,fe))-(fa(CAS,ns,ne,prefer=q3)[0]-nongold_sum(q3,CAS,ns,ne))
            gd=gold_seg(k,DDA,fs,fe)-gold_seg(q3,DDA,ns,ne)
            expl=SUB(EXPL); rd=SUB(RD); gna=SUB(GNA); ie=SUB(IE); ii=SUB(II)
            acc=SUB(ACC,ENV); ni=SUB(NI); cap=SUB(CAPX); capsrc='fy_minus_9m'
            ii_local = bool(plain2(k,II,fs,fe)) and bool(plain2(q3,II,ns,ne))
            lease=SUB(LEASE); tax=SUB(TAX)
            aisc=aisc_row(er,f"Three Months Ended December 31, {y}")
            cpk,csk=highlights(k); cp3,cs3=highlights(q3)
            ozp,ozs=(cpk[0]-cp3[2])*1000,(csk[0]-cs3[2])*1000
            derived=True
        net_int = None if (ie is None) else ((-ie) - (ii if ii is not None else 0.0))
        ni_gross_flag = (ii is None)
        bp = byproduct_aisc(key)
        cred, credsrc = byproduct_credits(key)
        for extra in ([bp['src']] if bp else [])+[credsrc]:
            if extra not in srcs: srcs.append(extra)
        recon = published = resid = None
        if aisc and ozs:
            recon = sum(aisc[0:7])*1e6/ozs
            published = aisc[9]
            resid = (recon-published)/published*100
        flags=['ONLY_CONSOLIDATED']
        if q==4: flags.append('derived_q4')
        if derived: flags.append('derived_from_cumulative')
        flags.append('NOT_DISCLOSED:royalties')
        if tax is None: flags.append('NOT_DISCLOSED:cash_tax_paid')
        if ni_gross_flag: flags.append('NOT_DISCLOSED:interest_income')
        elif not ii_local: flags.append('INTEREST_INCOME_FROM_LATER_FILING')
        out.append(dict(ticker='NEM',quarter=key,period_start=f"{y}-{QS[q]}",period_end=f"{y}-{QE[q]}",
            basis='consolidated',
            segment_revenue_gold=m(gr), total_revenue=m(tot), opcost_ex_dda=m(gc), segment_dda=m(gd),
            royalties=None, corporate_g_and_a=m(gna), exploration_expensed=m((expl or 0)+(rd or 0)),
            capex_total=m(cap), reclamation_accretion=m(acc), lease_payments=m(lease),
            net_interest=m(net_int), cash_tax_paid=m(tax),
            gold_oz_sold=int(ozs), gold_oz_produced=int(ozp),
            published_aisc=published, aisc_basis='co-product',
            published_aisc_byproduct=bp['published'] if bp else None,
            published_aic=None, byproduct_credits=cred,
            net_income_attributable=m(ni),
            recon_aisc=None if recon is None else round(recon,1),
            recon_residual_pct=None if resid is None else round(resid,3),
            flags=';'.join(flags), source_file=';'.join(dict.fromkeys(srcs)), _capsrc=capsrc,
            _aisc_components=aisc))
json.dump(out, open('/tmp/claude-0/-home-user-agents/f3c15123-340b-5994-9540-4d134f7a1688/scratchpad/nem/final.json','w'), indent=1)
COLS=['ticker','quarter','period_start','period_end','basis','segment_revenue_gold','total_revenue',
 'opcost_ex_dda','segment_dda','royalties','corporate_g_and_a','exploration_expensed','capex_total',
 'reclamation_accretion','lease_payments','net_interest','cash_tax_paid','gold_oz_sold','gold_oz_produced',
 'published_aisc','aisc_basis','published_aisc_byproduct','published_aic','byproduct_credits','net_income_attributable','recon_aisc','recon_residual_pct',
 'flags','source_file']
import os
os.makedirs('data/interim',exist_ok=True)
with open('data/interim/NEM_quarterly.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=COLS,extrasaction='ignore'); w.writeheader()
    for r in out:
        w.writerow({c:('' if r[c] is None else r[c]) for c in COLS})
print("rows",len(out))
for r in out:
    print(f"{r['quarter']} resid={r['recon_residual_pct']:>7} co-product={r['published_aisc']:>6} by-product={r['published_aisc_byproduct']:>6} credits={r['byproduct_credits']:>6}")
