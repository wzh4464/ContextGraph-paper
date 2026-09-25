# ContextGraph（v1.0）ICLR 2027 审稿意见与 Best Paper 修改路线图

> **审稿对象**：tag `v1.0`（commit `e5203d2`）的完整 LaTeX 源码、附录，以及 `figures/scripts/*.json`。没有参考提交历史。
>
> **评审方法**：
> 1. 7 位独立审稿人分别从 rigor、fairness、novelty、method、consistency、best-paper、presentation 七个视角写完整审稿；
> 2. 每条弱点由一位对抗式核查员回到源文件尝试反驳，结果为 confirmed 55 条、overstated 46 条、refuted 0 条；
> 3. AC 汇总成元评审；
> 4. 完整性审查员复核元评审，其指出的错误都已人工核实并在本文中修正。
>
> **行号约定**：下文中不带文件名的 `L<n>` 指 `main.tex` 的行号。

---

## 0. 结论速览

- **推荐：3（Reject），置信度 4/5。** 七个视角中有六个给 3，presentation 给 5。
- **问题出在推断与归因，而不是算术。** 论文里的差值、半宽、McNemar p 值都能复算对上，数据隔离审计也做得扎实。问题在于：
  - 按论文自己的保守区间（Table 7），能站住的只有两项：Verified500 和 Related-Lite99 相对 no memory 的增益（后者只比半宽高 1.3 pp）。
  - 以下主张都落在噪声内，却写进了摘要、Findings 和结论：
    - "在每个 benchmark 上都是最高"；
    - DeepSWE113 的增益；
    - 大部分组件消融；
    - 跨仓库迁移；
    - 跨 backbone 与 pool size 的趋势。
  - 标题里的机制 **condition matching 从没有被单独隔离过**，Limitations 也自己承认了这一点。
- **冲击 best paper 的核心改造**：从"又一个在排行榜上赢了的记忆系统"，转向"**coding agent 的经验记忆何时、为何有效**"的因果性回答。具体包括：
  - 预先登记竞争假设，做因子化的干预实验；
  - 配对统计、ITT 指标、成本对等；
  - 一个能做样本外预测的简单模型；
  - 一个可复用的 continual-SWE 评测协议；
  - 一个极简实现。

  坦白说：即使全部做完，拿 Outstanding Paper 的概率也不高。但这是把概率最大化的路线，而且做完后会是一篇扎实的 accept。

---

## 1. 论文概述

ContextGraph 是一个面向 coding agent 的经验记忆系统：
- **蒸馏**：用 Claude 4 Sonnet 把过去的成功和失败轨迹蒸馏成 strategies 和 warnings，每条附带 applicability condition 与 intended outcome。
- **存储**：存进一个有 8 类节点、7 类关系的 typed graph（Eq. 1，Table 12）。
- **检索**：agent 在规划前和出错后，用工具自行搜索这个图（agent-directed selection，Eq. 2）。
- **更新**：每个任务结束后，把轨迹在线蒸馏回图中。

**主实验**（DeepSeek V4 Pro 0813 + mini-SWE-agent）：

| Benchmark | ContextGraph | 相对 no memory |
|---|---|---|
| Verified500 | 69.2% | +7.6 pp |
| Related-Lite99 | 35.1% | +13.7 pp |
| DeepSWE113 | 72.1% | +11.3 pp |

在 7 个记忆方法中，ContextGraph 的点估计在三个 benchmark 上都最高。

**附加实验**：
- Gemini 3.1 Pro + live-SWE-agent：Verified pass@1 从 82.3% 升到 88.9%；
- LoLBench 20 题：3/20 对 1/20。

**核心科学主张**来自 Related-Lite99 上的消融：raw trajectories（20.5）和 static playbook（20.8）都"停在 no-memory 水平"（21.4）。作者据此提出"抽象 + 条件匹配"这一 recipe，并写进了标题。

---

## 2. 评分

| 视角 | 评分 | 置信度 | 核心依据 |
|---|---|---|---|
| Rigor | 3 | 4 | Table 7 的 16 项里只有 5 项超过半宽；没有 run 级方差和配对检验；单次运行与五次均值混用 |
| Fairness | 3 | 4 | distiller、访问接口、更新方式、预算口径都不对等；最接近的竞争者 LangMem 只跑了一个 benchmark |
| Novelty | 3 | 4 | 各组件均有先例；标题里的机制没有被隔离；graph 的贡献为 −4.0±13.1 |
| Method | 3 | 4 | condition 没有形式化；Select、排序函数、k、工具 API、prompt、构图算法均未给出 |
| Consistency | 3 | 4 | no-memory 参照在不同实验间漂移 7–11 pp；分母口径不统一；多个五次均值不可能来自完整运行 |
| Best-paper | 3 | 4 | 证据脆弱；insight 与 AutoGuide、CLIN、MTL，以及 bib 中未引用的若干 2026 年工作高度重叠 |
| Presentation | 5 | 4 | 结构清楚，但主张与证据不匹配；Limitations 放在全部附录之后 |
| **AC 综合** | **3** | **4** | |

**升分条件**（写给作者看的明确方向）：
- **升到 5**：解释 no-memory 漂移（C3）；在 ITT 与配对分析下，Verified500 和 Related-Lite99 仍然显著；按证据改写全部主张。
- **升到 6**：满足下面两条之一，同时让 LangMem 跑完全部 benchmark：
  - 在选择阶段做的 condition-stripped 实验显示出显著效应；
  - 或者，把贡献重新定位为经过检验的替代机制（见 C4）。
- **8 及以上（冲奖区间）**：见 §6。

---

## 3. 主要优点

- **S1 评测覆盖面广，控制相对到位。**
  - 所有方法共享同一个 agent、backbone 和预算：500 steps，Verified500 与 Related-Lite99 为 $20，DeepSWE113 为 $50，LoLBench 为 $100（L161–163）。
  - 作者自己改写的 baseline 用 † 标出（Fig. 3，Table 6）。
  - Fig. 4 在三个 backbone 上加了四组对照：Mem0、LangMem、random summaries、oracle。
- **S2 数字可追溯，不确定性报告相对诚实。**
  - Table 7 只加粗超过半宽的差异，对自己不利的也照实标出（DeepSWE 为 11.3 对 12.2）。
  - Table 9 的 exact McNemar p 值与不一致计数吻合（0/7→.016，1/8→.039）。
  - JSON 数据与表格一致。
- **S3 数据隔离工作扎实。**
  - Table 8 对每个初始池都做了实例级审计，以及 token-Jaccard ≥ 0.85 的补丁相似度审计，分别移除 18、6、3、5 条。
  - 还做了检索期日志检查。
  - 对于审计之前就存在的 curated pool，作者主动披露，并给出 89 题的敏感性分析。
- **S4 有两个有信息量的负对照。** raw trajectories 和 static playbook 两个设计本身很有价值；"更多上下文 ≠ 有用的记忆"与 SWE-ContextBench 中 free context 为 +0.00 的结果一致。不过它们在统计上能支持什么，要打折扣，见 C1。
- **S5 在强 backbone 上仍有收益，且更省 token。**
  - Verified500：+7.6，半宽 5.9；每任务 token 从 236K 降到 201K，减少 14.8%（口径见 M1）。
  - Gemini pass@1：+6.6，半宽 4.3，但有前提，见 M3。
