#!/usr/bin/env python3
"""Focused checks for the quarto venv PreToolUse hook.

Run: `python3 test_quarto_venv_hook.py` (stdlib only, exit 0 = pass).
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "quarto_venv_pretooluse.py"


def run_hook(command: str, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    env.update(env_extra or {})
    event = {
        "hook_event_name": "PreToolUse",
        "cwd": str(Path.cwd()),
        "tool_input": {"command": command},
    }
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env=env,
    )


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        check.failed = True


check.failed = False

# Non-quarto commands always pass through, no venv needed.
r = run_hook("ls -la && git status")
check("non-quarto command passes without venv", r.returncode == 0)

# Quarto without an active venv is blocked (exit 2).
for cmd in (
    "quarto render report.qmd",
    "quarto preview",
    "make docs && quarto render .",
    "uv run quarto render report.qmd",
    ".venv/bin/quarto render report.qmd",
    "python -m quarto render report.qmd",
):
    r = run_hook(cmd)
    check(f"blocked without venv: {cmd!r}", r.returncode == 2)

# Quarto with an active venv passes.
with tempfile.TemporaryDirectory() as tmp:
    r = run_hook("quarto render report.qmd", {"VIRTUAL_ENV": tmp})
    check("quarto passes with VIRTUAL_ENV set", r.returncode == 0)

# A bare VIRTUAL_ENV pointing nowhere does not count.
r = run_hook("quarto render report.qmd", {"VIRTUAL_ENV": "/nonexistent-venv-xyz"})
check("quarto blocked when VIRTUAL_ENV dir is missing", r.returncode == 2)

# The word inside prose is not treated as a quarto invocation.
r = run_hook('echo "use quarto for publishing"')
check("prose mentioning quarto passes", r.returncode == 0)

sys.exit(1 if check.failed else 0)
