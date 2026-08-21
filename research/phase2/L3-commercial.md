# L3-commercial — 商业产品线深度核实（云巨头 / 独立头部 / 传统BI / 国内厂商）

调研日期：2026-08-20　｜　时效硬约束：仅采纳 2025-01 之后证据　｜　能力层级：L1 单句 text-to-SQL → L2 多步/自纠错 → L3 分析归因 → L4 规划与主动分析 → L5 数据建设与治理

## 执行路径

- Databricks Genie One 官方新闻稿（2026-06-16，GA/预览边界） https://www.databricks.com/company/newsroom/press-releases/databricks-launches-genie-one-all-new-agentic-coworker-every-team
- Databricks 下一代 Genie 博客（实为 2026-04-26，1.5M Genie Spaces） https://www.databricks.com/blog/next-generation-databricks-genie
- Databricks AI/BI + Genie One 2026 发布说明（scheduled task 频率降级为「最快每日」） https://docs.databricks.com/aws/en/ai-bi/release-notes/2026
- Snowflake Intelligence GA 新闻稿（2025-11-04，1000+客户/15000+ agent） https://www.snowflake.com/en/news/press-releases/snowflake-intelligence-brings-agentic-AI-to-the-enterprise/
- Snowflake CoWork 官方产品页（Deep Research / Automations / Cortex Sense，9,100 周活客户） https://www.snowflake.com/en/product/snowflake-cowork/
- Snowflake CoWork 官方文档（工具集、orchestrator 规划、限制） https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence
- Snowflake Intelligence→CoWork 更名确认（2026-06-02 Summit） https://siliconangle.com/2026/06/03/snowflake-cowork-powers-real-world-agentic-ai-snowflakesummit/
- Snowflake 语义模型 BIRD 数据原始出处（2025-03-31，57%→78%） https://www.snowflake.com/en/blog/engineering/agentic-semantic-model-text-to-sql/
- Snowflake Cortex Analyst 官方文档限制（不做趋势洞察、无跨轮结果记忆） https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst
- Microsoft Fabric data agent 官方概念文档（只读、5数据源、25行×25列上限） https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent
- Fabric Build 2026 分析栈发布（NL2SQL 改进 + Code Interpreter + GPT-5.X 约20%提升） https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Building-the-agentic-analytics-stack-Fabric-Analytics-at-Build/ba-p/5191634
- BigQuery Conversational Analytics GA（2026-07-01，AI.KEY_DRIVERS 归因/deep-dive） https://cloud.google.com/blog/products/data-analytics/conversational-analytics-in-bigquery-now-ga
- AWS re:Invent 2025 分析栈（SageMaker Data Agent 拆解任务生成 SQL+Python） https://aws.amazon.com/blogs/big-data/aws-analytics-at-reinvent-2025-unifying-data-ai-and-governance-at-scale
- Salesforce Tableau Agentic Analytics Platform（2026-05-05，3300万语义模型） https://www.salesforce.com/news/stories/tableau-agentic-analytics-platform-announcement/
- Salesforce 完成收购 Waii（2025-08-15） https://www.hpcwire.com/bigdatawire/this-just-in/salesforce-completes-acquisition-of-waii-to-advance-natural-language-to-sql-in-data-cloud/
- Alation 收购 Numbers Station（2025-05-20） https://www.alation.com/news-and-press/alation-acquires-numbers-station-unlocking-new-era-of-agentic-workflows/
- IBM 收购 Seek AI（2025-06-02，并设 Watsonx AI Labs） https://www.cio.com/article/4000760/ibm-acquires-seek-ai-launches-watsonx-labs-to-scale-enterprise-ai/
- Mews 收购 DataChat（2025-10-28，酒店 PMS 垂直收编） https://www.mews.com/en/press/mews-acquires-datachat
- ServiceNow 收购 Pyramid Analytics（2026-02-12 宣布 / 03-10 完成，数亿美元） https://siliconangle.com/2026/02/12/servicenow-buys-pyramid-analytics-streamline-access-business-intelligence/
- SAP 收购 Dremio（2026-05 宣布 / 07-06 完成） https://news.sap.com/2026/05/sap-to-acquire-dremio-unify-sap-and-non-sap-data-power-agentic-ai/
- ThoughtSpot Spotter Semantics（2026-03-12，确定性 search-token 而非 LLM 生成 SQL） https://www.thoughtspot.com/press-releases/thoughtspot-introduces-spotter-semantics-to-bring-trust-and-context-to-enterprise-ai
- Qlik Agentic Data Engineering GA（Data Product / Data Quality / Catalog / Pipeline Agent） https://www.qlik.com/blog/qlik-agentic-data-engineering-is-generally-available-heres-what-that-actually-means
- Qlik 从 Answers 到 Agentic Action（2026-04，Discovery Agent 已产出 10万+ discoveries） https://www.qlik.com/us/news/company/press-room/press-releases/qlik-extends-analytics-from-answers-to-agentic-action
- TextQL $17M 战略轮官方博客（Blackstone 领投，收入 9x，NDR>300%） https://textql.com/blog/textql-raises-17m-blackstone
- WisdomAI $50M Series A（2025-11-12，累计 $73M，约40家企业客户） https://techcrunch.com/2025/11/12/ai-data-startup-wisdomai-has-raised-another-50m-led-by-kleiner-nvidia/
- Omni $120M Series C（2026-04-23，估值 $1.5B，收入 4x） https://omni.co/blog/press-release-omni-series-c-funding
- Sigma $80M Series E（估值 $3B，ARR $200M，2000+ 企业客户） https://www.sigmacomputing.com/resources/announcements/series-e
- Julius AI $10M 种子（2025-07-28，200万用户） https://techcrunch.com/2025/07/28/ai-data-analyst-startup-julius-nabs-10m-seed-round/
- Hex $70M Series C（2025-05-28，累计 $172M）+ 收购 Hashboard（2025-04-30） https://hex.tech/blog/series-c/
- 蚂蚁 Agentar-Scale-SQL 登顶 BIRD（2025-09-25，EX 81.67%）+ 开源（2025-12） https://arxiv.org/abs/2509.24403 ／ https://finance.sina.com.cn/tech/roll/2025-12-15/doc-inhawaui2465773.shtml
- 火山引擎 Data Agent 2026 升级（2026-06-23，规划器/反思器/执行器；抖音集团10类岗位36类任务） https://cn.chinadaily.com.cn/a/202606/24/WS6a3b7969a310d709c2fb9d01.html
- 阿里云 DMS ChatBI / Data Copilot 官方文档（大小模型融合 + 点赞沉淀 SQL） https://help.aliyun.com/zh/dms/data-copilot
- 腾讯云 ChatBI 波动归因与生成报告升级（2025-08） https://blog.csdn.net/cloudbigdata/article/details/149850466
- 帆软 FineChatBI Text2DSL 路线 https://www.jazzyear.com/article_info.html?id=1288
- Aloudata Agent NL2MQL2SQL「100% 准确」宣称 https://aloudata.com/blogs/aloudata-agent-noetl-semantic-layer
- Silicon Data 实为 GPU 算力定价/基准公司（$30.5M Series A） https://www.silicondata.com/news-room/silicon-data-raises-30-5-million-series-a

