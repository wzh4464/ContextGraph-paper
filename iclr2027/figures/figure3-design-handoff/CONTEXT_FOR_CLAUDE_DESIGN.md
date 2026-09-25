# ContextGraph Figure 3：交给 Claude Design 的完整上下文

请据此重新设计论文的核心方法架构图。图中文字使用英文，设计说明可以用中文。可以自由调整布局和信息分组；保持下面的方法含义和数据流。

## 1. 论文背景与设计目的

论文标题：**ContextGraph: Self-Improving Coding Agents via Cross-Repository Experience Graphs**。

ContextGraph 是 coding agent 的长期经验记忆架构。不同项目中的历史修复留下任务、调查过程、尝试过的动作、错误和结果。系统从中抽象出可迁移的策略与警告，把这些建议与来源经历、错误模式和结果关联，供后续任务使用。

新任务中的 agent 重点在两个时机查询记忆：**生成计划之前，以及遇到错误之后**。第一次帮助决定从哪里调查、先尝试什么、避开什么；第二次利用新出现的失败和刚执行的动作，帮助修订诊断和下一步行动。具体复现、编辑与测试由当前仓库中的 agent 完成。

图的中心信息：

> **Experience from different repositories becomes actionable guidance for planning and error recovery.**

目标读者是刚接触 coding-agent memory 的博士生。看图后应能回答：经验从哪里来、记忆是什么、图关系有什么用、什么时候查询，以及返回的建议怎样影响当前修复。

论文通过开源修复基准展示架构效果。本图承担方法解释，实验数字由结果图承担。

## 2. 三条设计理由

| 问题 | 设计 | 图中应体现的作用 |
|---|---|---|
| 源仓库的文件、变量和环境细节难以直接迁移 | Experience abstraction | 提炼该做什么、避免什么、何时适用 |
| 相关错误与有效策略分散在不同经历中 | Experience graph + graph retrieval | 通过关系找到共享策略及其来源 |
| 计划前与遇错后的信息和需求不同 | Memory access at two decision points | 用任务信息规划，用失败观察调整下一步 |

三个核心设计是 abstraction、graph retrieval、memory access。历史轨迹和当前仓库是输入来源与应用环境。

## 3. 当前 Figure 3 的全部模块

以下覆盖当前六个模块。新版不必继续使用六个方框。

### A. Past trajectories：多个仓库的历史经历

输入包括任务、动作、错误和结果。成功经历提供有效策略，失败经历也可以提供值得避免的尝试。

当前英文标注：

```text
Past trajectories
tasks, actions, errors,
and outcomes
```

建议明确画出多个 source repositories 与一个 current repository。历史轨迹里的局部代码和命令属于来源上下文，本图强调提炼出来的决策经验。

### B. Experience abstraction：提炼可迁移建议

语言模型提取调试、测试、代码导航和失败尝试中的经验。抽象去除妨碍迁移的源仓库专有细节，保留动作、理由和适用情境。

- **Strategies**：有帮助的调查或修复方向。
- **Warnings**：应避免的无效或昂贵尝试。
- **Applicability context**：建议在什么情境下有用。

当前英文标注：

```text
Experience abstraction
what to do / avoid
and when it applies
```

### C. Experience graph：把建议与上下文关联

图连接策略、来源经历和反复出现的错误模式。来自不同经历的相似策略可以合并为共享规则，同时保留来源关系。

设计时使用如下概念层次：

| 概念 | 含义 |
|---|---|
| Source experience | 一次历史任务的经历及结果 |
| Strategy / warning | 从经历中提炼的建议 |
| Shared rule | 合并相似策略形成的共享建议 |
| Error pattern | 与策略相关的错误类型或模式 |
| Source context / outcome | 帮助理解建议来源和使用理由的信息 |

当前英文标注：

```text
Experience graph
strategies and warnings
linked to errors and sources
```

建议画一个有含义的小型关联网络，例如两个来源经历连接到同一共享策略，错误模式与该策略相连。这样的图能表达跨项目共享经验。无需画完整数据库 schema。

论文中的概念路径：

```text
Error pattern — Shared rule — Source strategy — Past trajectory
```

这表示关系结构，不是某个案例中观测到的完整检索日志。代码中的规则—错误、策略—共享规则、策略—来源轨迹关系支持这条结构路径。最终图中无需列数据库关系名。

### D. Graph retrieval：选择相关且互补的经验

