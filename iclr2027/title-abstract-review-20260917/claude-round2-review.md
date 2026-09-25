# 第二轮回应

> 历史修订记录：保留文件日期当时的意见、数字和状态。当前稿件以 [main.tex](../main.tex) 为准；其中的建议不代表当前待办。

## 接受的更正

- **RAG 与回归测试的二分法撤回。** 新颖性只落在表示(要求、触发输入、可执行观察,在历史版本上 fail-to-pass 验证)、适配和证据三点上,不写"首个"。
- **三个 Django 案例同库,不是独立样本;表内检查不是任务。** 因此不报比例。
- **不主张图的必要性。**
- **318 与 346 不矛盾。** 附录需标明 318 属旧版本;346 的 run-to-method 映射仍是实质缺口。

## 标题:选 A

**ContextGraph: Turning Past Repairs into Executable Requirements for Coding Agents**

- 原标题没有交代对象。
- B 的 "Executable Memory" 正是 ExpeRepair、TRACE 等已占的类别;"what bug reports leave out" 暗示系统已覆盖这些遗漏,证据撑不住。
- C 丢掉了系统名的连续性,我撤回首轮对它的选择。
- A 只陈述表示上的转换,与现有证据匹配。
- 如果转换含人工步骤,正文须写明。

## 对你 176 词稿的质疑

1. **"must still hold" 预设了适用性。** 执行只能判定修复是否满足检查,判定不了这条检查是否该适用。历史实现导入错误的负面结果说明历史并不总是对的。应改为携带"要求产生时的条件",交给执行检验。适用性由谁判定,须在正文写明。
2. **"controlled comparison" 名不副实。** 实际是单任务、单次运行的一对匹配,应直接写 "two matched runs"。
3. **"guides its correction" 是 n=1 的因果表述。** 该 feedback 修复还破坏了普通子类。只能写"提交了通过组合检查的修复"。
4. **"recover omitted requirements" 过于一致。** 12708 中单独的 Requirement 记忆失败,应写成具体行为。
5. **"complement" 与 "Together… motivate" 又把两条轨道连了起来,** 与你同意的拆分相悖。
6. **"7.4 percentage points" 是单次运行、无 CI 的重复信息,** 应删去。
7. **"pass a task's tests" 应写成 official verifier。**
8. **图关系用一般现在时不妥,** 应限定为 prototype。

## 与你的分歧

我同意把 two-adapter 细节压缩进 "prototype"。但 "one run per arm" 这四个词要留:没有它,"three cases" 会被读成比率。负迁移那一句保留,它是稿内区分度最高的发现,也顺带约束了"历史必然适用"的误读。

## 最终摘要(约 209 词)

> An issue report states only part of what a correct repair must do. Coding-agent repairs accepted by a benchmark's official verifier can still miss requirements that earlier repairs in the same project established. ContextGraph aims to make such requirements actionable by representing a past repair as a behavioral requirement, the input that triggers it, and an executable observation of the outcome, validated fail-to-pass on the historical versions. Similarity retrieval proposes candidates; in our prototype, graph relations over inputs and operations connect a historical triggering condition to the current workflow as executable checks. In three selected Django development cases, one run per arm, memory-informed repairs preserve a query string, remove a redundant uniqueness constraint, or honor a destination timezone, while matched no-memory repairs pass official verification without these behaviors. In one case, a repair satisfies the current and historical examples separately but fails when their conditions are combined; of two matched runs, only the one given the composed checks and execution feedback yields a repair that passes them. Memory content matters: a requirement sentence sometimes suffices, whereas a retrieved implementation can import errors that the no-memory repair avoids. These cases show existence, not prevalence: memory can carry a past requirement's triggering conditions into a new task for execution to examine.

**可选句(不计入字数):**

> Separately, in one run per arm on SWE-bench Verified (GPT-5.4, mini-SWE-agent), a ContextGraph memory system ⟨version/config⟩ resolves 346 of 500 tasks versus 309 without memory; this system-level comparison does not isolate the composition mechanism.

这句只有在版本、配置和单次运行三项都确认后才加入。任何一项未确认就整句不放,也不要用 318 替代。

## 工程师比喻

不给它任何摘要篇幅:摘要每个词都要用来界定证据范围,而这个比喻恰恰暗示了稿内没有测过的通用能力差距。
