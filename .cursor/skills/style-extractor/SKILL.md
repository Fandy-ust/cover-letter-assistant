---
name: style-extractor
description: Batch-analyzes a set of reference cover letter documents to extract writing style and generate knowledge/writing_strategies.md. Use when the user uploads or points to existing reference documents (past cover letters, writing samples) for one-time or batch analysis. Do NOT use for saving feedback given during an active drafting session — that is handled by the style-updater skill.
---

# Style Extractor

## Project context
- Reference drafts live in `raw_materials/reference_drafts/`
- Output goes to `knowledge/writing_strategies.md`

## Workflow

1. Read all reference drafts provided via `@file` references.
2. Read `@knowledge/writing_strategies.md` to preserve any existing rules.
3. Analyze the drafts across the six dimensions below.
4. Write the **complete updated** `knowledge/writing_strategies.md`.

## Six dimensions to extract

| Dimension | What to capture |
|---|---|
| **Tone & Voice** | Formal/conversational, confident/humble |
| **Sentence Structure** | Short & punchy vs. long & flowing |
| **Vocabulary** | Power words used, phrases to avoid |
| **Opening & Closing** | How letters typically begin and end |
| **Structure** | Paragraph count, use of bullets, body flow |
| **Quirks** | Any distinctive patterns worth replicating |

## Output format for `writing_strategies.md`

```markdown
# Writing Strategies

## Tone & Voice
## Sentence Structure
## Vocabulary Preferences
## Opening & Closing Patterns
## Structure & Formatting
## Unique Quirks
```

After saving, summarise the top 3 most distinctive style traits found.

## Note on continuous updates
`writing_strategies.md` is also updated incrementally by the **Cover Letter Writer** skill when the user gives generalizable feedback during drafting. This means the file improves over time without needing to re-run the full extractor. Re-run this skill only when adding a significant batch of new reference drafts.