- **S6 分析工具有价值，披露坦诚。**
  - 逐 lesson 记录来源仓库（Table 5），按 stream 三分位统计首轮结果（Table 4）。
  - Appendix G 把已发表的参考数字与本文运行分开，并指出 Supermemory 的 55.95% 是 FAIL_TO_PASS rate。
  - 代码、prompt 和 schema 的发布目前只是论文中的声称（匿名链接），审稿时无法核实。

---

## 4. 主要问题

### 致命（Critical）

**C1. 标题中的机制"condition matching"从未被隔离；"停在 no-memory 水平"是数据支持不了的等价性主张**

- **证据**
  - 标题写的是 "Condition-*Matched*"。另外三处相关表述：
    - 摘要 L29–34："match each lesson to the condition under which it applies"；
    - 贡献 2（L125–128）："We identify what makes coding-agent memory work: abstraction and condition matching"；
    - §5.3 Finding（L278–280）。
  - 唯一的支撑是 static playbook。按 L264–266 的定义，这个变体**同时**去掉了五样东西：按任务选择、在线更新、出错后检索、读取 source，以及注入位置（改放进 system prompt）。Limitations（L468–471）也承认它混淆了 "condition matching together with per-task memory access"。
  - condition 在 Eq. 1、Table 12 的 schema、Algorithm 1 中都没有表示，只在 §4.1 的文字里出现。Fig. 1(a) 和 Fig. 2 都把它标成 "Context"。
- **"停在 no-memory 水平"（L33、L114、L127、L272）是等价性主张。** 显著的其实是"full − 变体"这个差，而这个显著性是从 CG−NM（13.7/12.4）继承来的。真正有信息量的是变体相对 no memory 的差：

  | 变体 − no memory | 差值 | 95% CI |
  |---|---|---|
  | raw | −0.9 | 约 [−12.2, +10.4] |
  | static playbook | −0.6 | 约 ±11.4 |

  这两个区间都排除不了"raw 带来约 10 pp 收益"的可能。
- **raw 臂本身也有混杂。** Related-Lite99 的初始池是 300 条 summary（L398–400，supplement L6–10），所以 raw 臂的 "trajectory excerpts" 只能来自另一个池，而且它跳过了 Claude 4 Sonnet 的蒸馏。于是"抽象"和池来源、格式、长度、distiller 是绑在一起的。
- **修复**
  - 做 Limitations 自己提出的 **condition-stripped** 变体，并且要在**选择阶段**去掉 condition：agent 在已删除 condition 字段的池上做实时选择。另加一组"condition 在 lesson 之间打乱"的实时选择对照。
  - 在这些实验完成之前：
    - 把 "stay at the no-memory level" 改为 "do not significantly improve over no memory"；
    - 把 "identify" 改为 "provide evidence consistent with"；
    - 标题中去掉 "Condition-Matched"。

**C2. 摘要、Findings 和结论的主张超出了论文自己的统计证据**

Table 7 的 16 项里只加粗了 5 项：Verified500 7.6/5.9、Related-Lite99 13.7/12.4、Gemini 6.6/4.3、raw 14.6/12.3、playbook 14.3/12.3。其余被写成定论的比较如下：

| 不显著或不可靠的比较（差值/半宽） | 正文表述 |
|---|---|
| DeepSWE113 相对 no memory：11.3/12.2 | 摘要 L27，无条件陈述 |
| 相对最强 baseline：2.2/5.8、3.8/13.1、5.9/12.0；相对 LangMem：1.1/约 13.2 | "highest rate … on each" |
| 四个组件消融：10.8/12.6、6.4/13.0、4.0/13.1、1.9/13.2 | §5.3 "each add further gains"；结论（L444–448）的四条实践有三条依赖这些 |
| 三个 other-repositories-only 效应：1.4/6.0、7.3/12.0、6.7/12.5 | §5.5 "worth building" |
| Kimi 28/98 对 18/97、MiniMax 27/98 对 19/98，都是单次运行 | §5.6 "improves with all three backbones" |
| pool size：50–200 是单次运行，300 是五次均值；50 条时的 20.2 低于 no memory 的 21.4；最大的一跳（+6.8）恰好落在聚合方式切换处 | "collecting more experience pays off"（L436） |
| LoLBench：3/20 对 1/20（Fisher p≈0.60） | "the only memory method that solves more"（L252） |
| static CG − 在线 ExpeRepair：−2.6/12.8；Kimi 与 MiniMax 的差值 | Table 7 **没有列出**，挑选比较项本身有选择性 |

- **Related-Lite99 的 13.7 也只是"有条件显著"。** 它只比半宽高 1.3 pp，而同一批 99 题上 no memory 在不同实验间漂移了 7 pp（见 C3）。如果按 SWE-ContextBench 原始的固定池协议，对应的是 static pool 28.7−21.4 = 7.3，半宽 12.0，不显著。另外，所有消融、pool size 和跨模型实验都只在这个增益最大、且协议被改过的 benchmark 上做，没有留出 benchmark 来做设计选择。
- **方法层面**
  - 非配对区间忽略了配对（配对会让区间更窄），但也忽略了 run 间方差，以及在线更新带来的任务间相关。对 online 组来说，这个区间不一定保守。
  - 所有五次均值都没有给出 per-run 值或 SD。
  - Verified500 很可能只跑了一次（9 个值全部是 k/500，文中也没有说明）。
  - 没有做多重比较校正。
  - 主文从未引用 Table 9 中不显著的复现：V3.2 exp p=.39，Kimi p=.73。
- **修复**
  - 用已有的 per-task 结果做配对推断：单次运行用 exact McNemar；五次运行用 task×run 两级 bootstrap，或 mixed-effects logistic（success ~ method + (1|task) + (1|seed)）。
  - 按比较族做 Holm 校正，报告 run 级 SD，在 Fig. 3/4 和 Table 3/5 中直接画出 CI。
  - 摘要改为："在 Verified500 与 Related-Lite99 上显著优于 no memory；相对最强 baseline 为数值最高，差异在噪声范围内"。
  - LoLBench 降级为 case study。

**C3. no-memory 参照在不同实验之间漂移 7–11 pp，文中没有解释**

下表都是 Related-Lite99 上的 no memory：

| backbone | 来源 | 数值 | 说明 |
|---|---|---|---|
| DeepSeek V4 Pro | 主比较（Table 3/6） | 21.4% | 五次均值 |
| DeepSeek V4 Pro | retry 实验（Table 4） | 14.2/99 ≈ 14.3% | 五次均值；L313 称用的是 "main-comparison budget" |
| DeepSeek V4 Pro | Table 9 | 14.14% | |
| Kimi K3 | Fig. 4 | 18/97 = 18.6% | |
| Kimi K3 | Table 9 | 29.29% | 甚至高于 Fig. 4 中 Kimi 的 ContextGraph（28.6%） |

