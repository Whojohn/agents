# Text-to-SQL / Data Agent 领域 SOTA 调研报告

调研基准日：2026-08-20 ｜ 证据时效线：2025-01 至今 ｜ 方法：10 名渠道调研员广度发现（~230 候选）→ 4 名组长深度验证（每条结论带一手来源）→ 交叉核对汇总。中间过程见 `research/phase1/`（执行路径+候选清单）与 `research/phase2/`（深度验证结论）。

**能力分级口径（全文统一）**：L1 单句 text-to-SQL → L2 多步查询/自纠错 → L3 分析与归因 → L4 规划与主动分析 → L5 数据建设与治理（建模/数仓/指标层）。

---

## TL;DR（十条硬结论）

1. **L1（单句 SQL）已基本解决且被小模型吃下**：1.5B 模型 BIRD-Dev 67.08、0.8B test 59.59、27B 免微调 test 78.42。继续投入单句准确率的 ROI 已很低；纯 text-to-SQL 开源项目（sqlcoder、Dataherald、MAC-SQL 等）2025-2026 全线停更，被通用大模型直接吞掉。
2. **主流榜单不可再按名次引用**：CIDR'26/PVLDB 论文实测 BIRD Mini-Dev 标注错误率 52.8%、Spider2.0-Snow 62.8%，修正后排名相关性从 r=0.85 掉到 0.32——BIRD Top-10 内的名次差没有统计意义；Spider2.0-Snow 因 gold 全公开已名义饱和（96.7% 不可采信）。BIRD 官方已认账整改（2025-11 发布清洗版 dev-1106，将移除 Oracle Evidence）。
3. **真实能力看四个数**：BIRD-Interact（交互式）16.33%、EntSQL（企业私域知识）15.9%、LiveSQLBench（抗污染）48%、DABstep validated hard 89.95%（含基准拟合成分）。任务越像真实分析，分数越低。
4. **学界权威判定当前 Data Agent 停在 "Proto-L3"**（两个独立分级框架结论一致）：缺全生命周期覆盖、缺未预定义算子处理、缺主动问题发现。L4/L5 目前只有考题（DAComp/FDABench），没有答卷。
5. **准确率的瓶颈不是模型，是语义层/口径**：dbt 2026 基准中语义层内题目两个模型都 100%，裸 text-to-SQL 仅 51-62%；Snowflake 加语义模型 +21pp（57→78）；Anthropic 内部无 skills 21% → 有 skills 95%。UC Berkeley "Tribal Knowledge"、EntSQL 15.9%、BIRD Oracle Evidence 是同一问题的不同表述。
6. **开源侧 star 数与可用性几乎无关**：Vanna（23.8k star）2026-03 已归档，pandas-ai 停更 10 个月，sqlcoder/Dataherald 死亡 2 年以上。真正代码活跃且到 L3+ 的开源不到十个；**唯一开源 L4 是港科大 DeepEye（仅 230 star）**。"会分析的（L3-L4）"与"会建设的（L5：altimate-code、dbt-agent-skills）"是两拨不相交的项目，端到端开源 Data Agent 尚不存在。
7. **商业产品 "agent" 一词已通胀，按官方文档裁定**：真 L4 只有 Databricks Genie One、Snowflake CoWork（原 Intelligence）、BigQuery Conversational Analytics、Qlik、火山引擎 Data Agent 五家；微软 Fabric Data Agent 文档自证只是 L2（只读、25 行×25 列上限）。L5 只有 Qlik Agentic Data Engineering 达到 GA，但零效果数据。
8. **纯 NL2SQL 公司已无独立价值**：2025-2026 六起并购（Numbers Station→Alation、Seek AI→IBM、Waii→Salesforce、DataChat→Mews、Pyramid→ServiceNow、Dremio→SAP），巨头买的都是语义层/知识图谱/湖仓底座。融资在流向两端：语义层底座（Omni $1.5B 估值、Sigma $200M ARR）与端到端 agent（TextQL 收入 9x、WisdomAI $73M）。
9. **落地路径已有共识**：先治理小范围数据资产（~20 张表舒适区）→ 开发前由业务专家写 10-20 道基准题 → 3-5 轮迭代（Databricks 实测 0%→54%→77%→100%）→ 语义层人工拥有、agent 只做有监督精修（LLM 自动生成语义层是净负收益）→ skills/语义层进 CI 防腐烂（Anthropic 实测不维护一个月 95%→65%）。
10. **失败第一杀手是静默错误**（fan-out join 虚增、口径歧义给出错数而非报错），其次是"学术分数到生产的断崖"（Spider1.0 91% → Spider2.0 21%；LinkedIn 生产系统自评仅 53% 正确）。

