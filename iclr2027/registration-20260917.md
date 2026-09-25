# ICLR 2027 摘要登记材料

状态：已于 2026-09-17 成功提交 ICLR 2027 摘要登记，并打开服务端投稿页面逐项核对。投稿编号 **32193**，OpenReview ID **4HhoVdv5da**。[投稿页面](https://openreview.net/forum?id=4HhoVdv5da)。新标题、197 词摘要、10 位作者及顺序均已保存；互惠审稿人为 **Zihan Wu (~Zihan_Wu2)**，不申请豁免；用户已确认全体作者三项声明。未上传 PDF 或补充材料。

论文来源：`exp/iclr2027-audited-evidence-v1`，提交 `7792bd9ded164825c1e91b5955e5d5e22ee64df3`，`iclr2027/main.tex`。标题和摘要已按用户批准的两轮 Fable 5.1 讨论建议修订；采用 197 词机制摘要，不将独立系统汇总数归因于新组合机制。本次没有重新验证实验结果；论文 README 将相关汇总表描述为历史或用户提供结果。

主仓库：`fix/verified-nullable-training-v1`，提交 `d8d3ce47e4eec0df45a959e73c1ff277c84f20da`。

## Title

ContextGraph: Turning Past Repairs into Executable Requirements for Coding Agents

## Authors — 当前预览

以 ASE Industry 编码智能体主稿为基础，补入用户指定的 **XU HAN** 和 **Guowen Yuan**，并按用户最新指示将 **Wang Yuan** 移至最后一位。保留其他作者的相对顺序；不列入 Li Shangyu 或 Jiakun Liu。

| 顺序 | 作者 | 署名角色 | 已选 OpenReview 账号 |
|---|---|---|---|
| 1 | Zihan Wu | 第一作者，与 Jie Xu 同等贡献 | `~Zihan_Wu2` |
| 2 | Jie Xu | 共同第一作者，与 Zihan Wu 同等贡献 | `~Jie_Xu21` |
| 3 | Yun Peng | 通讯作者 | `~Yun_Peng3` |
| 4 | Zeyang Zhuang | 作者 | `~Zeyang_Zhuang1` |
| 5 | Chun Yong Chong | 作者 | `~Chun_Yong_Chong1` |
| 6 | Xin Zhou | 作者 | `~Xin_Zhou24` |
| 7 | Rui Shu | 作者 | `~Rui_Shu2` |
| 8 | XU HAN | 作者 | `~XU_HAN24` |
| 9 | Guowen Yuan | 作者 | `~Guowen_Yuan1` |
| 10 | Wang Yuan | 作者 | `~Wang_Yuan4` |

署名预览：**Zihan Wu\*, Jie Xu\*, Yun Peng†, Zeyang Zhuang, Chun Yong Chong, Xin Zhou, Rui Shu, XU HAN, Guowen Yuan, Wang Yuan**

\* Equal contribution. † Corresponding author: Yun Peng.

共同第一作者及通讯作者标注依据用户对 ContextGraph 的最新指示。符号用于署名展示，不作为 OpenReview 个人账号姓名的一部分。

共 10 位作者。此名单用于 ICLR 登记预览，现已提交；原始 ASE 资料中的 Yuan Wang 保留为来源记录，当前登记采用 Wang Yuan。匿名评审稿的作者栏仍为 Anonymous authors。

Wang Yuan 的登记账号：[`~Wang_Yuan4`](https://openreview.net/profile?id=~Wang_Yuan4)。用户已确认使用该账号关联的 Gmail，取代此前提出的华为邮箱。2026-09-17 现场核对：账号显示 Wang Yuan，邮箱显示 `****@gmail.com (Confirmed)`；完整地址被网站遮蔽，不推断或填造完整邮箱。作者选择通过该 OpenReview profile ID 完成。

补充作者依据：用户提供的 [LoLBench 投稿](https://openreview.net/forum?id=KGbougSbbQ)作者名单。原有名单已包含其余适用作者，新增账号为 [`~XU_HAN24`](https://openreview.net/profile?id=~XU_HAN24)；根据用户明确指示排除 `~Jiakun_Liu2`。

新增 Guowen Yuan 使用用户指定的 [`~Guowen_Yuan1`](https://openreview.net/profile?id=~Guowen_Yuan1)，已核对页面显示姓名及账号 ID。用户链接末尾的句号为标点，不属于 profile ID。

## Abstract

Coding agents can pass a benchmark's official tests while missing requirements established by earlier repairs. We present ContextGraph, a repair-memory prototype that represents past experience as a behavioral requirement, its triggering input, and an executable observation of the outcome. Source-version executions record behavior before and after the historical repair. Similarity retrieval selects candidate experiences, and graph relations connect their input conditions and operations to construct checks for the current workflow. In three selected Django development comparisons, each with one repair per arm, memory-informed repairs preserve query strings, remove redundant uniqueness constraints, or honor destination timezones that matched no-memory repairs omit, although both arms pass official verification. A further development case reveals that a repair can satisfy current and historical examples separately yet fail when their conditions are combined. In a matched pair of agent runs, only the agent given the composed checks and their execution feedback produces a repair satisfying the joint behavior. Memory content also affects correctness: concise requirements sometimes suffice, while historical implementations can introduce additional errors. These findings motivate carrying the conditions behind past repairs into new tasks, where execution can test candidate repairs against those requirements and expose interactions missed by separate checks.

## Suggested keywords

coding agents, long-term memory, program repair, executable requirements, graph-based retrieval

## Suggested TL;DR

ContextGraph turns requirements from past repairs into executable checks that expose omitted behavior in the current workflow.

## Suggested primary area

foundation or frontier models, including LLMs

## 登记字段准备记录（以下待确认事项已在最终提交时完成）

- 10 位作者已按上表顺序匹配 OpenReview profile ID 并加入浏览器预填表；同等贡献、通讯作者标注已在本材料记录，当前作者选择控件未提供这些角色字段。[作者来源与版本区别](ase-author-candidates-20260917.md)保留原始核对依据。
- 同意承担互惠审稿的作者；如申请豁免，需要真实适用的理由。表单要求即使没有合格审稿人，也指定一位作者并选择豁免理由。
- 共同作者对 Code of Ethics、论文公开及不可删除规则、互惠审稿和 AI 披露要求的声明。
- AI assistance 已选择写作润色、文献检索、研究构思或执行，以及起草论文章节。本次摘要由 AI 起草并经用户批准，论文 AI use statement 已同步披露。

用户明确要求先不上传 PDF，除非表单强制要求。2026-09-17 重新读取当前 Submission invitation，PDF 字段 `optional=true`，浏览器 PDF 及补充材料文件选择均为空，因此本次只登记摘要，不上传 PDF。本材料不请求 Google's Paper Assistant Tool 反馈，也未使用其一次性反馈额度。

表单三项必需声明仍未勾选，需作者提供事实确认：

1. 本人和全体共同作者已阅读并承诺遵守 ICLR Code of Ethics。
2. 本人和全体共同作者理解投稿会在评审开始时公开、评审结束后接受或拒绝的论文都会公开作者；撤稿会立即公开作者，评审开始后不能删除、隐藏或撤回公开记录。
3. 本人和全体共同作者同意遵守互惠审稿、AI 披露及 Author Guidelines 中的投稿要求。

## 截止与来源

- 摘要：2026-09-18 23:59 AoE，即北京时间 2026-09-19 19:59。
- 全文：2026-09-25 23:59 AoE，即北京时间 2026-09-26 19:59。
- 摘要截止后不可增删作者；实际表单还将互惠审稿作者及豁免相关字段标为截止后不可修改。
- [ICLR 2027 Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines)
- [OpenReview ICLR 2027](https://openreview.net/group?id=ICLR.cc/2027/Conference)
- [实际 Submission invitation](https://api2.openreview.net/invitations?id=ICLR.cc%2F2027%2FConference%2F-%2FSubmission)，读取时间 2026-09-17；duedate=1789819140000。

## 本轮修改与校验

- 已将用户批准的新标题、197 词摘要及 TL;DR 写入本地稿件与浏览器表单，并逐字核对一致。
- 10 位作者的顺序及 profile ID 已重新核对，PDF 和补充材料为空。
- OpenReview 官方资格检查确认 `~Zihan_Wu2` 具备 ICLR 2027 reciprocal reviewer 资格；资格不等于本人已承诺承担本次审稿，最终人选仍待用户指定。
- 尚未提交，仍待互惠审稿人和全体作者三项声明的事实确认。

## 最终提交核验

投稿编号 32193，ID 4HhoVdv5da。服务端摘要与本地 submission-payload.json 逐字一致；作者顺序已核对，末位 Wang Yuan；Reciprocal Reviewing Author 为 Zihan Wu，Exemption 为 We do not need an exemption。三项声明和四项 AI 用途披露均已保存。无 PDF 链接。本记录中的较早准备状态仅表示当时状态，已由本节覆盖。
