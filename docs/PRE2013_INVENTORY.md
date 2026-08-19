# 2005–2012 前 AISC 时代逐季可用性普查（PRE2013 Inventory）

**状态**：v1.0，机械性盘点，只读不改。方法论见第 2 节；结论均标注证据（文件名 + 原文片段）；
没有把握的地方标「未验证」，不猜。

**与既有两份文档的关系（做了什么、没重复什么）**：

- `docs/PRE2013_ANCHORS.md` 已经用概念级正则普查证明了「AISC 2013 年前不存在」「KGC 没有
  total cash cost」「GFI 的 NCE 覆盖 2008 起 4/4」「Barrick 的 G&A 叫 Corporate
  administration」——这些结论本文件**直接引用，不重新验证**，只在需要补充逐季颗粒度或
  AIC/cash operating cost 等本文件新增口径时才重跑普查。
- `docs/SEC_COVERAGE.md` 已经把「哪家公司哪一年在 EDGAR 上开始有真实内容」「40-F 空壳陷阱」
  「GFI 财年历史上是 6 月」这些结构性问题定了性，但明确留了尾巴：GFI 财年切换的**具体年份
  未精确定位**、南非公司季度节奏**未逐份验证**。本文件的增量工作主要就是把这些尾巴精确到
  「哪一份文件、哪一天」。
- 本文件**新增**、前两份文档都没有覆盖的发现：AU 的 `period_hint` 在 2005–2009 年的年报上
  系统性错标（第 5.1 节）；AEM 一份 2009 年 3 月的 6-K 把 FY2008 年度审计报表误装进
  "2008-Q1" 的桶里（第 4.1 节）；GFI/AU 的 SEC 申报**全程停留在 US GAAP**、真正的
  IFRS 断裂点其实不在南非申报人身上，而在两家用 40-F（非 20-F）的加拿大申报人身上，且
  精确落在 FY2011（第 5.3 节）；GFI 财年切换的精确窗口是 2010 年 7–12 月（第 4.3 节）。

---

## 1. 摘要：六家公司一句话结论

| 公司 | 一句话结论 |
|---|---|
| **NEM** | 六家里最干净。10-Q/10-K 全程季度制，`Costs applicable to sales` 这个锚点科目从 2005-Q1 一直用到 2013 年后，没有任何口径断裂，唯一的坑是 AISC 要等到 2012-Q4 才出现（早期自愿采用者）。 |
| **GOLD（Barrick）** | 2005 年前三季度在 EDGAR 上完全空白，2005-Q4 起才有真实内容；40-F 主文档是壳，真材料在 EX-99.x；2006 年 3 月完成收购 Placer Dome（$10.1B）；FY2011 从 **US GAAP**（~~加拿大 GAAP~~，见文末勘误二）切到 IFRS（40-F 强制口径）；AISC-cash 早在 2012-Q4 就出现，比 WGC 官方指引还早。 |
| **KGC（Kinross）** | 2005 年**全年零申报**（本地语料和抓取日志双重确认），但 FY2005 年度数据能从 2006 年 4 月提交的 40-F 里捞回来；从没用过 "total cash cost"；GEO（黄金当量盎司）从 2006-Q1 起就 4/4 污染；2006–2010 连续吃进 Bema Gold、Underworld Resources、Red Back Mining 三笔并购；FY2011 同样从加拿大 GAAP 切到 IFRS。 |
| **AEM（Agnico Eagle）** | 用 20-F 不用 40-F，所以**没有**被强制的 IFRS 断裂（全程 US GAAP）；但有一个真实的文件级陷阱——2009-03-31 提交的一份 6-K 把 FY2008 年度审计报表塞进了 "2008-Q1" 的 period_hint 桶里，同一桶里还混着真正的 2008 Q1 单季数据；2008 年 Q2/Q3 的真实单季财报在本地语料里疑似缺失（只有几份空壳 cover 6-K）。全程不报售出盎司（`ONLY_PRODUCED`）。 |
| **AU（AngloGold Ashanti）** | **最大的隐藏陷阱**：2005–2009 的五份年报（对应 FY2004/2006/2007/2008/2009）全部被现有 manifest 管线的 `period_hint` 字段错误地往后错标了 1–2 个季度，原因是这几年 SEC 索引里 20-F 的 `reportDate` 字段缺失、退化成等于 `filing_date`，导致按「6-K 式」的滞后映射规则误判。真实年度数据其实每年都在，但**不能信 period_hint，要看文件里"for the year ended"这句话**。季度层面，AU 的 Q1/Q3 通常只有简版经营+损益数据（无完整三表），Q2/Q4 才有完整审计包，2009–2010 一度改善为全年 4/4 完整，但不稳定。SEC 申报全程停留在 US GAAP，IFRS 只是南非本地口径的旁注，不构成断点。 |
| **GFI（Gold Fields）** | **【已推翻，见文末勘误】**~~唯一一家真正意义上「半年报为主」的公司：8 年 32 个季度里只有 12 个季度有完整财务报表，其余多是运营更新或 SENS 公告。~~ **实际：32 个日历季度全部有完整季度财报 6-K（三表齐全、离散季度列）。**财年切换的精确窗口是**2010 年 7 月 1 日至 12 月 31 日**（一份 6 个月的过渡期 20-F，2011-03-31 提交）——此前财年止于 6 月 30 日，此后是日历年。NCE 从 2008-Q2 起披露，是 2013 年前唯一真正意义上的全成本口径。和 AU 一样，GFI 的 SEC 申报全程停留在 US GAAP，IFRS 从未成为其 20-F 的主口径。 |

**总体数字**：192 个「公司×年×季」格子（6×8×4）中，manifest 分类给出 **151 个（78.6%）**
有真实财报文件（`REAL`）、27 个（14.1%）只有运营更新（`OPS_ONLY`）、7 个（3.6%）只有监管
公告等非财务文件（`OTHER_ONLY`）、7 个（3.6%）完全无申报（`NONE`）。但这个数字**不能直接
当"可提取"用**——AU 的 26 个 `REAL` 格子里有相当一部分年报被错误分到了别的季度（见上），
GFI 的 12 个 `REAL` 格子集中在极少数月份。逐公司细节见第 4 节。

---

## 2. 方法说明

