---
name: workspace-switcher
description: Manages multiple job applications by switching the active workspace. Use when the user wants to start a new application, switch to a different job, list existing applications, or resume a previously saved application. Saves the current workspace to applications/ and loads the target into workspace/ so all other skills always read from the same place.
---

# Workspace Switcher

Manages multiple job applications. All other skills always read from `workspace/` — this skill handles saving and loading between applications.

## File structure

```
workspace/
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
| "new application" / "start fresh" | Create new slug, save current, clear workspace |
| "switch to [company]" / "load [slug]" | Save current, load target into workspace |
| "list applications" / "what applications do I have" | List folders in `applications/` + show `.active` |
| "save current application" | Save workspace → `applications/[slug]/` |
| "delete [slug]" | Confirm first, then remove from `applications/` |

## Workflow for switching

1. Read `workspace/.active` to get the current slug.
2. **Save current**: copy `workspace/job_description.md`, `application_brief.md`, `final_draft.md` → `applications/[current-slug]/` (skip if slug is `none`).
3. **Load target**: copy the target application's files from `applications/[target-slug]/` → `workspace/`. Missing files are fine — leave them empty.
4. Update `workspace/.active` with the new slug.
5. Confirm: *"Switched to **[slug]**. workspace/ is now ready."*

## Workflow for new application

1. Save current workspace (step 2 above).
2. Ask the user for a short slug: `[company]-[role]` e.g. `stripe-backend`.
3. Clear `workspace/job_description.md`, `application_brief.md`, `final_draft.md` (overwrite with empty templates).
4. Update `workspace/.active` with the new slug.
5. Confirm: *"New application **[slug]** is active. Run job-researcher to begin."*

## Rules
- Slug format: lowercase, hyphens only, no spaces. e.g. `google-swe`, `meta-pm-2025`.
- Never delete from `applications/` without explicit user confirmation.
- Never modify `my_info/` or `knowledge/` — those are global across all applications (e.g. writing_strategies.md is shared).
