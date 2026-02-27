---
name: cover-letter-writer
description: STEP 3 of the application pipeline. Writes and iteratively refines a cover letter using workspace/application_brief.md, workspace/job_description.md, and knowledge/writing_strategies.md. Trigger when the user wants to generate, revise, shorten, rewrite, or polish the cover letter in workspace/final_draft.md. Requires application_brief.md to exist - if missing, direct the user to run application-advisor first.
---

# Cover Letter Writer

## Project context
- Brief: `workspace/application_brief.md`
- Job description: `workspace/job_description.md`
- Style rules: `knowledge/writing_strategies.md`
- Output: `workspace/final_draft.md`

## Workflow

### Initial draft
1. Read `@workspace/application_brief.md` - use the matched experiences, angles, and tone note.
2. Read `@workspace/job_description.md` - use the Company Intelligence section and "Notes for application" to add specificity and mirror the company's language.
3. Read `@knowledge/writing_strategies.md` - apply vocabulary, structure, and tone rules strictly.
4. Write a complete, personal cover letter. Not generic. Not templated-sounding.
5. Save to `workspace/final_draft.md`.

### Iterative refinement
- Stay in conversation after the initial draft.
- Apply **only** the changes the user requests.
- Always output the **complete updated letter** - never partial snippets.
- End each revision with: *"What would you like to change?"*

## Rules
- Follow writing strategies strictly - they encode the user's real voice.
- The brief's "Tone Note" overrides default tone choices.
- Save the updated draft to `workspace/final_draft.md` after every revision.
- Do not update `writing_strategies.md` or `style_notes.md` - that is handled by the **style-updater** skill.
