# L1-academic：学术与榜单线深度验证（截止 2026-08-20）

## 执行路径
- CIDR'26/PVLDB v19n5《Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards》：https://arxiv.org/abs/2601.08778 ｜ CIDR 版 https://www.vldb.org/cidrdb/2026/text-to-sql-benchmarks-are-broken-an-in-depth-analysis-of-annotation-errors.html ｜ DOI https://doi.org/10.14778/3796195.3796206
- BIRD 官方榜（curl 抓原始 HTML 自行解析表格，非二手转述）：https://bird-bench.github.io/ — 含 Overall 榜、Oracle Knowledge 列、News 区、Submission 区
- Spider 2.0 官方榜（同样自行解析 HTML，共 133 行表格）：https://spider2-sql.github.io/ — Snow/Lite/DBT 三赛道 + News 区披露"已公开全部 gold answer"
- BIRD-CRITIC 官方榜（自行解析，确认数据陈旧）：https://bird-critic.github.io/
- BIRD-Interact 官方站 + 论文：https://bird-interact.github.io/ ｜ https://arxiv.org/abs/2510.05318
- LiveSQLBench 官方榜：https://livesqlbench.ai/
- DABstep：**未用二手数据**，直接下载官方 HF 后端数据集 task_scores(985,050 行)+submissions 元数据(2,179 条提交)，用 DuckDB 复算 validated/unvalidated 双榜 — https://huggingface.co/datasets/adyen/DABstep ｜ 榜单 https://huggingface.co/spaces/adyen/DABstep ｜ 论文 https://arxiv.org/abs/2506.23719
- 复算结果与 NVIDIA 官方博客数字逐位吻合（89.95/87.57/45.24），交叉验证方法无误：https://huggingface.co/blog/nvidia/nemo-agent-toolkit-data-explorer-dabstep-1st-place
- 分级框架双源：https://arxiv.org/abs/2510.23587（Survey，L0–L5 定义表）｜ https://arxiv.org/pdf/2602.04261（SIGMOD'26 Tutorial）
- 方法谱系：Arctic-Text2SQL-R1 https://arxiv.org/abs/2505.20315 ｜ Reasoning-SQL https://arxiv.org/abs/2503.23157 ｜ Agentar-Scale-SQL https://arxiv.org/abs/2509.24403 ｜ DeepEye-SQL https://arxiv.org/abs/2510.17586 ｜ SLM-SQL https://arxiv.org/abs/2507.22478
- Data Agent 侧：DeepAnalyze https://arxiv.org/abs/2510.16872 ｜ DS-STAR https://research.google/blog/ds-star-a-state-of-the-art-versatile-data-science-agent/ ｜ DeepEye 系统 https://arxiv.org/html/2603.28889 ｜ FDABench https://arxiv.org/abs/2509.02473 ｜ DAComp https://arxiv.org/pdf/2512.04324 ｜ MMTU https://github.com/MMTU-Benchmark/MMTU ｜ DAB https://ucbepic.github.io/DataAgentBench/
- 真实企业场景：EntSQL https://arxiv.org/abs/2606.03363 ｜ Spider2.0-AIFunc https://arxiv.org/abs/2607.06229 ｜ Tribal Knowledge https://arxiv.org/pdf/2602.13521 ｜ Text-to-Big SQL https://arxiv.org/pdf/2602.21480

## 剔除
- BEAVER | 核心论文 arXiv:2409.02038 为 2024-09，官网 leaderboard 未渲染出任何分数，无 2025+ 可核实证据。
- DAB (UC Berkeley EPIC) | 仅 54 条 query，且 2026-06-12 更新后榜单页无任何条目，规模与数据都不足以支撑结论。
- Papers with Code / BenchLM.ai 类聚合榜 | 二手转录、覆盖稀疏（Spider2-Lite 仅收录 1 个模型），不作为 SOTA 依据。
- InfiAgent-DABench / DA-Code / TAG-Bench / AutoKaggle | 均为 2024 年发起，2025+ 只有被引用没有实质更新。
- MCTS-SQL / Alpha-SQL / R3-SQL / AGRO-SQL / MTIR-SQL / MARS-SQL / FINER-SQL / SQLConductor / EvolSQL / DecoSearch / LinkAlign / AgentNLQ | 同属"L1 单句 SQL + 搜索或 RL 变体"，方法论已被 Arctic/Reasoning-SQL/Agentar 三条主线覆盖，边际信息量低，不逐一深读。
- NL2SQLBench / LogicCat / TACO / DP-Bench / BADGER / DataGovBench / LongDA / DSGym / TableVista / TABVERSE / MBABench / InsightEval / UniDataBench / AiDABench / DSAEval / ReasonTabQA | 2025-2026 基准发布过密且互相高度重叠，均无活跃第三方榜单，只作为"评测碎片化"的证据统计，不单独下结论。
- 两篇 Data Science Agent 综述（2508.02744 / 2510.04023）| 与 2510.23587 的 L0–L5 框架重复且分级更粗。
- Next-Gen DB Interfaces / TKDE 综述 | 主体内容成文于 2024，2025 修订未改变结论。

