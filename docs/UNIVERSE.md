# 黄金开采季度利润率研究 —— 样本筛选说明（Universe / Selection Screen）

> 状态：v2.0（第二轮补做）。第一轮（v1.0）覆盖 2005–2025 年 139 行，逐年公司数从 2 到 13
> 家不等，从未真正到过 20 家，且 `gold_revenue_share_pct`（黄金收入占比——项目实际的选样
> 标准，"黄金收入占比最大的前 20 家"）139 行全部留空。第二轮把行数补到 **163 行**，新增/
> 修正了 2006、2007、2013、2017、2018、2019 年的大量公司，把 `gold_revenue_share_pct`
> 从 0 行填到 **43 行**（全部来自本轮实际打开的公司 10-K/20-F/40-F/年报原文，不是估算），
> 并新增 `panel_eligible`／`ineligible_reason` 两列。详见第 11 节，那是本文件目前最新、
> 最应该先读的部分；第 0–10 节是第一轮的原始记录，为保留审计痕迹而未删改，其中关于
> "`gold_revenue_share_pct` 全部留空"的表述（见第 3.2、9.1 节）已被第 11 节取代，
> 阅读时请以第 11 节为准。
>
> 本研究目前覆盖的 6 家公司（Newmont、Barrick、Agnico Eagle、Kinross、
> AngloGold Ashanti、Gold Fields）此前是凭研究员判断挑选的，**没有书面、可复现的筛选标准**。
> 本文件和同目录下的 `data/universe/top20_by_year.csv` 是补做的筛选文档：给出 2005–2025
> 年（共 21 年）每年按黄金产量排名的前 10–20 家公司名单、数据来源、交叉验证情况和置信度，
> 让读者自己判断这 6 家公司是否真的是"最大的 6 家"，以及研究漏掉了谁。

---

## 0. 一句话结论

**不是。** 严格按年度黄金产量排名，Newmont、Barrick、AngloGold Ashanti、Gold Fields 在几乎
所有年份都稳居前十，站得住脚；但 **Kinross 从 2022 年起已经不是前 6**——俄罗斯的 Polyus、
中国的紫金矿业（Zijin Mining）产量都已超过 Kinross，2024–2025 年甚至 Gold Fields 也被
紫金反超。研究没有把 Polyus、紫金矿业、乌兹别克斯坦国营的 Navoi（Muruntau 矿）纳入考虑，
如果只是因为它们数据难拿、账目不透明而排除，这是可以接受的（前提是写清楚），但**不能不
声明就排除**——目前的方法论文档里没有这句话。详见第 8 节。

---

## 1. 排名指标的选择与理由

### 1.1 用什么排名：**权益黄金产量（attributable gold production），单位盎司**

行业里给"最大金矿公司"排名，常见的口径至少有四种，本研究选择第一种：

| 口径 | 说明 | 是否采用 |
|---|---|---|
| **权益产量（attributable / equity ounces）** | 按公司在每座矿山的权益比例折算的黄金产量。合资矿山、非全资子公司只计入公司实际能分到的那部分产量 | **采用** |
| 合并产量（consolidated production） | 只要并表就 100% 计入，不管少数股东占多少 | 不采用——会系统性高估持有非全资资产多的公司（如 Kinross、AngloGold 在南非、加纳的历史合资结构） |
| 托管/作业产量（managed production） | 按"谁在运营矿山"计入，不管股权 | 不采用——运营权和现金权益是两回事，运营方不一定能拿到相应比例的现金流 |
| 黄金收入 / 市值 | 按收入或市值排名 | 不采用为主排名指标，仅作为第二指标（见 1.2） |

选权益产量而不是合并产量，和本研究主报告（`docs/METHODOLOGY.md` §2）里"Attributable, never
consolidated"的原则完全一致：少数股东权益下的现金不是股东能拿到的钱，同一逻辑用在产量排名
上，就是少数股东权益下的产量也不是这家公司真正"产出"的黄金。

### 1.2 为什么不用收入或市值排名

- **市值**混入了大量不产金的公司——最典型的是 Franco-Nevada、Wheaton Precious Metals、
  Royal Gold 这类"版税/流媒体"（royalty/streaming）公司。它们不开矿，只是买断别人矿山未来
  产量的一个折扣价格购买权，市值可以做到几百亿美元，比很多真正的矿商还大，但**一盎司金子
  都不是它们挖出来的**。本研究的排名口径明确排除这类公司（见第 8 节）。
- **收入**受金价波动、套期保值（hedging）、副产品（铜、银）收入占比影响太大，两个产量完全
  相同的公司可能因为对冲策略不同而收入相差 20% 以上，尤其是 2005–2010 年这段套保历史复杂
  的时期。产量是更贴近"这家公司到底挖了多少金子"这个问题本身的指标。

### 1.3 盎司 vs 吨——中国、俄罗斯公司的单位换算

中国的紫金矿业（Zijin Mining，紫金矿业）、山东黄金（Shandong Gold）、招金矿业
（Zhaojin）、中国黄金集团（China National Gold）年报都以"吨"（tonne）披露矿产金
（不是"金精矿"或贸易/冶炼金，见下）。本研究统一按

```
1 吨 = 32,150.7 金衡盎司（troy ounce）
```

换算为盎司后再排名。**特别提醒**：紫金矿业年报里同时披露"矿产金"（自己矿山挖出来的）
和"合质金 / 冶炼金"（含收购矿石冶炼、贸易业务在内的总产出），后者数字大很多。本表**只用
矿产金**，与其他公司的"权益产量"口径对齐；把紫金的"总产金量"直接和 Newmont 的权益产量
比较是不可比的，会系统性高估紫金的真实矿山产出排名。核实过程中发现一个具体例子：紫金
2011 年年报摘要显示"合质金 86.17 吨"，但其中"矿产金"只有 28.62 吨（约 92 万盎司）——
差了 3 倍，如果不加区分，紫金在 2011 年会被错误地排进全球前 10。

---

## 2. 纳入规则（Inclusion Rule）

**一家公司在某年被列入该年榜单，当且仅当：**

1. 该年度有**至少一个可核实的来源**（公司年报/10-K/20-F/40-F/新闻稿，或行业权威机构如
   Metals Focus、GFMS/汤森路透黄金调查、World Gold Council、S&P Global Market
   Intelligence、Kitco News、MINING.com 年度榜单）披露了其**当年权益黄金产量**的具体数字；
2. 该数字按 1.3 节规则统一换算为盎司；
3. 该公司当年产量数值**进入了本研究实际核实到的、当年最大产量公司集合的前 20 名区间**
   （见第 9 节关于"部分年份数据不完整"的说明——不代表没被核实到的公司一定排不进前 20）。

