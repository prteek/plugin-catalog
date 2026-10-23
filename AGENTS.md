# AGENTS.md

This repo is a Muse-native plugin catalog (see `muse-dev/README.md`).

## Layout

- `.agents/plugins/marketplace.json` — marketplace catalog (Codex schema: `source` is `{"source": "local", "path": ...}`); keep its plugin `version` in sync with `plugin.json`.
- `muse-dev/` — the developer-utilities plugin.
  - `skills/<name>/SKILL.md` — one skill per directory (`duckdb`, `plot`, `project-docs`).
  - `commands/<name>.md` — Markdown command templates (`show-commands`, `copy-to-clipboard`); `$ARGUMENTS` receives the user's input.
  - `hooks/` — opt-in teaching-questions hooks (`teaching_sessionstart.py`, `teaching_pretooluse.py`).
  - `.muse-plugin/plugin.json` — plugin manifest (name, version, skills, commands, hooks, MCP servers).
  - `README.md` — install, setup, usage, and changelog.

## Skills

- Follow `SKILL.md` frontmatter convention (`name`, `description`).
- Keep skill scope narrow — one domain/workflow per skill.
- Reference guides vs. executable tools: document when/how Claude should invoke the skill (e.g. `duckdb` always with `-csv` output; `plot` requires `-d,` CSV input and `-H` for headers).
- After adding `muse-dev/skills/<name>/SKILL.md`, register it in `.muse-plugin/plugin.json` under `capabilities.skills` with `path: "skills/<name>/SKILL.md"`.

## Hooks and MCP

- Hooks are opt-in per repo via `Teaching questions: on` in git-ignored `MUSE.local.md`; markers live in `~/.muse/teaching-questions/` so hooks never write into the repo.
- `MotherDuck` MCP server uses `https://api.motherduck.com/mcp` with `MUSE_MOTHERDUCK_TOKEN` auth (see `muse-dev/README.md` Setup).

## Versioning

- Impact-based semver, bumped only for functional changes: `0.0.x` fixes, `0.x.0` new skills/commands/hooks/servers (backward-compatible), `x.0.0` breaking changes (delete/rename/workflow change). Docs-only and other non-functional changes need no version bump (enforced by the `version-bump` PreToolUse hook, which blocks `git push` when the pushed range adds `muse-dev/skills/`, `muse-dev/commands/`, `muse-dev/hooks/`, or `muse-dev/.muse-plugin/` changes on top of the deployed `origin/main` version without a version bump — no re-increment once the version is already ahead of main). Keep the plugin `version` in sync in `.muse-plugin/plugin.json`, `.agents/plugins/marketplace.json`, and `muse-dev/README.md`.
