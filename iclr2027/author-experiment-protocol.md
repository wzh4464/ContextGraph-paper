# 作者用实验协议

本文件保留 2026-09-22 简化论文前的完整实验操作说明，供实际执行和核查使用；不编入论文。正文使用 ContextGraph 和具体实验设置，不使用内部发布标签。实验数值判读见 `实验补齐与结论判读.md`，运行配置见 `method-evaluation-contract.json`。

## 方法与实现协议

```latex
\section{Default method contract and implementation boundary}
\label{sec:method-contract}
This appendix specifies the default to freeze for the new comparisons. It does
not retroactively rename historical systems or assert that a release has been
completed. \expmark{CG-Fixed-v1 is a specification awaiting its release manifest;
the automatic public-program preparation, unified applicability assessor,
and validation interface remain to be implemented and audited.} The existing retrieval and two operation-specific
adapters are development prototypes.

\subsection{One default, separately named variants}
CG-Fixed-v1 fixes same-repository Qwen3-Embedding-8B/FAISS top-three retrieval,
source273 plus an admitted pre-base expansion, complete witnessed records,
typed source bindings, current-contract admission, frozen operation adapters,
and execution feedback. It does not use an initial function-match veto,
iterative pool search, or cross-target memory updates. Rejecting a candidate
does not silently retrieve a fourth source; empty slots and fallback are counted.
All attempts, including applicability, construction, execution, and failures,
share the total target budget. Source construction and any human work are
reported separately and included in amortized cost.

CG-Agentic-v1 changes only candidate selection and is evaluated in E10 under
the same downstream gate, composer, source bank, and total budget. CG-Online-v1
changes only the cross-task update policy and is evaluated in E14. An
agentic-plus-online combination, if later tested, requires its own manifest;
it cannot be pooled with either isolated variation. E05 retrieval alternatives
remain development ablations of the fixed candidate policy, not a license to
choose the held-out winner after observing its results.

The manifest must bind source/target IDs and exposure status; source data and
index hashes; Qwen revision; model/agent versions; gate prompt/schema and
budgets; public-program preparer, support classifier, and their resource caps;
binding extractor; every adapter and its preconditions; validator,
fallback, total budget, and benchmark verifier. A label without these hashes is
not a frozen release. E07, E15, the default rows of E08/E09, Figure~\ref{fig:results-overview},
and the final abstract must reference the same release. Neither an adapter fix
nor a source-bank expansion may use E15 outcomes and retain the old release ID.

\subsection{Constructing the current executable program}
\label{sec:public-program}
The default starts from a public issue, the repository at its pinned base,
and the benchmark's agent-visible environment; no executable reproduction is
assumed. A bounded no-memory prefix of the common coding agent performs the
following steps before methods receive arm-specific memory:
\begin{enumerate}
\item Inspect public source, tests, build instructions, and version-matched
documentation. Localize the issue's operation and record file/symbol spans
and the public evidence connecting it to the reported behavior.
\item Extract a supplied reproduction or generate a minimal current program.
Prepare imports, dependencies, objects, data and environment using permitted
agent tools; retain the issue's types, roles, and operation sequence.
\item Emit a versioned artifact containing setup/exercise/observe functions,
an invocation command, runtime/fixture identities, the operation span, role
bindings, a contract-grounded expected outcome, and construction provenance.
Record whether code was extracted, adapted, or generated.
\item Execute on the original base. The intended operation must be reached
with a meaningful observer; passing is not required and a real violation is
retained. A setup error, unexercised operation, unjustified oracle, or exhausted
budget returns a named failure state rather than a fabricated reproduction.
\end{enumerate}
The prefix cannot access target gold patches, withheld evaluator checks,
method memory, or later repairs, and cannot edit the candidate implementation.
Its fixture files and traces are kept separately. Prompts, step/token/time
caps, allowed tools, validation, and fallback are frozen before target runs.
Numerical caps remain release-manifest fields to fill, not hidden extra budget.

For each target/repetition, all methods receive the same resulting public
artifact, status, and prefix transcript. The solver branches only afterward.
The entire prefix consumes each arm's total work allowance even if physically
executed once and reused. Report actual billed prefix charges once in the
campaign ledger; separately attribute the full prefix cost to each method's
end-to-end estimate, so shared work is neither free nor billed multiple times.
If preparation fails, all arms retain that status and the remaining budget;
CG may deliver an accepted cited requirement as text but no invented joint
check. The agent can continue ordinary repair work, but an unreleased second
preparer cannot silently replace the frozen composition input.

No researcher prepares or fixes individual target fixtures in the automatic
E07/E15 arms. Target-specific human preparation is a separately labeled
assisted setting with time and edits recorded. One-time development of a
general adapter is different from preparing a particular target's input.
The current \texttt{compose\_public\_lookup\_ast\_v1.py} extracts named
Models/TestCase spans and uses researcher-written setup/observer wrappers;
it is evidence for a known-case transformation, not the automatic entry point
specified here. Existing development results retain that conditional scope.

\subsection{Support strata and the scope of mechanism claims}
\label{sec:support-strata}
Freeze the adapter registry's supported languages, APIs, operations, and type
preconditions. Before any arm is run, use a frozen public-evidence classifier
on each original issue/repository snapshot to record within-scope,
outside-scope, or uncertain, including the matching rule and input hash.
This classification precedes preparation, acceptance, delivery, and outcomes;
its preflight work is recorded in the common preparation allowance. Predicted
support is not guaranteed successful construction. Do not relabel strata after
an execution fails or an adapter is added.

Report all assigned targets in every stratum for every method, including
no-$P_q$, empty retrieval, rejected obligations, unsupported composition,
text fallback, and missing verification. Break down downstream delivery as
an outcome, not a filter defining the efficacy population. Support-stratified
system effects do not identify mediation by composition. The current E03
mechanism claims are restricted to its development panel. Attributing held-out
gains to a component requires a separately preregistered replication on
untouched tasks, not juxtaposing successful E03 and E07/E15 results.

\subsection{Applicability: evidence, actions, and ownership}
The gate evaluates an obligation on the current version, not whether a historical
program happens to execute. Its input is the original public target snapshot,
current issue, version-matched contracts/tests, reachable pre-base history,
and the source requirement and evidence. Target gold patches, withheld checks,
future task results, and the agent's evolving patch cannot justify the obligation.
If existing code conflicts with a documented bug report, code behavior alone
cannot settle the intended semantics.

The output is \texttt{accept}, \texttt{reject}, or \texttt{uncertain}, with current
contract anchors, source anchors, input/type/operation mapping, observer
justification, and a reason code. Acceptance requires an affirmative current
contract anchor and compatible semantics. An explicit current contract change
rejects the old obligation. Missing evidence, ambiguous mappings, or unresolved
conflicts cause abstention. A numeric LLM confidence score alone is insufficient.

\begin{itemize}
\item The source writer proposes witnesses; source executions and recorded
researcher semantic review admit historical evidence. This review is not a
current-target applicability decision.
\item The automatic runtime assessor makes target decisions using a fixed
schema and the solver backbone. Bounded public-evidence collection is allowed;
no per-target human correction is admitted in the automatic comparison.
\item Independent, arm-blind evaluation annotators adjudicate current validity
for E15/E16 and seal their evidence. Two annotators resolve disagreement through
a third reviewer; unresolved cases remain uncertain. Their labels are withheld
from the runtime assessor and solver.
\item Developer review may improve the gate on source/development tasks before
freeze. A human-assisted target decision must be labeled as a separate variant,
with its time and interventions reported.
\end{itemize}

Rejected and uncertain requirements supply no mandatory historical assertion.
The agent continues on the public task, with no claim that absence of memory
is evidence of irrelevance. Accepted but unsupported requirements can be
provided as cited text only. Their original source witnesses remain in the
bank as source evidence; they are not executed or scored as valid current
checks merely because an adapter is unavailable. This fallback replaces the
older plan's unqualified delivery of a stored witness.

\subsection{A uniform composition interface}
The composer consumes $(P_q,m,b,\mathcal A)$: the current public program and
runtime identity, accepted memory, a typed binding record, and a versioned
adapter registry. A binding contains input values/types, constructors, operation
arguments, relations, current object references, and source-evidence spans.
Every alternative binding producer serializes this same schema. The composer
returns a candidate program, observer, mapping trace, adapter ID, resource
cost, and a status: valid, unsupported, invalid fixture, invalid binding,
invalid observer, or uncertain semantics.

For each accepted record, select an adapter whose declared operation signature
and semantic preconditions match. Instantiate it with the bindings, preserving
both the source trigger and current operation sequence. The shared validator
checks the program/fixture interface, provenance and binding completeness,
non-vacuous triggering, and an observer whose expected outcome is justified
without consulting the candidate repair or the operation being tested as its
own oracle. A syntax check or absence of exceptions alone is insufficient.

A controlled execution can yield a meaningful requirement violation. Such a
failure is useful feedback and must not be filtered out for failing. Import,
setup, invalid-observer, and unrelated infrastructure failures remain
unassessed; they cannot be reclassified as target semantic failures. Repair
observations may guide edits but cannot rewrite the frozen requirement,
observer, acceptance evidence, or target evaluation suite.

\paragraph{What is automated and what is authored.}
The range adapter in \texttt{lookup\_condition\_product.py} and the timezone-role
adapter in \texttt{construct\_timezone\_role\_family\_v1.py} are researcher-written.
Restricted source AST extractors recover the bindings they support; source
writers generate witness candidates. Their current support is limited to the
specified Python/Django operations. The existing free-form composition
prototype is not evidence of an automatic, general-purpose adapter learner.
New operation families require a documented adapter, preconditions, validators,
and source/development tests, all frozen before evaluating untouched targets.
Unsupported cases measure a limitation rather than receiving an ad hoc fix.

\paragraph{What E03 can attribute.}
B and C share the exact composer, adapter registry, validators, gate decisions,
candidate IDs, and solver feedback policy. B reconstructs all bindings from
complete textual records; C receives stored bindings in the same schema.
The common gate exports only admission decisions and current-contract anchors
to these arms; withheld bindings and mapping traces must not leak through its
explanation, validation messages, or another tool response.
C--B therefore tests supplying explicit relation information rather than
requiring its reconstruction. D/E remove one binding family before the same
bounded reconstruction step. G receives C's bindings but uses a free-form
composer under the same shared validation and check budget; C--G tests composer
choice. F additionally supplies the same checks' execution observations before
editing; ordinary agent tools remain available to every arm. F--C measures
supplied observations, not removal of all possible execution feedback.
C--B does not establish that
Neo4j or a graph storage format is indispensable: serialized equivalent
relations can support the same computation.

H/I replace a separate historical check with a joint check under matched
two-slot and feedback budgets (Appendix~\ref{sec:planned-graph}). Preparation
and delivery failures remain assigned. I--H estimates this development-panel
policy effect, not the cause of all formal-benchmark gains.

```

## 实验设计与填写说明

```latex
% Proposed experiments only; TBD cells are not measured outcomes.
\begingroup
\raggedbottom
\expcolor
% Keep planning tables with their protocol instead of floating past headings.
\makeatletter
\renewenvironment{table}[1][]{%
  \par\addvspace{\intextsep}\noindent
  \begin{minipage}{\linewidth}\def\@captype{table}%
}{%
  \end{minipage}\par\addvspace{\intextsep}%
}
\makeatother

\section{Experiment 1 plan: matched repair effectiveness}
\label{sec:planned-outcomes}
\ifexperimentreview
\noindent\textbf{Internal author checklist.} Red marks experiments and results
still to complete. Black coverage counts are existing measurements. Bands in
``Author check'' notes are proposed practical-effect examples, not data,
predictions, or power calculations; see Appendix~\ref{sec:experiment-decisions}.
\par\medskip
\fi
These tables specify the experiments needed to extend the paper's argument.
\textit{TBD} denotes an unmeasured result, not a projected score. Sample sizes
are proposed allocations. All new solver experiments use the authorized
DeepSeek V4 Pro OpenRouter route; new embeddings use the pinned Qwen3-Embedding-8B
space. Each submission is verified immediately with its benchmark's verifier;
independent semantic trajectory reviews occur at most ten minutes apart.
Intervals resample paired targets, retaining each target's repetitions together.
The common no-memory public-program prefix is specified in
Appendix~\ref{sec:public-program}; every arm receives its artifact or failure
state and bears its full attributed resource cost within the total budget.
Infrastructure failures remain unassessed; paired effects state the number of
jointly assessed targets. USD denotes metered API charges; local CPU/GPU time
is measured separately.

\paragraph{Comparison regimes.}
The primary comparison freezes each method's memory before target evaluation.
All seven methods use the same admitted historical sources and backbone;
their native memory construction may differ, with construction cost reported.
ExpeL, ExpeRepair, ReasoningBank, and ACE are adapted to the common agent and
their code revisions, prompts, and changed interfaces are recorded. A common
solver does not make an adapted implementation identical to the original full
system. No target gold patch or withheld evaluation check enters memory.
The same backbone is used for new extraction, selection, composition, and
repair roles so that a stronger auxiliary model cannot explain the effect.

\expcriterion{E14 (P2, required for an online-adaptation claim): compare updating and frozen arms within each method under matched orders and permitted feedback. Illustrative gains are +3--8 pp resolution or +4--12 pp Combined. Use at least three fixed orders and report order dependence.}
A secondary sequential-update setting permits methods to update only after
the current prediction is submitted, using the same permitted feedback and
task order, with separate memory stores per arm. It starts from the frozen
banks and is reported separately; it does not overwrite the primary frozen
results. This distinguishes ACE-style offline and online adaptation rather
than disabling updating without describing the resulting baseline.

The primary result panel is now in the main text,
Table~\ref{tab:planned-fourbench}. It fixes the same public preparation prefix,
gate, candidates, and total budget for Flat and CG-Fixed-v1. Complete records,
per-task predictions, verifier receipts, and costs accompany every result.



\begin{table}[!htbp]
\centering
\caption{\textbf{Order the work around the scientific argument.}
The experiment sequence uses development tasks to determine useful content and
fix the method before the four-manifest comparison. Each later stage answers
a distinct question; numerical gains are measured rather than assumed.}
\label{tab:planned-sequence}
\small
\begin{tabular}{lp{0.40\linewidth}p{0.40\linewidth}}
\toprule
Stage & Question & Experiment and evidence \\
\midrule
1 & What should memory communicate? & Content and source-utility interventions
in Tables~\ref{tab:planned-content}--\ref{tab:planned-utility}. \\
2 & What must the graph preserve? & Relation and composition ablations in
Table~\ref{tab:planned-graph}. \\
3 & Can retrieval find useful conditions? & Ranking and source coverage in
Tables~\ref{tab:planned-retrieval}--\ref{tab:planned-pool}. \\
4 & Is the method ready for independent evaluation? & Implement the gate and
validators; freeze the contract in Appendix~\ref{sec:method-contract}; audit
exposure and seal independently authored behavioral checks. \\
5 & Does the fixed method help in practice? & Resolution (E07), held-out
completeness (E15), applicability and harmful transfer (E16), then matched
retry efficiency and amortized cost (E08/E09). \\
\bottomrule
\end{tabular}
\end{table}

\section{Experiment 2 plan: content and mechanism ablations}
\label{sec:planned-content}
Use 24 distinct development targets from the existing dev70 partition, spanning
at least four repositories and four operation families. Select task/source
pairs from public issues and source evidence before observing the new repairs.
Use three fresh repetitions per arm, with common target and source IDs, and
counterbalance arm order within targets. The proposed allocation is 72 attempts
per arm. Fix a common target-level evaluation suite before candidate outcomes:
each target has applicable joint checks and neighboring behaviors that pass
on its original base. These tests define the outcomes across content, source,
graph, and retrieval interventions. A regression is an attempt failing at
least one of these originally passing preservation checks.
Prepare $P_q$ with the frozen common prefix before splitting arms. A supplied
researcher reproduction defines a separate conditional-on-$P_q$ setting and
cannot be pooled with the automatic entry-point evaluation. Keep preparation
and delivery failures in the assigned 24-target panel. Mechanism conclusions
are restricted to this development population.

\paragraph{Shared method-level panel.}
Before internal ablations, evaluate all seven methods on this same 24-target
suite with three fresh repetitions, reporting Official, Joint, Preserve, and
Combined. Fix the behavioral checks before seeing any of these submissions.
This panel tests whether full systems differ on the missing requirements;
the following interventions identify which content or operation causes a change.

\begin{table}[!htbp]
\centering
\caption{Planned method-level behavioral comparison. Repeat this complete
panel on the second authorized backbone with the same tasks and protocol.
Each entry reports the mean task success rate and sample standard deviation
across three repetitions; paired confidence intervals resample targets.}
\label{tab:planned-method-behavior}
\small
\begin{tabular}{lcccc}
\toprule
Method & Official & Joint & Preserve & Combined \\
\midrule
No memory & \pending & \pending & \pending & \pending \\
FAISS Flat & \pending & \pending & \pending & \pending \\
ExpeL & \pending & \pending & \pending & \pending \\
ExpeRepair & \pending & \pending & \pending & \pending \\
ReasoningBank & \pending & \pending & \pending & \pending \\
ACE & \pending & \pending & \pending & \pending \\
ContextGraph & \pending & \pending & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E12 (P0): +8--17 pp Combined over Flat corresponds to about two to four additional targets per 24-task repetition. Preserve of 95--100\% is only a descriptive goal. Claims of no material Official/Preserve degradation need a prespecified margin (e.g., -5 pp) and interval evidence.}
\end{table}

\begin{table}[!htbp]
\centering
\caption{\textbf{Which representation transfers the missing requirement?}
Each target uses the same single historical source and the same solve budget.
The rows vary only the delivered content: requirement $r$, historical patch
$H$, witness $W=(I,A,O)$, and source executions $E^{-},E^{+}$.
All rows receive the same execution tool and current-task instructions.
Official is benchmark resolution; Joint requires all predeclared combined
current/historical checks; Preserve requires the neighboring input checks;
Combined requires all three on the same repair in this fixed suite. Additional joint
and neighboring evaluation inputs and observers are fixed before these runs
and withheld from the solver; delivered source witnesses remain visible.
Report mean task success across repetitions and paired intervals. The
$r+W$ versus $r+H$ contrast compares executable examples with a patch reference;
the last two rows isolate supplying the source execution observations.}
\label{tab:planned-content}
\small
\begin{tabular}{lcccc}
\toprule
Delivered memory & Official $\uparrow$ & Joint $\uparrow$ & Preserve $\uparrow$ & Combined $\uparrow$ \\
\midrule
None & \pending & \pending & \pending & \pending \\
Requirement $r$ & \pending & \pending & \pending & \pending \\
Historical implementation $H$ & \pending & \pending & \pending & \pending \\
$r+H$ & \pending & \pending & \pending & \pending \\
$r+W$ & \pending & \pending & \pending & \pending \\
$r+W+E^{-}+E^{+}$ & \pending & \pending & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E02 (P0): illustrative practical effects are +8--17 pp Combined for $r+W$ versus $r+H$, and +4--12 pp for adding $E^{-},E^{+}$. Test each paired contrast separately; use the preservation/Official guardrails in the decision guide.}
\end{table}

\begin{table}[!htbp]
\centering
\caption{\textbf{What makes one source experience useful?}
On a 12-target subset chosen before candidate outcomes, form a pool of four
distinct sources per target using dense, lexical, operation-connected, and
same-repository random selection, filling duplicates from the same policy.
Deliver each source individually in the complete-witness format for three
repetitions: 144 source-conditioned attempts, plus the matched no-memory
controls from Table~\ref{tab:planned-content}, evaluated with the same fixed suite.
First separate sources without an established operation connection. Classify
connected sources by compatibility with the current requirement, then by whether
the behavior holds on the original workflow. Report source-pair
counts, change in Combined success, and new failures of the originally passing
preservation checks. These per-source effects supply development
utility labels for Table~\ref{tab:planned-retrieval}.}
\label{tab:planned-utility}
\small
\begin{tabular}{p{0.44\linewidth}ccc}
\toprule
Source/current relation & Source pairs & $\Delta$ Combined & $\Delta$ regressions \\
\midrule
Adds an omitted requirement & \pending & \pending & \pending \\
Preserves already-satisfied behavior & \pending & \pending & \pending \\
Conflicts with the current requirement & \pending & \pending & \pending \\
No established operation connection & \pending & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E04 (P1): an omitted-requirement group gain of +8--17 pp is a practical example; within $\pm5$ pp illustrates a near-zero effect for other groups. These are not required category rankings. Report group counts and uncertainty; conflicting history need not always harm a competent agent.}
\end{table}

\subsection{Graph relations and retrieval}
\label{sec:planned-graph}

\paragraph{E03: relations, composer, observations, and joint conditions.}
The result panel is in main Table~\ref{tab:planned-graph}.
Use the same 24 development targets, three repetitions, fixed source IDs and
complete records, contract-admission decisions, check count, shared validator,
and total construction-plus-solver budget. B--F share the identical composer
and adapter registry. B reconstructs all bindings from text into the same typed
schema supplied to C. D/E reconstruct only one withheld binding family.
The common gate exposes decisions and contract anchors, not withheld bindings
or mapping traces; tool and validation messages must respect the same mask.
G receives C's bindings but replaces its composer by bounded free-form program
generation; validation and check counts stay fixed. Among A--G, F alone adds the same
checks' observed failures before editing, including their execution cost.
Ordinary agent tools remain available in every arm, so F--C tests supplied
observations, not removal of all possible execution feedback. Construction
failures remain in the denominator.

\paragraph{H/I: separate versus joint checks.}
Use the same historical record, accepted requirement, bindings, current program
$P_q$, environment, starting solver state, and remaining total budget.
Both arms receive the same current and historical requirement text and source
evidence. H executes $P_q$ plus a standalone historical check on the current
version; I executes the same $P_q$ plus the joint check combining the historical
trigger with the current operation. Thus each arm has two check slots; I replaces
the second slot rather than adding tests. Independently justify the historical
check's current applicability and environment adaptation in both arms.

Match execution caps, feedback rounds, observation format/token limit, and
the repair/rerun schedule; meter actual generation and execution costs. Give
neither arm extra evaluator checks, and keep ordinary agent tools available
to both. Different observed failures are the consequence of the intervention,
not a reason to supply extra rounds. I is a dedicated matched arm, not silently
pooled with F. Failure to prepare or deliver a check remains in the assigned
denominator; do not select only targets with two passing separate checks.

The sealed evaluator tests separate and joint behavior on every submitted
repair. Report I--H in Combined and the paired rate of ``separate checks pass,
joint check fails,'' with the same assigned-target denominator and assessment
coverage. The latter is a diagnostic joint event, not a population selected
after observing which patches pass separate checks. A diagnostic on the common
pre-edit state is descriptive, not a replacement for the repair comparison.
An I--H benefit supports this condition-composition policy on these development
tasks; it is not a factorial interaction estimate for every possible condition.

\expcriterion{E03 (P0): I--H is the primary joint-condition contrast; +4--12 pp
Combined is an illustrative practical effect, not a predicted result. C--B
tests supplied relations with the same composer (+8--17 pp example), C--G
tests composer choice, and F--C tests supplied observations. Report each
contrast and its paired uncertainty separately; E03 does not attribute the
formal benchmarks' system gains.}


\begin{table}[!htbp]
\centering
\caption{\textbf{Can a retriever find behaviorally useful memory?}
Panel A ranks the four-source pools from Table~\ref{tab:planned-utility};
panel B ranks the entire frozen source bank on all 24 development targets.
For B, measure standalone source utility on the union of all policies' top-three
sources, using the same intervention as Table~\ref{tab:planned-utility}.
Freeze rankings and the evaluation suite before obtaining these utility labels.
Hold the payload format and maximum $k=3$ fixed. Utility@3 is the sum of
standalone $\Delta$ Combined over delivered sources divided by three; empty
slots contribute zero, the no-memory utility. Report uncertainty across targets.
These ranking policies are development variants; the default in
Table~\ref{tab:planned-fourbench} remains the declared FAISS top-three policy.
Changing it requires a new release and independent evaluation. As an end-to-end development check,
run each top-three packet with three repetitions and the
same composer; the Combined column measures the packet's actual combined
effect. Composable@3 is the fraction of targets with at least one retrieved
condition that retains the current and historical triggers and executes with
its observer. A target with no delivered condition remains in this denominator.
The operation-reranking row is a proposed policy; the current implementation
retains FAISS order and supplies operation links without a hard veto.}
\label{tab:planned-retrieval}
\small
\begin{tabular}{p{0.40\linewidth}cccc}
\toprule
Candidate ranking & Utility@3 & Composable@3 & Combined & Retrieval ms \\
\midrule
\multicolumn{5}{l}{A. Controlled four-source pools; 12 development targets} \\
\midrule
FAISS dense similarity & \pending & \pending & \pending & \pending \\
BM25 & \pending & \pending & \pending & \pending \\
Dense + BM25 reciprocal-rank fusion & \pending & \pending & \pending & \pending \\
Dense + soft operation reranking & \pending & \pending & \pending & \pending \\
Dense with a required operation match & \pending & \pending & \pending & \pending \\
\midrule
\multicolumn{5}{l}{B. Full source bank; 24 development targets} \\
\midrule
FAISS dense similarity & \pending & \pending & \pending & \pending \\
BM25 & \pending & \pending & \pending & \pending \\
Dense + BM25 reciprocal-rank fusion & \pending & \pending & \pending & \pending \\
Dense + soft operation reranking & \pending & \pending & \pending & \pending \\
Dense with a required operation match & \pending & \pending & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E05 (P1): example improvements over FAISS are Utility@3 +0.05--0.15 (fraction units), Composable@3 +10--20 pp, and Combined +4--12 pp. A retrieval gain without a repair gain supports retrieval quality only; include selection cost.}
\end{table}

\section{Experiment 3 plan: generalization, robustness, and cost}
\label{sec:planned-coverage}

\expcriterion{E11 (P1): repeat all seven E12 arms on a second frozen backbone; +8--17 pp Combined over Flat is an illustrative useful effect. Evaluate each model separately. Development replication does not establish cross-model held-out benchmark performance.}
\expcriterion{E13 (P1): vary $k=1,3,5$ and $B=B_0/2,B_0,2B_0$ one at a time for CG and Flat, holding total budget fixed. A loss no larger than 5 pp relative to default is a practical margin, assessed by intervals; monotonic gains are not required.}
Repeat the seven-method panel within each backbone; report per-model effects
rather than averaging away a failure to transfer. The second model and its
budget are frozen before execution. For sensitivity, vary retrieved source
count over $k\in\{1,3,5\}$ and selected-record token allowance over
$B\in\{B_0/2,B_0,2B_0\}$ one at a time on the development suite, with $B_0$
chosen before outcomes. Keep the total selection-plus-solve budget fixed and
report actual delivered sources, tokens, valid joint delivery, Combined, and USD.
Record complete-record rejection explicitly when a record exceeds the allowance;
never silently truncate a witness. These sensitivity settings do not tune the
held-out tasks. Distractor and source-removal tests below hold the other factors fixed.

\begin{table}[!htbp]
\centering
\caption{\textbf{Does memory reach useful solutions with less computation?}
Extend the same frozen comparison to three real passes, retrying each arm's
own validly unresolved tasks. Produce this panel separately for each benchmark.
Freeze memory across passes and retain each arm's own prior-attempt feedback
under the same policy. Report cumulative resolved/planned, all-attempt tokens
and USD per resolved task after three passes, and active seconds to resolve 10\% of the
fixed manifest. Active time includes model, tool, and verification execution;
worker allocation and task order are matched. A threshold never reached is
reported as such. The 10\% threshold is rounded up to a whole task. Count
target-time composition, failed attempts, and verification in active time;
zero resolutions give undefined cost per solve. Add the one-time build cost
from Table~\ref{tab:planned-amortization} to the three-pass API total. This tests the early-resolution
pattern in Table~\ref{tab:swectx-stream} using measured time and cost.}
\label{tab:planned-efficiency}
\small
\begin{tabular}{lcccccc}
\toprule
Method & Pass@1 & Pass@2 & Pass@3 & Tokens/solve & USD/solve & Time to 10\% \\
\midrule
No memory & \pending & \pending & \pending & \pending & \pending & \pending \\
FAISS Flat & \pending & \pending & \pending & \pending & \pending & \pending \\
ExpeL & \pending & \pending & \pending & \pending & \pending & \pending \\
ExpeRepair & \pending & \pending & \pending & \pending & \pending & \pending \\
ReasoningBank & \pending & \pending & \pending & \pending & \pending & \pending \\
ACE & \pending & \pending & \pending & \pending & \pending & \pending \\
ContextGraph & \pending & \pending & \pending & \pending & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E08 (P1): ratios CG/control of 0.70--0.90 for matched-resolution time and 0.75--0.90 for tokens or USD per solve illustrate useful savings. Require compatible quality and a ratio interval below 1. An unreached time threshold is censored, not a finite speedup.}
\end{table}

\begin{table}[!htbp]
\centering
\caption{\textbf{Can the bank supply usable experience across the four benchmarks?}
The source273 column is an existing measured same-repository witness-coverage
count, meaning at least one witnessed source from the repository. Expand the
bank from official training data and pre-base commits, and develop the operation
adapters needed beyond Django before the method freeze. New witnesses count
source false-to-true contrasts. Expanded coverage and valid joint delivery use
all planned targets as their denominator; the latter also requires both triggers
and a working observer. An accepted but unsupported composition falls back to a cited requirement
as text, not an unvalidated current assertion; rejected or uncertain
requirements are not enforced. Each fallback reason is counted separately. Freeze this delivery policy with the common
bank before the four-benchmark comparison.}
\label{tab:planned-coverage}
\small
\begin{tabular}{lcccc}
\toprule
Benchmark & Source273 coverage & New witnesses & Expanded coverage & Joint delivery \\
\midrule
Verified150 & \knownresult{133/150} & \pending & \pending & \pending \\
Related-Lite99 & \knownresult{91/99} & \pending & \pending & \pending \\
LoLBench100 & \knownresult{2/100} & \pending & \pending & \pending \\
DeepSWE113 & \knownresult{0/113} & \pending & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E01 (P0): operational planning bands are 80--95\% witnessed repository coverage and 50--80\% valid joint delivery, not expected repair scores. Coverage alone cannot support effectiveness; retain failures, fallbacks, and human interventions in the denominators.}
\end{table}

\begin{table}[!htbp]
\centering
\caption{\textbf{Does scale help through useful-source coverage or ranking?}
Use the 12-target source-utility study with a fixed delivered $k=3$.
First add 0, 4, or 16 same-repository distractors per target while retaining
its original four-source pool; measure selection stability and Combined
success for FAISS and the chosen graph policy. Then replace the source with
the highest measured standalone utility with an additional distractor,
keeping the pool size fixed. Freeze these manipulations before new packet
outcomes and run three repetitions per cell. Distractors have complete witnesses
for other operations, selected from public source bindings. This development
experiment uses earlier standalone utility labels and fresh packet trials.
Retention is reported separately for Flat and Graph (F/G); choosing a source
by measured utility does not imply its effect is positive.}
\label{tab:planned-pool}
\small
\begin{tabular}{lcccc}
\toprule
Pool condition & Size & Retained F/G & Flat Combined & Graph Combined \\
\midrule
Original candidate pool & 4 & \pending/\pending & \pending & \pending \\
Add 4 distractors & 8 & \pending/\pending & \pending & \pending \\
Add 16 distractors & 20 & \pending/\pending & \pending & \pending \\
Replace best source, fixed size & 20 & n/a & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E06 (P1): a loss no larger than 5 pp under distractors is a practical robustness margin; compare the drop against Flat. A 4--12 pp loss after source removal illustrates dependence. Compare removal to the 20-source distractor arm, not the original four-source pool.}
\end{table}

\begin{table}[!htbp]
\centering
\caption{\textbf{When does executable memory repay its construction cost?}
Measure actual source construction, before/after execution, embedding, and
indexing charges separately from solve-time retrieval and condition execution.
For each benchmark and method, use only first-pass trajectories to report
$[C_{\mathrm{build}}+C_{\mathrm{solve}}(N)]/R(N)$ at the listed cumulative task
counts in the fixed task order. $R(N)$ counts first-pass official resolutions;
solve cost includes target-time construction and failed attempts. Prefixes beyond the manifest,
or with $R(N)=0$, are n/a. For each memory method, report the first observed
prefix with at least the control's resolutions and lower total cost per
resolution, or ``not reached.'' This is the first observed cost crossover,
not a prediction that the advantage persists at every larger prefix.
Use measured costs at these prefixes rather than projecting a success rate.}
\label{tab:planned-amortization}
\small
\begin{tabular}{lccccc}
\toprule
Method & Build USD & USD/solve at 25 & At 50 & At 100 & First crossover \\
\midrule
No memory & n/a & \pending & \pending & \pending & Reference \\
FAISS Flat & \pending & \pending & \pending & \pending & \pending \\
ExpeL & \pending & \pending & \pending & \pending & \pending \\
ExpeRepair & \pending & \pending & \pending & \pending & \pending \\
ReasoningBank & \pending & \pending & \pending & \pending & \pending \\
ACE & \pending & \pending & \pending & \pending & \pending \\
ContextGraph & \pending & \pending & \pending & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E09 (P1): an all-in cost/solve ratio of 0.75--0.90 at an observed valid prefix (50 or 100) illustrates practical amortization, with competitive resolution. Report the first observed crossover; do not project one. $N=100$ is unavailable for Related-Lite99.}
\end{table}

\clearpage
\section{Independent confirmation: completeness and applicability}
\label{sec:planned-independent}
The development panels select the method; the following tests establish its
scope. Their manifests, annotation rules, and endpoints are sealed before
new solver outcomes are visible. They do not reuse the 24 development tasks.

\subsection{E15: independently specified held-out behavioral completeness}
\label{sec:heldout-protocol}
After freezing CG-Fixed-v1, audit the four official manifests for any use in
method, prompt, adapter, or threshold development. Preserve exposure records;
a previously inspected failure cannot become untouched by renaming a split.
Use a prespecified seed and public repository/operation strata to sample up to
40 unexposed targets per benchmark, 160 in the proposed allocation. If a
manifest has fewer eligible untouched tasks, report the actual available
sample and narrow the claim; do not quietly substitute tasks or call exposed
ones held out. This allocation is not a power guarantee.

Two independent annotators, blind to arm identity and new candidate patches,
specify requirements from current public contracts, the issue, pre-base history,
and version-matched documentation/tests. Historical evidence helps identify an
obligation, but a current-contract justification is required. The team does
not use CG's generated checks, retrieval success, or graph contents to select
targets or define expected outcomes. A third reviewer resolves disagreements;
unresolved obligations remain unassessed. Record requirement anchors, intended
outcomes, applicability, provenance, and disagreements before repair inspection.
The method developers and solver receive neither the private suite nor its labels.

Separate the reported-issue behavior, still-valid historical obligations,
combined triggers, and originally passing neighbors. Exercise nonempty outputs
or other meaningful observations where relevant; absence of an exception alone
is not a correctness oracle. Each arm is graded against the same sealed suite.
A target without any assessable additional historical obligation is recorded as
ineligible for this specific behavioral endpoint, not scored as a vacuous pass
and not replaced because CG retrieves nothing. Report behavioral eligibility
out of all sampled tasks and its repository/operation distribution.

Reuse E07 first-pass patches only when the suite was sealed before any new
arm outputs were revealed and the release/protocol matches exactly. Otherwise
use a new declared evaluation batch. The behavioral endpoint is Combined on
the predeclared behaviorally eligible sample, with assessed/eligible and
eligible/sampled counts. Official successes failing an applicable held-out
requirement are reported per eligible task (omission burden), and per official
success as a descriptive conditional rate. The latter compares different
post-treatment subsets and is not the primary causal endpoint.

Report each benchmark and repository stratum separately. A benchmark-balanced
aggregate, if prespecified, has equal benchmark weights and target-clustered
paired intervals within strata; it does not establish improvement on every
benchmark. E15 is a sample of assessable untouched tasks, not a claim about all
software operations. Joint, Preserve, missingness, and Official must accompany
Combined so that fewer official successes cannot masquerade as fewer omissions.

\begin{table}[!htbp]
\centering
\caption{\textbf{E15: do repairs satisfy independent held-out requirements?}
Detailed companion to main Table~\ref{tab:planned-heldout}. Repeat this panel
for each benchmark, using up to 40 sampled untouched targets.
State sampled, behaviorally eligible, assessed, and jointly assessed counts.
Cells report count/eligible and rate; omission is Official-pass with a failed
applicable behavioral requirement, divided by eligible tasks. Report the
Graph--Flat paired difference and interval for Combined.}
\label{tab:planned-heldout-detail}
\small
\begin{tabular}{lccccc}
\toprule
Method & Official & Joint & Preserve & Combined & Omission \\
\midrule
No memory & \pending & \pending & \pending & \pending & \pending \\
FAISS Flat & \pending & \pending & \pending & \pending & \pending \\
ExpeL & \pending & \pending & \pending & \pending & \pending \\
ExpeRepair & \pending & \pending & \pending & \pending & \pending \\
ReasoningBank & \pending & \pending & \pending & \pending & \pending \\
ACE & \pending & \pending & \pending & \pending & \pending \\
CG-Fixed-v1 & \pending & \pending & \pending & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E15 (P0): +5--10 pp Combined over Flat is an illustrative useful magnitude, requiring independent checks, paired uncertainty, and compatible Official performance. A 2--5 pp reduction in omission burden is a secondary example, not a substitute for Combined. Wide intervals or a gain limited to some strata require narrower claims; this proposed sample is not a power analysis.}
\end{table}

\subsection{E16: current-contract admission and harmful transfer}
\label{sec:applicability-audit}
Evaluate the frozen gate against the independently adjudicated requirements
encountered by the fixed retrieval policy on E15, including accepted, rejected,
and uncertain candidates. No item may be sampled because of its gate decision
or repair outcome. Annotators use the same current-validity rules, remain blind
to gate output, and do not expose their labels to the runtime assessor.

A separate prespecified challenge set proposes 60 applicable, 60 contradicted,
and 30 genuinely ambiguous requirement/target pairs. Include changed API
contracts, incompatible types/roles, superseded behavior, and insufficient
specification. These deliberately balanced strata test failure modes; they do
not estimate their natural deployment prevalence. Preserve target/source
clusters when estimating uncertainty. Record every target decision, cited
anchor, source version, reason, additional model/tool cost, and abstention.

False acceptance is accepted/known-contradicted; useful acceptance is
accepted/known-applicable; uncertain enforcement is accepted/gold-uncertain.
Report the denominators, not only percentages, and wrong requirements among
all accepted obligations as a separate precision view. The challenge set's
class balance must not be used to infer precision in the natural retrieval stream.
Also compare default gating with a declared gate-bypass variant on the same
eligible E15 targets, holding candidate source IDs, source records, composer,
check-construction rules, and total budget fixed. Delivered assertions may
differ because the bypass arm omits applicability rejection; it is not a new
default. Withheld evaluation obligations, not enforced historical assertions,
determine regressions and Combined.

\begin{table}[!htbp]
\centering
\caption{\textbf{E16: can the gate reject stale obligations without losing useful memory?}
Panel A audits the automatic gate on both candidate populations. Panel B uses
the held-out behavioral suite for submitted repairs; record applicability
cost and memory delivery for both arms. The current-contract labels are made
independently of generated programs and repair outcomes.}
\label{tab:planned-applicability}
\small
\begin{tabular}{lcccc}
\toprule
Candidate population & Pairs & False accept & Useful accept & Uncertain enforced \\
\midrule
Natural retrieved pairs & \pending & \pending & \pending & \pending \\
Separate challenge strata & \pending & \pending & \pending & \pending \\
\midrule
Repair policy & Official & Preserve & Combined & Omission \\
\midrule
CG-Fixed-v1 gate & \pending & \pending & \pending & \pending \\
Gate bypass (ablation only) & \pending & \pending & \pending & \pending \\
\bottomrule
\end{tabular}
\expcriterion{E16 (P0): a proposed false-acceptance tolerance is 5\%, judged with an upper interval bound and useful-acceptance coverage, not a point estimate alone. Zero errors need at least 59 independent contradicted pairs for a one-sided exact 95\% upper bound below 5\%; correlated pairs do not satisfy this calculation. Report natural and challenge strata separately. Claim reduced harmful transfer only if held-out behavioral outcomes support it.}
\end{table}
\endgroup

```
