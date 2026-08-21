# L2-opensource：开源项目线深度验证（截至 2026-08-20）

## 执行路径

- GitHub API（`search_repositories` 全量字段）逐仓核实 `pushed_at`/`archived`/`license`/`stargazers_count`，共核实 34 个仓库；**关键点：阶段 1 多处把 `updated_at`（star/issue 活动）误当成代码更新**，本文一律用 `pushed_at`（真实代码推送）+ 默认分支 commit 页交叉验证
- https://github.com/Canner/WrenAI + /commits/main + /releases —— 确认 main 分支 2026-07-30~08-20 连续 commit；2026-08 内 5 次组件发版
- https://github.com/sinaptik-ai/pandas-ai/commits/main —— 确认最新 commit 为 2025-10-28 "fix: remove deprecated method from documentation (#1842)"
- https://github.com/vanna-ai/vanna —— 归档横幅原文 "This repository was archived by the owner on Mar 29, 2026. It is now read-only."
- https://github.com/vanna-ai/vanna/releases/tag/v2.0.2 —— 渲染为 "02 Feb 14:14"（无年份=当年），与 API `pushed_at=2026-02-02T14:14:20Z` 完全对齐
- https://pypi.org/project/dbgpt/#history —— DB-GPT 权威发版时间轴：0.7.0(2025-03-24)→0.7.3(2025-07-25)→0.7.4(2025-10-24)→0.7.5(2026-02-11)→0.8.0(2026-03-27)→0.8.1(2026-06-18)
- https://github.com/eosphoros-ai/DB-GPT、https://github.com/getnao/nao、https://github.com/agno-agi/dash、https://github.com/zhongyu09/openchatbi、https://github.com/HKUSTDial/DeepEye、https://github.com/FireBird-Technologies/Auto-Analyst、https://github.com/tencentmusic/supersonic、https://github.com/dataease/SQLBot、https://github.com/OpenDCAI/DataFlow —— 逐个读架构判定能力层级
- https://github.com/AltimateAI/altimate-code、https://github.com/dbt-labs/dbt-agent-skills、https://github.com/JetBrains/databao-agent、https://github.com/cube-js/cube —— 候选清单外补充的 L5 线索（均 2026 年新增）
- WebSearch: Vanna 归档去向 / Chat2DB 仓库迁移（CodePhiliaX→OtterMind）/ 2026 开源 agentic analytics 盘点

## 剔除

- `db-agent/db-agent` | 28 star、29 fork，README 自称"生产级"但无任何用户或发版证据，属营销型空壳
- `YASSERRMD/schema-forge` | 8 star 个人实验，无社区
- `eosho/langchain_data_agent` | LangGraph 官方范式的示例工程，不构成独立能力
- `didilili/shopkeeper-agent` | 教程/课程配套项目，非可复用产品
- `OpenDCAI/DataFlow-Agent` | 8 star、2026-06 新建子仓，尚未独立成项目（能力已并入 DataFlow 主仓评估）
- `Snowflake/Arctic-Text2SQL-R1-7B`、`CycloneBoy/slm_sql` | 单篇论文的权重/复现代码，属模型线而非工程项目（slm_sql 37 star，2025-08 后无更新）
- `Awesome-Text2SQL` / `Awesome-LLM-based-Text2SQL` / `NL2SQL_Handbook` / `SJTU-DMTai/Awesome-Data-Agent-Papers` | 是论文清单不是可运行系统，只保留索引价值，不占用"项目"评估位
- `CoRAL-ASU/weaver`、`stym06/kepler`、`itrummer/thalamusdb` | Show HN/会议单点产出，2026 年无持续代码与采用证据
- `langchain-ai/deepagents`（28k star，2026-08-20 活跃）| 通用 agent harness，text-to-SQL 仅是 examples 目录，列为对照组而非 Data Agent 项目
- `zjunlp/DataMind` 之外的 ICLR/AAAI 配套仓 | 未见可独立部署形态，不重复列举

