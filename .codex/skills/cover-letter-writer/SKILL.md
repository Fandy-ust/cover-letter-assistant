---
name: cover-letter-writer
description: STEP 3 of the application pipeline. Writes and iteratively refines a cover letter using active_application/application_brief.md, active_application/job_description.md, optional guidance from memory/style_guidelines.md and memory/writing_strategies.md, and the bundled natural-voice reference. Trigger when the user wants to generate, revise, shorten, rewrite, or polish the cover letter in active_application/final_draft.md, especially when they want it to sound more natural and less generic. Requires application_brief.md to exist - if missing, direct the user to run application-advisor first.
---

# Cover Letter Writer

## Project context
- Brief: `active_application/application_brief.md`
- Job description: `active_application/job_description.md`
- Style guidelines (optional): `memory/style_guidelines.md`
- Writing strategies (optional): `memory/writing_strategies.md`
- Natural voice reference (optional): `references/natural_voice.md`
- Output: `active_application/final_draft.md`

## Workflow

### Initial draft
1. Read `@active_application/application_brief.md` - use the matched experiences, angles, and tone note.
2. Read `@active_application/job_description.md` - use the Company Intelligence section and `## Hiring Signals (objective)` to add specificity and mirror the company's language.
3. If `@memory/style_guidelines.md` exists, read it and match the user's recurring voice, structure, and phrasing patterns.
4. If `@memory/writing_strategies.md` exists, read it and apply those strategies strictly. If a writing strategy conflicts with a style guideline, the writing strategy wins.
5. If `references/natural_voice.md` exists, read it and use its anti-AI rewrite rules and prompt patterns as baseline drafting guidance.
6. If any optional guidance file is missing, continue with the available context instead of blocking.
7. Write a complete, personal cover letter. Not generic. Not templated-sounding.
8. Save to `active_application/final_draft.md`.

### Iterative refinement
- Stay in conversation after the initial draft.
- Apply **only** the changes the user requests.
- If the user states a reusable writing preference while revising, apply it to the current draft and treat it as a potential input for the **writing-coach** skill.
- Always output the **complete updated letter** - never partial snippets.
- End each revision with: *"What would you like to change?"*

## Rules
- Follow writing strategies strictly when they exist.
- Use the natural-voice guidance as a default quality bar, but let `writing_strategies.md` and direct user edits override it.
- If `style_guidelines.md` is missing, rely on the brief's tone note and the user's requested edits.
- If `writing_strategies.md` is missing, do not invent extra writing strategies.
- The brief's "Tone Note" overrides default tone choices.
- Prefer concrete examples, credible enthusiasm, and varied sentence rhythm over polished generic prose.
- Distinguish between one-off draft edits and reusable preferences. Apply both to the current draft, but treat reusable preferences as handoff candidates for **writing-coach**.
- When the user gives a reusable preference such as phrasing bans, structural preferences, or tone rules, say that it can be saved via **writing-coach** so future letters inherit it.
- Save the updated draft to `active_application/final_draft.md` after every revision.
- Do not update `writing_strategies.md` - that is handled by the **writing-coach** skill.