**不满足"上市/可获得公开产量数字"这一条的公司不会被静默剔除**——本研究采用的做法是：
只要有可信赖的产量数字（哪怕来自 S&P Global 之类第三方估算而非公司自己披露），**照样列入
榜单，并打上"非上市/国有/无财务可用"标记**，而不是因为它不方便纳入利润率研究就把它从
"世界最大金矿商"名单里删掉。乌兹别克斯坦国有的 Navoi Mining and Metallurgical Company
（Muruntau 金矿运营方）就是这样处理的：2023–2025 年三年数据显示它稳居全球产量前 5，
本表如实列入,但同时注明它不发布可审计的财务报表,不能进入利润率研究本体。

---

## 3. 数据来源与交叉验证方法

### 3.1 一级来源（source_primary）优先级

1. 公司官方文件：10-K / 20-F / 40-F（SEC EDGAR）、年报（Integrated Annual Report）、
   季度/年度业绩公告（press release）——**优先使用**；
2. 公司自己对外的产量新闻稿（如 "Newmont Delivers Strong Full-Year Results"）；
3. 上述文件不可得或检索窗口内未能定位时，退而使用行业汇编（见 3.2）作为一级来源，并在
   `source_primary` 字段中如实注明这是汇编数据，不是公司原始文件。

### 3.2 二级来源 / 交叉验证（source_crosscheck）

按本研究方法论文档的口径，交叉验证来源包括：Metals Focus、GFMS/Thomson Reuters Gold
Survey、World Gold Council、S&P Global Market Intelligence、**MINING.com 年度 Top 10
榜单本身也被允许作为交叉验证源**（因为它逐年独立编制，不是公司自己发的稿子）、Kitco
News、《The Northern Miner》、《Canadian Mining Journal》。

**置信度判定规则**（与任务书一致）：

| confidence | 条件 |
|---|---|
| `high` | 两个独立来源给出的数字相差 ≤3% |
| `medium` | 只有一个权威来源；或两个来源相差 3%–10% |
| `low` | 靠指引区间（guidance）、百分比反推、或跨年插值估算出来的数字；必须在 source 字段写清楚推算方法 |

本轮研究中，139 行数据里 **44 行 high、88 行 medium、7 行 low**（详见第 9 节和
`top20_by_year.csv`）。没有一行是凭空编的数字——凡是找不到可核实来源的年份/名次，
**直接留空**，不用估算值填充，这是任务书的硬性要求，也是本研究唯一不可妥协的规则。

### 3.3 特别注意：不少"独立"来源其实同源

MINING.com、《The Northern Miner》、Kitco News 经常互相转载或引用同一份 Metals Focus /
公司新闻稿数据。本表在标注 `source_crosscheck` 时,只有在两篇文章**明显独立编制**（不同
撰稿人、不同发布机构、数字有独立取整误差而非完全复制）时才算作真正的交叉验证；如果高度
怀疑是同源转载，`confidence` 保持在 `medium`，不虚报为 `high`。2025 年紫金矿业的数字就是
一个反例：Investing News Network 引用的 2,415 koz 与紫金矿业自己 2026 年 3 月公告的
"90 吨、同比+23%"（约合 2,894 koz）相差约 17%，超出了 10% 的容忍带，本表按 `medium`
处理并在备注中写明分歧，供读者自行判断哪个数字更可信。

---

## 4. 并集名单（Union List）——任何一年进过前 20 的公司

以下公司在 2005–2025 中至少有一年出现在本研究**实际核实到**的年度前 20 名单里
（同一家公司改名/重组按同一实体合并列出，历史名称见备注）：

| 公司（研究期内曾用名） | Ticker/交易所 | 国家/地区 | 现状 |
|---|---|---|---|
| Newmont（Newmont Mining → Newmont Corporation，2019 年并购 Goldcorp 后一度称 Newmont Goldcorp） | NEM (NYSE) | 美国 | 存续，目前全球最大 |
| Barrick（Barrick Gold Corp，2025 年更名 Barrick Mining，交易代码由 GOLD 改为 B） | GOLD→B | 加拿大 | 存续 |
| AngloGold Ashanti（2023 年主要上市地/公司总部迁往英国，CIK 由 1067428 变为 1973832） | AU (NYSE) | 南非/英国 | 存续 |
| Gold Fields | GFI (NYSE/JSE) | 南非 | 存续 |
| Kinross Gold | KGC (NYSE/TSX) | 加拿大 | 存续 |
| Agnico Eagle Mines | AEM (NYSE/TSX) | 加拿大 | 存续，2022 年并购 Kirkland Lake Gold |
| Placer Dome | 已退市 | 加拿大 | **2006 年被 Barrick 收购**，2005 年后不再独立存在 |
| Goldcorp | 已退市 | 加拿大 | **2019 年被 Newmont 收购** |
| Newcrest Mining | 已退市 | 澳大利亚 | **2023 年被 Newmont 收购** |
| Randgold Resources | 已退市 | 泽西/英国（LSE 上市） | **2019 年与 Barrick 合并** |
| Polyus | PLZL (MOEX) | 俄罗斯 | 存续，2022 年后西方投资者可获得的披露大幅减少 |
| Polymetal International → Solidcore Resources | POLY→AIX | 俄罗斯→**2023 年迁册哈萨克斯坦** | 存续，改名 Solidcore Resources |
| Sibanye Gold → Sibanye-Stillwater | SBSW (NYSE/JSE) | 南非 | 存续，主业已转向铂族金属，黄金占比下降 |
| Harmony Gold Mining | HMY (NYSE/JSE) | 南非 | 存续 |
| Compania de Minas Buenaventura | BVN (NYSE) | 秘鲁 | 存续 |
| Freeport-McMoRan | FCX (NYSE) | 美国 | 存续，铜矿为主业，黄金为格拉斯伯格（Grasberg）副产品 |
| Kirkland Lake Gold | 已退市 | 加拿大 | **2022 年被 Agnico Eagle 收购** |
| Northern Star Resources | NST (ASX) | 澳大利亚 | 存续 |
| Nordgold | NORD (原 LSE，2022 年除牌) | 俄罗斯 | 因制裁从伦交所摘牌，后续披露不完整 |
| Zijin Mining Group 紫金矿业 | 2899.HK / 601899.SS | 中国 | 存续，近三年增长最快的主要金企之一 |
| Shandong Gold Mining 山东黄金 | 1787.HK / 600547.SS | 中国 | 存续 |
| Navoi Mining and Metallurgical Company (NMMC) | 无（国有，不上市） | 乌兹别克斯坦 | 全球产量前 5，**无可审计财务数据** |

**共 22 家公司**，远超研究目前覆盖的 6 家——这正是任务书预期的"名单是动态的、会超过 20 家"。

### 4.1 未纳入并集名单、但需要点名解释的公司

- **招金矿业（Zhaojin）、中国黄金集团（China National Gold）**：本轮检索没能找到它们任何
  一年独立、可核实的权益产量数字进入全球前 20（中国全国黄金产量虽然全球第一，但分散在紫金、
  山东黄金、招金、中国黄金集团、其他省属国企等多家企业之间，没有一家能单独占到全国产量的
  大头——见第 8.3 节"国家总量 ≠ 单一公司产量"的陷阱）。不代表它们从未进过全球前 20,
  只代表本轮时间预算内没有查到扎实数字，留作后续工作。
