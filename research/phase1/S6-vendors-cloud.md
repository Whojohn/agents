# S6 云与数据平台头部厂商 — text-to-SQL / 对话式分析 / data agent 产品能力（广度调研）

## 执行路径
- WebSearch: "Databricks Genie text-to-SQL 2026 update" → databricks.com/blog/next-generation-databricks-genie, docs.databricks.com/aws/en/ai-bi/release-notes/2026
- WebSearch: "Snowflake Cortex Analyst text-to-SQL 2025 2026" → docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst, docs.snowflake.com/en/release-notes/2026/other/2026-04-13-cortex-agents-agentic-analyst
- WebSearch: "AWS re:Invent 2025 Amazon Q data agent text-to-SQL" → aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2025/, aws.amazon.com/blogs/big-data/aws-analytics-at-reinvent-2025-*
- WebSearch: "Microsoft Fabric Copilot data agent natural language 2025 2026" → blog.fabric.microsoft.com/.../fabric-data-agents-microsoft-copilot-studio, aytac.dev fabric-data-agents GA article
- WebSearch: "Google BigQuery conversational analytics Gemini data agent 2025 2026" → cloud.google.com/blog/products/data-analytics/conversational-analytics-in-bigquery-now-ga, docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/overview
- WebSearch: "OpenAI ChatGPT data analysis agent SQL database connector 2025 2026" → 未发现 OpenAI 官方 text-to-SQL/data-agent 专用产品，仅通用 Deep Research + MCP 连接器
- WebSearch: "Anthropic Claude data analysis SQL agent enterprise 2025 2026" → databricks.com/company/newsroom/press-releases/databricks-and-anthropic-*, Anthropic 自身工程博客关于 agentic analytics 的实践（非独立产品）
- WebSearch: "Snowflake Intelligence agent 2025 announcement" → snowflake.com/en/news/press-releases/snowflake-intelligence-brings-agentic-AI-to-the-enterprise, docs.snowflake.com/en/release-notes/2025/other/2025-11-04-snowflake-intelligence (GA)
- WebSearch: "Databricks Data Intelligence Platform NL2SQL benchmark 2025" → 未找到独立 NL2SQL 基准，仅 DBSQL 性能更新（过滤，非 text-to-SQL 核心）
- WebSearch: "AWS Redshift Amazon Q Business analytics agent 2025" → aws.amazon.com/blogs/big-data/write-queries-faster-with-amazon-q-generative-sql-for-amazon-redshift, aws.amazon.com/blogs/big-data/secure-generative-sql-with-amazon-q
- WebSearch: "Amazon QuickSight Q generative BI natural language 2025 2026" → aws.amazon.com/about-aws/whats-new/2025/04/amazon-quicksight-q-embedded
- WebSearch: "Power BI Copilot natural language query 2025 2026 update" → powerbi.microsoft.com/en-us/blog/power-bi-january-2026-feature-summary/, powerbi.microsoft.com/en-us/blog/deprecating-power-bi-qa/
- WebSearch: "Google Looker Gemini conversational analytics 2025" → cloud.google.com/blog/products/data-analytics/gemini-in-looker-deep-dive, docs.cloud.google.com/looker/docs/conversational-analytics-overview
- WebSearch: "Snowflake Data Science Agent 2025 announcement" → snowflake.com/en/news/press-releases/snowflake-intelligence-and-data-science-agent-deliver-the-next-frontier-of-data-agents-for-enterprise-ai-and-ml (Summit 2025, 2025-06-03)

## 候选

