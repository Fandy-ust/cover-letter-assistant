---
name: workspace-switcher
description: Manages multiple job applications by switching the active workspace. Use when the user wants to start a new application, switch to a different job, list existing applications, or resume a previously saved application. Saves the current workspace to applications/ and loads the target into active_application/ so all other skills always read from the same place.
---

# Workspace Switcher

Manages multiple job applications. All other skills always read from `active_application/` — this skill handles saving and loading between applications.

## File structure

```
raw_inputs/
    job/                      ← transient raw job inputs for the active role
        README.md

active_application/
    .active                  ← current application slug (e.g. "google-swe")
    job_description.md
    application_brief.md
    final_draft.md

applications/
    google-swe/              ← saved snapshots
        job_description.md
        application_brief.md
        final_draft.md
    meta-pm/
        ...
```

## Commands — respond to natural language like:

| User says | Action |
|---|---|
| "new application" / "start fresh" | Create new slug, save current, clear active application |
| "switch to [company]" / "load [slug]" | Save current, load target into active application |
| "list applications" / "what applications do I have" | List folders in `applications/` + show `.active` |
| "save current application" | Save active application → `applications/[slug]/` |
| "delete [slug]" | Confirm first, then remove from `applications/` |

## Workflow for switching

1. Read `active_application/.active` to get the current slug.
2. **Save current**: copy `active_application/job_description.md`, `application_brief.md`, `final_draft.md` → `applications/[current-slug]/` (skip if slug is `none`).
3. **Clear raw job inputs**: remove everything in `raw_inputs/job/` except `README.md`.
4. **Load target**: copy the target application's files from `applications/[target-slug]/` → `active_application/`. Missing files are fine — leave them empty.
5. Update `active_application/.active` with the new slug.
6. Confirm: *"Switched to **[slug]**. active_application/ is now ready, and raw_inputs/job/ has been cleared."*

## Workflow for new application

1. Save current active application (step 2 above).
2. Ask the user for a short slug: `[company]-[role]` e.g. `stripe-backend`.
3. Clear `active_application/job_description.md`, `application_brief.md`, `final_draft.md` (overwrite with empty templates).
4. Remove everything in `raw_inputs/job/` except `README.md`.
5. Update `active_application/.active` with the new slug.
6. Confirm: *"New application **[slug]** is active. raw_inputs/job/ was cleared. Run job-researcher to begin."*

## Rules
- Slug format: lowercase, hyphens only, no spaces. e.g. `google-swe`, `meta-pm-2025`.
- Never delete from `applications/` without explicit user confirmation.
- Never modify `memory/` — it is global across all applications (e.g. writing_strategies.md is shared).
