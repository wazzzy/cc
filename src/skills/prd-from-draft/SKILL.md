---
name: prd-from-draft
scope: project
description: Generate a PRD from existing markdown draft files (spark.md, brainstorm.md, or any markdown input). Use when user says "write PRD from draft", "PRD from these files", or "generate PRD". Unlike write-prd, this skill does NOT interview the user or explore a codebase. It synthesizes existing written material into a structured PRD.
---

# PRD from Draft

Generate a Product Requirements Document from existing markdown files. This skill synthesizes written material (idea descriptions, brainstorm notes, design discussions) into a structured PRD without interviewing the user.

## Process

1. Read all input files provided (spark.md, brainstorm.md, or whatever files are referenced).
2. Identify: the problem being solved, the proposed solution, user stories, key decisions already made, and what's explicitly out of scope.
3. Write the PRD to `prd.md` in the current working directory.
4. If critical information is missing and can't be inferred, ask one focused question at a time. Do not invent requirements.

## PRD Template

```markdown
## Problem Statement

The problem being solved, from the user's perspective.

## Solution

The proposed solution, from the user's perspective.

## User Stories

Numbered list. Each story:

N. As a <actor>, I want <feature>, so that <benefit>

**Acceptance Criteria:**
- Criterion 1
- Criterion 2

## Implementation Decisions

Decisions already made during ideation. Include:
- Architecture and module boundaries
- Schema shapes and data models
- API contracts
- Third-party service choices
- Security and auth approach

Do NOT include file paths or code snippets.

## Testing Decisions

- What should be tested
- Testing approach
- Types of tests needed

## Out of Scope

Explicitly excluded items from the brainstorm/design discussions.

## Open Questions

Anything unresolved that needs answering before implementation.
```

## Rules

- Do not interview the user. Synthesize what's already written.
- Do not explore a codebase. This skill operates on written material only.
- If a decision was clearly made during brainstorming, include it. Don't re-open settled questions.
- If something is ambiguous, flag it in Open Questions rather than guessing.
- Keep user stories extensive. Cover every behavior described in the source material.
