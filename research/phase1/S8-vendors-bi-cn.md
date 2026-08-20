# S8 - 传统BI厂商 + 国内厂商 ChatBI/Data Agent 广度调研

## 执行路径
- WebSearch: `Tableau AI Agent 2026 text to SQL "Tableau Next"` → help.tableau.com, salesforce.com/news (Tableau Agentic Analytics Platform)
- WebSearch: `Salesforce Agentforce data analytics agent 2025 2026 text to SQL` → salesforce.com/blog/text-to-sql-agent, cio.com (Waii收购)
- WebSearch: `Qlik AI Agent ChatBI 2025 2026 announcement` → qlik.com新闻室, klarmetrics.com, bix-tech.com
- WebSearch: `ThoughtSpot Spotter AI agent 2025 2026 text to SQL` → thoughtspot.com/product/spotter-semantics, techtarget.com
- WebSearch: `Strategy (MicroStrategy) AI Auto agent 2025 2026 natural language query` → strategy.com/software/news, techtarget.com
- WebSearch: `SAP Joule data agent 2025 2026 natural language analytics` → community.sap.com, leverx.com
- WebSearch: `Salesforce acquires Waii date 2026 text-to-SQL Agentforce` → salesforce.com news稿, cxtoday.com (确认完成收购日期 2025-08-15)
- WebSearch: `阿里云 ChatBI text2SQL 2025 数据 Agent 发布` → developer.aliyun.com, help.aliyun.com (ChatBI on DMS, PolarDB Data-Agent)
- WebSearch: `蚂蚁 数据 Agent Text2SQL 2025 2026 发布` → view.inews.qq.com, blog.csdn.net, sina.com.cn (Agentar-Scale-SQL 登顶BIRD)
- WebSearch: `百度 ChatBI 数据智能体 2025 text2sql 发布` → 未找到百度官方专属产品的强信号
- WebSearch: `百度析言GBI 2025 数据分析 大模型` → 未确认到"析言GBI"为百度产品的独立强信号
- WebSearch: `百度智能云 千帆 数据分析Agent 2025 发布` → sina.com.cn, stcn.com (千帆数据智能平台/Agent Infra，2025-2026)
- WebSearch: `腾讯 ChatBI 数据分析Agent 2025 2026` → cloud.tencent.com/developer, sohu.com (腾讯云BI ChatBI，OlaChat)
- WebSearch: `字节跳动 火山引擎 ChatBI 数据Agent text2sql 2025` → cnblogs.com/bytedata (火山引擎 Data Agent 2025-04-08发布)
- WebSearch: `帆软 FineBI AI GPT 数据分析 2025 2026 发布` → zhihu.com (FineBI 7.0)，gongke.net (FineChatBI)
- WebSearch: `观远数据 ChatBI Agent 2025 2026 发布` → zhihu.com (入选2025全球企业级AI Agent优秀厂商图谱)，guandata.com
- WebSearch: `Kyligence AI 数据智能体 text2sql 2025 2026` → blog.csdn.net (2025年1月亮相DC·AI生态创新中心)
- WebSearch: `衡石科技 HENGSHI SENSE Agent 2025 2026 AI数据分析` → hengshi.com/blog (SENSE 6.0/6.2, Data+AI Agent架构)
- WebFetch: `https://www.sohu.com/a/1054173632_122297451` (2026企业Data Agent平台选型评测，8款主流产品横评) → 补充发现 网易有数、九数云(帆软)、Power BI Copilot、衡石

## 候选

