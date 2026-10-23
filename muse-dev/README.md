# muse-dev Plugin

Developer utilities for Muse.

## Version

Current: `0.4.0`

## Features

### Skills

| Skill | Purpose |
|-------|---------|
| `project-docs` | Set up or update a minimal doc set (`README`, `summary`, `decisions`, `todolist`) for a project folder |
| `duckdb` | Query CSV, Parquet, or DuckDB files locally or from URLs using SQL via the DuckDB CLI |
| `plot` | Create terminal-based plots from data using YouPlot |

### Commands

| Command | Purpose |
|---------|---------|
| `show-commands` | Display the commands used for the previous output, ready to copy and re-run |
| `copy-to-clipboard` | Copy previous results to the clipboard (tsv, csv, json, markdown) |

### Hooks

The teaching-questions hooks block Muse-run `git commit` until the user passes 3 conceptual questions. Opt-in per repo by adding this line to `MUSE.local.md` at the repo root (keep that file git-ignored):

```
Teaching questions: on
```

- **SessionStart:** tells Muse teaching questions are on and gives it the session id.
- **PreToolUse (Bash):** blocks a `git commit` run by Muse until the user passes. One pass allows one commit. Commits typed in a terminal are not checked.
- Say "teaching questions off" or "on" to switch for the current session. Markers live in `~/.muse/teaching-questions/`, so nothing is written into the repo.

The quarto-venv hook is always on: it blocks any `quarto ...` command run by Muse unless a Python virtual environment is active (`VIRTUAL_ENV` set). That env is assumed to have all necessary dependencies installed — generally the `.venv` in the working directory, so run `source .venv/bin/activate` before rendering.

The version-bump hook is always on: it blocks a `git push` run by Muse when the pushed range adds `skills/`, `commands/`, `hooks/`, or `.muse-plugin/` changes on top of the deployed version (`origin/main` on GitHub) without a version bump — commit the bump first, then re-push. Once the version is bumped ahead of main, further changes ride along with no re-increment. Docs-only and other non-functional changes pass through — they don't require users to update the plugin, so they need no bump.

### MCP Servers

#### MotherDuck (HTTP)

Cloud-hosted DuckDB for analytics and data querying.

**Endpoint**: `https://api.motherduck.com/mcp`

**Authentication**: `MUSE_MOTHERDUCK_TOKEN` environment variable

## Installation

```bash
muse plugins install <path-to-plugin-catalog>/muse-dev
```

## Setup

```bash
export MUSE_MOTHERDUCK_TOKEN="your_motherduck_token_here"
```

## Usage

Invoke skills directly:

```
/duckdb SELECT * FROM read_csv('data.csv') LIMIT 10
/plot
```

After querying with `/duckdb`, pipe to `/plot` for terminal visualisation. After finishing analysis work, use `analysis-project-docs` to record status, decisions and next tasks.

## Architecture

```
muse-dev/
├── .muse-plugin/
│   └── plugin.json          # Plugin manifest (version 0.4.0)
├── commands/
│   ├── show-commands.md        # Repeat previous commands for copying
│   └── copy-to-clipboard.md    # Copy results to clipboard (tsv/csv/json/markdown)
├── hooks/
│   ├── teaching_sessionstart.py  # SessionStart: announce teaching questions
│   ├── teaching_pretooluse.py    # PreToolUse: gate git commit
│   ├── quarto_venv_pretooluse.py # PreToolUse: require active venv for quarto
│   └── version_bump_pretooluse.py # PreToolUse: require version bump for functional changes
├── tests/
│   ├── test_quarto_venv_hook.py  # Checks for the quarto venv gate
│   └── test_version_bump_hook.py # Checks for the version-bump gate
├── skills/
│   ├── analysis-project-docs/
│   ├── duckdb/
│   └── plot/
└── README.md                # This file
```

## Changelog

### 0.4.0
- Version-bump hook (`PreToolUse` on `git push`): blocks the push when the pushed range adds functional changes (`skills/`, `commands/`, `hooks/`, `.muse-plugin/`) on top of the deployed `origin/main` version without a version bump; no re-increment once the version is ahead of main, and docs-only changes pass through. Checks in `muse-dev/tests/test_version_bump_hook.py`. Versioning policy (AGENTS.md): bumps only for functional changes, never for docs-only edits.

### 0.3.0
- Quarto-venv hook (`PreToolUse`): blocks Muse-run `quarto` commands unless a Python virtual environment is active (generally `.venv` in the working directory). Checks in `muse-dev/tests/test_quarto_venv_hook.py`.

### 0.2.0
- Commands: `show-commands` and `copy-to-clipboard`.

### 0.1.0
- MotherDuck MCP server (`https://api.motherduck.com/mcp`, `MUSE_MOTHERDUCK_TOKEN` auth).
- Teaching-questions hooks (`SessionStart` + `PreToolUse`): opt-in via `Teaching questions: on` in `MUSE.local.md`; markers in `~/.muse/teaching-questions/`.
- Skills: `analysis-project-docs` (compact generic single file, no project-specific paths), `duckdb`, `plot`.
- Renamed `analysis-project-docs` to `project-docs` and refined it to a minimal 4-file set (`README`, `summary`, `decisions`, `todolist`), following the `project-docs` skill in `regression_room`.
