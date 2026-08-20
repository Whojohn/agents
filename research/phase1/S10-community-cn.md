# S10 中文社区广度调研 (text2sql / ChatBI / 数据 Agent)

调研日期：2026-08-20（时效约束：仅收 2025-01 之后活跃条目，2025 前条目仅在仍是主流时收录并注明）

## 执行路径
- WebSearch: "text2sql 2025 知乎" — 发现 XiYan-SQL/M-Schema、SuperChatBI、Spider 2.0 中文讨论
- WebSearch: "ChatBI 2025 大模型" — 观远ChatBI、有数ChatBI、FreeWheel ChatBI
- WebSearch: "数据分析 Agent 2025 开源" — 积木报表JimuChatBI、通用Agent框架(LangGraph/CrewAI，非本渠道重点)
- WebSearch: "NL2SQL 实践 2025 大模型 落地" — 商业银行NL2SQL综述
- WebSearch: "机器之心 text2sql agent 2025" — Tool-SQL、Chat2DB、DataFunSummit 2025
- WebSearch: "量子位 数据分析 Agent 2025" — 量子位智库趋势报告、瓴羊白皮书线索
- WebSearch: "DB-GPT 2025 更新 text2sql" — DB-GPT-Hub、Awesome-Text2SQL
- WebSearch: "M-Schema NL2SQL 论文 知乎" — XiYan-SQL 框架细节
- WebSearch: "阿里 蚂蚁 腾讯 字节 text2sql 智能问数 2025" — 字节 Data Agent 线索
- WebSearch: "掘金 NL2SQL Agent 大模型 2025"
- WebSearch: "SuperSonic 腾讯 开源 语义层 text2sql" — 腾讯音乐 SuperSonic
- WebSearch: "帆软 智能问数 大模型 2025" — 帆软FineBI AI
- WebSearch: "天池 CCKS text2sql 评测 2025" — 未发现专门2025评测，转向其他渠道
- WebSearch: "Chat2DB 开源 GitHub 2025 AI"
- WebSearch: "袋鼠云 有数 ChatBI 大模型 智能问数"
- WebSearch: "开源 text2sql 项目 GitHub 中文 2025 star"
- WebSearch: "MCP 数据库 text2sql 开源 2025" — MCP+数据库新范式(多篇)
- WebSearch: "瓴羊 数据分析Agent白皮书 2025" — 瓴羊白皮书详情
- WebSearch: "XiYanSQL 2025 更新 通义" — XiYan-MCP-server, XiYanSQL-QwenCoder-2504, CRITIC
- WebSearch: "SQLBot 开源 数据问答 Agent" — DataEase/飞致云 SQLBot (2025-08开源)
- WebSearch: "DeepSeek 数据分析 Agent 开源 2025" — DeepSeek-V3.2/V4 Agent能力
- WebSearch: "华为 GaussDB 智能问数 text2sql 2025" — 未发现直接相关产品，跳过
- WebSearch: "析言GBI 阿里云 智能问数" — 阿里云百炼 析言GBI 产品细节
- WebSearch: "BIRD-CN 中文 text2sql 基准 数据集" — BIRD为国际基准，无独立中文版
- WebSearch: "SuperCLUE 数据分析 Agent 榜单 2025" — SuperCLUE-Agent 基准
- WebSearch: "Vanna.ai 中文 text2sql RAG 知乎" — Vanna 中文社区讨论(项目本身非中文渠道原创)
- WebSearch: "观远数据 ChatBI DeepSeek 2025 升级"
- WebSearch: "CSDN Text2SQL Agent 框架 2025 开源项目 推荐"
- WebSearch: "Text2Sql.Net GitHub MCP 开源项目" — 未确认为独立活跃中文项目，不收录
- WebSearch: "字节跳动 Data Agent 宽表 NL2SQL 火山引擎" — 火山引擎 Data Agent (2026-04发布)
- WebSearch: "Coze 工作流 text2sql 智能体 案例" — Coze/Dify 工作流版 Text2SQL 实践案例(信贷风控)
- WebFetch 尝试: realworld-ai.io/zh/arena/10-nl2sql (403，未获取到内容)
- WebFetch 尝试: zhihu.com/p/1982406887027786390 "Data Agent厂商测评" (503，未获取到内容，仅保留搜索摘要信息)

## 候选