- no-memory 组不接触任何记忆池，本不应随记忆配置变化。两个五次均值相差约 7 题，远超 run 噪声，指向**没有披露的协议差异**。
- 可见的线索：§5.4 和 Table 9 都没写 "0813"；episodic 配置没有说明 scaffold（supplement L13–15）。
- **影响**：§5.4 被用来说明"主协议下在线更新的收益如何累积"（L311–313），这条跨实验推理因此不成立。读者也无法判断主结果对应的是哪一套配置。
- **修复**：逐实验**如实**列出 scaffold commit、模型 snapshot、prompt、temperature、harness 版本、运行日期和分母；每个实验中 no memory 与记忆组同批次并行运行。如果确实存在协议差异，就在主协议下重跑 §5.4。注意：不要为了"统一"去改型号名，要如实标注每个实验实际用的 snapshot。

**C4. 一个更简单的替代解释没有被排除：CG 的独有优势可能来自"流内在线积累（尤其是同仓库经验）+ agentic 检索"，而不是抽象、condition 或 graph**

- **静态或通用的记忆在 Related-Lite99 上都挤在 +5 到 +7 pp 一带**：

  | 方法 | Resolution (%) |
  |---|---|
  | random summaries | 27.1 |
  | oracle | 27.8 |
  | FAISS | 26.8 |
  | Mem0 | 26.8 |
  | Supermemory | 26.5 |
  | ACE | 28.1 |
  | **static CG（关闭在线更新）** | 28.7 |
  | **other-repos-only CG** | 28.7 |

- **明显更高的只有做流内积累的方法**：CG 35.1、ExpeRepair 31.3；LangMem 34.0 的更新方式没有说明。static CG 与 random summaries 基本相同（28.7 对 27.1）。
- **两个 28.7 本身有信息量**：
  - other-only 排除了同仓库 lesson，包括在线新增的那部分；
  - static pool 排除了全部在线 lesson。

  两者相等，正是"Related-Lite99 上的在线收益几乎全部来自同仓库的在线 lesson"这一假设所预测的结果（这两个值也可能来自同一批运行，需要作者说明）。
- **Verified500 上方向相同**：78.4% 的选中 lesson 来自其他仓库，但 other-only 只有 +1.4±6.0；少数同仓库 lesson 贡献了 6.2 pp。这属于在测试流上学习，而不是跨仓库迁移。
- **泄露的疑虑**：审计只用了 Jaccard ≥0.85 这一个阈值。本文 curated 池在 99 个目标中就有 10 个近重复，说明近重复在这个领域很常见。如果存在低于阈值的泄露，最可能正好体现在同仓库这 6.2 pp 上。
- **修复**：把它列为首要检验的竞争假设 **H1**（见 §6），具体包括：
  - 做 2×2 分解：{初始池, 在线} × {同仓库, 跨仓库}，给出配对 CI；
  - 统计选中 lesson 来自 benchmark **已标注相关前驱**的比例；
  - 在 Jaccard 0.5 和 0.7 阈值下重算同仓库部分的增益。

### 重大（Major）

**M1. 对比协议不对等：distiller、更新方式和预算口径**

- **Distiller**：ContextGraph 用 Claude 4 Sonnet 蒸馏（L164）。以下各处的蒸馏或反思模型都没有说明：
  - 所有 baseline；
  - Fig. 4 里那 300 条 summary；
  - Gemini 和 LoLBench 两组实验。

  由另一个模型往记忆里写入知识，所以摘要中的 "self-improving" 并不严格成立。bib 中有一篇 distill2026（"Agent Memory Distillation … Hierarchical Teacher Memory"）讨论的正是这种 teacher-memory 效应，但没有引用。
- **更新方式**：Table 2 caption（L173）写的是 "baseline updates follow each implementation's default behavior"。
  - 按 Table 1，ReasoningBank、ACE、ExpeRepair、Supermemory 都在线更新，ExpeL 不更新，FAISS Flat 没有说明，所以并不是整体不对称。
  - 真正的问题有两点：
    - 更新粒度、信号和所用 LLM 都没有说明，而 ExpeRepair 和 ACE 的"默认行为"由作者自己的改写决定；
    - 关闭在线更新后的 ContextGraph（28.7）**低于**在线的 ExpeRepair（31.3），与 ACE（28.1）持平，但 §5.3（L277）只拿它和最弱的 ExpeL（20.7）比，说 "stays 8.0 points above"。
- **预算与成本**
  - 没有说明以下几项是否计入 500 steps / $20：memory 的搜索与读取动作、每个任务一次的蒸馏调用、text-embedding-3-large 的调用。
  - 45,115 个节点的构图成本没有报告。
  - "201K versus 236K"（L246）的 token 对比有四个问题：只和 no memory 比、只在 Verified500 上、没有方差、没说明是否包含蒸馏。它还和成功率混杂，因为成功的任务往往更早结束。
- **修复**
  - 所有方法用同一个 distiller，另做一组 backbone 自蒸馏；
  - 所有支持更新的 baseline 在同一个 stream 上逐任务更新；
  - 给出完整成本表：agent 循环、memory 工具调用、蒸馏、embedding、摊销后的构图成本；
  - token 对比按任务配对，并按结局分层。

**M2. 访问接口可能不对等；最接近的竞争者 LangMem 在主表中缺席**

- **fixed top-k 的结果**：只有 ContextGraph 在 Table 1 的 Selection 列中标为多步 agentic search。换成 fixed top-k 后，它只有 24.3，**低于** FAISS Flat（26.8）、ACE（28.1）、ExpeRepair（31.3）。也就是说，在 baseline 所用的接口下，lesson 格式加 graph 并没有胜过普通向量检索。这些差异都在噪声内，但方向不利。
- **LangMem 是否接口对等**：LangMem 的标准用法本身就是 agent 调用 memory 工具，而论文没有说明它是怎么接入的。
  - 如果它是以工具方式接入的，那它就是接口对等的对照。此时它在 Related-Lite99 上拿到 34.0 对 35.1，也就是 no-memory 增益的约 92%，说明 lesson 格式加 graph 几乎没有额外贡献。
  - 同时，摘要里 "on each" 指的三个 benchmark 中，LangMem 在 Verified500 和 DeepSWE113 上都缺席；Mem0 同样如此。
- **Fig. 4 的聚合口径**：DeepSeek 列的 Mem0 26.8、LangMem 34.0、oracle 27.8 都不能写成 k/495，却恰好等于 26/97、33/97、27/97。这提示它们可能是单次运行，而与之比较的 CG 是五次均值。
- **缺少统计**：k、每个任务选中的 lesson 数、memory 调用次数与 token 都没有报告。
- **修复**
  - 说明 LangMem 的接入方式；
  - LangMem 与 Mem0 跑全部 benchmark，并加入 Table 7；
  - 把同一个 agentic search 工具开放给 ReasoningBank、ExpeRepair、LangMem 各自的存储；
  - 报告选择统计，并加一个按 lesson 数和 token 数匹配的 top-k 变体。

