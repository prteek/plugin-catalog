#!/usr/bin/env python3
"""Teaching questions hook (SessionStart) for the muse-dev plugin.

Muse-native port of da-dev's teaching_questions.py. When the user has opted
in, tells Muse that teaching questions are on and gives it the session id
used for the marker files.

Opt-in: the project's MUSE.local.md contains the line
"Teaching questions: on", or the session's `on` marker exists. The session's
`off` marker switches it off. Markers live in
~/.muse/teaching-questions/ as `<state>-<session id>`, so nothing is written
into the repo.
"""
import json
import os
import re
import sys
from pathlib import Path

event = json.load(sys.stdin)
root = Path(
    os.environ.get("MUSE_PROJECT_DIR")
    or os.environ.get("CLAUDE_PROJECT_DIR")
    or event.get("cwd")
    or "."
)
session = event.get("session_id", "")
markers = Path.home() / ".muse" / "teaching-questions"


def marker(state: str) -> Path:
    return markers / f"{state}-{session}"


local = root / "MUSE.local.md"
opted_in = local.is_file() and re.search(
    r"teaching questions:\s*on\b", local.read_text(), re.IGNORECASE
)
if not (opted_in or marker("on").is_file()) or marker("off").is_file():
    sys.exit(0)

if event.get("hook_event_name") == "SessionStart":
    print(
        f"Teaching questions are on (session id {session}). After writing or "
        "changing code, use the muse-dev:teaching-questions skill before any "
        "commit; a hook blocks git commit until the user passes."
    )
sys.exit(0)
