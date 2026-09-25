# Fresh PhD 视角逐句审读

> 历史修订记录：保留文件日期当时的意见、数字和状态。当前稿件以 [main.tex](main.tex) 为准；其中的建议不代表当前待办。

本记录对应可读性修订；后续架构主线与段落移位见 `architecture-story-20260923.md`。

审读对象：当前 ICLR 稿件的摘要、正文、图注、表注和编译进入 PDF 的附录文字。读者假设：了解基本机器学习、会读 Python，但没有做过 coding-agent memory，也不熟悉 Django。参考文献条目不作语言改写。

## 判断

修改前，新生可以读懂“历史经验能够帮助修复”的大意，但很难准确复述 ContextGraph 如何工作。主要障碍是术语先于解释、具体输入关系出现太晚，以及实验条件被压缩成内部简称。这一轮直接修改这些句子，并保留三条设计理由及对应实验。

修改后的核心过程可以复述为：**从旧修复中记住需要满足的行为和触发输入；把这个输入放进当前正在修复的操作；运行检查，把失败交给 agent 继续修改。**

这是基于逐句审读的判断，尚未做真实新生阅读测试。

## 具体句子怎样改

以下记录需要修改的句子或相邻句组；清楚的句子保留。英文摘录对应本轮修改前后的实际文字，省略了引用和部分上下文。

| 位置 | 原句中的障碍 | 新生会卡在哪里 | 本轮处理 |
|---|---|---|---|
| 摘要开头 | “guidance for subsequent improvement” | 什么 guidance？改善哪一步？ | 直接说学习旧修复，再说明新任务的测试通过仍可能遗漏旧要求。 |
| 摘要方法 | “an executable memory framework” | 记忆为什么能执行？ | 定义为 “a requirement linked to a runnable example and its expected outcome”。 |
| 摘要方法 | “uses these relations to compose checks” | compose 具体做什么？ | 改成把历史输入与正在修复的操作结合，运行检查并返回失败。 |
| 摘要结果 | “25 resolutions … in two passes” | resolution 和 pass 指什么？ | 改为 25 个任务、两轮修复，对照需要三轮。 |
| 摘要案例结果 | “Development experiments explain the mechanism” | 系统成功率是否验证了所有新机制？ | 写成开发实验分别考察三项设计，并列出各自发现。 |
| 引言首句 | “make agents better at improving themselves” | 定义重复了术语本身。 | 明确为改进 agent 自身的问题求解流程。 |
| 引言 agent | 默认知道 coding agent | agent 在软件仓库里做什么？ | 用 reads, edits, and tests a repository 给出动作。 |
| 引言重定向例子 | “deployment prefix … query parameters” | 没有 URL 很难想象两个要求。 | 加入说明性 URL `/app/login?next=home`，再区分当前前缀问题与历史查询串要求。此 URL 是解释例子，不是新增实验输入。 |
| 引言历史要求 | “historical requirement” | 指历史代码，还是当前仍要满足的行为？ | 首次出现时说明是 earlier fix 所要求的行为；适用性判断仍在方法中解释。 |
| 图 2 图注 | 两段 Django `filter` 代码直接互换 | 不懂框架就看不懂转换。 | 先说等值查询变成两个端点都等于 x 的范围查询，再指明历史类型 R 的作用。 |
| 挑战一 | “constraint deletion … different columns” | 为什么不同列就不行？ | 明确：bug 由两个约束共享列触发，分开列测试会遗漏它。 |
| 挑战二 | “current query … historical named-tuple example” | named tuple 尚未解释。 | 挑战先用普通输入与特殊输入类型说明组合问题；背景再解释具体类型。 |
| 引言方法概述 | 再重复一次 69.2% / 61.8% | 增加篇幅但没有帮助理解设计。 | 改为引出三个设计与对应贡献，结果仍保留在摘要、首图和实验。 |
| 背景相关方法 | 连续列出多种 memory 术语 | 阅读主线被名词打断。 | 缩成这些方法保存、组织经验；随后立即说本文要保留什么。 |
| 背景构造器 | “different constructor calls” | 相同值为何产生不同 bug？ | 说明本例中 named tuple 接收两个参数，普通 tuple 子类接收一个 iterable。 |
| 背景 lazy User | 未解释 lazy | “懒”的对象与条件组合有何关系？ | 定义为需要时才加载 user 的包装对象，再解释它被放进范围端点。 |
| 方法公式前 | 先出现版本符号和 memory tuple | 为什么需要这些项？ | 先用一句话概括：要求、测试例子、旧修复前后结果；再给公式。 |
| 方法构造 | “A source writer …” | source writer 是人还是模型？ | 明确为 language-model writer，随后说明执行和研究者检查。 |
| 方法图结构 | “graph links … input roles” | 节点与边到底存什么？ | 列出链接的记录，并用范围类型/端点、时区源/目标说明关系。 |
| 方法检索 | “three distinct witnessed sources” | witnessed source 是什么实体？ | 改为三个具有已验证示例的历史修复。 |
| 方法检索 | “Graph joins return …” | 为什么突然讲数据库操作？ | 改为沿图链接取回要求、程序、执行结果和输入角色。 |
| 方法检索 | “adjacent operation” | adjacent 是相邻代码行，还是相关功能？ | 用不同数据库约束的删除操作说明。 |
| 方法组合输入 | “a current executable program Pq” | 整个仓库能直接成为 Pq 吗？ | 明确 Pq 是复现当前 issue 的可运行程序；保留其准备方式的独立段落。 |
| 方法 adapter | “An adapter implements the combination” | 用待解释词解释待解释词。 | 定义为面向某类操作的小型程序变换例程。 |
| 方法范围公式 | “scalar equality lookup … point-range semantics” | 两个程序为何具有相同预期结果？ | 先说明两个端点都等于 x；再解释适用条件下应选出相同数据行。 |
| 方法嵌套查询 | “lazy User inside an annotated subquery” | 框架细节遮住真正要保留的东西。 | 改为 lazy User 留在原嵌套查询中，不能替换为更简单的整数。 |
| 实验设置 | Verified500 / Related-Lite98 / 99 | 名称中的数字为何不同？ | 明确任务数，以及 98 题设置排除一个共同环境构建失败。 |
| 实验指标 | “neighboring behavior” | 是相邻函数还是相近测试？ | Preserve 定义为已正常工作的相关行为；Combined 要求同一补丁通过全部三组检查。 |
| 内容实验 | “The constraint Requirement agent” | Requirement 是方法名还是某个 agent？ | 改为只收到约束文字要求的 agent；四种输入在前一句逐一说明。 |
| 内容实验 | “both retrieved packets” | packet 是网络包还是记忆？ | 改为 retrieved memory sets。 |
| 内容实验 | “non-builtin sequences into positional arguments” | 不易看出为什么会破坏子类。 | 直接说把每个元素作为独立参数传入，会破坏另一种构造约定。 |
| 组合实验 | “an original-base pair” | 两组从什么状态开始？ | 写明两个 agent 都从原始未修复代码开始。 |
| 反馈实验 | “name disambiguation” | 修复实际做了什么？ | 改为区分约束名称并修好两类情况。 |
| 跨模型实验 | “backbones” | 和 coding agent 是同一个东西吗？ | 正文统一使用 language models / models。 |
| Oracle 对照 | “one paired summary” | 为何这是特殊对照？ | 说明直接给出已知相关摘要，跳过检索。 |
| 重试实验 | “pre-base history … each subsequent pass” | base、pass、attempt 的关系不明。 | 解释历史先于目标代码版本，每轮只重试尚未解决的任务。 |
| 重试表注 | “Wins/losses … exact McNemar” | 7/0 是运行次数还是任务数？ | 明确 wins 是仅 memory 成功的任务，losses 是仅无记忆成功的任务。 |
| 池大小实验 | “competition during ranking” | 池扩大为什么不一定更好？ | 说明新增来源也会改变进入 top-three 的来源。 |
| 池大小结果 | “not monotonic” | 可以更直接。 | 改为结果并未在每一步都改善。 |
| 表注版本名 | V1 / V2 / best-of-two | 需要记内部标签，且旧重试次数并不统一。 | 改成 one attempt 和 results including failure reruns。数值保留。 |
| RSI 相关工作 | “regularizes harness changes” | 两个未解释术语叠在一起。 | 改成约束协调 agent 工具与动作的代码变更。 |
| 附录案例 | “Both still generates …” | Both 容易被读成“两个都”。 | 改成 the repair given Both；Requirement / Implementation 同理。 |
| 附录案例 | “second container reconstruction” | 第二次重建在哪里，为什么重要？ | 说明查询处理代码中较晚的一次输入容器重建仍未被修复。 |
| 附录方法 | “typed bindings … observer” | 这些对象与程序怎么对应？ | binding 解释为对象到角色的映射；observer 是检查运行结果的代码。 |
| 附录消融 | “C--B … C--G … F--C” | 必须先找表格才能读懂整段。 | 对每个字母比较同时写出改变的内容：关系来源、组合方式、编辑前执行反馈。 |
| 附录测试 | fail-to-pass / pass-to-pass | 不知道两类测试的职责。 | 增补请求修复的行为与原来已正常行为的解释。 |

