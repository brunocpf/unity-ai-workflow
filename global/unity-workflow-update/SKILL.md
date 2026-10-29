---
name: unity-workflow-update
description: Check, assess or update the Unity AI workflow installed in the current project. Compare a candidate kit with the project's version, decide which changes apply, preserve local decisions and keep kit updates separate from game or Unity/package migrations.
---

The locally cached candidate kit is at `{{KIT_ROOT}}`. Read its `references/workflow-updates.md`. The current game's `.unity-workflow/installation.json`, local standards, native locks, project docs and ADRs describe what's installed; don't assume the global candidate is newer or suitable.

For a request about new upstream changes, look at `https://github.com/brunocpf/unity-ai-workflow` and fetch a candidate into a separate temporary checkout at an exact commit. Don't change the installed cache or pull into the game. The bundled cache works offline; if upstream is unavailable, say you couldn't check for newer versions.

Run the candidate's `install.py assess --target <absolute-project-path>` with Python 3.9+. Read the changed references/examples and the affected project code; decide for each change whether it applies now, later, not at all, or needs a separate migration, and why. The file list alone can't decide that. Put the decisions in the PR or final response; no separate upgrade report.

Checking/reviewing stops with the assessment. When updating is requested, do a dry run first, keep project exceptions, apply the update and run the project's checks. If the candidate conflicts with the project, defer that version or record the exception in an ADR before applying it. Engine/package/save migrations need their own request and tests.

For a global-only update, no game is needed: run the candidate's `install.py install-global` and `check-global`, and report the installed version. Global updates never change existing projects. If a project has no installation manifest, inspect how the kit was adopted manually instead of guessing or overwriting it.