| 名称 | 类型 | 一句话描述 | 日期 | URL |
|---|---|---|---|---|
| Databricks Genie（Genie One / Genie Agents 重构） | 产品 | AI/BI Genie 从单一 text-to-SQL 对话框重构为含 Genie One/Code/App Builder/ZeroOps/Ontology 的全套 agentic 数据平台，账户级 GA、支持定时任务 | 2026-06 (Data+AI Summit 2026) | https://www.databricks.com/blog/next-generation-databricks-genie |
| Snowflake Cortex Analyst | 产品 | 全托管 text-to-SQL 服务，基于语义视图（Semantic Views）对结构化数据生成 SQL，BIRD-SQL 上因语义模型提升 21 个百分点准确率 | 2025年起持续迭代 | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst |
| Snowflake Cortex Agents（改进版 SQL 生成） | 产品/更新 | Cortex Agents 直接使用 Cortex Analyst 语义视图作为工具生成 SQL，准确率与延迟均改善 | 2026-04-13 | https://docs.snowflake.com/en/release-notes/2026/other/2026-04-13-cortex-agents-agentic-analyst |
| Snowflake Intelligence | 产品 | 企业级对话式智能代理，员工用自然语言提问、跨结构化/非结构化数据生成分析洞察，GA 面向 1.2万+客户 | 2025-11-04 GA（2025-06 Summit 预览） | https://www.snowflake.com/en/news/press-releases/snowflake-intelligence-brings-agentic-AI-to-the-enterprise/ |
| Snowflake Data Science Agent | 产品 | 自动化 ML 模型开发流程的智能代理，多步推理+上下文理解生成可执行 ML pipeline | 2025-06-03（私有预览） | https://www.snowflake.com/en/news/press-releases/snowflake-intelligence-and-data-science-agent-deliver-the-next-frontier-of-data-agents-for-enterprise-ai-and-ml/ |
| Snowflake Cortex AISQL | 产品 | 用 SQL 命令对文本、图像等多模态数据进行分析 | 2025-06 (Summit 2025) | https://www.snowflake.com/en/blog/engineering/cortex-analyst-text-to-sql-accuracy-bi/ |
| AWS re:Invent 2025 分析代理（Athena for Spark serverless notebook + agent） | 产品 | 新代理将复杂分析/ML任务拆解为步骤，自动生成 SQL 和 Python 代码，感知 notebook 上下文 | 2025-12 (re:Invent 2025) | https://aws.amazon.com/blogs/big-data/aws-analytics-at-reinvent-2025-unifying-data-ai-and-governance-at-scale/ |
| Amazon Q generative SQL for Redshift | 产品 | Redshift Query Editor v2 内置，将自然语言转换为 SQL 查询，2025 年持续扩展区域 | 2024 GA，2025 持续更新 | https://aws.amazon.com/blogs/big-data/write-queries-faster-with-amazon-q-generative-sql-for-amazon-redshift/ |
| Amazon Q in QuickSight（Generative BI） | 产品 | 自然语言构建可视化、复杂计算、数据故事生成（data story），嵌入式仪表盘 GA | 2025-04 GA（embedded） | https://aws.amazon.com/about-aws/whats-new/2025/04/amazon-quicksight-q-embedded |
| Microsoft Fabric Data Agent | 产品 | 面向 OneLake（Lakehouse/Warehouse/语义模型）的自然语言问答代理，理解企业数据架构与治理策略；已 GA 进入 Microsoft 365 Copilot | 2025下半年-2026（M365 Copilot 集成 GA） | https://www.aytac.dev/en/news/fabric-data-agents-microsoft-365-copilot-ga/ |
| Fabric Data Agents + Copilot Studio 多代理编排 | 产品/预览 | Fabric 数据代理与 Microsoft Copilot Studio 集成，实现跨工具多代理编排 | 2025-2026（预览） | https://blog.fabric.microsoft.com/en-us/blog/fabric-data-agents-microsoft-copilot-studio-a-new-era-of-multi-agent-orchestration |
| Fabric NL2SQL Engine 改进 + Creator Agent for SQL/Eventhouse | 产品/预览 | Build 2026 发布的改进版 NL2SQL 引擎、SQL/Eventhouse 数据源 Creator Agent、Python Code Interpreter Tool | 2026-05/06 (Build 2026) | https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Build-2026-From-data-to-intelligence-Faster-with-Fabric-Data/ba-p/5191636 |
| Power BI Copilot（自然语言问答，替代 Q&A） | 产品 | 生成式 AI 驱动的自然语言查询/可视化/报表页生成/DAX 辅助，移动端支持；legacy Q&A 于2026-12 弃用 | 2025-2026 持续迭代，Q&A 弃用2026-12 | https://powerbi.microsoft.com/en-us/blog/deprecating-power-bi-qa/ |
| BigQuery Conversational Analytics | 产品 | Gemini 推理内嵌 BigQuery，自然语言转 SQL、多步分析（ML.FORECAST/异常检测）、可视化报告、自主代理工作流，GA | 2026-07-01 GA | https://cloud.google.com/blog/products/data-analytics/conversational-analytics-in-bigquery-now-ga |
| Conversational Analytics API（BigQuery/Looker/Data Studio 通用） | 产品/框架 | 面向开发者的 API，用自然语言问答结构化数据，支持 BigQuery、Looker、Data Studio 多数据源 | 2025 (Next 25 发布) - 持续更新 | https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/overview |
| Gemini in Looker / Looker Conversational Analytics | 产品 | 基于 LookML 语义层的自然语言 Explore 查询，可定制数据代理跨最多5个 Explore 查询，自动生成 Slides 摘要 | 2025 (Next 25 起，逐步扩展至全平台) | https://cloud.google.com/blog/products/data-analytics/gemini-in-looker-deep-dive |
| Databricks × Anthropic 战略合作 | 产品/合作 | 将 Claude 模型直接引入 Databricks 数据智能平台，10000+企业可构建对其专有数据推理的 agent | 2025-03 | https://www.databricks.com/company/newsroom/press-releases/databricks-and-anthropic-sign-landmark-deal-bring-claude-models |
| Anthropic 内部 Agentic Analytics 实践（Claude Code + 语义层） | 其他/工程实践 | Anthropic 披露用 Claude Code 连接数据库产出分析报告，通过语义层+evals 将业务分析查询自动化率提升至95%，准确率约95%（此前仅21%） | 2025-2026 | https://medium.com/@joparga3/anthropic-is-telling-you-that-agentic-analytics-is-not-just-text-to-sql-ce605454bbc9 |
| Snowflake × Anthropic 合作（Cortex 上部署 Claude） | 产品/合作 | Snowflake 与 Anthropic 达成2亿美元级合作，将 Claude 引入 Snowflake Cortex 驱动企业级 agentic AI | 2025 | https://www.hpcwire.com/bigdatawire/this-just-in/snowflake-and-anthropic-announce-200m-partnership-to-bring-agentic-ai-to-global-enterprises/ |
| OpenAI Deep Research（MCP 数据连接器更新） | 产品 | ChatGPT Deep Research 更新至 GPT-5.2 基座，支持通过 MCP servers 连接更多数据源生成研究报告（非专用 text-to-SQL 产品，但与 data agent 广义相关） | 2026-02 | https://en.wikipedia.org/wiki/ChatGPT_Deep_Research |

## 备注
- 未找到 OpenAI 官方发布的专用企业级 text-to-SQL / 对话式数据分析产品（类似 Cortex Analyst / Genie / Fabric Data Agent）；OpenAI 在该领域主要以底层模型（GPT-5系列）+ MCP 生态被第三方（如 CData Connect AI）集成，未列为独立候选产品，仅记录 Deep Research 更新供参考。
- Anthropic 同理，未发布独立 data-agent 产品，而是通过与 Databricks / Snowflake 的模型合作 + 官方工程博客披露的内部实践进入该领域，已在候选中注明为"合作/实践"类型。
