# S9 - 英文社区渠道调研 (Hacker News / Reddit / 英文博客·Substack)

调研时间: 2026-08-20

## 执行路径
- WebSearch: `site:news.ycombinator.com "text to SQL" 2025`
- WebSearch: `site:news.ycombinator.com "text2sql" OR "data agent" Show HN 2025`
- WebSearch: `reddit text2sql 2025 LLM`
- WebSearch: `reddit r/dataengineering "text to sql" agent 2025`
- WebSearch: `site:reddit.com r/LocalLLaMA text-to-sql agent`（Reddit 结果被搜索引擎屏蔽，改用间接结果）
- WebSearch: `site:reddit.com r/MachineLearning text2sql OR "text-to-sql" 2025`（同上，Reddit 直接结果基本不可见）
- WebSearch: `site:news.ycombinator.com "Show HN" data agent SQL 2026`
- WebSearch: `"data agent" LLM database Show HN 2025 2026`
- WebSearch: `"WrenAI" OR "Wren AI" reddit OR "hacker news" 2025 text-to-sql`
- WebSearch: `"Snowflake Cortex Analyst" OR "Databricks Genie" reddit discussion accuracy 2025`
- WebSearch: `Substack "text-to-sql" evaluation hallucination blog 2025 2026`
- WebSearch: `"vanna.ai" OR "dataherald" reddit 2025 review`
- WebSearch: `"Text to SQL: Local, Secure, and Smarter" hacker news`
- WebSearch: `awesome-data-agents HKUSTDial github survey data agents 2026`
- WebSearch: `"text-to-sql is dead" blog post semantic layer`
- WebSearch: `reddit "LocalLLaMA" "text to sql" model fine-tune 2026`
- WebSearch: `Hex "Notebooks" OR "Julius AI" OR "Outerbase" text-to-sql agent reddit hacker news 2025`
- WebSearch: `llmsql-bench LLMSQL benchmark huggingface release date 2025`
- WebSearch: `WrenAI 14k stars 2026 GenBI release`
- WebFetch (HN Algolia API, 用于核对确切日期/标题): items 46890117, 47678048, 46350486, 45115616, 46547746, 46509568, 48052476, 45543132, 47802054, 45733525
- WebFetch: https://www.ashpreetbedi.com/articles/sql-agent （核实自我改进 SQL agent 项目内容）
- 备注: 直接的 Reddit 帖子 (r/LocalLLaMA, r/MachineLearning, r/dataengineering) 搜索引擎索引很弱，几乎拿不到可读的 reddit.com 帖子链接/内容，只能通过二手引用/新闻摘要间接确认社区讨论存在；HN 侧的 Show HN 与讨论帖覆盖较充分。

## 候选

