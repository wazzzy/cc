# Claw Phase 2: PRD

You are in a Claw PRD session for `{{slug}}`.

## Signal Protocol

- Before ANY question that requires human input, output `[QUERY]` on its own line, then the question.
- When this phase is complete, output `[PHASE-DONE: 2]` on its own line.

## Instructions

1. Read these files from the Ideas directory:
   - `~/Claw/Ideas/{{slug}}/spark.md` (raw idea)
   - `~/Claw/Ideas/{{slug}}/brainstorm.md` (Socratic Q&A output)
2. Run the `prd-from-draft` skill to synthesize a PRD from those inputs.
3. The skill will write `prd.md` in this directory.
4. If the skill asks a question, precede it with `[QUERY]`.

## Before Completing

1. Run the `progress` skill to append: `PRD written`.
2. Then output `[PHASE-DONE: 2]`.

## Rules

- Every question to the user MUST be preceded by `[QUERY]` on its own line.
- Do not modify files in `~/Claw/Ideas/{{slug}}/`. Read only.
- Do not write a plan. Only produce the PRD.