- **Petropavlovsk、Alrosa、Rio Tinto、BHP、Anglo American、Norilsk Nickel**：见第 8 节，
  逐一说明为什么排除。

---

## 5. 逐年进出榜情况（Entries / Exits by Year）

下表基于 `top20_by_year.csv` 中**本轮实际核实到并写入表格**的公司集合逐年对比，
"进"指该年首次出现在已核实名单中，"出"指上一年出现、当年从已核实名单消失。
**请注意**：很多"出"是因为本轮检索没有找到该年该公司的数字（数据缺口），
不代表该公司当年真的跌出了前 20——两者的区别在备注列里标出。

| 年份 | 新进入已核实名单 | 从已核实名单消失 | 备注（真实事件 vs 数据缺口） |
|---|---|---|---|
| 2005 | AngloGold Ashanti, Barrick, Gold Fields, Newmont, Placer Dome | — | 起始年 |
| 2006 | — | Gold Fields, Placer Dome | Placer Dome：**真实事件**，2006 年 3 月被 Barrick 收购，产量并入 Barrick；Gold Fields：数据缺口 |
| 2009 | Goldcorp | — | 数据补充，非首次上榜（Goldcorp 此前应已在榜，只是 2005-2008 未查到数字） |
| 2010 | — | Goldcorp, AngloGold Ashanti | 数据缺口（本轮只查到 Barrick、Newmont 两家 2010 年实际数） |
| 2011 | Gold Fields, Harmony Gold, Kinross, Newcrest, Polyus, Buenaventura | — | 数据补充（mining.com 2012 年文章反推 2011 年 YoY） |
| 2013 | — | Gold Fields, Goldcorp, Harmony, Kinross, Newcrest, Polyus, Buenaventura | 数据缺口，2013 年是本表最薄弱的年份之一 |
| 2014 | Agnico Eagle, Sibanye Gold | Buenaventura | Agnico Eagle **真实事件**：产量持续增长首次进入已核实前十；Buenaventura 为数据缺口 |
| 2017 | Randgold, Polymetal | Agnico Eagle, AngloGold, Barrick, Gold Fields, Goldcorp, Kinross, Newcrest, Newmont, Polyus, Sibanye | 数据缺口严重——2017 年只查到两家公司的独立数字，头部公司名次未能重建，见第 9 节 |
| 2018 | — | Randgold, Polymetal | Randgold **真实事件**：2019 年 1 月与 Barrick 合并，2018 是其作为独立公司的最后完整年份 |
| 2019 | Newmont Goldcorp（更名） | Harmony | Newmont **真实事件**：2019 年 4 月完成对 Goldcorp 收购，公司一度更名 Newmont Goldcorp（2020 年改回 Newmont Corporation）；Goldcorp 作为独立上市公司**在此年内消失** |
| 2020 | Kirkland Lake, Northern Star, Nordgold, Polymetal（数据恢复） | — | 数据大幅补充（Visual Capitalist/Mining Intelligence 完整前十+补充名单） |
| 2021 | — | Gold Fields, Goldcorp(已并入 Newmont)、Newcrest, Kirkland Lake, Nordgold, Northern Star, Polymetal, Sibanye, Agnico Eagle | 数据缺口——本轮只查到 2021 年前 4 名的扎实数字 |
| 2022 | Freeport-McMoRan, Zijin Mining, Agnico Eagle（数据恢复）, Gold Fields（数据恢复）, Newcrest（数据恢复） | — | Freeport、紫金矿业**首次以扎实数字进入本表全球前十**（真实事件——两者都是产量增长后新晋前十，非仅数据缺口） |
| 2023 | Navoi/NMMC, Solidcore Resources | Newcrest | Navoi **首次纳入**（S&P Global 估算口径，非公司自报）；Newcrest：**真实事件**，2023 年 11 月被 Newmont 收购，2023 全年是其作为独立公司的最后一个完整年度 |
| 2024 | Shandong Gold, Northern Star（数据恢复） | Navoi, Solidcore | 数据缺口（Navoi、Solidcore 2024 年数字本轮未查到） |
| 2025 | Navoi（数据恢复） | Freeport, Shandong Gold | 数据缺口 |

**三个可归为"真实事件"（而非单纯数据缺口）的结构性大变化**，与任务书列出的背景一致：

1. **并购潮**：Placer Dome→Barrick（2006）、Goldcorp→Newmont（2019）、
   Randgold→Barrick（2019）、Kirkland Lake→Agnico Eagle（2022）、Newcrest→Newmont（2023）。
   每一次都让收购方的产量台阶式跳升，也让一家原本稳定在前十的独立公司永久退出"公司"口径的
   排名（虽然产的矿还在，只是并入了别家报表）。
2. **俄罗斯制裁**：2022 年 2 月俄乌冲突后，Polyus、Polymetal（后改名 Solidcore 并迁册
   哈萨克斯坦）、Nordgold、Petropavlovsk 的西方媒体/分析机构披露大幅减少或完全中断，
   部分公司退市（Nordgold 从伦交所摘牌）或陷入财务困境（Petropavlovsk 2022 年进入
   破产程序）。这不是公司变小了，是**信息不透明度陡增**——这正是任务书要求特别标注的
   "披露原因排除，而非规模原因排除"的典型场景。
3. **中国生产商崛起**：紫金矿业 2022 年起以扎实数字进入本表全球前十，2024–2025 年产量
   已超过 Gold Fields、Kinross；山东黄金规模也在快速接近全球前十的门槛。这是过去研究
   完全没有覆盖的一块。

---

## 6. 被排除的公司及理由

### 6.1 因"不产金"而排除——版税/流媒体公司

Franco-Nevada、Wheaton Precious Metals、Royal Gold、Sandstorm Gold 等公司经常出现在
按**市值**排名的"全球十大黄金公司"listicle 里（本轮检索中，Insider Monkey/Yahoo Finance
的"Top 20 Gold Mining Companies"榜单里排第 6、7、13 位的分别是 Franco-Nevada、Wheaton、
Royal Gold），但这些公司**不开采黄金**，只是买断矿商未来产量的一定比例（streaming）或
预先支付换取营收分成（royalty）。它们没有"权益黄金产量"这个概念——本表以产量为排名口径，
这类公司**结构性地不适用**，全部排除，不是因为规模不够。

### 6.2 因"金为副产品、非主业"而排除——多元化矿业巨头

Rio Tinto、BHP、Anglo American、Norilsk Nickel、Alrosa 是本轮任务书要求专门核查的名字。
核查结论：

- **Rio Tinto / BHP**：主业铁矿石、铜、铝土矿，黄金仅在少数铜矿（如 Rio Tinto 的 Oyu
  Tolgoi、BHP 参股的 Escondida）中作为副产品少量产出，未查到任何一年黄金权益产量单独
  披露超过百万盎司的证据，**结构上不可能进入全球金矿商前 20**。
