#!/usr/bin/env python3
"""Assemble the chart payload.

Two things this file refuses to do, because both would invent data:

1. It does not put half-yearly observations onto a quarterly axis. Gold Fields
   files financial statements twice a year and AngloGold stopped filing
   standalone quarterlies in 2016; splitting those into quarters is exactly the
   pro-rata the methodology forbids. Every observation therefore carries its own
   [x0, x1) span in months, and the axis is continuous months, not slots.

2. It does not compute the aggregate at a frequency finer than the slowest
   reporter in the selection. The aggregate buckets are HALF-YEARS, so a
   half-yearly filer contributes one whole observation and a quarterly filer
   contributes two -- six months of revenue either way, verified below.

Everything the front end needs to draw grade, bias and censoring is pushed here;
the page recomputes no thresholds of its own (DEGRADATION 9.5 item 7).
"""
import json
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
EPOCH = 2013
AGG_MIN_PANEL = 4   # below this many companies in a bucket the aggregate is not drawn

q = pd.read_csv(ROOT / "data/final/margins.csv")
a = pd.read_csv(ROOT / "data/final/margins_annual.csv")
audit = pd.read_csv(ROOT / "data/final/censoring_audit.csv")

# Position of each fidelity_vector character, so the tooltip can name the field
# that earned the grade instead of showing 13 anonymous letters.
FIELD_LABELS = ["黄金收入", "总收入", "营业成本", "权利金", "公司管理费", "费用化勘探",
                "资本开支", "复垦摊提", "租赁付款", "净利息", "实缴现金税",
                "一次性项目", "维护保养"]