| 名称 | 类型 | 一句话描述 | 日期 | URL |
|---|---|---|---|---|
| XiYan-SQL / XiYanSQL-QwenCoder（析言，阿里通义） | 开源模型/框架 | 阿里提出的 M-Schema + 多生成器集成 NL2SQL 框架，持续发布 3B/7B/14B/32B 系列模型并在 BIRD/Spider 刷榜 | 2025-02～2025-05 持续更新 | https://github.com/XGenerationLab/XiYan-SQL |
| XiYan-MCP-server | 框架 | 为 XiYanSQL 提供的 MCP 服务端，支持本地(PC/Mac)与云端调用 | 2025-03 | https://github.com/XGenerationLab (相关仓库) |
| 析言GBI（阿里云百炼） | 产品 | 基于通义大模型的原生数据分析助理，多智能体架构做NL2SQL+分析+可视化，在中国一汽等落地准确率92.5% | 2024-2025持续迭代 | https://help.aliyun.com/zh/model-studio/xiyan-gbi/ |
| SQLBot（DataEase/飞致云） | 开源项目 | 基于大模型+RAG的智能问数(ChatBI)系统，开箱即用、可被Dify/Coze/MaxKB集成，开源后迅速破1500 star | 2025-08 | https://github.com/dataease/SQLBot |
| SuperSonic（腾讯音乐开源） | 开源框架 | 融合 ChatBI(大模型)与 Headless BI(语义层) 的新一代 AI+BI 平台，中文社区持续讨论 | 2024年开源，2025年仍活跃 | https://github.com/tencentmusic/supersonic |
| Chat2DB | 开源项目/产品 | AI驱动的通用数据库工具与SQL客户端，支持NL2SQL、SQL转自然语言、SQL优化，40+数据库 | 持续更新至2025 | https://github.com/chat2db/Chat2DB |
| DB-GPT-Hub（Eosphoros AI） | 开源框架 | Text2SQL端到端微调框架及基准测试套件，支持Qwen/Llama/Baichuan/ChatGLM等 | 持续更新 | https://github.com/eosphoros-ai |
| Awesome-Text2SQL | 开源项目(资源合集) | DB-GPT社区维护的Text2SQL/Text2DSL/Text2API/Text2Vis中英文资源合集 | 持续更新 | https://github.com/eosphoros-ai/Awesome-Text2SQL |
| 观远ChatBI（观远数据） | 产品 | 商业BI产品完成DeepSeek-R1适配升级，强调复杂查询与跨表分析准确率与成本优化 | 2025-02 | https://zhuanlan.zhihu.com/p/1917994366355629764 |
| 有数ChatBI（袋鼠云） | 产品 | 大模型驱动的数据分析产品，落地重庆烟草(15分钟→10秒)、高校场景，强调多轮问数 | 2025-01 | https://zhuanlan.zhihu.com/p/23069870146 |
| SuperChatBI（东尔科技/Doer Tech） | 产品 | 面向金融BI的智能问数系统，完成DeepSeek-R1模型升级 | 2025 | https://zhuanlan.zhihu.com/p/23259319867 |
| FreeWheel ChatBI | 产品实践 | 视频广告数据分析场景的大模型ChatBI落地案例，InfoQ深度拆解 | 2025 | https://www.infoq.cn/article/zn5fv8qxoncytiaumglo |
| 网易数帆ChatBI | 产品/方案 | 网易数帆的ChatBI与领域模型结合方案 | 2025-05 | https://www.53ai.com/news/zhinenghuagaizao/2025052907418.html |
| 帆软FineBI AI智能问答助手 | 产品 | 国产BI厂商基于大模型推出自然语言分析与智能分析建议能力，登顶2025 AI Cloud 100 China Insight赛道 | 2025 | https://www.finebi.com/blog/article/68b0015928946ecca8945740 |
| 瓴羊《2025数据分析Agent白皮书》 | 报告/榜单类 | 阿里云智能集团旗下瓴羊发布，系统梳理数据分析Agent技术架构与行业落地实践 | 2025-12 | https://www.geekpark.net/news/358158 |
| 火山引擎 Data Agent（字节跳动） | 产品 | 字节火山引擎推出的企业级AI数据专家，NL2SQL为执行核心，叠加NL2Semantics与Multi-Agent决策执行 | 2026-04（发布），持续演进文章至2025-2026 | https://www.cnblogs.com/bytedata/p/18818520 |
| 积木报表 JimuChatBI | 开源项目 | 免费开源的对话式智能数据分析产品，自然语言问表无需写SQL，支持企业级权限控制 | 2025年社区讨论活跃 | (国内开源社区，需进一步核实官方仓库) |
| Tool-SQL | 论文/框架 | 基于LLM+Agent的Text2SQL方案，集成数据库索引器、错误检测器做迭代校验 | 2024年末-2025年讨论延续 | https://www.53ai.com/news/zhinenghuagaizao/2024092535091.html |
| SuperCLUE-Agent | 基准/榜单 | 中文大模型Agent能力测评基准，含工具使用/复杂任务能力评测，定期更新 | 持续更新至2025 | https://www.cluebenchmarks.com/superclue_agent.html |
| MCP+数据库(Text2SQL) 技术范式 | 其他(技术趋势) | 2025年中文社区兴起的用MCP协议桥接大模型与数据库做Text2SQL的新模式，多个开源实现(focus_mcp_sql等) | 2025 | https://www.cnblogs.com/datafuntalk/p/18829322 |
| "Data Agent全景扫描"（知乎综述） | 其他(综述) | 从NL2SQL到自主数据智能体的行业全景梳理文章，覆盖多家厂商产品路线 | 2025-2026 | https://zhuanlan.zhihu.com/p/2028396139871760917 |
| Coze/Dify 工作流版 Text2SQL 案例(信贷风控) | 其他(实践案例) | 用Coze/Dify工作流实现四层架构(理解-增强-生成-校验)的Text2SQL风控策略场景 | 2025 | https://zhuanlan.zhihu.com/p/1912682006585775173 |
| DeepSeek-V3.2 / V4 Agent能力增强 | 模型 | DeepSeek新版本强化Agent与推理能力，中文社区讨论其在数据分析类任务上的应用潜力 | 2025-12 (V3.2)，2026 (V4预览) | https://api-docs.deepseek.com/news/news251201/ |
| "2025 AI数据分析工具/Data Agent厂商测评与选型指南"（知乎） | 榜单 | 对比多家Data Agent/ChatBI厂商产品的测评与选型指南文章 | 2025 | https://zhuanlan.zhihu.com/p/1982406887027786390 |