- **数据来源**：`data/raw/manifest.csv`（6,880 行，`fetch_filings.py` 产出的既有语料元数据，
  含 `doc_role`、`has_financial_statements`、`has_operating_stats`、`report_date`、
  `filing_date`、`period_hint` 等字段）。本文件对 2005–2012 年份的 2,551 行做了：
  1. 按 `(ticker, period_hint)` 建立网格，用 `doc_role` 是否属于
     `{financial_statements, combined_release, annual_financial_statements,
     annual_combined_release}` 判定该季度是否有"真财报"；
  2. 对全部 `.htm/.html` 文件（PDF 未纳入本轮正则扫描，见下方"已知覆盖缺口"）做去标签
     全文正则扫描，统计 22 个概念（AISC 两种变体、AIC、total cash cost、cash operating
     cost、NCE、CAS、cost of sales、production cost、GEO、gold segment revenue、
     royalty、G&A、exploration、capex、rehab、reclamation、accretion、tax paid、
     oz sold、net interest、IFRS）在"真财报"文件与"任意文件"里各自首次出现的
     `period_hint`；
  3. 对若干关键结论做了**逐文件人工核实**（第 8 节，≥6 份，实际核实了 17 处）。
- **脚本位置**（本次新增，供复核）：
  - `/tmp/claude-0/-home-user-agents/f3c15123-340b-5994-9540-4d134f7a1688/scratchpad/inv/grid.py`
    ——从 manifest.csv 构建可用性网格，输出 `grid.json`。
  - `/tmp/claude-0/-home-user-agents/f3c15123-340b-5994-9540-4d134f7a1688/scratchpad/inv/concepts.py`
    ——概念级正则扫描，输出 `found_real.json`（真财报文件中的命中）、`found_any.json`
    （任意文件中的命中）、`samples.json`（每个"公司×概念"最多 3 条原文片段样本）。
  - 复用了既有 `probe_pre2013.py` / `probe_gfi_nce.py` / `probe_unitcost.py`
    （`docs/PRE2013_ANCHORS.md` 的产出脚本，本轮只读不改，用于交叉验证不重复劳动）。
- **已知覆盖缺口（未验证/需要后续处理）**：
  - AU 有 328 份 PDF、GFI 有 384 份 PDF，其中 AU 18 份、GFI 53 份**没有同名 .htm 版本**
    （即内容只存在于 PDF 里），本轮的概念正则扫描**没有解析这些 PDF**（`manifest.csv`
    自带的 `has_financial_statements` 标记对 PDF 是解析过的，网格判断没有缺口，但本文件
    第 4 节引用的具体原文片段全部来自 .htm，PDF-only 文件的科目原文措辞未逐份复核）。
  - `doc_role` 分类是关键词计数（≥2 个不同短语命中记为"有财报"），存在软性边界案例——
    第 8.4 节验证了 Barrick 一份 AIF 文件被计入"有财报"但实际未包含完整三张报表（同一
    accession 下的另一份 exhibit 才有）；这类边界案例**不改变格子级别的可用性结论**（同
    季度总有别的文件真正带表），但意味着**不能不加验证地直接用某个单一"REAL"标记的文件**，
    必须看文件名和内容。

---

## 3. 可用性网格

图例：**R** = 该季度至少一份真财报（资产负债表/利润表/现金流量表齐全或接近齐全）；
**O** = 只有运营/生产更新（有产量、单位成本，没有完整三表）；**x** = 只有监管公告/新闻稿等
非财务文件；**.** = 该季度本地语料完全没有申报。方括号是该季度"真财报"候选文件数（供交叉核实
用，不代表数字质量）。**灰色高亮的行在第 4 节有专门的错标/断裂说明，不能直接读字面。**

### AEM
| 年 | Q1 | Q2 | Q3 | Q4 | 备注 |
|---|---|---|---|---|---|
| 2005 | R | R | x | R | |
| 2006 | x | R | . | R | |
| 2007 | R | R | x | R | |
| 2008 | **R\*** | x | O | R | **Q1 桶被 FY2008 年报污染，见 §4.1** |
| 2009 | R | R | R | R | |
| 2010 | x | x | R | R | |
| 2011 | R | R | R | R | |
| 2012 | R | R | R | R | |

### AU
| 年 | Q1 | Q2 | Q3 | Q4 | 备注 |
|---|---|---|---|---|---|
| 2005 | O | **R\*** | O | R | **Q2 桶实际是 FY2004 年报，见 §4.2** |
| 2006 | R | R | R | R | |
| 2007 | O | **R\*** | O | R | **Q2 桶实际是 FY2006 年报** |
| 2008 | **R\*** | O | R | R | **Q1 桶实际是 FY2007 年报** |
| 2009 | **R\*** | R | R | R | **Q1 桶实际是 FY2008 年报** |
| 2010 | **R\*** | R | R | R | **Q1 桶实际是 FY2009 年报；Q4 起 report_date 恢复可信** |
| 2011 | O | R | R | R | |
| 2012 | R | R | R | R | |

### GFI
| 年 | Q1 | Q2 | Q3 | Q4 | 备注 |
|---|---|---|---|---|---|
| 2005 | O | R | R | O | 财年止 6/30，Q2/Q3 是半年报+年报窗口 |
| 2006 | O | R | R | O | 同上 |
| 2007 | O | R | O | O | |
| 2008 | O | R | R | O | |
| 2009 | O | R | O | O | |
| 2010 | O | R | O | **R\*** | **Q4 桶是 6 个月过渡期年报（2010-07~12），见 §4.3** |
| 2011 | O | O | O | R | 财年已切到日历年，年报回到 Q4 |
| 2012 | O | O | O | R | |

### GOLD
| 年 | Q1 | Q2 | Q3 | Q4 | 备注 |
|---|---|---|---|---|---|
| 2005 | . | . | x | R | **前三季度 EDGAR 零内容，见 §4.4** |
| 2006 | R | R | R | R | Placer Dome 收购完成于本年 3 月 |
| 2007 | R | R | R | R | |
| 2008 | R | R | R | R | |
| 2009 | R | R | R | R | |
| 2010 | R | R | R | R | 最后一年加拿大 GAAP |
| 2011 | R | R | R | R | **FY2011 起改用 IFRS，见 §4.4/§5.3** |
| 2012 | R | R | R | R | AISC-cash 于 Q4 首次出现 |