META = {
    "NEM": {
        "name": "纽蒙特", "en": "Newmont Corporation", "cik": "0001164727",
        "exchange": "NYSE: NEM（美国本土申报人，US GAAP）",
        "forms": "10-Q（季度财务报表）· 10-K（年报）· 8-K 附件 EX-99.1（业绩新闻稿与经营统计表）",
        "revenue_src": "10-Q 管理层讨论「Consolidated sales:」表的 <b>Net</b> 行、Gold 列，科目原文 <b>Consolidated gold sales, net</b>。另由按矿山与金属拆分的收入附注独立验算。",
        "opcost_src": "利润表 <b>Costs applicable to sales</b>（附注声明已剔除折旧摊销与复垦），分部附注 Gold 各行加总",
        "aisc_note": "10-K/10-Q 头条为<b>共同产品</b>口径（按 GEO 牌价的相对销售价值分摊），8-K 另发<b>副产品</b>口径。2026 年起公司把指引改为副产品口径。两者差距在 2026Q1 达 66%。",
        "quirks": [
            "分部结构在窗口内变过两次：2023Q1 从「五大地理区域」改为「按矿山」，2023Q4 并入 Newcrest 后再调整，均已追溯重述。",
            "现金税 2024Q1 前无季度披露。2013–2023 由 10-K 审计年度数按季度黄金收入占比分摊，逐行打 <code>CASH_TAX_ALLOCATED_FROM_FY</code>。",
            "「归属口径」只有盎司数有，收入与成本各行<b>只有合并口径</b>，全行打 <code>ONLY_CONSOLIDATED</code>。",
            "内华达金矿（NGM）按 <b>38.5% 比例合并</b>；Barrick 则 100% 全额合并再挂少数股东权益。两家在这一点上永久不可比。",
            "白银单位在 2021 年报「千盎司」、2026 年报「百万盎司」，同一张表相差 762 倍——解析器按科目文字读单位，不用固定乘数。",
        ],
    },
    "GOLD": {
        "name": "巴里克", "en": "Barrick Mining Corporation", "cik": "0000756894",
        "exchange": "NYSE: B（2025年5月由 GOLD 改）· TSX: ABX（外国私募发行人，IFRS）",
        "forms": "6-K 附件 EX-99.1（新闻稿）与 EX-99.2（管理层讨论 + 简明中期财务报表）· 40-F（年报）",
        "revenue_src": "管理层讨论 <b>Revenues - as adjusted</b>（归属口径）。另在合并口径记 <b>Gold sales</b> 附注行。",
        "opcost_src": "附注 <b>Site operating costs</b>。注意：黄金 <b>Cost of sales</b> <u>包含</u>权利金，Site operating costs 才是不含的那行。",
        "aisc_note": "头条为<b>副产品</b>口径。其所谓「共同产品」经核实<b>只是把副产品抵扣加回去</b>，并未把联合成本分摊给副产品，因此<b>不可</b>与纽蒙特比较。2024Q2 后停止披露 AIC。",
        "quirks": [
            "报表有<b>四列</b>，管理层讨论的非GAAP表却是<b>五列</b>且第二列是<b>上一季</b>而非去年同季。解析器一律按表头文字定位，绝不按列序。",
            "Kibali（45%）与 Porgera（24.5%）<b>权益法核算</b>，收入不进合并报表，却<b>计入</b>公布 AISC 的归属盎司分母。",
            "2013–2016 的资本开支原先取自一个无法识别口径的来源（存 137.13，现金流量表为 270）。已按现金流量表重新提取，谷底 GAIM 因此下移 7.09 个百分点。",
            "2025Q1 起附注新增「Mining and production taxes」行，是<b>从 Site operating costs 里切出来的</b>。两者之和连续，GAIM 不受影响。",
            "2019Q1 Randgold 合并、2019Q3 内华达金矿合资<b>两处成分断裂</b>，前端在该处断线不连。",
        ],
    },
    "AEM": {
        "name": "艾格尼可鹰", "en": "Agnico Eagle Mines Limited", "cik": "0000002809",
        "exchange": "NYSE / TSX: AEM（外国私募发行人，IFRS，美元）",
        "forms": "6-K 两份 EX-99.1（管理层讨论 + 中期财务报表 / 新闻稿）· 40-F（年报）",
        "revenue_src": "<b>REVENUES FROM MINING OPERATIONS</b> 按金属拆分表的 <b>Gold</b> 行。原始单位千美元，已换算为百万美元。",
        "opcost_src": "利润表 <b>Production costs</b>（附注声明不含摊销）",
        "aisc_note": "同时公布副产品与「共同产品」两套，但其<b>「共同产品」同样只是把抵扣加回去</b>，成本一分未分摊给副产品。真正的收入加权共同产品由我们自行计算。",
        "quirks": [
            "AISC 分母是<b>产出</b>盎司而非销售盎司。已按各期实际产出/销售盎司逐行重述为销售口径——<b>此前这段代码从未真正执行过</b>（判定条件读的是首行的口径字符串），修正后 36 行移动，均值 −0.56 个百分点。",

            "三次追溯重述：IAS 16 试生产收入、Kirkland Lake 与 Yamana 购买价格分摊。一律采用<b>最新版本</b>。",
            "2022Q1 为 <b>52 天存根季度</b>（Kirkland Lake 于 2月8日并表），打 <code>STUB_QUARTER</code>，不做平滑掩盖。",
            "同一份文件里「Total Capital Expenditures」有<b>三个不同数字</b>，相差 14%。按方法论取现金流量表口径。",
            "复垦摊提被<b>捆在 Finance costs 里</b>，记 null 而非 0，避免与净利息重复计算。",
        ],
    },
    "KGC": {
        "name": "金罗斯", "en": "Kinross Gold Corporation", "cik": "0000701818",
        "exchange": "NYSE: KGC / TSX: K（外国私募发行人，IFRS，美元）",
        "forms": "6-K 附件 EX-99.x（新闻稿 + 管理层讨论 + 中期财务报表）· 40-F（年报）",
        "revenue_src": "利润表 <b>Metal sales</b> 减去管理层讨论披露的 <b>silver revenue</b>——两个已披露行相减，绝非「价格×盎司」倒推。",
        "opcost_src": "利润表 <b>Production cost of sales</b>",
        "aisc_note": "头条为<b>黄金当量（GEO）</b>口径，公司称之为 co-product accounting——这在代数上成立。<b>金罗斯与纽蒙特是本组仅有的两家真正披露共同产品重述的公司。</b>但换算比价四个季度内从 97.41:1 摆到 57.79:1。",
        "quirks": [
            "<b>无按金属拆分的收入附注</b>，金/银拆分只存在于管理层讨论的非GAAP对账里。",
            "<code>gold_oz_produced</code> 列装的是 <b>GEO</b>——金罗斯全文未披露纯黄金产量，全行打 <code>GEO_BASIS</code>。",
            "2022Q1–2023Q3 为<b>终止经营列报</b>：俄罗斯资产 2022Q1 移出、Chirano 2022Q2 才移出——<b>2022Q1 被重述了两次</b>。",
            "Finance expense 虽是毛捆绑，但金罗斯<b>把它拆开了</b>，净利息与复垦摊提可分别取用，既穷尽又不重叠。",
            "白银占金属销售 0.59%–5.91%（均值 2.84%），远低于外部资料常引用的约 8%。",
        ],
    },
    "AU": {
        "name": "安格鲁黄金", "en": "AngloGold Ashanti plc", "cik": "0001067428 → 0001973832",
        "exchange": "NYSE: AU · JSE（外国私募发行人，IFRS，美元）",
        "forms": "2013–2015：6-K 季度报告 · 2016 起：6-K <b>半年报</b>（Q1/Q3 只有产量与 AISC 的运营更新，没有成本表）· 20-F 年报",
        "revenue_src": "利润表 <b>Revenue</b> 与分部附注的黄金收入行，合并口径（<code>ONLY_CONSOLIDATED</code>）。",
        "opcost_src": "<b>Cost of sales</b> 附注。<b>权利金已含在其中</b>——见下。",
        "aisc_note": "<b>本公司的 AISC 利润率在 2013Q1–2022H2 整段被撤回、不予发布。</b>公布 AISC 的分母是<b>归属口径且含权益法合资企业</b>的盎司与收入，而我们的黄金收入是<b>合并口径、不含权益法</b>。2014Q4 6-K 原文：利润表「Gold income 1,278」、分部附注「Equity-accounted investments included above (142)」，而 AISC 附录是「Attributable gold income ... 1,407」÷「Attributable gold sold - oz (000) 1,171」，公司自报 Price received $1,202，我们算出来是 $1,091。拿归属口径的 AISC 去除合并口径的价格，利润率被压低 4.9–23.8 个百分点。正确的分母公司披露了，但尚未提取，因此<b>宁可留空也不发布一个已知错误的数</b>。2023Q1 起公司自身口径变更，两者一致，从该期起恢复发布。原公布 AISC 为<b>归属口径且包含权益法合资企业</b>，而收入与成本是合并口径。我们自建的对账式沿用本行自己的合并口径字段，因此与公司公布值之间存在<b>两个方向相反的已知缺口</b>：（1）用全部资本开支而非维持性资本开支（推高），（2）漏掉合资企业按比例的成本与资本开支加项（压低，且实测占优）。<b>残差未做调平，按算出来的原样报告。</b>",
        "quirks": [
            "<b>我曾两次断言这家公司空着的权利金与复垦列在静默漏掉成本、每行值 3.9–4.6 个百分点、是面板最大的单一缺陷。这是错的。</b>派去修它的任务从 Cost of sales 附注提出了 8 个期间的真实权利金再从营业成本里减掉，GAIM 变动的行数<b>为零</b>——证明权利金本来就在营业成本里面。错因是判定「哪些字段已被别行包含」的白名单只按四家公司标定过，安格鲁与金田从来不在其中。",
            "2016 年起停发独立季报：41 行中 13 行为<b>半年</b>观测，画在图上占六个月宽度，不拆成季度。",
            "Obuasi 于 2015Q2 重分类为终止经营且<b>前期未重述</b>，该处强制序列断点。",
            "Sukari 金矿按 <b>100% 合并</b>，而安格鲁只持有 50%。",
            "2023 年迁册英国，CIK 由 1067428 变为 1973832，取数需缝合双 CIK。",
        ],
    },
    "GFI": {
        "name": "金田", "en": "Gold Fields Limited", "cik": "0001172724",
        "exchange": "NYSE: GFI · JSE（外国私募发行人，IFRS，美元）",
        "forms": "6-K 半年度与全年业绩公告 · 20-F 年报。<b>不发季度财务报表</b>。",
        "revenue_src": "收入表的黄金行，<b>已扣除副产品收入</b>（<code>GOLD_REV_NET_OF_BYPRODUCT_REVENUE</code>）。",
        "opcost_src": "<b>Cost of sales</b>，为<b>含公司管理费的总额</b>口径。",
        "aisc_note": "AISC 与 AIC 均按 WGC 口径公布，但 H2 的每盎司数多数由「全年减上半年」倒算。Cerro Corona 用<b>黄金当量盎司</b>，内嵌一个漂移的价格比。",
        "quirks": [
            "<b>本组唯一的半年度申报人</b>：32 行中 20 行为半年观测。这是把整个面板的聚合频率定在半年的原因——把金田拆成季度就是方法论明令禁止的插值。",
            "<b>公司管理费追不到出处。</b>六个数值散落三份文件，没有一处有科目标题。已从成本堆栈中撤出，另存 <code>corporate_g_and_a_unsourced</code> 列并打 <code>PROVENANCE_UNRESOLVED</code>。撤出使金田 GAIM <b>上升</b>约 1.73 个百分点——这是对我们有利的方向，故明说。",
            "另有 21 行在一个<b>描述性</b>标志里写明营业成本是含管理费的总额，但没有任何代码读那个标志。已将其中 17 行转为机器可读的 <code>TIERAEQ:corporate_g_and_a:BUNDLED_IN_OPCOST_GROSS</code>。",
            "2013 年两行的营业成本原为「净额」口径，重述为总额后，管理费与复垦成为<b>备查子集</b>，若再相加即双重计算，故单独存放。",
            "公司自行披露 2018 年末现金流量表存在<b>内部控制重大缺陷</b>（成本截止日为 12月21日）。该年的资本开支与现金税取自这张报表。",
        ],
    },
}

