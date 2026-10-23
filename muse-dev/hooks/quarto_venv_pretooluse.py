#!/usr/bin/env python3
"""Quarto venv gate (PreToolUse) for the muse-dev plugin.

Blocks any `quarto ...` command run by the agent unless a Python virtual
environment is active. The active env is expected to have all necessary
dependencies installed; generally this is the `.venv` in the working
directory (`source .venv/bin/activate` before running quarto).
"""
import json
import os
import re
import sys
from pathlib import Path

QUARTO_RE = re.compile(
    r"(?:^|[;&|(`]|\n|\|\||&&)\s*(?:\S+/)?quarto\b"  # quarto, ./quarto, .venv/bin/quarto
    r"|\buvx?\s+(?:run\s+)?quarto\b"  # uv run quarto / uvx quarto
    r"|\bpython\S*\s+-m\s+quarto\b",  # python -m quarto
)

try:
    event = json.load(sys.stdin)
except (json.JSONDecodeError, EOFError):
    sys.exit(0)

if event.get("hook_event_name") not in ("PreToolUse", "", None):
    sys.exit(0)

tool_input = event.get("tool_input", {}) or {}
command = tool_input.get("command", "") or ""
if not QUARTO_RE.search(command):
    sys.exit(0)

venv = os.environ.get("VIRTUAL_ENV", "").strip()
if venv and Path(venv).is_dir():
    sys.exit(0)

candidates: list[Path] = []
for raw in (
    tool_input.get("cwd"),
    tool_input.get("working_directory"),
    tool_input.get("workdir"),
    event.get("cwd"),
    os.environ.get("MUSE_PROJECT_DIR"),
    os.environ.get("CLAUDE_PROJECT_DIR"),
):
    if raw:
        candidates.append(Path(str(raw)).expanduser())
candidates.append(Path.cwd())

existing = next(
    (
        c
        for c in candidates
        if (c / ".venv").is_dir() or (c / ".venv" / "bin" / "activate").is_file()
    ),
    None,
)
hint = (
    f"found at {existing / '.venv'} — run `source .venv/bin/activate` first"
    if existing is not None
    else "expected at ./.venv in the working directory"
)

print(
    "Quarto blocked: no active Python virtual environment (VIRTUAL_ENV is not "
    f"set). Activate the environment ({hint}), which is assumed to have all "
    "necessary dependencies installed, then re-run the quarto command.",
    file=sys.stderr,
)
sys.exit(2)
