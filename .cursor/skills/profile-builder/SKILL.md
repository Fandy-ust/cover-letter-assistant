---
name: profile-builder
description: Builds and updates the user's personal profile from raw CV or career materials. Use when the user shares CV/background context as files in raw_inputs/profile/ or directly in chat, and wants to update memory/personal_profile.md. Also use when the user wants to add a new experience, skill, or education entry to their profile.
---

# Profile Builder

## Project context
- Profile lives at `memory/personal_profile.md`
- Raw materials can come from files in `raw_inputs/profile/` (supported formats: pdf, txt, md) or directly from chat context.

## Workflow

1. Read `@memory/personal_profile.md` (current state).
2. Read the raw material the user provides (either via `@file` reference or pasted/summarized in chat).
3. Extract and structure the information — ask the user to clarify anything ambiguous.
4. Write the **complete updated** `memory/personal_profile.md`. Never delete existing content without asking.

## Output format for `personal_profile.md`

```markdown
# Personal Profile

## Contact Information

## Professional Summary

## Experiences
### [Job Title] — [Company] (YYYY – YYYY)
- STAR-style bullet points

## Education

## Skills
```

## Rules
- Append and improve — never overwrite without reading first.
- Use STAR-style summaries for each experience where possible.
- After saving, confirm what was added or changed.
