# S2 arXiv 广度调研：Data Agent / Data Science Agent / 数据分析类论文与Benchmark

## 执行路径
- WebSearch: `arxiv 2025 "data analysis agent" LLM benchmark` — 发现 DataSciBench、DataGovBench、Data Agents Levels综述、DSGym、两篇DS Agent综述
- WebSearch: `arxiv 2025 "data science agent" LLM autonomous` — 发现 EvoDS、DatawiseAgent、AutoKaggle、DeepAnalyze、R&D-Agent、LongDA
- WebSearch: `arxiv 2025 2026 "table reasoning" agent LLM benchmark multi-table` — 发现 TableVista、TABVERSE、MMTU(线索)、ReasonTabQA、Reasoning-Table、ASTRA
- WebSearch: `arxiv 2025 2026 "agentic data analysis" benchmark` — 发现 AiDABench、FDABench、UniDataBench、LongDS-Bench、DABstep(线索)
- WebSearch: `arxiv 2025 2026 text-to-SQL agent LLM benchmark` — 发现 BIRD-Interact(线索)、Text-to-SQL annotation errors (CIDR2026)、Text-to-Python vs Text-to-SQL、DAComp、Arming Data Agents with Tribal Knowledge
- WebSearch: `arxiv 2025 2026 "BI agent" OR "business intelligence agent" LLM` — 未见2025+新BI agent专文，交叉确认已有条目
- WebSearch: `arxiv 2026 data agent benchmark heterogeneous data reinforcement learning` — 确认 FDABench 细节
- WebSearch: `arxiv 2025 2026 "spreadsheet agent" OR "chart agent" OR "insight agent" LLM benchmark` — 发现 InsightEval、MBABench、AgentFuel
- WebSearch: `arxiv MMTU massive multi-task table understanding benchmark NeurIPS 2025` — 确认 MMTU (NeurIPS 2025 D&B Track, 28K题/25任务) 及 GitHub 仓库
- WebSearch: `arxiv BIRD-Interact DABstep AutoKaggle DeepAnalyze RealHiTBench data agent` — 确认 BIRD-Interact、DABstep、DeepAnalyze、DSAEval 的 arXiv 链接与日期；AutoKaggle 确认为 2024-10 旧作（社区仍常被引用，标注为pre-2025）

看过的关键页面（除搜索结果摘要外未逐一深读全文，仅核对标题/摘要/日期）：
- https://arxiv.org/abs/2502.13897 (DataSciBench)
- https://arxiv.org/pdf/2602.04261 (Data Agents: Levels, SOTA, Open Problems)
- https://github.com/MMTU-Benchmark/MMTU

## 候选