## 结论

### 一、基准可信度裁定：**先打折，再看分**

**1.1 指控是实锤，且已进入顶会/顶刊双通道。** Jin/Choi/Zhu/Kang（UIUC）的工作同时以 CIDR'26 和 PVLDB Vol.19 No.5 发表，专家复核给出的标注错误率是：**BIRD Mini-Dev 52.8%、Spider 2.0-Snow 62.8%（CIDR 版记 66.1%）**。错误定义包含"gold SQL 本身写错"与"问题本身有歧义（多个合理 SQL）"两类，不是纯粹的口径之争。（https://arxiv.org/abs/2601.08778 ｜ https://doi.org/10.14778/3796195.3796206）

**1.2 影响面：排名会被打乱，但不是全盘推翻。** 重测 BIRD 榜上 16 个开源 agent，相对分数变动 **-7% ~ +31%**，名次变动 **-9 ~ +9 位**；关键统计是——未修正子集与全集的排名相关性 r=0.85，**修正后掉到 r=0.32**。这句话的实际含义是：**BIRD 榜 Top-10 内部的名次差（80.83 vs 81.67 vs 81.95）在统计上没有意义**，但"81% 档 vs 60% 档"的量级差异仍然可信。（同上）

**1.3 BIRD 官方已经认账并动手了 —— 这一点是我认为最重要的裁定依据。** BIRD 官网 News 2025-11-13"Major Updates"明确写：已完成全面质量管控，发布**更干净的开发集 `bird-sql-dev-1106`**；新提交须标注使用该 split（榜上即 `New Dev` 标记，如 Claude Opus 4.6 Baseline New Dev 68.77/70.15，2026-02-21）；并预告"**移除 Oracle Evidence，改开交互式赛道**"。此前 2025-05-25 也公告过"最后一次清洗 dev(1534)"。（https://bird-bench.github.io/）

**1.4 因此，各榜的可信度分层（这是我给出的核心裁定）：**

| 榜单 | 可信度 | 理由 |
|---|---|---|
| BIRD Overall (test) | **中等偏可信，但只看量级** | test 标签不公开，须发 `bird.bench23@gmail.com` 由组织方评测（约 10 天返回），非自报；但受 1.1 标注错误影响，Top-10 内名次不可信 |
| BIRD `New Dev` 标记条目 | **较可信** | 跑在清洗后的 dev-1106 上；但**与旧 Dev 分数不可直接比较** |
| Spider 2.0-Snow | **应大幅打折** | 见 1.5 |
| Spider 2.0-Lite / DBT | 中等 | 同为公开 gold，但分数未饱和，仍有区分度 |
| BIRD-CRITIC | **数据陈旧，不可作为当前 SOTA** | 见 1.6 |
| LiveSQLBench | **设计上最抗污染** | 隐藏测试集轮换为下一版开发集 + 业务规则漂移 |
| BIRD-Interact | **可信且最有信息量** | 分数极低、无饱和空间 |
| DABstep | **必须区分 validated / unvalidated** | 见三章，差别是天壤 |

**1.5 Spider 2.0-Snow 已经"名义饱和"，我判定它不能再用于评价 SOTA。** 官网 News 2024-12-24 明写"**决定公开全部样例与 gold answer 供自评**"，2025-01-07 另行警告"**不建议拿我们发布的 Gold SQL 做 SFT，会影响评测公平性**"，2025-04-20 还提供了 oracle ground-truth tables。在 gold 全公开 + 标注错误率 62.8% 的双重条件下，当前 Snow 榜首 **Genloop Sentinel Agent v2 Pro 96.70**、Native mini 96.53、QUVI-3+Gemini-3-pro 94.15 —— 拿到 96.7% 意味着**连那 62.8% 的错误 gold 也一并"答对"了**，这只能解释为对公开答案的过拟合，而非能力。**强证据**：同样 547 题的 Spider2.0-Lite 榜首只有 **76.23**（Tianqiong Data Agent + GLM 5.2），DBT 榜首仅 **65.6**。20 分的裂口就是可信度的裂口。（https://spider2-sql.github.io/）

