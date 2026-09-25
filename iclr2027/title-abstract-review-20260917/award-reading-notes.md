# ICLR 获奖论文阅读记录

> 历史修订记录：保留文件日期当时的意见、数字和状态。当前稿件以 [main.tex](../main.tex) 为准；其中的建议不代表当前待办。

阅读日期：2026-09-17。目的：为 ContextGraph 的标题、摘要和论文主线提供参考。

下载并检查了以下六份 PDF，阅读重点为摘要、引言、核心论证/实验组织及结论；这不是对全部证明和实验的独立复现。获奖身份来自 ICLR 官方名单。OpenReview PDF 下载返回 403，因此本地保存的是作者公开的 arXiv 版本，不能一概视为获奖时的 camera-ready。版本、页数、下载地址和 SHA-256 见 [sources.json](sources.json)。

| 获奖年份 | 论文（公开版本） | 本地版本 | 对 ContextGraph 有用的写作观察 |
|---|---|---|---|
| 2026 | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120v1) | 2505.06120v1，2025-05-09，36 页 | 把现实使用中的需求逐步显露变成可比较的实验条件，再区分能力与不可靠性。容易记住的标题背后有明确操作化定义和大规模诊断。 |
| 2026 | [Transformers are Inherently Succinct](https://arxiv.org/abs/2510.19315v3) | 2510.19315v3，2026-05-15，21 页；晚于颁奖 | 换一个评价视角，并精确定义它。结论的强度由定理条件支撑；ContextGraph 不应借用这种确定语气来描述少数开发案例。 |
| 2025 | [Safety Alignment Should Be Made More Than Just a Few Tokens Deep](https://arxiv.org/abs/2406.05946v1) | 2406.05946v1，2024-06-10，25 页 | 用一个具体机制解释多种失败，再用针对机制的干预检验解释。可以学习“统一解释”，不应照搬标题句式或把几个案例写成普遍规律。 |
| 2025 | [AlphaEdit](https://arxiv.org/abs/2410.02355v4) | 2410.02355v4，2025-04-22，32 页 | 标题直接交代关键约束；摘要从知识更新与保留的冲突进入方法、理论和实验。启发是让方法名称之后的词语指出真正起作用的机制。 |
| 2024 | [Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588v2) | 2309.16588v2，2024-04-12，21 页 | 现象、机制解释、简单干预和多场景验证贯通；首页图直接显示所解决的问题。ContextGraph 的首图可以优先显示“分别通过、组合失败、反馈后修复”。 |
| 2024 | [Never Train from Scratch: Fair Comparison of Long-Sequence Models Requires Data-Driven Priors](https://arxiv.org/abs/2310.02980v4) | 2310.02980v4，2024-04-28，19 页 | 通过改变比较条件暴露原结论中的混杂因素。ContextGraph 要固定来源、预算、反馈和检查数量，才能归因于关系组合。 |

官方名单：[2026](https://blog.iclr.cc/2026/04/23/announcing-the-iclr-2026-outstanding-papers/)、[2025](https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/)、[2024](https://blog.iclr.cc/2024/05/06/iclr-2024-outstanding-paper-awards/)。六篇均为 Outstanding Paper，未把 Honorable Mention 当作同一奖项。

这些是样本中的写作与研究组织观察，不是“采用某种标题即可获奖”的因果证据。2025 官方标准明确同时考虑理论洞见、实践影响、出色写作与实验严谨性；2026 官方评语特别肯定多轮对话论文的实验设计和诊断方法。

PDF 下载文件保留在本地；仓库保存本文和来源校验记录。

## 网上写作经验：取一手建议

Simon Peyton Jones 的 [How to write a great research paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2015/02/simon-peyton-jones_paper.pdf) 强调：先提炼一个可复用的核心想法；用具体问题和例子建立直觉；每个贡献都要可检验，并由正文证据支持；按照读者理解问题的顺序组织，而不是复述研究过程。

应用到本文：把“经验记忆提高成功率”的宽泛叙述，收敛成一个更具体、可以反驳的主张——历史输入条件与当前操作的组合，有时能暴露分别执行两者时遗漏的行为。现有 Django 对照支持这个现象存在；发生频率、跨仓库普遍性以及自动组合系统的总体收益仍需独立评估。

## 应保留与应避免

- 保留当前“修好报告中的 bug，仍可能漏掉历史需求”的开场，强化可执行条件的作用。
- 将相似性检索、关系组合和执行反馈写成各自有作用的步骤；FAISS 库名不必占用摘要空间。
- 将系统总体基准、旧版 curated memory、当前可执行开发干预分别标明，不能把不同版本合写成一个已完成的大规模机制验证。
- “实习生 vs 资深工程师”没有对应的人类实验或专业水平测量。引言可用资深工程师如何识别隐含要求作动机，但摘要应直接讲可测行为。
- 获奖样本允许很短的标题，也允许长而具体的标题；不机械学习长度、口号或拟人化。
