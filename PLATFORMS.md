# Platform Setup Notes

This project is built around a portable file workflow:

- `raw_inputs/`
- `memory/`
- `active_application/`
- `applications/`

The agent platform is just the orchestration layer on top.

## Codex

- Keep the skill files in `.codex/skills/`.
- Codex can use those `SKILL.md` files as the project skill implementation.
- This repository is currently wired for Codex out of the box.

## Cursor

- Keep the skill files in `.cursor/skills/`.
- Cursor can read those `SKILL.md` files directly as the project skill implementation.
- Keep the Cursor tree aligned with `.codex/skills/` so both platforms follow the same workflow contracts.

## Claude Code

- Reuse the existing `SKILL.md` files as the source instructions.
- Port each skill into your preferred Claude Code project guidance format, such as project docs, command templates, or reusable prompt files.
- Keep the same file contracts and workflow steps so the agents continue to pass work through the repo in the same way.

## Recommended approach

- Treat `.codex/skills/` and `.cursor/skills/` as parallel implementations of the same workflow contracts.
- Keep the workflow logic platform-neutral.
- If you adapt the project to another platform, preserve the same file names and folder responsibilities whenever possible.
