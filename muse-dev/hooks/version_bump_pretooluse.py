#!/usr/bin/env python3
"""Version-bump gate (PreToolUse) for the muse-dev plugin.

Blocks a `git push` run by the agent when the range being pushed adds
functional changes (skills, commands, hooks, the plugin manifest / MCP
config) on top of the deployed version (the `origin/main` ref on GitHub)
without also bumping the plugin version. Once the version is bumped,
further changes ride along with no re-increment. Docs-only and other
non-functional changes never trigger the gate, since they don't require
users to update the plugin.

The version lives in `muse-dev/.muse-plugin/plugin.json` (mirrored in
`.agents/plugins/marketplace.json` and `muse-dev/README.md`).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PUSH_RE = re.compile(r"(?:^|[;&|(]|\n)\s*git(?:\s+-\S+(?:\s+\S+)?)*\s+push\b")
VERSION_RE = re.compile(r'"version"\s*:\s*"([^"]+)"')

# Staged paths under these prefixes count as functional changes.
FUNCTIONAL_PREFIXES = (
    "muse-dev/skills/",
    "muse-dev/commands/",
    "muse-dev/hooks/",
    "muse-dev/.muse-plugin/",
)

VERSION_FILE = "muse-dev/.muse-plugin/plugin.json"


def git(args: list[str], root: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout if out.returncode == 0 else None


try:
    event = json.load(sys.stdin)
except (json.JSONDecodeError, EOFError):
    sys.exit(0)

if event.get("hook_event_name") not in ("PreToolUse", "", None):
    sys.exit(0)

command = (event.get("tool_input", {}) or {}).get("command", "") or ""
if not PUSH_RE.search(command):
    sys.exit(0)
if "--dry-run" in command or re.search(r"\bpush\b.*(?:--delete|(?<!\S)-d\b)", command):
    sys.exit(0)  # rehearsals and branch deletions push no code

root = Path(
    os.environ.get("MUSE_PROJECT_DIR")
    or os.environ.get("CLAUDE_PROJECT_DIR")
    or event.get("cwd")
    or "."
)

toplevel = git(["rev-parse", "--show-toplevel"], root)
if not toplevel:
    sys.exit(0)  # not a git repo: nothing to gate
top = Path(toplevel.strip())

# What the push would publish: everything on this side of the merge-base
# with the deployed main.
pushed = git(["diff", "--name-only", "-z", "origin/main...HEAD"], top)
if pushed is None:
    sys.exit(0)  # no remote ref available (offline / no remote): fail open
functional = sorted(
    {p for p in pushed.split("\0") if p.startswith(FUNCTIONAL_PREFIXES)}
)
if not functional:
    sys.exit(0)


def manifest_version(spec: str) -> str | None:
    shown = git(["show", spec], top)
    if not shown:
        return None
    m = VERSION_RE.search(shown)
    return m.group(1) if m else None


head_version = manifest_version("HEAD:" + VERSION_FILE)
main_version = manifest_version("origin/main:" + VERSION_FILE)
if head_version is None or main_version is None:
    sys.exit(0)  # can't compare: fail open
if head_version != main_version:
    sys.exit(0)  # version already bumped on top of main: no re-increment

print(
    "Push blocked: it would publish functional changes without a plugin "
    f"version bump ({', '.join(functional)}). Bump the version in "
    f"{VERSION_FILE} (mirror in `.agents/plugins/marketplace.json` and "
    "`muse-dev/README.md`): patch (`0.0.x`) for fixes, minor (`0.x.0`) for "
    "new backward-compatible skills/commands/hooks/servers, major (`x.0.0`) "
    "for breaking changes — commit the bump, then re-push. Docs-only and "
    "other non-functional changes need no version bump.",
    file=sys.stderr,
)
sys.exit(2)