## 剔除

- Silicon Data | 阶段1误判：实为 AI 算力定价/GPU 基准指数公司（CME 用其 H100/B200 指数做期货标的），与 text-to-SQL/Data Agent 无关；且金额为 $30.5M 非 $31M。
- 网易有数 / 九数云 / FineBI NEXT「2026-09 场景Agent」 | 唯一来源是 sohu.com 一篇厂商横评软文，无官方发布佐证，且 2026-09 晚于当前日期属未发生事件。
- Text2SQL.ai / AI2SQL | 网页玩具级 SQL 生成器，无企业部署、无语义层、无 2025+ 实质产品更新，不构成商业头部。
- Chat2DB | 定位是 AI 增强 SQL 客户端（IDE），非数据分析 agent，评价体系不同。
- Dataherald | 开源引擎而非商业厂商，且 2025 年后无活跃商业化信号，归属开源分工组。
- Coginiti | 累计融资仅 $6M，2025+ 无融资/产品/客户任何可核实新信号。
- Hebbia | 非结构化文档检索（金融/法律），不触及仓库结构化查询，与本赛道评价维度不可比。
- OpenAI Deep Research / ChatGPT MCP 连接器 | 通用研究 agent，OpenAI 未发布任何企业级 text-to-SQL / 语义层产品，仅作为底座模型出现在他家产品里。
- Zenlytic | 融资停留在 2024-09（$9M A 轮），2025+ 无融资、无客户规模、无准确率任何可核实新证据，降为观察位。
- 百度智能云千帆「数据智能平台」 | 反复检索未找到对标 Cortex Analyst/Genie 的独立数据 agent 产品文档，仅有平台级 Agent Infra 泛述，证据不足。
- Menza / Livedocs / Fabi.ai | 种子期或刚公开发布，无融资额、ARR、客户数任何硬数据，不进入头部象限。
- Amazon Q generative SQL for Redshift | 2024 GA 的老功能，2025 年仅扩区域，无能力层级变化，已被 SageMaker Data Agent 取代叙事位。

---

## 结论

### 0. 总纲：2026 年商业产品的真实分层

**核心判断：绝大多数「Data Agent」在官方文档里仍是 L1-L2，只有极少数跨到 L3-L4，L5 目前只有 Qlik 一家给出了 GA 级产品化答案。**

