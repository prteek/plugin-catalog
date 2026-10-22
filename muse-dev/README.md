# muse-dev Plugin

Developer utilities for Muse. Muse-native port of selected `da-dev` capabilities.

## Version

Current: `0.2.0`

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
│   └── plugin.json          # Plugin manifest (version 0.2.0)
├── commands/
│   ├── show-commands.md        # Repeat previous commands for copying
│   └── copy-to-clipboard.md    # Copy results to clipboard (tsv/csv/json/markdown)
├── hooks/
│   ├── teaching_sessionstart.py  # SessionStart: announce teaching questions
│   └── teaching_pretooluse.py    # PreToolUse: gate git commit
├── skills/
│   ├── analysis-project-docs/
│   ├── duckdb/
│   └── plot/
└── README.md                # This file
```

## Changelog

### 0.2.0
- Commands: `show-commands` and `copy-to-clipboard`, ported from the `da-dev` skills in the Bricklane `da.plugin-catalog` repo.

### 0.1.0
- MotherDuck MCP server (`https://api.motherduck.com/mcp`, `MUSE_MOTHERDUCK_TOKEN` auth).
- Teaching-questions hooks (`SessionStart` + `PreToolUse`): opt-in via `Teaching questions: on` in `MUSE.local.md`; markers in `~/.muse/teaching-questions/`.
- Skills: `analysis-project-docs` (compact generic single file, no project-specific paths), `duckdb`, `plot`.
- Renamed `analysis-project-docs` to `project-docs` and refined it to a minimal 4-file set (`README`, `summary`, `decisions`, `todolist`), following the `project-docs` skill in `regression_room`.