**M3. retry 和 pass@k 的收益混入了同任务的自我反馈，协议也不是标准做法**

- **同任务 lesson 可被检索**：experience-memory.tex L109–111 写明，重试一个未解决的任务时 "can select the lessons distilled from its own earlier failure"，overlap-audit 也确认了这一点。
- **信息泄露**：哪些任务进入重试，对三组是对称的；但只有记忆组能检索到本任务上一次尝试的 lesson。而"被再次尝试"本身就隐含了"官方判定失败"，相当于 **1 bit 的标签泄露**，与 L199–201 的精神相悖。这些 lesson 还是 Claude 4 Sonnet 写的，等于一个更强的模型对同一任务做了反思。
- **Gemini**
  - 尝试是顺序进行的，每次尝试后更新记忆（L240–241）。
  - no memory 的 pass@1→pass@5 只从 82.3 升到 82.8，看起来接近确定性解码，文中也没给 temperature。
  - 82.3、88.9、91.7 都不是 k/500 的形式，而 82.6、90.4、82.8 是。如果 pass@1 是多次顺序尝试的平均，那么 **pass@1 本身也被同任务反馈污染了**。所以 Gemini 的 +6.6 是有条件的显著。
  - L243–244 把 Gemini 的 pass@k 上升归因于 "the effect that Section 5.4 isolates"，但 §5.4 用的是不同的 backbone、benchmark 和记忆配置。
- **LoLBench**：pass@3 = 25.0 有同样的混杂，而 baseline 都没有报告 pass@3。
- **retry 实验**
  - 用的池是 291 条带参考修复和验证提示的记录，早于审计；
  - 89 题的敏感性检验只跑了一次、只看首轮、只和 no memory 比，没有覆盖 online 对 static 的比较；
  - stream 的结论只依赖一个差异（8.6 对 5.6，满分 33），没有 CI，没有交互检验，五次运行用的是同一个任务顺序。
- **修复**
  - 把指标改名为 "sequential attempts with memory"。
  - 增加三组对照：
    - no-memory Reflexion，反思者同样用 Claude 4 Sonnet；
    - temperature > 0 的独立采样，配合无偏 pass@k；
    - 排除同任务 lesson 的 ContextGraph。
  - 说明 Gemini pass@1 的估计量。

**M4. 以"已完成评测"为分母，完成率却没有报告；ContextGraph 自己很可能也有未完成的评测**

- L156–157 和 Table 6 脚注都以已完成评测为分母，但主比较没有给出完成率。
- 按"五次完整运行的均值必为 k/495（Related-Lite99）或 k/565（DeepSWE113）"逐项反推，以下数值**都不可能**来自五次完整运行：
  - Related-Lite99：CG 35.1、FAISS 26.8、ExpeL 20.7、RB 24.9、fixed top-k 24.3、raw 20.5、planning-only 33.2；
  - DeepSWE113：CG 72.1、no memory 60.8、ExpeL 58.7、RB 61.7、other-only 67.5。

  如果先把每次运行的比率四舍五入再求平均，其中部分值仍能解释，所以这只能作为给作者的问题，还不能下定论。
- Table 11（dev50）是唯一给出完成率的表。CG 的完成率最低（96%），它的"领先"完全来自分母：32/48 对 ExpeL 的 32/50；按全部任务计，两者持平。
- 目前无法判断这种口径偏向哪一方。
- **修复**：以 ITT（intention-to-treat）为主指标，即未完成按未解决计；报告每个方法、每次运行的完成数与失败原因。

**M5. 方法与配置无法从论文复现**

- **没有规定的内容**
  - condition 的表示与索引方式。
  - Eq. 2 的问题：
    - `Select` 没有定义；
    - `t` 在 Eq. 2 中是步编号，在 Algorithm 1 中是任务编号；
    - `H` 既指初始轨迹，又指动作历史；
    - `θ` 指的其实是一个冻结的 API 模型。
  - 排序函数、候选数、query 的构造方式、工具 API、检索结果的注入格式。
  - mini-SWE-agent 没有显式的规划阶段，"before planning" 由什么触发？什么算作 "error"？
- **构图的疑点**
  - MERGED_INTO 只有 8,910 条，即 9,600 条 Strategy 中有 690 条没有并入任何规则。
  - 已合并的 8,910 条变成 7,835 条 CanonicalRule，只压缩了约 12%。
  - PlaybookEntry 恰好也是 8,910 条，与 MERGED_INTO 的数量相同。检索单元到底是什么？
  - 781 个 Community 是如何形成的？既然 PlaybookEntry "carry no edges"，agent 又怎样 "follow graph links"？
- **在线标签**：Algorithm 1 第 e 步只写了 "agent-visible outcomes"。成功或失败由谁判定？与官方结果的一致率是多少？错误的"成功 lesson"会沿着 stream 传播下去。
- **池与参数**
  - Related-Lite99 的池在 Table 8 中是 1,494 条轨迹，在 §5.6 中是 "300 summaries"。这 300 条是怎么选出、由谁撰写的？baseline 用的是哪一个池？
  - schema 快照基于 1,795 条轨迹，而审计前是 1,762 条，对不上。
  - top-k 的 k、static playbook 的规模和来源都没有给出。如果 playbook 是从这 99 个评测任务的运行里挑出来的，那就属于测试集派生。
  - 全文没有 prompt、temperature 和 seed。

**M6. 以方法命名的"graph"没有被证明有用**

- No graph links 为 31.1，即 −4.0±13.1，而且只在 Related-Lite99 上做过。这个 benchmark 的池只有 300 条 summary，图统计也没有报告。
- 图最丰富的 Verified500 上没有做这个消融，也没有链接遍历的遥测数据。
- 出错后检索（−1.9±13.2）同样不显著，却被写进了结论里的实践建议。
- **修复**
  - 在 Verified500 和 DeepSWE113 上做 no-graph-links；
  - 报告遥测数据；
  - 与 HippoRAG、ExpGraph 那种算法式检索做对比；
  - 如果仍然没有效应，就把 graph 定位为 provenance 存储，并从标题中去掉。

**M7. 评测协议与外部效度**

- **协议变更**：Related-Lite99 被改为随 stream 增长（L195–197）。按原始的固定池协议，对应的数字是 28.7，而不是 35.1。
- **自称与实际不符**：§5.6 L397 自称 "keep the Related-Lite99 protocol of the main comparison"，但实际上：
  - Kimi 和 MiniMax 是单次运行、以已完成评测为分母；
  - MiniMax 还经过一层 "API compatibility layer"；
  - pool size 50–200 是单次运行。
- **开发集与测试集**：Table 11 的开发集是 Verified 上的 50 题，必然落在 Verified500 之内。
- **预训练污染**：没有讨论 SWE-bench Verified 对 2026 年 backbone 和 distiller 的预训练污染，也没有 post-cutoff 评测。
- **Gemini 与 LoLBench 的设置缺失**
  - Gemini 实验不在 Table 2 中：初始池、预算、运行次数都没有给出。
  - LoLBench 没有给出选题规则，也没有说明 baseline 如何接入 Codex。六个 baseline 全部恰好 1/20，令人怀疑它们是否真的检索到了内容。