- **Anglo American**：黄金业务已于 1998 年前后分拆为独立的 AngloGold（后来的
  AngloGold Ashanti）——本表已单独覆盖 AngloGold Ashanti，Anglo American 母公司本身
  2005 年后不再产金。
  - **Norilsk Nickel**：主业镍、钯（全球最大钯生产商之一），黄金为电解精炼副产品，
  规模远小于百万盎司量级。
- **Alrosa**：俄罗斯国家钻石公司，与黄金无关，任务书列出该名字大概率是作为"容易被误认成
  贵金属公司"的反例。

以上五家：**排除理由是规模/主业结构，不是披露问题**，与 8.2 节"因披露原因排除"的
Navoi/Polyus 等公司性质不同，这里明确加以区分。

### 6.3 国家总量 ≠ 单一公司——排除"国家"作为排名单位

部分行业 listicle（尤其是把"gold producing countries"和"gold mining companies"两张表放在
一起的文章）容易造成误解：中国 2024 年全国黄金产量 380.2 吨全球第一，但**中国没有一家公司
单独产出这么多**——380 吨分散在紫金矿业（矿产金约 2024 年 81 吨左右）、山东黄金
（矿产金 2023 年 41.78 吨）、招金、中国黄金集团及大量地方国企之间。本表严格以"公司"为
排名单位，国家层面的产量数字（USGS Mineral Commodity Summaries、World Gold Council
"Gold production by country"）只用于交叉验证个别公司数字的合理性，**不作为公司排名的
替代**，也不把"中国"本身当作一个排名条目纳入表格。

---

## 7. 国有/非上市但产量足够进前 20 的公司——不能静默剔除

任务书特别要求：这类公司要"带着标记留在排名表里，不能因为凑不齐财务数据就悄悄删掉"。
本轮核实到一家明确符合条件的公司：

**Navoi Mining and Metallurgical Company（NMMC，纳沃伊矿冶联合企业）**——乌兹别克斯坦
国有企业，运营 Muruntau 露天金矿（全球最大单体金矿之一）。2023–2025 年产量数据显示其
稳定位居全球第 4–5 位，规模上远超 Kinross、Gold Fields 等本研究现有覆盖的公司。**不发布
可审计的国际会计准则财务报表**，无法计算 AISC、毛利率等本研究核心指标，因此不能进入
`docs/METHODOLOGY.md` 定义的利润率研究本体——但这是"数据不可得"，不是"规模不够"，
两者必须分开说清楚，本表已在 `country` 列标注为 `UZ`、`ticker` 留空并在
`source_primary` 中注明"国有、无可用财务数据"。

中国黄金集团（China National Gold Group）同样是国有企业，理论上产量可能进入全球前 20
（其上市子公司中国黄金国际资源 China Gold International Resources 只是集团一小部分
资产），但本轮检索未能找到集团层面可核实的权益产量数字，未列入表格——这是**数据缺口**，
不是排除，留作后续工作（见第 9 节）。

---

## 8. 本表 vs. 现有 6 家公司研究——直接对比

结合第 5 节的逐年数据，把现有研究的 6 家公司和当年**已核实数据里的实际前 6/前 10** 做对比：

| 年份 | 已核实前 6（按产量，仅含本表已核实到数字的公司，可能因数据缺口而不完整） | 现有研究 6 家里明显不在前 6 之列 |
|---|---|---|
| 2011–2016 | Barrick, Newmont, AngloGold, Goldcorp, Kinross/Newcrest 排 5–6 位 | **Gold Fields** 多数年份排在 Goldcorp、Newcrest 之后（第 7 位左右），够不上前 6；Agnico Eagle 2011-2013 未进前十 |
| 2020 | Newmont, Barrick, Polyus, AngloGold, Kinross, Gold Fields | 6 家基本吻合，但 **Polyus 已经比 Kinross、Gold Fields 都大**，未被现有研究覆盖 |
| 2022 | Newmont, Barrick, Agnico Eagle, AngloGold, Polyus, Gold Fields | Kinross 排第 7，**跌出前 6** |
| 2024 | Newmont, Barrick, Agnico Eagle, Polyus, AngloGold, Zijin（并列第 5） | **Kinross 排第 8、Gold Fields 并列第 7，双双跌出前 6**；紫金矿业该年已是全球第 5-6 大金企,完全未被现有研究覆盖 |
| 2025 | Newmont, Agnico Eagle, Barrick, AngloGold, Polyus, Zijin（不计入非上市 Navoi） | 同上，**Kinross 第 9、Gold Fields 第 8**，双双跌出前 6 |

**结论**：Newmont、Barrick、AngloGold Ashanti 三家在几乎全部 21 年都稳居前 6，站得住脚；
**Agnico Eagle 是 2022 年 Kirkland Lake 并购之后才真正进入前 6**，2011–2020 年间它多数
年份排在前十开外；**Kinross 和 Gold Fields 从 2022 年起已经不是产量口径的前 6**，被
Polyus（俄罗斯，制裁导致披露受限）和紫金矿业（中国，账目语言/口径差异导致过去被忽略）
反超。如果研究的目的是"当今全球最大 6 家金矿商的利润率"，现有名单在 2022 年之后已经
**不再准确**，需要讨论是否替换或至少并行展示 Polyus/紫金矿业作为参照组
（哪怕它们的账目质量、可比性存在第 6.2 节以外的其他障碍，比如 Polyus 的合并报表在
2022 年后基本停止对外披露、紫金矿业的 A+H 股财报是中文/港式准则，需要单独的方法论适配）。

---

## 9. 诚实的缺口清单——读者不应该信什么

**这是本文件最重要的一节。** 以下是本轮研究在 21 年 × 最多 20 名的完整矩阵里，
**明确没有做到、不应该被当作扎实结论使用**的部分：

### 9.1 完全没有的数据

- **`gold_revenue_share_pct`（黄金收入占总收入比例）列，本表 139 行全部留空。**
  逐年逐公司核实这个比例，需要打开每家公司当年的产品/分部收入附注,工作量相当于再做一次
  完整的样本筛选，本轮时间预算内没有展开。方向性提示（未写入表格,仅供参考）：
  Freeport-McMoRan 黄金收入占比历史上多在 10%–20%（铜为主业）；紫金矿业黄金收入占集团
  总收入约 15%–20%（铜、锌收入更大）；Sibanye-Stillwater 2020 年后黄金收入占比降至
  少数（主业转向铂族金属）；其余"纯金"公司通常在 90% 以上，但没有逐年核实,不能写成
  具体数字。
- **2013、2017、2019 三个年份**：本表数据严重不完整。2013 年只查到 Barrick、
  AngloGold Ashanti 两家；2017 年只查到 Randgold、Polymetal 两家零散数字（头部公司
  Barrick/Newmont/AngloGold 当年名次因缺乏扎实数字未能重建）；2019 年只查到 Barrick
  一家的具体产量数字（Newmont 当年"全球第一"的事实是确定的,但具体盎司数没查到）。
  **这三年的完整前十/前二十不应被视为本研究已核实内容。**