### KGC
| 年 | Q1 | Q2 | Q3 | Q4 | 备注 |
|---|---|---|---|---|---|
| 2005 | . | . | . | . | **全年零申报，见 §4.5；FY2005 数据靠 2006 年报补** |
| 2006 | R | R | R | R | |
| 2007 | R | R | R | R | Bema Gold 收购完成于本年 2 月 |
| 2008 | R | R | R | R | |
| 2009 | R | R | R | R | |
| 2010 | R | R | R | R | Red Back Mining / Underworld Resources 收购完成于本年 |
| 2011 | R | R | R | R | **FY2011 起改用 IFRS** |
| 2012 | R | R | R | R | AISC-cash 于 Q4 首次出现 |

### NEM
| 年 | Q1 | Q2 | Q3 | Q4 | 备注 |
|---|---|---|---|---|---|
| 2005–2012 | R | R | R | R | 全程 10-Q/10-K，US GAAP 全程不变，唯一变化是 2012-Q4 首次出现 AISC |

---

## 4. 逐公司详述

### 4.1 AEM（Agnico Eagle Mines）——申报节奏、口径、断裂点

**申报形式**：20-F（不是 40-F）+ 不定期 6-K。这个选择本身就是本轮最重要的发现之一——见
§5.3，AEM 因为用 20-F 报告，选择全程使用 US GAAP，**没有被 2011 年加拿大强制 IFRS 卷入**。

**口径首现**（真财报文件中，`concepts.py` 扫描）：

| 口径 | 首现 period | 证据文件 | 原文片段 |
|---|---|---|---|
| total cash cost | 2005-Q1 | `2005-Q1_0001047469-05-014784_a2158340z6-k.htm` | "In the first quarter of 2005 total cash costs per ounce decreased to $67 per ounce" |
| cash operating cost | 2005-Q2 | — | 与 total cash cost 同义混用 |
| Costs applicable to sales | 2005-Q4 | `2005-Q4_0001047469-06-004056_a2168598z20-f.htm` | "…recognized in costs applicable to sales in the same period as the revenue…" |
| AISC（含 cash 变体） | **2012-Q4** | `2012-Q4_0001047469-13-003581_a2211934z20-f.htm` | "…total cash costs per ounce, all-in sustaining costs, minesite costs per tonne…" |
| AIC / NCE | 全程未见 | — | AEM 不是 GFI 式全成本口径公司 |

**GAIM 输入项**：`docs/PRE2013_ANCHORS.md` 已确认 AEM 全程**不报售出盎司**（只报产量，
`gold_oz_sold` 需打 `ONLY_PRODUCED`），且 `cash_tax_paid` 是全公司最弱项（2009–2012 仅
1/4）。本轮未发现新的缺项，直接沿用。

**本轮新发现的两个文件级陷阱（未见于既有两份文档）**：

1. **"2008-Q1" 桶被 FY2008 年度审计报表污染**。accession `0001047469-09-003540`
   于 **2009-03-31** 提交（比它实际覆盖的期间晚了整整一年），随附的
   `a2192067zex-99_3.htm` 标题就是 "Exhibit 99.3 Annual Audited Consolidated
   Financial Statements (Prepared in accordance with United States GAAP)"，正文写明
   "REPORT OF INDEPENDENT REGISTERED PUBLIC ACCOUNTING FIRM…as of December 31, 2008"、
   "Years ended December 31, 2008"——这是 **FY2008 全年度**的审计报表，混在 2009 年
   股东周年大会委托书（`zex-99_1` 是 Notice of 2009 AGM）里一起提交，但 manifest 管线
   按 6-K 滞后映射规则把它标成了 "2008-Q1"。同一个 period_hint 桶里还混着一份**真正的**
   2008 年 Q1 数据（`2008-Q1_0001104659-08-032653_a08-14181_16k.htm`，2008-05-13 提交，
   `doc_role=combined_release`）。**任何直接读取"2008-Q1"标签取数的脚本都会有 50% 概率
   抓错文件（拿到年度数字当季度数字）**，必须打开文件核对"for the/period/year ended"字样。
2. **AEM 2008 年 Q2、Q3 的真实单季财报在本地语料里疑似缺失**。这两个季度分别只有
   `2008-Q2_0001047469-08-009549_a2187529z6-k.htm`（1,940 字符，纯 6-K 封面，无正文）和
   `2008-Q3_0001047469-08-012005_a2188564z6-k.htm`（1,938 字符，同上）以及若干
   filer `0001104659` 提交的小体量（8–20KB）通知性 6-K，**没有一份体量接近典型财报
   exhibit（通常 200KB+）**。这与加拿大 NI 51-102 要求季度中期财报的规范不符，**判断
   为语料抓取缺口而非公司未披露，标记"未验证"，建议补抓**。

### 4.2 AU（AngloGold Ashanti）——最大的隐藏陷阱

**申报形式**：20-F 年报 + 不定期 6-K，6-K 数量虚高（大量 SENS 型公告），已知问题。

**本轮最重要的新发现：2005–2009 年的 5 份年报全部被 `period_hint` 错标**。核实方法：
对每份年报打开正文，搜索 "for the year ended December 31, 20XX"，与 manifest 给出的
`period_hint` 对比：

| 提交日期 | manifest 给出的 period_hint | 正文实际声明的年度 | 判断 |
|---|---|---|---|
| 2005-07-14 | `2005-Q2` | "For the year ended December 31, **2004**"（`2005-Q2_0001205613-05-000121_aga_main.htm`） | **错标，晚了 2 个季度** |
| 2006-03-20 | `2005-Q4` | FY2005 | 正确（凑巧落在滞后映射窗口内） |
| 2007-07-09 | `2007-Q2` | "For the year ended December 31, **2006**"（`2007-Q2_0001205613-07-000086_aga_20f.htm`） | **错标** |
| 2008-05-19 | `2008-Q1` | "For the year ended December 31, **2007**"（`2008-Q1_0001205613-08-000079_aga_20f.htm`） | **错标** |
| 2009-05-05 | `2009-Q1` | "For the year ended December 31, **2008**"（`2009-Q1_0001205613-09-000042_aga_combined.htm`） | **错标** |
| 2010-04-19 | `2010-Q1` | "For the year ended December 31, **2009**"（`2010-Q1_0001205613-10-000058_aga_combined.htm`） | **错标** |
| 2011-03-31 起 | 与 report_date 一致 | — | 恢复正确（`report_date` 字段此后被 SEC 正确填充） |

