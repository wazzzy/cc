# Claw Phase 4: Build

You are in a Claw build session. The slug is the name of the current working directory.

## Signal Protocol

- Before ANY question that requires human input, output `[QUERY]` on its own line, then the question.
- When a phase of the plan completes, output `[PHASE-DONE: N]` on its own line (where N is the plan phase number).

## Plan

Determine the slug from the current directory name, then read the implementation plan and task list:
- `~/Claw/Plans/<slug>/plan.md`
- `~/Claw/Plans/<slug>/todo.md`

## Review Fixes (if applicable)

Check if any review files exist at `docs/review-*.md` in this directory. If one exists, read it and fix the issues it describes before continuing with plan work.

## Git Rules

- Work on branch `dev/<slug>`. Create it from main if it doesn't exist.
- Commit freely to `dev/<slug>` as you work. Frequent, small commits.
- **Never commit to main.**
- **Never push to remote** unless the user explicitly asks.

## Instructions

1. Check out `dev/<slug>` (create from main if needed).
2. If a review file exists (see above), address the findings first.
3. Work through the plan phases in order (or the specific phase requested).
4. For each plan phase:
   a. Implement the work described
   b. Run tests if applicable
   c. Commit progress to `dev/<slug>`
   d. Run the `progress` skill to append: `Phase N done`
   e. Output `[PHASE-DONE: N]`
5. Wait for the user before starting the next phase.

## Rules

- Every question to the user MUST be preceded by `[QUERY]` on its own line.
- Do not modify files in `~/Claw/Ideas/` or `~/Claw/Plans/`. Those directories are read-only during build.
- Do not merge to main. Do not push to remote.
- Write `progress.md` BEFORE signaling `[PHASE-DONE]`.
