---
name: duckdb
description: "Query and analyze CSV, Parquet, or DuckDB files locally or from URLs using SQL"
---

# DuckDB Skill

Use this skill to query and analyze data files (CSV, Parquet, .duckdb) locally or from URLs with SQL. DuckDB is an embedded analytical database that allows you to run SQL queries directly on files without needing to load them into memory.

```shell
duckdb -csv -c "SELECT * FROM
   read_csv_auto('data.csv') LIMIT 10"

```

## Usage

Pass SQL queries as arguments to the skill. The skill executes queries using DuckDB CLI against files in the project directory.

## Output Formatting

**Important:** Do not use DuckDB's native table formatting. Instead, format results always use -csv flag to output in CSV format, which can be easily converted to:
- **Markdown tables** for tabular data (use pipes and dashes)
- **Bullet lists** for simple results
- **Structured text** with clear headers and sections

This ensures human readability and integrates well with documentation.

## When to Use This Skill

**Always use this skill** when the user asks to read data from:
- A URL (e.g. `https://raw.githubusercontent.com/...`) pointing to a CSV, Parquet, or other data file
- A local CSV, Parquet, or `.duckdb` file

Do **not** use MotherDuck MCP or any other tool for reading raw data files from URLs — use this skill exclusively.

## Examples

- `SELECT DISTINCT Location FROM read_csv('data.csv')`
- `SELECT * FROM read_parquet('data.parquet') LIMIT 10`
- `SELECT * FROM read_csv('https://raw.githubusercontent.com/kojix2/rdatasets/master/data/datasets/islands.csv')`

## Notes

- Results are displayed in human-readable format, DUCKDB output is always with -csv flag to ensure consistent formatting