**根因**：manifest 的 `infer_period()` 逻辑对 6-K 用"申报月份滞后 1 个季度"的规则做映射，
这个规则对准时申报的文件有效，但 AngloGold 这几年的 20-F 是在财年结束后 **5–7 个月**才
提交（法定 20-F 截止是财年结束后 6 个月内，AngloGold 常常压线甚至压线之后几天提交），
超出了滞后映射假设的 1 个季度窗口，导致往后错标 1–2 个季度。**这不是"缺数据"，是"数据在，
标签错"**——AU 2004–2012 每一个日历年都有一份真实年报，只是不能信 `period_hint`，必须
用文件正文的"for the year ended"核对。**任何下游用 AU 数据的脚本都必须先修这个映射，
否则会把 FY2004 的数字当成 FY2005 Q2 的数字用。**

**季度层面的真实节奏**：核实了 `2005-Q1_0001205613-05-000078_aga_quarter.htm`——标题是
"REPORT FOR THE QUARTER ENDED MARCH 31, 2005 PREPARED IN ACCORDANCE WITH IFRS"，
内容有生产、金价、部分损益数字（如 "Cost of sales (3,415)"），但**不含独立的资产负债表/
现金流量表表格**（0 个 `<table>` 标签，表格靠纯文本对齐），因此被正确分类为 `OPS_ONLY`
而非 `REAL`。对比 `2005-Q2_...aga_finstat.htm`（H1 2005 正式财务报表，"SIX MONTHS ENDED
JUNE 30, 2005"），后者才是完整审计/审阅的三表package。**结论：AU 的 Q1/Q3 是"简版损益
+经营数据"，Q2/Q4（半年报+年报）才是完整财务报表**——这个格局在 2005、2007 年最典型
（OROR），2009–2010 一度改善成全年 4/4 都有完整报表，但不稳定，需要逐季核实，不能假设
某一年份的格局会延续到下一年。

**SEC 申报口径**：见 §5.3，AU 的 SEC 财务报表全程是 US GAAP，IFRS 只在叙述性文字里出现。

### 4.3 GFI（Gold Fields）——财年切换精确定位 + 半年报为主

**财年切换的精确窗口（本轮最重要的定位工作）**：`2010-Q4_0001193125-11-084306_d20f.htm`
（提交于 2011-03-31，`report_date=2010-12-31`）正文明确写着：

> "transition period from July&nbsp;1, 2010 to December&nbsp;31, 2010"（多处出现，含
> "Gold Fields notes that this transition report on Form 20-F…"）

即：GFI 财年历史上止于 **6 月 30 日**（最后一个完整旧财年是 FY2010，对应
`2010-Q2_0001193125-10-272998_d20f.htm`，`report_date=2010-06-30`），随后提交了一份
覆盖 **2010 年 7 月 1 日至 12 月 31 日（6 个月过渡期）**的 20-F 作为切换文件，此后
**FY2011 起是标准日历年**（`report_date=2011-12-31`）。这比 `docs/SEC_COVERAGE.md`
第 8 节"未精确定位"的描述精确了整整一步——**切换发生在 FY2010→FY2011 之间，过渡期是
2010H2，不是 2009 年附近**。

**半年报为主的证据**：32 个季度格子里只有 12 个是 `REAL`，且这 12 个几乎全部落在 Q2/Q3
（对应旧财年下的年报/半年报发布窗口）或切换后的 Q4（新财年年报）。其余 20 个季度是
`OPS_ONLY`——GFI 每季度都发运营更新（产量、单位成本），但完整审计三表只在半年/全年
节点出现。`2011-Q1_0001205613-11-000054_gf_fatalities.htm`（一份矿难死亡通报）被正确
分类为 `other`——核实内容确系非财务性监管公告，证明 GFI 的 6-K 洪水（2011-Q1 单季 33 份
`other` vs 4 份 `ops_only`）确实主要是 SENS 型公告，与 `docs/SEC_COVERAGE.md` 的判断
一致。

**成本口径**：沿用 `docs/PRE2013_ANCHORS.md` 的 NCE 结论（2008-Q2 起 4/4），本轮补充了
"all-in cost"这个说法本身的出处——`2008-Q3_0001205613-08-000156_gf_annual.htm`：
"…the real all in cost of producing an ounce of gold, or NCE per ounce of gold…"，
即 GFI 自己把"all-in cost"等同于 NCE，这是**叙述性说法**，不是独立报表科目；真正的
表格科目名是 Notional Cash Expenditure（NCE）。

**SEC 申报口径**：见 §5.3，全程 US GAAP，无断裂。

### 4.4 GOLD（Barrick）——2005 年前三季度空白 + Placer Dome + 40-F 空壳

**2005 年前三季度 EDGAR 零内容**：本地语料从 `2005-Q3_0000950157-05-000818_form6k.htm`
才开始有文件，前两季度完全没有。与 `docs/SEC_COVERAGE.md` 的整体判断（FPI 电子化申报
2002–2003 年才起步，早年零星）一致，本轮进一步确认这个空白**具体延伸到了 2005 年 Q1–Q2**，
Barrick 一直到年底才恢复稳定的季度电子申报节奏。

**Placer Dome 收购**（本轮精确定位到月份）：`2006-Q1_0000909567-06-000713_o31437exv99w1.htm`
（2006 年 Q1 业绩发布）原文："In March 2006, Barrick completed the acquisition, and
Placer Dome became a wholly-owned subsidiary."，收购总代价约 $10.1–10.4 billion；
紧接着 Q2 又把 Placer Dome (CLA) Limited 的部分资产以 $1.641 billion 转售给
Goldcorp（`2006-Q2_0000909567-06-001389_o32613exv99w1.htm`）。**这是一个真实的规模
断裂点**：2006 年起 Barrick 的资产负债表、产量、成本结构都因这笔收购发生跳变，任何
2005→2006 的环比/同比分析都要标注这一点。

**40-F 空壳陷阱**（沿用并验证了 `docs/SEC_COVERAGE.md` 的判断）：抽样打开
2006-Q4 同一批文件——`o35578exv99w1.htm`（Annual Information Form，只讨论财报但
不含完整三表本身）、`o35578exv99w3.htm`（"Management's Responsibility for Financial
Statements"，208 个表格，真正的财务报表）、`o34936exv99w1.htm`（"YEAR-END REPORT
2006", 364 个表格，真正的完整业绩包）——**证实了同一处 accession 下不同 exhibit 的
含金量天差地别**，AIF 本身即便被 `doc_role` 分类器计入"有财报"（因为叙述中提到
"cash flow statement"、"segment information"等词），实际不含表格数据，真材料在
`exv99w3`/独立发布的 Year-End Report 里。**提取 agent 不能只挑 period_hint 桶里的
第一份文件，要挑对文件。**