**1.6 BIRD-CRITIC 公开榜实际上是"冻结"的。** 我解析原始 HTML 确认：1.0-Open 榜首仍是 **o1-preview 35.5%**，第 2 deepseek-r1 32.0%，第 3 gpt-4o 27.5%，**全部条目日期停在 2025-04-20**（个别 2024-11）。到 2026-08 这已是 16 个月前的快照，**它反映的是"当时测过什么模型"，不是今天的 SQL 调试能力上限**。人类基线 78.87%。任何引用"SWE-SQL SOTA 仅 35%"的说法都必须加这个时间戳。（https://bird-critic.github.io/）

### 二、逐榜当前 SOTA（均为一手核实）

**BIRD Overall（test EX，全部 Oracle Knowledge=✔️）** — https://bird-bench.github.io/
| 日期 | 方法 | Dev | Test |
|---|---|---|---|
| 2025-12-16 | AskData + GPT-4o (AT&T CDO) | 77.64 | **81.95** |
| 2025-09-25 | Agentar-Scale-SQL (蚂蚁) | 74.90 | 81.67 |
| 2026-06-19 | Sber Text2SQL | 75.74 | 81.33 |
| 2026-05-27 | Xiaomi Text2SQL | 73.66 | 80.83 |
| 2026-08-19 | RAS (Adya AI) | 72.49 | 79.82 |
| 2026-07-14 | DeepEye (HKUST-GZ) | 74.49 | 79.09 |
| 2026-07-10 | DeepEye-SQL (27B) | 74.49 | 78.42 |

三个必须同时说出口的限定：(a) 人类基线 **92.96**，差距仍有 11 分；(b) 榜首全部依赖 **Oracle Knowledge（人工标注的 evidence 提示）**，BIRD 官方自己已宣布要移除它 —— 这意味着**当前 81% 是"给了答案线索"的成绩**；(c) 2025-12 至 2026-08 共 8 个月，榜首从 81.95 只挪到 81.67/81.33，**BIRD 事实上已停止提供区分度**。能力层级：**L1**。

**Spider 2.0** — Snow **96.70**（已饱和，见 1.5，不采信）／Lite **76.23**／DBT **65.6**。参照系：原论文中 o1-preview 仅 17.1%、GPT-4o 10.1%（对比 Spider 1.0 的 86.6%）。Spider2 需要跨 BigQuery/Snowflake、>3000 列、常超 100 行 SQL，任务形态本身是 **L2**（多步 + 环境交互），DBT 赛道涉及仓库级建模，触及 **L5** 边缘。

**BIRD-Interact** — 这是我认为**信息量最大的一个榜**。600 题（full）/300 题（lite），双模式：c-Interact（被动对话，流程固定）与 a-Interact（模型主导的主动交互）。论文报告 **GPT-5 在 full 上 c-Interact 仅 8.67%、a-Interact 17.00%**；官网记 full 最佳 **16.33%**，lite 约 24%/18%。仅 Claude-3.7-Sonnet 表现出"Interaction-Time Scaling law"（多轮越交互越好）。能力层级：任务是 **L2→L3**，而模型实际达成率不足 1/5。（https://arxiv.org/abs/2510.05318 ｜ https://bird-interact.github.io/）

**LiveSQLBench** — 榜首 **DIA (Data Intelligence Agents) 48.00%**（2026-05-29），其后 MiniMax M3 (Claude Code) 40.17、Claude Opus 4.6 (OpenHands CLI) 38.00、Gemini 3.1 Pro 36.50。覆盖 CRUD 而非仅 SELECT，配分层知识库（HKB）需多跳推理。**在抗污染设计下 SOTA 只有 48%，这个数字比 BIRD 的 81% 更接近真实能力**。能力层级：**L2**（含 L5 的 CRUD/DDL 雏形）。（https://livesqlbench.ai/）

