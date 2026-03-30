# Repo Guidance

## Pipeline

- This repository uses a file-based application pipeline. Shared memory lives in `memory/`. The current role lives in `active_application/`. Saved role snapshots live in `applications/`.
- Prefer the Codex skills in `.codex/skills/` for step-specific behavior.
- Follow the pipeline order unless the user is explicitly asking for a later step and the required upstream files already exist:
  1. `profile-builder` updates `memory/personal_profile.md`
  2. `voice-archivist` updates `memory/style_guidelines.md`
  3. `workspace-switcher` creates or switches the active role
  4. `job-researcher` writes `active_application/job_description.md`
  5. `application-advisor` writes `active_application/application_brief.md`
  6. `cover-letter-writer` writes `active_application/final_draft.md`
  7. `application-submitter` writes `active_application/submission/`
  8. `writing-coach` updates `memory/writing_strategies.md`

## Skill Boundaries

- Treat `active_application/job_description.md` as the single source of truth for job context.
- Treat `active_application/application_brief.md` as the single source of truth for candidate positioning.
- Treat `memory/` as global shared memory. Do not clear or rewrite it during workspace switching.
- Use bundled scripts when a skill provides one instead of recreating deterministic filesystem or PDF steps in chat.

## Python Environment

- Prefer `PDF_PYTHON` when it is set for any Python or PDF-generation workflow in this repository.
- Otherwise use the active `python` from the current session.
- Do not assume a desktop app inherited the intended Conda environment correctly; verify the active interpreter when environment behavior is ambiguous.

## Codex Skills

- Codex-discoverable skills live under `.codex/skills/`.
- Keep skill descriptions trigger-oriented because they are the primary routing surface.
