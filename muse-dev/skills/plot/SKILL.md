---
name: plot
description: "Create terminal-based plots from data using YouPlot"
---

# Plot Skill (YouPlot)

Use `uplot` to create terminal plots. Install with `brew install youplot`.

## Key Rules

- **Always use `-d,`** for CSV input (default is tab-separated)
- **Wide form required**: each column = one series, each row = one observation, use PIVOT in DuckDB to reshape if needed
- **Use `-H` for header rows** to label series (don't use `tail -n +2` to remove headers)
- Use `-H` if input has a header row
- Do not reshape the plot using -h and -w options, default size is good for most cases

## Commands

| Command | Description |
|---|---|
| `bar` | Horizontal bar chart |
| `hist` | Histogram |
| `line` / `lines` | Line / multi-series line (requires wide form) |
| `scatter` | Scatter plot |
| `box` | Boxplot (requires wide form) |
| `count` | Bar chart by occurrence count |

## Common Options

```
-d,          CSV delimiter
-H           has header
-t STR       title
--xlabel/-ylabel STR  axis labels
-w/-h INT    width/height
```

## Patterns

### Bar chart
```bash
duckdb -csv -noheader -c "SELECT name, count FROM t ORDER BY count DESC" \
  | uplot bar -d, -t "Title"
```

### Line chart (multi-series)
```bash
duckdb -csv -c "SELECT x, y1, y2 FROM t" \
  | uplot lines -d, -H -t "Title"
```

### Scatter
```bash
duckdb -csv -noheader -c "SELECT x, y FROM t" \
  | uplot scatter -d, -t "X vs Y"
```

### Boxplot (long → wide with PIVOT)
Boxplot needs one column per group. Use DuckDB `PIVOT`:

```bash
duckdb -csv -c "
  SELECT * EXCLUDE(rn) FROM (
    PIVOT (
      SELECT ROW_NUMBER() OVER (PARTITION BY grp ORDER BY val) AS rn, grp, val
      FROM t
    ) ON grp USING first(val) GROUP BY rn
  )
" | uplot box -d, -H -t "Groups vs Value"
```

**PIVOT caveats:**
- `ROW_NUMBER()` (`rn`) is needed to align rows across groups but must be **excluded from the SELECT** before piping — uplot will treat it as an extra series otherwise
- Use `SELECT * EXCLUDE(rn)` in an outer query (can't exclude inside PIVOT directly)
- Use `-H` (not `tail -n +2`) so column headers become group labels on the plot
- Avoid `!=` in `-c` inline SQL — the shell escapes `!`; use `<>` instead

> **Note**: When piping through `/dev/stdin`, DuckDB reads the stream twice. Fix with `read_csv('/dev/stdin', auto_detect=false, ...)`.
