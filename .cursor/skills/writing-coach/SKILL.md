---
name: writing-coach
description: Updates writing memory based on user feedback given during cover letter drafting. Use when the user has reviewed active_application/final_draft.md and gives corrections, preferences, or opinions about the writing — either directly in chat or through referenced notes/files. NOT for analyzing reference draft batches (that belongs to voice-archivist). Writes directly to memory/writing_strategies.md.
---

# Writing Coach

Updates writing memory from user feedback on `active_application/final_draft.md`. Feedback can be provided directly in chat or via `@file` notes. Different from `voice-archivist`, which analyzes reference draft batches.

## Memory model

| Memory | File | Purpose |
|---|---|---|
| **Style baseline** | `memory/style_guidelines.md` | Extracted from reference drafts (via **Voice Archivist**) |
| **Writing rules** | `memory/writing_strategies.md` | Confirmed, reusable rules to apply in future letters |

## Workflow

1. Read `@active_application/final_draft.md` first. Always ground decisions in the current draft text.
2. Read the user's feedback (chat feedback and/or any referenced note files).
3. Read `@memory/writing_strategies.md`.
4. Classify each piece of feedback:

**Write to writing rules** when the user is explicit and deliberate:
- *"never use 'passionate about'"*, *"always end with a call to action"*, *"keep it under 3 paragraphs"*

**Ignore / do not save** when the feedback is clearly job-specific:
- *"mention the Paris office"*, *"reference their 2024 product"*

5. Append to `memory/writing_strategies.md` under the most relevant section. Never overwrite existing rules.
6. Summarise what was saved and where.