| 名称 | 类型 | 一句话描述 | 日期 | URL |
|---|---|---|---|---|
| Tableau Agent / Agentic Analytics Platform (Tableau Next) | 产品 | Salesforce旗下Tableau推出的生成式AI对话分析代理，跨Cloud/Server/Desktop/Next，2026年7月扩展到Dashboards | 2025-2026持续迭代 | https://www.salesforce.com/news/stories/tableau-agentic-analytics-platform-announcement/ |
| Salesforce Horizon Agent | 产品 | Salesforce内部text-to-SQL AI agent，2024-08 Early Access，2025-01 GA | 2025-01 GA | https://www.salesforce.com/blog/text-to-sql-agent/ |
| Salesforce收购Waii | 收购/技术 | Salesforce收购NL-to-SQL平台Waii，整合进Data Cloud/Agentforce/Tableau语义引擎 | 2025-08-15完成收购 | https://www.cio.com/article/4037742/salesforce-to-acquire-waii-to-enhance-sql-analytics-in-agentforce.html |
| Qlik 数据 Agent 组合 (Qlik Answers等) | 产品 | Qlik Cloud推出Agentic experience私有预览，2026年演变为多Agent组合(预测/工作流/内容构建/监控) | 2025-12私有预览，2026扩展 | https://www.qlik.com/us/news/company/press-room/press-releases/qlik-debuts-agentic-experience |
| Qlik MCP Server | 产品 | Qlik正式GA的MCP服务器，让第三方AI应用接入Qlik数据做决策支持 | 2026-02-10 GA | https://klarmetrics.com/qlik-agentic-ai-2026/ |
| ThoughtSpot Spotter | 产品 | ThoughtSpot对话式AI分析师，用patented search-token架构而非直接LLM生成SQL | 2024-11发布，持续迭代 | https://www.thoughtspot.com/product/agents |
| ThoughtSpot Spotter Semantics | 产品 | ThoughtSpot新发布的agentic语义层，将agent意图编译为确定性SQL | 2026-03-12 | https://www.globenewswire.com/news-release/2026/03/12/3254770/0/en/ThoughtSpot-Introduces-Spotter-Semantics-to-Bring-Trust-and-Context-to-Enterprise-AI.html |
| ThoughtSpot Spotter Agents (Viz/Model/Code) | 产品 | Spotter系列细分agent(SpotterViz/SpotterModel/SpotterCode)，2026年初GA | 2026年初GA | https://www.techtarget.com/searchbusinessanalytics/news/366636078/ThoughtSpot-automates-full-platform-with-new-Spotter-agents |
| Strategy (MicroStrategy) Auto / Auto Answers | 产品 | MicroStrategy自然语言BI机器人，支持自由提问获取治理数据答案，2025年增加个性化能力 | 2025-01-30更新 | https://www.strategy.com/software/news/microstrategy-delivers-rapid-value-from-ai-through-personalized-experiences-with-latest-release_01-30-2025 |
| SAP Joule Analytical Insights | 产品 | SAP Joule集成SAP Analytics Cloud能力，自然语言查询转实时洞察 | 2025 Q1受控发布，Q2 GA | https://community.sap.com/t5/technology-blog-posts-by-sap/introducing-analytical-insights-in-joule-empowering-smarter-decisions/ba-p/14083673 |
| 阿里云 ChatBI on DMS | 产品 | 阿里云DMS推出的ChatBI，自研大小模型融合方案保障NL2SQL准确率 | 2025持续迭代 | https://help.aliyun.com/zh/document_detail/3013002.html |
| 阿里云 PolarDB Data-Agent | 产品 | PolarDB内置Data-Agent，将自然语言转换为SQL查询和智能图表 | 2025 | https://help.aliyun.com/zh/polardb/polardb-for-mysql/user-guide/chatbi-best-practices |
| 蚂蚁数科 Agentar-Scale-SQL / Agentar SQL | 开源项目/模型 | 蚂蚁数科数据智能体核心技术，登顶BIRD-SQL榜单(执行准确率+效率双第一)，随后开源全套论文/代码/模型 | 2025-09登顶，2025-12-13开源 | https://blog.csdn.net/u013970991/article/details/155965869 |
| 百度智能云 千帆 数据智能平台/Agent Infra | 产品/平台 | 百度智能云在千帆平台上推出数据智能平台及企业级Agent基础设施，2026定位"Agent原生"爆发 | 2025发布，2026持续升级 | https://www.stcn.com/article/detail/3632554.html |
| 腾讯云 BI ChatBI | 产品 | 腾讯云BI内置基于大模型的智能助手ChatBI，支持自然语言数据分析、波动归因 | 2025-2026持续迭代 | https://cloud.tencent.com/developer/article/2657482 |
| 腾讯 OlaChat | 产品 | 腾讯内部智能数据助手，持续优化架构与关键模块设计以提升数据分析智能化 | 2025持续迭代 | https://www.cnblogs.com/clarance/p/19050435 |
| 火山引擎(字节) Data Agent | 产品 | 字节跳动火山引擎发布的企业级AI数据专家Data Agent，基于字节内部数据实践与LLM | 2025-04-08 | https://www.cnblogs.com/bytedata/p/18818520 |
| 火山引擎 ChatBI (DataWind) | 产品 | 火山引擎DataWind团队的ChatBI，支持飞书内自然语言多轮问数，正演进为独立智能体产品 | 2024-05发布，2025持续演进 | https://www.cnblogs.com/bytedata/p/18990210 |
| 帆软 FineBI 7.0 / FineChatBI | 产品 | 帆软FineBI 7.0推出"指标中心+智能问数"双引擎，FineChatBI为对话式AI业务数据分析工具，采用Text2DSL技术 | 2025-2026持续迭代 | https://zhuanlan.zhihu.com/p/1974522704876020923 |
| 帆软 FineBI NEXT (场景Agent) | 产品 | 帆软新一代产品线，2026年9月发布场景化Agent能力(据行业横评文章) | 2026-09(评测文章提及) | https://www.sohu.com/a/1054173632_122297451 |
| 观远 ChatBI / 观远问数Agent | 产品 | 观远数据基于LLM的场景化问答式BI，具备意图识别、知识召回、数据查询、可视化生成能力；入选2025全球企业级AI Agent优秀厂商图谱 | 2025持续迭代 | https://www.guandata.com/bi-copilot |
| Kyligence AI 数据智能体 / Kyligence Copilot | 产品 | Kyligence数据智能体首批亮相神州数码DC·AI生态创新中心，核心是"AI增强语义层"解决Text2SQL准确率问题 | 2025-01 | https://blog.csdn.net/weixin_39074599/article/details/145326465 |
| 衡石科技 HENGSHI SENSE 6.0 / 6.2 | 产品 | 衡石采用"Data+AI Agent"架构，NL2Metrics技术+指标语义层，向所有AI Agent开放BI/数据分析能力调用 | 2025-07(6.0)，2026(6.2) | https://www.hengshi.com/blog/1341.html |
| 网易有数 | 产品 | 网易旗下BI产品，被行业横评文章列为2026年主流Data Agent平台之一 | 2026-07(评测文章提及) | https://www.sohu.com/a/1054173632_122297451 |
| 九数云 (帆软旗下) | 产品 | 帆软旗下轻量化BI产品，被列为2026年主流Data Agent平台横评对象之一 | 2026-07(评测文章提及) | https://www.sohu.com/a/1054173632_122297451 |
| Aloudata Agent | 产品 | 国内新兴厂商Aloudata推出的数据分析决策Agent，独创NL2MQL2SQL技术路径(NoETL指标语义层+多Agent协同) | 2025 | https://zhuanlan.zhihu.com/p/1967625018541342812 |
