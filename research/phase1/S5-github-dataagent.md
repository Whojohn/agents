# S5 - GitHub 渠道:Data Agent / SQL Agent 广度调研

日期:2026-08-20

## 执行路径
- WebSearch: `"data agent" github repository 2025 open source stars`
- WebFetch: https://github.com/topics/data-agent (逐条查看仓库列表)
- WebSearch: `"SQL agent" github repo 2025 text-to-sql agent framework`
- WebSearch: `"data analysis agent" OR "AI data analyst" github open source 2025 2026`
- WebFetch: https://github.com/topics/sql-agent
- WebFetch: https://github.com/topics/text-to-sql?o=desc&s=updated
- WebSearch: `Vanna AI OR "DB-GPT" OR dataherald OR defog OR waii github stars 2025 activity`
- WebFetch: https://getnao.io/blog/open-source-analytics-agent-builder-playbook/ (2026年开源分析agent对比文章)
- WebSearch: `eosphoros-ai DB-GPT github stars 2025 2026 active`
- WebSearch: `"awesome data agent" OR "awesome text-to-sql" github list 2025`
- WebSearch: `WrenAI github stars 2025 2026 canner`
- WebSearch: `PandasAI github 2025 2026 active development stars`
- 未使用 gh CLI(环境未安装,认证也不可用),全部通过 WebSearch/WebFetch 完成

## 候选