- **11–20 名区间，绝大多数年份**：任务书预先提示过这一点会发生——年度"全球十大金矿商"
  listicle 是行业惯例，第 11–20 名极少被系统性汇编。本表只在 2020、2023、2024 年
  勉强补充了个别第 11 名（Kirkland Lake、Solidcore Resources、Shandong Gold Mining），
  其余年份 11–20 名区间基本是空的。**这不代表这些位置不存在公司，只代表本轮没查到
  扎实数字。**

### 9.2 置信度较低、需要谨慎使用的数字

- **2011 年整年**：所有数字都是从 mining.com 2012 年文章里公布的"较上年变动百分比"反推
  出来的（例如"Barrick 2012 年 742 万盎司，同比 -3.4%"倒推 2011 年为 768 万盎司）。
  这是**单一来源的二次推算**，不是任何人直接报告的数字，`confidence` 统一标为 `medium`，
  但比起真正的"两个独立来源互相印证"要弱。
- **2009、2010 年的 Barrick、Newmont**：只查到公司发布的**产量指引区间**（guidance），
  没有查到经审计的实际完成数——本表对应单元格已留空，只保留了公司名和推断的名次
  （因为多年模式一致，名次本身相对可信），`confidence` 标为 `low`。
- **2013 年 AngloGold Ashanti**：数字是从"南非业务占集团总产量 32%"反推出来的
  （1.3M oz ÷ 0.32），32% 是四舍五入后的披露数字，反推误差可能有几个百分点，
  `confidence` 标为 `low`。
- **2021 年 Kinross**：数字是从 2022 年新闻稿"同比增长 35%"反推的，**不是公司直接报告
  的 2021 年数字**，`confidence` 标为 `low`。
- **2025 年紫金矿业**：如 3.3 节所述，两个来源相差约 17%，超出正常交叉验证容忍带，
  `confidence` 保持 `medium` 且带分歧说明,不应视为已经解决的数字。

### 9.3 未纳入交叉验证、只有单一来源的年份

2005–2014 期间（除 2015 年外）几乎所有行都只有 `source_primary`，`source_crosscheck`
留空——这是因为这段时期的行业年度榜单本身就稀少，公开可检索的独立复核来源很少。
2015 年是本表唯一一个 2005–2019 区间内做到"两个独立媒体各自编制、数字互相吻合"的年份
（MINING.com + Canadian Mining Journal），因此是这段时期里质量最高的一年，可以当作
其余年份数据质量的参照基准——其余年份普遍弱于 2015 年。

### 9.4 完全没有触碰的公司

招金矿业、中国黄金集团、Zhaojin 之外的其他中国省属黄金国企、Petropavlovsk（俄罗斯，
2022 年破产重整前也曾是百万盎司级公司）、Eldorado Gold、Centerra Gold、IAMGOLD、
Alamos Gold、New Gold、Evolution Mining、B2Gold、Endeavour Mining、
South Deep（Gold Fields 旗下)以外的独立中小型金企——这些公司多数产量规模在
50–150 万盎司区间,历史上部分年份可能踩线进入全球前 20,但本轮完全没有时间逐一核实,
**一行都没有写进表格**,不是因为查过确认不够格,而是根本没查。

---

## 10. 文件清单

- `data/universe/top20_by_year.csv`——本文件描述的全部 139 行原始数据，
  字段：`year, rank, company, ticker, country, attributable_gold_koz,
  gold_revenue_share_pct, source_primary, source_crosscheck, confidence`。
- 本文件（`docs/UNIVERSE.md`）——方法论、并集名单、进出榜情况、排除理由、缺口清单。

下一步建议（第一轮制定，部分已在第二轮/第 11 节完成，未完成的保留在第 11.8 节）。

---

## 11. 第二轮补做记录（v2.0）——`gold_revenue_share_pct`、`panel_eligible` 与逐年补全

> 本节是本文件当前最新、信息量最大的部分。第 0–10 节是第一轮（v1.0）的原始记录，
> 予以保留但不再是最新状态；凡两节冲突，以本节为准。

### 11.1 本轮方法论：只用本轮会话里实际打开过的文件

任务书的硬性要求延续不变：**每一个产量数字、每一个收入占比数字，都必须来自本轮会话
实际检索/下载/读取过的来源，能具体指到文件**，查不到就留空、把置信度标低，绝不用脚本
或个人记忆生成"看起来权威"的数字。本轮实际使用的一手来源类型：

- **SEC EDGAR 直接下载**：用 `data.sec.gov/submissions/CIK....json` 拿到公司完整申报
  历史，再逐份下载 10-K（Newmont、Freeport-McMoRan）、40-F 及其 Annual Information Form
  附件（Barrick、Kinross、Agnico Eagle）、20-F（AngloGold Ashanti、Gold Fields、
  Sibanye-Stillwater）的原始 HTML，本地抽取纯文本后 grep 关键科目（"Sales, net: Gold"、
  "of our Sales were attributable to copper"、"Revenues from mining operations"、
  "Gold Mines Ownership" 产量表等）。这是本轮质量最高的数据来源，产量和收入占比经常能
  在同一份文件里同时找到。
- **公司官网 PDF 年报直接下载**：紫金矿业 H 股年度业绩公告（HKEX 披露文件，PDF，
  用 `pypdf` 抽取全文后定位"经营分部信息"附注）、Newcrest FY2018 年报（Newmont IR 服务器
  镜像，PDF）。
- **行业榜单网络检索**（MINING.com、Kitco News、Mining Weekly、公司自己的新闻稿摘要）：
  用于本轮时间预算内无法逐一打开一手文件核实的补充年份/公司，**全部标注 medium 或 low
  置信度，绝不标 high**，并在 `source_primary` 里如实写明是"公司披露的检索摘要"而非
  本轮亲自打开的原始文件。

### 11.2 逐年行数：本轮之前 vs 之后

| 年份 | 之前 | 之后 | 年份 | 之前 | 之后 | 年份 | 之前 | 之后 |
|---|---|---|---|---|---|---|---|---|
| 2005 | 5 | 5 | 2012 | 10 | 10 | 2019 | 2 | 6 |
| 2006 | 3 | 4 | 2013 | **2** | **9** | 2020 | 13 | 13 |
| 2007 | 3 | 4 | 2014 | 10 | 10 | 2021 | 5 | 5 |
| 2008 | 3 | 3 | 2015 | 10 | 10 | 2022 | 10 | 10 |
| 2009 | 4 | 4 | 2016 | 10 | 10 | 2023 | 11 | 11 |
| 2010 | 2 | 2 | 2017 | **2** | **12** | 2024 | 11 | 11 |
| 2011 | 10 | 10 | 2018 | 3 | 4 | 2025 | 10 | 10 |