判定方法：不看营销词（"agentic"/"agent"满天飞），只看官方文档三件事——(a) 是否只读；(b) 是否能自主规划多步并产出报告/文档；(c) 是否能定时/主动触发并对外执行动作。

| 分层 | 代表 | 判据 |
|---|---|---|
| L1-L2 | Fabric data agent、Cortex Analyst、阿里云 DMS ChatBI、PolarDB Data-Agent | 严格只读、单问单答、无跨轮结果记忆 |
| L3 | 腾讯云 ChatBI、观远/衡石、Julius、WisdomAI | 有归因模型、生成解读报告，但不主动、不规划长任务 |
| L4 | Genie One、Snowflake CoWork、BigQuery CA、火山 Data Agent、Qlik Answers | 多步规划 + 定时/告警 + 产出物 + MCP 对外动作 |
| L5 | Qlik Agentic Data Engineering（部分）、Genie ZeroOps（私有预览） | 自主建管道/治数据质量/改数据模型 |

---

### 一、云与数据平台巨头（四象限之一）

**1) Databricks Genie One — 目前最完整的 L4，且已 GA**（https://www.databricks.com/company/newsroom/press-releases/databricks-launches-genie-one-all-new-agentic-coworker-every-team）
- 2026-06-16 Data+AI Summit 2026 发布。**GA：Genie One、Genie Agents、Genie Code**；**私有预览：Genie App Builder、Genie ZeroOps**。
- 官方能力表述（可对照）：设置告警做常驻监控、调度任务、创建可复用 skill、通过 MCP 工具「take action anywhere」、产出 documents/reports/artifacts → **L4**。
- Genie Ontology 是「self-improving context layer」，连接 50+ 应用与数据系统，持续抽取业务知识 → 语义层自动化，触及 **L5 边缘但非完整数据建设**。
- Genie Code 定位「数据工程、ML、分析工作流的自主 agent」→ 若兑现即 **L5**，但新闻稿未给出自主改动生产管道的证据。
- Genie ZeroOps 是后台 agent「自主监控、调查并提出修复方案」——注意是 **propose fixes 而非 apply**，且仅私有预览 → **L4→L5 过渡态**。
- **规模数据**：1.5M Genie Spaces（2026 年内创建，https://www.databricks.com/blog/next-generation-databricks-genie）。**无任何官方准确率数字**。
- ⚠️ 阶段1修正：`next-generation-databricks-genie` 博客实为 **2026-04-26**（讲统一 Genie Chat 取代 Databricks One），并非 Summit 的 Genie One 发布，两者不可混为一条。
- ⚠️ 能力边界证据：官方发布说明记载 scheduled task **频率已从小时级/分钟级下调为最快每日**（https://docs.databricks.com/aws/en/ai-bi/release-notes/2026）——说明「主动分析」在成本与稳定性上仍受限。

**2) Snowflake：Intelligence 已更名 CoWork，从 L2 抬到 L4**（这是阶段1完全漏掉的关键变化）
- 2025-11-04 Snowflake Intelligence GA（https://www.snowflake.com/en/news/press-releases/snowflake-intelligence-brings-agentic-AI-to-the-enterprise/）。**规模数据（迄今该赛道最硬的一组）**：1000+ 客户部署 15000+ AI agent（截至 2025-10-24）；Snowflake 自家 GTM 助手服务 6000+ 员工、每周回答 12500+ 问题；总客户基数 12000+。
- **2026-06-02 Snowflake Summit 2026 更名为 Snowflake CoWork**（Cortex Code 同时更名 CoCo），存量客户自动迁移（https://siliconangle.com/2026/06/03/snowflake-cowork-powers-real-world-agentic-ai-snowflakesummit/）。定位从「对话式分析」扩为「personal work agent」。
- CoWork 官方产品页（https://www.snowflake.com/en/product/snowflake-cowork/）：**Deep Research** 跨全数据资产做带引用的多步调查 → **L3-L4**；通过 MCP 连 Slack/Gmail/Jira/Salesforce/Teams **直接执行动作** → **L4**；**Automations（公开预览）** 定时简报与异常告警推送到邮件/Slack/移动端 → **L4 主动分析**；**Cortex Sense（私有预览）** 免手工搭语义模型、自动汇聚数据与定义 → **L5 苗头**。
- **规模数据**：9,100+ 客户每周使用 Snowflake AI 产品（截至 2026-01-31 当周）。
- **成熟度诚实标注**：官方页面自述 Skills / Automations / Agent Memory / Cortex Sense **仍在公开或私有预览**，Agent Studio「即将 GA」——即 CoWork 的 L4 能力大部分尚未 GA。
- 官方文档（https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence）确认 orchestrator 会「解释意图、选择工具、规划动作序列」，Deep Research 拆成并行子调查、最长 10 分钟；工具仅三类（Cortex Analyst / Cortex Search / 自定义 UDF·存储过程）；限制：单文件 50MB、最多 5 文件、不支持地图类图表。
- **准确率数据（本次唯一被追到原始出处的 BIRD 数字）**：https://www.snowflake.com/en/blog/engineering/agentic-semantic-model-text-to-sql/（2025-03-31）——在 BIRD 四个数据集上，vanilla Claude 3.5 Sonnet 平均 **57% → 加语义模型的 agentic 系统 78%，+21pp**（分数据集：52→83 / 63→80 / 45→70 / 69→79）；官方同时点出 **BIRD 人类准确率 93%**。⚠️ 阶段1把这个数字挂在了 2024-08 的 `cortex-analyst-text-to-sql-accuracy-bi` 博客上，**来源错配**，那篇是 2024 年的 90%+/GPT-4o 掉到 51% 的另一组数据，已过时效线。
- **底层 Cortex Analyst 本体仍是 L1-L2**：官方文档明写「只能回答 SQL 能解的问题，不产出『你观察到什么趋势』这类洞察」「无法访问上一轮 SQL 的结果」——所以 Snowflake 的 L3+ 全部靠 Cortex Agents/CoWork 编排层补齐，不是 text-to-SQL 本体变强。