## 逐段复读后的结论

| 部分 | 新生现在应能回答的问题 | 仍需技术基础的内容 |
|---|---|---|
| 摘要、引言 | 为什么旧经验有用但纯文字不够？三个设计各解决什么问题？ | RSI 是研究方向，本文重点是经验记忆。 |
| 背景 | 相同值为何不能替代相同输入类型？为什么分开通过仍可能组合失败？ | Python 对象、构造函数和基本数据库查询。 |
| 方法 | 存什么、取什么、怎样改写当前复现程序、如何使用失败反馈？ | 完整复现还需附录的输入绑定与适配器细节。 |
| 整体效果 | 比较哪些方法，数字用什么任务数，成功如何判定？ | 各历史比较保留自己的模型与尝试设置。 |
| 三组机制实验 | 每组改变了什么，检查发现了什么，结论是什么？ | Django 的具体缺陷机制在附录展开。 |
| 扩展实验 | oracle 是什么、重试如何累计、池变大为何不必然更好？ | 配对统计检验保留标准名称。 |
| 附录计划 | 哪些尚待完成，分别检验哪个设计？ | 协议中的预算、分组和统计定义保留必要精度。 |

## 保留的必要区别

整体成功率衡量经验复用的系统效果；开发案例展示保存触发条件、组合检查和执行反馈如何帮助修复。正文只在设置处集中说明一次。自动准备当前复现程序仍是红色待实现内容，不能通过语言润色写成已完成。

保留全部原图、实测数据、红色待填项和绿色补充项。没有增加假想实验结果，没有运行新实验。

## 验证

正文保持 8 页，总计 33 页。逐块对照确认本轮编辑前后的 38 个 tabular 块完全一致（部分编号表含多个 panel）；图文件及其引用保持不变。编译无未解析引用与 overfull box。最终构建和页面预览保存在主仓库 `outputs/paper-fresh-phd-review-20260923/`。