---

## 一、基准与学术 SOTA（详见 `research/phase2/L1-academic.md`）

### 1.1 榜单可信度裁定（先打折，再看分）

| 榜单 | 可信度 | 要点 |
|---|---|---|
| BIRD Overall (test) | 中等，只看量级 | 榜首 AskData+GPT-4o 81.95（2025-12）、蚂蚁 Agentar-Scale-SQL 81.67（2025-09）；人类基线 92.96；全部依赖将被移除的 Oracle Knowledge；8 个月榜首零前进，已失去区分度 |
| Spider 2.0-Snow | 不采信 | gold 全公开 + 62.8% 错标下的 96.7% 是过拟合；同题 Lite 榜首仅 76.23、DBT 65.6 |
| BIRD-CRITIC | 陈旧快照 | 全部条目停在 2025-04，榜首 o1-preview 35.5% 不能当今日上限 |
| BIRD-Interact | 最有信息量 | GPT-5 主动交互模式仅 17%——主动澄清/交互是当前最大短板，而它是 L3 归因的前置能力 |
| LiveSQLBench | 设计最抗污染 | SOTA 48%，比 BIRD 的 81% 更接近真实能力 |
| DABstep | 必须区分 validated | 2179 条提交仅 28 条 validated（1.3%），未验证池有 16 条自称 100 分；validated hard 曲线 13 个月从 9% → 89.95%（NVIDIA KGMON），是唯一真实且剧烈的进步曲线 |

引用卫生规则：厂商普遍拿 easy split 冒充总分（如流传的 "Energent 94.4%" 实为 easy，其 hard 仅 57.67）。

### 1.2 方法谱系

- **RL/执行反馈（L1 降本路线）**：Arctic-Text2SQL-R1（只用执行正确性奖励，7B 打赢 70B）vs Reasoning-SQL（四类部分奖励+GRPO）——两者主张相反且分差落在标注噪声内，路线优劣未决。
- **Test-time scaling（L1-L2 堆算力）**：Agentar-Scale-SQL（蚂蚁，BIRD 81.67）、ReFoRCE（Snowflake）——有效但边际收益已尽。
- **软件工程化范式（最值得进生产）**：DeepEye-SQL（SIGMOD'26）：schema linking 关系闭包 + N-version 生成 + 确定性校验工具链 + 执行引导裁决，~3B 激活参数免微调 BIRD test 78.42。
- **小模型路线**：SLM-SQL 1.5B 达 67.08——L1 已被吃下。
- **Data Agent 侧**：DeepAnalyze（8B 端到端，Proto-L3）、Google DS-STAR（DABstep hard 45.24，已证 L3 但一半任务仍失败）、NVIDIA KGMON（"重模型离线蒸馏工具库 → 小模型在线调用"方法论被验证，Haiku 4.5 推理快 30 倍）。
- **两个被忽略的维度**：成本效率评测完全缺席（agent 会写正确但极贵的查询）；SQL 与 LLM 正在融合成新原语（Spider2.0-AIFunc：AI 函数进 SQL，L1/L3 边界将消失）。

---

## 二、开源项目格局（详见 `research/phase2/L2-opensource.md`，全部按 `pushed_at` 真实代码推送核实）

