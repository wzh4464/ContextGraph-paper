# 第二审稿人意见:标题与摘要的编辑决定

> 历史修订记录：保留文件日期当时的意见、数字和状态。当前稿件以 [main.tex](../main.tex) 为准；其中的建议不代表当前待办。

我只依据你提供的文本审阅,没有运行任何工具,也没有独立复核任何数字。下面的"支持"仅指稿内自洽,不代表数据已验证。

## 1. 最强的单一洞见,以及现标题和摘要的问题

**洞见:** issue 只描述了完整修复的一部分。通过官方 verifier 的修复,仍可能违反同一项目历史修复已经确立的要求。可迁移的经验单位不是 patch 或相似文本,而是一条要求,连同它的触发输入和可执行的观察。这个单位要沿当前 workflow 组合后才起作用:Django12663 中,当前检查和历史检查各自通过,组合后失败。

- **与 RAG 的区别:** RAG 检索相似内容,帮助完成已陈述的任务,衡量标准是官方得分。这里记忆改变的是任务应满足什么,增益恰好落在官方 verifier 看不到的地方(Table 5 到 7 每个修复都通过官方验证)。
- **与回归测试的区别:** 回归测试在同一代码路径上原样重放旧测试。这里把历史输入条件接到另一个任务的当前操作上,生成两边测试集里都没有的检查。

**现标题**准确,但属于"系统名加过程"的写法,没有说出洞见。标题不是瓶颈,可以小改。

**现摘要**有五个实质问题:

1. 第 3 句就进入 FAISS 机制,还没有交代问题。
2. 346/500 紧跟在 executable witness 和 graph composition 之后,读者会以为增益来自这个机制。§3 自述这些系统是 "expose rules or repair episodes",README 也没有确立方法版本的归因。
3. 14/99→21/99 来自另一条轨道(DeepSeek、curated episodic memory、291 episodes),摘要只用 "Earlier" 一词带过。
4. "explain how history improves the repair itself" 把两条轨道因果地连起来。模型、记忆形态、任务池都不同,稿内证据支持不了这个连接。
5. 负面结果一条都没有出现。

另外,"Remember the requirement, not the patch" 这类口号不能用。Table 6 中 Django12708 只有 Implementation 通过、Requirement 失败;Fig. 2 中原始历史全部通过,而单独的 requirement 句子没有。

## 2. 六篇获奖论文里可观察到的模式

以下是观察到的相关性,不是获奖的因果。样本只有六篇,按结果选出,没有未获奖的对照,而且 arXiv 版本可能与 camera-ready 不同。

- **标题:** 5 篇的标题是一句可反驳的主张或现象(Need Registers、Never Train from Scratch、Get Lost、More Than a Few Tokens Deep、Inherently Succinct)。AlphaEdit 是"名字加精确机制"。
- **摘要顺序:** 依次是通行做法、被命名的缺口或现象、有范围的证据、含义。Registers、SafetyDepth、Lost 三篇都先诊断后补救,补救本身就是对诊断的检验(Registers 原文 "to test this hypothesis")。
- **数字很少:** Registers、SafetyDepth、Succinct 的摘要没有任何数字。其余三篇各有一两个头条数字,总体范围都写明(15 个 LLM、20 万次对话、三种模型)。
- **证据广度与主张广度匹配:** 都是跨模型或架构、同一任务集上的受控对照。
- **留下可复用的词汇:** registers、shallow/deep alignment、aptitude/unreliability。
- **限制写得坦率:** Lost 有很长的 limitations;SafetyDepth 写的是 "can often… some common exploits"。

对本稿最接近的结构是 SafetyDepth 和 Registers,即先诊断现象、再命名、最后给补救。现稿的顺序相反:先系统,再 benchmark,最后个案。

## 3. 标题与摘要

**三个候选标题:**

1. **What the Issue Leaves Out: Past Repairs as Executable Requirements for Coding Agents**
2. ContextGraph: Composing Past Repair Requirements with the Current Workflow
3. Repair Memory as Executable Requirements: Carrying Triggering Conditions from Past Fixes to New Ones

**我选第 1 个。** 它说出了洞见,只作存在性主张,不暗示普遍性或优越性。第 2 个标题把尚处原型阶段的 composition 放在最前面,证据最薄。

**今天可用的摘要(约 209 词):**

> An issue report states only part of what a correct repair must do. We observe that coding-agent repairs accepted by a benchmark's official verifier can still violate requirements that earlier repairs in the same project had already established. ContextGraph stores a past repair as an executable requirement: the required behavior, the input that triggers it, and an observer of the outcome, validated fail-to-pass on the historical versions. Dense retrieval proposes candidate repairs; graph relations over inputs and operations compose a historical condition with the current workflow, in our prototype through two operation-specific Django adapters, and execute it during repair. In selected Django development cases with one attempt per arm, memory-informed repairs preserve query strings, delete redundant uniqueness constraints, or honor a destination timezone; the matched no-memory repairs pass official verification without these behaviors. In one case the current and historical checks each pass while their composition fails, and in a matched pair only the agent given the composed check submits a repair that passes it. Content matters: a requirement sentence sometimes suffices, whereas a historical implementation can import errors that the no-memory repair avoids. Separately, a ContextGraph memory system resolves 346/500 SWE-bench Verified tasks versus 309/500 without memory (GPT-5.4, mini-SWE-agent); this system-level comparison does not isolate the composition mechanism.

