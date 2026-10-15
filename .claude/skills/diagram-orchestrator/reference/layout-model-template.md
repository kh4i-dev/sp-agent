# Layout Model Manifest — Template

> Create one copy per non-trivial diagram at `docs/domain/<diagram-name>-model.md`.
> This is a planning artifact, not a replacement for the editable diagram source.
> Keep the source-of-truth distinction explicit: observed facts, derived relationships, assumptions, and unknowns.

## 1. Purpose and acceptance context

- Diagram ID/name:
- Diagram type:
- Purpose / question the diagram should answer:
- Audience:
- Output target: A4 portrait / A4 landscape / slide / screen
- Source-of-truth files:
- As-Is or To-Be:
- Required notation / standard:
- Status: DRAFT / REVIEW / APPROVED

## 2. Nodes

| Stable ID | Display name | Node kind | Domain/zone | Source evidence | Confidence |
|---|---|---|---|---|---|
| N-01 | | | | file + symbol/line | Observed / Derived / Assumption / Unknown |

Rules:
- Every node must have a reason to exist in this diagram.
- Do not invent a node just to make the layout symmetrical.
- Record excluded neighboring concepts if their absence could be mistaken for an omission.

## 3. Edges / transitions

| Edge ID | From | To | Semantic type | Direction | Label / multiplicity / guard | Evidence | Mandatory adjacency? |
|---|---|---|---|---|---|---|---|
| E-01 | N-01 | N-02 | FK / association / call / include / transition | | | file + symbol/line | Yes / No |

Rules by diagram type:
- ERD: reconcile each in-scope database FK with exactly one represented relationship; document excluded schemas/views explicitly.
- Class: list each in-scope association/generalization/aggregation/composition and role/multiplicity.
- Use Case: list each actor-use-case association and each include/extend with a semantic justification.
- Sequence: derive messages and branches from implementation or an explicitly marked scenario specification.
- Activity: list decisions, guards, merge/fork/join semantics, and exception paths.
- State: list each state and transition with trigger/guard/effect evidence.
- Architecture/deployment: distinguish actual runtime links from proposed target-state links.

## 4. Semantic invariants (must not be sacrificed for aesthetics)

- [ ] All nodes/edges have evidence or are explicitly marked as assumptions.
- [ ] No relation was removed merely to reduce crossings.
- [ ] Cardinalities, directions, guards, role names, and state transitions are correct.
- [ ] As-Is and To-Be elements are not silently mixed.
- [ ] Scope and exclusions are stated.
- [ ] Unknowns are listed rather than guessed.

## 5. Layout plan

- Primary reading direction:
- Zones/lanes/packages:
- Hub nodes and why:
- Must-be-near node pairs:
- Inheritance/state hierarchy constraints:
- Long/parallel/cyclic edges likely to cause problems:
- Labels that need concise wording without losing meaning:
- Candidate A:
- Candidate B:
- Why the selected candidate is best supported:
- Why manual layout or decomposition may be required:

## 6. Render and review evidence

| Attempt | Source revision/hash | Renderer + version | Single change/hypothesis | Result | Decision |
|---|---|---|---|---|---|
| Baseline | | | Initial render | | Keep / Reject |
| A | | | | | Keep / Reject |
| B | | | | | Keep / Reject |

### Visual proof-of-view

- Exact rendered PNG path:
- File hash:
- Render timestamp:
- Three labels transcribed from the PNG itself:
  1.
  2.
  3.
- Node/zone placement observed:
- Crossings / overlaps / clipping:
- Longest or anomalous edge:
- Text readability at target print size:
- Visual balance:
- Final status: PASS / PASS WITH CONDITIONS / FAIL / BLOCKED

## 7. Remaining uncertainty

- Verified:
- Derived:
- Heuristic:
- Unknown:
- Accepted limitations and who accepted them:
