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
    submission_email.md      ← send-ready email draft for this role
    submission/              ← bundled send artifacts
        submission_email.md  ← archived copy of the send-ready email
        README.md

applications/
    google-swe/              ← saved snapshots
        job_description.md
        application_brief.md
        final_draft.md
        submission_email.md
        submission/
            submission_email.md
            README.md
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
2. **Save current** by copying the entire `active_application/` contents into `applications/[current-slug]/` (skip if slug is `none`):

```bash
current_slug="$(tr -d '\n' < active_application/.active)"
if [ "$current_slug" != "none" ]; then
  mkdir -p "applications/$current_slug"
  cp -R active_application/. "applications/$current_slug/"
fi
```

3. **Clear raw job inputs** while preserving `raw_inputs/job/README.md`:

```bash
python - <<'PY'
from pathlib import Path
import shutil

root = Path("raw_inputs/job")
root.mkdir(parents=True, exist_ok=True)

for path in list(root.iterdir()):
    if path.name == "README.md":
        continue
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
PY
```

4. **Reset `active_application/`** before loading the target, while preserving scaffold `README.md`:

```bash
python - <<'PY'
from pathlib import Path
import shutil

root = Path("active_application")
root.mkdir(parents=True, exist_ok=True)

for path in list(root.iterdir()):
    if path.name == "README.md":
        continue
    if path.name == "submission" and path.is_dir():
        for subpath in list(path.iterdir()):
            if subpath.name == "README.md":
                continue
            if subpath.is_dir():
                shutil.rmtree(subpath)
            else:
                subpath.unlink()
        continue
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()

(root / "submission").mkdir(parents=True, exist_ok=True)
PY
```

5. **Load target** by copying the entire saved application back into `active_application/`:

```bash
target_slug="[target-slug]"
cp -R "applications/$target_slug/." active_application/
printf '%s\n' "$target_slug" > active_application/.active
```

6. Confirm: *"Switched to **[slug]**. active_application/ is now ready, and raw_inputs/job/ has been cleared."*

## Workflow for new application

1. Save current active application (step 2 above).
2. Ask the user for a short slug: `[company]-[role]` e.g. `stripe-backend`.
3. Clear `raw_inputs/job/` using the exact command in step 3 above.
4. Reset `active_application/` using the exact command in step 4 above.
5. Recreate the expected empty working files:

```bash
python - <<'PY'
from pathlib import Path

root = Path("active_application")
(root / "submission").mkdir(parents=True, exist_ok=True)

for rel in [
    "job_description.md",
    "application_brief.md",
    "final_draft.md",
    "submission_email.md",
]:
    (root / rel).write_text("")
PY
```

6. Update `active_application/.active` with the new slug:

```bash
new_slug="[company]-[role]"
printf '%s\n' "$new_slug" > active_application/.active
```

7. Confirm: *"New application **[slug]** is active. raw_inputs/job/ was cleared. Run job-researcher to begin."*

## Rules
- Slug format: lowercase, hyphens only, no spaces. e.g. `google-swe`, `meta-pm-2025`.
- Never delete from `applications/` without explicit user confirmation.
- Never modify `memory/` — it is global across all applications (e.g. writing_strategies.md is shared).
- Prefer whole-directory copy and reset commands over file-by-file copy; this reduces drift as `active_application/` evolves.
