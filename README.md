# plugin-catalog

Muse plugin catalog. Currently ships one plugin:

- [`muse-dev`](muse-dev/README.md) — developer utilities for Muse (Muse-native port of `da-dev`): `duckdb`, `plot`, and `project-docs` skills, `show-commands` and `copy-to-clipboard` commands, opt-in teaching-questions hooks, and a MotherDuck MCP server.

## Install

From a local clone:

```bash
git clone https://github.com/prteek/plugin-catalog.git
muse plugins install ./plugin-catalog/muse-dev
```

Or straight from GitHub as a marketplace:

```bash
muse plugins marketplace add catalog https://github.com/prteek/plugin-catalog
muse plugins install muse-dev@catalog
```

## Setup

```bash
export MUSE_MOTHERDUCK_TOKEN="your_motherduck_token_here"
```

## Usage

```
/duckdb SELECT * FROM read_csv('data.csv') LIMIT 10
/plot
/show-commands
/copy-to-clipboard tsv
```

See [`muse-dev/README.md`](muse-dev/README.md) for skills, hooks, MCP details, and changelog.