**AISC-cash 早期采用**：`2012-Q4_0001193125-13-062690_d482590dex991.htm`（Q4/FY2012
业绩发布）——"Gold all-in sustaining cash costs for the fourth quarter and full year
2012 of $972 per ounce…"，另一份文件披露 FY2012 全年 $945/oz——与
`docs/SEC_COVERAGE.md` 第 7 节已更正的结论一致，本轮重新验证，确认无误。

**IFRS 断裂**：见 §5.3，精确落在 FY2011。

### 4.5 KGC（Kinross）——2005 年零申报 + 三连并购

**2005 年零申报（双重验证）**：本地语料目录从 2004-Q3 直接跳到 2006-Q1，中间完全没有
2005 年任何文件；上一轮抓取脚本留下的日志（`fetch_2005_2012.log`）也明确记录
"KGC 2005-Q1/Q2/Q3/Q4: NO DOCS AT ALL"，两个独立信号一致，**判断为真实缺口而非本轮
误判**（但日志来自既往会话，本轮未重新直连 EDGAR 复核，仍标"高置信度未独立复核"）。

**FY2005 年度数据的补救路径**：2006 年 4 月提交的首份 40-F
（`2006-Q1_0001047469-06-004477_a2169058z40-f.htm`，附件
`a2169058zex-99_1.htm`）正文明确写着 "FOR THE YEAR ENDED DECEMBER 31, **2005**"——
说明**KGC 的 FY2005 年度数字是可以拿到的**，只是没有季度颗粒度，且这份文件按 manifest
规则被标成了"2006-Q1"（同样属于滞后映射把年报标进了错误季度的现象，但这里错标的方向
是"年报→第二年 Q1"而不是像 AU 那样错开好几个季度，原因是 KGC 这份 40-F 提交时间
（4 月初）本身就接近 KGC 财年结束后的正常申报窗口，属于边界情况，未系统性影响其余年份，
其余年份的 40-F 都在 report_date 与 filing_date 一致性检查中通过）。

**三笔收购**（关键词命中数确认时间点，与公开史实吻合）：
- Bema Gold：2006 年 25 份文件提及（收购宣布期），2007 年 17 份（收购于 2007 年 2 月完成
  后的整合期）；
- Red Back Mining：仅 2010 年出现，48 份文件（2010 年 9 月完成的大额收购，$7.1B 规模）；
- Underworld Resources：2008–2010 年递增（2、6、13 份），2010 年 5 月完成收购。

三笔收购叠加意味着 KGC 2007–2010 年的资产结构、GEO 基准、地域分布逐年都在跳变，
**不建议对 KGC 2006–2010 做资产层面的环比连续性假设**。

**GEO 污染**（沿用 `docs/PRE2013_ANCHORS.md`）：`gold equivalent ounce` 从 2006-Q1 起
4/4 命中，`total cash cost` 全程 0 命中——本轮重新扫描确认无误（`total_cash_cost` 概念
2005–2012 命中数 = 0）。

**IFRS 断裂**：见 §5.3，精确落在 FY2011（40-F 强制口径，与 Barrick 同构）。

### 4.6 NEM（Newmont）——基准公司，全程无断裂

**最干净的一家**：10-Q（Q1–Q3）+ 10-K（Q4）全程稳定，`report_date` 与实际期间完全一致，
没有发现任何 period_hint 错标。`Costs applicable to sales (exclusive of depreciation,
depletion and amortization)` 这个锚点科目从 `2005-Q1_0001193125-05-090450_d10q.htm`
起就是这个措辞，一直延续到 2013 年后（与 `docs/PRE2013_ANCHORS.md` 已确认的"锚点连续"
结论一致）。唯一的真实变化是 **2012-Q4 首次出现 AISC**
（`2012-Q4_0001144204-13-010569_v335918_ex99-1.htm`："All-in sustaining cost[3] of
$1,149 per ounce"）——早期自愿采用者，早于 WGC 2013 年 6 月正式指引。美国本土申报人，
US GAAP 全程不变，无 IFRS 断裂。唯一薄弱项是 `cash_tax_paid`（`docs/PRE2013_ANCHORS.md`
已指出 2009–2012 部分年份弱），本轮未发现新问题。

---

## 5. 跨公司共同发现：三个系统性陷阱

### 5.1 `period_hint` 对"迟到年报"不可靠

manifest 的滞后映射规则（`infer_period()`）假设 6-K/年报的申报日期距实际期间不超过约
1 个季度。这个假设对 NEM、GOLD、KGC、AEM、GFI 的绝大多数年报成立（它们的 `report_date`
字段本身就正确），**唯独 AU 在 2005–2009 年间因为 SEC 索引里 `report_date` 字段退化成
等于 `filing_date`**（而 AU 的 20-F 又习惯性地压线甚至过线提交，比法定 6 个月期限还晚），
导致映射规则系统性地把年报标错 1–2 个季度（详见 §4.2 的核对表）。AEM 也出现了一次孤立
的错标（§4.1，2009 年 3 月的 6-K 把 FY2008 年报塞进 "2008-Q1"），但那是个案，不是系统性
问题。**给下游的建议**：任何脚本读取 AU 的年度数据，必须以文件正文的"for the year ended"
为准，不能信 `period_hint`；读取其余五家公司时，`period_hint` 基本可信，但年报类文件仍
建议做一次文本层面的期间自检（成本很低，收益是排除类似 AEM 那种孤立个案）。

### 5.2 `doc_role` 分类器有已知边界案例，但格子级结论稳健

`has_financial_statements` 用的是"≥2 个关键短语命中"规则，个别文件（如 Barrick 的
AIF）会因叙述性提及财报相关词汇而被计入"有财报"，但本身不含完整表格。本轮核实了这类
边界案例，发现**它们从未导致某个季度格子从"有真材料"变成"没有真材料"**——因为同一
accession 或同一季度总有别的文件真正带表。因此第 3 节的网格在**格子（有/无真材料）**
这个粒度上是可信的，但**在"选中哪一份具体文件来读数"**这个粒度上不可信，必须让提取
agent 打开候选文件核实内容，不能盲选 manifest 里排在前面的那个。

