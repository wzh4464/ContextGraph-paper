# ContextGraph 经验抽象层级

ContextGraph 当前捕获的经验，主要分布在 **方法级 / 项目级 / 框架级**，并已出现 **组织级** 雏形。

| 经验 | 层级 | 为什么 |
|---|---|---|
| "Run targeted test files or specific test cases rather than full test suites…" | 方法级测试知识 | 通用于任何 Python repo，指导验证策略 |
| "Create a minimal reproduce script early…" | 方法级调试知识 | 是解 bug 的通用 workflow |
| "Avoid trial-and-error editing; make systematic changes and validate each fix with tests." | 方法级工程纪律 | 针对 agent 行为，不绑定项目 |
| "After changing a function signature, search all callers and update call sites." | 方法级 / 轻架构级 | 涉及调用关系，但仍是通用规则，不知道真实系统架构 |
| "Fix root cause, not symptom." | 方法级诊断原则 | 抽象经验，不依赖 repo |
| "Do NOT modify files unrelated to reported bug." | 组织级雏形 | 像团队代码审查规范，但目前只是 Playbook 规则，不具备组织范围 / Owner / 审批上下文 |
| "When you cannot compile C extensions, verify with AST / grep / reproduce scripts." | 方法级验证知识 | 通用替代验证策略 |
| "In Django projects, set `DJANGO_SETTINGS_MODULE` before executing scripts." | 项目 / 框架级操作知识 | 绑定 Django 生态，但不是某个 Django 项目的架构图 |
| "In Django ORM combined query, clone sub-query before `set_values()`…" | 项目级修复模式 | `scripts/inject_repo_specific_strategies.py` 里有这类 repo-specific 策略，但属于手工 / 增强图注入 |
| "DVC CLI help text lives in `dvc/commands/<subcommand>.py`…" | 项目级导航知识 | 有项目目录约定，但当前系统不是自动维护完整 DVC 架构 |
