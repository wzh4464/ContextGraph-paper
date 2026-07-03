# 挖什么才能多解几道 LoLBench held-out 题：基于 634 证据的挖掘清单

## 1. 一句话诊断

**634 的复盘把杠杆彻底锁定了**：codex 对这类 feature（pattern-matching）的实现是**结构上正确的**（3–4k 行、完整的 parser/AST/symtable/compile/ceval 栈，21/21 语义抽查通过），只差 **4 个精确的编译前端 bug**（3 个一行 + 1 处删除）就从 f2p 2/285 跳到 264/285。因此真正的杠杆**不是**抽象规则、不是文件/架构图、不是整段 exemplar、也不是 regen/registration 那套"机械税"——而是**"实现某一类 feature 时最容易犯的那几个精确 bug（CFG 不变量 / 语法规则漏 action / 编译期-vs-运行期报错语义 / 可选 ASDL 字段的 NULL-guard）以及它们的精确修法"**，并且必须**以错误签名为 key**，在 agent 恰好实现该 feature 时才投递。这是四大证伪家族从未瞄准过的一格。

---

## 2. 别再挖的（已证伪，附证据）

| 家族 | 已挖内容 | 证伪证据 | 为什么再挖也没用 |
|---|---|---|---|
| **1. 富度 / 抽象一行规则** | 7691(843)→7694(2115) | 4-graph×2-mode 全 20×20：无配置超过 ~1-3/20；4 个 mcp 臂 **0 次 query_memory 调用**仍 resolve PEP-709（记忆既非必要也非充分） | 泛化类目（code_navigation/error_handling/testing）不含任何 feature 级正确性内容 |
| **2. 架构 / 文件 recipe** | 7695 FeatureRecipe + RepoArchitectureMap | 同日隔离 A/B：0 flip；PEP-615 反而**更差(20<24)**，25KB recipe 把 codex 误导到 Doc/*.rst | 前沿模型**已经知道**要改哪些文件（treat 与 ctrl 改的文件相同）；注入只会稀释或误导 |
| **3. 正确性 exemplar** | 7696 TestAnatomy + ExemplarSkeleton | 同日 A/B：PEP-696 0/29<3/29(更差)，PEP-615 29<30 | 挖的是**正确代码骨架 + 测试断言**，不告诉 agent 它会犯哪个 subtle bug |
| **4. 真实 gold-hunk 类比** | Method4，注入最近训练 PR 的真实 gold 代码（leak-clean jac0.01–0.1） | gold 2/20 vs base 1/20，那 +1=PEP-709 被反作弊 BLOCK **没注入**=方差；f2p 双向剧震，**PEP-634 264→0 / PEP-615 42→24** | 最强 leak-clean 干预仍净零收益，误导和帮助一样频繁 |
| **5. 机械税（regen/registration）** | Method6/7810 CoChangeRule/SymptomRemedy/Runbook，**投递已验证** | 同日 A/B：treat 1/6==base 1/6；agent.log 机械提及 617=168/634=34 次却 pass@1 不变 | **决定性负面**：codex-xhigh **没有忘记**这套税，覆盖的 bug 类它根本不犯，所以无可修 |

> 一条横切结论：**agent 已经拥有的知识注入无用**（文件位置、架构、regen 税）。train_lessons.json 目前**三层全是机械税**（NearMiss/SymptomRemedy/Runbook），且 miner **把每一个正确性 bug 都误标成 regen 修复**（"Segmentation fault"→"make regen-ast"是**错的**）——照它建图会教错 634 那一类的修法。别再往这个方向堆。

---

## 3. 该挖什么（按证据强度排序）

> 贯穿原则（634 教训 + 三次证伪共识）：**挖错误签名→精确修法的机制对（不是 feature 代码）**，以**结构触发器**（错误串 / ASDL `?` / 新 node-kind / 新 grammar 规则）为 key，**只在 agent 实际实现该 feature 时投递**。抽象成不变量/症状键控的微规则，**绝不投递字面 gold hunk**（会像 Method4 一样误导，且版本漂移 codegen.c↔compile.c 会指错文件）。

### ⓵【最高】codex blind-solve 执行日志里的「错误签名 → 下一次编辑 → 是否消失」转移对
- **挖什么**：离散的 `(精确错误串) → (agent 下一步的 diff hunk) → (下次 build 该错是否清除)` 三元组，按 feature-category 归类。正好是 634 那 4 个 bug 的粒度（缺 NEXT_BLOCK / dummy_name 代替 gather / guard 检查 / 运行期-vs-编译期 dup-key）。
- **数据源**：`jie:~/LoLBench-trainpr/runs/codex-solve-r{1,2}/*/agent_out/agent.log`（20 任务×2 run，每个 100K–270K 行）。CPython-820 codex-solve = 228,527 行 / 471 build-test-error 信号；Kafka-820 = 137,982 行 / 865 信号。
- **怎么抽**：**逐转移抽取，不做尾部摘要**（build_codex_debug.py 的尾切片每个日志只拿到 ~4 条泛化规则）。对每个 build/test 失败，抓紧随其后的编辑 + 下一次 build 结果，形成 error→fix 对。
- **为什么这次可能不同（挂 634）**：Method6 已经解析过其中 67 个，但**过滤成了 regen 税**（codex 不忘=null）；**同一批日志里的不变量违规错误从未被抽取**，而 634 证明这一类 codex **确实会犯**。这是区分"未测窗口"与"已失败 Method6"的直接、leak-free 再挖。
- **能翻哪几道**：634（dummy_name/CFG）、654（over-broad check）、701（tokenizer edge）、617（regen/registration plumbing）——这些**单-bug/少-bug 掩盖整模块**的近未命中。
- **leak 风险**：**最低**。传的是机制（j_this≈0），不是 feature 代码；训练 PR 自带，miner 已硬排除 11 个 held-out PR 号。

### ⓶【高】ASDL 可选字段 / 新 node-kind → 全消费者 NULL-guard 义务（S1）
- **挖什么**：每个训练 gold 的 `Parser/Python.asdl` diff 中**新增 `?` 的字段**（798: `expr? value`；810: `int? is_lazy`, `int? level`）和新增的 node-kind（798: comprehension elt 里的 Starred），发成规则：**"PEP 把节点 N 的子 X 变可选/加 kind K → 必须在每个消费者（ast.c / ast_preprocess.c / codegen.c / symtable.c）加 `if(X==NULL){…}else{…}` / `if(elt->kind==K_kind)` 分支；漏一个就在运行期 SEGV / NoneType._fields / 'not a mapping'，不是编译错误"**。用 gold 的 codegen 分支（`if(val==NULL)→DICT_UPDATE else MAP_ADD`）做锚。
- **数据源**：`CAPBench-train harbor_tasks` 的 798/810 golden patch + 训练轨迹 `798 agent.log @15224`（agent 真在 `{**d for d in ...}` 上 SEGV exit 139，靠给 symtable.c 加 `if(value)` guard 修好——**且 agent 修的消费者和 gold 修的不同**：agent 改 symtable.c，gold 改 ast_preprocess.c，两者都对）。
- **怎么抽**：从 asdl diff 提 `?` 字段集，从 gold 提每个消费者的 guard 位点，合成"guard **所有**消费者"的**位点集合义务**（**不是单文件 hunk**——单文件会像 Method4 误导）。
- **为什么挂 634**：这就是 634 bug#2（garbage/NULL 子节点→SEGV）的正确形态，且训练侧 agent+gold **各自独立命中过同一 SEGV 类**，跨任务 leak-clean。
- **能翻哪几道**：634、以及任何让现有 AST 节点长新可选子的 grammar-PEP（646/696 结构同族）。
- **leak 风险**：低（抽象不变量 + 位点集合，非字面 hunk）；只挖 5 个训练 PEP。

### ⓷【高】新-SyntaxError 目录 + 编译期-vs-运行期报错决策表（S2 + 放置分层表）
- **挖什么**：(a) 从 gold `Grammar/python.gram` 提**每条 `invalid_*` 规则 ↔ 其 `RAISE_SYNTAX_ERROR_KNOWN_*("精确文案")` 串**（798 给出 10 对精确 pairs，如 "cannot use dict unpacking in generator expression"）；(b) cpython_17（lazy imports）编码的**4 层报错放置决策表**：纯语法→grammar `invalid_*` 规则（排在合法 alt 之前）；作用域相关→symtable `check_*_context` 读 ste_type/ste flag；fblock/模块相关→codegen `_PyCompile_InExceptionHandler`；**值相关（如 634 重复映射键）→运行期 ValueError（不在编译期）**。
- **数据源**：798/810 golden patch 的 python.gram + symtable.c + codegen.c hunk。
- **怎么抽**：存成 `(feature-shape → [{context, message, 编译期?}])` + 一张 4 行放置分层表，**键控于层知识而非可复制的代码**。
- **为什么挂 634**：直击 634 bug#3（irrefutable 检查漏 `!m->guard` 的假 SyntaxError）和 bug#4（编译期查了 spec 要求运行期查的 dup-key）。这是**层知识**，最高迁移性、最难被误抄。
- **能翻哪几道**：634、654（over-broad 无条件检查——正确形态是 fblock-conditional）。
- **leak 风险**：低。

### ⓸【中高】grammar-rule 必带 action 反模式（S3）+ CFG 基本块义务（S4）
- **挖什么**：(a) **每条新 python.gram 规则必须有完整 action 返回真节点/seq**；`_PyPegen_dummy_name(p)` / 漏 action → garbage asdl_seq → SEGV（798 agent.log @4996/@6108 亲眼见 agent 自己写了 dummy action，与 634 bug#2 同类；正确形态见 cpython_16 `star_named_expressions_sequence: a=... { a }`）。(b) **条件跳转后必须开新基本块**（旧树 NEXT_BLOCK，新树 NEW_JUMP_TARGET_LABEL/USE_LABEL）；症状串 "malformed control flow graph" → 缺块边界，**不是 regen**。
- **数据源**：cpython_16/17 golden 的 python.gram + codegen.c；798 训练轨迹。
- **怎么抽**：症状串键控的 INVARIANT 文本（**只投不变量描述，不投 `NEW_JUMP_TARGET_LABEL(c,unpack_start)` 字面**——634 是 compile.c/NEXT_BLOCK 时代，字面会指错文件）。
- **为什么挂 634**：直击 bug#1（malformed CFG）+ bug#2（dummy action）。
- **能翻哪几道**：634；617/701 的 plumbing 侧沾边。
- **leak 风险**：低（版本漂移使字面无法复制，反而强制抽象）。

### ⓹【中】公共 API 表面 manifest + 新模块交付 manifest
- **挖什么**：(a) 从训练 gold 的 `__all__` diff + 测试 import 行，提**每个 PEP 新增的精确公共名 + 测试如何 import**，蒸馏成"实现 spec 的**精确** sentinel/method/dunder 名，不要私有等价物"；(b) 从 requirement_docs + 训练 PR 的 `new file mode` 提"PEP-N 要求**创建**文件 F 暴露符号 S"的预检 manifest。
- **数据源**：训练 gold `__all__` diff（791 新 math.integer 子模块、793 新 C entry point）；`~/LoLBench-clean/requirement_docs/CPython_PEP-*.md`。
- **为什么挂 634 家族**：696 的确证根因是 agent 用了非-spec 私有机制（`__typing_has_default__`）**从未导出 `typing.NoDefault`**（grep NoDefault=0）→ 掩盖全部 NoDefaultTests；649 的确证根因是**从没创建 `Lib/annotationlib.py`**（678 行补丁 0 处 annotationlib 引用）。这两个都是"漏了交付 spec 的确切符号/文件"，manifest 预检能在 agent 烧预算前逮住。
- **能翻哪几道**：**696（最大绝对上升空间：25 个 ERROR 全被一个缺失符号掩盖）**；649 至少从"结构性遥远"拉回"知道要造哪个模块"（但 649 仍需真写 annotationlib，天花板有限）。
- **leak 风险**：低-中（符号名来自 spec/公开文档，非 gold 实现代码）。

### ⓺【中】TIER-3 行为角落目录（615/680/695 的多-bug簇）
- **挖什么**：同 feature 族训练 PR 的新测试断言的**subtle 行为清单**（TZ folds/gaps、C 加速器 GC-tracking、type-param mangling/deref/lazy-eval、TOMLDecodeError 精确文案），做成"别忘了处理"检查单。已有现成物：`mac:~/capbench_work/correctness_extracted/ta_*.json` 的 `misses` 列表（cpython_16 有 11 条"过 p2p 挂 f2p 的典型错法"）。
- **数据源**：训练 eval_tests / f2p 测试名 + 已生成的 TestAnatomy JSON（只做过静态 eval，从未作为 error-string 键控的可检索反-bug 目录再挖）。
- **为什么挂 634**：615 曾被"自己的 patch + 2 个精确 C-API fail（ZoneInfo C 类型须非-GC-tracked + 不暴露 _weak_cache）"enrich 后**翻成 resolved**（这是 same-task streaming 机制的 leak-clean 子发现，独立于被撤回的 pass@3 污染数字）。
- **能翻哪几道**：615（32/44→，~12 个混合 C/py bug）、680（9/13→，~4 个行为 bug）。**杠杆较低**——这些是多-bug簇，即便完美键控也只逐点蚕食。695（~15 个 scope bug）**不是"几处编辑就到"**。
- **leak 风险**：中——若存 held-out 的 f2p 断言且训练类比太近（646↔798 结构近同），可能泄答案。**每次 resolve 必须同日隔离对照 + Jaccard-vs-gold + agent.log grep git-fetch/web_search**。

---

## 4. 诚实的天花板

即便做到最好，以下对抗性理由说明 pass@1 仍可能不动：

1. **Method6 是最强反例**：它已经投递了**已验证、正确检索、机械精确**的 symptom→remedy 记忆，pass@1 **纹丝不动**（1/6==1/6），因为 codex-xhigh 不忘那类 bug。整个赌注押在"编译前端不变量类（不同于 regen 税）是 agent **真会**犯的"——而 634 只证明 codex **一次**（n=1、一道题）犯了 4 个这类 bug，这是"检索规则能泛化"的**很薄**的证据。
2. **634 自己的结论把可修性归给 test-feedback，不是记忆**：这些是**硬编译错误**，agent **如果看到 build 输出就会修**。静态注入"永远在跳转后 NEXT_BLOCK"——agent **无法知道自己生成的代码违反了它**，除非跑 build。**记忆能携带不变量，但指不出违规的那一行；只有编译器错误能。**
3. **检索稀释/误导是已证倒打**：7695 recipe 把 615 推向 Doc/*.rst（更差），gold-hunk 把 634 推到 264→0。一个精确不变量节点在 2000+ 规则池里，要么 top-k 浮不上来（无效），要么错的浮上来（有害）。
4. **codex 方差是主导项**：634 单题就 3→282→3、264→0；701 deg→72→0；695 84/82/84。任何 +1/+2 都在噪声地板内——**没有同日对照 A/B + 多 seed，什么都不算**。
5. **feature 迁移很薄 + 数据缺口**：train(2025-26) vs test(2020-22) 路径漂移；PEP-701(tokenizer)、FLIP-498/501、全部 Ruff **无训练类比**；PEP-646 **在 harbor 里根本没被 attempt**（数据缺口）。
6. **成本诚实**：找到 634 那"3 个一行"花了人类 **19 个诊断容器** + patch-重跑；事后是一行不代表 agent 或记忆规则能廉价发现。被撤回的 "记忆 1/3→3/3" PPT 是变量/日期混淆冒充记忆效应的长期警示。

**诚实的预期天花板：+0 ~ +2 个 clean resolve**，且**只在配上运行时错误键控投递（见 §5）时**才有机会。最可能翻的近未命中题（按证据）：
- **654（exception-groups）** — 单-bug：无条件加的 "break/continue/return cannot appear in except* block" 检查在模块编译期就 fire，拒了合法的块内 break/continue → 49 个 f2p 全 ERROR。**一个条件化修复很可能解锁 ~全部 49**。（**注意**：post-unmask f2p **未验证**——清了 gate 底层测试仍可能挂，见 caveat。）
- **701（f-strings）** — 单-bug：新 PEG tokenizer 无法 token 化 test_fstring.py:967 的一个构造 → 75 个 f2p 全 ERROR。一个 tokenizer edge-case 修复很可能解锁 75。
- **617（PEG parser）** — 3 个 registration/regen 缺失 gate 全部（GeneratedParser 未 regen / _peg_parser 未注册 Modules/Setup / use_peg flag 未接 sys.flags）。
- **696（type-defaults）** — 缺失 `typing.NoDefault` 公共符号掩盖 25 个 ERROR（§3⓹）。

> 但 634/654/701 的"少-bug掩盖"是**强证据、非已验证**：634 清掉主 gate 后仍有 21 个长尾。**在建任何记忆前，先对 654/701 做离线 unmask eval**（只 patch 前端 gate、重 grade）确认 ROI——654/701 若 unmask 后底层仍大量挂，这条方向的天花板就更低。

---

## 5. 最小验证实验（同日对照，投资前先测）

**测的是 §3⓵ + 运行时错误键控投递**——因为四大证伪的共识是：更好的 error→fix 挖掘**若仍走 up-front 静态注入**（四大家族的投递方式）就是浪费；唯一可能存活 Method6 逻辑的是**在 agent 已犯 bug、错误已出现时**才投递、并指向违规行。

**构建（1 天）**：
1. 从 §3⓵ 挖出一个**只针对 654 与 701 的极小错误键控库**（每题 3–8 条），key = 精确错误串（"'break','continue' and 'return' cannot appear in an except* block" / "unterminated string literal (detected at line …)（test_fstring.py）"），value = 不变量 + 修法方向（**"该检查应只禁止**离开** except* fblock 的跳转，须 fblock-conditional 而非无条件"**）。**仅从 5 个训练 PEP + 训练轨迹挖，绝不碰 654/701 自身 gold。**
2. 加一个**修复步投递 hook**：跑 agent → 捕获**第一个**硬 build/import 错误 → 用该错误串检索库 → 只在这一步把匹配的不变量注回。（这是对 bare test-feedback loop 的严格超集，也是唯一在"agent 已犯 bug"时才 fire、能指向违规行的投递模式。）

**Treatment vs Control（同日、同 seed、隔离并行）**：
- **Control**：codex + 裸重跑（agent 看得到自己的 build 错误，但**无**库注入）——这一臂顺带隔离"仅仅让它多看一次错误"的效应。
- **Treatment**：codex + 上述错误键控修复步投递。
- **两臂都必须能看到 build 输出**（否则测的是错误的东西）。

**任务**：**654、701**（单-bug 掩盖、上限最高），可加 **617**（plumbing，第三个正交类）。

**判定「真收益」vs「方差」**：
- 真收益 = 某题 f2p 从"全 ERROR（load-fail 掩盖）"跃到**大量通过**（654: →~49，701: →大量），且 **treatment 出现、control 不出现**，并**跨 ≥2 seed 复现**（634 曾 3→282→3，单跑无意义）。
- **每个 resolve 必过反作弊**：Jaccard-vs-gold（应 ≈0，机制迁移非抄代码）+ grep agent.log 无 `git fetch`/`ls-remote`/`web_search`（同一 proxy 已泄 github gold **两次**）+ 确认 NO_PROXY 把 github/raw/codeload/pypi 等黑洞化、`web_search="disabled"`（顶层，非废弃的 `[features]`）。
- **廉价前置门**：先做 654/701 的**离线 unmask eval**（只手 patch 前端 gate、重 grade）。若 unmask 后 f2p 仍大量挂 → 这条方向 ROI 低于预期，**别投入建库**；若 unmask 后大量通过 → §3⓵ 值得做全量。

**为什么这个实验判定性**：它把"记忆挖掘"和"投递通道"解耦——如果 treatment 赢而 control 不赢，证明**错误键控投递**是那个未测的杠杆；如果两臂都赢，证明真正的 lever 是 test-feedback harness（记忆无关，正是全记录一致的 forward pointer）；如果两臂都不赢，654/701 的"少-bug near-miss"叙事就得下修，四大证伪 + Method6 的"impl-correctness 不可被静态记忆归约"结论再加一分。