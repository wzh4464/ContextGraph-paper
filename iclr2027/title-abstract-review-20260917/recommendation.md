# ContextGraph 标题与摘要修改建议

> 历史修订记录：保留文件日期当时的意见、数字和状态。当前稿件以 [main.tex](../main.tex) 为准；其中的建议不代表当前待办。

2026-09-17。已通过用户指定代理与 Claude Code Fable 5.1 完成两轮讨论；实际输出确认模型为 `claude-fable-5-1`。以下是主助手综合原文、获奖样本和讨论后的判断，不等于原样采用模型意见。

## 决定

**改摘要，标题小改。** 保留当前具体的问题开场，将可执行条件与联合检查的发现提前；去掉 FAISS 库名和旧 Related-Lite99 数字，避免不同方法版本的证据被串成同一个实验。摘要不加入实习生／资深工程师类比。

论文最值得让读者记住的内容是：**通过当前任务的验证仍可能遗漏历史要求；历史条件与当前流程的组合，能够在已有开发案例中暴露分别检查两者时没有发现的行为。** 这比“记忆让智能体更有经验”更具体，也更容易设计反证实验。

## 推荐标题

**ContextGraph: Turning Past Repairs into Executable Requirements for Coding Agents**

中文：**ContextGraph：将历史修复转化为编程智能体的可执行需求**。

相较原题 `ContextGraph: From Past Repairs to Executable Requirements`，明确加入研究对象 coding agents，并用 Turning 描述方法的具体转换。它保留项目名，避免暗示系统已经普遍解决所有隐含需求。

没有选 `What the Issue Leaves Out` 作主标题：它有记忆点，可作报告主题，但容易让读者首先期待一篇系统测量 bug report 遗漏率的论文，现稿尚未完成这样的广泛研究。没有选 `Coding Agents Need Executable Memory`：当前证据不支持“必需”或通用优越性。

## 推荐摘要：按当前能够明确归属的机制证据

Coding agents can pass a benchmark's official tests while missing requirements established by earlier repairs. We present ContextGraph, a repair-memory prototype that represents past experience as a behavioral requirement, its triggering input, and an executable observation of the outcome. Source-version executions record behavior before and after the historical repair. Similarity retrieval selects candidate experiences, and graph relations connect their input conditions and operations to construct checks for the current workflow. In three selected Django development comparisons, each with one repair per arm, memory-informed repairs preserve query strings, remove redundant uniqueness constraints, or honor destination timezones that matched no-memory repairs omit, although both arms pass official verification. A further development case reveals that a repair can satisfy current and historical examples separately yet fail when their conditions are combined. In a matched pair of agent runs, only the agent given the composed checks and their execution feedback produces a repair satisfying the joint behavior. Memory content also affects correctness: concise requirements sometimes suffice, while historical implementations can introduce additional errors. These findings motivate carrying the conditions behind past repairs into new tasks, where execution can test candidate repairs against those requirements and expose interactions missed by separate checks.

这是供审阅的建议稿，尚未替换 main.tex 或 OpenReview。它有意将尚未建立版本映射的系统总分留在下面单列；并非断言该总分错误。

### 中文翻译

编程智能体即使通过了基准的官方测试，仍可能遗漏此前修复所确立的要求。我们提出修复记忆原型 ContextGraph，将历史经验表示为行为要求、触发该要求的输入，以及对结果的可执行观察。系统通过在历史修复前后的源码版本上执行，记录相应行为。相似性检索选出候选经验，图中的关系则连接这些经验的输入条件与操作，为当前工作流程构造检查。在三个选定的 Django 开发对照中，每组各有一个修复结果：带记忆的修复能够保留查询字符串、移除冗余唯一性约束，或遵循目标时区；对应的无记忆修复虽然也通过官方验证，却遗漏了这些行为。另一个开发案例表明，一个修复可以分别满足当前示例和历史示例，却在条件组合后失败。在一对匹配的智能体运行中，只有获得组合检查及执行反馈的智能体提交了满足联合行为的修复。记忆内容也影响正确性：简洁的需求陈述有时已经足够，而历史实现也可能引入额外错误。这些发现支持将历史修复背后的条件带入新任务，使执行能够依据这些要求检验候选修复，并揭示单独检查时遗漏的交互。

## 346/500 主结果如何处理

当前 main.tex 的新 Verified500 表报告 346/500 对 309/500（69.2% 对 61.8%，相差 7.4 个百分点），主仓库 9 月 16 日报告确认它来自新增的作者提供汇总。附录 318/500 是旧结果，二者本身并不矛盾。本轮没有重跑或逐 patch 复核。