### 5.3 真正的 IFRS/GAAP 断裂点不在南非申报人身上，而在两家用 40-F 的加拿大申报人身上

这是本轮对任务书原始假设（"IFRS 首次采用——南非/加拿大申报人 2005–2011 各不相同"）的
一次重要修正，逐点核实如下：

- **AU、GFI（南非，20-F）**：核实了 2005、2008、2009、2010、2011 多个年份的 20-F 正文
  "prepared in accordance with…"表述，**全部年份的 SEC 主财务报表都是 "U.S. generally
  accepted accounting principles (US GAAP)"**，IFRS 只作为南非本地/JSE 法定口径的旁注
  出现（"IFRS financial statements are furnished as unaudited additional
  information"一类的表述）。**结论：AU、GFI 在本研究覆盖的 2005–2012 年 SEC 申报口径
  上没有发生 GAAP 断裂**，域内 IFRS 强制令（2005 年 JSE 层面）不影响 SEC 财报本身。
- **GOLD、KGC（加拿大，40-F/MJDS）**：核实了 FY2010 vs FY2011 的年报正文——
  `GOLD` 的 `2010-Q4_..._1ex99d3.htm`："prepared in accordance with United States
  generally accepted accounting principles"；`2011-Q4_..._dex993.htm`："prepared in
  accordance with International Financial Reporting Standards"。`KGC` 的
  `2010-Q4_..._a2202509zex-99_1.htm` 只出现 1 次 "Canadian GAAP"、0 次 IFRS；
  `2011-Q4_..._a2208497zex-99_1.htm` 出现 5 次 IFRS/International Financial
  Reporting Standards。**两家精确同步在 FY2011 从加拿大 GAAP 切到 IFRS**，与加拿大
  强制上市公司 IFRS 换轨日（2011 财年起）完全吻合，这是因为 40-F/MJDS 要求跟随加拿大
  本土监管口径，无法像 20-F 那样自由选择 US GAAP。
- **AEM（加拿大，但用 20-F）**：核实了 `2011-Q4_0001047469-12-003484_a2208447z20-f.htm`
  ——FY2011 年报里反复出现 "prepared in accordance with US GAAP"，**没有**切换到 IFRS。
  **结论：AEM 因为选择用 20-F（而不是像 GOLD/KGC 那样用 40-F）申报，全程停留在 US GAAP，
  规避了加拿大 2011 年的强制 IFRS 换轨**。这是六家公司里唯一一个"表单选择决定是否有
  断裂"的案例。
- **NEM（美国本土）**：全程 US GAAP，无涉。

**给方法论的提醒**：判断某公司是否有 GAAP 断裂，不能按"国籍"分类（"南非公司都在
2005 年切 IFRS""加拿大公司都在 2011 年切 IFRS"），要按**申报表单类型**分类——
40-F/MJDS 跟随本国口径会真的断，20-F 可以自由选择、往往选 US GAAP 从而不断。

---

## 6. 建议的提取顺序与优先级

**最容易、优先做**：
1. **NEM** —— 全程干净，10-Q/10-K 无断裂，直接按现有 2013 年后的抽取逻辑复用即可，
   唯一需要注意的是 2005–2011 段没有 AISC，走 pseudo-AISC 降级路线（`total cash cost`
   + CAS 锚点）。
2. **GOLD（2006–2012）** —— 40-F 附件结构清楚（AIF / Financial Statements /
   Year-End Report 三件套），已知怎么挑文件；唯一要处理的是 FY2011 的 GAAP→IFRS 断点
   （需要在切换年份前后核对科目是否连续可比，特别是 reclamation/rehabilitation 准备金
   计提方法在 IFRS 下可能与 US GAAP 下不同）；2005 年只能做 Q4/年度。
3. **KGC（2006–2012）** —— 结构与 GOLD 类似（40-F+EX-99.x），但要打 GEO_BASIS 标记、
   叠加三笔并购的资产跳变提示；2005 年整年放弃，用 2006 年 40-F 附带的 FY2005 年度数字
   做一个单点补充（不做季度）。

**中等难度**：
4. **AEM（2005–2012）** —— 20-F/US GAAP 全程无断裂是好消息，但要先修复"2008-Q1"桶的
   污染（用文本期间自检剔除年报误标）、并单独核实 2008 Q2/Q3 是否真的缺数据（建议先
   尝试用 SEC 全文检索按日期窗口重新拉取这两个季度，如果确认永久缺失就整体降级为
   "半年推算"）。全程不报售出盎司，需要 `ONLY_PRODUCED` 降级处理。

**最难、部分格子应直接放弃**：
5. **AU（2005–2012）** —— 必须先在提取管线里加一段"年报期间自检"逻辑（读取文件正文的
   "for the year ended"，覆盖 manifest 的 period_hint），否则会系统性地把年度数字错配
   到季度标签上。修复这个之前**不建议任何自动化批量提取**。季度层面 Q1/Q3 只有简版数据，
   完整三表集中在 Q2/Q4，需要逐年判断哪年是"全季度"哪年是"半年报模式"（本轮核实到
   2005、2007 是明显的半年报模式，2009–2010 一度是全季度模式，不能假设）。
6. **GFI（2005–2012）** —— 32 个季度只有 12 个有真材料，其余 20 个只能做运营层面的
   产量/单位成本推算，缺完整资产负债表和现金流量表。**建议直接把 GFI 的非年报/半年报
   季度（每年的 Q1，多数年份的 Q3/Q4）标记为"不可提取三表口径，只能提取 NCE/产量"，
   不要试图强行拆分成 4 个季度**——按 `METHODOLOGY.md` 的半年度记法处理（如
   "2008H1"/"2008H2"），不要伪造季度颗粒度。财年切换窗口（2010H2 过渡期）单独作为
   一条"6 个月"记录处理，不要拆成两个季度也不要按 3 个月折算。

**总结一句话**：NEM > GOLD ≈ KGC（结构清楚，断点已定位）> AEM（有个文件级陷阱要先修）
> AU（有系统性标签错误要先修，季度粒度本身也不稳定）> GFI（结构性只有半年报，别浪费
力气伪造季度）。

---

## 7. 未验证事项清单

- KGC 2005 年零申报的结论依赖本地语料 + 一份既往会话遗留的抓取日志双重信号，**本轮没有
  直连 EDGAR 全文检索/submissions API 做第三方复核**，理论上不能完全排除是抓取脚本的
  日期窗口设置问题（虽然可能性很低，因为两个独立来源一致）。
