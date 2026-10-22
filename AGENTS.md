# AGENTS.md

This repo is a Muse-native plugin catalog (see `muse-dev/README.md`).
For shared plugin/skill conventions, refer to `../../bricklane/da.plugin-catalog/CLAUDE.md`
(repository overview, skill scope, marketplace, versioning rationale).

## Layout

- `muse-dev/` — the plugin (Muse-native port of `da-dev` capabilities).
  - `skills/<name>/SKILL.md` — one skill per directory (`duckdb`, `plot`, `project-docs`).
  - `hooks/` — opt-in teaching-questions hooks (`teaching_sessionstart.py`, `teaching_pretooluse.py`).
  - `.muse-plugin/plugin.json` — plugin manifest (name, version, skills, hooks, MCP servers).
  - `README.md` — install, setup, usage, and changelog.

## Skills

- Follow `SKILL.md` frontmatter convention (`name`, `description`): see referenced `CLAUDE.md` “Adding a New Skill” and “Managing Skill Documentation”.
- Keep skill scope narrow — one domain/workflow per skill.
- Reference guides vs. executable tools: document when/how Claude should invoke the skill (e.g. `duckdb` always with `-csv` output; `plot` requires `-d,` CSV input and `-H` for headers).
- After adding `muse-dev/skills/<name>/SKILL.md`, register it in `.muse-plugin/plugin.json` under `capabilities.skills` with `path: "skills/<name>/SKILL.md"`.

## Hooks and MCP

- Hooks are opt-in per repo via `Teaching questions: on` in git-ignored `MUSE.local.md`; markers live in `~/.muse/teaching-questions/` so hooks never write into the repo.
- `MotherDuck` MCP server uses `https://api.motherduck.com/mcp` with `MUSE_MOTHERDUCK_TOKEN` auth (see `muse-dev/README.md` Setup).

## Versioning

- Same impact-based semver as the referenced catalog: `0.0.x` fixes/docs only, `0.x.0` new skills/servers (backward-compatible), `x.0.0` breaking changes (delete/rename/workflow change). Current version `0.1.0` in `.muse-plugin/plugin.json` and `muse-dev/README.md`.