14/99→21/99 和"两轮对三轮"移出摘要,留在正文。最后一句 346/309 的条件是:提交前你能确认产生它的系统版本和配置。确认不了就整句删掉,摘要仍然成立。

**未来版本,只给结构,不给任何数字。** 前提是冻结方法后在 held-out 150 上用预先声明的 joint/preserve 套件完成实验。此时摘要第 2 句可以换成"在 ⟨N⟩ 个通过官方验证的修复中 ⟨实测比例⟩ 违反历史要求",末句换成 Graph−Flat 的配对差和 CI。标题也可以升级为 "Passing the Verifier, Missing the Requirement"。没有这些数据就不要用这个标题。

## 4. 实习生与资深工程师的类比

**决定:摘要不放;引言也不用这一对,最多放一句替代表述。** 理由有四条:

1. 这个类比把读者引向"资历等于通用能力"。稿内证据是项目局部的、具体的要求,没有测过通用能力差距。
2. 资深工程师的经验是隐性的、可泛化的。本文的贡献正相反,是显式的、可执行的、带触发条件的,类比会模糊最有区分度的这一点。
3. 负面结果(Implementation 记忆导入错误)在"资深"框架下难以自洽。
4. redirect 例子已经完成了"先例子后细节"的任务,而摘要每个词都很贵。六篇获奖论文的摘要也都没有用人物类比,但这只是观察。

若坚持,可在引言第 2 段末加一句,写成"记得那次事故的维护者",不写"资深":*"A maintainer who handled the earlier fix would ask about the query string; ContextGraph aims to make that question executable."*

## 5. 三个最高优先级的证据缺口

这三项靠改措辞补不上:

1. **现象的普遍性和 held-out 检验。** 现在是挑选的个案,每臂一次尝试,部分检查(MySQL、named-zone、ordinary-subclass)是看过修复之后才构造的。需要在 held-out 150 上预先声明套件、多次重复、给出 CI,才能从"存在"走到"现象"。
2. **归因和噪声底。** 346 对 327 对 309 无法归因到 composition。Table 1 里 Kimi 上 random summaries 为 +7,oracle 在两个 backbone 上低于无记忆,说明单次运行的波动与所称效应同量级。需要 planned Table A–F 和 Flat 对 Graph 的配对比较、多 seed、逐任务配对检验。
3. **泛化、负迁移和成本。** 目前只有 Django 和两个手写 adapter,source273 对 LoLBench 的覆盖是 2/100、DeepSWE 是 0/113。冲突记忆导致的回归率、构建成本和 token 都没有测。

**现在就能改的措辞和整理:**

- §3 的标题去掉 "reduces retry rounds",改成限定到单次实验的表述。
- "identify the information responsible" 加上 "in selected cases";"This progression explains why" 改为 "is consistent with"。
- 对账三处不一致:35/98 与 34.69%;318/500 与 346/500 的版本关系;Codex 的 5/30 与 1/20 分母。
- 投稿 PDF 删去 11 张 TBD 表,以及 benchmark 身份未定的 Gemini、token、Codex 表,留在仓库里作预注册。
- Table 1 领先只有 1 个任务时不要加粗。
- 增加 Limitations 段。

## 6. 现摘要的数字与因果主张审计

| 主张 | 状态 | 处置 |
|---|---|---|
| 346/500 对 309/500 | 供给的聚合数,本次未复核;单次运行,无 CI;方法版本未归因;附录另有旧的 318 | 加限定保留,或删除 |
| 14/99→21/99 | 稿内自洽(McNemar p=.016),但属于不同的池、模型和轨道;记忆含 reference fixes,10 个目标是近重复(剔除后 19/89 对 13/89) | 移出摘要,正文写明轨道 |
| 两轮达 25,对照三轮 | 计数属实,但第 3 轮是 27 对 25(p=.75),每臂只重试自己未解决的任务,不代表更少的 token 或成本 | 移出摘要;236K 对 201K 的 token 数总体未定,任何地方都不要引用 |
| "explain how history improves" | 跨轨道的因果,不成立 | 改成"显示历史要求能增加什么" |
| "three paired Django cases" | 属实,但是挑选的、每臂一次尝试;12708 和 11138 来自六任务 cohort | 加 "selected, one attempt" |
| "composing… recovers… misses" | 只有单个任务(12663)的存在性证据 | 加 "in one case" |
| "graph relations… composed"(一般现在时) | 实际是两个操作特定的 adapter,不是通用的自主组合 | 写明是原型 |
| Table 8 各行 | 是同一任务内的检查,彼此不独立 | 不得汇总成样本量 |
| 负面结果(Implementation 在 72 个时区组合里失败 32 个,其中 16 个是无记忆修复能通过的;Both 的 MySQL 失败;feedback 修复破坏普通子类) | 现摘要没有 | 已写入新摘要 |

## 需要主助手或你确认的三点

1. 346/500 是哪个 ContextGraph 版本跑出来的。
2. 三个 joint 检查是在看到修复之前还是之后构造的。
3. 是否同意把 planned 表从投稿版中移除。

按现有证据,这是一篇洞见清楚、证据仍在个案层面的稿子。上述改动解决的是主张与证据不匹配的问题,不改变证据量本身。
