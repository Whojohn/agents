#!/usr/bin/env python3
"""Assemble the chart payload: quarterly series, annual series, and per-company
source/method metadata for the collapsible appendix."""
import json
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
q = pd.read_csv(ROOT / "data/final/margins.csv")
a = pd.read_csv(ROOT / "data/final/margins_annual.csv")

META = {
    "NEM": {
        "name": "纽蒙特", "en": "Newmont Corporation", "cik": "0001164727",
        "exchange": "NYSE: NEM（美国本土申报人）",
        "forms": "10-Q（季度财务报表）· 10-K（年报）· 8-K 附件 EX-99.1（业绩新闻稿与经营统计表）",
        "revenue_src": "10-Q 管理层讨论与分析「Consolidated sales:」表的 <b>Net</b> 行、Gold 列，科目原文 <b>Consolidated gold sales, net</b>。另由 Note 5 按矿山与金属拆分的收入附注独立验算，22 个季度差额均为 0。",
        "opcost_src": "利润表 <b>Costs applicable to sales</b>（附注声明已剔除折旧摊销与复垦），分部附注 Gold 各行加总",
        "aisc_note": "10-K/10-Q 头条为<b>共同产品</b>口径（按 GEO 牌价的相对销售价值分摊），8-K 另发<b>副产品</b>口径。2026 年起公司把指引改为副产品口径。两者差距在 2026Q1 达 66%。",
        "quirks": [
            "分部结构在窗口内变过两次：2023Q1 从「五大地理区域」改为「按矿山」，2023Q4 并入 Newcrest 后再调整，均已追溯重述。但 2021–2022 的 10-Q 自愿披露了矿山层明细，所以矿山层面板是连续的。",
            "现金税 2024Q1 前无季度披露。2021–2023 由 10-K 审计年度数（1,534 / 1,122 / 794 百万美元）按季度黄金收入占比分摊，逐行打 <code>CASH_TAX_ALLOCATED_FROM_FY</code> 标志。",
            "「归属口径」只有盎司数有，收入与成本各行<b>只有合并口径</b>，全行打 <code>ONLY_CONSOLIDATED</code>。",
            "内华达金矿（NGM）按 <b>38.5% 比例合并</b>；Barrick 则 100% 全额合并再挂少数股东权益。两家在这一点上永久不可比。",
            "白银单位在 2021 年报「千盎司」、2026 年报「百万盎司」，同一张表相差 762 倍——解析器按科目文字读单位，不用固定乘数。",
        ],
    },
    "GOLD": {
        "name": "巴里克", "en": "Barrick Mining Corporation", "cik": "0000756894",
        "exchange": "NYSE: B（2025年5月由 GOLD 改）· TSX: ABX（外国私募发行人）",
        "forms": "6-K 附件 EX-99.1（新闻稿）与 EX-99.2（管理层讨论 + 简明中期财务报表）· 40-F（年报）",
        "revenue_src": "管理层讨论 <b>Revenues - as adjusted</b>（归属口径，2026Q1 = 3,607 百万美元）。另在合并口径记 Note 6 <b>Gold sales</b>（4,756）。",
        "opcost_src": "Note 7 <b>Site operating costs</b>。注意：黄金 <b>Cost of sales</b> <u>包含</u>权利金，Site operating costs 才是不含的那行——22 个季度用恒等式验证。",
        "aisc_note": "头条为<b>副产品</b>口径。其所谓「共同产品」经核实<b>只是把副产品抵扣加回去</b>，并未把联合成本分摊给副产品，因此<b>不可</b>与纽蒙特、自由港的真共同产品数字比较。2024Q2 后停止披露 AIC，改用 AISC 对账。",
        "quirks": [
            "报表有<b>四列</b>（本季/去年同季/本半年/去年同半年），管理层讨论的非GAAP表却是<b>五列</b>且第二列是<b>上一季</b>而非去年同季。同一份文件里「第二列」有两种含义——解析器一律按表头文字定位，绝不按列序。",
            "Kibali（45%）与 Porgera（24.5%）<b>权益法核算</b>，收入完全不进合并报表，却<b>计入</b>公布 AISC 的归属盎司分母。因此只有已对账的归属收入口径与之自洽。",
            "2025Q1 起 Note 7 新增「Mining and production taxes」行，是<b>从 Site operating costs 里切出来的</b>，不是从 Royalty expense。故 2025Q1 前后 royalties 单列不可比，但两者之和连续，GAIM 不受影响。",
            "2025Q4 租赁付款为空：审计年度数 12 小于九个月数 20，倒算为 −8，不成立。公司做了重述，该格留空而非强填 0。",
            "盎司数<b>只披露到千盎司</b>，任何每盎司指标含最多 ±0.07% 的舍入。",
        ],
    },
    "AEM": {
        "name": "艾格尼可鹰", "en": "Agnico Eagle Mines Limited", "cik": "0000002809",
        "exchange": "NYSE / TSX: AEM（外国私募发行人，IFRS，美元）",
        "forms": "6-K 两份 EX-99.1（其一为管理层讨论 + 中期财务报表，其二为新闻稿）· 40-F（年报，含 EX-99.2 审计报表、EX-99.3 年度管理层讨论）",
        "revenue_src": "Note 14（2026）/ Note 16（2021）<b>REVENUES FROM MINING OPERATIONS</b> 按金属拆分表的 <b>Gold</b> 行。原始单位为千美元，已换算为百万美元。",
        "opcost_src": "利润表 <b>Production costs</b>（2026，COST OF SALES 块内）/ <b>Production</b>（2021，附注声明不含摊销）",
        "aisc_note": "同时公布副产品与「共同产品」两套，但其<b>「共同产品」同样只是把抵扣加回去</b>，成本一分未分摊给副产品、分母仍是纯黄金盎司。真正的收入加权共同产品由我们自行计算：2026Q2 为 1,511 美元/盎司，公司公布的「共同产品」1,534 高估黄金 23.6 美元/盎司。",
        "quirks": [
            "AISC 分母是<b>产出</b>盎司而非销售盎司，全行打 <code>AISC_PER_PRODUCED</code>。22 个季度产出与销售差距均值 +0.91%、区间 −4.89%~+3.53%，<b>有符号且均值回归</b>，不能用单一系数换算。其中约六成是三个矿山实物权利金造成的定义性楔子（Canadian Malartic 5%、Detour Lake 2%、Macassa 1.5%）。",
            "2021 年 AISC 的分母科目叫 <b>Adjusted gold production</b>（剔除试生产盎司），2022 年起改叫 <b>Gold production</b>。逐年读表头，不假设。",
            "三次追溯重述：IAS 16 试生产收入（2021 全年收入 +1.90%）、Kirkland Lake 购买价格分摊、Yamana / Canadian Malartic 购买价格分摊。一律采用<b>最新版本</b>。",
            "2022Q1 为 <b>52 天存根季度</b>（Kirkland Lake 于 2月8日并表），打 <code>STUB_QUARTER</code>，不做平滑掩盖。",
            "同一份文件里「Total Capital Expenditures」有<b>三个不同数字</b>：现金流量表 809.3、管理层讨论 800.9（含资本化勘探）、新闻稿 699.2（不含）——相差 14%。按方法论取现金流量表口径。",
            "复垦摊提被<b>捆在 Finance costs 里</b>，无法单列，故记 null 而非 0，避免与净利息重复计算。",
        ],
    },
    "KGC": {
        "name": "金罗斯", "en": "Kinross Gold Corporation", "cik": "0000701818",
        "exchange": "NYSE: KGC / TSX: K（外国私募发行人，IFRS，美元）",
        "forms": "6-K 附件 EX-99.x（新闻稿 + 管理层讨论 + 中期财务报表）· 40-F（年报）",
        "revenue_src": "利润表 <b>Metal sales</b> 减去管理层讨论第11节的 <b>silver revenue</b>——两个已披露行相减，绝非「价格×盎司」倒推。验证：所得除以黄金销售盎司，与公司公布的平均实现金价在 22 个季度内偏差均 ≤0.036%。",
        "opcost_src": "利润表 <b>Production cost of sales</b>",
        "aisc_note": "头条为<b>黄金当量（GEO）</b>口径，公司自己称之为 co-product accounting——这在代数上成立：按现货比价把白银折入分母，等价于按相对收入分摊联合成本（验证：486,507 + 771,000÷61.61 = 499,021 ≈ 公布的 499,035）。<b>因此金罗斯与纽蒙特是本组仅有的两家真正披露共同产品重述的公司。</b>但换算比价四个季度内从 97.41:1 摆到 57.79:1，波动 68%。",
        "quirks": [
            "<b>无 IFRS 15 按金属拆分附注</b>，利润表只有一行 Metal sales，分部附注只按矿山拆。金/银拆分只存在于管理层讨论的非GAAP对账里，且专门的 <b>Attributable gold revenue</b> 表 2024Q4 才出现。",
            "<code>gold_oz_produced</code> 列装的是 <b>GEO</b>——金罗斯全文未披露纯黄金产量。全行打 <code>GEO_BASIS</code>。",
            "2022Q1–2023Q3 为<b>终止经营列报</b>：俄罗斯资产于 2022Q1 移出持续经营，Chirano 在 2022Q1 报表里<b>仍在</b>持续经营、2022Q2 才移出——<b>2022Q1 被重述了两次</b>（Metal sales 768.0 → 700.9）。2021 全年从 3,729.4 重述为 2,599.6。",
            "Finance expense 是毛捆绑，但金罗斯<b>把它拆开了</b>，所以净利息取利息行、复垦摊提单独取，既穷尽又不重叠。",
            "白银占金属销售 0.59%–5.91%（均值 2.84%），远低于外部资料常引用的约 8%。",
            "无单独的勘探科目——利润表行为 <b>Exploration and business development</b>，且其定义在 2022Q2–2024Q4 间漂移过。取整行并标注，宁可口径略宽也不要口径不一致。",
        ],
    },
}

