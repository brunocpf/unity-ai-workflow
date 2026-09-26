#!/usr/bin/env python3
"""Verify owned staged C# without rewriting or staging user files. Run at repo root."""
from pathlib import Path
import subprocess
import sys


def git_names(*args):
    return [x for x in subprocess.check_output(["git", *args]).decode("utf-8").split("\0") if x]


def main():
    paths = git_names("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    paths = [p for p in paths if p.endswith(".cs") and p.startswith(("Assets/Game/", "tooling/"))]
    paths = [p for p in paths if not p.endswith((".g.cs", ".generated.cs"))]
    if not paths:
        return 0
    # Formatting tools read the working tree. Do not falsely certify a different index snapshot.
    partial = git_names("diff", "--name-only", "-z", "--", *paths)
    if partial:
        print("Selected C# has unstaged edits. Stage the intended whole files or validate the index in a separate worktree:", *partial, sep="\n")
        return 1
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())
    quality = root / "tooling/quality/check.py"
    if not quality.is_file():
        print("Bootstrap must install tooling/quality/check.py; refusing whitespace-only validation.")
        return 1
    return subprocess.run([sys.executable, str(quality), "--root", str(root), *paths], cwd=root).returncode


if __name__ == "__main__":
    sys.exit(main())
