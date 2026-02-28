---
name: profile-builder
description: Builds and updates the user's personal profile from raw CV or career materials. Use when the user uploads a CV, LinkedIn export, or any background document to raw_materials/personal_materials/ and wants to update my_info/personal_profile.md. Also use when the user wants to add a new experience, skill, or education entry to their profile.
---

# Profile Builder

## Project context
- Profile lives at `my_info/personal_profile.md`
- Raw materials (CVs, exports) are in `raw_materials/personal_materials/` (supported formats: pdf, txt, md)

## Workflow

1. Read `@my_info/personal_profile.md` (current state).
2. Read the raw material the user provides via `@file` reference.
3. Extract and structure the information — ask the user to clarify anything ambiguous.
4. Write the **complete updated** `my_info/personal_profile.md`. Never delete existing content without asking.

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
