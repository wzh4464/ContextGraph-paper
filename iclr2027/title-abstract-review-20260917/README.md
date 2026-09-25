# ContextGraph 标题与摘要评审资料

> 历史修订记录：保留文件日期当时的意见、数字和状态。当前稿件以 [main.tex](../main.tex) 为准；其中的建议不代表当前待办。

2026-09-17，针对 `exp/iclr2027-audited-evidence-v1`，源稿提交 `7792bd9ded164825c1e91b5955e5d5e22ee64df3`。

- [最终建议、英文摘要和中文翻译](recommendation.md)
- [获奖论文阅读笔记与公开来源](award-reading-notes.md)
- [摘要与实验结论的证据边界](evidence-boundaries.md)
- [Claude Fable 5.1 第一轮独立评审](claude-round1-review.md)
- [Claude Fable 5.1 第二轮讨论](claude-round2-review.md)
- [下载来源、版本与校验值](sources.json)
- 调用状态、原始请求/日志、下载 PDF 和投稿回执仅保留在本地。

主助手阅读了当前正文、附加结果、计划表和修订说明，并抽读六篇获奖论文的摘要、引言、核心论证/实验组织、结论；Claude 第一轮输入包含全文 LaTeX、README、附加结果与计划表，以及获奖论文开篇和结论摘录。第二轮用于讨论标题选择、精简后的摘要和科学表述边界。AI 意见不是新的实验结果。

Claude Code 2.1.274 通过用户指定的本地代理调用，主评审模型由实际返回的 `modelUsage` 确认为 `claude-fable-5-1`。初始未使用代理的请求返回 403，未产生可用评审；相关失败日志保留作区分。

本目录保存研究材料和建议稿；未修改论文 `main.tex`，未向 OpenReview 提交标题、摘要或 PDF。