- AU/GFI 384+328 份 PDF 中分别有 18/53 份没有同名 htm，本轮的概念级正则扫描（AISC/AIC/
  total cash cost 等首现年份判定）**没有覆盖这些纯 PDF 文件**，理论上存在"某个口径其实
  更早出现在一份纯 PDF 里，但被本轮扫描漏掉"的可能，需要用 pypdf 补一轮扫描。
- AEM 2008 年 Q2/Q3 财报缺失，判断为"语料抓取缺口"而非"公司未披露"，但**没有做 EDGAR
  全文检索复核**来确认真的存在应抓未抓的文件，也没有排除"公司当年确实只发了摘要没发
  完整报表"这个可能性。
- AU 的年报错标模式核实到了 5 个具体样本点（FY2004/2006/2007/2008/2009），**没有逐份
  验证 2011、2012 年是否也有类似但更隐蔽的错标**（本轮抽样显示这两年 report_date 已经
  正确，但只抽查了年报，没有抽查同年的季度 6-K 是否也可能有类似问题）。
- 第 4 节列出的"口径首现年份"全部来自**本地语料库现有覆盖范围**内的首次正则命中，
  不代表该公司在 SEC 之外（如 SEDAR、公司官网历史年报 PDF）没有更早的同类披露——本报告
  的结论范围严格限定在"本项目 `data/raw/` 目录当前持有的文件"。
- GAIM 输入项里的 `net_interest`、`cash_tax_paid`、`corp_ga` 等概念本轮用的是较宽泛的
  正则（比如 "reclamat" 会命中一切提到"复垦义务"的风险因素段落，不只是真正的报表科目
  行），**首现年份的判定是"文本层面首次出现该话题"的上界，不等于"该年该季度的报表里
  一定有一条独立、可取数的科目行"**——第 4 节给出的具体例外（如 AEM 不报售出盎司、
  AEM 现金税实缴弱）沿用了 `docs/PRE2013_ANCHORS.md` 更严格的逐项核实结论，但本轮
  新增的宽口径正则结果本身需要提取 agent 逐份确认是否真的落在一条独立科目行上，
  不能直接当"该项可得"的证据使用。

---

## 8. 附录：抽样验证记录（≥6 份文件逐份核实，实际核实 17 处）

| # | 文件 | 核实目的 | 核实方法与结果 |
|---|---|---|---|
| 1 | `data/raw/GFI/2010-Q4_0001193125-11-084306_d20f.htm` | GFI 财年切换的精确窗口 | 全文检索 "transition period"，命中 "from July 1, 2010 to December 31, 2010"，确认 6 个月过渡期年报 |
| 2 | `data/raw/AU/2005-Q2_0001205613-05-000121_aga_main.htm` | AU period_hint 是否可信 | 全文检索 "for the year ended"，命中 "December 31, 2004"，与 period_hint "2005-Q2" 不符，确认错标 |
| 3 | `data/raw/AU/2008-Q1_0001205613-08-000079_aga_20f.htm`、`2009-Q1_..._aga_combined.htm`、`2010-Q1_..._aga_combined.htm` | 验证错标是否为系统性模式 | 逐份核实，分别命中 FY2007/FY2008/FY2009，确认连续 4 年都错标，模式一致 |
| 4 | `data/raw/GOLD/2006-Q4_0000909567-07-000544_o35578exv99w1.htm`（AIF）vs `…exv99w3.htm`（Financial Statements）vs `2006-Q4_0000909567-07-000250_o34936exv99w1.htm`（Year-End Report） | 40-F 附件哪份真正带表 | 分别数 `<table` 标签：AIF 未直接命中三表标题，exv99w3 有 "Management's Responsibility for Financial Statements" + 208 个表格，Year-End Report 有 364 个表格；确认真材料在后两份 |
| 5 | `data/raw/AU/2005-Q1_0001205613-05-000078_aga_quarter.htm` | 验证 `OPS_ONLY` 分类是否正确 | 提取纯文本核实标题 "REPORT FOR THE QUARTER ENDED MARCH 31, 2005"，含损益片段但 0 个 `<table>` 标签、无独立资产负债表/现金流量表标题，确认分类合理 |
| 6 | `data/raw/GFI/2011-Q1_0001205613-11-000054_gf_fatalities.htm` | 验证 `other` 分类是否正确 | 打开确认内容是矿难死亡通报（6-K 封面 + 通告），非财务文件，分类合理 |
| 7 | `data/raw/GOLD/2010-Q4_..._1ex99d3.htm` vs `2011-Q4_..._dex993.htm` | Barrick GAAP→IFRS 断裂的精确年份 | 分别检索 "prepared in accordance with"，FY2010 命中 US GAAP，FY2011 命中 IFRS，确认断点在 FY2011 |
| 8 | `data/raw/KGC/2010-Q4_..._a2202509zex-99_1.htm` vs `2011-Q4_..._a2208497zex-99_1.htm` | Kinross GAAP→IFRS 断裂的精确年份 | 关键词计数，FY2010 命中 "Canadian GAAP"=1/"IFRS"=0，FY2011 命中 "IFRS"=5，确认与 Barrick 同步 |
| 9 | `data/raw/AEM/2011-Q4_0001047469-12-003484_a2208447z20-f.htm` | 验证 AEM 是否也在 FY2011 切换 | 检索 "prepared in accordance with"，全部命中 "US GAAP"，无 IFRS，确认 AEM 未切换（对照组） |
| 10 | `data/raw/AEM/2008-Q1_0001047469-09-003540_a2192067zex-99_3.htm` | 验证 "2008-Q1" 桶污染猜想 | 提取纯文本，标题 "Annual Audited Consolidated Financial Statements"，正文 "as of December 31, 2008"，确认是 FY2008 年度报表被误标 |
| 11 | `data/raw/AEM/2008-Q2_0001047469-08-009549_a2187529z6-k.htm`、`2008-Q3_..._a2188564z6-k.htm` | 验证 2008 Q2/Q3 是否真缺数据 | 提取纯文本，长度仅 1,938–1,940 字符，纯 6-K 封面无正文实质内容，确认无真实财报 |
| 12 | `data/raw/KGC/2006-Q1_0001047469-06-004477_a2169058zex-99_1.htm` | 验证 KGC 2005 年度数据是否可从 2006 年报补回 | 检索 "for the year ended"，命中 "DECEMBER 31, 2005"，确认可用 |
| 13 | `data/raw/GOLD/2006-Q1_0000909567-06-000713_o31437exv99w1.htm` | Barrick-Placer Dome 收购完成月份 | 检索 "completed the acquisition"，命中 "In March 2006, Barrick completed the acquisition, and Placer Dome became a wholly-owned subsidiary" |
| 14 | `data/raw/AU/*.htm`（2004–2012，抽样） | AngloGold 对冲账簿平仓时间窗 | 关键词计数 "closed out"/"eliminat…hedge" 类短语，2010/2011 年命中 11/10 次，远高于 2007–2009 的 0–3 次，确认平仓集中在 2010–2011 |
| 15 | `data/raw/KGC/*.htm`（2006–2010，抽样） | Kinross 三笔并购时间点 | 关键词计数 "Bema Gold"（2006–2010 递减）、"Red Back Mining"（仅 2010 年 48 份）、"Underworld Resources"（2008–2010 递增），与公开收购史吻合 |
| 16 | `data/raw/NEM/2005-Q1_0001193125-05-090450_d10q.htm` | NEM 锚点科目最早出现 | 检索 "Costs applicable to sales"，命中 "(exclusive of depreciation, depletion and amortization)"，确认 2005-Q1 即已使用此后延续多年的措辞 |
| 17 | `data/raw/GOLD/2012-Q4_0001193125-13-062690_d482590dex991.htm`、`data/raw/KGC/2012-Q4_0000701818-13-000002_ex99-1.htm` | 交叉验证 AISC-cash 早期采用（复核 `docs/SEC_COVERAGE.md` 已更正的结论） | 检索 "all-in sustaining"，Barrick 命中 "$972 per…"/FY2012 "$945"，Kinross 命中 "independently reporting an all-in sustaining cost"，均确认 2012-Q4 首现，与既有文档结论一致 |