HUE = {"NEM": ("#2a78d6", "#3987e5"), "GOLD": ("#eb6834", "#d95926"),
       "AEM": ("#1baf7a", "#199e70"), "KGC": ("#eda100", "#c98500")}
ORDER = ["NEM", "GOLD", "AEM", "KGC"]

quarters = sorted(q.quarter.unique())
years = sorted(a.year.unique())


def col(g, idx, key, keys):
    m = g.set_index(key)
    return [None if idx_v not in m.index or pd.isna(m[keys].get(idx_v)) else round(float(m[keys].get(idx_v)), 2)
            for idx_v in idx]


series = []
for t in ORDER:
    gq, ga = q[q.ticker == t], a[a.ticker == t]
    m = META[t]
    series.append({
        "id": t, "name": m["name"], "en": m["en"], "light": HUE[t][0], "dark": HUE[t][1],
        "cik": m["cik"], "exchange": m["exchange"], "forms": m["forms"],
        "revenueSrc": m["revenue_src"], "opcostSrc": m["opcost_src"],
        "aiscNote": m["aisc_note"], "quirks": m["quirks"],
        "l1": col(gq, quarters, "quarter", "L1"), "l2": col(gq, quarters, "quarter", "L2"),
        # revenue and cost totals let the page re-aggregate any company subset
        "rev": col(gq, quarters, "quarter", "gold_revenue"),
        "cost": col(gq, quarters, "quarter", "gold_cost_total"),
        "aiscUsd": col(gq, quarters, "quarter", "aisc_comparable"),
        "oz": [None if pd.isna(v) else int(v) for v in
               (gq.set_index("quarter").gold_oz_sold.reindex(quarters))],
        "aRev": col(ga, years, "year", "gold_revenue"),
        "l0": col(gq, quarters, "quarter", "L0a"), "aisc": col(gq, quarters, "quarter", "aisc_margin"),
        "price": col(gq, quarters, "quarter", "realised_price"),
        "aL1": col(ga, years, "year", "L1"), "aL0": col(ga, years, "year", "L0a"),
        "aAisc": col(ga, years, "year", "aisc_margin"), "aPrice": col(ga, years, "year", "realised_price"),
        "meanGaim": round(gq.L1.mean(), 1), "meanAisc": round(gq.aisc_margin.mean(), 1),
        "gap": round((gq.aisc_margin - gq.L1).mean(), 1),
        "residMean": round(gq.recon_residual_pct.abs().mean(), 3),
        "residMax": round(gq.recon_residual_pct.abs().max(), 3),
    })

payload = {
    "quarters": quarters, "years": [int(y) for y in years], "series": series,
    "partialYear": int(a[~a.complete].year.max()) if (~a.complete).any() else None,
    "meanGap": round((q.aisc_margin - q.L1).mean(), 1),
    "meanAisc": round(q.aisc_margin.mean(), 1), "meanGaim": round(q.L1.mean(), 1),
    "n": len(q), "nCo": q.ticker.nunique(),
}
(ROOT / "charts").mkdir(exist_ok=True)
(ROOT / "charts/data.json").write_text(json.dumps(payload, ensure_ascii=False))
print(f"quarters {len(quarters)}  years {len(years)}  series {len(series)}  "
      f"partial year {payload['partialYear']}  mean gap {payload['meanGap']}")