| 名称 | 类型 | 一句话描述 | 日期 | URL |
|---|---|---|---|---|
| DataSciBench | 基准 | 面向数据科学任务的LLM Agent综合评测基准，覆盖不确定ground truth场景 | 2025-02 | https://arxiv.org/abs/2502.13897 |
| DatawiseAgent | 框架 | Notebook中心化的LLM Agent框架，用于自动化数据科学全流程 | 2025-03 | https://arxiv.org/abs/2503.07044 |
| R&D-Agent | 框架 | 面向自主数据科学的LLM Agent框架，聚焦研发闭环 | 2025-05 | https://arxiv.org/abs/2505.14738 |
| DABstep | 基准 | 450+真实多步数据分析任务，混合结构化与非结构化数据 | 2025-06 | https://arxiv.org/abs/2506.23719 |
| MMTU | 基准 | 28K题/25类真实表格任务的大规模多任务表理解与推理基准（NeurIPS 2025 D&B） | 2025-06 | https://github.com/MMTU-Benchmark/MMTU |
| Large LLM-based Data Science Agent Survey | 论文/综述 | 系统综述LLM数据科学Agent的能力、挑战与方向 | 2025-08 | https://arxiv.org/pdf/2508.02744 |
| FDABench | 基准 | 面向异构数据（6种模态）分析查询的数据Agent基准，含PUDDING构建框架 | 2025-09 | https://arxiv.org/abs/2509.02473 |
| LLM-Based Data Science Agents Survey | 论文/综述 | 另一篇聚焦数据科学Agent能力/挑战/未来方向的综述 | 2025-10 | https://arxiv.org/html/2510.04023v1 |
| DeepAnalyze | 模型/框架 | 8B参数的自主数据科学Agentic LLM，端到端产出分析师级报告 | 2025-10 | https://arxiv.org/abs/2510.16872 |
| BIRD-Interact | 基准 | 通过动态交互（澄清、知识检索、错误恢复）重构text-to-SQL评测 | 2025-10 | https://arxiv.org/abs/2510.05318 |
| Mixture-of-Minds | 论文 | 多智能体强化学习框架用于表格理解 | 2025-10 | https://arxiv.org/pdf/2510.20176 |
| LLM/Agent驱动的企业级数据分析 | 论文 | 面向企业应用与系统级部署的LLM+Agent数据分析方法论 | 2025-11 | https://arxiv.org/pdf/2511.17676 |
| UniDataBench | 基准 | 评测数据分析Agent跨结构化与非结构化数据的能力 | 2025-11 | https://arxiv.org/abs/2511.01625 |
| InsightEval | 基准 | 专家标注的基准，评测LLM数据Agent的洞察发现能力 | 2025-11 | https://arxiv.org/pdf/2511.22884 |
| DAComp | 基准 | 覆盖数据智能全生命周期（采集-清洗-分析-治理）的数据Agent基准 | 2025-12 | https://arxiv.org/pdf/2512.04324 |
| DataGovBench | 基准 | 面向真实数据治理工作流的LLM Agent基准 | 2025-12 | https://arxiv.org/pdf/2512.04416 |
| LongDA | 基准 | 面向长文档数据分析场景的LLM Agent基准 | 2026-01 | https://arxiv.org/pdf/2601.02598 |
| DSGym | 基准/框架 | 面向数据科学Agent训练与评测的整体性框架 | 2026-01 | https://arxiv.org/pdf/2601.16344 |
| ReasonTabQA | 基准 | 面向真实工业场景的表格问答综合基准 | 2026-01 | https://arxiv.org/pdf/2601.07280 |
| DSAEval | 基准 | 在广泛真实数据科学问题上评测数据科学Agent | 2026-01 | https://arxiv.org/html/2601.13591v1 |
| Text-to-Python vs Text-to-SQL | 论文 | 对比Text-to-Python与Text-to-SQL在显式逻辑与歧义处理上的差异 | 2026-01 | https://arxiv.org/pdf/2601.15728 |
| Data Agents: Levels, SOTA, Open Problems | 论文/综述 | 提出数据Agent能力分级框架，梳理现状与开放问题 | 2026-02 | https://arxiv.org/pdf/2602.04261 |
| Arming Data Agents with Tribal Knowledge | 论文 | 探讨为数据Agent注入组织"部落知识"（隐性业务知识）的方法 | 2026-02 | https://arxiv.org/pdf/2602.13521 |
| AiDABench | 基准 | AI数据分析基准（AI Data Analytics Benchmark） | 2026-03 | arXiv:2603.15636 |
| AgentFuel | 框架/评测生成器 | 用于时序数据分析Agent的可定制化评测生成工具 | 2026-03 | https://arxiv.org/pdf/2603.12483 |
| TableVista | 基准 | 面向视觉与结构复杂表格的多模态表理解基准 | 2026-05 | https://arxiv.org/pdf/2605.05955 |
| MBABench | 基准 | 评测LLM Agent在金融领域端到端电子表格任务上的表现 | 2026-05 | https://arxiv.org/abs/2605.22664 |
| LongDS-Bench | 基准 | 长时程Agentic数据分析的失败模式基准 | 2026-05 | https://arxiv.org/pdf/2605.30434 |
| TABVERSE | 基准 | 跨格式（表格/图像/文本等）表理解基准，评测LLM与VLM | 2026-06 | https://arxiv.org/pdf/2606.09578 |
| EvoDS | 框架 | 具备技能学习与上下文管理的自演化自主数据科学Agent | 2026-06 | https://arxiv.org/pdf/2606.03841 |
| AutoKaggle（标注：pre-2025旧作，仍被广泛引用） | 框架 | 多智能体框架，自动化参与Kaggle式数据科学竞赛（Reader/Planner/Developer/Reviewer/Summarizer） | 2024-10（社区在2025-2026仍活跃引用） | https://arxiv.org/html/2410.20424v1 |