查询描述当前任务和 agent 已知的情况。检索结合三个来源：

1. **Semantic search**：语义相关的建议。
2. **Keyword search**：具体错误词和其他查询词。
3. **Graph connections**：错误模式、共享规则与来源经历之间的关联。

当错误类型可用时，错误相关的图检索通道参与候选选择。系统合并候选，再选出一小组相关、尽量不重复的经验。不同错误可以关联到同一调查策略，因此字面不同的任务也可能共享经验。

返回内容：**策略、警告、来源上下文**。

当前英文标注：

```text
Graph retrieval
semantic + keyword search
+ connections in the graph
```

底层实现包括相似度检索、关键词检索、Personalized PageRank、候选融合和多样性选择。这些供理解机制，不要求全部写进主图。

### E. Memory access：两个重点访问时机

**Before planning**

- 输入：任务描述、当时已有的代码上下文。
- 返回建议的用途：决定先调查哪里、如何缩小问题、如何复现、避免什么。
- 后续动作：形成调查／修复计划。

**After an error**

- 输入：失败命令、复现或测试带来的错误，最近动作、相关文件和当前假设。
- 返回建议的用途：寻找其他可能原因和可尝试的动作。
- 后续动作：修订诊断，继续编辑和测试。

当前英文标注：

```text
Memory access
before planning: task
after errors: failure
```

新版应把两个时机放在 agent 工作流上，让读者看到它们发生于何时。它们使用同一份经验图，不需要额外引入两个 memory agents。

### F. Current repository：在当前代码中执行修复

agent 完成调查、规划、编辑和测试。记忆影响决策，agent 依据当前代码开发具体实现。

当前英文标注：

```text
Current repository
investigate and plan
edit and test
```

保留 action/test → observation/error → next action 的反馈关系。检索输出 guidance，当前 agent 产生代码修改并调用仓库工具。

## 4. 完整数据流与箭头语义

### 构建经验记忆

```text
Past trajectories from multiple repositories
    → Experience abstraction
    → Strategies / warnings with applicability context
    → Linked experience graph
```

### 计划生成前的查询

```text
Current issue + available code context
    → Retrieve relevant experience
    → Strategies + warnings + source context
    → Investigation / repair plan
    → Agent actions: inspect, edit, test
```

### 出现错误后的查询

```text
Observed failure + recent action + current hypothesis
    → Query the same experience graph again
    → Relevant recovery guidance
    → Revise diagnosis and next action
    → Continue acting and testing
```

当前图的箭头：历史轨迹 → 抽象 → 经验图 → 检索；当前仓库与 memory access 双向传递 context / guidance；memory access 与 retrieval 双向传递 query / lessons。

新版可以拆成独立方向。箭头应区分：

- **Query / task state**：agent 向记忆提出需求。
- **Guidance / retrieved lessons**：记忆向 agent 返回建议。
- **Action → observation**：当前任务中的执行反馈。

已完成的新轨迹可以进入后续记忆构建。这是架构的扩展能力，论文中的系统比较使用固定记忆池；主图不必额外画在线更新回路。

## 5. 可选的具体案例

论文中已有 Django Trac #33018 案例：取反条件下对空查询结果的处理有问题。

- 一次 `python-statemachine` 失败经历把大量精力花在搭建完整 Django 应用上，启发了先隔离最小失败行为的建议。
- 一次 `sievelib` 成功经历同样支持先复现、再编辑。
- 使用经验的 Django agent 沿查询编译的异常路径定位到 `Exists.as_sql()`，修改局部处理并添加回归测试。
- 无记忆对照尝试最后产生广泛格式修改，没有完成核心修复。

若需要一个 memory-card 插图，可用以下概括文案：

```text
Strategy
Isolate the failing behavior before changing the code.

Warning
Avoid full framework setup before a minimal reproduction.

Context
Framework setup is obscuring the underlying failure.
```

这是对论文案例的概括，不是系统原始输出。可压缩为一条策略、一条警告。不要由此补造两次精确查询、错误类型、检索分数或图遍历日志。

## 6. Figure 2、3、4 的关系与必要性

图号按 2026-09-24 最新正文。