- **oracle**
  - 配置不明。DeepSeek 上 oracle 为 27.8，与 random 的 27.1 相当；MiniMax 上 oracle 是 15/95，低于 no memory 的 19/98。
  - 因此 "exceeds the oracle on every backbone"（L411）信息量很低。
  - SWE-ContextBench 中 agent-selected summaries 的效果是 −4.04，与本文 agent selection 带来增益的方向相反，文中没有调和。

**M8. 新颖性与定位**

- **各组件都有先例**：

  | 组件 | 已有工作 |
  |---|---|
  | 条件化 lesson | CLIN、AutoGuide |
  | 抽象带来的迁移 | Memory Transfer Learning |
  | agent 搜索经验卡 | MemGovern |
  | 规划与诊断两个时点检索 | Agent KB；ExpeRepair（Table 1 中 After errors 为 ✓） |
  | 在线更新 | ReasoningBank、ACE |
  | community 节点 | GraphRAG（未引用） |

- **Table 1 的问题**
  - 没有"存储/匹配 condition"这一列；
  - 漏掉了 CLIN、AutoGuide、MemGovern、Agent KB，以及本文自己的 baseline FAISS Flat、Mem0、LangMem；
  - ContextGraph 与 ExpeRepair 在三列上都是 ✓，剩下的区别只有 agentic search 和 typed graph，而这两项的消融都不显著。
- **`references.bib` 里有 27 个条目在正文中一次都没有被引用，其中几篇与本文核心主张直接相关**：
  - *Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents*（cueanchored2026）；
  - *Learning When to Remember: Risk-Sensitive Contextual Bandits for Abstention-Aware Memory Retrieval in LLM-Based Coding Agents*（rscbmc2026，与 condition gating 最接近）；
  - *Decision-Aware Memory Cards: Counterfactual-Inspired Context Selection …*（cicl2026）；
  - *VibeMemBench*（vibemembench2026）、*Measure Before You Manage*（measure2026）：两个 coding-agent 记忆 benchmark；
  - *Agent Memory Distillation*（distill2026，见 M1）、MemRepair、CODESKILL、AdaMEM；
  - Getafix（2019）早已不属于同期工作。

  作者显然知道这些工作，却没有讨论，审稿人会质疑其中的选择性。至于哪些属于 ICLR 同期工作的豁免范围，要按截稿日期逐篇判断。

### 次要（Minor）

- **Limitations 与 Ethics**：Limitations、Reproducibility、Ethics 都放在全部附录之后（p.20），而正文 p.9 还有约三分之一空白。Limitations 只有两句。Ethics 没有讨论跨项目共享记忆可能造成的代码或密钥泄露，以及 memory poisoning；而在线 lesson 会保留 "files and commands"（experience-memory.tex L56）。
- **附录组织**
  - 附录按实验历史组织（label 为 sec:historical、sec:new-results），还同时出现 "summary-memory" 和 "episodic-memory" 两套 ContextGraph 配置；
  - Table 13 重复了 Fig. 4 的 DeepSeek 列，而 Kimi 和 MiniMax 的计数只在 JSON 里；
  - Tables 9、11、12 没有被主文引用。
- **图**
  - Fig. 1 下方的 TikZ 条与主图风格不一致。它补充了"更新"这一步，但箭头很短，建议改成主图内的回环。
  - Fig. 1(a) 和 Fig. 2 都把 condition 标成 "Context"。Django 这条 lesson 的措辞在 §3、Fig. 1、Fig. 2 中各不相同，比如 "Setup is obscuring the failure" 与 "Failure appears without the full app"。
  - Fig. 3 从 0 起画，差异几乎看不出来，没有 CI，"72.1" 压在边框上。
  - Fig. 4 没有误差线，看不出哪些是单次运行、哪些是五次均值，数值标签约 6pt。
- **表**
  - Table 2 的标题是 "Main benchmark comparisons"，内容实际是设置表，而且缺少 Gemini 那一行。
  - Table 4 的 pass@k 表头下填的是任务数，不是比率。
  - Table 14 用的是相对增益，与全文的绝对 pp 不一致。
  - Table 15 有七行相同的 5.0，而且只有 ContextGraph 报告了 pass@3。
- **叙事**
  - 研究问题（L80–81）预设了答案。
  - 13.7 这个数字在四处重复。
  - 六个粗体 "Finding" 混杂了三类内容：复述结果、未经检验的因果归因、规范性建议（"worth building"、"pays off"）。
- **参考文献**
  - 大小写丢失：Swe-bench、github、llm。
  - SWE-bench 应引 ICLR 2024 版；ExpeRepair 已被 FSE 2026 接收，仍引 arXiv。
  - Supermemory 以厂商博客为来源。
  - live-SWE-agent、Codex、Nebius SWE-bench-extra、text-embedding-3-large 都没有引用。

---

## 5. 给作者的问题（rebuttal 中最关键的 12 个）

1. **no-memory 漂移。** Related-Lite99 上 DeepSeek V4 Pro 的 no memory 为什么在 Table 3 是 21.4，在 Table 4（五次均值、同样预算）是 14.3%，在 Table 9 是 14.14？Kimi K3 为什么是 18.6（Fig. 4）对 29.29（Table 9）？各实验的 scaffold、snapshot、prompt、temperature、harness 和日期有什么不同？
2. **运行次数与配对检验。** Verified500 跑了几次？请给出每个五次均值的 per-run 值与 SD，以及 Table 7 每一行的配对检验（McNemar 或 task×run bootstrap），经 Holm 校正后的结果。
3. **完成率与 ITT。** 主比较和消融中，每个方法、每次运行各有多少未完成评测？ITT 口径下结果如何？35.1、72.1、20.7 分别是怎么聚合出来的？
4. **distiller、更新与预算。**
   - 每个 baseline 用哪个 LLM 构建记忆？更新粒度和信号是什么？
   - 如果所有方法用同一个 distiller、都逐任务更新，排名会变吗？backbone 自蒸馏的 ContextGraph 得多少分？
   - memory 动作、蒸馏和 embedding 是否计入预算？201K 是否包含它们？
5. **condition 与消融参数。**
   - 在选择阶段去掉 condition 和 outcome 字段后，结果是多少？
   - fixed top-k 的 k 是多少？
   - static playbook 有多少条 lesson？"最常被选中"是在哪些运行上统计的？
