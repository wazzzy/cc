# Claw Phase 5: Review

You are in a Claw review session. The slug is the name of the current working directory.

## Signal Protocol

- Before ANY question that requires human input, output `[QUERY]` on its own line, then the question.
- When the review is complete, output `[PHASE-DONE: 5]` on its own line.

## Instructions

1. Determine the slug from the current directory name.
2. Review the diff between `main` and `dev/<slug>`.
3. Read the plan for context: `~/Claw/Plans/<slug>/plan.md`
4. Evaluate: correctness, test coverage, edge cases, obvious issues, alignment with the plan.
5. Write the review to `docs/review-<YYYY-MM-DD>.md` in this directory. Create the `docs/` directory if needed.

## Review File Format

```markdown
# Code Review: <slug>

**Date:** YYYY-MM-DD
**Branch:** dev/<slug>
**Commits reviewed:** <count>

## Summary

1-3 sentence overview.

## Issues

### Issue N: <title>

**Severity:** critical | major | minor | nit
**Location:** <file:line>
**Description:** What's wrong and why.
**Suggestion:** How to fix it.

## Strengths

What was done well (brief).

## Verdict

PASS | PASS WITH NITS | NEEDS CHANGES
```

## Before Completing

1. Run the `progress` skill to append: `Review complete - <VERDICT>`.
2. Then output `[PHASE-DONE: 5]`.

## Rules

- **Read-only.** Do not edit any source files. Only produce the review file.
- Every question to the user MUST be preceded by `[QUERY]` on its own line.
- Be direct. No filler. Cite specific lines.
