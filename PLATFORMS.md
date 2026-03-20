# Platform Setup Notes

This project is built around a portable file workflow:

- `raw_inputs/`
- `memory/`
- `active_application/`
- `applications/`

The agent platform is just the orchestration layer on top.

## Cursor

- Keep the skill files in `.cursor/skills/`.
- Cursor can read those `SKILL.md` files directly as the project skill implementation.
- This repository is currently wired for Cursor out of the box.

## Claude Code

- Reuse the existing `SKILL.md` files as the source instructions.
- Port each skill into your preferred Claude Code project guidance format, such as project docs, command templates, or reusable prompt files.
- Keep the same file contracts and workflow steps so the agents continue to pass work through the repo in the same way.

## Codex

- Reuse the same `SKILL.md` files as the source prompt specs.
- Port them into the repo-level guidance format you want Codex to follow, for example a project instruction file or task-specific prompt docs.
- Keep the workflow file-based so Codex reads and writes the same folders as the Cursor version.

## Recommended approach

- Treat `.cursor/skills/` as the reference implementation, not the only implementation.
- Keep the workflow logic platform-neutral.
- If you adapt the project to another platform, preserve the same file names and folder responsibilities whenever possible.
