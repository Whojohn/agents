## 执行路径
- WebSearch: `arxiv 2025 "text-to-SQL" survey`
- WebSearch: `arxiv 2026 "text-to-SQL" reinforcement learning agent`
- WebSearch: `arxiv 2025 "NL2SQL" multi-agent schema linking`
- WebSearch: `arxiv 2026 "text-to-SQL" self-correction fine-tuning small model`
- WebSearch: `arxiv "text-to-SQL survey" 2026`
- WebSearch: `Arctic-text2sql-r1 OR CHASE-SQL OR XiYan-SQL OR OmniSQL text-to-SQL 2025`
- WebSearch: `MCTS-SQL Monte Carlo Tree Search text-to-SQL arxiv`
- WebSearch: `Reasoning-SQL reinforcement learning partial rewards arxiv 2025`
- 关键页面：arxiv.org/abs/2505.20315 (Arctic-Text2SQL-R1)，arxiv.org/abs/2503.23157 (Reasoning-SQL)，arxiv.org/abs/2501.16607 (MCTS-SQL)，arxiv.org/abs/2406.08426 (Next-Gen DB Interfaces survey，2025-11 revised)，arxiv.org/pdf/2602.04261 (Data Agents survey)
- 说明：部分 arXiv 编号前缀显示为 25xx/26xx，反映站点当前日期为 2026-08，按题目要求覆盖 2025-01 至今（含 2026）

## 候选
| 名称 | 类型 | 一句话描述 | 日期 | URL |
|---|---|---|---|---|
| Next-Generation Database Interfaces: A Survey of LLM-based Text-to-SQL | 论文/综述 | 覆盖 LLM 时代 text-to-SQL 全流程的高引综述，2025-11 仍在更新 | 2024-06 初稿/2025-11 修订 | https://arxiv.org/abs/2406.08426 |
| A Survey of Text-to-SQL in the Era of LLMs: Where are we, and where are we going? | 论文/综述 | IEEE TKDE 2025 发表的另一篇系统性综述，梳理方法分类与未来方向 | 2024-08 初稿/2025 期刊发表 | https://arxiv.org/pdf/2408.05109 |
| Data Agents: Levels, State of the Art, and Open Problems | 论文/综述 | 把 text-to-SQL 放入更广的"数据智能体"分级框架中讨论现状与开放问题 | 2026-02 | https://arxiv.org/pdf/2602.04261 |
| NL2SQLBench | 基准 | 面向 LLM NL2SQL 方案的模块化可扩展评测框架 | 2026-04 | https://arxiv.org/pdf/2604.16493 |
| BIRD-INTERACT | 基准 | 从"动态交互"视角重构 text-to-SQL 评测，引入多轮/交互式场景 | 2025-10 | https://arxiv.org/pdf/2510.05318 |
| Spider 2.0-AIFunc | 基准 | 将 Spider 2.0 真实场景 text-to-SQL 扩展到 AI-native SQL 工作流 | 2026-07 | https://arxiv.org/pdf/2607.06229 |
| Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards | 论文 | 指出主流 text-to-SQL 基准/榜单存在系统性标注错误，质疑现有排名可信度 | 2026-01 | arxiv:2601.08778 |
| Arctic-Text2SQL-R1 | 论文/模型 | Snowflake 提出的纯执行正确性奖励 RL 框架，32B 模型刷新 BIRD SOTA | 2025-05 | https://arxiv.org/abs/2505.20315 |
| Reasoning-SQL | 论文 | 面向 text-to-SQL 定制的部分奖励(schema-linking/AI反馈/语法检查)+GRPO 强化学习方法 | 2025-03 | https://arxiv.org/abs/2503.23157 |
| MCTS-SQL | 论文 | 用蒙特卡洛树搜索让轻量级 LLM 在 text-to-SQL 上达到接近大模型效果 | 2025-01 | https://arxiv.org/abs/2501.16607 |
| Alpha-SQL | 论文 | 零样本场景下用 MCTS 逐步推导 SQL 构造动作的框架 | 2025-02 | arxiv:2502.17248 |
| R3-SQL | 论文 | 用排序奖励(Ranking Reward)+重采样改进 text-to-SQL 的 RL 训练 | 2026-04 | https://arxiv.org/pdf/2604.25325 |
| TRUST-SQL | 论文 | 面向未知 schema 场景的工具集成多轮强化学习 text-to-SQL 框架 | 2026-03 | https://arxiv.org/pdf/2603.16448 |
| AGRO-SQL | 论文 | Agentic Group-Relative Optimization + 高保真数据合成的 RL 方法 | 2025-12 | arxiv:2512.23366 |
| SERL-SQL | 论文 | 选择性事后蒸馏(Selective Hindsight Distillation)的强化式智能体 text-to-SQL 学习 | 2026-08 | https://arxiv.org/abs/2608.00485 |
| MTIR-SQL | 论文 | 多轮工具集成推理的强化学习 text-to-SQL 方法 | 2025-10 | arxiv:2510.25510 |
| MARS-SQL | 论文 | 多智能体强化学习框架用于 text-to-SQL | 2025-11 | arxiv:2511.01008 |
| FINER-SQL | 论文 | 用细粒度执行反馈(密集奖励)提升小语言模型的 text-to-SQL 能力 | 2026-05 | https://arxiv.org/abs/2605.03465 |
| SQLConductor | 论文 | 搜索到策略(Search-to-Policy)学习，分步编排 text-to-SQL 流程 | 2026-06 | https://arxiv.org/pdf/2606.23537 |
| SQL-of-Thought | 论文 | 多智能体 text-to-SQL，含 schema linking/子问题拆解/CoT/显式错误修正闭环 | 2025-09 | https://arxiv.org/html/2509.00581v2 |
| LinkAlign | 论文 | 面向真实世界大规模多数据库场景的可扩展 schema linking 方法(EMNLP 2025) | 2025 | arxiv (EMNLP 2025) |
| AgentNLQ | 论文 | 通用型 NL-to-SQL 智能体，探讨多智能体架构提升准确率 | 2026-05 | https://arxiv.org/pdf/2605.19010 |
| SLM-SQL | 论文 | 系统探索小语言模型(SLM)用于 text-to-SQL 的可行路径 | 2025-07 | https://arxiv.org/pdf/2507.22478 |
| Schema on the Inside | 论文 | 两阶段微调方法，将 schema 信息内化以实现大规模高效 text-to-SQL | 2026-03 | https://arxiv.org/html/2603.24023v1 |
| Cheaper, Better, Faster, Stronger | 论文 | 不用 CoT/微调，通过多重 schema 表示实现小模型稳健 text-to-SQL | 2025-05 | https://arxiv.org/abs/2505.14174 |
| RubikSQL | 开源项目/产品 | 阿里系工业级 NL2SQL 系统，具备终身学习的智能体知识库 | 2025-08 | https://arxiv.org/html/2508.17590v1 |
| Agentar-Scale-SQL | 论文 | 通过编排式测试时扩展(test-time scaling)推进 text-to-SQL 效果 | 2025-09 | https://arxiv.org/html/2509.24403v3 |
| DecoSearch | 论文 | 复杂度感知路由 + 计划级修复的 text-to-SQL 框架 | 2026-06 | https://arxiv.org/pdf/2606.17821 |
| EvolSQL | 论文 | 结构感知的进化式数据合成方法，规模化生成 text-to-SQL 训练数据 | 2026-01 | https://arxiv.org/pdf/2601.04875 |