**BIRD-CRITIC** — 见 1.6，o1-preview 35.5%（2025-04 快照），人类 78.87%。任务本质是"修 SQL 缺陷"，**L2**。

**Data Agent 类新基准（全部指向同一结论：任务越像真实分析，分数越低）**
- **DABstep**（Adyen×HF，450+ 题金融多步分析，answer key 隐藏）：见第三章，**L3**。
- **MMTU**（NeurIPS'25 D&B，28,136 题/25 类表任务/52 数据集）：GPT-5 **0.696**、o3 0.691、Gemini-2.5-Pro 0.665；非推理模型 GPT-4o 仅 0.507。**L2**（表理解+推理+编码，非 SQL 单点）。（https://github.com/MMTU-Benchmark/MMTU）
- **FDABench**（KDD'26，2,007 题，跨 DB/文档/网页/图像/视频/音频 6 模态）：**L3**，是目前唯一系统性覆盖"异构源联合分析"的基准。（https://arxiv.org/abs/2509.02473）
- **DAComp**（2025-12，ByteDance 等）：覆盖采集→探索→处理→分析→建模全生命周期，明确指出现有 agent 在"跨阶段推理"和"解空间未枚举"上崩塌。**L4–L5**。（https://arxiv.org/pdf/2512.04324）
- **EntSQL**（2026-06，1,066 中英对照题，5 个业务域，需从长文档中 grounding 私域业务知识）：**最佳系统仅 15.9%**。这个数字应当被当作"企业落地真实难度"的锚点 —— 它和 BIRD 的 81.95% 是同一件事的两个极端。**L1 任务 + L5 前提（业务知识/语义层）**。（https://arxiv.org/abs/2606.03363）
- **Spider2.0-AIFunc**（2026-07，465 题/125 库，把 LLM 能力作为 SQL 原生函数：分类/过滤/情感/抽取/相似检索/聚合）：闭源模型 67–70%，最佳开源 58.1%。这是"SQL 与 LLM 融合"的新战场。**L3**。（https://arxiv.org/abs/2607.06229）

### 三、DABstep 深挖：我一手复算出的双榜，结论与外界流传的完全不同

我下载官方后端数据集（985,050 条 task_scores + 2,179 条提交元数据）用 DuckDB 复算，得到三个别处看不到的事实：

**3.1 只有 28/2,179 条提交是 validated（1.3%）。** 其余 2,150 条属于 Unvalidated tab。在未验证池里，**39 条声称 hard ≥95%，其中 16 条声称 hard = 100.0%**，包括名字直接叫 `Think Evolve Labs LLC - ThinkEvolve Spoofer` 的条目，以及大量 `test-`、`try2`、`_test20` 之类的调试提交。单个用户最高提交 **142 次**（461 个 org 中若干用户提交 100+ 次）—— 在答案隐藏的前提下，这就是**反复提交探测答案**的典型模式。**结论：DABstep 未验证榜单没有任何参考价值，引用 DABstep 必须指明 validated。**

**3.2 validated 榜的真实曲线（hard split，我复算，与 NVIDIA 官方博客逐位吻合）：**
| 日期 | Agent | hard | easy |
|---|---|---|---|
| 2026-02-22 | **NVIDIA KGMON Data Explorer**（Haiku 4.5 推理 / Opus 4.5-4.6 学习） | **89.95** | 87.5 |
| 2025-12-09 | OceanBase DataPilot (Qwen3) | 87.57 | 86.11 |
| 2025-11-04 | gg-agent-gpt5 | 62.96 | 88.89 |
| 2025-09-19 | CambioML energent.ai DS Agent (GPT-5) | 57.67 | 94.44 |
| 2025-07-08 | **DS-STAR** (Google, Gemini-2.5-Pro) | 45.24 | 87.5 |
| 2025-08-03 | AgenticData (清华, Qwen3) | 40.48 | 94.44 |
| 2025-05-28 | Claude 4 Sonnet ReACT baseline | 19.84 | 81.94 |
| 2025-02-02 | o3-mini baseline | 13.76 | 72.22 |
| 2025-01-23 | Claude 3.5 Sonnet ReACT baseline | 9.26 | 77.78 |

**这是本次调研里唯一一条"真实且剧烈"的进步曲线：13 个月内 hard 从 ~9–14% 涨到 89.95%。** 且驱动力不是底座模型变强 —— 榜首推理阶段用的是 **Claude Haiku 4.5（小模型）**，比 baseline 快 30 倍（20 秒/题 vs 10 分钟）。（https://huggingface.co/blog/nvidia/nemo-agent-toolkit-data-explorer-dabstep-1st-place）