| 名称 | 类型 | 一句话描述 | 日期 | URL |
|---|---|---|---|---|
| Canner/WrenAI | 开源项目/产品 | 开源 GenBI 引擎,治理化 text-to-SQL + 语义层,支持20+数据源生成仪表盘,~17.3k star,持续活跃 | 持续迭代(2025-2026) | https://github.com/Canner/WrenAI |
| eosphoros-ai/DB-GPT | 开源项目/框架 | 面向"AI+数据"下一代产品的开源 agentic 数据助手,~19k star,2025年仍有版本发布 | 持续迭代 | https://github.com/eosphoros-ai/DB-GPT |
| sinaptik-ai/PandasAI(pandas-ai) | 开源项目 | 对话式数据分析工具,基于LLM+RAG让用户"聊数据",~23.8k star,2025年10月仍有更新 | 持续迭代 | https://github.com/sinaptik-ai/pandas-ai |
| Vanna AI | 开源项目/框架 | 开源 text-to-SQL 框架(RAG方式生成SQL),~21.5k star,是该类目长期主流项目之一 | 2023年起,2025年仍主流 | https://github.com/vanna-ai/vanna |
| FireBird-Technologies/Auto-Analyst | 开源项目 | 基于DSPy的模块化多agent数据科学平台,可做数据清洗/统计检验/建模 | 活跃 | https://github.com/FireBird-Technologies/Auto-Analyst |
| zjunlp/DataMind | 论文+开源项目 | 开源LLM数据分析agent,论文被ICLR/AAAI/KDD 2026接收,含技能发现框架诊断LLM数据分析短板 | 2025-2026 | https://github.com/zjunlp/DataMind |
| agno-agi/dash (Agno Dash) | 开源项目/框架 | 自学习SQL agent,六层上下文架构,能从历史运行中自动纠错学习,~1.7k star | 2025-2026活跃 | https://github.com/agno-agi/dash |
| getnao/nao | 开源项目 | 面向分析场景的"上下文工程"agent,原生dbt集成+评测框架+治理控制,~610 star | 2025-2026活跃 | https://github.com/getnao/nao |
| HKUSTDial/DeepEye | 开源项目/论文 | "自主数据agent系统",港科大团队研究项目,~230 star | 2025 | https://github.com/HKUSTDial/DeepEye |
| OpenDCAI/DataFlow | 开源项目/框架 | 基于最新LLM的数据准备算子与pipeline框架,~7.6k star | 活跃 | https://github.com/OpenDCAI/DataFlow |
| tianlan-ltd/Magic-Insight | 开源项目 | 一站式数据智能agent,可从文档/数据库/图片中挖掘洞察,~545 star | 2025 | https://github.com/tianlan-ltd/Magic-Insight |
| Text2SqlAgent/text2sql-framework | 框架 | 极简agentic text-to-SQL SDK,只给LLM一个execute_sql工具,让其自主探索schema/自我纠错,无需RAG/语义层,Spider 80表20/20 | 2025 | https://github.com/Text2SqlAgent/text2sql-framework |
| db-agent/db-agent | 开源项目/产品 | 面向生产环境的text-to-SQL agent,适配Databricks/Snowflake/AWS,含安全护栏,一键部署 | 2025 | https://github.com/db-agent/db-agent |
| antgroup/Agentar-Scale-SQL | 论文/框架 | 蚂蚁集团出品,通过可扩展计算(scaling)显著提升Text-to-SQL在高难度基准上的表现 | 2025 | https://github.com/antgroup/Agentar-Scale-SQL |
| Snowflake-Labs/ReFoRCE | 论文/框架 | Snowflake出品的text-to-SQL agent,自精炼+格式约束+列探索,登顶Spider 2.0榜单 | 2025 | https://github.com/Snowflake-Labs/ReFoRCE |
| wbbeyourself/MAC-SQL | 论文/框架 | 多智能体协作text-to-SQL框架(Selector/Decomposer/Refiner三agent),COLING 2025收录,社区常引用 | 2025年论文收录,项目持续维护 | https://github.com/wbbeyourself/MAC-SQL |
| CoRAL-ASU/weaver | 论文/开源项目 | 模块化agentic pipeline,结合SQL执行与LLM做表格问答,EMNLP 2025 | 2025 | https://github.com/CoRAL-ASU/weaver |
| dataease/SQLBot | 开源项目/产品 | 基于LLM+RAG的智能问答系统(NL2SQL方向),~6.6k star | 活跃 | https://github.com/dataease/SQLBot |
| zhongyu09/openchatbi | 开源项目 | 基于自然语言到SQL的智能对话式BI工具,~624 star | 2025 | https://github.com/zhongyu09/openchatbi |
| OtterMind/Chat2DB | 开源项目/产品 | 跨平台数据库客户端+SQL工作台,支持40+数据库,AI辅助生成查询,~28k star,长期主流且持续更新 | 长期项目,2025仍主流迭代 | https://github.com/OtterMind/Chat2DB |
| eosho/langchain_data_agent | 开源项目 | 基于LangGraph的NL2SQL示例项目,自然语言提问返回SQL与结果,~234 star | 2025 | https://github.com/eosho/langchain_data_agent |
| SJTU-DMTai/Awesome-Data-Agent-Papers | 榜单 | LLM-based数据agent方向的论文/基准精选清单(数据准备/NL2SQL/表格推理/数据科学&AutoML agent) | 2025维护中 | https://github.com/SJTU-DMTai/Awesome-Data-Agent-Papers |
| DEEP-PolyU/Awesome-LLM-based-Text2SQL | 榜单/论文 | Text-to-SQL方向综述性精选列表,配套TKDE2025综述论文《Next-Generation Database Interfaces》 | 2025 | https://github.com/DEEP-PolyU/Awesome-LLM-based-Text2SQL |
| langchain-ai/langchain(SQL agent模块+deepagents text-to-sql示例) | 框架 | 通用agent框架内置SQL agent能力(create_sql_agent等)及deepagents下的text-to-sql-agent示例,作为"通用框架SQL能力"对照组 | 持续迭代 | https://github.com/langchain-ai/deepagents/tree/main/examples/text-to-sql-agent |
| YASSERRMD/schema-forge | 开源项目 | Rust编写的schema感知SQL编码agent,自动生成并执行查询,~8 star,规模小但代表个人开发者新尝试 | 2025 | https://github.com/YASSERRMD/schema-forge |

## 备注
- Chat2DB、Vanna AI、DB-GPT、PandasAI 属于2025年前已存在但2025-2026年仍是该类目主流/持续迭代的项目,按规则予以保留并注明。
- 已区分"专门数据分析/SQL agent项目"(WrenAI、DB-GPT、Agno Dash、nao、DataMind、Auto-Analyst等)与"通用agent框架内置SQL能力"(LangChain SQL agent模块)两类。
- LlamaIndex 的 NLSQLTableQueryEngine 也是通用框架SQL能力的代表,搜索中未找到2025年后针对该模块的独立活跃度证据,未单列,仅作为已知背景。
