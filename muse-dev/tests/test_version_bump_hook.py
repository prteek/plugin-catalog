#!/usr/bin/env python3
"""Focused checks for the version-bump PreToolUse hook (push gate).

Run: `python3 test_version_bump_hook.py` (stdlib only, exit 0 = pass).
Builds throwaway git repos under $TMPDIR; nothing touches the real repo.
The hook never pushes; it only inspects what a push would publish.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "version_bump_pretooluse.py"
PLUGIN_JSON = '{\n  "name": "muse-dev",\n  "version": "0.3.0"\n}\n'


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True)


def make_repo(*, deployed: bool = True) -> Path:
    repo = Path(tempfile.mkdtemp(prefix="version-hook-"))
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "test")
    (repo / "muse-dev" / ".muse-plugin").mkdir(parents=True)
    (repo / "muse-dev" / ".muse-plugin" / "plugin.json").write_text(PLUGIN_JSON)
    (repo / "muse-dev" / "README.md").write_text("# muse-dev\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    if deployed:
        # Pretend the init commit is the deployed main on GitHub.
        git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    return repo


def commit_all(repo: Path, msg: str) -> None:
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", msg)


def run_hook(command: str, repo: Path) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items()
           if k not in ("VIRTUAL_ENV", "MUSE_PROJECT_DIR", "CLAUDE_PROJECT_DIR")}
    event = {"hook_event_name": "PreToolUse",
             "cwd": str(repo),
             "tool_input": {"command": command}}
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event),
                          capture_output=True, text=True, env=env)


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        check.failed = True


check.failed = False

# Commits are no longer gated — only pushes are.
repo = make_repo()
(repo / "muse-dev" / "skills").mkdir(exist_ok=True)
(repo / "muse-dev" / "skills" / "new.md").write_text("skill\n")
git(repo, "add", "-A")
check("commit with unbumped functional change passes",
      run_hook("git commit -m 'new skill'", repo).returncode == 0)
check("non-git command passes",
      run_hook("quarto render report.qmd", repo).returncode == 0)

# Nothing to publish beyond docs: push passes.
repo_docs = make_repo()
(repo_docs / "muse-dev" / "README.md").write_text("# muse-dev\n\nMore docs.\n")
commit_all(repo_docs, "docs")
check("docs-only push passes without bump",
      run_hook("git push", repo_docs).returncode == 0)

# Functional changes on top of the deployed version, no bump: blocked.
repo = make_repo()
(repo / "muse-dev" / "skills").mkdir(exist_ok=True)
(repo / "muse-dev" / "skills" / "new.md").write_text("skill\n")
commit_all(repo, "new skill")
r = run_hook("git push origin HEAD", repo)
check("unbumped functional push is blocked", r.returncode == 2)
check("block message names the file and the fix",
      "muse-dev/skills/new.md" in r.stderr and "re-push" in r.stderr)

# Same range with a bumped version: passes, including follow-up work.
(repo / "muse-dev" / ".muse-plugin" / "plugin.json").write_text(
    PLUGIN_JSON.replace("0.3.0", "0.4.0"))
commit_all(repo, "bump to 0.4.0")
(repo / "muse-dev" / "skills" / "extra.md").write_text("skill\n")
commit_all(repo, "more work")
check("no re-increment once version is ahead of main",
      run_hook("git push", repo).returncode == 0)

# Chained push commands are still gated.
repo2 = make_repo()
(repo2 / "muse-dev" / "hooks").mkdir(exist_ok=True)
(repo2 / "muse-dev" / "hooks" / "x.py").write_text("# hook\n")
commit_all(repo2, "hook")
check("chained git push is blocked",
      run_hook("make docs && git push", repo2).returncode == 2)

# Rehearsals and branch deletions push no code.
check("dry-run push passes",
      run_hook("git push --dry-run", repo2).returncode == 0)
check("branch deletion passes",
      run_hook("git push origin --delete old-branch", repo2).returncode == 0)

# No main ref at all (offline / no remote): fail open.
repo4 = make_repo(deployed=False)
(repo4 / "muse-dev" / "skills").mkdir(exist_ok=True)
(repo4 / "muse-dev" / "skills" / "new.md").write_text("skill\n")
commit_all(repo4, "new skill")
check("passes without bump when main is unknown",
      run_hook("git push", repo4).returncode == 0)

sys.exit(1 if check.failed else 0)