**3.3 但必须打一个折：**NVIDIA 的方法是"学习阶段用重模型解代表性任务→refactor 成可复用的 `helper.py` 函数库→推理阶段小模型只调函数签名→离线反思把洞察写回 system prompt"。由于 DABstep 是**固定的 450 题**，这本质上是**针对该基准拟合出一套任务专用工具库**。合规（dev split 本就带答案），但 89.95% 是**基准工程分，不是泛化分**。真正可迁移的结论是方法论：**"重模型离线蒸馏出工具 → 小模型在线调用"这条路线在 L3 数据分析上被验证有效**。

**3.4 顺手纠一个正在流传的错误引用：**外部报道称"Energent.ai 在 DABstep 达到 94.4%，超过 Google 的 88% 和 OpenAI 的 76%"。对照我复算的 validated 数据：CambioML/energent.ai 的 **94.44 是 easy split**，其 hard 只有 **57.67**；"Google 88%" 对应 DS-STAR 的 **easy 87.5**（DS-STAR 自己的博客诚实地引用 hard 45.2%）。**厂商宣传普遍拿 easy 冒充总分 —— 这是本线索里必须写进最终报告的一条卫生规则。**（对照 https://research.google/blog/ds-star-a-state-of-the-art-versatile-data-science-agent/）

### 四、方法谱系与能力层级

**RL / 执行反馈（L1，效率路线）**
- **Arctic-Text2SQL-R1**（Snowflake，2025-05，2026-01 修订）：核心主张是"**只用执行正确性做奖励**，不做中间监督、不做奖励塑形"，配强 SFT 初始化 + 数据筛选；**7B 打赢此前 70B 级系统**，6 个基准 SOTA 并登顶过 BIRD。→ 这条线的价值是**成本**，不是天花板。（https://arxiv.org/abs/2505.20315）
- **Reasoning-SQL**（Pourreza/Talaei/Mirhoseini/Arik 等，2025-03）：反向主张 —— 用 4 类**部分奖励**（schema-linking、AI feedback、n-gram 相似、语法检查）+ GRPO 缓解奖励稀疏；14B 在 BIRD 上超 o3-mini 4 分、超 Gemini-1.5-Pro-002 3 分。（https://arxiv.org/abs/2503.23157）
- **判断**：两者结论相反（简单奖励 vs 部分奖励），且都只在 BIRD/Spider 上验证 —— 结合第一章，**这类 1–4 分的差距正落在标注噪声区间内，不足以裁定路线优劣**。

**Test-time scaling（L1–L2，堆算力路线）**
- **Agentar-Scale-SQL**（蚂蚁，2025-09/2025-12 v6）：三维编排式扩展 = 内部扩展（RL 强化内在推理）+ 顺序扩展（迭代精修）+ 并行扩展（多样化合成 + 锦标赛选择），BIRD test **81.67**。（https://arxiv.org/abs/2509.24403）
- **ReFoRCE**（Hao AI Lab × Snowflake）：自纠错 + 格式约束 + 列探索，曾登顶 Spider2；当前 Snow 榜 **62.89（+o3）**，已被大量新 agent 超过。（https://spider2-sql.github.io/）
- **判断**：test-time scaling 确实有效但**边际收益已尽** —— BIRD 榜 8 个月内只前进 0 分即是证据。

**Multi-agent / 软件工程范式自纠错（L2，工程化路线，我认为是最有实操价值的一支）**
- **DeepEye-SQL**（HKUST-GZ × 华为云，SIGMOD'26，arXiv 2025-10）：把 text-to-SQL 当**软件工程流程**做 —— schema linking 强制关系闭包（grounding）→ **N-version SQL 生成**容错 → "Syntax-Logic-Quality" 确定性工具链在执行前拦截错误 → 置信度感知 + 执行引导裁决（而非简单多数投票）。**用 ~30B total/~3B activated 的开源 MoE、完全不微调**，达到 BIRD-Dev 73.5 / BIRD-Test 75.07（当前榜上该条目已到 78.42）/ Spider-Test 89.8。（https://arxiv.org/abs/2510.17586）
- **判断**：这是把"L1 能力"用工程手段推到"L2 可靠性"的最佳范本，且对小模型友好，**是最容易迁移进生产系统的一条**。