合计 139 → **163 行**。最薄弱的三个年份里，2013 从 2 行补到 9 行，2017 从 2 行补到
12 行——这两年现在都有一手来源支持的头部 6–9 家公司；**2019 年仍然只补到 6 行**（本轮
新增 Gold Fields、Kinross、AngloGold Ashanti、Polyus 四家，加上原有的 Newmont Goldcorp、
Barrick），Agnico Eagle、Newcrest、Sibanye、Goldcorp（已被收购中）等公司的 2019 实际
产量本轮检索到的都是"指引区间"或口径存疑的数字，没有采用。**2010 年仍然只有 2 行**——
Barrick、Newmont 的 2010 实际完成数（不是指引）本轮依然没有查到，留空。**没有任何一年
真正做到完整的前 20**——11–20 名区间本轮只在 2020（Kirkland Lake、Northern Star、
Nordgold）、2023（Solidcore Resources）、2024（Northern Star、Shandong Gold）勉强补上
个别公司，其余年份的 11–20 名区间依然是空的，这一点第 9.1 节的诚实提示仍然成立。

### 11.3 本轮修正的存量行（实体归属没有变，产量数字被一手文件校正）

以下行的公司归属（哪家公司在哪一年）**没有改变**——本轮没有发现任何"用后继公司名字
回填并购前年份"的错误，第一轮的实体归属处理是对的。但以下产量数字被本轮实际打开的
一手文件（不是估算）替换或校正，全部升级为 `high` 置信度：

| 年份 | 公司 | 原数字 | 校正后 | 来源 |
|---|---|---|---|---|
| 2007 | Barrick | 8,060（medium） | 8,060（**high**，数字不变但一手确认） | Barrick FY2008 40-F AIF 附件，2007 对比列 |
| 2008 | Barrick | 7,657（medium） | 7,657（**high**） | Barrick FY2008 40-F AIF 附件 |
| 2011 | Barrick | 7,681（反推） | **7,676** | Barrick FY2012 40-F AIF，逐矿产量表 "Company Total 7,421 7,676" |
| 2012 | Barrick | 7,420 | **7,421** | 同上 |
| 2014 | Barrick | 6,250 | **6,249** | Barrick FY2016 40-F AIF，"Company Total 6,117 6,249" |
| 2015 | Barrick | 6,120 | **6,117** | 同上 |
| 2018 | Barrick | 4,500 | **4,527** | Barrick FY2019 40-F AIF，"Company Total 4,527 5,323" |

这些校正幅度都在 1% 以内，不影响排名结论，但既然本轮已经打开了一手文件，就按文件里的
精确数字更新，不再沿用press稿的取整数字。

**2005 年 Gold Fields 一行做了置信度下调而非删除**：原始来源标注为"2009 年年报 5/10 年
历史产量表"，给出 4,219 koz。本轮打开 Gold Fields FY2007 20-F 发现该公司当时财年为
7 月–次年 6 月（不是日历年），且明确披露"FY2006 权益产量 4.074 百万盎司、FY2007 权益
产量 4.024 百万盎司"，是一条逐年下降的序列。4,219 这个数字放在这条序列前面（更早、更高）
是自洽的，本轮判断它大概率对应"截至 2005 年 6 月 30 日的财年"而非日历年 2005，但没有
找到直接证实这一点的一手文件，所以**保留数字、把置信度从 medium 降到 low**，并在
`source_primary` 里加注这个财年错位的可能性。这是任务书"查不到就标低、不要删掉"原则
的具体应用。

### 11.4 `gold_revenue_share_pct`——本轮从 0 填到 43 行

**43 / 163 行填了黄金收入占总收入的百分比**，全部来自本轮实际打开的公司 10-K / 20-F /
40-F 年报或年度业绩公告原文，没有一个是估算或反推市场传言。confidence 分布（全表）：
**high 52 行、medium 101 行、low 10 行**（含产量和收入占比两类数字共用同一个置信度列，
下同）。43 行 `gold_revenue_share_pct` 里的具体方法，按公司列出：

- **Newmont（2005–2025，21 年几乎全覆盖，是本轮覆盖最完整的公司）**：Newmont 历年
  10-K 里有两种可用的一手披露格式，交替使用：(1) 分部附注里的 "Sales, net: Gold $X /
  Copper $Y"（2005 年用的就是这个）；(2) 更省事的一句话："For [年份], [年份], [年份]，
  X%、Y%、Z%，分别为我们的销售额中归属于铜的部分"（2006–2020 年多份 10-K 里反复出现这句
  话，每次给出当年及前两年三个数字，本轮只需要打开 6 份 10-K——FY2008、FY2011、FY2014、
  FY2017、FY2020、FY2023/FY2025——就把 2005–2025 全部 21 年的铜收入占比覆盖了，
  金收入占比 = 100% − 铜占比）；2021 年之后 Newmont 收购 Goldcorp（并入 Peñasquito
  银铅锌矿）、Newcrest（并入 Cadia/Red Chris 铜矿），10-K 改用逐金属美元列表格式
  （Gold/Copper/Silver/Lead/Zinc），本轮直接读取 2021–2025 五年的具体美元数字。
  **金收入占比区间：2007 年最低 78%（当年铜价高、Batu Hijau 铜矿贡献大），2020 年最高
  99%；2021 年并购 Goldcorp 之后回落到 86–90% 区间，是公司层面byproduct结构变化的
  真实反映，不是数据质量问题。**
- **AngloGold Ashanti（2008–2010、2020–2025，9 年）**：早年（2008–2010）该公司 20-F
  的收入附注明确写"Product sales represent revenue from the sale of gold"——也就是说
  "Product sales"这个科目本身的定义就是 100% 黄金收入，不需要再拆分（`Total revenues`
  另外还含一项非经营性的"利息、股息及其他"，本表计算占比时分母只用经营性收入口径，
  与其他公司的处理方式一致）。2020–2022 年的 20-F 利润表里"Gold sales"科目与
  "Total revenue"科目金额完全相等（**100%**），2023 年起新增"By-products"（银、硫酸）
  单独披露，金收入占比略降到 97.8–98.4%。**这是一家结构上几乎纯金的公司，21 年里没有
  查到任何一年铜、锌等其他金属收入的证据**。
- **Gold Fields（2023–2025，3 年）**：FY2025 20-F 收入附注直接给出 Gold/Copper/Silver
  三项美元数字（该公司近年在秘鲁 Cerro Corona、智利 Salares Norte 新增了铜、银副产品
  收入），金收入占比 95.4%–96.3%，比 AngloGold 略低但仍是绝对主业。
- **Agnico Eagle（2021–2023，3 年）**：40-F 附带的财务报表 Note 19（分部信息）直接
  披露"Sales of precious metals (gold and silver) accounted for 99.6% of revenues...
  in 2023"，本轮进一步拆出纯金部分（扣除银）：97.2%（2021）、98.5%（2022）、
  98.7%（2023）。
