---
description: Display executable commands from previous operations
---

Display the terminal commands that were used to generate the previous output, formatted so you can easily copy and run them manually.

- Display the command(s) that were just executed in executable code blocks.
- Include comments explaining what each command does.
- Make them easy to copy and paste into your terminal.

Examples: after a data analysis, show `duckdb -csv -c "SELECT * FROM my_table" | uplot lines -d, -H`; after data processing, show the exact pipes and transformations used; after creating a plot or querying a database, show the exact command to re-run it with different parameters.

Use immediately after an operation, while it is fresh in context. Copy the displayed commands to your notes and modify them as needed for different inputs or parameters.