**小模型路线（L1）**
- **SLM-SQL**（2025-07）：0.5B–1.5B，SFT（SynSQL-Think-916K）+ RL（SynSQL-Merge-Think-310K）+ 推理期纠错式自洽；**1.5B 达 BIRD-Dev 67.08，0.5B 达 56.87**，5 个模型平均提升 31.4 分。（https://arxiv.org/abs/2507.22478）
- 榜上佐证：`xorazm-text2sql-0.8b`（0.8B）BIRD test **59.59**；Struct-SQL（4B）60.42。**参照 DeepSeek-R1 Baseline 的 New Dev 60.93 —— 0.8B 已接近旗舰推理模型的裸模型水平。**（https://bird-bench.github.io/）
- **判断**：单句 SQL 已被小模型基本吃下，**继续在 L1 上投入的 ROI 已经很低**。

### 五、重点：谁真正跨出了 L2–L5，边界在哪

**5.1 分级框架本身已经有权威版本，且两版结论一致：现状是 "Proto-L3"。**
《A Survey of Data Agents: Emerging Paradigm or Overstated Hype?》（2025-10，HKUSTDial，仿 SAE J3016）给出 L0–L5 定义表：**L0** 全人工；**L1** 无状态的查询响应助手；**L2** 具备环境感知与交互，但**流水线仍由人编排**；**L3** 在监督下**自主编排**面向多样任务的数据流水线；**L4** **主动发现**值得调查的问题并无监督地编排流水线；**L5** 发明新方法、独立推进 SOTA。系统归位：**L1** = DIN-SQL / Chat2VIS / DB-GPT / LLMTune；**L2** = CHASE-SQL / AutoPrep / DataVoyager / MatPlotAgent / QUITE；**Proto-L3** = Data Interpreter / iDataLake / **DeepAnalyze** / BigQuery。（https://arxiv.org/abs/2510.23587 ｜ 同组 SIGMOD'26 Tutorial https://arxiv.org/pdf/2602.04261 结论一致）

**该综述判定"卡在 L2→L3"的三条具体理由（这是全篇最有价值的判断）：**(a) **任务范围窄** —— 绝大多数系统只做"分析"，不覆盖 management/preparation 全生命周期；(b) **自治不完整** —— 仍依赖人定义的组件与流程，或依赖已预处理好的数据，无法端到端接管原始异构数据；(c) **无法处理未预定义算子** —— 真 L3 要能应对没见过的场景、发现并调用新能力，现有系统只会调预置工具。**共性诊断：战术能力强，缺战略性高阶推理。**

**5.2 逐个系统的能力边界实测（对照本次任务的 L1–L5 口径）**

| 系统 | 声称 | 我判定的实际层级 | 边界证据 |
|---|---|---|---|
| **DeepAnalyze**（人大 RUC-DataLab，8B，2025-10） | 端到端出"分析师级深度研究报告" | **L3，Proto** | 课程式 agentic 训练 + 数据接地的轨迹合成；8B 胜过基于最强闭源模型的 workflow agent。**但**被 2510.23587 明确归入 Proto-L3；其论文自陈痛点是"依赖预定义 workflow"，而其自身是否已摆脱仍无第三方基准佐证。https://arxiv.org/abs/2510.16872 |
| **DS-STAR**（Google Cloud AI Research，2025-11） | versatile data science agent | **L3（已证）** | Analyzer/Planner/Coder/Verifier/Router 五角色迭代，最多 10 轮；DABstep hard **45.24**（我复算确认）、KramaBench 44.7、DA-Code 38.5。**边界：45% 意味着一半以上真实多步分析仍失败。** |
| **NVIDIA KGMON Data Explorer**（2026-02） | DABstep 第一 | **L3（最强，但含基准拟合）** | hard **89.95**；机制是"重模型离线生成可复用工具库 → 小模型在线单遍调用 → 离线反思回注 prompt"。**边界：工具库是针对固定 450 题拟合的，换域需重跑学习阶段。** |
| **DeepEye 系统**（HKUST-GZ，SIGMOD'26 Companion，2026-03） | steerable self-driving data agent | **L3 上限，L4 未达** | 统一节点协议（确定性 ToolNode + 概率性 AgentNode）、记忆增强 Planner 生成 DAG、数据库式的编译/校验/优化/执行四阶段、云原生沙箱；产出 Data Video/Dashboard/报告。**边界（关键）：论文只有 demo 场景，没有定量基准结果；且 "steerable" 的定义就是"人可以手改 workflow"——即官方承认需要 human-in-the-loop，正是 L3"监督下"而非 L4。** https://arxiv.org/html/2603.28889 |
| **BIRD-Interact 范式** | 交互式评测 | 定义了 **L2→L3 的正确考法** | a-Interact（模型主动澄清/检索知识/错误恢复）是目前最贴近真实分析对话的评测设计。**边界残酷：GPT-5 仅 17.00%。** 这说明**主动交互能力是当前最大短板**，而它恰是 L3 归因分析的前置条件。 |
| **DAComp / FDABench / DAB** | 全生命周期 / 异构源 / 多库 | 面向 **L4–L5** 的考题，尚无强解 | DAComp 明指 agent 在跨阶段推理与非枚举解空间上失效；FDABench 六模态 2,007 题；DAB 仅 54 题且榜单空白。**共同信号：L4/L5 目前只有考题、没有答卷。** |

