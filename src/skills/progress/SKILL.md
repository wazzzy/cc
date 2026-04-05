---
name: progress
scope: project
description: Append a timestamped milestone entry to progress.md. Use when a phase completes, a significant milestone is reached, or you need to log progress. Format is append-only with timestamps.
---

# Progress Logger

Append a milestone entry to `progress.md` in the current working directory. Create the file if it doesn't exist.

## Format

Each entry follows this exact format:

```
## YYYY-MM-DD HH:MM - <Title>

<Optional body: 1-3 lines of context>
```

## Rules

- **Append only.** Never overwrite, delete, or reorder existing entries.
- **Timestamp every entry.** Use the current date and time.
- **Keep titles short.** Under 60 characters. State what happened, not why.
- **Body is optional.** Only add if there's context the title can't capture.
- **One entry per milestone.** Don't batch multiple events into one entry.

## Usage

When asked to log progress, or when a phase of work completes, append the entry to `progress.md` and confirm what was logged.