HUE = {"NEM": ("#2a78d6", "#4b95ea"), "GOLD": ("#eb6834", "#f5804f"),
       "AEM": ("#1baf7a", "#2fc78f"), "KGC": ("#eda100", "#f2b62e"),
       "AU": ("#8d54c9", "#a679dd"), "GFI": ("#c2334f", "#dc5570")}
ORDER = ["NEM", "GOLD", "AEM", "AU", "KGC", "GFI"]
# Short display name: "Gold Fields Limited".split()[0] is "Gold", which is not a
# company. Spell them out rather than deriving them.
SHORT = {'NEM': 'Newmont', 'GOLD': 'Barrick', 'AEM': 'Agnico Eagle', 'KGC': 'Kinross', 'AU': 'AngloGold Ashanti', 'GFI': 'Gold Fields'}


def span(period):
    """(x0, x1) in months since EPOCH-01. Q spans 3, H spans 6, FY spans 12."""
    year, kind = int(period[:4]), period[4]
    if kind == "F":                       # '2005FY' -- Kinross filed nothing
        x0 = (year - EPOCH) * 12          # interim that year, so the audited
        return x0, x0 + 12                # annual IS the observation
    n = int(period[5:])
    width = 3 if kind == "Q" else 6
    x0 = (year - EPOCH) * 12 + (n - 1) * width
    return x0, x0 + width