**5.3 L5（数据建设/治理/语义层）：唯一实质性进展是"部落知识"这条线。**
UC Berkeley（Agarwal, Biswal, Zeighami, Cheung, Gonzalez, Parameswaran）《Arming Data Agents with Tribal Knowledge》（2026-02）把问题定义为：企业里真正决定 SQL 正确与否的，是**未成文的业务逻辑、指标口径、schema 语义约定**；论文将这些隐性知识结构化并注入 agent，实证能显著改善歧义查询的解释。这与 EntSQL 的 15.9%、LiveSQLBench 的分层知识库（HKB）、BIRD 的 Oracle Evidence 是**同一个问题的三种表述** —— **模型能力不是瓶颈，语义层/指标层的缺失才是**。（https://arxiv.org/pdf/2602.13521 ｜ https://arxiv.org/abs/2606.03363）

**5.4 两个被普遍忽略、但对 Data Agent 定位很关键的补充维度：**
- **成本/效率维度完全缺席。**《Both Ends Count! Just How Good are LLM Agents at Text-to-Big SQL?》（Universitat Rovira i Virgili，2026-04）指出：在 Athena/BigQuery/Spark SQL 上，agent 能生成**正确但极其昂贵**的查询，现有评测全部只看正确性。对真实数仓场景，这是致命盲区。（https://arxiv.org/pdf/2602.21480）
- **SQL 与 LLM 正在融合成新原语。** Spider2.0-AIFunc 把分类/情感/抽取/相似检索做成 SQL 原生 AI 函数（Snowflake 6 类），闭源 67–70%/最佳开源 58.1%。**这意味着未来 "Data Agent 写的 SQL" 本身就内嵌 LLM 调用，L1 与 L3 的边界会消失。**（https://arxiv.org/abs/2607.06229）

### 六、给最终报告的六条硬结论
1. **不要引用任何单一 text-to-SQL 榜单排名**；BIRD Top-10 名次差已被证明落在标注噪声内（修正后排名相关性 r=0.32）。要引用就引用**量级**和**是否用 Oracle Knowledge**。
2. **Spider 2.0-Snow 的 96.7% 与 DABstep 未验证榜的 100% 都不可采信**；前者 gold 全公开且标注错误率 62.8%，后者 2,150/2,179 条提交未验证、16 条自称满分。
3. **看真实能力请看四个数**：BIRD-Interact full **16.33%**（交互）、EntSQL **15.9%**（企业私域知识）、LiveSQLBench **48%**（抗污染）、DABstep validated hard **89.95%**（多步分析，含基准拟合）。
4. **L1 已解决**：0.8B 模型 BIRD test 59.59、1.5B Dev 67.08、27B 免微调 Test 78.42 —— 单句 SQL 不应再是投入重点。
5. **L2 已工程化**：DeepEye-SQL 的"N-version 生成 + 确定性校验工具链 + 执行引导裁决"是可直接搬进生产的范式。
6. **L3 刚起步、L4–L5 仅有考题**：权威分级（2510.23587 / 2602.04261）判定业界统一停在 **Proto-L3**，缺的是全生命周期覆盖、未预定义算子处理、主动问题发现；而**语义层/指标层（tribal knowledge）而非模型能力，才是 L5 的真正瓶颈**。
