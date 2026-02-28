---
name: cover-letter-writer
description: STEP 3 of the application pipeline. Writes and iteratively refines a cover letter using active_application/application_brief.md, active_application/job_description.md, and memory/writing_strategies.md. Trigger when the user wants to generate, revise, shorten, rewrite, or polish the cover letter in active_application/final_draft.md. Requires application_brief.md to exist - if missing, direct the user to run application-advisor first.
---

# Cover Letter Writer

## Project context
- Brief: `active_application/application_brief.md`
- Job description: `active_application/job_description.md`
- Style Guidelines: `memory/style_guidelines.md`
- Writing Strategies (hard rules): `memory/writing_strategies.md`
- Output: `active_application/final_draft.md`

## Workflow

### Initial draft
1. Read `@active_application/application_brief.md` - use the matched experiences, angles, and tone note.
2. Read `@active_application/job_description.md` - use the Company Intelligence section and "Notes for application" to add specificity and mirror the company's language.
3. Read `@memory/style_guidelines.md` - match the user's baseline voice, structure, and phrasing patterns.
4. Read `@memory/writing_strategies.md` - apply confirmed rules strictly. If a strategy conflicts with a guideline, the strategy wins.
5. Write a complete, personal cover letter. Not generic. Not templated-sounding.
6. Save to `active_application/final_draft.md`.

### Iterative refinement
- Stay in conversation after the initial draft.
- Apply **only** the changes the user requests.
- Always output the **complete updated letter** - never partial snippets.
- End each revision with: *"What would you like to change?"*

## Rules
- Follow writing strategies strictly - they encode the user's real voice.
- The brief's "Tone Note" overrides default tone choices.
- Save the updated draft to `active_application/final_draft.md` after every revision.
- Do not update `writing_strategies.md` - that is handled by the **writing-coach** skill.