def half_of(period):
    """Half-year bucket, or None for a period that cannot sit in one."""
    year, kind = int(period[:4]), period[4]
    if kind == "F":
        return None                       # 12 months does not go in a 6-month
    n = int(period[5:])                   # bucket without the split we refused
    return f"{year}H{n if kind == 'H' else (1 if n <= 2 else 2)}"


def num(v, nd=2):
    return None if pd.isna(v) else round(float(v), nd)


# --- invariant: the label's implied span must equal the row's own month count.
bad = [(r.ticker, r.quarter) for r in q.itertuples()
       if (span(r.quarter)[1] - span(r.quarter)[0]) != int(r.months)]
if bad:
    raise SystemExit(f"period label disagrees with months column: {bad[:5]}")

q = q.assign(half=q.quarter.map(half_of))

# A (ticker, half) bucket that does not total six months cannot be weighted
# against one that does -- a company contributing a single quarter would count
# as a full half of industry activity. Until 2005-2012 landed this could not
# happen, so it was an assert. It happens now for real reasons: Agnico's
# 2008Q2 and Q3 filings do not exist, Kinross has no 2005 interim at all, and
# an annual row has no half. Excluding those buckets from the AGGREGATE is
# right; crashing the build over them is not, and neither is silently
# weighting three months as six. The observations still draw on the company
# line -- only the aggregate declines to use them.
# Months of USABLE data, not months of existing rows. Agnico emits a row for
# 2008Q2 and 2008Q3 even though no filing exists -- correctly, since the period
# is real and the nulls are the honest record -- so a bucket can look complete
# while only one of its two quarters carries a margin. Counting row months
# would let one quarter stand in for a whole half of industry activity.
q["_usable_months"] = q.months.where(q.L1.notna(), 0)
covered = q.groupby(["ticker", "half"])._usable_months.transform("sum")
q["partial_half"] = q.half.notna() & (covered != 6)
n_partial = int(q.partial_half.sum())
if n_partial:
    by = (q[q.partial_half].groupby("ticker").quarter
          .agg(lambda s: f"{len(s)} ({s.min()}..{s.max()})").to_dict())
    print(f"partial half-year buckets excluded from the aggregate: {n_partial} rows  {by}")