### 2.1 生产可用第一梯队（代码活跃 + 发行证据）

| 项目 | star | 最近代码 | 层级 | 定位 |
|---|---|---|---|---|
| DB-GPT | 19.8k | 2026-08 | L3（局部 L4/L5） | 中文圈唯一覆盖查询/分析/建模/微调的成体系开源栈，MIT |
| WrenAI | 17.3k | 2026-08 | L2+语义层 | MDL 语义层换正确性，主动放弃自主推理 |
| Chat2DB | 28.0k | 2026-08 | L1-L2 | AI 增强 SQL 客户端（已迁至 OtterMind 组织） |
| Cube | 20.7k | 2026-08 | L5 基础设施 | 开源语义层，agent 的口径地基 |
| SQLBot | 6.6k | 2026-08 | L1-L2 | 飞致云中文问数，月度发版，注意 GPLv3+ 限制 |
| SuperSonic | 5.0k | 2026-08 | L2+语义层 | 腾讯音乐 ChatBI+Headless BI |
| nao | 1.6k | 2026-08 | L3 | 上下文工程 + dbt 集成 + 自带 agent 评测框架（开源罕见） |
| altimate-code | 0.8k | 2026-08 | **L5** | 2026 新：dbt 脚手架/列级血缘/测试生成/FinOps，数据建设 agent 最实形态，MIT |
| dbt-agent-skills | 0.7k | 2026-08 | **L5** | dbt Labs 官方，把建模工作流固化为 agent 技能 |

### 2.2 关键判定

- **唯一开源 L4：HKUSTDial/DeepEye**（230 star，SIGMOD Demo 2026）——意图分解→分层规划→拓扑调度→自动产出报告/仪表盘/数据视频，完整可跑。星数最低、含金量最高。
- **真 L3 仅 5 个且各有硬伤**：DB-GPT（复杂度高）、openchatbi（唯一把 Adtributor 归因做成一等公民，单人维护）、Auto-Analyst（偏 dataframe）、agno dash（自学习+Engineer agent 沉淀数据资产，template 形态）、nao（自定义许可证）。
- **已衰退需降级**：Vanna（归档）、pandas-ai（停 10 个月）、sqlcoder（27 个月）、Dataherald（25 个月）、MAC-SQL（18 个月）；XiYan-SQL 整条开源线 2026 年明显降速（模型仓 2025-09 起停更）。
- **许可证风险**：Aix-DB/DataMind/OmniSQL/MAC-SQL 无 LICENSE（不可商用）；QueryWeaver AGPL。
- **结构性结论**："会分析的"与"会建设的"完全不相交；端到端（问数→归因→建模→治理）开源 Data Agent 在 2026-08 时点不存在——这是空白，也是机会。

---

## 三、商业产品格局（详见 `research/phase2/L3-commercial.md`）

### 3.1 层级判定（不看营销词，只看官方文档四个开关：能否写 / 能否调度 / 能否跨轮记忆 / 能否对外执行动作）

| 层级 | 产品 | 判据要点 |
|---|---|---|
| L1-L2 | **Microsoft Fabric Data Agent**、Snowflake Cortex Analyst 本体、阿里云 DMS ChatBI/PolarDB、帆软 FineChatBI、ThoughtSpot（确定性路线）、Kyligence | Fabric 文档自证：严格只读、最多 5 数据源、响应上限 25 行×25 列；Cortex Analyst 自述无跨轮结果记忆 |
| L3 | 腾讯云 ChatBI（Delta/Shapley 统计归因，非 LLM 自由发挥）、AWS SageMaker Data Agent、WisdomAI、Julius、Hex、观远/衡石 | 有归因/解读，但不主动、不规划长任务 |
| L4 | **Databricks Genie One**（2026-06 GA）、**Snowflake CoWork**（原 Intelligence，2026-06 更名，L4 能力多在预览）、**BigQuery Conversational Analytics**（2026-07 GA，归因做成 SQL 原语 AI.KEY_DRIVERS）、**Qlik**、**火山引擎 Data Agent**（规划器+反思器+执行器，抖音集团 10 类岗位 36 类任务） | 多步规划 + 定时/告警主动触发 + 产出报告 + MCP 对外动作 |
| L5 | 仅 **Qlik Agentic Data Engineering** GA（数据产品/质量/目录/管道四 agent），零效果数据；Genie ZeroOps、Cortex Sense 均私有预览 | 宣称远多于交付 |

