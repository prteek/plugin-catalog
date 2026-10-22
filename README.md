# plugin-catalog

Muse plugin catalog. Currently ships one plugin:

- [`muse-dev`](muse-dev/README.md) — developer utilities for Muse (Muse-native port of `da-dev`): `duckdb`, `plot`, and `project-docs` skills, opt-in teaching-questions hooks, and a MotherDuck MCP server.

## Install

```bash
git clone https://github.com/prteek/plugin-catalog.git
muse plugins install ./plugin-catalog/muse-dev
```

## Setup

```bash
export MUSE_MOTHERDUCK_TOKEN="your_motherduck_token_here"
```

## Usage

```
/duckdb SELECT * FROM read_csv('data.csv') LIMIT 10
/plot
```

See [`muse-dev/README.md`](muse-dev/README.md) for skills, hooks, MCP details, and changelog.