n_annual = int(q.half.isna().sum())
if n_annual:
    print(f"annual rows carried on the company line, outside every half bucket: {n_annual}")

halves = sorted([h for h in q.half.dropna().unique()],
                key=lambda h: (int(h[:4]), int(h[5])))
audit_by_period = audit.set_index("quarter")

series = []
for t in ORDER:
    g = q[q.ticker == t].copy()
    ga = a[a.ticker == t]
    m = META[t]
    obs = []
    for r in g.itertuples():
        x0, x1 = span(r.quarter)
        flags = str(getattr(r, "flags", "") or "")
        obs.append({
            "p": r.quarter, "h": None if pd.isna(r.half) else r.half,
            "x0": x0, "x1": x1, "f": r.freq,
            # Excluded from the aggregate, still drawn: the half is incomplete
            # for this company, or the row is a 12-month annual.
            "part": bool(r.partial_half),
            "l1": num(r.L1), "l2": num(r.L2), "l0a": num(r.L0a),
            "l0b": num(r.L0b), "l0badj": num(r.L0b_adj), "aisc": num(r.aisc_margin),
            "grade": r.fidelity_grade, "vec": r.fidelity_vector,
            "bias": num(r.bias_pt_central), "biasLo": num(r.bias_pt_lo),
            "biasHi": num(r.bias_pt_hi),
            "out": bool(r.is_outlier), "hl": bool(r.in_headline_aggregate),
            # SERIES_BREAK means "do not connect this point to the previous one":
            # the entity or the basis changed underneath the series.
            "brk": "SERIES_BREAK" in flags,
            "rev": num(r.gold_revenue, 1), "cost": num(r.gold_cost_total, 1),
            "ni": num(r.net_income_attributable, 1), "trev": num(r.total_revenue, 1),
            "oz": None if pd.isna(r.gold_oz_sold) else int(r.gold_oz_sold),
            "price": num(r.realised_price, 0), "aiscUsd": num(r.aisc_comparable, 0),
            "imp": num(r.impairment_charges, 1),
        })
    series.append({
        "id": t, "name": m["name"], "en": m["en"], "short": SHORT[t],
        "light": HUE[t][0], "dark": HUE[t][1],
        "cik": m["cik"], "exchange": m["exchange"], "forms": m["forms"],
        "revenueSrc": m["revenue_src"], "opcostSrc": m["opcost_src"],
        "aiscNote": m["aisc_note"], "quirks": m["quirks"],
        "obs": obs,
        "freqMix": {k: int(v) for k, v in g.freq.value_counts().items()},
        "grades": {k: int(v) for k, v in g.fidelity_grade.value_counts().items()},
        "meanGaim": round(g.L1.mean(), 1), "meanAisc": round(g.aisc_margin.mean(), 1),
        "gap": round((g.aisc_margin - g.L1).mean(), 1),
        "years": [int(y) for y in ga.year],
        "aL1": [num(v) for v in ga.L1], "aL0": [num(v) for v in ga.L0a],
        "aAisc": [num(v) for v in ga.aisc_margin],
        "aPrice": [num(v, 0) for v in ga.realised_price],
        "aComplete": [bool(v) for v in ga.complete],
    })

# Censoring strip, one entry per reporting period actually present in the panel.
strip = []
for p in sorted(q.quarter.unique(), key=lambda s: span(s)[0]):
    row = audit_by_period.loc[p] if p in audit_by_period.index else None
    x0, x1 = span(p)
    strip.append({
        "p": p, "x0": x0, "x1": x1,
        "n": int(row.companies_covered) if row is not None else 0,
        "ex": int(row.companies_excluded) if row is not None else 0,
        "exT": None if row is None or pd.isna(row.excluded_tickers) else row.excluded_tickers,
        "distress": bool(row.sector_distress_diagnostic) if row is not None else False,
        "breach": int(row.companies_breaching_aisc_cap) if row is not None else 0,
    })