### 3.2 商业侧硬数据（全网仅此几组）

- 准确率：Snowflake BIRD 57%→78%（+21pp，语义模型，2025-03 原始出处）；蚂蚁 Agentar-Scale-SQL BIRD EX 81.67% 双榜第一（已开源 32B 模型）；Fabric "GPT-5.X 内部基准 +20%"（不可复现）。**Databricks/Google/Tableau/Qlik/全部国内 BI 厂商：零准确率数字——选型时的重大风险信号**。
- 规模：Snowflake 1000+ 客户 15000+ agent、9100+ 客户周活；Databricks 150 万 Genie Spaces；Sigma ARR $200M/$3B 估值；Omni $1.5B 估值/收入 4x；TextQL 收入 9x/NDR>300%；Julius 200 万用户/ARR $15M+。
- 并购（六起全部核实）：Alation←Numbers Station、IBM←Seek AI、Salesforce←Waii（成为 Tableau 下代语义引擎底座）、Mews←DataChat、ServiceNow←Pyramid、SAP←Dremio。规律：**买的全是语义层/知识图谱/数据底座，纯 NL2SQL 引擎已无独立公司价值**。
- 特色路线：ThoughtSpot Spotter Semantics 坚持确定性 search-token 编译、明确不用 LLM 生成 SQL（"绕开准确率问题"派）；帆软 Text2DSL（把不可控一步拆成人可审的两步）；Aloudata "100% 准确" 宣称需打折（100% 只在 MQL→SQL 编译段，NL→MQL 仍是 LLM 推断）。

---

## 四、落地实践：准确率之外的问题（详见 `research/phase2/L4-production.md`）

### 4.1 冷启动——"补上下文"有效，"堆语料"无效

- **Anthropic（一手，最强证据）**：无 skills ≤21% → 有 skills ≥95%。两个反直觉结论：① 把历史 SQL 语料全给 agent，答案 80% 情况就在语料里，但准确率几乎不动（<1pp）；② **LLM 自动生成语义层是净负收益**——"Claude 起草文档，人类拥有定义"。
- **边界条件（Snowflake）**：agent 自动化流水线可以在**有 ground-truth 监督下**把语义模型精修出 +21pp。结论：**语义层可以被 agent 自动"精修"，不能被 agent 自动"发明"**。
- **可复制 SOP（Databricks）**：单 Genie Space 五轮迭代 0%→54%（补元数据）→77%（自定义指标)→100%（领域规则）；基准题 10-20 道、开发前由业务专家写好、>80% 才进 UAT。
- **中文一手量级**：FreeWheel 标注 400+ 选表示例、300+ SQL 示例（用 SQL2Text 反向放大语料），全流程准确率 90%+；贝壳 93% 的前提是根本没做通用 text-to-SQL——建在已治理的指标宽表平台上。

### 4.2 口径一致性——语义层的真正价值

dbt 2026 基准：语义层内题目两模型 100%，裸 text-to-SQL 51-62%；范围外语义层 0%（确定性报错）。总结句：**"语义层的失败是一条错误消息；text-to-SQL 的失败是一个错误的数字。"** 三条诚实的反向证据：更好的建模对两边都有效（+20-26pp）；语义层对未定义问题硬失败，需要显式降级路径；规模是真瓶颈（当前工具舒适区约 20 张治理良好的表）。仓库原生语义层 2026 已成标准件（Snowflake Semantic Views、Databricks Metric Views 先后 GA）。