**3) Microsoft Fabric Data Agent — 官方文档证明它是严格 L2，不是 L3+**（最重要的"祛魅"结论）
- 官方概念文档（https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent，GA）逐条限制：
  - **只生成 read 查询**，不生成任何 create/update/delete；不触发 notebook、异常检测作业或任何写/动作工作流 → **排除 L4/L5**。
  - 单 agent **最多 5 个数据源**；每数据源最多 100 条示例查询。
  - **响应上限 25 行 × 25 列**，明确自述「面向对话式洞察而非返回完整数据集」。
  - 不支持非结构化数据（pdf/docx/txt）；不支持非英语；不可更换 LLM；对话历史可能丢失。
- 机制是：问题解析→数据源识别→分派 NL2SQL / NL2DAX / NL2KQL / Graph 工具→校验→执行→格式化。是**路由 + 单轮生成**，无自主多步规划 → **L2**。
- 2026 Build 增量（https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Building-the-agentic-analytics-stack-Fabric-Analytics-at-Build/ba-p/5191634）：NL2SQL 与数据源路由改进（预览）、意图模糊时**会反问澄清**、**Code Interpreter 工具带来 Python 执行**（预测/统计/数据变换）→ 把 Fabric 推到 **L2→L3 边缘**；基座升级到 GPT-5.X 带来**内部基准约 20% 准确率提升**（官方措辞为 internal benchmarks，非公开可复现）。
- 真正的 L4 编排在 Fabric 之外：由 Copilot Studio / Azure AI Foundry 等外部 orchestrator 调用 Fabric data agent，官方原文「data agents remain focused on read-only, governed data access」——**微软把 agent 边界画得最清楚，Data Agent 就是一个受治理的只读数据工具**。

**4) Google BigQuery Conversational Analytics — 2026-07-01 GA，L3-L4 且内建归因原语**（https://cloud.google.com/blog/products/data-analytics/conversational-analytics-in-bigquery-now-ga）
- 官方明列：agent **构建分析计划并执行完整多步调查**；`AI.FORECAST` 预测、`AI.DETECT_ANOMALIES` 异常检测、**`AI.KEY_DRIVERS` 定位指标变动背后的分段（即归因）** → **L3 归因能力被做成了 SQL 原语，这是与竞品的关键差异**。
- **Deep-dive 模式**产出可下载报告；**agentic workflows 可按计划监控数据、跑多步流程并推送洞察** → **L4**。
- 长期记忆跨会话保留术语与上下文；展示推理步骤/生成的 SQL/上下文引用（可解释性）；跨云读 Iceberg / Databricks Unity / AWS Glue / SAP / Salesforce。
- **无任何准确率或采用规模数字**，仅 MoneySuperMarket 一条「数周→数分钟」客户证言。官方文档亦未列限制，属营销侧信息不对称。

**5) AWS — 唯一把 agent 放进 notebook 而非 BI 的巨头，L3**（https://aws.amazon.com/blogs/big-data/aws-analytics-at-reinvent-2025-unifying-data-ai-and-governance-at-scale）
- re:Invent 2025 发布 **Amazon SageMaker Data Agent**：给定目标后**把复杂分析/ML 任务拆成步骤、生成所需 SQL 与 Python、并全程感知 notebook 环境** → **L3（多步 + 代码执行 + 上下文）**，未见定时/主动/对外动作证据故不判 L4。
- 载体是新的 serverless notebook（SQL + Python + Spark + 自然语言四合一，后端 Athena for Spark），从 SageMaker / Athena / Redshift / S3 Tables 控制台均可进入。
- AWS 引用的是「数据团队 60-70% 时间花在无差别任务上」的动机数据，**无准确率、无部署规模**。
- 战略含义：AWS 走「给数据工程师配副驾」路线，Databricks/Snowflake 走「给业务方配同事」路线，两者的 L 层级看似接近，服务对象完全不同。

