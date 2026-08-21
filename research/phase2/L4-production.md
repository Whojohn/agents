# L4 — 落地实践线：准确率之外的生产问题（冷启动 / 口径 / 维护 / 兜底）

调研日期：2026-08-20 ｜ 时效线：仅采信 2025-01 之后来源 ｜ 深读条目：21

## 执行路径

- Anthropic《How Anthropic enables self-service data analytics with Claude》(2026-06-03) — 一手，两次取证核对原句 https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude
- Anthropic《Demystifying evals for AI agents》(2026-01-09) https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- dbt Labs《Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update》(2026-04-07) https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026
- dbt Labs《The analytics engineer in 2026》(2026-06-16) https://www.getdbt.com/blog/the-analytics-engineer-in-2026-system-designer-governance-owner-ai-context-provider
- Snowflake Engineering《Agentic Semantic Model Improvement》(2025-03-31) https://www.snowflake.com/en/blog/engineering/agentic-semantic-model-text-to-sql/
- Databricks《How to Build Production-Ready Genie Spaces, and Build Trust Along the Way》(2026-02-06) https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way
- 贝壳商机平台《基于 NL2SQL 实现指标查询实践》InfoQ (2025-08-27) https://www.infoq.cn/article/TZfeOJOBCtyh5fW5Xg8N
- FreeWheel ChatBI 落地实践 InfoQ (2025-06-29) https://www.infoq.cn/article/zn5fv8qxoncytiaumglo
- LinkedIn《Text-to-SQL for Enterprise Data Analytics》KDD'25 workshop (2025-07-18) https://arxiv.org/abs/2507.14372
- HN 讨论《Text-to-SQL is dead, long live text-to-SQL》(2025-10-28, 62分) https://news.ycombinator.com/item?id=45733525
- nao《20 Best AI Analytics Agents Compared: 2026 Benchmark》(2026-02-03) https://getnao.io/blog/ai-data-agents-compared/
- Cube《Semantic Layer for AI Agents (2026)》(2026-08-17) https://cube.dev/articles/semantic-layer-for-ai-agents-2026
- TianPan《Text-to-SQL in Production: Why Correct SQL Is the Easy Part》(2026-04-10) https://tianpan.co/blog/2026-04-10-text-to-sql-failure-modes-production
- AtScale《How Anthropic's AI Accuracy Went from 21% to 95%》(2026-06-11，二手交叉验证) https://www.atscale.com/blog/anthropic-ai-accuracy-semantic-layer/
- Ashpreet Bedi《Self-Improving Text2SQL Agent》(2025-12-15) https://www.ashpreetbedi.com/articles/sql-agent
- arXiv 2511.10674《Continual Learning of Domain Knowledge from Human Feedback in Text-to-SQL》(2025-11) https://arxiv.org/abs/2511.10674
- HN Show HN: Dinobase (2026-04-07, 12分) https://news.ycombinator.com/item?id=47678048
- Databricks《Next-generation Databricks Genie》(2026-04-26) https://www.databricks.com/blog/next-generation-databricks-genie
- Aloudata《解构智能问数：为什么 NL2SQL 不是终点》腾讯新闻 (2025-06-23) https://news.qq.com/rain/a/20250623A05IBH00
- 仓库原生语义层 GA 时间线交叉核对（Snowflake Semantic Views SQL GA 2026-03，Databricks Metric Views GA 2026-04）https://cube.dev/articles/semantic-layer-for-ai-agents-2026
- 中国一汽 GPT-BI（ifeng 2024-05-11 / InfoQ 2024-04-19 / 财经网 2026-07-15）三源交叉核对后剔除，见下

## 剔除

