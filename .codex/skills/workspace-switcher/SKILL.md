---
name: workspace-switcher
description: Manages multiple job applications by switching the active workspace. Use when the user wants to start a new application, switch to a different job, list existing applications, or resume a previously saved application. Saves the current workspace to applications/ and loads the target into active_application/ so all other skills always read from the same place.
---

# Workspace Switcher

Manage multiple job applications. All other skills always read from `active_application/`, so this skill should dispatch to the bundled script rather than re-implementing workspace state transitions in chat.

## Bundled script

Use `.codex/skills/workspace-switcher/scripts/workspace_switcher.py` for all workspace operations in this skill. Run it from the repository root.

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
    submission/              ← send-ready artifacts for this role
        submission_email.md  ← send-ready email draft
        README.md

applications/
    google-swe/              ← saved snapshots
        job_description.md
        application_brief.md
        final_draft.md
        submission/
            submission_email.md
            [Name]_Cover_Letter.pdf
            README.md
    meta-pm/
        ...
```

## Commands — respond to natural language like:

| User says | Action |
|---|---|
| "new application" / "start fresh" | Ask for slug, then run the single `new` command |
| "switch to [company]" / "load [slug]" | Run the single `switch` command |
| "list applications" / "what applications do I have" | Run `list` |
| "save current application" | Run `save-current` |
| "delete [slug]" | Confirm first, then remove from `applications/` via the bundled script |

## Primary commands

Switch to a saved application:

```bash
python .codex/skills/workspace-switcher/scripts/workspace_switcher.py switch [target-slug]
```

Create a new active application:

```bash
python .codex/skills/workspace-switcher/scripts/workspace_switcher.py new [company]-[role]
```

List saved applications and the current active slug:

```bash
python .codex/skills/workspace-switcher/scripts/workspace_switcher.py list
```

Save the current active application without switching:

```bash
python .codex/skills/workspace-switcher/scripts/workspace_switcher.py save-current
```

Delete a saved application after explicit confirmation:

```bash
python .codex/skills/workspace-switcher/scripts/workspace_switcher.py delete [target-slug] --confirm
```

## Workflow rules

1. For "new application", ask the user for a slug if they did not provide one.
2. For "delete", ask for explicit confirmation before passing `--confirm`.
3. For all other operations, prefer the single high-level script command over piecing together lower-level subcommands in chat.
4. Confirm the resulting active slug or deleted slug after the script completes.

## Rules
- Slug format: lowercase, hyphens only, no spaces. e.g. `google-swe`, `meta-pm-2025`.
- Never delete from `applications/` without explicit user confirmation.
- Never modify `memory/` — it is global across all applications (e.g. writing_strategies.md is shared).
- Use the bundled script for workspace operations instead of rewriting filesystem commands inline.
- Prefer the high-level `switch` and `new` commands over manual sequencing of save/reset/load steps.
