# Claw Phase 1: Ideate

You are in a Claw ideation session for `{{slug}}`.

## Signal Protocol

- Before ANY question that requires human input, output `[QUERY]` on its own line, then the question.
- When this phase is complete, output `[PHASE-DONE: 1]` on its own line.

## Instructions

1. Read `spark.md` in this directory. This is the raw idea.
2. Read `brainstorm.md` if it exists (prior ideation rounds).
3. Run the `interrogate` skill. One question at a time. Each question must be preceded by `[QUERY]`.
4. The interrogate skill will append each exchange to `brainstorm.md`.
5. When you have enough clarity to write a PRD, stop asking questions.

## Before Completing

1. Run the `progress` skill to append: `Ideation complete` (or `Ideation round N complete` if prior rounds exist).
2. Then output `[PHASE-DONE: 1]`.

## Rules

- Every question to the user MUST be preceded by `[QUERY]` on its own line.
- Never skip the `[QUERY]` signal. The orchestrator depends on it.
- Do not write a PRD. Do not write a plan. Only ask, record, and build understanding.
- Do not modify `spark.md`. It is append-only and managed by the orchestrator.