- Snowflake《Cortex Analyst text-to-SQL accuracy》博客（90%、150 题内部基准）| 2024-08-29 发表，早于时效线，其数字不作本轮证据；改用 2025-03 的 agentic semantic model 博客。
- 中国一汽 GPT-BI「准确率 20%→92.5%」| 一手源为 2024-05 凤凰财经，超出时效线；坊间流传的「468 指标 / 6 万评测 / 3.2%→90%」在财经网 2026-07 报道中无法核实，属未溯源转述。
- 火山引擎 DataWind ChatBI（AICon 2025-05 页面）| 仅演讲大纲，无架构、准确率、评测集等实质内容，不构成一手实践证据。
- Aloudata《解构智能问数》(腾讯新闻) | 厂商 CMO 署名稿，零量化数据，仅作「口径冲突是数据工程问题」的观点参照，不作证据。
- Databricks《Next-generation Genie》公告 | 2026 年新建 150 万 Genie Space 是采用量而非质量指标，公告本身无落地方法论。
- AtScale 自家 Tier-1 银行基准（算力降 21000x、70%→100%、省 900 万美元）| 无公开方法论与题目集，不可复现，剔除；该文仅保留为 Anthropic 结论的二手交叉验证。
- Dinobase「SQL 比 MCP 工具准确率高 2-3 倍、token 效率高 16-22 倍」| HN 仅 12 分，75 题自建基准 + LLM-as-judge，评论已指出聚合型题目偏置未拆解，仅作弱信号。
- Self-Improving SQL Agent 的 HN 帖 (46350486) | 仅 1 分无讨论；改引其原文博客本身。
- arXiv 2511.10674 | BIRD dev 上的学术方法验证，非生产部署，仅作「反馈沉淀为程序性记忆」的方法参照。
- 各类《Best semantic layer tools 2026》导购榜单（Atlan / Knowi / Dawiso / Colrows）| SEO 内容，无一手评测数据。
- 中文《2026 企业 AI Agent 落地避坑指南》系列（七牛云 / CSDN / 实在智能）| 通用 Agent 内容农场文，非 text-to-SQL 一手实践，「65% 失败率」等数字无出处。

## 结论

### 0. 定位：落地问题几乎全部出现在 L2 以上，而 L1 已不是瓶颈

dbt 2026 基准显示，纯 text-to-SQL 在同一套题上的准确率两年内从 32.7%（GPT-4 时代）提升到 64.5%（Sonnet 4.6 / GPT-5.3 Codex）——模型侧确实在进步（L1）。但同一份基准里，**语义层内题目两个模型都是 100%，而裸 text-to-SQL 只有 62.5% / 51.2%**。也就是说 L1 的剩余差距不是"模型不够聪明"，而是"没人告诉它口径"。生产问题的重心已经完全转移到 L2~L5。
https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026

学术分数与生产可靠性之间存在断崖：o1-preview 在 Spider 1.0 上 91.2%，在企业级 Spider 2.0 上仅 21.3%（ICLR 2025）；LinkedIn 生产系统（知识图谱 + text-to-SQL agent + 聊天机器人，300+ 周活）在自建内部基准上也**只有 53% 的回答"正确或接近正确"**。这是目前公开可查的、最诚实的大厂生产数字。【L2】
https://arxiv.org/abs/2507.14372 ｜ https://tianpan.co/blog/2026-04-10-text-to-sql-failure-modes-production

---

### 1. 冷启动：证据高度一致——"补上下文"有效，"堆语料"无效

**最强证据（Anthropic，2026-06-03，一手）**：同一个 Claude，**无 skills 时准确率不超过 21%，加上 skills 后稳定在 95% 以上**，业务分析查询自动化率 95%。其栈分四层：数据基础（canonical 数据集）→ 事实来源（语义层优先、血缘图、精选查询模式）→ skills（成对的 knowledge + runbook markdown，按域路由到"~30 个描述相关表的参考文件"）→ 验证（离线 evals / 消融 / 线上监控 / 对抗审查）。【L3-L5】
https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude

**两个反直觉的负面结论（同一来源，最有价值的部分）**：
1. **直接给 SQL 语料库不管用**。把历史 SQL 全量给 agent 后，"约 80% 的情况下答案确实在语料里"，但"flip rate 是平的"——正确率几乎不动（消融显示 <1 个百分点）。瓶颈不是资料有无，而是**结构**。
2. **LLM 自动生成语义层是净负收益**。原话："由 LLM 从原始表和查询日志自动生成指标定义来引导语义层……在我们的 evals 上相对一个更小的、人工精选的语义层是净负的。" 落地规则：**Claude 起草文档，人类拥有定义**。
   交叉验证：AtScale 转述为"LLM 写出的定义看似合理，却把你想消灭的歧义又偷偷带了回来"。
   https://www.atscale.com/blog/anthropic-ai-accuracy-semantic-layer/

**重要反例与边界条件（Snowflake，2025-03-31）**：Snowflake 的"agentic semantic model improvement"用多 agent 流水线（建模 agent / 关系 agent / 语义模型编辑器 / 自定义指令编辑器 / 评估 agent）自动迭代语义模型，在 4 个 BIRD-SQL 子集上把 vanilla Claude 的 **57% 平均提升到 78%（+21 个百分点）**（Debit Card 52%→83%、California Schools 63%→80%、Thrombosis 45%→70%、Toxicology 69%→79%）。【L2-L5】
https://www.snowflake.com/en/blog/engineering/agentic-semantic-model-text-to-sql/

> **组长判断（这是本报告最关键的一条辨析）**：Snowflake 与 Anthropic 看似矛盾，实则不矛盾。Snowflake 的自动化流水线是**有 ground-truth SQL 监督的**（"比较生成 SQL 与正确 SQL 并建议修正"），Anthropic 否定的是**无监督地从原始表和查询日志里凭空生成定义**。结论应表述为：**语义层可以被 agent 自动"精修"，但不能被 agent 自动"发明"**——必须有人工定义或标注答案作为锚。

**可复制的迭代曲线（Databricks，2026-02-06，最实用的冷启动 SOP）**：单个 Genie Space 的真实五轮迭代：命名混乱的基线 **0% → 补元数据 54% → 加自定义指标 77% → 加领域规则 100%**；基准题只用 13 道；行业经验阈值是"**进入 UAT 前 benchmark 应 >80%**"。基准题应由 SME + 真实终端用户在**开发之前**写好，10~20 道即可。【L2】
https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way

**中文一手实践的冷启动量级（FreeWheel，2025-06-29）**：标注 **400+ 选表示例、300+ SQL 示例**；做法是"先用初始版本的 Text2SQL 生成 SQL，再人工 Review 和修改"，并用 **SQL2Text 把线上采样的 SQL 反向转成问题**来放大语料；业务术语与指标定义进向量库靠 RAG 动态检索。结果：选表准确率 95%+，常见问题全流程准确率 90%+，异常检测 P/R 均 >90%。架构为 LangGraph 多 agent（意图识别 / 智能选表 / Text2SQL / 可视化 + 时序预测、异常检测、下钻、漏斗）。【L3】
https://www.infoq.cn/article/zn5fv8qxoncytiaumglo

**贝壳商机平台（2025-08-27）**：综合准确率 **93%**，但关键在于它**根本没做通用 text-to-SQL**——底座是 Apache Doris 上已建好的商机指标平台，"核心指标聚合在宽表中""减少复杂 JOIN 推理"，因此"无需额外引入 DSL 层"。语义资产包括指标知识库（名称/口径定义/依赖字段/所属表/维度限制）、衍生指标公式（转成交率=成交量/商机量）、领域词义（"三好经纪人"=响应率>x 且转化率>y 且商机量>z）、默认指标策略。【L1-L2】
https://www.infoq.cn/article/TZfeOJOBCtyh5fW5Xg8N

