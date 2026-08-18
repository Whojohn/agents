#!/usr/bin/env python3
"""Render the margin series as a self-contained HTML page with inline SVG."""
import json, pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
d = pd.read_csv(ROOT/"data/final/margins.csv")
NAMES = {"NEM":"Newmont","GOLD":"Barrick","AEM":"Agnico Eagle","KGC":"Kinross"}
HUE_L = {"NEM":"#2a78d6","GOLD":"#eb6834","AEM":"#1baf7a","KGC":"#eda100"}
HUE_D = {"NEM":"#3987e5","GOLD":"#d95926","AEM":"#199e70","KGC":"#c98500"}
order = ["NEM","GOLD","AEM","KGC"]
quarters = sorted(d.quarter.unique())

series = []
for t in order:
    g = d[d.ticker==t].set_index("quarter")
    series.append({
        "id": t, "name": NAMES[t], "light": HUE_L[t], "dark": HUE_D[t],
        "l1":[None if pd.isna(g.L1.get(q)) else round(g.L1.get(q),2) for q in quarters],
        "l2":[None if pd.isna(g.L2.get(q)) else round(g.L2.get(q),2) for q in quarters],
        "l0":[None if pd.isna(g.L0a.get(q)) else round(g.L0a.get(q),2) for q in quarters],
        "aisc":[None if pd.isna(g.aisc_margin.get(q)) else round(g.aisc_margin.get(q),2) for q in quarters],
        "price":[None if pd.isna(g.realised_price.get(q)) else round(g.realised_price.get(q)) for q in quarters],
        "mean_gaim": round(g.L1.mean(),1), "mean_aisc": round(g.aisc_margin.mean(),1),
        "gap": round((g.aisc_margin-g.L1).mean(),1),
    })
payload = {"quarters":quarters, "series":series,
           "meanGap": round((d.aisc_margin-d.L1).mean(),1),
           "n": len(d), "nCo": d.ticker.nunique()}
(ROOT/"charts").mkdir(exist_ok=True)
(ROOT/"charts/data.json").write_text(json.dumps(payload))
print("quarters",len(quarters),"series",len(series),"mean gap",payload["meanGap"])
