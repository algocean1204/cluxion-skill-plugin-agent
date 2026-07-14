---
name: clx-modular-architecture-design
description: >
  Analysis-driven hierarchical module architecture design. Pre-development tech-stack
  selection, evidence-gated module decomposition (splitting and commonization only pass
  through analysis gates), field-level IN/OUT specs, straight-line main pipeline, and a
  single DESIGN.md deliverable. Trigger: designing the structure of a NEW system/project,
  or a large-scale refactor design, or explicit requests for 설계도/아키텍처/모듈 설계/
  파이프라인 설계/architecture/system design. Do NOT use for simple structure questions
  or small edits.
---

# Analysis-Driven Module Architecture Design

> **"Modularization is the RESULT of analysis, not the default. Every split/commonization decision carries a one-line justification."**

Kept as this skill's identity: OUT=1, straight-line pipeline, field-level specs.
Changed: decomposition happens **only through gates**, and the deliverable is a **single DESIGN.md** (no HTML).

## Workflow

### Phase 0: Mode selection

- **Greenfield**: new system → Phases 1–4 as written.
- **Refactor**: existing code → inventory current modules first (`rg`/tree scan: real call
  sites, sizes, change hot-spots from git log), THEN run Phases 2–4 on the target design,
  and add a **migration order** to DESIGN.md (strangler pattern: which module moves first,
  what stays temporarily duplicated, cutover checks). Gates apply identically — refactors
  over-split even more easily than greenfield.

### Phase 1: Tech-stack agreement — the ONLY approval gate

Establish purpose, deployment target, performance needs, stack preference (skip questions
the user already answered) → propose as a table → **one user approval**. Every later phase
proceeds without approval and reports results. Under goal/loop, replace even this gate with
"propose + state the chosen default + proceed".

### Phase 2: Scale Gate — decide decomposition depth first

| Scale | Rough size (files) | Allowed depth |
|-------|--------------------|---------------|
| Small | ~10 | Feature level (F1..FN) only. Start with NO C0 |
| Medium | ~40 | Feature + Level-2 modules. C0 only via admission review |
| Large | beyond | Full hierarchy + C0. Write feature-by-feature |

Decomposing past the allowed depth is forbidden unless the Phase-3 split gate provides evidence.

### Phase 3: Decomposition — apply the analysis gates

**Read `references/module-design-rules.md` first**, then in order:

1. Feature decomposition (F1..FN)
2. **Split gate** on every split candidate: 2+ reasons to change **AND** (2+ real reuse sites
   ∥ independent test value ∥ different change cadence/owner). Fails the gate → **keep it together**
3. **C0 admission review** on every commonization candidate (rule of three + interface stability
   + domain independence). Fails → keep it feature-local — **duplication at this stage is allowed**
4. **Merge signals** sweep: pass-through modules, always-called-together, effectively identical
   IN/OUT → merge them
5. Derive the straight-line main pipeline

### Phase 4: Detailed IN/OUT specs + DESIGN.md

For every module: IN (main/aux — type, source, description), exactly one OUT (field-level),
**failure semantics** (what the OUT looks like on failure — Result-style object or declared
exception; never an unspecified crash), internal logic, C0 usage, constraints, and a
**parallel mark** (`parallel-safe: yes/no` + resource note) whenever the user stated
quantified resources — the design must show how stated RAM/cores get saturated. Then generate a **single `DESIGN.md`** following
`references/ai-behavior-guide.md`: header → tech-stack table → folder tree → main pipeline
(optional mermaid) → C0 (if any) → feature cards → dependency table → implementation
checklist → **design decision log** (justification for every split/commonization/merge).

## Core rules (quick reference)

| Rule | Meaning |
|------|---------|
| **Justification duty** | Every split/commonization gets one written reason — no reason, keep together |
| **Split gate** | 2+ change reasons AND (2+ reuse ∥ test value ∥ different cadence) |
| **C0 admission** | 3rd real use site + stable interface + domain-independent — all three or stay local |
| **Module floor** | A single function is NOT a module — modules are cohesive responsibility units |
| **OUT = 1** | One OUT per module (a multi-field result object counts as one) |
| **Straight pipeline** | One branch-free line; conditionals live inside modules |
| **Spec = code level** | Types, sources, and fields written out in IN/OUT |
| **Deliverable** | Single `DESIGN.md` — HTML generation forbidden |

## Living design (drift prevention)

DESIGN.md is not a one-shot artifact. Any deviation during implementation — a module merged,
a boundary moved, a type changed — updates the decision log **in the same turn** as the code
change. A design that disagrees with the code is worse than no design.

## Mandatory verification before declaring the design done

- [ ] Decision log covers every split / commonization / merge with a reason?
- [ ] Every C0 module has 3+ real use sites?
- [ ] No module left matching a merge signal?
- [ ] OUT=1 everywhere, IN sources named, pipeline straight, zero circular deps?
- [ ] Every module's failure semantics specified (no unspecified crash paths)?
- [ ] Parallel marks + resource math present when the user stated quantities?
- [ ] Each module boundary has one contract-test stub in the implementation checklist?
- [ ] Module count within the Scale Gate bound? (exceeding requires logged evidence)
- [ ] Refactor mode: migration order + cutover checks included?
