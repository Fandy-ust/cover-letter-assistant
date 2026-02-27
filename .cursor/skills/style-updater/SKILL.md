---
name: style-updater
description: Updates style memory based on user feedback given during cover letter drafting. Use when the user has reviewed workspace/final_draft.md and gives corrections, preferences, or opinions about the writing — NOT when analyzing reference documents. Distinct from style-extractor (which processes reference drafts in batch). Writes to knowledge/style_notes.md (soft memory) or knowledge/writing_strategies.md (hard memory) depending on confidence.
---

# Style Updater

Updates style memory from live user feedback on `workspace/final_draft.md`. Different from `style-extractor`, which analyzes reference documents.

## Memory model

| Memory | File | Purpose |
|---|---|---|
| **Soft** | `knowledge/style_notes.md` | Tentative — observed once, not yet confirmed |
| **Hard** | `knowledge/writing_strategies.md` | Permanent — confirmed, recurring preferences |

## Workflow

1. Read `@workspace/final_draft.md` and the user's feedback.
2. Read `@knowledge/style_notes.md` and `@knowledge/writing_strategies.md`.
3. Classify each piece of feedback:

**Write to hard memory** when the user is explicit and deliberate:
- *"never use 'passionate about'"*, *"always end with a call to action"*, *"keep it under 3 paragraphs"*

**Write to soft memory** when the preference is implied or seen for the first time:
- A correction that could be a habit or could be job-specific
- A tone shift that might reflect a general preference

**Ignore / do not save** when the feedback is clearly job-specific:
- *"mention the Paris office"*, *"reference their 2024 product"*

4. Append to the correct file under the most relevant section. Never overwrite.
5. Summarise what was saved and where.

## Promoting soft → hard memory

If a pattern in `style_notes.md` has been observed multiple times across sessions, suggest promoting it:
*"I've noted '[observation]' a few times now — should I move it to writing_strategies.md as a permanent rule?"*