# Headline aggregate: outliers trimmed AND X-grade rows dropped. in_headline_
# aggregate existed as a column that nothing read, so 22 rows the fidelity rules
# call unpublishable were sitting inside the headline number.
kept = q[~q.is_outlier & q.in_headline_aggregate]
eras = []
for lo, hi, label in [(2013, 2016, "2013–2016 谷底"), (2017, 2020, "2017–2020 复苏"),
                      (2021, 2026, "2021–2026 牛市")]:
    e = kept[(kept.quarter.str[:4].astype(int) >= lo) & (kept.quarter.str[:4].astype(int) <= hi)]
    gaim = (e.gold_revenue - e.gold_cost_total).sum() / e.gold_revenue.sum() * 100
    # Weight AISC over the revenue that HAS an AISC. Leaving AISC-less revenue in
    # the denominator silently scores those periods as a zero AISC margin.
    ea = e[e.aisc_margin.notna()]
    aisc = (ea.aisc_margin * ea.gold_revenue).sum() / ea.gold_revenue.sum()
    eras.append({"label": label, "lo": lo, "hi": hi, "n": len(e),
                 "n_aisc": len(ea), "gaim": round(gaim, 2), "aisc": round(aisc, 2),
                 "gap": round(aisc - gaim, 1)})

payload = {
    "epoch": EPOCH,
    # Both ends, not just the far one. The front end used to scale x as
    # m / xmax, which silently assumes the series starts at the epoch. It did
    # while the panel began in 2013Q1 (x0 = 0). The 2005-2012 extraction makes
    # 2005Q1 map to -96, and every one of those points would have been drawn
    # off the left edge of the plot area, on top of the y-axis labels.
    "xmin": min(span(p)[0] for p in q.quarter),
    "xmax": max(span(p)[1] for p in q.quarter),
    "halves": halves, "aggMinPanel": AGG_MIN_PANEL,
    "series": series, "strip": strip, "eras": eras,
    "fieldLabels": FIELD_LABELS,
    "n": len(q), "nCo": q.ticker.nunique(), "nPeriods": q.quarter.nunique(),
    "first": min(q.quarter, key=lambda s: span(s)[0]),
    "last": max(q.quarter, key=lambda s: span(s)[0]),
    "nOutlier": int(q.is_outlier.sum()),
    "gradeCounts": {k: int(v) for k, v in q.fidelity_grade.value_counts().items()},
    "nAB": int(q.fidelity_grade.isin(["A", "B"]).sum()),
    "biasMean": round(q.bias_pt_central.mean(), 2),
    "biasMax": round(q.bias_pt_central.max(), 2),
    # L0b_adj differs from L0b on 5 rows. The column exists; the extraction
    # behind it does not, and a chart that draws the two as separate layers
    # would claim an impairment-stripping pass nobody has run.
    "nAdj": int((q.L0b_adj - q.L0b).abs().gt(1e-9).sum()),
    "meanGap": round((q.aisc_margin - q.L1).mean(), 1),
}
(ROOT / "charts").mkdir(exist_ok=True)
blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
(ROOT / "charts/data.json").write_text(blob)

# The page is a single self-contained file: src/page.html is the template, the
# payload is inlined at build time. Keeping the template separate is what makes
# the build re-runnable -- inlining into the source would consume the
# placeholder and the next run would have nothing to substitute.
tpl = (ROOT / "src/page.html").read_text()
if tpl.count("__DATA__") != 1:
    raise SystemExit(f"src/page.html has {tpl.count('__DATA__')} placeholders, expected 1")
(ROOT / "charts/gold_margins.html").write_text(tpl.replace("__DATA__", blob))
print(f"series {len(series)}  observations {payload['n']}  "
      f"periods {payload['nPeriods']} ({payload['first']}..{payload['last']})  "
      f"aggregate buckets {len(halves)} half-years")
print(f"grades {payload['gradeCounts']}  A/B rows {payload['nAB']}  "
      f"outliers {payload['nOutlier']}  bias mean {payload['biasMean']}pt")
for e in eras:
    print(f"  {e['label']}  n={e['n']:3d}  GAIM {e['gaim']:6.2f}%  "
          f"AISC {e['aisc']:6.2f}%  gap {e['gap']:.1f}pt")