---

### 二、独立头部（按 ARR / 融资 / 估值排序，逐条对照 2025+ 新闻源）

| 公司 | 最新轮次 | 金额/估值 | 日期 | ARR/规模 | 能力层级 | 核实来源 |
|---|---|---|---|---|---|---|
| **Sigma Computing** | Series E | $80M @ **$3B 估值**（Princeville 领投；Databricks/ServiceNow/Workday Ventures 跟投） | 2026-05 | **ARR $200M**（2026-04 达成，同比 100%+ 增长）、**2000+ 企业客户**（AMD/Duolingo/JPMorgan） | **L2-L3**，自述向 agentic analytics 转型 | https://www.sigmacomputing.com/resources/announcements/series-e |
| **Omni Analytics** | Series C | $120M @ **$1.5B 估值**（ICONIQ 领投，含 $30M 员工老股）；估值较 2025-03 的 $650M 翻倍 | 2026-04-23 | 收入 **4x YoY**；BambooHR 10万+用户 | **L2**（语义层 + 把治理数据开放给 Claude/ChatGPT/Cursor/VS Code 等外部 agent）→ 它选择做**别人 agent 的语义底座**，而非自己做 L4 | https://omni.co/blog/press-release-omni-series-c-funding |
| **WisdomAI** | Series A | $50M（Kleiner Perkins 领投 + NVentures），**累计 $73M** | 2025-11-12 | **约 40 家企业客户**（从 2024 底的 2 家起步）；某客户 10 席→450 席 | **L3**（"enterprise context layer" 处理脏数据；新增 agentic 实时告警）；关键设计：**LLM 只写 query 不生成答案**，以规避幻觉 | https://techcrunch.com/2025/11/12/ai-data-startup-wisdomai-has-raised-another-50m-led-by-kleiner-nvidia/ |
| **Hex** | Series C | $70M，**累计 $172M**；2025-04-30 收购 Hashboard 补 BI | 2025-05-28 | 未披露 ARR；2026-06 员工 272 人 | **L3**（notebook 形态 SQL+Python+Agent） | https://hex.tech/blog/series-c/ |
| **TextQL** | 战略轮 | $17M（**Blackstone Innovations Investments 领投**，Hof/Neo/Unshackled/Dropbox 跟投） | 2026-04 | **收入 9x YoY，NDR > 300%**；已在 Amazon、Dropbox 生产环境运行 | **L3-L4**（agent "Ana" 自述替代三周数据请求周期→90 秒自动答案，定位 virtual data scientist） | https://textql.com/blog/textql-raises-17m-blackstone |
| **Julius AI** | Seed | $10M（Bessemer 领投；Perplexity/Vercel/Twilio 创始人跟投），累计 $11M | 2025-07-28 | **200 万+ 用户**、日均执行 400 万行分析代码、1000 万+ 可视化；**ARR > $15M**（两年内） | **L3 但偏 PLG/文件分析**（自然语言做分析、可视化、预测建模、训 ML 模型）；**未见企业数仓直连与治理能力证据** | https://techcrunch.com/2025/07/28/ai-data-analyst-startup-julius-nabs-10m-seed-round/ |

**读法**：钱在往两个方向走——(a) **语义层/治理底座**（Omni、Sigma）拿最大票，因为所有人都发现准确率瓶颈在上下文不在模型；(b) **端到端 agent**（TextQL、WisdomAI）拿增长最快的票（9x 收入、NDR>300%）。**没有一家纯 text-to-SQL API 公司拿到大额独立融资——它们全被收购了（见下）。**

---

### 三、并购：赛道被平台方系统性收编（四件全部核实确认，另发现两件阶段1遗漏的重磅）