6. **在线标签。** 在线轨迹的成功/失败标签由谁判定？在各 benchmark 上与官方结果的一致率是多少？
7. **同任务 lesson。** 在 Gemini pass@k、LoLBench pass@3 和 retry 实验中，检索到同任务 lesson 的比例是多少？排除它们后结果如何？Gemini pass@1 的估计量是什么？no memory 组的 temperature 是多少？
8. **同仓库 lesson 的来源。** Verified500 上的同仓库 lesson 来自初始 Nebius 池还是在线更新？Related-Lite99 上两个 28.7 是否来自同一批运行？选中 lesson 中有多少来自 SWE-ContextBench 标注的相关前驱？
9. **LangMem。** LangMem 以什么方式接入（工具还是注入）？它是否在线更新？34.0 是单次运行还是五次均值？
10. **池与图的规模。** 300 条 summary 如何从 1,494 条轨迹中产生？各 baseline 在 Related-Lite99 上用的是哪个池？实际所用的图有多少节点和边？1,795 与 1,762 为什么对不上？检索单元是 PlaybookEntry 还是 CanonicalRule？
11. **oracle 与已有结果。** oracle 如何交付（注入位置、格式）？SWE-ContextBench 中 agent-selected summaries 为 −4.04，本文的 agent selection 为何带来增益？
12. **Gemini 与 LoLBench 设置。** Gemini 实验用了哪个初始池、多少预算、跑了几次？LoLBench 的 20 题是怎么选的？baseline 如何接入 Codex，是否真的检索到了内容？

---

## 6. 冲击 Best Paper 的修改路线图

### (a) 先定论题的形式：预先登记竞争假设，而不是先定结论

ICLR Outstanding Paper 通常需要同时具备四点：
1. 一个清晰、一般、最好有些出人意料的 insight；
2. 因果级别的证据（受控干预、剂量–反应关系、样本外预测）；
3. 简洁的方法，或者一个能改变领域评测范式的协议/benchmark；
4. 广泛的影响。

目前这篇论文是"系统 + 排行榜领先"，四点中只沾到 4 的边。

**建议改为回答一个问题：coding agent 的经验记忆，收益究竟来自哪里？** 在实验之前预先登记三个互相竞争的假设：

| 假设 | 内容 | 现有数据中的线索 |
|---|---|---|
| **H1 流内积累** | 收益主要来自同一个 stream 中在线积累的同仓库或相关前驱经验 | 两个 28.7；Verified other-only 仅 +1.4；静态记忆都聚在 +5–7 |
| **H2 选择精度** | 收益来自 agent 按任务选择 lesson 的精度（agentic access），而不是存了什么 | fixed top-k −10.8；LangMem 接近 CG |
| **H3 条件门控** | lesson 显式带有的 applicability condition 使 agent 能正确拒绝不适用的 lesson | 目前**没有直接证据**，只有被混淆的 playbook 对照 |

注意这些假设和论文自己的数据已经有张力：random summaries（+5.7）高于 fixed top-k CG（+2.9），ACE 的整本 playbook 也有 +6.7。所以不能只凭"精度越高越好"这一条线索下结论。

**标题按结果决定**（刻意避开与 bib 中 "Delivery, Not Storage" 撞车的措辞）：
- H3 成立："Knowing When a Lesson Applies: Condition-Gated Experience Memory for Coding Agents"
- H1 成立："Coding Agents Learn Most from Their Own Stream: A Causal Study of Experience Memory"
- H2 成立："Where Does Experience Memory Help Coding Agents? Selection, Streams, and Conditions"

无论哪种结果，只要证据干净，都是一篇有一般性 insight 的论文。一个"被严谨证伪的流行直觉"本身也很有冲奖潜力。

**摘要级表述（草稿）**："coding agent 的经验记忆何时有效？我们在冻结协议、ITT 指标和配对统计下，做了 lesson 内容（抽象/原始/随机）× 访问方式（agent 按任务选择/top-k/全局注入）× 适用条件（保留/删除/打乱）× 更新（静态/在线/仅跨仓库）的因子实验，覆盖约 700 个修复任务和 3 个 backbone。我们发现 [……]；一个三参数模型能在未见过的 backbone 上预测 pool size 与 playbook 的结果。我们还发布了 Continual-SWE 协议和一个极简实现。"

### (b) 第 0 步：只用已有日志的分析（最便宜，先于任何新实验）

1. **配对推断**：逐任务、逐运行做 McNemar 或 bootstrap，报告 run 级 SD，做 Holm 校正，加入 Table 7 缺失的比较项。
2. **完成数与 ITT 重算**：给出每个方法、每次运行的完成数，并按 ITT 重算全部结果。
3. **选中 lesson 的来源分解**：按同仓库/跨仓库 × 初始池/在线分类，并统计来自 **SWE-ContextBench 已标注相关前驱**的比例。Related-Lite 自带相关性标注，这是检验 H1 最便宜、最客观的方式。
4. **选择精度的客观度量**：以相关性标注为金标准，计算选择的 precision/recall，再看 resolution 是否随精度分层变化（初步检验 H2）。
5. **重试中的同任务 lesson**：统计 retry、Gemini、LoLBench 中检索到同任务 lesson 的比例。
6. **遥测**：每个任务的 memory 动作数、选中 lesson 数、链接遍历次数、出错后检索的频率、memory token 占比。
7. **澄清统计口径**：no-memory 漂移的来源、两个 28.7 的来源、Gemini pass@1 的估计量。

### (c) 必做实验（已按可行性修订规模）

| 编号 | 设计 | 数据与规模 | 统计 | 支持哪个假设 |
|---|---|---|---|---|
| **E1 冻结协议** | 冻结 scaffold commit、模型 snapshot、prompt、temperature（>0）、预算口径（包含蒸馏与 memory token）；no memory 与各方法同批次并行运行 | Related-Lite99 与 DeepSWE113 各 5 seeds；Verified500 3 seeds | mixed-effects logistic（task、seed 为随机效应）；ITT；Holm 校正 | 所有结论的前提 |
| **E2 条件因子实验（核心）** | 所有组都在**选择阶段**实时选择：(a) 完整 lesson；(b) 删除 condition 与 outcome 字段后的池；(c) condition 在 lesson 之间打乱；(d) 同一批 lesson 全局注入，按 token 匹配。另加一组 replay 臂：固定已选集合、只删字段，作为次要对照和保真度检查 | 先在 Related-Lite99 + DeepSWE113（212 题）上做；预先设定等价性界限（例如 ±5 pp）；完整版扩到 712 题 | 配对差异 + 95% CI；等价性检验（TOST） | (a) > (b)≈(c) 支持 H3；(a)≈(b) 则 H3 被否定 |
| **E3 流内积累的分解** | CG × {静态, 仅跨仓库在线, 仅同仓库在线, 全部在线}；再加一组"移除 benchmark 标注的相关前驱"；≥5 个随机任务顺序 | Related-Lite99 + DeepSWE113 | forward-transfer 斜率及 CI；stream 三分位 × 条件的交互 | 直接检验 H1 |
| **E4 对等 baseline 网格（缩减版）** | 三个最接近的 baseline（ExpeRepair、LangMem、ACE）× {静态, 在线} × {原生接口, 共享 agentic search 工具}；统一初始池与 distiller | 212 题 × 3 seeds（约 7.6K 次运行） | ITT；每美元解决数 | 接口对等后 CG 仍领先，说明表示方式本身是贡献；否则支持 H2 |
| **E5 Distiller 解耦** | CG × {backbone 自蒸馏, Claude 4 Sonnet}；再做 **自蒸馏抽象 lesson vs raw**，把"抽象"与"强模型改写"分开 | Related-Lite99 + DeepSWE113 × 5 | 配对差异 | 自蒸馏保留大部分增益时，"self-improving" 与"抽象"都成立 |
| **E6 retry/pass@k 对照** | 独立采样（T=0.7）+ 无偏 pass@k；no-memory Reflexion（反思者同为 Claude 4 Sonnet）；排除同任务 lesson 的 CG；重试只由 agent 自检触发 | Related-Lite99 + Verified 200 题子集；Gemini 至少加一个 memory baseline | pass@k 曲线 + CI | 排除同任务 lesson 后仍优于 Reflexion，才算跨任务经验成立 |
| **E7 规模曲线** | pool size {30, 100, 300, 1,000, 全部已审计池}（嵌套随机子集）× 同仓库占比 {0, 25%, 50%}；3 个 backbone | Related-Lite99（上限 1,494 条）+ DeepSWE113（上限 497 条） | 拟合饱和曲线 | 检验"更多经验 → 更高精度" |
| **E8 外部效度** | post-cutoff 任务（SWE-rebench / SWE-bench-Live，晚于所有模型 cutoff，150–300 题）；Multi-SWE-bench 约 300 题；LoLBench 扩到 ≥100 题，所有方法都报 pass@k | 如左 | 配对差异 | 在无污染、多语言条件下效应是否仍在 |