---

## 勘误（2005–2012 提取轮，原文复核后）

**GFI 的频率判定错了，而且错得对下游有实际影响。**

本文件第 1 节和 §4.3 称 Gold Fields「8 年 32 个季度里只有 12 个季度有完整财务报表」。提取
agent 逐份打开全部 32 个季度的申报后报告与此不符，主代理回原文复核，确认 **agent 是对的**：

- `2007-Q3_0001205613-07-000137_goldfields_quarter….htm` —— 108KB，利润表 / 资产负债表 /
  现金流量表齐全，封面逐字 "quarter ended 30 September 2007"。同一季度另外两份 6-K
  （`…_goldfields_sale`、`…_goldfields_sell`）是 6KB 级的 SENS 处置公告。
- `2009-Q1_0001205613-09-000046_gf_q3.htm` —— 利润表列头为 "Quarter | March 2009 |
  December 2008 | March 2008 | Nine months to March 2009 | March 2008"，**确有离散季度列**。
  同一份文件同时印南非兰特表和 "UNITED STATES DOLLARS" 表，所以美元数字无需任何外部汇率源
  （已逐项核对 2009Q1：Revenue 868.5 / Operating costs, net 453.0 / A&D 115.4 /
  Net interest paid 16.5，与提取值一致）。

**错因，值得单独记下来，因为它不是 GFI 独有的**：本文件的网格用 manifest 的 `doc_role`
关键词分类判定「该季度有无真财报」。GFI 每季提交多份 6-K，其中绝大多数是 SENS 公告、
真正的季报只有一份；按份数投票，季报被公告淹没。**任何「一个季度提交十几份 6-K」的
申报人都可能被同样误判。** 第 2 节声明过 PDF 未纳入正则扫描，但没有声明这一条。

**影响**：主代理据此下达的提取指令里写着「GFI 是唯一真正意义上的半年报公司……半年数据记为
2010H1/2010H2，永远不要拆成两个季度」。agent 拒绝了这个前提并上报，而不是照做。**若它照做，
GFI 2005–2012 会被压成 16 个半年行、损失一半时间分辨率，而且下游没有任何检查会发现——
因为半年行本来就是这个面板的合法频率。**

（GFI 在 2016 年之后才真正转为半年报，与 2005–2012 是季度报并不矛盾：`GFI_mixed.csv` 里
2013–2015 是 12 个季度行，半年行从 2016H1 才开始。）

**六月制财年的结论不变，仍然成立**：季度列本身是日历季度，六月制财年只影响累计列与年度
审计数；过渡期 20-F 封面逐字 "For the transition period from July 1, 2010 to December 31,
2010"，KPMG 审计意见覆盖 "the six-month period ended December 31, 2010"。


## 勘误二：Barrick 2011 年前是 US GAAP，不是加拿大 GAAP

第 1 节把两家用 40-F 的加拿大申报人一并写成「FY2011 从加拿大 GAAP 切到 IFRS」。**对 Kinross 成立，
对 Barrick 不成立。** 逐份计数：

| 文件 | "US GAAP" 类表述 | "Canadian GAAP" 类表述 |
|---|---|---|
| `GOLD/2007-Q1_0000909567-07-000657_o36103exv99w1.htm` | 18 | **0** |
| `GOLD/2007-Q2_0000909567-07-001011_o37244exv99w1.htm` | 27 | **0** |
| `GOLD/2007-Q3_0000909567-07-001337_o38247exv99w1.htm` | 26 | **0** |
| `KGC/2007-Q1_0001047469-07-004316_a2177983zex-99_1.htm` | 0 | 1 |

Barrick 每份季报封面逐字写着 **"Based on US GAAP and expressed in US dollars"**。它作为大型美国上市
申报人走 MJDS 通道、直接用 US GAAP，与 Kinross 不同。**断裂的年份（FY2011 起转 IFRS）两家都对，
错的只是 2011 年之前那一侧的口径名。**

两家的提取 agent 各自独立按原文记录（GOLD 24 行 `US_GAAP` / 8 行 `IFRS`；KGC 21 行 `CDN_GAAP` /
8 行 `IFRS`），都没有照抄这份文档的说法。

**本文件在这一轮里被推翻的第三条**（前两条：GFI 的报告频率、AU 的季度完整性），加上
`PRE2013_ANCHORS.md` 被推翻的两条（AEM 售出盎司、AU 的 `cash_tax_paid` 覆盖），共五条。
共同的形态是：**用元数据或正则普查代替读原文，得出一个看起来具体、实际没被任何一份申报证实的结论**，
然后这个结论被写进下一轮的指令里当作前提。
