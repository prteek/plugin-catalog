---
description: Copy previous results to clipboard in specified format (tsv, csv, json, markdown). TSV/CSV formats are optimized for Excel pasting.
argument-hint: <format: tsv|csv|json|markdown>
---

Copy the most recent results to the clipboard in the format given as `$ARGUMENTS`.

1. **Identify the most recent table/data output** in the conversation (the immediately preceding command/tool result). It must be tabular data (markdown table, structured data) — NOT text, documentation, or error messages.
2. **Validate the format argument.** Supported: `tsv`, `csv`, `json`, `markdown`. If invalid: error `Error: Invalid format '$ARGUMENTS'. Supported: tsv, csv, json, markdown`.
3. **Validate data compatibility.** Markdown tables and structured data (JSON, lists) are compatible with all formats. Text/documentation is NOT: error `Error: Data is not compatible with $ARGUMENTS format`. If the data changed since the last output: error `Error: Previous results have changed`.
4. **Convert and copy with bash** (macOS `pbcopy`). Do NOT just say "copying" — actually run the command:
   - **TSV**: tab-separated columns, newline-separated rows.
   - **CSV**: comma-separated; quote fields containing commas, quotes, or newlines.
   - **JSON**: validate and copy as-is.
   - **Markdown**: copy the markdown table as-is.

   ```bash
   cat <<'EOF' | pbcopy
   [formatted data with tabs/commas as appropriate]
   EOF
   echo "✓ Data copied to clipboard in [FORMAT] format"
   ```

5. **Error conditions** (always surface an error, never bypass): no previous output available; previous output is not tabular/structured; format incompatible with data structure; multiple incompatible outputs in context.

Always extract the exact table data from the most recent output, format it properly (tabs for TSV, commas for CSV), execute the `cat <<'EOF' | pbcopy` command, and confirm with an output message showing what was copied.