| 事件 | 日期 | 状态 | 战略含义 |
|---|---|---|---|
| **Alation ← Numbers Station** | 2025-05-20 | ✅ 确认 | Stanford 系，此前融资 $17M+（Norwest/Madrona/Factory）。**元数据目录厂商买 agent** = 承认目录本身不产生价值，要靠 agent 消费元数据。https://www.alation.com/news-and-press/alation-acquires-numbers-station-unlocking-new-era-of-agentic-workflows/ |
| **IBM ← Seek AI** | 2025-06-02 | ✅ 确认 | 并入 watsonx，同日发布 NYC 的 Watsonx AI Labs（$500M 支持）。https://www.cio.com/article/4000760/ibm-acquires-seek-ai-launches-watsonx-labs-to-scale-enterprise-ai/ |
| **Salesforce ← Waii** | 2025-08-07 签约 / **2025-08-15 完成** | ✅ 确认 | 最具技术含量的一笔：Waii 的**动态构建企业数据元数据知识图谱**成为 **Tableau 下一代语义引擎的底座**，同时注入 Data Cloud 与 Agentforce。https://www.hpcwire.com/bigdatawire/this-just-in/salesforce-completes-acquisition-of-waii-to-advance-natural-language-to-sql-in-data-cloud/ |
| **Mews ← DataChat** | 2025-10-28 | ✅ 确认 | **买家是酒店 PMS 公司，不是数据厂商** → 信号是「垂直 SaaS 直接买通用对话式分析做 agentic hospitality」，说明该能力开始被当作垂直行业的功能组件而非独立品类。https://www.mews.com/en/press/mews-acquires-datachat |
| **ServiceNow ← Pyramid Analytics**（阶段1遗漏） | 2026-02-12 宣布 / 2026-03-10 完成 | ✅ 确认，作价估计「数亿美元」 | 工作流平台把 BI 内化为 AI 平台的分析层，让业务方在工作流里直接自然语言提问。https://siliconangle.com/2026/02/12/servicenow-buys-pyramid-analytics-streamline-access-business-intelligence/ |
| **SAP ← Dremio**（阶段1遗漏） | 2026-05 宣布 / **2026-07-06 完成** | ✅ 确认，金额未披露（Dremio 2022 年估值 $2B） | 为 Business Data Cloud 补 Iceberg 原生湖仓，**明确目标是"power agentic AI"**——巨头买的是 agent 的**数据底座**，不是 agent 本身。https://news.sap.com/2026/05/sap-to-acquire-dremio-unify-sap-and-non-sap-data-power-agentic-ai/ |

**结论**：2025-2026 共 6 起相关并购，买方类型分三类——数据治理厂商（Alation）、平台巨头（IBM/Salesforce/SAP）、工作流与垂直 SaaS（ServiceNow/Mews）。**纯 NL2SQL 引擎已不具备独立公司价值，估值锚点转移到语义层/知识图谱/湖仓底座。**

---

### 四、传统 BI 厂商 AI 化

**1) Salesforce / Tableau — L3-L4 承诺，交付分批**（https://www.salesforce.com/news/stories/tableau-agentic-analytics-platform-announcement/）
- 2026-05-05 发布 Agentic Analytics Platform，自我定位从可视化转为「knowledge and decision engine」。
- **可核实的独特资产：十年沉淀的 3300 万个语义模型**作为知识接地——这是竞品无法复制的存量。
- 交付节奏（重要的期望管理）：Tableau Agent 对话式能力 **已可用**；MCP servers **已可用**；**Auto Knowledge Graph 2026-07**；**Agentic Analytics Command Center 2026 秋**。
- 「触发工作流的自动化决策」+ headless 分发到 Slack/Teams/Claude/ChatGPT → 若 Command Center 如期交付则为 **L4**；当前可核实部分为 **L3**。
- **无任何准确率数字**；引用的 97% 财富100强是 Tableau 整体而非 agentic 平台。
- Waii 的知识图谱是这条线的技术底座（见并购表）。

**2) Qlik — 唯一给出 GA 级 L5 产品的厂商**（https://www.qlik.com/blog/qlik-agentic-data-engineering-is-generally-available-heres-what-that-actually-means）
- **Agentic Data Engineering 已 GA**，含四个 agent：**Data Product Agent**（数据产品的规格/创建/治理/发布）、**Data Quality Agent**（剖析、监控并**修复**数据错误）、**Catalog & Business Glossary Agent**（自动发现/分类/文档化）、**Pipeline Agent**（自动构建与部署智能管道，季内预览、年内 GA）。
- 官方原文强调这些不是助手而是「autonomous, goal-based components…take action」；且支持用 **Claude Code / GitHub Copilot + VS Code 以自然语言构建和更新 Qlik 数据管道**，产出「day one 即带治理与质量评分的管道」→ **这是本次调研中唯一有 GA 证据的 L5（数据建设与治理）**。
- 分析侧：2026-02 agentic experience GA；2026-04 扩展为 Answers + Discovery Agent + MCP Server + 预测/自动化/分析开发 agent，闭环「detect → investigate → predict → act」→ **L4**。
- **规模数据**：Discovery Agent 自 2026-02 GA 起已为客户产出 **10 万+ discoveries**；多数开通 agentic 工具的 Qlik Cloud 账户在实际使用（https://www.qlik.com/us/news/company/press-room/press-releases/qlik-extends-analytics-from-answers-to-agentic-action）。
- ⚠️ **无任何自家性能数据**，唯一引用的是 Gartner「2029 年 agentic 数据管理将自动化 75% 数据工程工作流」的预测——**L5 宣称目前缺少可验证的效果证据**。