尚缺的是 **346/500 对应的系统版本与当前可执行组合方法的对应关系**。已向用户询问，未得到答案时不替用户推定。不能因它紧跟在新方法介绍之后，就让读者自然理解为“图组合导致了全部 7.4 个百分点提升”。

若确认这是另一版 ContextGraph，且结果来源可追溯，可在上面的机制证据之后增加这句，明确其独立身份：

> A separate system-level evaluation on SWE-bench Verified reports 346/500 resolved tasks with ContextGraph and 309/500 without memory.

若确认它测试的正是当前冻结方法，正文应补上版本、源池、任务清单和预算，并据此重写主结果句；总体系统比较仍不能单独归因于组合机制，需要匹配消融。

14/99→21/99 和两轮对三轮保留在正文，完整交代 curated episodic memory、模型、预算和重试设置。摘要无需同时装入它们。不能把轮次差直接换算为 token 或成本节约。

## 对照获奖论文后，值得学的是什么

我们下载了六篇经官方确认的 Outstanding Papers，保存的是公开 arXiv 版本，版本差异有记录。重点读了摘要、引言、核心论证/实验组织和结论，并非复现所有实验。

- **先让读者理解一个具体问题。** Registers 的现象、解释和干预连贯；ContextGraph 可用“当前示例通过、历史示例通过、联合示例失败”的对照承担同样作用。[论文](https://arxiv.org/abs/2309.16588)
- **为主张定义可测量的范围。** 多轮对话论文将需求逐步揭示变成可比较的实验，区分能力与不可靠性。ContextGraph 也应区分官方任务成功与历史／联合要求是否满足。[论文](https://arxiv.org/abs/2505.06120)
- **让机制解释接受干预检验。** Safety Alignment 的论证先归纳失败机制，再检验有针对性的补救；本文需要内容和预算匹配的“分别执行 vs 组合执行”对照。[论文](https://arxiv.org/abs/2406.05946)
- **把比较条件本身当作研究对象。** Never Train from Scratch 用实验证明评价设置会改变结论；本文不同记忆池、模型、任务分母和方法版本也必须明确分开。[论文](https://arxiv.org/abs/2310.02980)

这不是获奖配方。ICLR 2025 官方列出的考虑因素同时包含洞见、实践影响、写作和实验严谨性；当前最需要补的是证据，而不是更强的形容词。[官方说明](https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/)

Simon Peyton Jones 的写作建议也适用：围绕一个清楚、可复用的想法组织论文，使每项可检验的贡献在正文有相应证据。[原始讲义](https://www.microsoft.com/en-us/research/wp-content/uploads/2015/02/simon-peyton-jones_paper.pdf)

## 与 Claude 讨论后保留的分歧和纠正

1. Claude 第一轮把 RAG 限定为完成已陈述要求、把回归测试限定为同路径重放；我反对这种过窄的定义，第二轮已撤回。本文需要相对 ExpeRepair、RETester、MIRA、TRACE 等工作的具体差异，不写“首个可执行记忆”。
2. Claude 第二轮将“反馈修复破坏普通子类”的早期内容干预与后面的 original-base matched pair 混淆。原文后一对照中两组都通过普通子类检查，增强组通过更多联合要求；最终摘要据此写作。见 [main.tex 的匹配对照](../main.tex)。
3. 7.4 个百分点是正确的描述性差值；缺少置信区间不会使算术差值失效。真正需要避免的是将它写成未经检验的统计显著性或特定机制的因果效应。
4. 共享仓库本身并不自动证明三个任务统计上不独立。当前更直接的限制是案例经过选择、尝试次数少、部分检查在看到修复后构造；同一任务内多个检查也不能充当多个独立任务。
5. 标题第二轮已共同收敛为推荐版本。摘要由主助手进一步删去“existence, not prevalence”等偏审稿答辩的句式，用 prototype、selected development comparisons、matched pair 等具体范围承载限定。

## 冲获奖标准，优先补的三项研究工作

1. 将主分数与完整方法版本绑定，完成未参与开发任务上的评价。
2. 固定来源、预算、反馈和检查数量，隔离图关系及组合条件的作用。
3. 使用预先固定的共同检查套件，跨仓库／模型衡量需求遗漏、联合行为、回归和总成本，并报告重复运行的不确定性。

详见 [证据边界及实验建议](evidence-boundaries.md)。上述工作尚未在本轮执行。现有稿件中的 TBD 表和未明确配置的附加结果仍须在正式 PDF 准备阶段处理；本轮没有修改或上传 PDF。

## 资料

- [六篇论文来源与阅读笔记](award-reading-notes.md)
- [Claude 第一轮原始评审](claude-round1-review.md)
- [Claude 第二轮讨论](claude-round2-review.md)
- [纯文本摘要](recommended-abstract.txt)
- 模型调用状态保存在本地 `consultation-status.json`。