> **冷启动小结**：所有成功案例的共同形状是 **"先把范围收窄到已治理的数据资产，再用几百条人工校验的示例 + 10~20 道基准题驱动 3~5 轮迭代"**。没有一个案例是靠喂大量原始语料或换更强模型解决的。

---

### 2. 口径一致性：语义层的价值不在"更准"，而在"失败时报错而不是给错数"

dbt 2026 基准（ACME Insurance，11 题 × 20 次，4 种配置，2026-04-07）：
| 配置（modeled 数据上） | Sonnet 4.6 | GPT-5.3 Codex |
|---|---|---|
| Text-to-SQL | 90.0% | 84.1% |
| Semantic Layer | 98.2% | 100.0% |

范围内题目语义层 100%（两模型），裸 text-to-SQL 62.5% / 51.2%；范围外题目语义层 **0%**（确定性报错），裸 text-to-SQL 70% / 100%。dbt 自己的总结句最精准：**"语义层的失败 = 一条错误消息；text-to-SQL 的失败 = 一个错误的数字。"**【L2-L5】
https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026

**但必须诚实标注三条反向证据，避免把"语义层"讲成万能药**：
1. **更好的建模对两边都有效**。同一基准中只加了 3 个 dbt model 来补实体跳数缺口，裸 text-to-SQL 也从 64.5% 跳到 84~90%。收益的一大部分来自"把数据建好"，而非"语义层"这个形态本身。
2. **语义层对未定义问题是硬失败**。nao 的横评把"需要大量前期建模、对未定义问题束手无策"直接列为语义层类工具的失败模式；并报告过"一份写得好的 rules.md 在 ad-hoc 查询上跑赢 MetricFlow 语义层"。【L2】
   https://getnao.io/blog/ai-data-agents-compared/
3. **规模才是真瓶颈**。HN 2025-10 讨论中，实践者 zurfer 报告在 Databricks Genie 上跨团队数百张表时，"当前工具最适合约 20 张组织良好的表"；getdot.ai 创始人 maxdemarzi 称 10~5000 张表可用，但补一句"要修好路、到处立好路牌是很费功夫的"。同帖批评方指出 Spider2 SOTA 仅 64%，宣称 99% 的都未经验证。【L1-L2】
   https://news.ycombinator.com/item?id=45733525

**生态层面的既成事实**：仓库原生语义层已在 2026 年落地为标准件——Snowflake Semantic Views 于 2026-03 达成标准 SQL 查询 GA，Databricks Metric Views 于 2026-04 GA。"要不要语义层"在产品侧已无争议，争议只剩"用中立层（dbt/Cube/AtScale）还是绑定仓库"。Cube 的立场句可作为业界共识表述：**"Text-to-SQL 给 agent 的是数据的访问权，语义层给它的是理解。"**【L5】
https://cube.dev/articles/semantic-layer-for-ai-agents-2026

---

### 3. 维护与防腐烂：把"语义层"当代码管，是唯一被验证有效的机制

**最硬的一个数字（Anthropic 一手）**：**"我们眼看着离线准确率从上线时的 ~95% 在一个月内漂移到 ~65%，直到我们把它当成一个工程问题来处理。"** 这条量化了"腐烂"的速度——**不做维护机制，一个月掉 30 个点**。【L5】

其解法不是流程规范而是**工具强制**：
- skills 与数据转换代码放在同一个 repo；
- **"一个 code-review hook 会标记任何没有改动 skill 文件的报表模型变更。目前大约 90% 的数据模型 PR 会在同一个 diff 里带上 skill 变更。"**
- 治理由三件事落地：结构化路由（tooling）、阻断式 CI、以及"下游团队要么建在受治理层上、要么给出偏离理由"的强制授权（mandate）。
https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude

**角色变化（dbt Labs，2026-06-16）**：analytics engineer 的三大职责重定义为**系统设计者 / 治理所有者 / AI 上下文提供者**；"治理已成为首要交付物"。核心论断：**"组织在 AI 上失败，不是因为模型错了，而是因为 AI agent 缺少理解数据含义所需的上下文。"** 2026 State of Analytics Engineering 报告称 **72% 的 analytics engineer 已把 AI 辅助编码纳入工作流**。判断句："把 2026 花在跟 AI 拼代码产量上的 AE，角色会萎缩；专注业务判断、上下文设计和治理所有权的，角色会扩张。"【L5】
https://www.getdbt.com/blog/the-analytics-engineer-in-2026-system-designer-governance-owner-ai-context-provider

**工具化的回归机制**：nao 内置 evals harness——定义标准问题集（question + expected SQL），针对每套上下文配置跑出可靠性/覆盖率/成本/速度分数，支持"只改一个变量（加 rules.md、去掉 dbt repo、抽样换成 profiling）再量化影响"。这与 Anthropic 的消融方法论同构，是目前"防腐烂"的标准动作。【L2】
https://getnao.io/blog/ai-data-agents-compared/

**增量沉淀模式**：Agno 作者的生产设计把循环写成"**每一个好查询变成未来的上下文，每一个错误变成一条规则，每一次澄清变成共享知识**"，且明确"不更新模型权重，只更新检索知识"，知识库保持人工可查可改。核心判断与 Anthropic 一致：**"大多数 Text-to-SQL 失败不是'模型笨'，而是'模型缺上下文和部落知识'。"**【L2】
https://www.ashpreetbedi.com/articles/sql-agent
学术侧对应工作：arXiv 2511.10674 把人类自然语言反馈蒸馏进结构化记忆供后续复用，其中 Procedural Agent 增益最大（BIRD dev，非生产部署）。
https://arxiv.org/abs/2511.10674

---

### 4. 兜底与信任：四层防线已收敛为行业标准动作

**评测集建设（Anthropic evals 方法论，2026-01-09）**：起步 **20~50 个来自真实失败的任务**即可；来源顺序为①把发版前的人工验证转成用例 ②从 bug tracker 和支持工单里挖用户报告的失败 ③优先真实场景。LLM-as-judge 必须与人类专家校准，要给"Unknown"逃生口，且**每个维度用独立的 judge 而非一个 judge 评所有维度**。关键判断："**evals 拖得越久越难建**。"【L2-L5】
https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

Anthropic 生产侧的具体做法：离线 evals（仪表盘自动生成 + 人工校验，外加长尾问题，ground truth 锚定快照日期，结果存为遥测）；消融（固定 eval 集，一次只变一个组件）；线上（**provenance footer 溯源脚注、对抗审查子 agent、数据质量检查**）；以及被动信号——**语义层使用占比、用户话语中的纠正性措辞**。

**中文实践的兜底细节（贝壳，最具操作性）**：
- SQL 安全：**仅允许 SELECT**；未指定时间则**默认最近 7 天或当月**；**自动追加 LIMIT 100**；
- 调 **Doris EXPLAIN** 分析执行计划，出现全表扫描则提示；
- 超出支持指标集合时**主动反馈并推荐替代项**（"暂不支持'业绩波动指数'，可查询'门店业绩总额'……"）；
- 双指标评测 **EM（精确匹配）+ EX（执行正确）**，用 SQL 模式对比算法判逻辑等价、用执行引擎判结果；**"只要有一个不一致就会走到人工来评估"**。
https://www.infoq.cn/article/TZfeOJOBCtyh5fW5Xg8N

**HITL（FreeWheel）**：面对模糊提问**主动追问澄清意图**；列表校验、SQL 校验失败**退回上一步重试**；语法检查之后**再由 LLM 做一次"业务正确性"评估**。
https://www.infoq.cn/article/zn5fv8qxoncytiaumglo