---

## 结论

### 一、总纲判断：开源侧 90% 的"热度"停在 L1/L2，真正 L3+ 的项目不到十个

阶段 1 清单里 star 数最高的四个项目——Chat2DB(28.0k)、Vanna(23.8k)、pandas-ai(23.8k)、DB-GPT(19.8k)——其中**两个已实质死亡**（Vanna 归档、pandas-ai 停更 10 个月）。star 数与"能不能用"几乎不相关，必须以 `pushed_at` 为准。

**能力层级定义对照**：L1 单句 text-to-SQL；L2 多步查询/自纠错；L3 分析与归因；L4 规划与主动分析；L5 数据建设与治理（建模/数仓/指标层）。

---

### 二、生产可用（代码活跃 + 有真实发行/部署证据）

| 项目 | star | 最近代码 push | 许可证 | 层级 | 定位一句话 |
|---|---|---|---|---|---|
| [eosphoros-ai/DB-GPT](https://github.com/eosphoros-ai/DB-GPT) | 19,772 | **2026-08-21** | MIT | **L3**（局部 L4/L5） | AWEL 工作流 + 多智能体 + 沙箱 Python 分析 + 微调，是中文圈唯一同时覆盖查询/分析/建模/微调的成体系开源栈 |
| [Canner/WrenAI](https://github.com/Canner/WrenAI) | 17,341 | **2026-08-20** | 自定义(NOASSERTION) | **L2→L5 语义层** | GenBI：MDL 语义层 + dry-plan 校验的受治理 text-to-SQL + 浏览器端仪表盘 |
| [OtterMind/Chat2DB](https://github.com/OtterMind/Chat2DB) | 27,996 | **2026-08-20** | 自定义 | **L1**(+L2) | 40+ 数据库的客户端/SQL 工作台，AI 只做生成/解释/优化；**注意仓库已从 CodePhiliaX 迁到 OtterMind 组织** |
| [cube-js/cube](https://github.com/cube-js/cube) | 20,672 | 2026-08-21 活跃 | Apache-2.0(后端)/MIT(客户端) | **L5 基础设施** | 开源语义层，2026 年明确加 `agentic-analytics`/`conversational-analytics` topic，为 agent 提供受治理指标口径 |
| [jeecgboot/jimureport](https://github.com/jeecgboot/jimureport) | 8,202 | 2026-08-10 | GPL-3.0 | **L1-L2** | JimuChatBI：一句话生成中文报表/数据大屏 |
| [OpenDCAI/DataFlow](https://github.com/OpenDCAI/DataFlow) | 7,618 | 2026-08-18 | Apache-2.0 | **L5（AI 数据侧）** | LLM 训练数据的算子/pipeline 框架 + DataFlow Agent 自动编排；注意是"给模型造数据"不是"给业务建数仓" |
| [dataease/SQLBot](https://github.com/dataease/SQLBot) | 6,647 | **2026-08-20** | FIT2CLOUD 许可证(GPLv3+署名限制) | **L1-L2** | 飞致云出品中文智能问数，月度发版（最新 v1.10.0），可被 Dify/n8n/MaxKB/DataEase 集成；v1.10.0 专门修了 SQL 注入与 prompt 注入 |
| [tencentmusic/supersonic](https://github.com/tencentmusic/supersonic) | 5,021 | 2026-08-03 | 自定义 | **L2 + L5 语义层** | ChatBI + Headless BI 融合，支持指标/维度/标签的语义建模，腾讯音乐内部产品的参考实现 |
| [agno-agi/dash](https://github.com/agno-agi/dash) | 2,249 | 2026-07-10 | Apache-2.0 | **L3**（含 L5 苗头） | 六层上下文自学习 SQL agent；**Analyst + Engineer 双 agent，Engineer 会沉淀可复用数据资产**（如 `dash.monthly_mrr`），是少数把"数据建设"写进 agent 职责的项目；注意它是 template 仓库 |
| [getnao/nao](https://github.com/getnao/nao) | 1,574 | **2026-08-20** | 自定义 | **L3** | YC 系开源分析 agent：nao-core CLI 做上下文工程 + dbt 原生集成 + **自带 agent 评测/单测框架**（开源里罕见） |
| [FalkorDB/QueryWeaver](https://github.com/FalkorDB/QueryWeaver) | 1,068 | **2026-08-20** | AGPL-3.0 | **L1-L2** | 用图数据库承载 schema 语义关系，替代"把 schema 塞满 prompt"；AGPL 对商用是硬约束 |
| [AltimateAI/altimate-code](https://github.com/AltimateAI/altimate-code) | 793 | **2026-08-21** | MIT | **L5** | 2026 新项目：agentic 数据工程 harness，100+ 确定性工具做 dbt manifest 解析、列级血缘、测试生成、跨仓数据比对、FinOps、PII 识别；可挂在 Claude Code/Codex 之下 |
| [FireBird-Technologies/Auto-Analyst](https://github.com/FireBird-Technologies/Auto-Analyst) | 703 | **2026-08-20** | MIT | **L3** | DSPy 多 agent 数据科学平台：planner 路由 + 预处理/统计检验/sklearn 建模/可视化四类 agent，已有托管产品 autoanalyst.ai |
| [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills) | 678 | **2026-08-20** | Apache-2.0 | **L5** | dbt Labs 官方 Agent Skills 集合（2026-01 新建），把数仓建模工作流固化成 agent 可发现的技能 |
| [zhongyu09/openchatbi](https://github.com/zhongyu09/openchatbi) | 626 | 2026-08-15 | MIT | **L3**（研究级） | LangGraph v1 编排：text2sql 子图 + 数据分析子 agent（基于 deepagents）做时序预测、异常检测、**Adtributor 多维下钻归因**；但作者自述归因/异常检测仍在"trending toward production"，单人维护 |

---

### 三、研究参考（论文代码 / 复现用，不建议直接上生产）

| 项目 | star | 最近代码 push | 许可证 | 层级 | 说明 |
|---|---|---|---|---|---|
| [HKUSTDial/DeepEye](https://github.com/HKUSTDial/DeepEye) | 230 | 2026-08-09 | Apache-2.0 | **L4** | **开源里层级最高的一个**：意图分解→分层规划→拓扑调度工作流引擎→数据视频/仪表盘/报告三类产物，含 FastAPI+Celery+React 完整可跑栈与 workflow inspector 人在环干预；SIGMOD Demo 2026，代码 2026-05 释出。星数低但含金量最高 |
| [JetBrains/databao-agent](https://github.com/JetBrains/databao-agent) | 144 | 2026-04-15 | 自定义 | **L3 + L5** | JetBrains 2026 新产品 Databao：context engine 从库/BI/文档自动生成受治理语义上下文，agent 再基于它出 SQL+图表；已加入 Snowflake 牵头的 Open Semantic Interchange。4 个月未推代码，观察中 |
| [pymc-labs/decision-lab](https://github.com/pymc-labs/decision-lab) | 182 | 2026-08 活跃 | Apache-2.0 | **L3-L4** | 带领域约束的自主 agent 工作流 + 并行探索 + 可复现环境，面向"决策"而非"查询" |
| [zjunlp/DataMind](https://github.com/zjunlp/DataMind) | 133 | 2026-07-24 | 无 LICENSE | **L3** | ICLR/AAAI/KDD 2026 系列：数据合成 + DataPRM 过程奖励模型 + LongDS-Bench 长程多轮基准。**无许可证=不可商用** |
| [XGenerationLab/XiYan-SQL](https://github.com/XGenerationLab/XiYan-SQL) | 1,018 | 2026-05-18 | Apache-2.0 | **L1-L2** | 阿里 M-Schema + 多生成器集成框架；框架仓 3 个月未推代码，配套模型仓 [XiYanSQL-QwenCoder](https://github.com/XGenerationLab/XiYanSQL-QwenCoder) 自 2025-09-03 起停更，[xiyan_mcp_server](https://github.com/XGenerationLab/xiyan_mcp_server) 停在 2026-02-11 —— **整条析言开源线 2026 年已明显降速** |
| [antgroup/Agentar-Scale-SQL](https://github.com/antgroup/Agentar-Scale-SQL) | 463 | 2026-05-09 | Apache-2.0 | **L1-L2** | 蚂蚁：test-time scaling 刷 BIRD/Spider 分数，纯打榜取向 |
| [Text2SqlAgent/text2sql-framework](https://github.com/Text2SqlAgent/text2sql-framework) | 154 | 2026-08 活跃 | — | **L2** | 反 RAG 派：只给 LLM 一个 `execute_sql` 工具，让它自己探索 schema、试查询、自纠错。作为"L2 极简基线"很有参考价值 |
| [RUCKBReasoning/OmniSQL](https://github.com/RUCKBReasoning/OmniSQL) | 453 | 2025-09-08 | 无 LICENSE | **L1** | VLDB'25，SynSQL-2.5M 百万级合成数据集是真资产，但代码 11 个月未动 |
| [Snowflake-Labs/ReFoRCE](https://github.com/Snowflake-Labs/ReFoRCE) | 138 | 2025-08-01 | Apache-2.0 | **L2** | 自精炼+格式约束+列探索，Spider 2.0 榜首方案；默认分支是 `o3`，12 个月未更新，属"论文归档态" |

---

### 四、已衰退 / 必须降级标注（archive 或 6 个月以上无代码 commit）

| 项目 | star | 最近代码 push | 停滞时长 | 判定 |
|---|---|---|---|---|
| [vanna-ai/vanna](https://github.com/vanna-ai/vanna) | 23,822 | 2026-02-02 | — | **已归档**：横幅原文 "archived by the owner on Mar 29, 2026, now read-only"。MIT 协议 |
| [sinaptik-ai/pandas-ai](https://github.com/sinaptik-ai/pandas-ai) | 23,759 | **2025-10-28** | ~10 个月 | **讨论热、代码停滞**：main 最后一次 commit 是文档修复，仍停在 3.0.0b 预发布；star/issue 活动持续到 2026-08 造成"活跃"假象 |
| [defog-ai/sqlcoder](https://github.com/defog-ai/sqlcoder) | 4,043 | **2024-05-23** | ~27 个月 | **已死**。阶段 1"仓库至 2026-08 仍有更新"系误读 `updated_at`，实为零代码推进 |
| [Dataherald/dataherald](https://github.com/Dataherald/dataherald) | 3,646 | **2024-07-24** | ~25 个月 | **已死**。阶段 1"2026-08 仍更新"同样是误读，25 个月无任何代码 |
| [apconw/Aix-DB](https://github.com/apconw/Aix-DB) | 2,227 | 2026-06-22 | 2 个月 | 代码尚可，但**仓库无 LICENSE 文件**——企业引入=法律风险，直接降级 |
| [eosphoros-ai/DB-GPT-Hub](https://github.com/eosphoros-ai/DB-GPT-Hub) | 2,006 | 2025-07-02 | ~13.5 个月 | 微调线已停；DB-GPT 主仓仍活跃，微调能力事实上已并入主仓 |
| [tianlan-ltd/Magic-Insight](https://github.com/tianlan-ltd/Magic-Insight) | 545 | **2024-11-06** | ~21 个月 | 已死，AGPL-3.0 |
| [wbbeyourself/MAC-SQL](https://github.com/wbbeyourself/MAC-SQL) | 345 | 2025-02-27 | ~18 个月 | 论文归档态。阶段 1"项目持续维护"不成立；无 LICENSE |
| [hexinfo/dat](https://github.com/hexinfo/dat) | 260 | 2025-12-26 | ~8 个月 | 语义建模思路对（pre-modeling），但已停更，Apache-2.0 |
| [DinobaseHQ/dinobase](https://github.com/DinobaseHQ/dinobase) | 264 | 2026-07 | 1 个月 | "agent-first database"，HN 热帖来源，规模仍小，观察名单 |

---

### 五、重点回答：谁真正做到了 L3+，而不是套壳单句 text-to-SQL

**真 L4（规划 + 主动产出）—— 只有 1 个**
- **DeepEye**：唯一具备"意图分解→分层规划→拓扑调度执行→自动产出报告/仪表盘/数据视频"完整闭环且代码可跑的开源系统。港科大出品，SIGMOD Demo 2026。https://github.com/HKUSTDial/DeepEye

**真 L3（多步分析与归因）—— 5 个，各有短板**
- **DB-GPT**：多智能体 + AWEL 编排 + 沙箱 Python 分析，生态最完整；短板是复杂度高、文档滞后。https://github.com/eosphoros-ai/DB-GPT
- **openchatbi**：唯一把 **Adtributor 多维下钻归因 + 异常检测 + 时序预测**写成一等公民的开源 ChatBI；短板是单人维护、作者自承未达生产。https://github.com/zhongyu09/openchatbi
- **Auto-Analyst**：planner 路由 + 统计检验/ML 建模 agent，分析深度真实；短板是偏 dataframe 数据科学，SQL/数仓侧弱。https://github.com/FireBird-Technologies/Auto-Analyst
- **agno-agi/dash**：错误诊断→修复→沉淀 learnings 的自学习闭环 + Engineer agent 沉淀数据资产；短板是 template 形态、7 月后未推代码。https://github.com/agno-agi/dash
- **nao**：上下文工程 + dbt 集成 + 内置评测框架，工程化程度最高；短板是自定义许可证、商业公司主导。https://github.com/getnao/nao

**真 L5（数据建设与治理）—— 全部是 2026 年新出现的，且与 text-to-SQL 是两条线**
- **altimate-code**（MIT，2026-02 新建，今天仍在推代码）：dbt 模型脚手架、列级血缘、测试生成、跨仓比对、FinOps、PII——**这是"数据建设 agent"目前最实的开源形态**。https://github.com/AltimateAI/altimate-code
- **dbt-agent-skills**（dbt Labs 官方，Apache-2.0）：把数仓建模工作流固化成 agent 技能。https://github.com/dbt-labs/dbt-agent-skills
- **Cube / WrenAI MDL / SuperSonic** 提供的是**受治理的指标语义层**，是 L5 的地基而非 agent 本身；WrenAI 明确"planning occurs through MDL semantic definitions rather than independent reasoning"——即它用语义层换取正确性，主动放弃了自主多步推理。

**关键结构性发现**：开源世界里 **"会分析的（L3-L4）"和"会建设的（L5）"是两拨完全不相交的项目**。DeepEye/openchatbi/Auto-Analyst 不碰数仓建模；altimate-code/dbt-agent-skills 不做业务问答归因。唯一试图跨界的是 agno-agi/dash 的 Analyst+Engineer 双 agent 设计和 DB-GPT 的全栈铺法，但都还很浅。**"从一句话问数一路做到自动建模+指标治理"的端到端开源 Data Agent，2026-08 时点仍不存在。**

**另一个反直觉发现**：纯 text-to-SQL 赛道的开源创新已经枯竭。2026 年新增的高质量项目全部往两端跑——要么往上做 agent 规划与归因（DeepEye/nao/dash），要么往下做语义层与数据工程（Cube/Databao/altimate-code/dbt-agent-skills）。中间层"更准的单句 SQL 生成"（sqlcoder、Dataherald、MAC-SQL、XiYanSQL 模型仓）全部停更或降速——这是被通用大模型能力上涨直接吞掉的赛道。
