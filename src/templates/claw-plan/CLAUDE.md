# Claw Phase 3: Plan

You are in a Claw planning session for `{{slug}}`.

## Signal Protocol

- Before ANY question that requires human input, output `[QUERY]` on its own line, then the question.
- When this phase is complete, output `[PHASE-DONE: 3]` on its own line.

## Instructions

1. Read `prd.md` in this directory.
2. Run the `plan-from-prd` skill to produce:
   - `plan.md` (phased implementation plan with acceptance criteria per phase)
   - `todo.md` (flat task list in order)
3. If the skill asks a question, precede it with `[QUERY]`.

## Before Completing

1. Run the `progress` skill to append: `Plan written (N phases)` where N is the number of phases produced.
2. Then output `[PHASE-DONE: 3]`.

## Rules

- Every question to the user MUST be preceded by `[QUERY]` on its own line.
- Do not modify `prd.md`. Read only.
- Do not start building. Only produce the plan and todo.
