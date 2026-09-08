# Source activation and applicability

One development target, Django12663, with source13590 and the same initial candidate.
Three fresh revisions compare the original source issue/patch, its generated
requirement, and that requirement plus the source program and actual initial
failures. All predictions received immediate official verification. The five
original behavior measurements comprise two source cases and three hidden joint
cases (scalar, ordinary tuple, named tuple with lazy User values).

After all three submissions, two additional ordinary-subclass inputs were authored
from inspection of the feedback patch and executed on all three repairs, the
initial candidate and the unmodified target. These ten executions are separate
from the original five-case protocol. The summary binds the actual patch and
execution receipt hashes; it makes no aggregate memory-form ranking.

Full original artifacts in ContextGraph:
- `results/verified_train_test_v1/codepath-memory-activation-v2/`
- `data/verified_train_test_v1/codepath-memory-activation-v2/final-assessment.json`
- `data/verified_train_test_v1/range-subclass-preservation-v1/`

The subsequent no-reference review also completed: it returned the exact initial
candidate, passed official verification, and failed both historical cases and
the named-tuple joint case. `no-reference-summary.json` preserves it separately.
The old runner rejected an empty reference tag; an exact-input audit confirmed
that its content was empty as prepared. Original outputs were unchanged and no
model or verifier was rerun.