**四层防御（工程综述，2026-04-10）**：①schema 动态检索注入 + 嵌入业务术语表 ②执行前用 AST（sqlglot）校验，拒绝 DDL、缺 WHERE、无 LIMIT 的 SELECT * ③只读凭据 + 行级安全 + STATEMENT_TIMEOUT + 全量查询日志 ④执行后用轻量二次 LLM 调用校验结果是否回答了原问题 + 行数/数值合理性检查。安全侧有真实 CVE：**Vanna.AI CVE-2024-5565**（LLM 生成 SQL 进 `exec()` 导致 RCE）；**ToxicSQL 投毒 0.44% 训练数据即达 85.81% 攻击成功率**；以及最普遍的结构性问题——**service account 广权限导致行级安全被绕过**（用户认证为 A，LLM 仍以服务账号身份发查询）。【L2】
https://tianpan.co/blog/2026-04-10-text-to-sql-failure-modes-production

---

### 5. 业界公认落地路径与失败模式

**路径共识（三家独立来源同构，可信度高）**：
1. **先数据基础，后 agent**。Databricks 的 iteration 0 = 0% 直接由"命名混乱"造成；Anthropic 把 canonical 数据集列为第一层；贝壳干脆建在已治理的指标平台上。**没有干净的表和显式 PK/FK，后面所有工作都是白做**。
2. **先写基准题，再建系统**。10~20 道由 SME + 真实用户在开发前写好，>80% 才进 UAT（Databricks）；20~50 个来自真实失败的任务起步（Anthropic）。
3. **先小范围高频域，再扩**。Genie Space / 域级 skills / 单一业务线指标平台，都是域级切分；HN 实践者的"约 20 张组织良好的表"是当前工具的舒适区。
4. **小而人工精选的语义层，而非自动生成的大语义层**（Anthropic 消融结论）；自动化只用于**有 ground truth 监督的精修**（Snowflake）。
5. **混合路由**：语义层优先 → 差一点就补最小建模 → 只对真正探索性问题回落到裸 text-to-SQL（dbt 官方推荐）。
6. **语义层/skills 进 CI**，用 code-review hook 与回归 evals 锁住漂移（Anthropic 90% PR 同 diff 带 skill 变更）。

**失败模式清单（按危害排序）**：
- **静默错误 > 报错**：fan-out join 虚增聚合、NULL 语义、日期边界/时区、业务名词歧义（"revenue"在财务和销售是两个数）。这是生产第一杀手，用户无法自行发现。
- **基准到生产的断崖**：Spider 1.0 91.2% → Spider 2.0 21.3%；LinkedIn 生产 53%。任何只报学术分数的方案都应打折看待。
- **上下文腐烂**：一个月 95%→65%（Anthropic）。schema 与定义在变，agent 知识不变。
- **"堆语料"幻觉**：答案 80% 的时候就在语料里，但准确率不动。检索失败与结构缺失，不是资料缺失。
- **自动生成定义引入歧义**：LLM 写指标定义净负收益。
- **语义层范围外硬失败**：0% 覆盖，需要显式的降级路径，否则用户体验断裂。
- **把上下文当事后补丁**（nao 的总结）：**"每个失败的根因都一样——上下文被当成事后想起来的事，而不是数据团队应该工程化的首要对象。"**
- **安全**：service account 绕过 RLS、生成 SQL 进 exec()（CVE-2024-5565）、训练数据投毒。
- **组织**：无人拥有指标定义。dbt 的解法是把 analytics engineer 明确为治理所有者与 AI 上下文提供者。

**能力层级现状判断**：以上所有一手生产证据集中在 **L1~L3**（单句取数、多步自纠错、带异常检测/下钻/漏斗的分析）。**L4（规划与主动分析）目前只有 Anthropic 一家给出了可信的自动化率数字（95% 业务分析查询）**，且其前提是 L5 级的数据建设投入（canonical 数据集 + 人工治理语义层 + skills 进 CI）。**结论：L4 不是靠 agent 框架堆出来的，是靠 L5 的数据与治理基建换来的。**