**3) ThoughtSpot — 反 text-to-SQL 路线，L2-L3 但确定性最高**（https://www.thoughtspot.com/press-releases/thoughtspot-introduces-spotter-semantics-to-bring-trust-and-context-to-enterprise-ai）
- 2026-03-12 发布 **Spotter Semantics**，自称「行业领先的 agentic 语义层」。
- **技术路线是本调研中最独特的一条**：坚持用专利 **search-token 引擎**把自然语言编译为确定性查询，**明确不用 LLM 生成 SQL**——理由是只有确定性才能保证一致可信。对本课题的方法论价值：**这是"绕开 text-to-SQL 准确率问题"而非"提升 text-to-SQL 准确率"的代表**。
- 新增：下一代 search token、**aggregate awareness**（按问题自动路由明细表或预聚合表，降延迟与算力成本）、集中式指标目录、**MCP server 对外部 AI agent 与 LLM 开放语义层**。
- 层级：查询侧 **L2**（确定性、可组合，但受 token 表达力限制）；SpotterViz/SpotterModel/SpotterCode 系列 agent 把平台自动化推到 **L3**。**无公开准确率数字**（其论点恰是"确定性不需要准确率指标"，但这也意味着不可与 BIRD 类基准比较）。

**4) SAP / Strategy(MicroStrategy)** — SAP 主线是买 Dremio 补底座（见并购表），Joule Analytical Insights 属 **L1-L2** 的自然语言查询；Strategy Auto Answers 2025-01 更新为个性化体验，仍是 **L1-L2 治理数据问答**，2025+ 无 agent 化实质突破。两家在本赛道属跟随者。

---

### 五、国内厂商

**1) 蚂蚁数科 Agentar-Scale-SQL — 国内唯一有国际基准硬数据的一家（L1-L2 技术，但技术领先）**
- 2025-09-25 登顶 **BIRD-SQL**：**执行准确率 81.67%、执行效率 77%，双榜第一**，超越 Google/Amazon，并连续领跑两月以上（https://news.qq.com/rain/a/20250926A0778J00）。
- 论文 arXiv:2509.24403《Agentar-Scale-SQL: Advancing Text-to-SQL through Orchestrated Test-Time Scaling》——**方法本质是编排式 test-time scaling**，即多候选生成 + 选择，属 **L1-L2 的极致工程化，不是 L3+**。
- 2025-12-13 全套开源（论文/代码/模型），2025-11 已开源 **Agentar-Scale-SQL-Generation-32B**（HuggingFace + ModelScope）（https://finance.sina.com.cn/tech/roll/2025-12-15/doc-inhawaui2465773.shtml）。
- **重要参照**：81.67% vs Snowflake 官方给出的 BIRD 人类基线 93% —— **单句 text-to-SQL 距离人类仍有 11pp 差距，这本身就是"必须往 L3+ 走"的论据**。

**2) 火山引擎（字节）Data Agent — 国内最接近 L4 的一家**（https://cn.chinadaily.com.cn/a/202606/24/WS6a3b7969a310d709c2fb9d01.html）
- 2026-06-23 Force 原动力大会升级，定位「企业数字合伙人」。**官方明确的架构是「规划器 + 反思器 + 执行器」协同完成任务理解、方案校验和多步调度** → **L3-L4**（规划 + 自我校验是 L4 的核心判据）。
- 强调「任务链的最后两步『生成产物』『推动执行』」是 agent 见效关键 → 与 Genie One / CoWork 的 artifact + action 叙事同构。
- 支持跨系统打通，融合结构化数据 + 知识文档 + 业务经验。
- **规模数据（国内最实的一组）**：抖音集团内部为 **10 类岗位角色完成 36 类工作任务**；使用占比 **数据分析与文档生成 30%、知识检索 20%+、创意生成 10%+**。
- 另一贡献：2025 年推出 **Data Agent 评测体系**并发布《2025 数据智能体实践指南》，测试集围绕**「分析周报」「现象归因」「自由探索」**三类场景，覆盖基础能力/复杂任务/可靠性/工具使用效率多层框架（https://zhuanlan.zhihu.com/p/1965003368121476250）——**这是国内唯一公开的 L3+ 评测标准尝试，方法论价值高于产品本身**，且其场景定义与本课题 L3/L4 的划分高度吻合。

