# 2005–2012 时代的科目锚点普查（实测，非推测）

**方法**：对 `data/raw/` 中 2005–2012 的全部本地文件做去标签全文正则扫描，按
「该年度中有多少个季度至少有一份文件命中该概念」计数。脚本见
`scratchpad/probe_pre2013.py` / `probe_unitcost.py` / `probe_gfi_nce.py`。
扫描的是**概念是否出现**，不抽取任何数字——数字仍由抽取 agent 逐份读原文。

这份普查的目的只有一个：**让 2005–2012 的抽取 agent 不必靠猜科目名。**
本项目已经因为「按一家公司的科目名去另一家公司里找」而返工过一次。

---

## 1. 结论一：AISC 在 2013 年前确实不存在（正面证实）

| 公司 | 2005–2011 命中 AISC 的季度数 | 2012 |
|---|---|---|
| AEM | 0 | 1 |
| AU | 0 | 0 |
| GFI | 0 | 0 |
| GOLD | 0 | 1 |
| KGC | 0 | 1 |
| NEM | 0 | 1 |

2012 年那几次命中全部出现在**第四季度**的文件里，是各公司对 2013 年将采用
WGC 新准则的**预告**，不是当期披露值。这与 WGC《Guidance Note on Non-GAAP
Metrics》2013 年 6 月首版的时间线一致。

**所以 2005–2012 段的校验和必须整体降级**，走 DEGRADATION §7 的 pseudo-AISC
路线。降级是设计好的，不是数据缺失。

---

## 2. 结论二：单位成本锚点**逐家不同**，且有两家不是「总现金成本」

DEGRADATION §7.2 的 pseudo-AISC 重建式默认锚在 Gold Institute 1996 口径的
"total cash cost"。实测下来，**六家里只有四家能这么锚**：

| 公司 | 2005–2012 单位成本锚点（逐字） | 覆盖 | 口径警告 |
|---|---|---|---|
| **NEM** | `Costs applicable to sales` | 4/4 全年份；显式 per-ounce 2009 起 4/4 | 与其 2013 年后的锚点**同名**，序列连续 |
| **GOLD** | `total cash cost` per ounce | 2006 起 4/4 | by-product |
| **AEM** | `total cash cost` per ounce | 3–4/4 | 同时有 by-product 与 co-product |
| **AU** | `total cash cost` per ounce | 4/4 全年份 | by-product |
| **GFI** | `Notional Cash Expenditure`（NCE） | **2008 起 4/4**；另有 total cash cost 2005 起 4/4 | GEO（Cerro Corona 铜） |
| **KGC** | `cost of sales per equivalent ounce` | 2007 起 4/4 | **GEO 基准，被白银污染** |

两个必须单独说的：

### 2.1 KGC 没有 "total cash cost" —— 一次都没有

2005–2012 全时段命中 0。Kinross 用的是
`attributable production cost of sales per equivalent ounce`，而且
**"gold equivalent ounce" 在每一年都是 4/4 命中**。

这意味着 Kinross 的 2005–2012 校验和天生带 GEO 污染。GEO 的陷阱在本项目已经
记录过：`GEO = 黄金盎司 + 副产品收入 ÷ 实现金价`，所以**用隐含金价去反查会完
美通过**，而收入和盎司两边同时被抬高。Kinross 该时代的每一行都必须打
`GEO_BASIS`，且 `gold_oz_sold` 不得用 GEO 顶替。

### 2.2 GFI 在 AISC 出现前五年就有一个真正的全成本指标

Gold Fields 的 **NCE（Notional Cash Expenditure）= 营业成本 + 全部资本开支**
（不只是维持性资本开支），按盎司计。**2008Q1 起 4/4 季度披露，一直到 2012**。

这比 total cash cost 更接近 GAIM 的口径——它已经把 capex 装进去了。
对 GFI 而言，2008–2012 段应当**优先用 NCE 作校验和**，total cash cost 退为次选。
这是本次普查唯一一个让保真度**上升**而不是下降的发现。

---

## 3. 结论三：Barrick 的 G&A 科目名在 2013 年前是另一个词

第一轮普查按 `general and administrative` 扫描，Barrick 在 2006–2008、2010 年
命中 **0/4**，看上去像是一个真实缺口。

复查后是假缺口。Barrick 该时代用的是 **`Corporate administration`**，
2006–2012 **每一年 4/4**：

| 年 | `general and administrative` | `corporate administration` |
|---|---|---|
| 2006 | 0/4 | **4/4** |
| 2007 | 0/4 | **4/4** |
| 2008 | 0/4 | **4/4** |
| 2009 | 2/4 | **4/4** |
| 2010 | 0/4 | **4/4** |
| 2011 | 4/4 | **4/4** |
| 2012 | 2/4 | **4/4** |

**规范含义**：`NOT_DISCLOSED` 只有在**穷举过该公司该时代的同义科目名之后**才
成立。按单一科目名扫出来的空洞，默认当作科目名不对，不当作缺口。

---

## 4. 其余 GAIM 输入项的可得性（2005–2012）

按「有多少季度能找到」计，六家横向：

| 输入项 | 可得性 | 说明 |
|---|---|---|
| `segment_revenue_gold` | 多数公司 4/4 | 分母有保障 |
| `capex_total` | 4/4 | 现金流量表 |
| `corporate_g_and_a` | 4/4（注意 §3 的科目名） | |
| `exploration_expensed` | 4/4 | |
| `reclamation_accretion` | 4/4（GOLD/KGC/NEM）；AEM 2009 起 1/4 | SFAS 143 自 FY2003 起，本时代全程有效 |
| `net_interest` | 2–4/4 | |
| `gold_oz_sold` | AU/GFI/KGC/NEM 4/4；AEM **0/4** | AEM 仍只报产量，须打 `ONLY_PRODUCED` |
| `cash_tax_paid` | **最弱**：AEM 2009–2012 仅 1/4；AU 2011–2012 **0/4** | 走 C1 年度按季度黄金收入分摊 |
| `lease_payments` | 不适用 | IFRS 16 / ASC 842 要到 2019 年，本时代属 Tier A-equivalent 零偏差，不是缺口 |

`cash_tax_paid` 是全表最大敞口，这一点在 2005–2012 比 2013 年后更严重，
须逐行记录降级档位。