**统计功效提醒**：在 20% 不一致率下，配对 McNemar 检出 10 pp 约需 155 题，检出 5 pp 约需 620 题。只在 Related-Lite99 的 99 题上做 E2，大概率得不出结论。

### (d) 机制与因果分析

1. **剂量–反应干预**：选择完成后，把比例 ρ ∈ {0, .25, .5, .75, 1} 的 lesson 替换为类型和长度匹配、但 condition 不成立的 lesson，**并与 k ∈ {1, 3, 5, 10} 交叉**，否则上下文饱和项无法识别。另设一组"condition 正确、action 有细微错误"的 lesson。预期得到单调曲线，并在某个 ρ* 处穿过 no-memory 线。
2. **Adherence 与中介分析**：用 LLM judge 判断 agent 是否执行了 lesson 中的 action，该 judge 先在 100 条人工标注轨迹上验证。然后检验中介路径：选择精度 → adherence → resolution。
3. **标签准确率**：给出 agent-visible 成功标签与官方结果的混淆矩阵；分别用官方标签（上界）、agent 标签、无标签三种来源做消融。
4. **负迁移分类**：对全部 loss 和约 50 个 win 做分类，统计哪类 lesson 误导了 agent、是否源于条件误匹配。用这些系统性证据取代 Django 这个单一案例。
5. **lesson 类型分析**：把 lesson 分为复现/隔离策略、API 语义、文件/命令指针三类，做 leave-one-type-out 干预。如果同仓库收益主要来自"文件/命令指针"，就应坦率地说明：这是在流上学习仓库知识，而不是迁移抽象策略。

### (e) 方法：极简化、形式化与理论

- **形式化**
  - lesson 定义为 ℓ = (polarity, condition c, action a, outcome o, sources, repo, emb)；
  - 动作空间 A = {search(q,k,type), read(id), neighbors(id,r), select(id), stop}，并给出评分函数、调用上限和注入格式；
  - 更新算子 G⁽ⁱ⁺¹⁾ = U(G⁽ⁱ⁾, τᵢ)，写清 merge、link、community 三步；
  - 任务编号、步编号、图版本分别用不同符号，去掉 θ。
- **极简化**：如果"lesson + condition + 在扁平存储上做 agentic search + 在线更新"与完整系统持平，就删去 community、fragment 和 canonical rule 三层。目前合并压缩只有约 12%，说明这几层作用有限。评审一向偏爱"简单但有效，而且说清了为什么有效"的方法。
- **理论**：给一个可检验的简单模型。设：
  - g：任何与修复相关的文本都会带来的通用收益，用来解释 random summaries 的 +5.7；
  - k：选中的 lesson 数，π：选择精度；
  - b、c：适用与不适用的 lesson 各自带来的收益和代价；
  - λ：上下文饱和惩罚系数。

  则

  E[Δ] ≈ g + k·(π·b − (1−π)·c) − λ·k²

  由此得到四个可检验的预测：
  - (i) 盈亏平衡精度 π* = c/(b+c)；
  - (ii) 全局 playbook 的收益 ≈ g + k·(q·b − (1−q)·c)，其中 q 是 lesson 适用的基率；
  - (iii) 池越大，可达到的 π 越高，所以 pool-size 曲线呈凹形；
  - (iv) 存在最优 k*。

  在一个 backbone 的 k×ρ 网格上拟合参数，然后在另一个 backbone 和 pool-size 曲线上做**样本外**检验。能做对样本外预测，是这类论文从 accept 走到 award 的关键一步。

### (f) 协议贡献：Continual-SWE

把本文已经改过的 stream 协议正式化并发布：
- **stream 与顺序**：Verified、Related-Lite、DeepSWE 三个 stream，按创建时间排序，另附至少 5 个随机排列和相关前驱标注。
- **审计**：
  - 覆盖在线新增的 lesson；
  - 使用 Jaccard 0.5、0.7、0.85 三个阈值；
  - 加一个经人工验证的 LLM 语义去重 judge。
- **ITT 与成本**：以 ITT 为指标，完整记账成本。
- **强制对照**：static pool、Reflexion、token 匹配的 best-of-k、移除相关前驱。
- **报告指标**：forward-transfer 斜率、负迁移率、同仓库/跨仓库归因。
- **定位**：必须与 SWE-ContextBench、VibeMemBench、*Measure Before You Manage* 区分清楚，说明它独有的是"流式 + 因果对照 + 成本对等"。

### (g) 写作与结构重组（9 页主文）

| 节 | 篇幅 | 内容 |
|---|---|---|
| 1 Intro | 1.0 | 用两句话引出 Django 例子；提出一个可证伪的问题；H1/H2/H3；给出校准过的发现摘要，每个数字只出现一次 |
| 2 Related work | 0.6 | 按设计轴组织：记忆单元、选择机制、结构、调用时机、更新；重建 Table 1，加 condition 列和 selector 列，补全 CLIN、AutoGuide、MemGovern、Agent KB、LangMem、Mem0、FAISS，以及 bib 中已有但未引用的 2026 年相关工作 |
| 3 Problem & protocol | 0.7 | 形式化的 stream 协议、ITT、预算口径、标签来源 |
| 4 Method | 1.2 | lesson 规范、工具 API 表、更新算子；重绘 Fig. 1，把"更新"画成主图内的回环 |
| 5 Experiments | 5.0 | 5.1 统一协议表；5.2 主结果（Fig. 3 改为"相对 no memory 的增益 + 配对 CI"，加入 LangMem 和 Mem0）；5.3 收益从哪里来（E2、E3 因子结果）；5.4 机制（精度、adherence、剂量–反应图）；5.5 沿 stream 学习（E6）；5.6 规模与外部效度 |
| 6 Limitations & broader impact | 0.3 | 放进主文，包括泄露与 memory poisoning 风险 |
| 7 Conclusion | 0.2 | |