**3) 腾讯云 ChatBI — L3，归因做得最实**
- 2025-03 上线**数据解读与波动归因**；2025-08 大升级「一键生成深度洞察报告」，支持发散提问、多轮对话、**多步计算与复杂表头分析**，自述「从问数智能体跃升为决策智能体」（https://blog.csdn.net/cloudbigdata/article/details/149850466）。
- 归因流程可核查：自动识别日期与指标 → 智能匹配维度 → **调用 Delta 法或 Shapley 值归因模型** → 量化各维度贡献度 → 生成可视化报告 → **L3，且归因是统计方法而非 LLM 自由发挥**，可信度高于纯 prompt 式归因。
- 无准确率与部署规模公开数据。

**4) 阿里云 — 产品线分散，均为 L1-L2**
- ChatBI on DMS：自研**大小模型融合**方案保障 SQL 生成准确率；Data Copilot 支持**点赞沉淀 SQL**，相似问题复用以提升准确率（https://help.aliyun.com/zh/dms/data-copilot）→ 典型 **L1-L2 + 反馈闭环**。
- PolarDB Data-Agent：自然语言转 SQL 与智能图表（https://help.aliyun.com/zh/polardb/polardb-for-mysql/chatbi-best-practices）→ **L1**。
- DataWorks ChatBI：零代码自然语言分析助手 → **L1-L2**。
- **无任何官方准确率数字**，且三条产品线（DMS / PolarDB / DataWorks）能力重叠、未收敛为统一 Data Agent，是与火山引擎的主要差距。

**5) 帆软 FineChatBI — Text2DSL 路线，L2**（https://www.jazzyear.com/article_info.html?id=1288）
- 不走 Text2SQL，走 **Text2DSL2SQL**：先把自然语言转成**用户看得懂、可干预**的数据查询结构（DSL），再由底层引擎编译成 SQL。**"可干预"是其核心卖点——把不可控的一步拆成人能审的两步。**
- 规则模型 + 大模型混合：规则模型处理简单明确问题以保证完全可控与快速响应，大模型处理复杂模糊问题。
- FineBI 7.0 为「指标中心 + 智能问数」双引擎。**无公开准确率数字**。层级 **L2**。

**6) Aloudata Agent — NL2MQL2SQL，宣称需打折看**（https://aloudata.com/blogs/aloudata-agent-noetl-semantic-layer）
- 路径：NL → MQL（指标查询语言，跑在 NoETL 指标语义层上）→ 由指标引擎编译出 SQL，宣称 **"100% 准确的 SQL 生成"**，架构含 CoT + ReAct、行列级权限。
- ⚠️ **严重存疑标注**：所谓 100% 只成立于 **MQL→SQL 这一段确定性编译**；真正的风险点 **NL→MQL 仍是 LLM 推断**，该宣称把语义理解误差偷换成了翻译层误差。与 ThoughtSpot、帆软属同一族思路（引入中间表示），但**只有 Aloudata 把它包装成"100%"**，属营销越界。层级 **L2**。

**7) 其余国内厂商（证据强度递减，仅列不展开）**：观远 ChatBI（场景化问答式 BI，含意图识别/知识召回/可视化生成，L2-L3）；衡石 HENGSHI SENSE 6.x（Data+AI Agent 架构 + NL2Metrics 指标语义层，向外部 agent 开放 BI 能力调用，L2-L3）；Kyligence（AI 增强语义层解 Text2SQL 准确率，L2）。三家均**无 2025+ 可核实的准确率或客户规模硬数据**。

---

### 六、给后续阶段的三条方法论结论

1. **"Agent" 一词已完全通胀，唯一可靠判据是官方文档的四个开关**：能否写/能否调度/能否跨轮记忆/能否对外执行动作。按此，Fabric 明确 L2（只读+25行上限），Cortex Analyst 明确 L2（无跨轮结果记忆），而 Genie One / CoWork / Qlik 明确 L4。
2. **准确率数据在商业侧近乎真空**。全部核实下来，只有三组数字可用：Snowflake BIRD 57%→78%（+21pp，2025-03，有原始出处与分数据集拆解）、蚂蚁 BIRD EX 81.67%（2025-09，第三方榜单可验证）、Fabric「GPT-5.X 带来约 20% 内部基准提升」（不可复现）。**Databricks / Google / Tableau / Qlik / 所有国内 BI 厂商均未给出任何准确率数字**——这本身是选型时的重大风险信号。
3. **产业的钱和并购都在往 L5 的方向走，但产品还没到**。SAP 买 Dremio、Salesforce 买 Waii、Alation 买 Numbers Station，买的都是**语义层/知识图谱/湖仓底座**而非 agent 本体；Genie Ontology、Cortex Sense、Qlik ADE 三个最激进的 L5 尝试中，两个在私有预览、一个 GA 但零效果数据。**结论：L1-L2 已商品化并被平台收编，L3-L4 是 2026 年的竞争主战场，L5 目前仍是宣称多于交付。**