### 4.3 维护与防腐烂

- **不维护的腐烂速度：一个月 95%→65%（Anthropic 实测）**。解法是工具强制而非流程：skills 与数据转换代码同 repo，code-review hook 强制数据模型 PR 同 diff 带 skill 变更（达成率 90%）。
- 角色变化：analytics engineer → 系统设计者/治理所有者/AI 上下文提供者（dbt，"治理已成首要交付物"）。
- 增量沉淀模式：每个好查询变上下文、每个错误变规则、每次澄清变共享知识——只更新检索知识、不动权重、人工可审。

### 4.4 兜底与信任（四层防线已收敛为标准动作）

① schema 动态检索 + 业务术语表注入；② 执行前 AST 校验（拒绝 DDL、无 LIMIT 全表扫）+ 仅 SELECT + 默认时间范围 + 自动 LIMIT；③ 只读凭据 + 行级安全 + 超时 + 全量日志（注意 service account 广权限绕过 RLS 是最普遍结构性漏洞；Vanna CVE-2024-5565 生成 SQL 进 exec 致 RCE）；④ 执行后二次 LLM 校验 + 合理性检查 + 溯源脚注；评测集 20-50 道起步、来自真实失败、越早建越容易。超出支持范围时主动说"不支持"并推荐替代——报错优于错数。

---

## 五、趋势判断与选型建议

1. **赛道重心已从 "更准的 SQL" 移到 "可信的分析"**：L1 商品化（小模型+平台内置），L3-L4 是 2026 竞争主战场，L5 是资本与并购的方向但产品未到。
2. **语义层/指标层是整个故事的必经之路**——学术（Tribal Knowledge/EntSQL）、商业（并购标的全是语义资产）、落地（所有成功案例）三线证据完全一致。**自建顺序：先治数据和口径，再上 agent；反过来必然失败**。
3. **交互能力是下一个突破口**：BIRD-Interact 17% 说明主动澄清/交互是最短板，而它是归因分析的前提；评测范式正整体从静态转向交互（BIRD 官方转向、火山引擎评测体系同构）。
4. **可复用的技术范式**：N-version 生成+确定性校验+执行裁决（DeepEye-SQL）；重模型离线蒸馏工具库+小模型在线调用（NVIDIA KGMON）；有监督的语义层自动精修（Snowflake）；中间表示可干预（Text2DSL/MQL/search-token）。
5. **空白与机会**：端到端开源 Data Agent（分析+建设不相交）；成本感知的查询生成与评测；语义层的自动化维护（当前唯一有效机制是 CI 强制）。
6. **选型速查**：要托管平台看 Genie One / CoWork / BigQuery CA（注意 CoWork 多数 L4 能力在预览）；要开源自建从 DB-GPT 或 WrenAI+Cube 起步，分析深度补 DeepEye/openchatbi 思路，数据建设配 altimate-code/dbt-agent-skills；国内看火山 Data Agent（最接近 L4）与腾讯 ChatBI（归因最实）；蚂蚁 Agentar 是可自部署的 BIRD SOTA 开源模型。

---

## 附：可信度声明

- 所有榜单分数来自官方榜单页原始 HTML 解析或官方数据集复算（DABstep 为 985,050 条原始记录 DuckDB 重算，与 NVIDIA 官方博客逐位吻合）；GitHub 活跃度全部按 `pushed_at`（真实代码推送）核实，纠正了广度阶段把 star/issue 活动误当代码更新的偏差。
- 已剔除并记录的不实/存疑信息：Spider2.0-Snow 饱和分数、DABstep 未验证榜、"Energent 94.4%" 类 easy 充总分、Aloudata "100% 准确"、Silicon Data（误入候选，实为 GPU 定价公司）、一汽 GPT-BI 数字（超时效线且不可溯源）等，明细见各 L 文件"剔除"节。