- **Freeport-McMoRan（2022–2024，3 年）**：10-K Note 16（业务分部信息）逐年披露
  Copper/Gold/Molybdenum/Other 美元收入，金收入占比 **14.9%（2022）、15.3%（2023）、
  17.7%（2024）**，与公司 MD&A 自己陈述的"2022 年收入主要来自铜（77%）、金（14%）、
  钼（6%）"基本吻合。本轮同时打开了 FY2015 10-K（2013–2015 三年数据）：金收入占比
  当年只有 7.4%–9.7%，比近年更低，因为 2013–2015 年 Freeport 还有一块石油天然气业务
  （2016 年前后剥离），进一步稀释了金收入占比——这段历史目前**没有写进 CSV**（Freeport
  2013–2015 年产量也没有查到进入全球前 20 的证据），只记录在这里备查。
- **Zijin Mining Group（2022、2023，2 年，方法论意义最大的一组数字）**：`docs/
  NONSEC_SOURCES.md` 第 3.1 节此前已经证实紫金矿业年报分部附注把"金锭"（矿产金）、
  "金精矿"（矿产但未自炼）、"加工精炼贸易金"（非自产/贸易）三块分开披露，但当时没有
  真正算出比例。本轮打开紫金 2023 年度业绩公告分部附注，用**"金锭"+"金精矿"两项对外
  销售收入**（矿产金口径，与本表 attributable_gold_koz 的定义对齐，明确排除非自产的
  "加工精炼贸易金"）除以合并对外销售总收入，得到 **2022 年 6.9%、2023 年 7.5%**——
  比 `docs/UNIVERSE.md` 第一轮"方向性提示"给出的"15%–20%"猜测低了一半以上。这印证了
  第一轮就担心的问题：紫金矿业虽然黄金产量已经进入全球前 10，但公司收入结构里铜、锌
  才是大头，用"黄金收入占比最大"这个选样标准衡量，紫金矿业其实排不进前列，这正是
  `panel_eligible` 之外、任务书选样标准本身需要读者注意的地方（见第 11.6 节）。
- **Sibanye-Stillwater（2021–2025，5 年，重要发现但未写入 CSV 行）**：本轮打开 FY2023
  与 FY2025 两份 20-F 的分部收入附注，发现该公司黄金收入占比是 **17.2%（2021）、
  13.6%（2022）、26.6%（2023）、33.1%（2024）、36.8%（2025）**——公司主业已经是铂族
  金属（PGM），黄金收入占比近年因金价上涨、PGM 价格下跌有所回升但仍是少数。**这五年
  没有写成 CSV 行**，因为本轮没有查到 Sibanye-Stillwater 这五年的黄金**产量**（盎司）
  数字进入全球前 20 的证据——该公司南非黄金业务 2019 年产量约 93.3 万盎司（见第 9.4
  节附近检索到的旁证），大概率够不上近年前 20 的门槛，所以只在文档里记录这个收入结构
  发现，不勉强凑一行产量不明的 CSV 记录。这个发现本身回答了任务书"能否辨别哪些是真正
  的金矿商、哪些是副产品"的问题——**Sibanye 是最典型的例子：曾经是纯金公司（母公司
  Gold Fields 2013 年分拆出来时就叫"Sibanye Gold"），现在黄金只占收入的 1/7 到 1/3**。

**其余 120 行留空的原因**，按类型：(a) **本轮没有时间打开一手文件核实**（占多数，
尤其是 2005–2016 年区间除 Newmont/Barrick/AngloGold 外的其他公司）；(b) **公司自己的
财务报表结构上就不披露产品级收入拆分**——Kinross 是本轮发现的典型个案：打开 FY2023
40-F 的 AIF（36.8 万字）和 MD&A（26 万字）全文，"Silver"这个词在 26 万字的 MD&A 里
只出现 1 次，公司统一用"gold equivalent ounce"（金当量盎司）披露所有金属销售，
**没有找到任何一处把银收入单独列出的科目**——本轮判断这不是"没查到"而是"这家公司的
披露结构本身就不支持拆分"，所以 Kinross 全部 10 行 `gold_revenue_share_pct` 留空，
`source_primary` 里写明这个结构性原因，而不是像其他公司一样只是"没来得及查"。

### 11.5 `panel_eligible` / `ineligible_reason`——判定标准与结果

判定问题："这个公司-年份的数据，能不能撑起 `docs/METHODOLOGY.md` 描述的**季度**黄金
开采利润率研究？"——不是"这家公司大不大"，而是"这家公司**这一年**有没有可信、连续、
产品级颗粒度足够细的财务/产量披露"。默认 `yes`，以下情形判 `no`（本表 163 行里
**15 行**判定为 `no`，涉及 **6 家公司**）：

| 公司 | 涉及年份 | 判 `no` 的理由 |
|---|---|---|
| Navoi/NMMC | 2023、2025（本表出现的两年） | 经审计 IFRS 报表完全不披露黄金销售盎司数、矿山产量吨位或任何单位成本口径（AISC/现金成本），公式的分母在公司自己的财务报表里根本不存在，无法做任何外部核对（`docs/NONSEC_SOURCES.md` 6.2） |
| Freeport-McMoRan | 2022、2023、2024（本表出现的三年） | 黄金是铜矿的副产品（本轮核实收入占比仅 14.9%–17.7%），公司不发布黄金专属的 AISC 或分部成本结构，整套成本披露都是围绕铜组织的 |
| Zijin Mining Group | 2022、2023、2024、2025（本表出现的四年） | 中国发行人的季度报（Q1/Q3）不披露分部/产品级收入，只有年报和半年报才有（`docs/NONSEC_SOURCES.md` 3.1、6.1），破坏季度面板的连续性；即使年度数据可用，本轮也发现真实矿产金收入占比只有约 7%–8%（见 11.4 节），黄金远不是紫金矿业的主业 |
| Shandong Gold Mining | 2024（本表出现的一年） | 与紫金矿业相同的中国发行人季度披露缺口（`docs/NONSEC_SOURCES.md` 2、4） |
| Polyus | 2023、2024、2025（本表出现的三年，2011–2022 各年判 `yes`） | 自 2023 财年起改发"已发布合并财务报表"，依据俄罗斯政府 2023 年第 1102 号令主动隐去分部资产负债表、关联方细节，审计师明确出具"不适合用于本目的以外任何用途"的强调事项段（`docs/NONSEC_SOURCES.md` 3.2、6.2）；2022 年及以前的完整无保留意见 IFRS 报表判 `yes` |
| Polymetal International | 2017、2020（本表出现的两年，Solidcore Resources 2023 年起的后继实体判 `yes`） | 官网对直连请求和 jina.ai 代理请求均返回 403——是本项目全部检索中唯一连兜底方案都失败的信源，本轮只找到一份俄文版 2020 年报镜像，没有找到完整、可长期依赖的英文历史序列（`docs/NONSEC_SOURCES.md` 3.2、5、6.3） |

**没有判 `no` 但值得注意的边界情形**（写在这里而不是表格里,因为本表目前没有对应的行）：
Sibanye-Stillwater 如果未来把 2019 年及以后的年份补充进 CSV，应判 `no`（黄金已是少数
收入来源，见 11.4 节）；Nordgold 2022 年及以后应判 `no`（公司彻底停止对外披露，
`docs/NONSEC_SOURCES.md` 6.3），但本表目前没有 Nordgold 2022 年及以后的行，这条规则
留给后续补充该公司数据时使用。

