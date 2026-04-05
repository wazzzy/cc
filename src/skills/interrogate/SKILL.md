---
name: interrogate
scope: user
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user says "interrogate me", "stress-test my plan", or "challenge my design". Do NOT trigger for PRD writing or general Q&A.
---

# Socratic Interrogation

Interview the user relentlessly about every aspect of this plan or idea until you both reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

## Process

1. Read any context files present in the working directory (spark.md, brainstorm.md, or whatever the user points you to).
2. If a question can be answered by exploring the codebase, explore the codebase instead of asking.
3. Ask **one question at a time**. For each question, provide your recommended answer.
4. After each answer, append the exchange to `brainstorm.md` in the current working directory:

```
### <question summary>

**Q:** <your question>

**Recommended:** <your recommendation>

**A:** <user's answer>
```

5. Continue until you have enough clarity to move forward. When done, summarize the key decisions reached.

## Rules

- One question at a time. Never batch questions.
- Always provide your recommended answer. The user can accept, reject, or modify.
- Append every exchange to brainstorm.md with the format above. Create the file if it doesn't exist.
- If the user says "enough" or "done", stop immediately and summarize.
- Do not generate a PRD. Do not write implementation plans. Just ask, record, and build shared understanding.
