# S3 - 官方榜单与 Papers with Code 广度调研

## 执行路径
- WebSearch: "text-to-SQL benchmark leaderboard 2025 2026"
- WebSearch: "data agent benchmark leaderboard 2025"
- WebSearch: "Spider 2.0 leaderboard text-to-SQL"
- WebSearch: "BIRD-CRITIC leaderboard SQL"
- WebFetch: https://bird-bench.github.io/ （抄录 Overall Leaderboard top5 + 子榜单列表）
- WebFetch: https://bird-critic.github.io/ （抄录 BIRD-CRITIC-1.0-Open top5，注意：页面缓存数据偏旧，日期疑似未更新）
- WebFetch: https://spider2-sql.github.io/ （抄录 Spider2.0-Snow top5）
- WebFetch: https://beaverbench.github.io/ （页面结构存在但未渲染出实际排名数据，未获取到具体数值）
- WebSearch: "Papers with Code text-to-SQL state-of-the-art Spider BIRD"
- WebSearch: "LiveSQLBench leaderboard top model 2026"
- WebSearch: "BIRD-Interact benchmark leaderboard agentic SQL"
- WebSearch: "DA-Code benchmark data science agent leaderboard"
- WebFetch: https://ucbepic.github.io/DataAgentBench/ （确认 DAB 范围与更新日期 2026-06-12，未获取到具体排名条目）
- WebFetch: https://benchlm.ai/benchmarks/spider2lite （Spider2.0-Lite 目前仅 1 个已录入模型 Interfaze Beta 52.9%，2026-08-20 更新）
- WebSearch: "TAG-Bench OR table-augmented generation benchmark leaderboard SQL analytics"
- WebSearch: "Kaggle text-to-SQL competition 2025 2026 data agent"
- WebSearch: "DABstep data agent benchmark leaderboard Hugging Face 2025"
- WebSearch: "InfiAgent-DABench OR DSBench data analysis agent benchmark leaderboard"
- WebSearch: "text-to-SQL arena leaderboard 2026 new benchmark enterprise SQL agent"
- WebSearch: "Spider 2.0-lite leaderboard top submissions 2026"

## 候选

