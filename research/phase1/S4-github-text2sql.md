# S4 GitHub 渠道调研：Text-to-SQL 开源项目与开源微调模型

## 执行路径
- WebSearch: "text2sql github 2025 open source project stars" — 看 GitHub Topics 页、Awesome-Text2SQL、eosphoros-ai 相关仓库
- WebSearch: "nl2sql github repository 2025 active" — 看 nl2sql topic 页、NL2SQL_Handbook
- WebSearch: "SQLCoder XiYan-SQL github 2025 update release" — 确认 XiYan-SQL 2025 全年多次发版
- WebSearch: "huggingface text-to-sql model 2025 finetuned" — 看 HF text-to-sql 模型列表
- mcp__github__search_repositories: `text2sql in:name,description,topics stars:>500` sort=stars — 拿到 WrenAI/SQLBot/DB-GPT-Hub 等星数与更新时间
- mcp__github__search_repositories: `nl2sql in:name,description,topics stars:>200` sort=stars — 补充 QueryWeaver、awesome-data-agents、Agentar-Scale-SQL 等
- mcp__github__search_repositories: `text-to-sql in:name,description,topics stars:>300` sort=updated — 结果超长未展开使用（已从其他查询获得足够信息）
- mcp__github__search_repositories: 逐个核实种子项目 `user:eosphoros-ai DB-GPT`、`user:vanna-ai vanna`、`user:defog-ai sqlcoder`、`user:XGenerationLab` — 确认 vanna 仓库已 archived，其余均活跃
- mcp__github__search_repositories: `repo:RUCKBReasoning/OmniSQL`、`repo:CycloneBoy/slm_sql`、`repo:Dataherald/dataherald` — 核实近期发现的新模型/项目活跃度
- WebSearch: ""OmniSQL" OR "CodeS" text-to-sql model github 2025" — 发现 OmniSQL(VLDB'25)、slm_sql、csc_sql、SIRIUS-SQL、ExeSQL、Reward-SQL 等新论文/仓库线索
- WebSearch: "dataherald chat2db text2sql github 2025 activity" — 核实 Dataherald / Chat2DB 现状
- WebSearch: "CodePhiliaX Chat2DB github stars 2025 2026" — 确认 Chat2DB 星数与最近 release
- WebSearch: "vanna-ai archived 2026 alternative text2sql successor" — 确认 vanna 于 2026-03-29 被 archive（此前 2025 底发布过 Vanna 2.0 重写），生态转向商业化/其他替代品
- WebFetch: https://huggingface.co/models?other=text-to-sql&sort=created — 看最新创建的 text-to-sql 模型（多为长尾个人微调，信号有限，仅作为 HF 侧参考）
- 关键页面：github.com/topics/text-to-sql, github.com/topics/nl2sql, github.com/eosphoros-ai/Awesome-Text2SQL, github.com/DEEP-PolyU/Awesome-LLM-based-Text2SQL, github.com/XGenerationLab/XiYan-SQL, github.com/vanna-ai/vanna/releases

## 候选

| 名称 | 类型 | 一句话描述 | 日期 | URL |
|---|---|---|---|---|
| Canner/WrenAI | 开源项目 | GenBI 开源治理型 text-to-SQL 平台，接 20+ 数据源生成可信仪表盘/图表/SQL，17.3k星，2026-08持续活跃更新 | 2024-03创建，持续活跃 | https://github.com/Canner/WrenAI |
| dataease/SQLBot | 开源项目 | 基于大模型+RAG的中文智能问数/对话式BI系统，6.6k星，2025-04创建后增长极快，仍高频更新 | 2025-04起 | https://github.com/dataease/SQLBot |
| eosphoros-ai/DB-GPT | 开源项目/框架 | 由text2sql项目演进的开源智能体式AI数据助理，19.7k星，持续活跃 | 2023创建，2025+持续活跃 | https://github.com/eosphoros-ai/DB-GPT |
| eosphoros-ai/DB-GPT-Hub | 开源项目 | DB-GPT配套的text2SQL模型微调/数据集仓库，2k星，2025年内持续更新 | 持续活跃 | https://github.com/eosphoros-ai/DB-GPT-Hub |
| vanna-ai/vanna | 开源项目(已归档) | 曾是最主流的开源text2sql RAG库(2.4万星)，2025底发布Vanna 2.0重写版，但2026-03-29仓库被archive，需在深读时确认其商业化走向 | 2025底2.0，2026-03归档 | https://github.com/vanna-ai/vanna |
| defog-ai/sqlcoder | 模型/开源项目 | SOTA开源text-to-SQL LLM家族，4k星，仓库至2026-08仍有更新 | 持续活跃 | https://github.com/defog-ai/sqlcoder |
| XGenerationLab/XiYan-SQL | 框架 | 阿里多生成器集成(ensemble)text2sql框架，BIRD等榜单SOTA，1k星，2025年多次迭代(含CRITIC技术) | 2025全年活跃 | https://github.com/XGenerationLab/XiYan-SQL |
| XGenerationLab/XiYanSQL-QwenCoder | 模型 | XiYanSQL系列开源模型(3B/7B/14B/32B)，2025-02/03/04多次发版更新 | 2025-02至2025-04+ | https://github.com/XGenerationLab/XiYanSQL-QwenCoder |
| XGenerationLab/xiyan_mcp_server | 框架 | XiYanSQL配套的自然语言查数据库MCP Server，2025-03创建，持续更新 | 2025-03起 | https://github.com/XGenerationLab/xiyan_mcp_server |
| RUCKBReasoning/OmniSQL | 模型/论文 | VLDB'25论文配套，SynSQL-2.5M百万级合成数据集+7B/14B/32B开源text2sql模型 | 2025-02创建，2026-08仍更新 | https://github.com/RUCKBReasoning/OmniSQL |
| Snowflake/Arctic-Text2SQL-R1-7B | 模型 | Snowflake用GRPO+执行反馈奖励训练的7B text2sql模型 | 2025-05发布 | https://huggingface.co/Snowflake/Arctic-Text2SQL-R1-7B |
| CycloneBoy/slm_sql | 模型/论文 | 探索小语言模型(SLM)做text-to-SQL的开源实现 | 2025-07创建，2026-07仍更新 | https://github.com/CycloneBoy/slm_sql |
| antgroup/Agentar-Scale-SQL | 框架 | 蚂蚁集团开源，利用可扩展计算(test-time scaling)提升text2sql性能的框架 | 2025-09创建，持续活跃 | https://github.com/antgroup/Agentar-Scale-SQL |
| FalkorDB/QueryWeaver | 开源项目 | 图数据库驱动的schema理解text2sql工具 | 2025-07创建，活跃 | https://github.com/FalkorDB/QueryWeaver |
| zhongyu09/openchatbi | 开源项目 | 基于LangGraph/LangChain的对话式BI智能体，含nl2sql能力 | 2025-09创建，活跃 | https://github.com/zhongyu09/openchatbi |
| apconw/Aix-DB | 开源项目 | LangChain/LangGraph+MCP多智能体协作的自然语言到数据洞察系统 | 2024创建，2025+活跃迭代 | https://github.com/apconw/Aix-DB |
| Dataherald/dataherald | 开源项目 | 企业级自然语言到SQL问答引擎，3.6k星，2026-08仍更新 | 持续活跃 | https://github.com/Dataherald/dataherald |
| CodePhiliaX/Chat2DB | 开源项目/产品 | AI驱动的通用数据库SQL客户端+text2sql，约25.6k星，社区活跃(需核实近期release节奏) | 持续活跃(注:release频率待核实) | https://github.com/CodePhiliaX/Chat2DB |
| hexinfo/dat | 开源项目/框架 | 基于数据建模+语义模型的自然语言问数(chatBI/text2sql)框架 | 2025-07创建，活跃 | https://github.com/hexinfo/dat |
| HKUSTDial/NL2SQL_Handbook | 其他(资源手册) | 持续更新的text-to-SQL技术追踪手册，1.6k星 | 持续活跃 | https://github.com/HKUSTDial/NL2SQL_Handbook |
| DEEP-PolyU/Awesome-LLM-based-Text2SQL | 论文/榜单 | TKDE2025综述论文配套的LLM-based text2sql资源大全 | 2025-09创建，活跃 | https://github.com/DEEP-PolyU/Awesome-LLM-based-Text2SQL |
| HKUSTDial/awesome-data-agents | 榜单 | "Data Agents综述"论文配套资源列表，覆盖text2sql等更广的数据智能体范畴 | 2025-08创建，活跃 | https://github.com/HKUSTDial/awesome-data-agents |
| didilili/shopkeeper-agent | 开源项目 | 电商数仓智能问数Agent实战教程项目(LangGraph+NL2SQL全栈) | 2026-04创建，活跃 | https://github.com/didilili/shopkeeper-agent |
| jeecgboot/jimureport | 产品/开源项目 | 中文对话式BI报表生成产品JimuChatBI，一句话生成报表/数据大屏(含text2sql) | 8.2k星，持续活跃 | https://github.com/jeecgboot/jimureport |
