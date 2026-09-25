# MulVul 写法与 RSI 定位

> 历史修订记录：保留文件日期当时的意见、数字和状态。当前稿件以 [main.tex](main.tex) 为准；其中的建议不代表当前待办。

## 标题

**ContextGraph: Executable Memory for Self-Improving Coding Agents**

中文：ContextGraph：面向自我改进编码智能体的可执行记忆。

## 论证顺序

参考 [MulVul 的 ACL 2026 正式版](https://aclanthology.org/2026.acl-long.391/)，采用“研究动机 → 具体问题 → 三个挑战 → 方法 → 结果 → 贡献”的顺序。学习其直接陈述问题、解释模块作用、用结果收束论点的写法，不移用漏洞检测领域的论断。

ContextGraph 的主线是：智能体需要让已有经验帮助后续改进；历史修复中存在当前 issue 没有写出的要求；把这些要求存成可执行记忆，组合到当前操作，再把执行反馈交给 agent。

| 挑战 | 对应设计 | 对应实验发现 |
|---|---|---|
| 摘要丢失触发条件 | Requirement memory：保存输入、操作、预期结果 | 内容干预解释列关系、构造器信息如何影响修复 |
| 历史条件与当前条件分别通过，交互仍失败 | Condition composition：把历史触发条件放入当前操作 | 联合检查发现分开检查遗漏的行为 |
| 已知要求没有落实到代码 | Execution feedback：以具体失败指导下一次修改 | 执行反馈修正文字复查仍未修好的行为 |

摘要保留两类证据：系统结果报告 Verified500 的 69.2% 对 61.8%，以及 Related-Lite99 达到25题所需的轮数；开发实验解释三个机制。原有图表、主表稿、CSV、实验协议及数据不变。

## RSI 在本文中的含义

RSI 指 recursive self-improvement。本文提供的是这一方向中的可执行经验记忆：先前修复留下的行为要求可以成为后续修复的检查和反馈。标题使用 self-improving coding agents，摘要和引言明确联系 RSI。

现有结果验证经验复用与反馈引导修复，不把静态记忆实验改写成已完成多代自主修改学习算法的实验，也不新增“自主更新后持续提高”“通用 RSI 已实现”等结论。这个范围用正文相关工作中的一句实验设置说明表达，避免反复限定。

## 新增参考文献及用途

| 文献 | 放置位置 | 支撑内容 |
|---|---|---|
| [Gödel Agent, ACL 2025](https://aclanthology.org/2025.acl-long.1354/) | 引言、相关工作 | 修改 agent 自身逻辑的 RSI 路线 |
| [Darwin Gödel Machine, ICLR 2026](https://arxiv.org/html/2505.22954v3) | 引言、相关工作 | 通过代码修改、评测与 agent 档案迭代改进 |
| [AlphaEvolve, 2025](https://arxiv.org/abs/2506.13131) | 相关工作 | 可执行评价引导程序演化 |
| [RRSI, 2026-09-21 v1](https://arxiv.org/abs/2609.24972v1) | 相关工作 | 对 agent harness 的递归演化施加正则约束 |
| [MulVul, ACL 2026](https://aclanthology.org/2026.acl-long.391/) | 相关工作；作者写作参考 | 跨模型评价驱动提示词演化 |

已有 ExpeL、ReasoningBank、ACE、Reflexion 文献保留，连接经验积累、记忆更新与反馈；没有用新闻或二手解读替代论文依据。

## 验证

正文8页；参考文献9–11页；总计33页。编译引用全部解析，无 overfull box。标题、摘要、引言、相关工作和结论已相互对齐。构建文件与修改前快照保存在 `/tmp/contextgraph-rsi-revision/`。