- **删除**：重复出现的数字；Table 13、Table 16 与 Panel B 重叠的部分。
- **修改**：Fig. 2 改成真实存储的 lesson 记录和选择日志；Table 11 移入附录，并注明任务 ID。
- **新增**：统一协议表、成本表、剂量–反应图、实际所用图的统计表。

### (h) 优先级与时间线

| 项目 | 解决的问题 | 工作量 | 影响 | 优先级 | 时段 |
|---|---|---|---|---|---|
| 只用日志的分析（§6(b) 全部 7 项） | C2、C3、C4、M3、M4 | 低 | 高 | P0 | rebuttal 前 |
| 按证据改写摘要、Findings、结论和标题措辞 | C1、C2 | 低 | 高 | P0 | rebuttal 前 |
| 披露全部配置，并对账 no-memory 漂移 | C3、M5 | 低–中 | 高 | P0 | rebuttal 前 |
| 选择阶段的 condition-stripped 与打乱实验（212 题 × 3–5 runs，预设等价界限） | C1 | 中 | 高 | P0 | rebuttal 前 |
| LangMem 跑 DeepSWE113（5 runs）与 Verified500（≥1 run），并说明接入方式 | M2 | 中 | 高 | P1 | rebuttal 前（尽力） |
| retry 排除同任务 lesson，加一组 Reflexion（同一反思者） | M3 | 中 | 中 | P1 | rebuttal 前（尽力） |
| E1 冻结协议后多 seed 重跑（含 Verified500 × 3） | C2、C3 | 高 | 高 | P0 | camera-ready / 下一投稿 |
| E2 完整版 + E3 流内分解 | 核心论题 | 高 | 高 | P0 | 下一投稿 |
| E4 缩减版网格 + E5 distiller 解耦 | M1、M2 | 高 | 高 | P1 | 下一投稿 |
| 剂量–反应、理论拟合与样本外检验 | 一般性 insight | 中 | 高 | P1 | 下一投稿 |
| E6 完整版 + Continual-SWE 发布 | 协议贡献 | 高 | 高 | P1 | 下一投稿 |
| E7 规模曲线 + E8 post-cutoff 与多语言 | 外部效度 | 高 | 中 | P2 | 下一投稿 |
| poisoning 与泄露实验，扩写 Ethics | 部署风险 | 中 | 中 | P2 | camera-ready |

**时间线**
- **rebuttal 前（约 2–3 周）**：日志分析、文档化、condition-stripped 实验、改写主张；尽力补上 LangMem 与同任务排除的实验。
- **camera-ready 或下一投稿（约 2–4 个月）**：冻结协议后全量重跑、因子实验与流内分解、对等网格、剂量–反应与理论、Continual-SWE、规模与外部效度实验。

---

## 7. 快速修复清单（不需要新实验，应当立即改）

1. **摘要与贡献 3**（L25–28、L129–132）：DeepSWE 的增益注明为不显著；"highest rate" 改为 "numerically highest"；注明 Verified500 的运行次数。
2. **"stay at the no-memory level"**（L33、L114、L127、L272）：改为 "do not significantly improve over no memory"，并给出 CI。
3. **Findings 与结论**（L224–225、L278–280、L370–373、L412–416、L434–436、L444–448）：只保留显著的结论；删除 "each add further gains"、"worth building"、"pays off"；说明 pool size 为 50 时低于 no memory。
4. **LoLBench**（L250–253）：改为报告计数 3/20 对 1/20，删除 "the only memory method"。
5. **L277**："8.0 points above ExpeL" 要么补上 CI，要么删掉，并同时说明 static CG（28.7）低于在线 ExpeRepair（31.3）。
6. **Table 2**：标题改为 "Evaluation settings"；增加 Gemini 行；新增 scaffold、backbone、runs、分母四列。
7. **Table 4**：表头写明单位是任务数（of 33 / of 99）；caption 注明所用池早于审计，且含 10 个近重复源。
8. **模型 snapshot 与 scaffold**：在每个实验中**如实**标注实际所用的版本，不要为了统一而改名（C3 的漂移可能就源于 snapshot 不同）。§5.4 中的 19/89 对 13/89 标注出处（Table 9）。
9. **需要澄清的数字**：两个 28.7 的来源；1,795 与 1,762 的差异；1,494 条轨迹如何变成 300 条 summary；检索单元是 PlaybookEntry 还是 CanonicalRule（8,910 = MERGED_INTO）。
10. **补充参数**：给出 fixed top-k 的 k、static playbook 的规模和来源、distiller，以及每个 baseline 的更新方式（Table 2 caption 与 §5.1）。
11. **token 结论**（L246）：说明统计口径（是否包含蒸馏与 memory 调用），并补上 baseline 的数字。
12. **L397**："keep the Related-Lite99 protocol" 改为如实描述：Kimi 和 MiniMax 为单次运行，MiniMax 经过兼容层，pool size 50–200 为单次运行。
13. **L411**：删除 "exceeds the oracle on every backbone"，或者为它补上 CI，并说明 oracle 的配置。
14. **Fig. 3 与 Fig. 4**：
    - 加误差线；
    - Fig. 3 的 caption 注明 Verified500 为单次运行；Fig. 4 的 caption 标明每个 bar 是单次运行还是五次均值；
    - 字号不小于 7pt；
    - 修正 "72.1" 压线。
15. **Fig. 1 与 Fig. 2**：
    - 把 "Context" 改为 "Condition"，并与 Table 12 的 schema 保持一致；
    - 统一 Django lesson 的措辞；
    - Fig. 1 的 TikZ 条改为主图内的回环。
16. **Table 14 与 Table 15**：Table 14 改为绝对 pp；Table 15 合并相同的行，补上 baseline 的 pass@3，或者删除 pass@3。
17. **Table 1**：增加 condition 列；补充 FAISS Flat、Mem0、LangMem、CLIN、AutoGuide、MemGovern、Agent KB 等行；引用 GraphRAG。
18. **主文引用**：主文引用 Tables 9、11、12；§5.6 概述 Table 9 中不显著的复现结果。
19. **Limitations、Reproducibility、Ethics**：移到 p.9 空白处（参考文献之前）。
    - Limitations 补充：pre-audit 池、分母口径、蒸馏成本、错误 lesson 的传播；
    - Ethics 补充：跨项目泄露与 memory poisoning。
20. **"self-improving"**（摘要 L19）：在完成自蒸馏对照之前，改为 "experience-accumulating"。
21. **相关工作**：讨论 bib 中已有但未引用的直接相关工作（Delivery Not Storage、Learning When to Remember、Decision-Aware Memory Cards、VibeMemBench、Measure Before You Manage、Agent Memory Distillation）。
22. **参考文献格式**：
    - 保护大小写：`{SWE}-bench`、`{GitHub}`、`{LLM}`；
    - SWE-bench 改引 ICLR 2024 版，ExpeRepair 改引 FSE 2026 版；
    - 补上 live-SWE-agent、Codex、Nebius SWE-bench-extra、text-embedding-3-large 的引用。