| 图 | 当前职责 | 内容 |
|---|---|---|
| Figure 2 | 具体行为示例与对照 | Django 中，文字要求与带历史条件的检查怎样影响修复；named-tuple range 与当前 query 的组合 |
| Figure 3 | 核心 memory 架构总览 | 跨仓经历抽象、经验关联、图检索、规划前与遇错后的记忆使用 |
| Figure 4 | 行为研究的构建与应用流程 | 历史版本上的示例检查、检索、条件组合、执行观察与修复验证 |

Figure 2 是具体例子，Figure 4 是该类行为研究的流程。它们没有完整表达跨仓策略抽象与两个查询时机，因此 Figure 3 的内容值得保留。

Figure 2、4 中出现的 requirement、input、operation、observer、witness、composer，以及同仓库 FAISS top-3，属于可执行条件研究。不要把这条研究流程搬进 Figure 3 作为默认核心架构。

Figure 3 的内容需要讲清楚，当前六方框的外观并非必须保留。若将来需要减少独立图数，可以把总览与行为分析组织成有层级的综合图。本次先重做 Figure 3，保留 Figure 2、4 的文件与正文位置。

## 7. 推荐视觉组织

推荐用两个阶段或两条横向区域：

**A. Build transferable experience**

多个 source repositories → 历史轨迹 → 经验抽象 → 小型关联网络。

**B. Use experience during repair**

当前任务 → 计划前查询 → 规划 → 行动／测试 → 观察。发生错误时，用新证据再次查询，再调整下一步行动。

同一个经验图服务两个查询时机。Graph retrieval 可以是经验图的访问接口，也可以是紧邻模块。用可理解的结构让读者看到“关联经验”与“检索经验”的联系。

可见信息优先级：

1. 多个仓库的经验可以指导当前仓库。
2. 返回内容是策略、警告和适用上下文。
3. 图中连接有实际含义，不能只剩一个数据库图标。
4. **Before planning** 和 **After an error** 是醒目的两个访问点。
5. agent 在当前代码中执行，新观察改变下一轮需求。

## 8. 设计语义边界

- 核心输出是抽象指导，不画成自动搬运和执行历史修复程序。
- witness、composer、AST adapter、历史版本执行验证属于 Figure 2、4 的研究内容。
- 不把同仓库 top-3 写成跨仓架构的固定规则；不补节点数、嵌入维度或候选数量。
- 全上下文迭代 code-agent search 是附录中的扩展设想，不画成当前已经完整实现的必经步骤。
- self-improvement 通过复用历史经验体现，不画权重训练或模型参数更新。
- 不添加企业场景、客户数据或新的实验成绩。

这些用于设计者把握含义，不需要把限制条款印到图里。

## 9. 视觉规格与交付

- ICLR research paper 方法图：白底、清楚线条、克制颜色、足够留白。
- 最终宽度 **5.5 英寸，约 140 mm**；以此打印尺寸核查文字，主要标注尽量达到 8–9 pt。
- 高度建议 1.8–2.3 英寸，可据内容调整；优先保证可读性。
- 核心标注使用英文。可用蓝色表示记忆、橙色表示经验输入／抽象、青绿色表示当前 agent 行动，与 Figure 2、4 协调。
- 区分控制流程、查询请求和返回建议；减少交叉箭头。
- 输出可编辑 **SVG、矢量 PDF、高清 PNG**，附字体与配色说明。
- 图形服务于解释方法，不需要堆放公式、数据库产品 logo 或模型品牌。
- 可以自由改变当前六方框布局，重点增强跨仓关联和两个查询时机的辨识度。

建议英文图注：

> ContextGraph turns experience from past coding tasks into reusable strategies and warnings linked to their source context. The agent retrieves this guidance before planning and after errors, using task information and new failure observations to select relevant lessons. It applies the guidance through investigation, edits, and tests in the current repository.

## 10. 随附材料与信息依据

附件按论文图号命名：

- `references/figure2-behavioral-example.pdf` / `.png`：当前 Figure 2。
- `references/figure3-current.pdf` / `.png`：当前 Figure 3 独立版，供核对内容。
- `references/figure4-behavioral-workflow.pdf` / `.png`：当前 Figure 4。
- `references/figure3-current-source.tex`：当前 Figure 3 的 TikZ 图源。

信息依据：当前 `experience-memory.tex`、`executable-analysis.tex`、`method-contract.tex`、`new-results-20260916.tex`。图关系和检索角色也核对了 `agent_memory/neo4j_store.py` 与 `agent_memory/playbook.py`。最终设计可以更换版式，无需依赖原图源。