| 名称 | 类型 | 一句话描述 | 日期 | URL |
|---|---|---|---|---|
| Kepler | 开源项目 | Show HN 上线的开源 text-to-SQL 平台，用自然语言查询数据仓库 | 2026-02-04 | https://news.ycombinator.com/item?id=46890117 (repo: https://github.com/stym06/kepler) |
| Dinobase | 开源项目 | 用 DuckDB + 带注解 schema 给 AI agent 暴露业务数据，作者称在 11 个模型上 SQL 方式比工具/MCP 方式准确率高 2-3 倍、token 效率高 16-22 倍 | 2026-04-07 | https://news.ycombinator.com/item?id=47678048 (repo: https://github.com/DinobaseHQ/dinobase) |
| Agent-data (CLI) | 开源项目 | 给 agent 提供实时结构化数据访问的命令行工具，Show HN 讨论热烈 | 2026-05-07 | https://news.ycombinator.com/item?id=48052476 (https://agent-data.dev/) |
| QueryWeaver (FalkorDB) | 开源项目 | 基于图语义层（graph semantic layer）做 Text2SQL，用图数据库理解业务实体关系而非塞满 prompt 的 schema | 首发 2025-09-03，后续帖 2026-01-06 | https://news.ycombinator.com/item?id=45115616 ；https://news.ycombinator.com/item?id=46509568 (repo: https://github.com/FalkorDB/QueryWeaver) |
| Self-Improving SQL Agent (Agno 作者博客) | 开源项目/博客 | 用"动态上下文检索 + 持续学习循环"（好查询变未来上下文、坏查询变规则）构建生产级自我改进 text2sql agent，作者是 Agno 框架维护者 | 2025-12-22 | https://news.ycombinator.com/item?id=46350486 (https://www.ashpreetbedi.com/articles/sql-agent) |
| DataFramer.ai — 合成 Text2SQL 数据生成 | 产品/博客 | 用 Claude Haiku 等小模型批量放大生成 text2sql 训练数据的实践博客，HN 讨论 | 2026-01-08 | https://news.ycombinator.com/item?id=46547746 (https://www.dataframer.ai/posts/amplifying-claude-haiku-text-to-sql/) |
| ThalamusDB | 开源项目 | 支持对文本/图片/音频做"AI 算子"的 SQL 引擎，Show HN 上线 | 2025-10-10 | https://news.ycombinator.com/item?id=45543132 (repo: https://github.com/itrummer/thalamusdb) |
| Valuepulse | 产品 | 用"context layer"统一建模业务域，支持自然语言生成 dashboard + 数据库查询 + 文档/网页统一搜索 | 2026-04-17 | https://news.ycombinator.com/item?id=47802054 (https://valuepulse.ai) |
| "Text-to-SQL is dead, long live text-to-SQL"（Exasol 博客） | 其他(博客/争议) | 争议性观点博客：认为纯 text-to-SQL 在强合规场景不可行，需要语义层配合，HN 62 分热烈讨论 | 2025-10-28 | https://news.ycombinator.com/item?id=45733525 (https://www.exasol.com/blog/text-to-sql-governance/) |
| dbt "Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update" | 基准/博客 | 用 GPT-5.3 Codex / Sonnet 4.6 重测，发现 text-to-SQL 准确率相比 GPT-4 时代从 32.7% 提升到 64.5%，但企业场景仍建议语义层 | 2026-04 | https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026 |
| "The 7-Table Fallacy: Why Text-to-SQL Isn't Enterprise AI"（Axius SDC Substack） | 其他(博客) | 批评类文章，引用 ACL2025 "Text-to-SQL Benchmarks for Enterprise Realities" 和 BIRD，指出纯 LLM 生成 SQL 在企业复杂 schema 下会"自信地生成错误结果" | 2025年内 | https://axiussdc.substack.com/p/the-7-table-fallacy-why-text-to-sql |
| "The Text-to-SQL Performance Cliff (2026)"（Medium, Vishal Mysore） | 其他(博客) | 讨论学术基准分数与企业生产可靠性之间存在"performance cliff"的实践文章 | 2026-03 | https://medium.com/@visrow/the-text-to-sql-performance-cliff-2026-why-natural-language-to-sql-breaks-a7281a23dbea |
| Datrics Text2SQL | 开源项目 | 开源高精度 RAG pipeline 做 schema 检索的 text2sql 工具，Show HN 上线 | 2025-03-20 | https://news.ycombinator.com/item?id=43424490 |
| WrenAI (Canner) | 开源项目 | 开源 GenBI agent：text-to-SQL + text-to-chart + 语义层，2026 年做了 Wren Engine 并入主仓库等大版本重构，GitHub star 数持续增长（约17k+） | 持续迭代至2026-05 | https://github.com/Canner/WrenAI |
| LLMSQL Benchmark (LLMSQL/llmsql-benchmark) | 基准 | 对 WikiSQL 现代化、清洗、扩展后的新 text-to-SQL 评测基准，ICDMW 2025 论文配套，2026年发布2.0版本并上线排行榜 | 论文2025，v2.0 2026-02，CLI/排行榜 2026-03 | https://github.com/LLMSQL/llmsql-benchmark ；https://llmsql.github.io/llmsql-benchmark/ |
| Awesome-LLM-based-Text2SQL (DEEP-PolyU) | 榜单 | TKDE2025 综述配套的社区维护 text2sql 论文/基准/开源项目资源合集仓库 | 2025年内持续更新 | https://github.com/DEEP-PolyU/Awesome-LLM-based-Text2SQL |
| awesome-data-agents (HKUSTDial) | 榜单 | 论文《A Survey of Data Agents: Emerging Paradigm or Overstated Hype?》配套的持续更新 data agent 论文清单，社区关注度高 | 论文2025-10，仓库持续更新 | https://github.com/HKUSTDial/awesome-data-agents |
| PremSQL | 开源项目 | 面向本地/隐私敏感场景的开源 text-to-SQL 库，用小模型构建端到端本地方案 | 2025年内活跃迭代 | https://pypi.org/project/premsql |
| Snowflake Cortex Analyst vs Databricks Genie | 产品 | 两大云厂商的对话式 BI/text-to-SQL 产品持续在社区被拿来对比准确率与治理能力，2026年多篇对比文章 | 2025 Summit 发布，2026年持续对比讨论 | https://colrows.com/blogs/cortex-analyst-vs-genie/ |
| Vanna (Vanna AI) | 开源项目 | 开源 RAG 式 text-to-SQL 框架，2025年发布 Vanna 2.0，社区评价活跃 | 2025年内 | https://vanna.ai/ (仓库: https://github.com/vanna-ai/vanna) |
| Dataherald | 开源项目 | 面向企业问答场景的开源自然语言转SQL引擎，持续被社区拿来与 Vanna 等对比 | 持续迭代 | https://github.com/Dataherald/dataherald |
| "AI Agents and the Pesky Problem of Data"（Joe Reis Substack） | 其他(博客) | 知名数据工程作者 Joe Reis 对"AI agent 直接查数据库"路线的实践反思博客 | 2025年内 | https://joereis.substack.com/p/ai-agents-and-the-pesky-problem-of |
| "Text-to-SQL Agents: Insights On How AI Builders Evaluate Accuracy & Avoid Hallucinations"（neurlcreators Substack） | 其他(博客) | 从业者视角总结的 text-to-SQL agent 评测方法与防幻觉实践（metadata驱动schema选择、few-shot、检索式方法） | 2025年内 | https://neurlcreators.substack.com/p/text-to-sql-agents-challenges |
