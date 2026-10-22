#!/usr/bin/env python3
"""Teaching questions hook (PreToolUse) for the muse-dev plugin.

Muse-native port of da-dev's teaching_questions.py. When the user has opted
in, blocks a `git commit` run by Muse until the user passes the questions.
One pass allows one commit. Commits typed in a terminal are not checked.

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

if event.get("hook_event_name") not in ("PreToolUse", "", None):
    sys.exit(0)

command = event.get("tool_input", {}).get("command", "")
# a git commit at the start of the command or of a chained/new-line command,
# not the words inside text
if not re.search(r"(?:^|[;&|(]|\n)\s*git(?:\s+-\S+(?:\s+\S+)?)*\s+commit\b", command):
    sys.exit(0)
if marker("passed").is_file():
    marker("passed").unlink()  # one pass, one commit
    sys.exit(0)

print(
    "Commit blocked: teaching questions are on and haven't been passed for "
    "this change. Ask the questions (muse-dev:teaching-questions skill) and, "
    "once the user passes, run "
    f"`mkdir -p ~/.muse/teaching-questions && touch "
    f"~/.muse/teaching-questions/passed-{session}` "
    "as its own command, then commit; or the user can say "
    '"teaching questions off" '
    f"(`touch ~/.muse/teaching-questions/off-{session}`).",
    file=sys.stderr,
)
sys.exit(2)
