---
name: voice-archivist
description: Batch-analyzes reference cover letter drafts to extract stable style guidelines and write memory/style_guidelines.md. Primary inputs are raw_inputs/style_samples/. If that folder is empty, the user can optionally select prior final_draft.md files from applications/. Do NOT use for saving feedback given during an active drafting session — that is handled by the writing-coach skill.
---

# Voice Archivist

## Project context
- Primary reference drafts live in `raw_inputs/style_samples/` (supported formats: pdf, txt, md)
- Optional fallback references: previous saved application letters in `applications/**/final_draft.md`
- Output goes to `memory/style_guidelines.md` (style baseline), not `memory/writing_strategies.md` (hard rules)

## Workflow

1. Read all reference drafts provided via `@file` references.
2. If **no** drafts were provided and `raw_inputs/style_samples/` appears empty:
   - Look for prior drafts in `applications/` (especially `applications/**/final_draft.md`).
   - Ask the user to pick a small set (e.g. 3–7) application slugs/drafts that best represent their voice.
   - Read only the user-selected `final_draft.md` files (do not guess).
3. Read `@memory/style_guidelines.md` to preserve any existing baseline.
4. Analyze the drafts across the six dimensions below.
5. Write the **complete updated** `memory/style_guidelines.md`.

## Six dimensions to extract

| Dimension | What to capture |
|---|---|
| **Tone & Voice** | Formal/conversational, confident/humble |
| **Sentence Structure** | Short & punchy vs. long & flowing |
| **Vocabulary** | Power words used, phrases to avoid |
| **Opening & Closing** | How letters typically begin and end |
| **Structure** | Paragraph count, use of bullets, body flow |
| **Quirks** | Any distinctive patterns worth replicating |

## Output format for `style_guidelines.md`

```markdown
# Style Guidelines

## Tone & Voice
## Sentence Structure
## Vocabulary Preferences
## Opening & Closing Patterns
## Structure & Formatting
## Unique Quirks
```

After saving, summarise the top 3 most distinctive style traits found.