### 11.6 六家小组（Newmont、Barrick、Kinross、Agnico Eagle、AngloGold Ashanti、
### Gold Fields）按年份会漏掉的最大产量公司

用本表**已核实到产量数字**的行，按年比较"六家小组里当年有数字的公司的最小产量"与
"六家小组之外、产量比这个最小值还大的公司"，得到下表（只列有缺口的年份；**注意**：
凡六家小组当年缺行的年份，"六家小组最小产量"本身被高估，缺口可能被低估，不是精确值）：

| 年份 | 六家小组之外、产量更大的公司（koz） | 备注 |
|---|---|---|
| 2013 | Goldcorp 2,670；Newcrest 2,110；Polyus 1,650；Sibanye Gold 1,430 | 六家小组当年只有 Barrick/Newmont/AngloGold 三家有数字，缺口被低估 |
| 2014 | Goldcorp 2,870；Newcrest 2,330；Polyus 1,700；Sibanye Gold 1,590 | |
| 2015 | Goldcorp 3,460；Newcrest 2,490；Polyus 1,750 | |
| 2016 | Goldcorp 2,870；Newcrest 2,460；Polyus 1,970 | |
| 2017 | Goldcorp 2,569；Newcrest 2,381；Polyus 2,160 | |
| 2019 | Polyus 2,841 | 六家小组当年只有 5 家有数字 |
| 2020 | Polyus 2,870；Newcrest 2,060 | |
| 2021 | Polyus 2,717 | |
| 2022 | Polyus 2,541 | |
| **2023** | **Navoi/NMMC 2,900；Polyus 2,900；Zijin Mining Group 2,170** | |
| **2024** | **Polyus 3,000；Zijin Mining Group 2,600** | |
| **2025** | **Navoi/NMMC 3,150；Polyus 2,528；Zijin Mining Group 2,415** | |

**读法**：2013–2017 年的"缺口"主要是 Goldcorp（2019 年被 Newmont 收购前一直独立存在）
和 Newcrest（2023 年被 Newmont 收购前独立存在）——这两家在各自被收购之前，几乎每年
产量都比六家小组里最小的一家还大，如果研究目的是"当年产量最大的 6 家"，这两家在
2013–2018 年间应该被认真考虑替换掉小组里的弱项（哪家最弱，取决于当年数据，见本文件
第 8 节的历史对比）。**2019 年之后 Polyus 持续、系统性地比六家小组里的最小值更大**，
2023 年起 Navoi/NMMC、紫金矿业也加入这个名单——但如第 11.5 节所述，这三家现在都是
`panel_eligible = no`（Navoi 无产量/成本口径、Polyus 2023 起报表被本国法令限缩、
紫金矿业黄金只占收入约 7–8% 且中国发行人季度披露不全）。**这正是任务书想要的分层结论：
按纯产量排名,六家小组从 2019 年起就已经不完整;但把"能否支撑一个可信的季度利润率面板"
也作为门槛之后,目前没有一个现成的替代者能无痛地补上——扩大到 7 家或 8 家小组、并列
展示 Polyus/紫金矿业作为参照组同时明确标注数据局限,可能比强行替换更诚实。**

### 11.7 诚实缺口清单（第二轮，补充第 9 节）

- **`gold_revenue_share_pct` 120 / 163 行仍然留空**，尤其是 2005–2019 年区间除
  Newmont/AngloGold/Gold Fields/Agnico Eagle/Freeport/Zijin 之外的几乎所有公司-年份
  （Barrick 只做了 5 个年份的收入占比：2012、2015、2018、2021、2024，中间年份没有逐年
  核实；AngloGold Ashanti 2011–2019 之间也有缺口）。这是本轮时间预算下最大的、留给
  下一轮的工作量。
- **Kinross 全部 10 行 `gold_revenue_share_pct` 留空且预计会一直留空**——不是数据缺口，
  是该公司披露结构本身不支持产品级拆分（见 11.4 节）,除非未来能找到一份专门的分部
  收入附注,否则这不是"下次多花时间就能查到"的类型。
- **2010、2018、2019 三个年份依然薄弱**：2010 年只有 2 行（Barrick、Newmont 都缺实际
  完成数，只有指引）；2018 年只有 4 行（Newmont、Barrick、Newcrest、Harmony，
  AngloGold/Gold Fields/Goldcorp/Kinross/Agnico/Polyus/Sibanye 2018 年实际数字本轮
  都没有查到——注意 Randgold 2018 是该公司作为独立公司的最后一个完整年份，本轮也没有
  查到它 2018 年具体产量数字，是个遗憾的缺口）；2019 年只有 6 行。
- **11–20 名区间**：第一轮的结论（"绝大多数年份是空的"）本轮基本没有改善，只是
  10 名以内的覆盖变厚了。这仍然是任务书预先提示过的、行业惯例导致的系统性缺口。
- **中国黄金企业只做了紫金矿业和山东黄金两家，且都只有个别年份**：招金矿业、中国黄金
  集团依然一行没有——`docs/NONSEC_SOURCES.md` 第 4 节已经确认招金矿业官网可连通，
  只是本轮没有真正打开文件读取分部数据,留作后续。
- **Sibanye-Stillwater 2019 年后的产量数字本轮没有查到**——收入结构（黄金占比
  13%–37%）已经查清楚（见 11.4 节），但作为排名所需的黄金产量盎司数没有查，所以
  没有写成 CSV 行，是"半查"状态,不是完全空白也不是完整。

### 11.8 下一步建议（更新版）

1. 逐年逐公司补齐 `gold_revenue_share_pct`，优先顺序：先补 Barrick（已知有铜业务、
   缺口最影响结论）中间年份、AngloGold Ashanti 2011–2019、Kirkland Lake/Newcrest/
   Randgold 等"应该接近 100%"的公司（哪怕只是为了验证这个假设，也应该抽查几年）；
2. Sibanye-Stillwater 2019–2025 年的黄金产量盎司数（能确定是否够格进入前 20，
   目前是收入结构已知、产量未知的悬案）；
3. Nordgold 2022 年之前的历史年份补齐产量+收入占比，并在补齐时同步应用 11.5 节定义的
   `panel_eligible` 规则（2022 起应为 `no`）；
4. 招金矿业、中国黄金集团的文本级核查（`docs/NONSEC_SOURCES.md` 第 4 节已列为待办）；
5. 评估是否把 Polyus、紫金矿业、Navoi/NMMC 正式纳入研究小组（或至少作为参照组并行展示），
   同时接受它们 `panel_eligible = no` 的现实——第 11.6 节的结论是：纯产量意义上六家小组
   从 2019 年起已经不完整，但没有一个现成替代者能同时满足"产量够大"和"数据可信到能撑起
   季度面板"两个条件,这需要研究负责人在方法论层面做取舍,而不是数据检索能单方面解决的
   问题。