| 名称 | 类型 | 一句话描述 | 日期 | URL |
|---|---|---|---|---|
| Spider 2.0 (含 Spider2.0-Snow/Lite) | 基准/榜单 | 企业级真实工作流 Text-to-SQL 基准，ICLR2025 Oral，榜单仍活跃，Snow赛道top为Genloop Sentinel Agent v2 Pro 96.70，Lite赛道top为Interfaze Beta 52.9%(2026-08) | 2024起持续更新 | https://spider2-sql.github.io/ |
| BIRD (主榜) | 基准/榜单 | 经典大规模真实数据库 Text-to-SQL 基准，Overall榜单持续有新提交，top为AskData+GPT-4o 81.95%(2025-09)、Agentar-Scale-SQL 81.67%(2026-06) | 2023起持续更新 | https://bird-bench.github.io/ |
| BIRD-CRITIC (SWE-SQL) | 基准/榜单 | 面向真实用户SQL问题修复/诊断的基准，NeurIPS2025 Main | 2025 | https://bird-critic.github.io/ |
| BIRD-Interact | 基准/榜单 | 以动态交互(对话式/主动Agentic)视角重构Text-to-SQL评测，ICLR2026 Oral，SOTA仅解决约16-24%任务 | 2025-10起 | https://bird-interact.github.io/ |
| LiveSQLBench | 基准/榜单 | 防污染、覆盖全SQL谱系的持续更新Text-to-SQL基准，含分层知识库 | 2025-09起 | https://livesqlbench.ai/ |
| BEAVER | 基准/榜单 | 面向真实私有企业数据库的Text-to-SQL基准，9128条查询，暴露现有模型能力巨大差距 | 2024末发起，2026-05仍在更新 | https://beaverbench.github.io/ |
| DAB (Data Agent Benchmark) | 基准/榜单 | UC Berkeley EPIC Lab出品，覆盖12个真实数据集/9领域/4种数据库系统的数据智能体评测，2026-06-12仍在更新分数 | 2025起 | https://ucbepic.github.io/DataAgentBench/ |
| DABstep | 基准/榜单 | Adyen+HuggingFace联合发布的多步数据分析智能体基准，450+真实金融分析任务，HF实时榜单 | 2025-06-30发布 | https://huggingface.co/blog/dabstep |
| InfiAgent-DABench | 基准/榜单 | 数据分析智能体评测基准(DAEval)，2024年发起但2025-2026仍被新方法(如Jupiter agent)刷榜 | 2024起，持续被引用/刷新 | https://infiagent.github.io/ |
| TAG-Bench | 基准 | UC Berkeley Sky Computing Lab提出的"表格增强生成(TAG)"基准，基于BIRD构建，统一Text2SQL与RAG范式 | 2024-08发起，2025-2026仍被引用 | https://github.com/TAG-Research/TAG-Bench |
| EntSQL | 基准 | 面向长上下文企业私有知识 grounding 的Text-to-SQL基准，中英双语，最佳系统仅15.9% | 2026-06 | https://arxiv.org/abs/2606.03363 |
| TACO | 基准 | 面向开放域、含歧义与跨数据库查询的Text-to-SQL基准 | 2026-06 | https://arxiv.org/pdf/2606.14201 |
| LogicCat | 基准 | 面向复杂链式推理(Chain-of-Thought)的Text-to-SQL基准 | 2025-05 | https://arxiv.org/pdf/2505.18744 |
| DP-Bench | 基准 | 首个评测"数据产品(Data Product)"生成能力的基准，模拟真实业务场景任务 | 2025-12 | (via WebSearch摘要，未独立核实官网) |
| BADGER | 基准 | 面向企业级生成式推理的"Agentic+Deterministic"混合评测框架 | 2026-06 | https://arxiv.org/pdf/2606.02109 |
| DA-Code | 基准 | 面向数据科学智能体的代码生成基准(数据清洗/ML/EDA)，2024年EMNLP发起，仍在2025-2026综述/新方法中被引用 | 2024-10起 | https://da-code-bench.github.io/ |
| DSAEval | 基准 | 面向真实世界广泛数据科学问题的数据科学智能体评测 | 2026-01 | https://arxiv.org/pdf/2601.13591 |
| DataGovBench | 基准 | 面向真实数据治理工作流的LLM智能体评测基准 | 2025-12 | https://arxiv.org/pdf/2512.04416 |
| LongDS-Bench | 基准 | 聚焦长程(long-horizon)智能体数据分析失败模式的基准 | 2026-05/06 | https://arxiv.org/pdf/2605.30434 |
| Holistic Agent Leaderboard (HAL) | 榜单 | 通用AI Agent综合评测基础设施，汇总编码/网页导航/助理/客服等9个基准(含部分数据/代码类任务) | 2025-10 | https://arxiv.org/pdf/2510.11977 |
| BenchLM.ai | 榜单/产品 | 第三方聚合型LLM基准榜单站点，收录Spider2.0-Lite、LiveBench等多个benchmark的实时提交 | 持续更新，快照2026-08 | https://benchlm.ai/ |
| "Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards" | 论文 | 系统分析Spider/BIRD等主流Text-to-SQL基准与榜单中的标注错误问题，对榜单可信度提出质疑 | 2026-01 (CIDR2026) | https://arxiv.org/pdf/2601.08778 |
| ReFoRCE | 开源项目/方法 | UCSD Hao AI Lab提出的自纠错+格式约束+列探索Text-to-SQL Agent，一度登顶Spider2.0榜单 | 2025 | https://haoailab.com/blogs/reforce/ |
| Agentar-Scale-SQL | 模型/方法 | 蚂蚁集团提出的基于测试时扩展(test-time scaling)的Text-to-SQL方法，BIRD榜单前列(81.67%, 2026-06) | 2026-06 | https://bird-bench.github.io/ |
| "Both Ends Count! Just How Good are LLM Agents at Text-to-Big SQL?" | 论文 | 探讨大规模("Big SQL")场景下LLM Agent的Text-to-SQL能力评测 | 2026-02 | https://arxiv.org/pdf/2602.21480 |
| "Data Agents: Levels, State of the Art, and Open Problems" | 论文 | 对"数据智能体(Data Agents)"进行分级并综述当前SOTA与开放问题的综述论文 | 2026-02 | https://arxiv.org/pdf/2602.04261 |
